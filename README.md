# 연구형 과학·계산 위키

연구자가 지정한 advanced topic을 인터넷에서 조사하고, 독립적인 복수 출처와 과학 지식이 일치하는 주장만 정리하는 개인 위키이다. Device Physics, Solid-State Physics, Computational Science의 세 분야를 유지하며, 검증한 콘텐츠만 주제에 맞게 추가한다.

새 문서를 만들 때는 `AGENTS.MD`, `refs/format.md`, `docs/research-workflow.md`, `skills/research-and-write-wiki/SKILL.md`를 따른다. 실제 콘텐츠 작업에서 효과가 확인된 조사·검증 방법은 `docs/research-workflow.md`의 로그에 누적한다.

## 시작하기

Python 3.10 이상을 권장한다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

로컬 미리보기:

```bash
./build.sh serve
```

엄격한 프로덕션 빌드:

```bash
./build.sh build
```

생성된 사이트는 `site/`에 저장된다. 문서 구조와 작성 규칙은 위의 네 기준 문서를 따른다.
