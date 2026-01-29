## 우선순위 업데이트

| 순위 | 문서 | 중요도 | 상태 | 진행 내용 |
|------|------|--------|------|-----------|
| 1 | Stream_Format.md | 🔴 | 🔶 부분 | v0.1 초안 완성. TID 할당 4원칙, 패킷 순서 규칙 정립. 세부 조합 규칙 보완 필요 |
| 2 | Literal 표현 | 🔴 | ✅ 해결 | **Quantity Node 0x32 UTF16** (Length 2워드 + Payload N워드) |
| 3 | Temporal 체계 | 🟠 | ✅ 해결 | **Quantity Node 0x30 초단위, 0x31 밀리초단위** |
| 4 | Collection 구조 | 🟠 | ✅ 해결 | **Group Edge** (AND/OR/XOR/LIST/SET/RANGE/PAIR) |
| 5 | SIDX Registry | 🟠 | 🔶 부분 | **동사 ✅**: 13,767개 완료 (verbs.json). **속성 ❌**: PropCode 미할당 |
| 6 | TID 관리 | 🟡 | ✅ 해결 | TID 할당 4원칙(필수성/유일성/스코프/순방향), 순환참조 금지 |
| 7 | 인코딩 규칙 | 🟡 | ✅ 해결 | **Big Endian (Network Byte Order) 확정** |
| 8 | Modality 정비 | 🟡 | 🔶 부분 | Full Verb Edge 참여자 19비트(+TMP, +EXT), 한정자 27비트 |

---

## 요약

| 상태 | 개수 | 항목 |
|------|------|------|
| ✅ 완전 해결 | **5** | Literal, Temporal, Collection, TID, 인코딩 |
| 🔶 부분 해결 | 3 | Stream, SIDX Registry(속성만), Modality |
| ❌ 미해결 | 0 | - |

---

## SIDX Registry 상세

| 분류 | 상태 | 내용 |
|------|------|------|
| **동사** | ✅ 완료 | 13,767개, 68 sub_primitive 허프만 코딩, verbs.json |
| **속성** | ❌ 미할당 | Triple Edge PropCode (Wikidata P번호 매핑 필요) |
| **개체** | 🔶 구조만 | Entity Node Lane/Type 정의됨, 실제 개체 ID 미할당 |

---

## 1월 29일 추가/변경된 것

| 타입 | 코드 | 내용 |
|------|------|------|
| Meta Node | 0 000 000 | 스트림 제어 (STREAM_START/END, VERSION, CREATOR 등) |
| Group Edge | 0 000 111 000 | 집합/그룹 (7개 타입) |
| Context Edge | 1100000 100 | 세계관/출처/관점 (62개 타입) |
| Quantity 0x30 | TIMESTAMP_SEC | Unix timestamp 초단위 |
| Quantity 0x31 | TIMESTAMP_MS | Unix timestamp 밀리초단위 |
| Quantity 0x32 | UTF16 | 문자열 리터럴 |
| Quantity 0x33 | RGBA | 32비트 색상 |
| Verb Edge | v0.1 | Tiny/Short/Full 3단계 모드 |
| Entity SIDX | v0.1 | Lane 분기, 가변 워드 (3/5워드) |
| Stream Format | v0.1 | TID 4원칙, 순방향 참조 |
| 인코딩 규칙 | - | Big Endian 확정 |

---

## 다음 우선순위 제안

**1. Stream_Format.md 보완** - 세부 조합 규칙, 에러 처리

**2. PropCode 할당** - Wikidata 상위 속성 매핑 (P31, P279 등)

**3. Modality 정비** - Full Verb Edge 상세 명세 완성

어느 쪽 먼저 할까요?