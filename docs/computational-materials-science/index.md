# Computational materials science

Computational materials science 영역에서는 원자·전자 수준의 계산 방법으로 재료의 구조와 물성을 해석한다. 현재 electronic structure, excited-state physics, molecular simulation, defect physics와 transport physics를 다룬다.

## 문서 목록

### Electronic structure

- [Hartree–Fock method](electronic-structure/hartree-fock-method.md) — 단일 Slater determinant 변분, Coulomb·exchange, Fock equation과 SCF 계산
- [Electron localization function](electronic-structure/electron-localization-function.md) — 같은 스핀 조건부 pair density에서 ELF를 유도하고, HEG 정규화, 실공간 topology, 계산 절차와 해석 한계를 설명

### Excited-state physics

- [GW approximation](many-body-perturbation/gw-approximation.md) — quasiparticle, Hedin equations, $G_0W_0$ 계산과 self-consistency·수렴·적용 범위

### Molecular simulation

- [Molecular dynamics: Overview](molecular-simulation/overview.md) — classical MD와 AIMD, statistical ensemble, 시간 간격 및 평형·표본화의 판단 기준

### Defect physics

- [Charged defect formation energy](point-defects/charged-defect-formation-energy.md) — charged defect formation energy, charge-transition level, FNV/eFNV finite-size correction과 equilibrium concentration
- [Nonradiative multiphonon emission](point-defects/nonradiative-multiphonon-emission.md) — deep defect의 electron–phonon coupling, nonradiative capture rate와 first-principles capture-coefficient calculation

### Transport physics

- [Electronic transport regimes](quantum-transport/transport-regimes.md) — ballistic, quasi-ballistic, diffusive transport를 길이 척도와 Landauer·BTE·drift–diffusion 지배식으로 비교
- [Carrier mobility from first principles](quantum-transport/carrier-mobility.md) — 전자구조와 electron–phonon coupling에서 BTE mobility를 계산하는 근사 계층, 수렴 절차와 mean free path 해석
- [NEGF formalism](quantum-transport/negf-formalism.md) — 전극 self-energy, 비평형 점유, density matrix와 단자 전류
- [Surface Green's function](quantum-transport/surface-greens-function.md) — 반무한 전극의 표면 응답과 López Sancho repeated-doubling
- [Recursive Green's function](quantum-transport/recursive-greens-function.md) — block-tridiagonal 소자의 재귀 계산과 Poisson–NEGF 소자 모사
- [Electron–phonon coupling](quantum-transport/electron-phonon-coupling.md) — 전자–포논 수송 Hamiltonian과 SCBA, LOE, Büttiker probe, MD–Landauer의 이론·근사·검증 기준
- [Büttiker probe method](quantum-transport/buttiker-probe-method.md) — fictitious terminal의 영전류 조건, voltage·dephasing probe와 NEGF 구현·검증
