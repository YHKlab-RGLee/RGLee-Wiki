# Device physics

MOSFET의 기본 동작, leakage current, short-channel effects와 architecture evolution을 다룬다. Memory device 문서에서는 시스템 메모리 계층과 셀 어레이·주변회로·칩 구조를 연결해 설명한다. Semiconductor process 문서에서는 실리콘 웨이퍼부터 소자 형성, 금속 배선과 패키징까지의 제조 흐름을 다룬다.

## 문서 목록

### 1. MOSFET

- [1.1. Overview](mosfet/basic-operation.md) — 네 단자 구조, nMOS와 pMOS, enhancement mode와 depletion mode, 채널 형성과 기본 전류–전압 특성
- [1.2. Leakage current](mosfet/leakage-mechanisms.md) — subthreshold leakage, gate dielectric tunneling, junction leakage, GIDL과 punch-through의 발생 원인·측정식·저감 방법
- [1.3. Short-channel effects](mosfet/short-channel-effects.md) — threshold-voltage roll-off, DIBL, SS degradation, punch-through의 추출식과 구조·공정별 억제책
- [1.4. Architecture evolution](mosfet/architecture-evolution.md) — SOI, HKMG, FinFET과 GAA nanosheet의 발전 배경, 구조적 차이와 핵심 설계 인자

### 2. Memory device

- [2.1. Overview](memory-device/basics.md) — 시스템 메모리 계층과 칩 내부 계층, cell array, word line·bit line, 주변회로와 sense amplifier
- [2.2. SRAM basic](memory-device/sram.md) — 6T bitcell의 hold·read·write, SNM, read/write window, $V_\mathrm{min}$과 통계적 검증
- [2.3. SRAM advance](memory-device/sram-advance.md) — PVT 변동과 수율, 저전압 assist, 8T·10T·FinFET·GAA·CFET cell과 신뢰성 불량 분석
- [2.4. DRAM basic](memory-device/dram.md) — 1T1C cell과 Precharge–Activate–Sense–Restore의 read 순서, write·refresh와 기본 timing
- [2.5. DRAM advance](memory-device/dram-advance.md) — 8F²·6F²·4F² cell과 PCAT·RCAT·BCAT·VCT의 구조 발전, leakage·신뢰성·RowHammer, 전력·성능과 DDR·HBM interface

### 3. Semiconductor process

- [3.1. Eight major processes](semiconductor-process/eight-major-processes.md) — 웨이퍼 제조, 산화, photolithography, 식각, 이온 주입, 증착, 금속 배선과 패키징의 원리·정량 지표·상충관계
