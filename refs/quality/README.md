# 문서 품질 관리

이 디렉터리는 `docs/` 아래 Markdown 문서의 자동 계량값과 근거 기반 읽기 평가를 보관한다. 원시 계량, 과학적 채점과 게시 준수 조건을 서로 분리한다.

## 기록 파일

- `rubric.yaml`: A–C 채점 항목, D 준수 조건과 강제 `revise` 규칙
- `assessment-template.yaml`: 신규 평가 입력 양식
- `documents.yaml`: 문서별 metadata, 자동 계량값, 현재 평가와 이력

`documents.yaml`은 직접 고치지 않고 `quality.sh`로 관리한다. article의 현재 평가는 하나의 체크리스트 형식만 사용한다. 아직 평가하지 않았거나 본문 변경으로 평가가 무효화된 article은 `review: null`이며 보고서에서 `pending`으로 표시한다.

`kind: article`인 문서만 정량 비교와 A–C 읽기 평가를 수행한다. `home`과 `index`는 navigation hub이므로 registry와 automatic check에는 포함하되, 읽기 평가 상태는 `excluded`로 기록한다.

## 자동 계량

`quality.sh sync`는 다음 값을 결정적으로 계산한다.

- `characters`: 참고문헌, fenced code와 Markdown 표기를 제외한 본문 글자 수
- `explanatory_elements.total`: 그림, 표, 독립 수식과 fenced code block의 합계
- 구성 요소별 `figures`, `tables`, `equations`, `code_blocks`
- source hash, 내부 링크와 기본 Markdown 구조에 대한 자동 검사

이 값은 최소 설명량을 확인하는 통과 조건이지 과학적 품질 점수가 아니다. 수식을 잘게 나누거나 문장을 늘려도 과학적 정확성·논리·이해 가능성이 자동으로 높아지지는 않는다.

## A–C 근거 기반 채점

LLM은 최종 점수를 직접 입력하지 않는다. 각 항목에 다음 정보를 제출한다.

- `rating`: `0`, `1`, `2`
- `evidence`: 판정에 사용한 구체적인 사실
- `locations`: 해당 절, 수식, 표 또는 문단 위치
- `reason`: 충족 여부와 보완점을 설명하는 한국어 문장

세 영역은 다음과 같다.

| 영역 | 배점 | 핵심 질문 |
| --- | ---: | --- |
| A. 목차와 논리적 구성 | 35 | 개념 의존 순서와 일반식에서 근사식으로 가는 전개가 타당한가? |
| B. 논문과 과학적 근거 | 35 | 주장을 직접 확인한 독립 문헌이 실제로 지지하는가? |
| C. 설명의 이해 가능성 | 30 | 독자가 개념, 수식, 인과관계와 근사의 손실을 따라갈 수 있는가? |

각 항목의 점수는 코드가 `배점 × rating / 2`로 계산한다. 문서 종류에 적용되지 않는 항목은 채점 대상에서 제외하고 해당 영역 안에서 배점을 다시 정규화한다.

## D 게시 준수 조건

D1–D6은 점수가 아니다. 하나라도 `fail`이면 총점과 관계없이 `revise`이다.

- D1 문서 구조
- D2 언어와 용어
- D3 수식과 정량 표현
- D4 표와 그림
- D5 인용과 참고문헌
- D6 링크와 저장소 상태

형식을 잘 지켜도 과학적 설명의 부족을 상쇄할 수 없으며, 과학적 내용이 좋아도 게시 요건을 위반한 문서는 통과하지 않는다.

## 강제 revise

`rubric.yaml`의 F1–F5 가운데 하나라도 해당하면 `forced_revise`에 근거와 위치를 기록한다. 또한 A4, B1, B2, B3, C3 또는 C5가 적용 대상이면서 0점이면 자동으로 `revise`이다.

평가자는 다음 세 질문에도 답해야 한다.

1. 문서의 개념 의존 순서는 무엇인가?
2. 독자가 가장 먼저 막힐 가능성이 큰 지점은 어디인가?
3. 이 문서를 revise로 판정할 가장 강한 근거는 무엇인가?

## 통과 기준

평가 대상인 article 문서는 다음을 모두 만족해야 `pass`이다.

1. 자동 검사가 통과한다.
2. 글자 수와 설명 요소가 비교 문서 평균의 80% 이상이다.
3. A–C 총점이 80/100 이상이다.
4. A, B, C가 각각 75% 이상이다.
5. 핵심 항목의 0점이 없다.
6. D1–D6이 모두 `pass`이다.
7. 적용되는 강제 `revise` 규칙이 없다.

## 평가 절차

```text
sync
  → 같은 종류의 관련 문서 두 개 이상과 정량 비교
  → 문서·근거 원문·제목 계층을 읽음
  → assessment-template.yaml을 임시 파일로 작성
  → strict build를 포함한 D 준수 조건 확인
  → review --assessment로 코드가 점수와 상태 계산
  → check로 registry와 현재 문서 일치 확인
```

평가 파일은 작업용 입력이므로 registry에 경로를 저장하지 않는다. 판정 내용 전체가 `documents.yaml`의 현재 review에 보존된다. 동일한 현행 기준으로 재평가하거나 문서 변경으로 평가가 무효화되면 직전 기록을 history에 보존한다.

## 명령

```bash
./quality.sh sync
./build.sh build
./quality.sh review docs/path/page.md \
  --assessment /tmp/page-assessment.yaml \
  --reference docs/path/related-a.md \
  --reference docs/path/related-b.md
./quality.sh check docs/path/page.md
./quality.sh report
```
