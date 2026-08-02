# Device Physics

MOSFET의 기본 동작, leakage current, short-channel effects와 architecture evolution을 다룬다. Memory device 문서에서는 시스템 메모리 계층과 셀 어레이·주변회로·칩 구조를 연결해 설명한다.

## 1. 문서 목록

- [(1) MOSFET: Basic Operation](mosfet/basic-operation.md) — 네 단자 구조, nMOS와 pMOS, enhancement mode와 depletion mode, 채널 형성과 기본 전류–전압 특성
- [(2) MOSFET: Leakage Current](mosfet/leakage-mechanisms.md) — subthreshold leakage, gate dielectric tunneling, junction leakage, GIDL과 punch-through의 발생 원인·측정식·저감 방법
- [(3) MOSFET: Short-Channel Effects](mosfet/short-channel-effects.md) — threshold-voltage roll-off, DIBL, SS degradation, punch-through의 추출식과 구조·공정별 억제책
- [(4) MOSFET: Architecture Evolution](mosfet/architecture-evolution.md) — SOI, HKMG, FinFET과 GAA nanosheet의 발전 배경, 구조적 차이와 핵심 설계 인자
- [(5) Memory Device: Basics](memory-device/basics.md) — 시스템 메모리 계층과 칩 내부 계층, cell array, word line·bit line, 주변회로와 sense amplifier
- [(6) SRAM: 6T Bitcell](memory-device/sram.md) — 6T bitcell의 hold·read·write, SNM, read/write window, $V_\mathrm{min}$과 통계적 검증
