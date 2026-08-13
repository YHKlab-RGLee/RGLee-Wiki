---
title: "2.1. AI agents: LangChain and LangGraph"
description: LLM agent의 기본 동작, LangChain과 LangGraph의 역할, 핵심 기능, Python 사용법과 운영 시 주의사항을 설명
status: verified
last_verified: 2026-08-13
---

# 2.1. AI agents: LangChain and LangGraph

Large language model agent (LLM agent)는 언어 모형이 주어진 목표와 현재 상태를 바탕으로 다음 행동을 선택하고, 도구 실행 결과를 다시 관찰하면서 종료 조건까지 작업을 반복하는 시스템이다. 단일 LLM 호출이 주로 입력에서 응답을 한 번 생성한다면, agent는 **모형 호출–도구 실행–관찰–상태 갱신**을 하나의 제어 순환으로 묶는다. ReAct는 추론과 외부 행동을 번갈아 생성하는 대표적인 초기 형식이며, 이후 연구에서는 계획, 기억, 도구 사용과 환경의 feedback을 LLM agent의 주요 구성 요소로 정리한다.[1,2]

LangChain과 LangGraph는 이 순환을 서로 다른 추상화 수준에서 구현한다. LangChain은 모형·도구·agent loop를 빠르게 조립하는 고수준 framework이고, LangGraph는 상태와 제어 흐름을 graph로 직접 정의하는 저수준 orchestration framework이자 runtime이다. LangChain v1의 agent는 LangGraph 위에 구현되므로 둘은 배타적인 선택지가 아니다. 표준 agent는 LangChain으로 시작하고, 명시적인 분기·반복·승인·재개가 필요할 때 LangGraph로 제어 흐름을 확장할 수 있다.[3–5]

## 1. LLM agent의 기본 구조

### (1) 구성 요소와 동작 순서

Agent의 최소 구성은 목표를 해석하고 다음 행동을 고르는 **model**, 외부 세계를 읽거나 바꾸는 **tools**, 중간 결과를 보존하는 **state**, 반복과 종료를 관리하는 **control loop**이다. 장기 작업에서는 상태 저장, 오류 복구, 사람의 승인과 실행 기록이 이 최소 구조를 둘러싼다.[1,2,6]

| 단계 | 입력 | 동작 | 출력 또는 상태 변화 |
| --- | --- | --- | --- |
| 1. 목표 수신 | 사용자 요청, system prompt | 해결할 문제와 제약을 해석한다. | 초기 message와 작업 상태 |
| 2. 다음 행동 선택 | message, 도구 목록, 현재 상태 | 모형이 직접 답할지 특정 tool을 호출할지 정한다. | 응답 초안 또는 tool call |
| 3. 도구 실행 | tool 이름과 구조화된 인자 | 응용 코드가 API, DB, 계산 함수 등을 실행한다. | 관찰 결과 또는 오류 |
| 4. 상태 갱신 | 이전 상태와 관찰 결과 | message와 응용 상태에 결과를 기록한다. | 다음 순환의 입력 |
| 5. 반복 또는 종료 | 갱신된 상태, 종료 조건 | 추가 행동이 필요하면 2단계로 돌아가고 아니면 끝낸다. | 최종 응답과 실행 이력 |

여기서 “model이 tool을 호출한다”는 표현은 model process가 임의의 Python 함수를 직접 실행한다는 뜻이 아니다. 모형은 보통 호출할 도구 이름과 인자를 구조화된 출력으로 제안하고, agent runtime이 허용된 함수만 실제로 실행한 뒤 결과를 message로 돌려준다.[4,6,7]

### (2) Workflow와 agent의 구분

Workflow는 개발자가 단계와 분기를 미리 정한 절차이고, agent는 실행 중 모형이 다음 도구와 경로를 동적으로 선택하는 부분을 포함한다. 실제 응용은 둘을 섞는 경우가 많다. 예를 들어 입력 검증과 결제 승인은 결정론적 workflow로 고정하고, 여러 검색 도구 가운데 무엇을 쓸지는 agent가 고르게 할 수 있다.[2,5,8]

| 구분 | Workflow | Agent |
| --- | --- | --- |
| 다음 단계의 결정자 | 코드에 작성된 규칙 | 모형의 판단과 코드 규칙의 결합 |
| 경로 | 비교적 고정된 순서와 분기 | 관찰 결과에 따라 동적으로 변함 |
| 장점 | 재현성과 검증이 비교적 쉬움 | 불완전하게 명세된 다단계 문제에 유연함 |
| 주요 위험 | 규칙에 없는 상황을 처리하기 어려움 | 비결정적 경로, 비용 증가, 잘못된 tool call |
| 적합한 예 | 자료 검증, 승인 절차, 정형 ETL | 조사, 지원 응답, 여러 도구를 조합한 문제 해결 |

Agent를 쓴다는 사실이 모든 단계를 모형에 맡겨야 한다는 뜻은 아니다. 권한 검사, 금액 한도, 자료형 검증과 같이 정확한 규칙이 있는 단계는 일반 코드로 강제하고, 자연어 해석이나 도구 선택처럼 불확실성이 있는 부분만 모형에 맡기는 편이 경로를 설명하고 시험하기 쉽다.[5,9,10]

## 2. LangChain과 LangGraph의 역할

### (1) 구조와 추상화 수준

| 비교 항목 | LangChain | LangGraph |
| --- | --- | --- |
| 주된 역할 | 모형, tool과 표준 agent loop를 빠르게 조립 | 상태를 가진 workflow와 agent의 실행 순서를 직접 설계 |
| 추상화 수준 | 고수준 agent framework | 저수준 orchestration framework와 runtime |
| 중심 API | `create_agent`, `@tool`, middleware, structured output | `StateGraph`, state schema, node, edge, checkpointer, `interrupt` |
| 제어 흐름 | “tool이 더 없을 때까지 반복”하는 기본 loop를 제공 | 순차, 조건 분기, cycle, 병렬 fan-out과 종료 조건을 명시 |
| 상태 관리 | message 중심의 agent state와 선택적 checkpointer | 사용자가 정의한 공유 state와 reducer, checkpoint |
| 적합한 시작점 | 일반적인 tool-calling agent와 빠른 prototype | 맞춤형 분기, 장시간 작업, 승인·재개와 복구가 핵심인 응용 |
| 둘의 관계 | 생성한 agent가 compiled LangGraph로 동작 | 단독 사용하거나 LangChain agent를 node·subgraph로 포함 가능 |

이 비교는 기능의 유무보다 **어느 수준에서 기본값을 제공하는가**의 차이이다. LangChain agent도 LangGraph의 persistence, streaming과 human-in-the-loop 기능을 활용할 수 있고, LangGraph node 안에서 LangChain의 model과 tool abstraction을 사용할 수 있다. LangGraph는 prompt나 agent architecture를 자동으로 정하지 않으므로 세밀한 제어와 함께 더 많은 설계 책임을 요구한다.[3,5,8,11]

### (2) 선택 기준

다음 질문으로 시작점을 고를 수 있다.

| 요구사항 | 권장 시작점 | 이유 |
| --- | --- | --- |
| 한 agent가 몇 개의 tool을 반복 호출하면 충분함 | LangChain | `create_agent`가 표준 loop와 message state를 제공한다. |
| 모형 공급자를 바꿀 가능성이 큼 | LangChain | 공통 model interface와 공급자별 integration을 제공한다. |
| 단계별 상태 schema와 분기를 직접 검토해야 함 | LangGraph | node와 edge가 제어 흐름을 코드에 드러낸다. |
| 중간 승인 뒤 같은 작업을 재개해야 함 | LangGraph | checkpoint와 `interrupt`를 중심 기능으로 제공한다. |
| 결정론적 전처리와 agent를 한 흐름에 결합함 | 둘을 조합 | LangChain agent를 LangGraph node 또는 subgraph로 넣을 수 있다. |

처음부터 복잡한 graph를 만드는 것이 항상 유리하지는 않다. 표준 loop로 표현되는 문제는 LangChain으로 최소 구현을 만들고, 실제 요구에서 고정 분기나 복구 지점이 드러날 때 LangGraph로 확장하는 방법이 유지보수 범위를 줄인다.[3,5,12,13]

## 3. LangChain 기본 개념과 핵심 기능

### (1) `create_agent`와 tool loop

LangChain v1에서 `create_agent`는 agent를 만드는 표준 고수준 API이다. `model`, `tools`, `system_prompt`를 주면 model node와 tool node가 필요한 동안 번갈아 실행되는 compiled graph를 반환한다. `invoke` 입력의 `messages`에는 새 사용자 message를 넣고, 결과의 마지막 message에서 최종 응답을 읽는다.[3,4,12,13]

| 구성 요소 | 지정 방법 | 실행 중 역할 |
| --- | --- | --- |
| Model | model 식별자 문자열 또는 model instance | 다음 응답이나 tool call을 생성한다. |
| Tool | Python 함수 또는 `@tool`로 감싼 함수 | 외부 정보 조회와 행동을 수행한다. |
| System prompt | `system_prompt` | 역할, 제약과 응답 원칙을 제공한다. |
| State | 기본 `messages`, 선택적 custom state | 대화와 중간 결과를 전달한다. |
| Middleware | `middleware=[...]` | model·tool 호출 전후의 정책과 처리를 삽입한다. |
| Checkpointer | `checkpointer=...` | thread별 상태를 저장하고 다음 호출에서 복원한다. |

`@tool`은 함수 이름, docstring과 type hint를 tool schema로 바꾸는 가장 단순한 방법이다. Docstring은 model이 도구의 용도를 선택하는 설명으로 사용되므로, 구현 세부보다 **언제 호출하고 무엇을 반환하는가**를 명확히 적어야 한다.[4,6,12]

### (2) 최소 사용 예제

다음 예제는 두 정수를 곱하는 tool을 agent에 제공한다. 예제의 model 이름과 환경 변수는 OpenAI integration을 사용한 경우이며, 다른 공급자를 사용하려면 해당 `langchain-*` package와 API key로 바꾼다.[3,12,14]

```bash
python -m pip install -U langchain langchain-openai
export OPENAI_API_KEY="YOUR_API_KEY"
```

```python
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """두 정수 a와 b를 곱한 값을 반환한다."""
    return a * b


agent = create_agent(
    model="openai:gpt-5.4",
    tools=[multiply],
    system_prompt=(
        "계산이 필요하면 제공된 tool을 사용하고, "
        "결과를 간결한 한국어로 설명하라."
    ),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "37과 24를 곱해 줘."}]}
)

print(result["messages"][-1].content)
```

이 호출에서 예상되는 제어 흐름은 다음과 같다.

| 순서 | 실행 주체 | 입력 | 출력 |
| --- | --- | --- | --- |
| 1 | Agent runtime | 사용자 message | model에 전달할 state |
| 2 | Model | message와 `multiply` schema | `multiply(a=37, b=24)` tool call |
| 3 | Tool runtime | 구조화된 인자 | 정수 `888` |
| 4 | Model | 원래 요청과 tool 결과 | 사용자에게 보낼 최종 설명 |

실제 tool 호출 여부와 문구는 model에 따라 달라질 수 있으므로, “반드시 한 번 호출한다”를 application invariant로 가정해서는 안 된다. Tool 인자 schema와 반환값을 검증하고, 중요한 계산은 결과를 다시 검사하는 일반 코드 또는 test를 둔다.[9,10,13]

### (3) Structured output, middleware와 memory

자연어 응답을 다른 프로그램이 소비해야 한다면 문자열을 임의로 parsing하기보다 `response_format`에 Pydantic model, dataclass 또는 `TypedDict` schema를 지정한다. 지원되는 방식에서는 검증된 결과가 agent state의 `structured_response`에 저장된다.[4,7,13]

```python
from pydantic import BaseModel, Field


class CalculationResult(BaseModel):
    expression: str
    value: int
    explanation: str = Field(description="한 문장의 한국어 설명")


typed_agent = create_agent(
    model="openai:gpt-5.4",
    tools=[multiply],
    response_format=CalculationResult,
)

typed_result = typed_agent.invoke(
    {"messages": [{"role": "user", "content": "37과 24를 곱해 줘."}]}
)
print(typed_result["structured_response"])
```

Middleware는 agent loop의 앞뒤나 model·tool 호출 주위에 동작을 삽입한다. 대화 요약, 재시도, rate limit, 개인 식별 정보 처리와 tool 실행 전 승인 같은 횡단 관심사를 agent 본체와 분리할 때 사용한다. Middleware가 보안 경계를 자동으로 만드는 것은 아니며, 실제 권한 검사는 tool과 외부 service에서도 독립적으로 시행해야 한다.[8–10,13]

짧은 대화 기억은 agent state와 checkpointer를 결합한다. 같은 `thread_id`로 호출하면 해당 thread의 checkpoint를 이어 사용할 수 있다.[11,15]

```python
from langgraph.checkpoint.memory import InMemorySaver


memory_agent = create_agent(
    model="openai:gpt-5.4",
    tools=[multiply],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "calculation-demo"}}

memory_agent.invoke(
    {"messages": [{"role": "user", "content": "내 기준값은 37이야."}]},
    config,
)
result = memory_agent.invoke(
    {"messages": [{"role": "user", "content": "그 값에 24를 곱해 줘."}]},
    config,
)
```

`InMemorySaver`는 process가 끝나면 사라지는 개발·시험용 저장소이다. 운영 환경에서는 DB-backed checkpointer를 사용하고, 보존 기간, 사용자별 thread 격리와 민감 정보 삭제 정책을 별도로 정한다.[11,15]

## 4. LangGraph 기본 개념과 핵심 기능

### (1) State, node와 edge

LangGraph의 Graph API는 먼저 공유 `State` schema를 정의하고, state를 읽어 부분 update를 반환하는 node를 추가한 뒤, node 사이의 edge를 연결하고 graph를 compile한다. `START`와 `END`는 각각 진입점과 종료점을 나타낸다. 조건부 edge의 routing function은 현재 state를 읽어 다음 node를 고른다.[5,8,16]

| 구성 요소 | 의미 | 설계할 내용 |
| --- | --- | --- |
| State | 실행 중 공유하는 자료 schema | field의 type, 초기값과 reducer |
| Node | 한 단계의 계산 함수 | 읽을 field와 반환할 부분 update |
| Edge | 실행 순서 | 고정 연결 또는 조건부 routing |
| `START` | 가상 진입점 | 최초 실행 node |
| `END` | 가상 종료점 | 정상 종료 조건 |
| Compile | graph 검증과 runtime 구성 | checkpointer, breakpoint 등 |

Node가 전체 state를 직접 변경하기보다 `dict` 형태의 update를 반환하면 runtime이 schema와 reducer 규칙에 따라 이를 병합한다. 여러 node가 같은 list에 값을 누적하는 경우처럼 기본 덮어쓰기가 맞지 않을 때에는 `Annotated` reducer를 명시해야 한다.[8,16]

다음 state에서는 각 node가 반환한 `events` 목록을 `operator.add`로 이어 붙인다. Reducer를 생략하면 새 목록이 이전 값을 덮어쓰므로, 병렬 node나 반복 경로가 같은 field를 갱신하는 graph에서는 병합 규칙 자체가 자료 계약의 일부이다.[8,16]

```python
import operator
from typing import Annotated
from typing_extensions import TypedDict


class TraceState(TypedDict, total=False):
    events: Annotated[list[str], operator.add]
```

### (2) 조건부 graph 예제

다음 예제는 LLM을 사용하지 않고 LangGraph의 상태와 routing만 보여 준다. 입력 정수가 음수가 아니면 제곱하고, 음수이면 오류 message를 만든다.[8,16]

```bash
python -m pip install -U langgraph
```

```python
from typing import Literal
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class NumberState(TypedDict, total=False):
    number: int
    is_valid: bool
    result: int
    error: str


def validate(state: NumberState) -> dict:
    return {"is_valid": state["number"] >= 0}


def route_after_validation(
    state: NumberState,
) -> Literal["square", "reject"]:
    return "square" if state["is_valid"] else "reject"


def square(state: NumberState) -> dict:
    return {"result": state["number"] ** 2}


def reject(state: NumberState) -> dict:
    return {"error": "0 이상의 정수를 입력해야 한다."}


builder = StateGraph(NumberState)
builder.add_node("validate", validate)
builder.add_node("square", square)
builder.add_node("reject", reject)

builder.add_edge(START, "validate")
builder.add_conditional_edges("validate", route_after_validation)
builder.add_edge("square", END)
builder.add_edge("reject", END)

graph = builder.compile()

print(graph.invoke({"number": 7}))
print(graph.invoke({"number": -2}))
```

첫 호출은 `START → validate → square → END`, 둘째 호출은 `START → validate → reject → END`를 따른다. 이처럼 경로를 코드에 명시하면 model이 필요 없는 validation과 업무 규칙을 결정론적으로 유지하고, 필요한 node에만 LLM 호출을 넣을 수 있다.[5,8,16]

### (3) Cycle과 종료 조건

Agent loop는 graph 관점에서 model node와 tool node 사이의 cycle이다. Model이 tool call을 생성하면 tool node로, 더 이상 tool이 필요하지 않으면 `END`로 routing한다. LangGraph는 cycle을 허용하지만 반복 횟수, 시간, 비용 또는 상태 기반 종료 조건을 반드시 설계해야 한다. 그렇지 않으면 같은 행동이 반복되거나 graph recursion limit에 도달할 수 있다.[1,4,8,16]

| 반복 제어 항목 | 예시 | 목적 |
| --- | --- | --- |
| 상태 기반 종료 | `task_complete is True` | 목표 달성 시 종료 |
| 최대 step | `attempts >= 5` | 무한 반복 방지 |
| 시간 제한 | node와 전체 실행 timeout | 느린 외부 service 격리 |
| 비용 제한 | 누적 token 또는 tool 비용 | 예상 밖의 지출 방지 |
| 오류 경로 | retry 후 fallback 또는 사람 검토 | 동일 오류의 무한 재시도 방지 |

`recursion_limit`은 `configurable` 안이 아니라 실행 설정의 최상위 key로 전달한다. 이는 업무 의미상의 종료 조건을 대신하지 않지만, 잘못 연결된 cycle이 무한히 진행되는 것을 막는 최종 상한으로 사용할 수 있다.[8,16]

```python
run_config = {
    "configurable": {"thread_id": "number-demo-1"},
    "recursion_limit": 25,
}
result = graph.invoke({"number": 7}, config=run_config)
```

## 5. Persistence와 human-in-the-loop

### (1) Checkpoint와 thread

Checkpointer를 지정해 graph를 compile하면 LangGraph는 실행 단계의 state snapshot을 checkpoint로 저장한다. Checkpoint는 `thread_id`별로 묶이며, 같은 thread의 상태 조회·재개, memory, time travel과 failure recovery의 기반이 된다.[5,11,15]

```python
from langgraph.checkpoint.memory import InMemorySaver


checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "number-demo-1"}}
result = graph.invoke({"number": 7}, config=config)
snapshot = graph.get_state(config)
```

Checkpoint는 외부 side effect까지 되돌리지 않는다. 예를 들어 node가 이미 email을 보낸 뒤 실패하면 graph state를 이전 지점에서 재개해도 보낸 email은 자동 취소되지 않는다. 재실행될 수 있는 node의 side effect는 idempotency key, transaction 또는 “계획 생성–승인–실행” 분리로 중복을 방지해야 한다.[11,17]

아래 패턴은 thread와 업무 action의 식별자를 결합해 같은 요청의 재실행을 외부 service가 알아볼 수 있게 한다. 실제 중복 방지는 client가 아니라 server 또는 transaction 저장소가 같은 key의 처리를 원자적으로 기록할 때 성립한다.[11,17]

```python
def execute_payment(state: dict, runtime) -> dict:
    idempotency_key = f"{runtime.config['configurable']['thread_id']}:{state['action_id']}"
    receipt = payment_client.charge(
        amount=state["amount"],
        idempotency_key=idempotency_key,
    )
    return {"receipt_id": receipt.id}
```

### (2) `interrupt`를 이용한 승인과 재개

`interrupt()`는 node 실행을 일시 중단하고 JSON-serializable payload를 caller에게 반환한다. Checkpointer와 `thread_id`가 있어야 같은 실행을 찾아 `Command(resume=...)`로 재개할 수 있다.[5,17]

```python
from langgraph.types import Command, interrupt


def approval_node(state: dict) -> dict:
    approved = interrupt(
        {
            "question": "이 작업을 실행할까요?",
            "proposed_action": state["proposed_action"],
        }
    )
    return {"approved": bool(approved)}


# 첫 호출은 approval_node에서 멈춘다.
paused = graph.invoke(initial_state, config=config)

# 같은 thread_id를 사용해 승인 값을 전달하고 재개한다.
resumed = graph.invoke(Command(resume=True), config=config)
```

Interrupt가 있는 node는 재개할 때 node 처음부터 다시 실행될 수 있으므로, `interrupt()` 앞의 side effect도 idempotent해야 한다. 승인 화면에는 model의 자연어 설명만 보여 주지 말고 실제 tool 이름, 구조화된 인자, 영향을 받는 대상과 권한 범위를 함께 표시해야 사람이 행동의 의미를 검토할 수 있다.[10,17]

## 6. LangChain–LangGraph 결합 패턴

### (1) LangChain agent를 LangGraph node로 넣기

LangChain의 `create_agent`가 반환하는 객체는 compiled LangGraph interface를 따르므로 `invoke`와 `stream`을 사용할 수 있고, 더 큰 `StateGraph`의 node 또는 subgraph로 조합할 수 있다. 대표 구조는 입력 분류와 권한 검사를 결정론적 node로 처리하고, 허용된 요청만 LangChain agent로 보내며, 결과 검증과 승인을 다시 고정 node로 처리하는 방식이다.[3,4,8,13]

| 단계 | 구현 계층 | 책임 |
| --- | --- | --- |
| 입력 검증 | LangGraph Python node | schema, 사용자 권한과 요청 범위를 검사 |
| 요청 분류 | LangGraph conditional edge | 조사·계산·거절 경로를 선택 |
| 동적 도구 사용 | LangChain agent node | 필요한 tool을 반복 선택하고 결과를 종합 |
| 결과 검증 | LangGraph Python node | 필수 field, 출처와 정책 준수 여부를 검사 |
| 고위험 행동 승인 | LangGraph `interrupt` | 실행 전 사람이 대상과 인자를 승인 |
| 최종 실행 | 최소 권한 tool | 승인된 구조화 인자만 외부 service에 적용 |

### (2) 확장 순서

작은 prototype은 다음 순서로 확장할 수 있다.

1. Tool 없이 model 호출의 입력과 출력 계약을 먼저 고정한다.
2. 읽기 전용 tool 하나를 추가하고 tool 인자와 반환값을 단위 시험한다.
3. `create_agent`로 반복 호출이 필요한 최소 agent를 만든다.
4. Structured output으로 응용 코드가 받을 결과 schema를 고정한다.
5. 분기, 승인 또는 재개가 실제로 필요해지면 LangGraph state와 node로 외곽 workflow를 만든다.
6. Checkpointer, trace, timeout, retry와 평가 자료를 운영 조건에 맞게 추가한다.

이 순서는 모든 프로젝트에 강제되는 규칙이 아니라 복잡성을 단계적으로 드러내기 위한 실무적 heuristic이다. 처음부터 multi-agent 구조를 채택하기보다 단일 agent와 명시적 workflow로 요구사항을 충족할 수 있는지 먼저 확인한다.[2,12,13]

## 7. 시험, 관측과 보안

### (1) 검증 범위

Agent는 같은 입력에도 model sampling, 외부 자료와 tool 상태에 따라 다른 경로를 택할 수 있다. 따라서 최종 문장 하나와 정확히 일치하는지만 검사하기보다 각 계층의 계약을 나누어 시험한다.[2,9,13]

| 시험 수준 | 고정할 입력 | 확인할 항목 |
| --- | --- | --- |
| Tool 단위 시험 | 명시적 함수 인자 | 반환 schema, 오류, timeout과 side effect |
| Node 단위 시험 | 작은 state fixture | 읽고 쓰는 field와 routing 결과 |
| Agent trajectory 시험 | 사용자 요청과 mock tool 결과 | 허용된 tool, 호출 인자, 최대 step과 종료 |
| 통합 시험 | test service와 고정 dataset | 인증, persistence, retry와 중복 실행 |
| 품질 평가 | 대표·경계·공격 입력 집합 | 정답성, 출처, 비용, latency와 정책 위반률 |

Trace에는 model 입력·출력, tool 이름과 인자, 상태 전이, 오류와 지연 시간을 연결해 기록하되 secret과 개인정보는 저장 전에 가린다. 운영 지표는 최종 성공률뿐 아니라 tool 오류율, 평균·상위 percentile latency, step 수, token 비용, interrupt 승인·거절률을 함께 본다.[5,8,13]

결정론적 node는 model을 거치지 않으므로 작은 state fixture로 직접 시험할 수 있다. 다음 시험은 정상 경로와 경계 입력의 routing 계약을 고정하며, agent 전체의 자연어 문구가 달라져도 업무 규칙의 회귀를 분리해 검출한다.[8,13]

```python
def test_validation_routes_boundary_values():
    assert validate({"number": 0}) == {"is_valid": True}
    assert route_after_validation({"is_valid": True}) == "square"
    assert validate({"number": -1}) == {"is_valid": False}
    assert route_after_validation({"is_valid": False}) == "reject"
```

!!! info "[Measurement]"
    같은 version의 agent와 tool, 고정된 평가 집합 $D$에서 각 요청의 업무 성공 여부 $s_i\in\{0,1\}$, tool 호출 수 $n_i^{\mathrm{tool}}$, 실패한 tool 호출 수 $n_i^{\mathrm{err}}$, 종단 간 지연 시간 $t_i$, 총 비용 $c_i$를 trace에서 집계한다. 이 문서에서는 서로 다른 운영 조건을 섞지 않고 다음 네 값을 함께 보고하는 규약을 사용한다.

    $$
    R_{\mathrm{success}}
    =\frac{1}{|D|}\sum_{i\in D}s_i
    $$

    $$
    R_{\mathrm{tool\ error}}
    =\frac{\sum_{i\in D}n_i^{\mathrm{err}}}
    {\sum_{i\in D}n_i^{\mathrm{tool}}}
    $$

    $$
    t_{95}=Q_{0.95}\!\left(\{t_i:i\in D\}\right)
    $$

    $$
    C_{\mathrm{success}}
    =\frac{\sum_{i\in D}c_i}{\sum_{i\in D}s_i}
    $$

    $R_{\mathrm{success}}$는 요청 성공률, $R_{\mathrm{tool\ error}}$는 tool 호출당 오류율, $t_{95}$는 종단 간 지연 시간의 95번째 백분위수, $C_{\mathrm{success}}$는 성공한 요청 한 건당 비용이다. 성공 건수가 0이면 $C_{\mathrm{success}}$는 정의하지 않는다. 성공 판정 rubric, timeout, 재시도 횟수, model·tool version과 평가 집합을 함께 기록해야 지표를 비교할 수 있다.[5,8,13]

### (2) Tool 권한과 prompt injection

외부 문서, web page와 tool 결과에 들어 있는 문장을 명령으로 신뢰하면 indirect prompt injection이 agent의 행동으로 이어질 수 있다. 또한 agent에 필요 이상의 tool, 권한과 자율성을 주면 잘못된 model 출력의 영향 범위가 커진다. OWASP는 이를 prompt injection과 excessive agency의 결합 문제로 설명하며 최소 기능·최소 권한, 고위험 행동의 독립 승인과 tool call 검증을 권고한다.[9,10]

!!! warning "[Interpretation Caveat]"
    System prompt에 “안전하게 행동하라”고 쓰는 것만으로 권한 경계가 생기지 않는다. 삭제·송금·배포처럼 되돌리기 어려운 행동은 model 밖의 인증·인가 코드가 실제 사용자 권한, 대상과 한도를 다시 검증해야 한다. 읽기 tool과 쓰기 tool을 분리하고, 쓰기 tool에는 idempotency와 사람의 승인을 적용한다.[9,10,17]

운영 전 최소 점검 항목은 다음과 같다.

- Agent가 볼 필요가 없는 tool을 등록하지 않는다.
- Tool credential은 해당 기능에 필요한 최소 권한과 자료 범위만 가진다.
- 외부 content와 tool output을 신뢰할 수 없는 data로 취급한다.
- Tool call을 실행하기 전에 이름, 인자 schema, 사용자 의도와 정책을 검사한다.
- 고위험·비가역 행동은 구조화된 내용을 사람에게 보여 주고 승인받는다.
- 반복 횟수, 시간, token·비용과 병렬 실행 수에 상한을 둔다.
- State와 trace의 개인정보, secret, 보존 기간과 삭제 경로를 관리한다.
- Version을 고정하고 upgrade 때 agent trajectory와 persistence를 회귀 시험한다.

## 8. 요약

- LLM agent는 model이 tool을 선택하고 관찰 결과를 state에 반영하는 순환이다. 모든 단계를 agent에 맡기지 말고 정확한 규칙은 결정론적 workflow로 유지한다.
- LangChain은 model·tool integration과 표준 agent loop를 제공하는 고수준 framework이다. LangChain v1에서는 `create_agent`, `@tool`, structured output, middleware와 checkpointer가 기본 구성 요소이다.
- LangGraph는 state, node와 edge로 실행 흐름을 직접 정의하는 저수준 orchestration framework와 runtime이다. 조건 분기, cycle, persistence, interrupt와 재개가 핵심 기능이다.
- LangChain agent는 LangGraph 위에서 동작하므로, 일반 tool-calling은 LangChain으로 만들고 맞춤형 workflow의 node로 조합할 수 있다.
- Checkpoint는 graph state를 저장하지만 이미 일어난 외부 side effect를 취소하지 않는다. 재시도 가능한 node에는 idempotency를 설계한다.
- 운영 환경에서는 최소 권한, tool call 검증, 고위험 행동 승인, 실행 상한, trace와 계층별 시험이 필요하다.

## 9. 참고문헌

1. S. Yao et al., “ReAct: Synergizing Reasoning and Acting in Language Models,” *International Conference on Learning Representations* (2023). [OpenReview](https://openreview.net/forum?id=WE_vluYUL-X).
2. L. Wang et al., “A survey on large language model based autonomous agents,” *Frontiers of Computer Science* **18**, 186345 (2024). [DOI](https://doi.org/10.1007/s11704-024-40231-1).
3. LangChain, “LangChain overview,” Python documentation (2026년 확인). [공식 문서](https://docs.langchain.com/oss/python/langchain/overview).
4. LangChain, “Agents,” Python documentation (2026년 확인). [공식 문서](https://docs.langchain.com/oss/python/langchain/agents).
5. LangChain, “LangGraph overview,” Python documentation (2026년 확인). [공식 문서](https://docs.langchain.com/oss/python/langgraph/overview).
6. LangChain, “Tools,” Python documentation (2026년 확인). [공식 문서](https://docs.langchain.com/oss/python/langchain/tools).
7. LangChain, “Structured output,” Python documentation (2026년 확인). [공식 문서](https://docs.langchain.com/oss/python/langchain/structured-output).
8. LangChain, “Middleware overview,” Python documentation (2026년 확인). [공식 문서](https://docs.langchain.com/oss/python/langchain/middleware/overview).
9. OWASP Foundation, “LLM06: Excessive Agency,” *OWASP Top 10 for Large Language Model Applications* (2026년 확인). [공식 자료](https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM06_ExcessiveAgency.html).
10. OWASP Foundation, “LLM Prompt Injection Prevention Cheat Sheet” (2026년 확인). [공식 자료](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).
11. LangChain, “Persistence,” LangGraph Python documentation (2026년 확인). [공식 문서](https://docs.langchain.com/oss/python/langgraph/persistence).
12. C. T. Ho, “LangChain Python Tutorial: A Complete Guide for 2026,” *The JetBrains Blog* (2026). [실습 자료](https://blog.jetbrains.com/pycharm/2026/02/langchain-tutorial-2026/).
13. A. Dutt, “LangChain v1: Build an Auto Meeting Recap Assistant,” *DataCamp* (2025). [실습 자료](https://www.datacamp.com/tutorial/langchain-v1).
14. LangChain, “OpenAI integration,” Python documentation (2026년 확인). [공식 문서](https://docs.langchain.com/oss/python/integrations/llms/openai).
15. LangChain, “Short-term memory,” Python documentation (2026년 확인). [공식 문서](https://docs.langchain.com/oss/python/langchain/short-term-memory).
16. LangChain, “Graph API overview,” LangGraph Python documentation (2026년 확인). [공식 문서](https://docs.langchain.com/oss/python/langgraph/graph-api).
17. LangChain, “Interrupts,” LangGraph Python documentation (2026년 확인). [공식 문서](https://docs.langchain.com/oss/python/langgraph/interrupts).
