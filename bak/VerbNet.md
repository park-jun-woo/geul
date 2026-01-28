## VerbNet 상세 구조

### 1. 기본 정보

| 항목 | 값 |
|------|-----|
| 버전 | 3.4 (최신) |
| 클래스 수 | 329개 |
| 동사 수 | 5,300+ |
| 형식 | XML |
| 기반 | Levin (1993) 분류 |

---

### 2. 클래스 구조 예시

```xml
<VNCLASS ID="give-13.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  
  <!-- 멤버 동사들 -->
  <MEMBERS>
    <MEMBER name="give" wn="give%2:40:00"/>
    <MEMBER name="hand" wn="hand%2:40:00"/>
    <MEMBER name="pass" wn="pass%2:40:01"/>
  </MEMBERS>
  
  <!-- 의미역 -->
  <THEMROLES>
    <THEMROLE type="Agent">
      <SELRESTRS>
        <SELRESTR Value="+" type="animate"/>
      </SELRESTRS>
    </THEMROLE>
    <THEMROLE type="Theme"/>
    <THEMROLE type="Recipient">
      <SELRESTRS>
        <SELRESTR Value="+" type="animate"/>
      </SELRESTRS>
    </THEMROLE>
  </THEMROLES>
  
  <!-- 통사 프레임 -->
  <FRAMES>
    <FRAME>
      <DESCRIPTION>NP V NP PP.recipient</DESCRIPTION>
      <EXAMPLES>
        <EXAMPLE>Mary gave the book to John.</EXAMPLE>
      </EXAMPLES>
      <SYNTAX>
        <NP value="Agent"/>
        <VERB/>
        <NP value="Theme"/>
        <PREP value="to"/>
        <NP value="Recipient"/>
      </SYNTAX>
      <SEMANTICS>
        <PRED value="has_possession">
          <ARGS>
            <ARG type="Event" value="start(E)"/>
            <ARG type="ThemRole" value="Agent"/>
            <ARG type="ThemRole" value="Theme"/>
          </ARGS>
        </PRED>
        <PRED value="has_possession">
          <ARGS>
            <ARG type="Event" value="end(E)"/>
            <ARG type="ThemRole" value="Recipient"/>
            <ARG type="ThemRole" value="Theme"/>
          </ARGS>
        </PRED>
      </SEMANTICS>
    </FRAME>
  </FRAMES>
  
  <!-- 하위 클래스 -->
  <SUBCLASSES>
    <VNSUBCLASS ID="give-13.1-1">
      ...
    </VNSUBCLASS>
  </SUBCLASSES>
  
</VNCLASS>
```

---

### 3. 클래스 번호 체계 (Levin 기반)

| 번호 | 유형 | 예시 클래스 |
|------|------|------------|
| 9 | Putting | put-9.1, spray-9.7 |
| 10 | Removing | remove-10.1, banish-10.2 |
| 11 | Sending | send-11.1, bring-11.3 |
| 13 | Giving/Getting | give-13.1, get-13.5.1 |
| 17-18 | Throwing | throw-17.1 |
| 21-22 | Cutting/Combining | cut-21.1, amalgamate-22.2 |
| 26 | Adjusting | adjust-26.9 |
| 29 | Characterize | appoint-29.1, dub-29.3 |
| 30 | Perception | see-30.1, peer-30.3 |
| 31 | Psych | amuse-31.1, admire-31.2 |
| 32-33 | Desire | want-32.1, long-32.2 |
| 35-37 | Communication | say-37.7, tell-37.2 |
| 38 | Sounds | animal_sounds-38 |
| 40 | Body States | breathe-40.1.2 |
| 43-45 | Change of State | break-45.1, bend-45.2 |
| 47-51 | Motion | run-51.3.2, escape-51.1 |
| 58-109 | 확장 (Korhonen) | become-109.1 |

---

### 4. 의미역 (Thematic Roles)

**VerbNet 표준 의미역:**

| 역할 | 정의 | 예시 |
|------|------|------|
| **Agent** | 의도적 행위자 | "John kicked the ball" |
| **Patient** | 상태 변화 대상 | "The window broke" |
| **Theme** | 이동/기술 대상 | "John gave **the book**" |
| **Experiencer** | 경험/인지 주체 | "John feared the dog" |
| **Stimulus** | 경험 유발 원인 | "The dog frightened John" |
| **Recipient** | 수령자 | "gave it **to Mary**" |
| **Beneficiary** | 수익자 | "baked a cake **for her**" |
| **Instrument** | 도구 | "cut **with a knife**" |
| **Location** | 장소 | "put it **on the table**" |
| **Source** | 출발점 | "came **from home**" |
| **Destination** | 도착점 | "went **to school**" |
| **Goal** | 목표 | "aimed **at the target**" |
| **Attribute** | 속성 | "painted it **red**" |
| **Material** | 재료 | "made **of wood**" |
| **Product** | 결과물 | "carved **a statue**" |
| **Topic** | 주제 | "talked **about art**" |
| **Predicate** | 술어 | "consider him **a fool**" |

---

### 5. 선택 제약 (Selectional Restrictions)

```xml
<SELRESTRS>
  <SELRESTR Value="+" type="animate"/>   <!-- 생물 -->
  <SELRESTR Value="+" type="human"/>     <!-- 인간 -->
  <SELRESTR Value="+" type="concrete"/>  <!-- 구체물 -->
  <SELRESTR Value="+" type="solid"/>     <!-- 고체 -->
  <SELRESTR Value="+" type="location"/>  <!-- 장소 -->
</SELRESTRS>
```

| 제약 | 의미 |
|------|------|
| +animate | 생물 |
| +human | 인간 |
| +machine | 기계 |
| +concrete | 구체적 |
| +solid | 고체 |
| +location | 장소 |
| +organization | 조직 |
| +comestible | 먹을 수 있는 |

---

### 6. 의미 술어 (Semantic Predicates)

```xml
<SEMANTICS>
  <PRED value="motion">
    <ARGS>
      <ARG type="Event" value="during(E)"/>
      <ARG type="ThemRole" value="Theme"/>
    </ARGS>
  </PRED>
  <PRED value="location">
    <ARGS>
      <ARG type="Event" value="end(E)"/>
      <ARG type="ThemRole" value="Theme"/>
      <ARG type="ThemRole" value="Destination"/>
    </ARGS>
  </PRED>
</SEMANTICS>
```

**주요 술어:**

| 술어 | 의미 |
|------|------|
| motion | 이동 |
| location | 위치 |
| has_possession | 소유 |
| transfer | 전달 |
| cause | 사역 |
| state | 상태 |
| contact | 접촉 |
| exert_force | 힘 가함 |
| emotional_state | 감정 상태 |
| perceive | 인지 |

**시간 함수:**

| 함수 | 의미 |
|------|------|
| start(E) | 이벤트 시작 |
| during(E) | 이벤트 진행 중 |
| end(E) | 이벤트 종료 |
| result(E) | 결과 상태 |

---

### 7. 계층 구조

```
give-13.1 (최상위)
│
├── give-13.1-1 (하위)
│   └── give-13.1-1-1 (더 하위)
│
└── contribute-13.2 (형제 클래스)
```

**상속:**
- 하위 클래스는 상위 클래스의 모든 속성 상속
- 추가 제약이나 프레임만 명시

---

### 8. WordNet 매핑

```xml
<MEMBER name="give" wn="give%2:40:00 give%2:40:03"/>
```

| VerbNet | WordNet |
|---------|---------|
| give-13.1 | give%2:40:00 |
| run-51.3.2 | run%2:38:00 |

---

### 9. GEUL 활용 방안

**현재 VerbNet:**
```
give-13.1
  Agent → Recipient: Theme
  PRED: has_possession(start, Agent, Theme)
        has_possession(end, Recipient, Theme)
```

**GEUL 변환:**
```
[Verb: give-13.1]  // VerbNet 클래스 ID 사용
[MRS: give-13.1]
  AGT: John_sidx
  RCP: Mary_sidx
  THM: book_sidx
```

---

### 10. 통계

| 항목 | 수량 |
|------|------|
| 최상위 클래스 | 274개 |
| 전체 클래스 | 329개 |
| 의미역 | 30개 |
| 통사 프레임 | ~1,600개 |
| 의미 술어 | ~70개 |
| 동사 lemma | 5,300+ |
