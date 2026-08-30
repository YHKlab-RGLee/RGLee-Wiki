# 문서 품질 관리

품질 시스템은 결정적 검사와 과학적 review를 분리한다. `check`와 `report`는 파일을 쓰지 않으며, `sync`와 `review`만 `documents.yaml`을 갱신한다.

## 변경 분류

| 변경 | review 영향 |
| --- | --- |
| Navigation 순서·label | 없음. `check`와 strict build만 실행한다. |
| H1·description·경로·index link | presentation hash만 바뀐다. 기존 과학 review를 보존한다. |
| H2·H3 제목·번호 | 정규화된 목차가 같으면 보존하고, 논리 구조가 바뀌면 `outline` review를 요구한다. |
| 과학 본문·수식·수치·인용 | `full` review를 요구한다. |

각 문서는 `source`, `content`, `outline`, `presentation` hash를 갖는다. `content`는 front matter와 heading을 제외한 과학 본문, `outline`은 표시 번호를 제거한 H2·H3 순서, `presentation`은 경로·H1·metadata를 나타낸다.

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

## Review

새 article 또는 과학 내용 변경은 `full` review를 사용한다. 과학 내용은 같고 목차 논리만 바뀌면 `outline` review를 사용한다. Navigation과 presentation 변경에는 읽기 review를 실행하지 않는다.

`full` review는 현재 `pass` article에서 peer baseline을 자동으로 선택한다. 같은 topic group에 두 문서 이상이 있으면 그 집합을 사용하고, 부족하면 같은 scientific domain, 다시 부족하면 전체 article로 넓힌다. 대상의 본문 글자 수와 설명 요소 합계가 peer 평균의 80% 이상이어야 원자적 review를 기록할 수 있다. 설명 요소는 그림·표·display equation·fenced code block의 합이다. 수동 비교 문서 선택과 반복 동기화는 필요하지 않다.

`refs/quality/assessment-template.yaml`은 `full`, `refs/quality/outline-assessment-template.yaml`은 `outline` review에 사용한다. 작업용 파일에 복사하여 각 criterion의 0/1/2 rating, 근거, 위치와 이유를 적는다.

```bash
./quality.sh sync
./quality.sh benchmark docs/path/page.md
./quality.sh review docs/path/page.md --assessment /tmp/page-assessment.yaml
./quality.sh check --all
./build.sh build
```

Full review는 목차·논리, 과학적 근거, 설명의 이해 가능성을 원자적 criterion으로 평가한다. 각 영역 75%, 전체 80% 이상이어야 하며 critical criterion의 0점, publication compliance 실패 또는 F1–F5 강제 수정 조건은 점수와 관계없이 `revise`이다. Outline review는 목차와 읽기 흐름에 관련된 criterion 및 compliance만 평가하며 분량 gate를 다시 실행하지 않는다.

## Registry

`documents.yaml`에는 현재 문서별 derived metadata와 compact current attestation만 저장한다. 평가 입력의 상세 근거는 review 시 검증하지만 registry에는 점수·영역 결과·compliance·강제 수정 여부·결론만 보관하여 크기를 제한한다. 이전 snapshot과 삭제 record는 중복 저장하지 않고 Git history를 사용한다. Rubric version이 바뀌면 해당 version의 review가 필요하다.

## 명령

```bash
./quality.sh sync              # 명시적으로 registry 갱신
./quality.sh benchmark ...     # read-only full-review coverage 사전 검사
./quality.sh review ...        # current review 기록
./quality.sh check --all       # read-only 전체 검사
./quality.sh check --changed   # read-only 변경 문서 검사와 전체 nav 검사
./quality.sh check-nav         # read-only navigation 전용 검사
./quality.sh report            # read-only 요약
```
