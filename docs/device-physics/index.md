# Device physics

MOSFET의 기본 동작, leakage current, short-channel effects와 architecture evolution을 다룬다. Memory device 문서에서는 시스템 메모리 계층과 셀 어레이·주변회로·칩 구조를 연결해 설명한다. Semiconductor process 문서에서는 실리콘 웨이퍼부터 소자 형성, 금속 배선과 패키징까지의 제조 흐름을 다룬다. Device reliability 문서에서는 트랜지스터와 배선의 주요 열화 메커니즘, 수명 시험과 통계적 외삽을 설명한다.

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
- [2.6. NAND basic](memory-device/nand.md) — NAND string과 문턱전압 저장, floating-gate·charge-trap 구조 및 program·read·erase 동작
- [2.7. NAND advance](memory-device/nand-advance.md) — MLC·TLC 상태 부호화, ISPP, 문턱전압 산포, 3D NAND의 macaroni channel과 string on-current

### 3. Semiconductor process

- [3.1. Eight major processes](semiconductor-process/eight-major-processes.md) — 웨이퍼 제조, 산화, photolithography, 식각, 이온 주입, 증착, 금속 배선과 패키징의 원리·정량 지표·상충관계
- [3.2. Etching](semiconductor-process/etching.md) — wet/dry etching, plasma ion–neutral synergy, anisotropy·selectivity·ARDE와 endpoint detection
- [3.3. Doping and annealing](semiconductor-process/doping-and-annealing.md) — diffusion·ion implantation의 농도 분포, channeling, damage·activation과 transient enhanced diffusion
- [3.4. Thin-film deposition](semiconductor-process/thin-film-deposition.md) — PVD·CVD·ALD와 epitaxy의 성장 원리, 막 두께·균일도·conformality 및 계측

### 4. Device reliability

- [4.1. Overview](device-reliability/overview.md) — 열화와 고장, mission profile, 가속 수명 시험과 공통 측정·보고 규약
- [4.2. Bias temperature instability](device-reliability/bias-temperature-instability.md) — oxide charge·interface state, stress–recovery 측정과 문턱전압 이동
- [4.3. Hot-carrier degradation](device-reliability/hot-carrier-degradation.md) — 드레인 고전계의 결함 생성, 바이어스 영역과 전기적 열화 지표
- [4.4. Time-dependent dielectric breakdown](device-reliability/time-dependent-dielectric-breakdown.md) — 절연막 결함 축적, percolation, breakdown 판정과 Weibull 통계
- [4.5. Interconnect reliability](device-reliability/interconnect-reliability.md) — electromigration 원자 flux, back stress, Black 모형과 Blech criterion
- [4.6. Reliability modeling](device-reliability/reliability-modeling.md) — 수명 분포, censored data, 가속 계수와 메커니즘별 외삽
