# Device Physics

MOSFET의 기본 동작, leakage current, short-channel effects와 architecture evolution에 더해 memory device의 공통 구조를 다룬다. MOSFET 문서는 기본 동작의 공통 기호와 측정 규약을 바탕으로 각 현상의 물리적 기원과 추출 방법을 설명하고, memory device 문서는 메모리 계층에서 셀 어레이·주변회로·칩 구조로 이어지는 공통 기반을 설명한다.

## 1. Contents

- [(1) MOSFET: Basic Operation](mosfet/basic-operation.md) — nMOS의 게이트 제어, 동작 영역, 대표 DC 특성과 공통 기호·추출 규약
- [(2) MOSFET: Leakage Current](mosfet/leakage-mechanisms.md) — subthreshold leakage, gate dielectric tunneling, junction leakage, GIDL과 punch-through의 발생 원인·측정식·저감 방법
- [(3) MOSFET: Short-Channel Effects](mosfet/short-channel-effects.md) — threshold-voltage roll-off, DIBL, SS degradation, punch-through의 추출식과 구조·공정별 억제책
- [(4) MOSFET: Architecture Evolution](mosfet/architecture-evolution.md) — SOI, HKMG, FinFET과 GAA nanosheet의 발전 배경, 구조적 차이와 핵심 설계 인자
- [(5) Memory Device: Basics](memory-device/basics.md) — 시스템 메모리 계층과 칩 내부 계층, cell array, word line·bit line, 주변회로와 sense amplifier
