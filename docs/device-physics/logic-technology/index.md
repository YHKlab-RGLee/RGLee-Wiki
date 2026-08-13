# 5. Logic technology

Logic technology는 MOSFET의 전기적 특성이 반복 배치 가능한 논리 셀의 기하 구조와 회로 성능으로 변환되는 계층을 다룬다. Standard-cell architecture와 process–device–cell–block 사이의 design–technology co-optimization (DTCO)을 연결하여 설명한다.

## 문서 목록

- [5.1. Standard-cell architecture](standard-cell-architecture.md) — cell height와 routing track, transistor folding과 fins/sheets 수, diffusion sharing, power rail·signal pin, 기본·복합 CMOS gate layout 및 drive-strength 설계
- [5.2. Logic DTCO](logic-dtco.md) — CPP·metal pitch·cell height의 결합, FinFET·GAA·CFET의 layout 영향, design rule과 block-level PPA를 연결하는 계층 간 최적화

## 선행 문서

[MOSFET: CMOS](../mosfet/cmos.md)에서 inverter와 NAND·NOR의 transistor network, 지연과 전력의 정의를 먼저 확인하는 것이 좋다. FinFET과 GAA의 폭 양자화와 기생 성분은 [MOSFET: Architecture evolution](../mosfet/architecture-evolution.md)을 따른다.
