# Meta Node 재설계 (v2 초안)

**작성일:** 2026-02-28
**상태:** 초안 (토론 결과 정리)
**대상:** grammar/meta-node/README.md 대체

---

## 1. 설계 원칙

- **단일 헤더:** 파일 포맷 관례를 따른다. Meta는 스트림 맨 앞에 한 번만 등장.
- **자기 서술 토큰:** Meta가 후속 토큰의 의미를 바꾸지 않는다. TID 폭(2케이스)만 예외.
- **최소 헤더:** 파싱 필수 정보만. CREATOR 등 부가 정보는 본문에서 GEUL로 표현.

---

## 2. 1st WORD 구조

```
┌──────────────┬──────┬─────┬───┬───┬──────┐
│   Prefix     │ MODE │ TID │ C │ M │ RSVD │
│   10비트     │  2   │  1  │ 1 │ 1 │  1   │
└──────────────┴──────┴─────┴───┴───┴──────┘
```

### MODE (2비트)

| MODE | 이름 | 설명 |
|------|------|------|
| 00 | File | 파일 헤더. EOF가 종료 |
| 01 | Stream Open | 스트림 시작. Close로 닫음 |
| 10 | Stream Close | 스트림 종료. 순수 종결자 |
| 11 | Reserved | 예약 |

### FLAGS

| 필드 | 비트 | 의미 |
|------|------|------|
| TID | 1 | 0=16bit(1워드), 1=32bit(2워드) |
| C | 1 | CREATED_AT 포함 |
| M | 1 | MODIFIED_AT 포함 |
| RSVD | 1 | 예약 (0) |

---

## 3. File (MODE=00)

```
1st: [Prefix 10][00][TID][C][M][0]
2nd: VERSION (Major 8 + Minor 8)
3rd~4th: CREATED_AT  ← C=1일 때 (Unix timestamp 32bit)
5th~6th: MODIFIED_AT ← M=1일 때 (Unix timestamp 32bit)

최소 2워드, 최대 6워드
```

파일 시스템 헤더와 동일. 모든 메타데이터를 앞에서 한 번 선언.
VERSION은 항상 존재 (하위 호환의 전제 조건).

---

## 4. Stream Open (MODE=01)

```
1st: [Prefix 10][01][TID][C][0][0]
2nd: VERSION (Major 8 + Minor 8)
3rd~4th: CREATED_AT  ← C=1일 때

최소 2워드, 최대 4워드
```

MODIFIED_AT은 스트림에서 의미 없음 (실시간이라 수정 시점 = 현재).

---

## 5. Stream Close (MODE=10)

```
1st: [Prefix 10][10][0000]

항상 1워드. 고정 토큰.
```

순수 종결자. 추가 데이터 없음. TCP FIN과 동일 역할.

---

## 6. VERSION 워드

```
┌──────────┬──────────┐
│  Major   │  Minor   │
│  8비트   │  8비트   │
└──────────┴──────────┘
```

- `0x0100` = v1.0
- `0x0201` = v2.1
- `0x0A05` = v10.5

---

## 7. CREATED_AT / MODIFIED_AT

- **형식:** 32비트 Unix timestamp (Big Endian)
- **기준:** 1970-01-01 00:00:00 UTC
- **범위:** 1970~2106년
- **워드:** 2워드 (상위 16bit + 하위 16bit)

---

## 8. Hex 값 정리

| 패킷 | 비트 | Hex | 워드 |
|------|------|-----|------|
| File(TID16, 타임스탬프 없음) | `0001 000 111 00 0 00 0` | 0x11C0 | 2 |
| File(TID16, C) | `0001 000 111 00 0 10 0` | 0x11C4 | 4 |
| File(TID16, C+M) | `0001 000 111 00 0 11 0` | 0x11C6 | 6 |
| File(TID32, C+M) | `0001 000 111 00 1 11 0` | 0x11CE | 6 |
| Stream Open(TID16) | `0001 000 111 01 0 00 0` | 0x11D0 | 2 |
| Stream Open(TID16, C) | `0001 000 111 01 0 10 0` | 0x11D4 | 4 |
| Stream Open(TID32) | `0001 000 111 01 1 00 0` | 0x11D8 | 2 |
| Stream Close | `0001 000 111 10 0 00 0` | 0x11E0 | 1 |

---

## 9. 스트림 구조 예시

### 9.1 최소 파일

```
[File Meta]        - 2워드 (0x11C0 + VERSION)
[... 패킷들 ...]
```

### 9.2 메타데이터 포함 파일

```
[File Meta]        - 6워드 (헤더 + VERSION + CREATED + MODIFIED)
[... 패킷들 ...]
```

### 9.3 스트림

```
[Stream Open]      - 2~4워드
[... 패킷들 ...]
[Stream Close]     - 1워드 (0x11E0)
```

### 9.4 전체 예시

```
"Apple이 Tesla를 인수했다" 파일:

1. File Meta (TID 16비트, CREATED_AT)
   0x11C4, 0x0100, 0x6978, 0xC900

2. Entity Node: Apple (TID=0x0001)
   [Entity 패킷...]

3. Entity Node: Tesla (TID=0x0002)
   [Entity 패킷...]

4. Verb Edge: acquire (TID=0x0100)
   [Verb 패킷...]

5. Event6 Edge: (Apple, acquire, Tesla)
   [Event6 패킷...]
```

---

## 10. 설계 근거

| 결정 | 이유 |
|------|------|
| 단일 헤더 | PNG/PDF/ELF 등 파일 포맷 관례. 파서가 첫 패킷만 읽으면 전체 맥락 파악 |
| File/Stream 분리 | 파일은 EOF로 종료, 스트림은 명시적 Close 필요. 사용 맥락이 다름 |
| VERSION 필수 | 하위 호환의 전제 조건. HTTP/1.1, PNG IHDR과 동일 |
| CREATOR 제외 | Entity + Triple Edge로 본문에서 표현 가능. "모든 것을 GEUL로" 원칙 |
| Stream Close 1워드 고정 | LLM 토큰으로서 항상 동일한 의미. 상태 의존 없음 |
| 32비트 타임스탬프 | 2106년까지 커버. 확장 필요시 RSVD 비트 활용 |
| TID 2케이스만 | 16bit(일반)와 32bit(대규모). LLM 컨텍스트 규모 대응에 충분 |

---

## 11. v1 대비 변경점

| 항목 | v1 (현행) | v2 (본 제안) |
|------|-----------|-------------|
| 구조 | 6개 독립 Type | MODE 기반 단일 헤더 |
| STREAM_END | 별도 Meta 패킷 | Stream Close (MODE=10) |
| CREATOR | Meta 내 4워드 EntityNode | 본문에서 GEUL로 표현 |
| VERSION | 별도 Meta 패킷 | 헤더 2nd WORD (필수) |
| CREATED_AT | 별도 Meta 패킷 | 헤더 FLAG (선택) |
| MODIFIED_AT | 별도 Meta 패킷 | 헤더 FLAG (File만) |
| 최소 크기 | 1워드 (STREAM_START만) | 2워드 (헤더 + VERSION) |
| 토큰 자기서술 | Meta가 해석 변경 가능 | TID 폭(2케이스)만 영향 |
