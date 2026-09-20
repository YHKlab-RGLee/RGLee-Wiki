# 문서 품질 관리

품질 시스템은 결정적 검사와 과학적 review를 분리한다. `check`, `report`, `benchmark`는 파일을 쓰지 않는다. `sync`는 `documents.yaml`을 갱신하고, `review`는 평가 근거 파일과 registry를 기록한다.

## 변경 분류

| 변경 | review 영향 |
| --- | --- |
| Navigation 순서·label | 없음. `check`와 strict build만 실행한다. |
| H1·description·경로·index link | presentation hash만 바뀐다. 기존 과학 review를 보존한다. |
| H2·H3 제목·번호 | 정규화된 목차가 같으면 보존하고, 논리 구조가 바뀌면 `outline` review를 요구한다. |
| 과학 본문·수식·수치·인용 | `full` review를 요구한다. |

각 문서는 `source`, `content`, `outline`, `presentation` hash를 갖는다. `content`는 front matter와 heading을 제외한 과학 본문, `outline`은 표시 번호를 제거한 H2·H3 순서, `presentation`은 경로·H1·metadata를 나타낸다.

미완료 `full` 검토는 후속 제목 수정이나 반복 `sync`로 `outline`로 낮추지 않는다. 실패 근거는 다음 검토까지 보존하고, 변경 전 통과 기록은 `last_pass`로 남긴다. Outline 검토에는 기존 과학 검토를 `scientific_review`로 연결하여 목차 검토가 과학 내용을 새로 검증한 것으로 오인되지 않게 한다.

현재 content hash는 Markdown 본문 순서와 링크 목적지도 포함한다. 따라서 절 이동이나 본문 링크 변경은 보수적으로 `full`로 분류될 수 있다. 이미지 파일 자체의 변경과 링크 대상 의미의 동등성은 자동 판정하지 못한다. 관련 변경에서는 참조 문서와 그림 의미를 직접 확인하고 필요한 과학 검토를 수행한다. 자동 분류를 근거로 이 검토를 생략하지 않는다.

## 결정적 검사

`./quality.sh check-nav`는 navigation 규칙만 검사한다. `./quality.sh check --changed`는 현재 작업에서 바뀐 Markdown과 전체 navigation을, `./quality.sh check --all`은 게시 전 전체 wiki 상태를 읽기 전용으로 검사한다.

전체 검사는 다음을 확인한다.

- 고정 domain 이름과 순서, 모든 Markdown 문서의 navigation 포함 여부
- navigation, H1과 index link에 수동 순서 번호가 없는지
- front matter description, H1–H3 깊이와 heading 번호 형식
- 내부 링크, 기본 인용 번호와 참고문헌 범위
- registry hash와 현재 파일의 일치
- article의 current `pass` review 또는 index/home의 `excluded` 상태

엄격한 MkDocs build는 `./build.sh build`가 이어서 실행한다.

## 범위를 지정한 동기화

`./quality.sh sync <문서 경로> ...`는 지정한 문서의 기록만 갱신하고, 나머지 문서의 metadata와 review는 보존한다. 인자 없는 `sync`는 기존처럼 전체 문서를 동기화한다. 메인은 완료된 작업 범위의 경로를 명시한다.

- 신규·수정 문서는 현재 경로를 지정한다. 함께 수정한 index 등도 포함한다.
- 삭제는 registry에 남아 있는 이전 경로를 지정한다.
- 이동은 이전 경로와 새 경로를 함께 지정한다. 기존과 같이 내용·목차가 일치하는 유일한 이동 후보의 검토를 이어받으며, 범위 밖의 기록은 이동 후보로 사용하지 않는다.
- 존재하지 않고 기존 기록도 없는 경로나 `docs/` 밖의 경로는 쓰기 전에 오류로 처리한다.
- 이전 schema/hash 형식의 registry는 전체 동기화로 먼저 갱신한다.

범위 지정은 기록의 갱신 범위를 제한한다. 메인은 registry 쓰기를 계속 직렬화하고, 검토 중인 문서의 버전을 고정한다. 전체 navigation 검사와 strict build의 범위는 바꾸지 않는다.

## Review

새 article 또는 과학 내용 변경은 `full` review를 사용한다. 과학 내용은 같고 목차 논리만 바뀌면 `outline` review를 사용한다. Navigation과 presentation 변경에는 읽기 review를 실행하지 않는다.

`full` review는 현재 `pass` article에서 peer baseline을 자동으로 선택한다. 같은 topic group에 두 문서 이상이 있으면 그 집합을 사용하고, 부족하면 같은 scientific domain, 다시 부족하면 전체 article로 넓힌다. 대상의 본문 글자 수와 설명 요소 합계가 peer 평균의 80% 이상이어야 원자적 review를 기록할 수 있다. 설명 요소는 그림·표·display equation·fenced code block의 합이다. 수동 비교 문서 선택과 반복 동기화는 필요하지 않다.

`refs/quality/assessment-template.yaml`은 `full`, `refs/quality/outline-assessment-template.yaml`은 `outline` review에 사용한다. 작업용 파일에 복사하여 각 criterion의 0/1/2 rating, 근거, 위치와 이유를 적는다.

```bash
./quality.sh sync docs/path/page.md
./quality.sh benchmark docs/path/page.md
./quality.sh review docs/path/page.md --assessment experiment/page-assessment.yaml
./build.sh changed
```

Full review는 목차·논리, 과학적 근거, 설명의 이해 가능성을 원자적 criterion으로 평가한다. 각 영역 75%, 전체 80% 이상이어야 하며 critical criterion의 0점, publication compliance 실패 또는 F1–F5 강제 수정 조건은 점수와 관계없이 `revise`이다. Outline review는 목차와 읽기 흐름에 관련된 criterion 및 compliance만 평가하며 분량 gate를 다시 실행하지 않는다.

## Registry

`documents.yaml`에는 문서별 derived metadata와 compact attestation을 저장한다. 새 검토의 상세 근거는 `refs/quality/evidence/<hash>.yaml`에 보존하고 registry의 `evidence_path`로 연결한다. 파일에는 평가한 문서 hash, rubric version, criterion별 근거·위치·이유를 기록한다. 변경되지 않은 주장의 검토 근거를 재사용할 때만 해당 파일을 읽는다. 과거 검토에 없던 상세 근거는 소급 생성하지 않는다. 이전 이력은 Git으로 관리한다. Rubric version이 바뀌면 해당 version의 review가 필요하다.

작업의 문맥 범위는 `AGENTS.md`의 표를 따른다. `report`는 저장된 상태를 출력하고, `benchmark`는 동기화 없이 현재 파일을 읽기 전용으로 측정한다. 최종 검사는 담당 스킬이 한 번 실행하며 호출한 스킬에서 반복하지 않는다. 전체 게시와 품질 도구 변경에는 `./build.sh build`를 사용한다. 정량 기준 충족만으로 내용의 정확성이나 설명의 충분성이 입증되지는 않는다.

검토 모델은 `review.model`의 `name`, `reasoning_effort`, `source`에 기록한다. 알 수 없는 값은 빈 문자열로 두며, 기존 검토에 현재 세션의 모델을 소급해서 넣지 않는다. `source`에는 확인 경로(예: 사용자 제공은 `user_declared`)를 적는다. Full/outline 평가 파일의 선택 항목 `model`을 통해 입력하면 registry와 상세 근거에 함께 저장된다. 생략한 새 검토는 빈 값으로 기록하며 이전 검토의 모델을 자동 상속하지 않는다. 일반 동기화는 기존 모델 정보를 보존하고, 재검토 대기로 바뀌면 이전 정보는 `last_pass`에 보존한다. 이 항목은 검토 수행 모델을 뜻하며 작성 모델이나 품질 점수 판정에는 사용하지 않는다.

## 명령

```bash
./quality.sh sync              # 전체 registry 갱신
./quality.sh sync docs/path/page.md  # 지정 문서만 갱신
./quality.sh benchmark ...     # read-only full-review coverage 사전 검사
./quality.sh review ...        # current review 기록
./quality.sh check --all       # read-only 전체 검사
./quality.sh check --changed   # read-only 변경 문서 검사와 전체 nav 검사
./quality.sh check-nav         # read-only navigation 전용 검사
./quality.sh report            # read-only 요약
./quality.sh report --changed  # 변경 Markdown의 저장된 상태만 출력
./quality.sh report docs/path/page.md  # 지정 문서만 출력
```
