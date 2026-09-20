# 전체 과학 문서 논리 구성 검토 결과

과학 문서 45개를 본문 전체 기준으로 검토했다. Home, index, Research Note는 논리 검토에서 제외했다. **33개 개선, 12개 유지, 미해결 0개**이며 현재 본문과 검토 기록의 해시가 모두 일치한다.

기존 문서를 바탕으로 선행 정의·가정·적용 범위를 보강하고, 설명 순서와 중복을 정리했다. 사용자가 추가 승인한 9개 문서는 계산 예제·유도·해석 조건까지 확장했으며 모두 full review와 정량 기준을 통과했다.

## 검증 결과

- `./build.sh changed`: 통과, strict MkDocs 4.05초.
- `./build.sh build`: 전체 품질 검사 및 strict MkDocs 통과, 4.10초.
- `git diff --check`: 통과.
- 품질 집계 회귀시험: 27개 통과.
- 45개 문서의 범위·전체 본문 읽기·현재 해시·registry pass 일치 검사: 통과.

전체 빌드는 과학 문서 외 Research Note와 탐색 문서도 검사하므로 article 46개, index/home 19개로 집계된다. Changed 검사에는 기존 작업의 변경분도 포함된다. 검토 모델 정보는 요청에 따라 공백으로 유지했다.

## 추가 확장한 9개 문서

| 문서 | 실질적으로 보강한 설명 | full review |
| --- | --- | --- |
| [Many-body perturbation theory: GW approximation](../../docs/computational-materials-science/many-body-perturbation/gw-approximation.md) | 준입자 방정식의 선형화 오차와 pole 모형 검산 | pass |
| [Molecular dynamics: Overview](../../docs/computational-materials-science/molecular-simulation/overview.md) | 조화 진동자 적분, canonical 온도 변동, 상관·block 오차 | pass |
| [Point defects: Charged defect formation energy](../../docs/computational-materials-science/point-defects/charged-defect-formation-energy.md) | 전하 상태의 하한 포락선·negative-U 예제와 점유 조건 | pass |
| [NEGF: Büttiker probe method](../../docs/computational-materials-science/quantum-transport/buttiker-probe-method.md) | 단일 probe 재주입·분포, 전하·열 보존 차이와 Schur 제거 | pass |
| [NEGF: Formulation](../../docs/computational-materials-science/quantum-transport/negf-formalism.md) | 비대칭 결합의 전달률, 단일 준위 점유와 전류 적분 | pass |
| [NEGF: Recursive Green's function](../../docs/computational-materials-science/quantum-transport/recursive-greens-function.md) | 두 slice 역행렬, 가변 크기 블록, 전달률 검산 | pass |
| [NEGF: Surface Green's function](../../docs/computational-materials-science/quantum-transport/surface-greens-function.md) | Retarded branch, 유한 사슬 극한, 비직교 결합과 경계 검산 | pass |
| [Memory device: NAND basic](../../docs/device-physics/memory-device/nand.md) | SLC 판독 여유, FN 전기장 민감도와 pulse 적분 | pass |
| [MOSFET: Overview](../../docs/device-physics/mosfet/basic-operation.md) | 채널 전위 분포, 전류·소신호 계산과 포화 적용 한계 | pass |

정량 기준은 각 검토 등록 시 도구가 산출한 동료 문서 기준으로 평가했다. 상세 값과 출처·검산 근거는 문서별 evidence 및 registry에 보존했다.

## 개선한 문서: 33개

- [Electronic structure: Electron localization function](../../docs/computational-materials-science/electronic-structure/electron-localization-function.md)
- [Electronic structure: Hartree–Fock method](../../docs/computational-materials-science/electronic-structure/hartree-fock-method.md)
- [Many-body perturbation theory: GW approximation](../../docs/computational-materials-science/many-body-perturbation/gw-approximation.md)
- [Molecular dynamics: Overview](../../docs/computational-materials-science/molecular-simulation/overview.md)
- [Point defects: Charged defect formation energy](../../docs/computational-materials-science/point-defects/charged-defect-formation-energy.md)
- [Point defects: Nonradiative multiphonon emission](../../docs/computational-materials-science/point-defects/nonradiative-multiphonon-emission.md)
- [NEGF: Büttiker probe method](../../docs/computational-materials-science/quantum-transport/buttiker-probe-method.md)
- [BTE: Carrier mobility from first principles](../../docs/computational-materials-science/quantum-transport/carrier-mobility.md)
- [NEGF: Inelastic electron–phonon scattering](../../docs/computational-materials-science/quantum-transport/electron-phonon-coupling.md)
- [NEGF: Formulation](../../docs/computational-materials-science/quantum-transport/negf-formalism.md)
- [NEGF: Recursive Green's function](../../docs/computational-materials-science/quantum-transport/recursive-greens-function.md)
- [NEGF: Surface Green's function](../../docs/computational-materials-science/quantum-transport/surface-greens-function.md)
- [Electronic transport regimes](../../docs/computational-materials-science/quantum-transport/transport-regimes.md)
- [AI agents: LangChain and LangGraph](../../docs/computational-science/ai-agents/langchain-langgraph.md)
- [Geometric deep learning: Crystal graph convolutional neural networks](../../docs/computational-science/geometric-deep-learning/crystal-graph-convolutional-neural-networks.md)
- [Geometric deep learning: Graph neural networks](../../docs/computational-science/geometric-deep-learning/graph-neural-networks.md)
- [Geometric deep learning: e3nn](../../docs/computational-science/geometric-deep-learning/symmetry-aware-approaches-e3nn.md)
- [Device reliability: Hot-carrier degradation](../../docs/device-physics/device-reliability/hot-carrier-degradation.md)
- [Device reliability: Interconnect reliability](../../docs/device-physics/device-reliability/interconnect-reliability.md)
- [Device reliability: Reliability modeling](../../docs/device-physics/device-reliability/reliability-modeling.md)
- [Device reliability: Time-dependent dielectric breakdown](../../docs/device-physics/device-reliability/time-dependent-dielectric-breakdown.md)
- [Logic technology: Logic DTCO](../../docs/device-physics/logic-technology/logic-dtco.md)
- [Logic technology: Standard-cell architecture](../../docs/device-physics/logic-technology/standard-cell-architecture.md)
- [Memory device: DRAM advance](../../docs/device-physics/memory-device/dram-advance.md)
- [Memory device: DRAM basic](../../docs/device-physics/memory-device/dram.md)
- [Memory device: NAND advance](../../docs/device-physics/memory-device/nand-advance.md)
- [Memory device: NAND basic](../../docs/device-physics/memory-device/nand.md)
- [Memory device: SRAM advance](../../docs/device-physics/memory-device/sram-advance.md)
- [Memory device: SRAM basic](../../docs/device-physics/memory-device/sram.md)
- [MOSFET: Overview](../../docs/device-physics/mosfet/basic-operation.md)
- [MOSFET: Short-channel effects](../../docs/device-physics/mosfet/short-channel-effects.md)
- [Semiconductor process: Doping and annealing](../../docs/device-physics/semiconductor-process/doping-and-annealing.md)
- [Semiconductor process: Etching](../../docs/device-physics/semiconductor-process/etching.md)

## 유지한 문서: 12개

- [Density functional theory](../../docs/computational-materials-science/electronic-structure/density-functional-theory.md)
- [BTE: Formulation and parameters](../../docs/computational-materials-science/quantum-transport/boltzmann-transport-equation.md)
- [Fourier neural operator](../../docs/computational-science/neural-operators/fourier-neural-operator.md)
- [Device reliability: Bias temperature instability](../../docs/device-physics/device-reliability/bias-temperature-instability.md)
- [Device reliability: Overview](../../docs/device-physics/device-reliability/overview.md)
- [Logic technology: CMOS](../../docs/device-physics/logic-technology/cmos.md)
- [Memory device: Overview](../../docs/device-physics/memory-device/basics.md)
- [MOSFET: Architecture evolution](../../docs/device-physics/mosfet/architecture-evolution.md)
- [MOSFET: Leakage current](../../docs/device-physics/mosfet/leakage-mechanisms.md)
- [MOS capacitor](../../docs/device-physics/mosfet/mos-capacitor.md)
- [Semiconductor process: Eight major processes](../../docs/device-physics/semiconductor-process/eight-major-processes.md)
- [Semiconductor process: Thin-film deposition](../../docs/device-physics/semiconductor-process/thin-film-deposition.md)

## 기록과 변경 범위

문서별 발견 사항·변경 이유·검증 근거는 [논리 검토 기록](logic-review-2026-09-20.yaml), 현재 품질 상태는 [registry](documents.yaml), 평가 원문은 `refs/quality/evidence/`에 있다. 논리 검토 기록의 중간 실패 이력은 보존했고 최종 상태는 `final_validation`에 별도로 명시했다.

본문 33개와 검토 기록·품질 메타데이터를 갱신했다. 검토 중 발견한 inline 수식의 `<`·`>`를 HTML로 오인해 글자 수를 누락하는 오류는 품질 집계 스크립트와 회귀시험에서 수정했다. 기존 작업의 navigation·skill·CI 등 변경은 이 작업의 신규 변경으로 집계하지 않았다.

미해결 항목은 없다. Commit과 push는 수행하지 않았다.
