## 우선순위 업데이트

| 순위 | 문서 | 중요도 | 상태 | 진행 내용 |
|------|------|--------|------|-----------|
| 1 | Stream_Format.md | 🔴 | 🔶 부분 | Meta Node에서 STREAM_START/END, TID 폭 정의. 스트림 조합 규칙은 미작성 |
| 2 | Literal 표현 | 🔴 | ✅ 해결 | **Quantity Node 0x32 UTF16** (Length 2워드 + Payload N워드) |
| 3 | Temporal 체계 | 🟠 | ✅ 해결 | **Quantity Node 0x30 초단위, 0x31 밀리초단위** |
| 4 | Collection 구조 | 🟠 | ✅ 해결 | **Group Edge** (AND/OR/XOR/LIST/SET/RANGE/PAIR) |
| 5 | SIDX Registry | 🟠 | ❌ 미해결 | 실제 동사/속성 ID 할당 없음 |
| 6 | TID 관리 | 🟡 | 🔶 부분 | STREAM_START에서 폭(16/32/64) 정의. 할당 규칙은 미정 |
| 7 | 인코딩 규칙 | 🟡 | ❌ 미해결 | 바이트 오더 등 미명시 |
| 8 | Modality 정비 | 🟡 | 🔶 부분 | Full Verb Edge 참여자 19비트(+TMP, +EXT), 한정자 27비트 |

---

## 요약

| 상태 | 개수 | 항목 |
|------|------|------|
| ✅ 완전 해결 | **4** | Literal, Temporal, Collection, (+RGBA 0x33 보너스) |
| 🔶 부분 해결 | 3 | Stream, TID, Modality |
| ❌ 미해결 | 2 | SIDX Registry, 인코딩 규칙 |

---

## 오늘 추가된 것

| 타입 | 코드 | 내용 |
|------|------|------|
| Meta Node | - | 스트림 제어 (STREAM_START/END, VERSION, CREATOR 등) |
| Group Edge | 0 000 111 000 | 집합/그룹 (7개 타입) |
| Quantity 0x30 | TIMESTAMP_SEC | Unix timestamp 초단위 |
| Quantity 0x31 | TIMESTAMP_MS | Unix timestamp 밀리초단위 |
| Quantity 0x32 | UTF16 | 문자열 리터럴 |
| Quantity 0x33 | RGBA | 32비트 색상 |

---

## 다음 우선순위 제안

**1. Stream_Format.md (1번)** - 스트림 조합 규칙 완성

또는

**2. 인코딩 규칙 (7번)** - Big Endian 명시 등 상호운용성

어느 쪽 먼저 할까요?