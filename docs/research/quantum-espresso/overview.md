---
description: SIESTA 사용자를 위해 Quantum ESPRESSO의 입력·출력 구조와 구조 최적화 및 전자구조 후처리 흐름을 연결해 설명하는 개요
---

# Quantum ESPRESSO: Overview

Quantum ESPRESSO (QE)는 density functional theory (DFT), plane wave basis와 pseudopotential을 바탕으로 한 여러 실행 프로그램의 모음이다. 이 글은 SIESTA에서 구조 최적화와 전자구조 분석을 해 본 독자가 QE의 파일과 실행 단계를 대응시킬 수 있도록 `pw.x` 중심의 ground-state workflow를 설명한다. 설치와 성능 조정은 범위에서 제외하며, 명령을 실제로 실행해 검증한 기록도 아니다. 프로그램 동작과 파일 형식은 2026년 9월에 직접 확인한 QE 7.5 온라인 input description과 공식 예제에 맞추되, 설치된 버전의 `INPUT_*.html`을 최종 기준으로 삼아야 한다.[1,2]

이 글에서 Fast Fourier transform (FFT)은 reciprocal-space와 real-space grid 사이의 변환, self-consistent field (SCF)는 전자 밀도를 반복 수렴시키는 계산, non-self-consistent field (NSCF)는 고정된 수렴 밀도에서 추가 $k$-point의 상태를 구하는 계산을 뜻한다. Unified Pseudopotential Format (UPF)은 QE pseudopotential container이다. Density of states (DOS)는 energy별 상태 수, projected density of states (PDOS)는 orbital projector로 분해한 DOS, local density of states (LDOS)는 위치와 energy에 따른 상태 밀도, integrated local density of states (ILDOS)는 정한 energy 구간에서 적분한 LDOS이다. Equation of state (EOS)는 energy와 volume의 관계를 fitting해 평형 volume과 bulk modulus를 얻는 모형이다.

## 1. 계산 모형과 프로그램 구성

### (1) Plane wave 기준의 차이

QE의 Plane-Wave Self-Consistent Field (PWscf)는 Kohn–Sham orbital을 plane wave로 전개하고, core–valence 상호작용을 norm-conserving (NC), ultrasoft (US) pseudopotential 또는 projector augmented-wave (PAW) dataset으로 표현한다. 따라서 basis 수렴의 중심 변수는 SIESTA의 orbital range·zeta·polarization 구성이 아니라 wavefunction cutoff `ecutwfc`, charge-density cutoff `ecutrho`, 그리고 $k$-point sampling이다.[2,3]

SIESTA는 finite-support numerical atomic orbital을 basis로 사용하고 charge density와 potential의 일부 연산에 real-space grid를 쓴다. 그러므로 두 코드의 `Ry` 단위 cutoff를 같은 물리량으로 해석하면 안 된다. SIESTA의 `MeshCutoff`는 주로 real-space integration grid의 세밀함을 정하지만, QE의 `ecutwfc`는 plane-wave orbital basis를 직접 자른다. QE의 `ecutrho`는 density와 potential용 FFT grid를 정하며 pseudopotential 종류에 따라 `ecutwfc`보다 더 커야 한다.[3–5]

### (2) 실행 프로그램의 연결

QE에서는 한 실행 파일이 모든 분석을 끝내기보다, ground-state 결과를 `prefix.save`에 저장하고 후속 executable이 이를 읽는다. SIESTA의 한 번의 실행과 여러 `SystemLabel.*` 출력에 익숙하다면, QE에서는 **공유 save directory를 매개로 작은 프로그램을 이어 붙인다**고 이해하는 편이 정확하다.[1,2]

| 단계 | 주 실행 프로그램 | 핵심 역할 | 대표 후속 결과 |
| --- | --- | --- | --- |
| Ground state·구조 최적화 | `pw.x` | SCF, NSCF, bands, `relax`, `vc-relax` | 표준 출력, `outdir/prefix.save/` |
| Total DOS | `dos.x` | 저장된 eigenvalue와 $k$-point weight로 DOS 적분 | energy–DOS 1D 표 |
| Band 후처리 | `bands.x` | band ordering과 plot용 자료 정리 | `filband`, `filband.gnu` |
| Atomic-orbital projection | `projwfc.x` | Löwdin projection과 PDOS | atom·projector별 1D 표, `atomic_proj.xml` |
| Real-space field | `pp.x` | charge density, LDOS, potential 등을 절단·변환 | 1D/2D 표 또는 3D XCrySDen Structure File (XSF)/Cube grid |
| Equation-of-state fitting | `ev.x` | 사용자가 만든 $E(V)$ 자료를 EOS에 fitting | $V_0$, $B_0$와 fitted curve 자료 |

이 분리는 SIESTA의 `.EIG`, `.bands`, `.PDOS`, `.RHO`, `.VH`, `.VT`를 각각 만드는 기능이 사라진다는 뜻이 아니다. 같은 물리량을 생성하는 시점과 도구가 `pw.x`와 PostProc package로 나뉜다는 뜻이다.[1,5,6]

### (3) SIESTA에서 옮길 때의 대응 지도

아래 표는 입력을 기계적으로 번역하는 사전이 아니라, 같은 목적의 설정과 결과가 QE workflow의 어느 단계에 놓이는지를 찾는 지도이다. 특히 basis와 grid, orbital projection은 정의가 다르므로 “가까운 대응”을 “같은 수치”로 해석하지 않는다.[4–16]

| SIESTA 개념·keyword·파일 | QE의 가까운 대응 | 옮길 때 확인할 점 |
| --- | --- | --- |
| `SystemLabel` | `prefix` | 후속 executable 모두 같은 `prefix/outdir`를 읽어야 한다 |
| `LatticeVectors`, fractional coordinate | `CELL_PARAMETERS`, `ATOMIC_POSITIONS (crystal)` | vector 방향, 길이 단위, 원자 순서를 함께 검사한다 |
| Pseudo-atomic orbital (PAO) basis 설정 | UPF + `ecutwfc` | basis 정의가 달라 직접 변환할 수 없다 |
| `MeshCutoff` | `ecutrho`와 FFT grid에 부분적으로 대응 | `ecutwfc`의 plane-wave orbital cutoff와 구분한다 |
| `kgrid.MonkhorstPack` | `K_POINTS (automatic)` | grid division뿐 아니라 shift convention도 확인한다 |
| `MD.TypeOfRun` fixed-cell optimization | `calculation='relax'` + `&IONS` | optimizer 이름과 종료 조건은 일대일 대응이 아니다 |
| `MD.VariableCell` | `calculation='vc-relax'` + `&CELL` | 허용 cell freedom과 목표 pressure를 명시한다 |
| `.EIG`/DOS 처리 | `nscf` → `dos.x` → `fildos` | DOS용 uniform mesh와 broadening을 별도로 기록한다 |
| `BandLines`, `.bands` | `bands` → `bands.x` → `filband.gnu` | reciprocal coordinate와 cell convention을 맞춘다 |
| `SystemLabel.PDOS(.xml)` | `projwfc.x`의 `pdos_atm...`, `atomic_proj.xml` | projection orbital과 orthogonalization 정의가 다르다 |
| `SystemLabel.LDOS` | `pp.x plot_num=10` | 둘 다 energy-window-integrated real-space field이다 |
| `.RHO`, `.VH`, `.VT` | `pp.x plot_num=0,11,1` | density와 두 potential의 성분·단위를 구분한다 |

### (4) 계산 단계의 의존성

각 postprocessor는 input text만 읽는 독립 프로그램이 아니다. 아래의 upstream `pw.x` 단계가 같은 `prefix.save`에 남긴 structure, eigenvalue, density 또는 wavefunction을 소비한다.[8–10,12,14,17–19]

| 목표 | 필요한 upstream 단계 | 실행 프로그램 | 핵심 산출물 | 다음 단계 전 검산 |
| --- | --- | --- | --- | --- |
| Total DOS | `scf` → dense uniform-grid `nscf` | `dos.x` | `fildos`, energy 1D table | energy range, smearing/tetrahedra, states/eV |
| Band dispersion | `scf` → path `bands` | `bands.x` | `filband.gnu`, path 1D table | path/cell convention, `nbnd`, eV |
| Atomic PDOS | `scf` → dense uniform-grid `nscf` | `projwfc.x` | `pdos_atm...`, energy 1D tables | projector label, spin convention, states/eV |
| Charge/potential | converged `scf` | `pp.x` | sampled spatial field | `plot_num`, component, cell and grid |
| Real-space LDOS/ILDOS | wavefunctions on the chosen $k$-mesh | `pp.x` | energy-resolved or integrated spatial field | energy window, energy zero, grid |
| EOS | independent, consistently converged $E(V)$ jobs | `ev.x` | fitted parameters and pointwise residuals | actual volume, energy unit, fit interval |

```text
pw.x scf ─┬─> pw.x nscf (dense uniform k mesh) ─┬─> dos.x
          │                                      └─> projwfc.x
          ├─> pw.x bands (high-symmetry path) ─────> bands.x
          ├─> pp.x (charge, potential, LDOS/ILDOS)
          └─> repeated fixed-volume jobs ──────────> E(V) table ─> ev.x
```

이 흐름도에서 화살표는 shell pipe가 아니라 저장 자료의 의존성을 뜻한다. `nscf`와 `bands`는 목적이 다르며, 앞 단계와 다른 `outdir`를 쓰거나 오래된 `prefix.save`를 섞으면 새 input이 맞아도 결과 provenance가 끊어진다.[8,17]

## 2. `pw.x` 입력 구조

### (1) Namelist와 card

`pw.x` 입력은 Fortran namelist와 card를 정해진 순서로 배치한다. `&CONTROL`은 calculation type과 파일 경로, `&SYSTEM`은 cell·원자 수·cutoff·occupation, `&ELECTRONS`는 SCF 알고리즘을 정의한다. 구조 최적화에서는 `&IONS`, variable-cell 계산에서는 `&CELL`이 추가된다. 이어서 `ATOMIC_SPECIES`, `ATOMIC_POSITIONS`, `K_POINTS`, 필요하면 `CELL_PARAMETERS` 등의 card를 둔다. Namelist는 `/`로 닫지만 card는 닫는 표식이 없으며, unit option은 `ATOMIC_POSITIONS (crystal)`처럼 card 이름과 띄어 쓴다.[6,20]

SIESTA의 Flexible Data Format (FDF)는 keyword 순서가 비교적 자유롭고 `%block`을 사용한다. QE namelist는 이름이 같은 변수라도 어느 namelist에 속하는지가 문법의 일부이며, `ATOMIC_SPECIES`의 pseudopotential filename은 `pseudo_dir` 아래 실제 파일과 일치해야 한다. 두 코드 모두 species label이 구조의 원자와 pseudopotential을 연결하지만, QE에서는 basis orbital 정의가 별도 input block에 있지 않고 plane-wave cutoff와 UPF dataset에 의해 결정된다.[4,6,20]

### (2) 주석을 단 SCF 예제

아래는 diamond Si primitive cell을 `ibrav=0`으로 직접 적은 교육용 입력이다. `Si.UPF`는 선택한 Si UPF 파일을 로컬에서 그렇게 이름 붙였다는 뜻이다. `ecutwfc=50 Ry`, `ecutrho=400 Ry`, $8\times8\times8$ grid는 문법과 변수 관계를 보여 주는 값이며, 특정 pseudopotential이나 목표 오차에 대해 검증된 production parameter가 아니다.[6,20,21]

```fortran
&CONTROL
  calculation = 'scf'       ! 고정 구조의 self-consistent ground state
  prefix      = 'si'        ! 후속 단계가 공유할 dataset 이름
  pseudo_dir  = './pseudo'  ! Si.UPF를 찾는 directory
  outdir      = './tmp'     ! si.save가 생기는 scratch directory
  tprnfor     = .true.      ! 표준 출력에 force를 계산·기록
  tstress     = .true.      ! 표준 출력에 stress를 계산·기록
  disk_io     = 'low'
/
&SYSTEM
  ibrav    = 0              ! CELL_PARAMETERS를 직접 제공
  nat      = 2
  ntyp     = 1
  ecutwfc  = 50.0           ! wavefunction cutoff, Ry
  ecutrho  = 400.0          ! charge-density cutoff, Ry
  occupations = 'fixed'     ! 이 예제는 절연체 Si를 가정
/
&ELECTRONS
  conv_thr    = 1.0d-10
  mixing_beta = 0.7
/

ATOMIC_SPECIES
Si  28.085  Si.UPF

CELL_PARAMETERS (angstrom)
0.0000  2.7155  2.7155
2.7155  0.0000  2.7155
2.7155  2.7155  0.0000

ATOMIC_POSITIONS (crystal)
Si  0.00  0.00  0.00
Si  0.25  0.25  0.25

K_POINTS (automatic)
8 8 8  0 0 0
```

`ibrav=0`은 SIESTA의 `LatticeVectors`와 가장 가까운 표현이다. Fractional coordinate인 `crystal`은 SIESTA의 `AtomicCoordinatesFormat Fractional`에 대응한다. 반대로 QE의 `ibrav`와 `celldm`/`A,B,C`를 쓰면 Bravais lattice를 압축해 지정할 수 있지만, `ibrav=0`과 `CELL_PARAMETERS`를 동시에 이해하는 편이 구조 변환과 version 간 재현에 유리하다. Cell vector는 symmetry detection이 깨지지 않도록 충분한 자릿수로 기록해야 한다.[6,20]

!!! warning "검증 범위"
    이 문서는 QE를 설치하거나 위 입력을 실행하지 않았다. 실제 계산에서는 선택한 UPF의 exchange–correlation functional, valence configuration, relativistic treatment와 권장 cutoff를 확인하고, `ecutwfc`, `ecutrho`, $k$-mesh, smearing을 목표 물성에 대해 독립적으로 수렴시켜야 한다.[21–23]

### (3) $k$-point sampling

`K_POINTS (automatic)` 다음의 여섯 정수는 `nk1 nk2 nk3 sk1 sk2 sk3`이다. 앞의 세 값은 Monkhorst–Pack형 uniform grid의 분할 수이고, 뒤의 세 값은 각 방향에 적용하는 QE의 0/1 shift flag이다. 이 flag를 grid 분할 수와 함께 기록하고 실제로 생성된 $k$-point mesh와 출력을 확인한다. `K_POINTS gamma`는 $\Gamma$만 사용하는 별도 경로이고, `K_POINTS crystal`은 reciprocal lattice fractional coordinate와 weight를 직접 받는다.[6,24,25]

SCF energy, force, stress와 DOS는 Brillouin zone 적분이므로 uniform mesh를 물성별로 수렴시켜야 한다. Band plot의 high-symmetry path는 적분 grid가 아니라 표본 경로이므로, SCF를 path만으로 대체할 수 없다. 일반적인 bands workflow는 uniform grid의 `scf`로 density를 얻은 뒤 `calculation='bands'`와 `K_POINTS crystal_b` 또는 `tpiba_b`로 경로의 eigenvalue를 계산한다. 이는 SIESTA에서 SCF용 `kgrid.MonkhorstPack`과 plot용 `BandLines`를 구분하는 것과 같은 원칙이다.[6,7,24,25]

| 계산 목적 | 권장되는 `K_POINTS` 역할 | 결과에 직접 영향을 주는 검산 항목 |
| --- | --- | --- |
| SCF energy·force·stress | `automatic` uniform integration mesh | grid density와 shift를 함께 수렴시킨다 |
| Total DOS·PDOS | 보통 SCF보다 조밀한 `nscf` uniform mesh | tetrahedra 사용 시 적합한 자동 uniform grid인지 확인한다 |
| Band plot | `crystal_b` 또는 `tpiba_b`의 ordered path | endpoint, 구간별 점 수, reciprocal coordinate convention을 기록한다 |
| 큰 고립계 | `gamma`를 후보로 검토 | supercell 크기와 dispersion을 확인한 뒤 $\Gamma$-only 근사를 정당화한다 |

Grid의 숫자를 다른 cell 표현에 그대로 복사하면 $k$-point 밀도가 바뀔 수 있다. Primitive cell과 conventional cell 사이를 변환했다면 reciprocal-vector 길이와 실제 irreducible point 수까지 다시 확인한다.[6,24]

## 3. Pseudopotential 선택과 UPF

### (1) 형식과 세 종류

QE의 기본 교환 형식은 UPF이다. UPF 2.x는 Extensible Markup Language (XML)와 비슷한 text container에 radial grid, local potential, nonlocal projector, pseudo-wavefunction과 필요한 augmentation/PAW 정보를 저장하며 NC, US, PAW dataset을 한 형식으로 표현한다. 형식 명세 자체도 개정 중이므로 file extension만 믿기보다 UPF header의 type, functional, relativistic treatment, valence state와 생성 정보를 읽어야 한다.[2,21]

| 종류 | 계산적 특징 | SIESTA 사용자에게 중요한 차이 |
| --- | --- | --- |
| NC | pseudo-wavefunction의 norm을 보존하며 대체로 더 높은 `ecutwfc`가 필요할 수 있다 | SIESTA가 전통적으로 사용하는 norm-conserving pseudopotential과 개념적으로 가장 가깝다 |
| US | augmentation charge를 도입해 더 부드러운 wavefunction을 허용한다 | `ecutrho/ecutwfc` 비를 임의로 4에 고정하지 말고 dataset 권고와 수렴 시험을 따른다 |
| PAW | transformation/augmentation dataset으로 all-electron 성질을 재구성한다 | `projwfc.x`의 `pawproj`와 `pp.x`의 PAW 전용 all-electron density option은 별도 의미를 가진다 |

SIESTA는 norm-conserving pseudopotential을 사용하며 `.vps`, `.psf`, `.psml` 형식을 지원한다. PseudoDojo의 curated Pseudopotential Markup Language (PSML) dataset도 사용할 수 있고, PSML을 선택했다면 SIESTA 5.4 manual은 그 파일에 든 local potential과 projector를 유지하도록 권고한다. QE는 NC뿐 아니라 US와 PAW도 읽으므로, SIESTA input을 옮길 때 chemical symbol과 functional만 맞추고 pseudopotential family를 무심코 바꾸면 basis cutoff, valence electron 수, spin–orbit treatment와 결과의 비교 조건까지 달라진다.[4,7,21,26]

### (2) 입수처와 선택 기록

QE 공식 pseudopotential page는 NC·US·PAW 지원을 설명하고, 검증된 후보로 Standard Solid-State Pseudopotentials (SSSP)를 안내한다. SSSP는 여러 공개 library의 dataset을 동일한 solid-state verification과 plane-wave convergence protocol로 비교하여 efficiency와 precision collection을 제공한다. 이는 “한 generator가 모든 원소에서 항상 최선”이라고 가정하는 library가 아니라 검증 결과로 원소별 dataset과 cutoff를 고른 collection이다.[21–23]

PseudoDojo는 optimized norm-conserving Vanderbilt dataset을 체계적으로 생성·검사하며 QE용 UPF를 제공한다. PSlibrary는 QE의 `ld1.x` input을 배포하여 scalar/fully relativistic US와 PAW dataset을 생성하는 library이다. 연구 기록에는 library 이름만 쓰지 말고 정확한 version, filename, checksum, exchange–correlation functional, relativistic level, valence configuration과 사용한 cutoff를 남겨야 한다.[22,26,27]

!!! note "실용적인 선택 순서"
    먼저 동일한 functional·relativistic 조건을 만족하는 검증 library를 고르고, 조성의 모든 원소가 한 계산 목적에 맞는지 확인한다. 이어서 library 권장 cutoff를 시작점으로 삼아 energy뿐 아니라 force·stress 또는 band quantity까지 수렴시킨다. SIESTA와 QE를 비교할 때에는 가능하면 같은 norm-conserving operator를 PSML/UPF로 공급하거나, 그렇지 못하면 pseudopotential 차이를 code 차이와 분리해 보고한다.[22,23,26]

## 4. 표준 출력과 save directory

### (1) 사람이 읽는 표준 출력

`pw.x -in input.in > output.out`처럼 redirect한 표준 출력은 input 요약, lattice와 symmetry, FFT grid와 plane-wave 수, SCF iteration, eigenvalue/occupation, energy decomposition, convergence, force·stress와 timing을 순서대로 보여 준다. Converged SCF energy는 관례적으로 `!    total energy = ... Ry` 줄에서 찾고, force는 `Forces acting on atoms (cartesian axes, Ry/au)`, stress는 `total stress (Ry/bohr**3) (kbar)` 표에서 읽는다.[20,28]

| 출력량 | 표준 출력의 대표 단위 | 읽을 때의 주의점 |
| --- | --- | --- |
| Total energy | Ry | 마지막 `! total energy`와 SCF convergence 여부를 함께 확인한다 |
| Force component | Ry/Bohr (`Ry/au`) | `Total force`만으로 원자별 최대 성분을 대신하지 않는다 |
| Stress tensor | Ry/Bohr$^3$와 kbar | 압력 $P$와 Cartesian tensor를 구분한다 |
| Eigenvalue·Fermi energy | 보통 eV로 명시 | calculation type과 occupation method를 함께 기록한다 |

QE input description에서 별도 dimension을 적지 않은 양은 Rydberg atomic unit을 쓴다. 그러나 postprocessor는 항상 같은 단위를 쓰지 않는다. 예를 들어 `dos.x`와 `projwfc.x` 표의 energy는 eV이고 DOS는 states/eV인 반면, `pp.x` field는 따로 적지 않으면 Rydberg atomic unit이며 potential은 전압 $V$가 아니라 electron charge가 곱해진 energy $eV$ 차원이다.[6,8–10]

### (2) 기계가 읽는 `prefix.save`

`outdir/prefix.save/`는 후속 계산과 restart를 위한 dataset이다. `data-file-schema.xml`은 구조·$k$-point·eigenvalue·계산 설정 등의 metadata를 담는다. Density와 wavefunction 등 나머지 restart payload는 구현에 따라 달라질 수 있으므로 filename layout을 가정하지 말고 documented reader를 통해 소비한다.[3,8,17]

```text
./tmp/si.save/
├── data-file-schema.xml       # 구조·격자·전자상태 metadata
└── <implementation-dependent payloads>
    # density, wavefunction, pseudopotential 관련 restart 자료
```

표준 출력은 사람이 계산 진행과 실패 원인을 읽기 좋고, XML/save dataset은 `dos.x`, `bands.x`, `projwfc.x`, `pp.x`가 다시 계산 결과를 소비하기 좋다. 자동화에서는 stdout의 공백과 문구를 고정 schema처럼 parsing하기보다 `data-file-schema.xml` 또는 검증된 parser를 우선하고, 3D density는 `pp.x`로 명시적인 XSF/Cube 등의 교환 형식으로 내보내는 편이 안전하다.[8,17]

## 5. 구조 최적화와 equation of state

### (1) `relax`와 `vc-relax`

`calculation='relax'`는 cell을 고정하고 ionic coordinate를 최적화한다. `calculation='vc-relax'`는 ion과 허용된 cell degree of freedom을 함께 바꾸며, `&CELL`의 `cell_dynamics`, `press`, `press_conv_thr`, `cell_dofree`가 cell update를 제어한다. 두 경우 모두 ionic step마다 SCF가 들어가므로 `etot_conv_thr`와 `forc_conv_thr`는 전자 SCF의 `conv_thr`와 다른 계층의 종료 조건이다.[2,6,29]

앞의 SCF 예제에서 fixed-cell relaxation으로 바꾸는 최소 delta는 다음과 같다. 아래 `<...>`는 실제 수렴 목표로 치환해야 하는 placeholder이며, 구조·species·cutoff·$k$-mesh block은 그대로 필요하다.[6,29]

```fortran
&CONTROL
  calculation   = 'relax'
  prefix         = 'si'
  pseudo_dir     = './pseudo'
  outdir         = './tmp'
  tprnfor        = .true.
  tstress        = .true.
  etot_conv_thr  = <ionic_energy_threshold_Ry>
  forc_conv_thr  = <force_threshold_Ry_per_Bohr>
/
&IONS
  ion_dynamics = 'bfgs'
/
```

Cell도 움직이는 경우에는 calculation type을 바꾸고 `&CELL`을 추가한다. `cell_dofree='all'`은 예시일 뿐이며, slab·wire·고정 shape EOS처럼 constraint가 있는 문제에서는 그대로 쓰면 안 된다.[6,29]

```fortran
&CONTROL
  calculation   = 'vc-relax'
  prefix         = 'si'
  pseudo_dir     = './pseudo'
  outdir         = './tmp'
  tprnfor        = .true.
  tstress        = .true.
  etot_conv_thr  = <ionic_energy_threshold_Ry>
  forc_conv_thr  = <force_threshold_Ry_per_Bohr>
/
&IONS
  ion_dynamics = 'bfgs'
/
&CELL
  cell_dynamics  = 'bfgs'
  press          = <target_pressure_kbar>
  press_conv_thr = <pressure_threshold_kbar>
  cell_dofree    = 'all'
/
```

두 입력 차이는 SIESTA의 구조 최적화와 variable-cell 설정에 대응시켜 이해할 수 있다. 다만 keyword를 일대일 번역해서는 안 된다. QE의 `cell_dofree`는 cell shape constraint를 명시하고, `vc-relax`의 최종 cell과 coordinate는 stdout과 XML의 마지막 configuration에서 확인해야 한다.[6,7]

### (2) $E(V)$ workflow와 `ev.x`

EOS는 여러 volume에서 얻은 total energy를 $E(V)$ 모형에 fitting하는 workflow이다. 평형 volume $V_0$ 근처의 bulk modulus는 선택한 EOS 모형 안에서 다음 곡률과 연결된다.

$$
B_0 = V_0\left.\frac{\partial^2 E}{\partial V^2}\right|_{V_0}.
$$

이 식에서 $E$는 각 고정 volume의 일관된 electronic total energy이고, $V$는 unit-cell volume이다. 실제 fitting은 유한한 점과 특정 Birch/Murnaghan 계열 함수에 의존하므로, $V_0$와 $B_0$에는 sampling 범위·점 수·relaxation constraint·cutoff·$k$-mesh 규약을 함께 기록해야 한다.[30–32]

**QE 기본 배포판에는 `pw.x calculation='eos'`처럼 volume 생성부터 fitting까지 수행하는 단일 calculation mode가 없다.** `ev.x`는 이미 계산한 lattice parameter–energy 또는 volume–energy 표를 여러 EOS 형태에 fitting하는 보조 프로그램이며, 각 volume의 `pw.x` job을 만들거나 실행하지 않는다. 따라서 SIESTA의 `aiida-siesta` `EqOfStateFixedCellShape` WorkChain과 같은 orchestration을 기대한다면 shell/Python 또는 AiiDA workflow를 별도로 써야 한다.[1,30,31,33]

재현 가능한 순서는 다음과 같다.

1. 예상 $V_0$ 주변의 scale factor 집합을 정하고 cell shape를 고정할지 함께 바꿀지 결정한다.
2. 각 volume에서 같은 UPF, cutoff, smearing과 비교 가능한 $k$-point density를 사용한다.
3. EOS 목적이 “고정 shape에서 내부 좌표가 완화된 $E(V)$”라면 cell volume은 고정한 채 ion만 `relax`한다. `vc-relax`로 각 점을 다시 영압까지 보내면 서로 다른 volume 표본이 유지되지 않는다.
4. 각 job의 **수렴한 마지막 total energy**와 실제 volume을 모아 `ev.x` 또는 검증된 fitting library에 넣는다.
5. fitted minimum이 sampling interval 안에 있고 residual이 한쪽으로 치우치지 않는지 확인한다.

EOS fitting에 넘길 최소 자료는 실제 volume과 수렴한 total energy의 두 열이다. 아래 값은 계산 결과가 아니라 stdout/XML에서 얻은 값으로 치환해야 하는 placeholder이다. `ev.x`는 선택한 구조 mode에 따라 첫 열을 lattice parameter 또는 volume으로 읽으므로, 설치본 prompt와 단위를 확인한 뒤 header 없는 입력 파일을 만든다. 다른 fitting library를 쓰면 그 library가 요구하는 energy·volume 단위로 명시적으로 변환한다.[30–32,34]

```text
<V_1_in_Angstrom^3>  <E_1_in_Ry>
<V_2_in_Angstrom^3>  <E_2_in_Ry>
<V_3_in_Angstrom^3>  <E_3_in_Ry>
...
<V_N_in_Angstrom^3>  <E_N_in_Ry>
```

`ev.x`나 다른 EOS fitter의 결과는 다음 기준으로 읽는다. 세부 output label과 제공되는 derivative는 program·version·선택한 EOS에 따라 달라지므로, 고정된 열 번호에 의존하지 않는다.[30–32,34]

| Fitting 결과 | 의미 | 검산 질문 |
| --- | --- | --- |
| EOS 함수와 residual | 선택한 함수가 각 계산점을 얼마나 잘 설명하는지 나타낸다 | 다른 함수나 fitting 범위에서도 minimum이 안정적인가 |
| $V_0$, $E_0$ | fitted 평형 volume과 minimum energy | $V_0$가 표본 범위 안에 있는가 |
| $B_0$ | $V_0$에서의 energy curvature로 얻은 bulk modulus | cutoff와 $k$-mesh 수렴 오차보다 안정적인가 |
| Pointwise $E-E_{\mathrm{fit}}$ | 각 계산점의 residual | 한쪽 volume 방향으로 체계적인 추세가 없는가 |

`vc-relax`는 목표 pressure에서 하나의 평형 cell을 찾는 데 적합하지만 EOS curve 자체는 아니다. SIESTA의 variable-cell relaxation과 SIESTA/AiiDA EOS WorkChain도 같은 구분을 갖는다. 하나는 stress를 줄이는 최적화이고, 다른 하나는 여러 volume의 energy를 모으는 workflow이다.[7,31,33]

## 6. DOS와 band structure

### (1) Total DOS

DOS는 $k$-point weight $w_{\mathbf{k}}$를 포함해 Kohn–Sham eigenvalue를 energy 축에 모은 양이다.

$$
D(E)=\sum_{n\mathbf{k}} w_{\mathbf{k}}\,\delta(E-\varepsilon_{n\mathbf{k}}).
$$

$n$은 band index이고 $\mathbf{k}$는 Brillouin zone 표본이며, $\delta$는 적분할 때 각 eigenvalue의 기여를 그 energy에 놓는 Dirac delta이다. 이 식은 spin index와 degeneracy factor를 생략한 축약형이다. 실제 spin-summed 또는 spin-resolved 정규화는 계산의 spin mode, $k$-point weight와 출력 column convention을 따르므로, DOS를 적분해 전자 수를 검산할 때 그 세 항목을 함께 기록한다. `dos.x`는 Gaussian broadening 또는 tetrahedron 계열 적분을 사용한다. Tetrahedron option은 `pw.x`에서 생성한 적절한 uniform grid가 필요하며, `dos.x`의 `degauss`는 Ry이지만 `Emin`, `Emax`, `DeltaE`와 출력 energy는 eV이다.[9,18,35]

Workflow는 `scf`로 density를 수렴시킨 뒤 더 조밀한 uniform mesh의 `nscf`로 eigenvalue를 만들고 `dos.x`를 실행하는 순서이다. `dos.x`는 wavefunction 자체는 요구하지 않지만 같은 `prefix`와 `outdir`의 saved data를 읽는다. `fildos`는 energy와 total DOS를 담는 1D table이며 DOS 단위는 states/eV이다. SIESTA의 `.EIG`+`Eig2DOS` 또는 `SystemLabel.DOS`에 가까운 결과이지만, QE에서는 SCF와 NSCF mesh를 명시적으로 분리하는 관행이 더 뚜렷하다.[9,11,18]

DOS용 `pw.x` 입력은 앞의 SCF 입력 전체에서 다음 항목을 바꾸는 fragment로 볼 수 있다. 실제 파일에는 동일한 `ATOMIC_SPECIES`, cell, position, 수렴된 cutoff를 다시 포함해야 한다. `nbnd`와 mesh는 필요한 unoccupied energy range에 맞춰 정한다.[6,9,18,35]

```fortran
&CONTROL
  calculation = 'nscf'
  prefix      = 'si'
  pseudo_dir  = './pseudo'
  outdir      = './tmp'
/
&SYSTEM
  ! ibrav, nat, ntyp, ecutwfc, ecutrho는 SCF와 일치시킨다.
  nbnd        = <number_covering_requested_energy_range>
  occupations = 'tetrahedra'
/
&ELECTRONS
  conv_thr = <electronic_threshold>
/
! ATOMIC_SPECIES, CELL_PARAMETERS, ATOMIC_POSITIONS는 생략하지 않는다.
K_POINTS (automatic)
<nk1_dense> <nk2_dense> <nk3_dense> <s1> <s2> <s3>
```

Gaussian broadening을 쓰는 `dos.x` 최소 template은 다음과 같다. `degauss`만 Ry이고 energy window와 `DeltaE`는 eV라는 비대칭을 입력 옆에 기록해 둔다. Tetrahedron workflow라면 설치본 문서의 `bz_sum`/occupation 조합을 확인하고 broadening placeholder를 그대로 사용하지 않는다.[9,35]

```fortran
&DOS
  prefix  = 'si'
  outdir  = './tmp'
  fildos  = 'si.dos.dat'
  Emin    = <lower_energy_eV>
  Emax    = <upper_energy_eV>
  DeltaE  = <energy_step_eV>
  ngauss  = 0
  degauss = <broadening_Ry>
/
```

### (2) Band dispersion

Band structure는 uniform integration grid가 아니라 선택한 reciprocal-space path의 $\varepsilon_{n\mathbf{k}}$를 보여 준다. 먼저 `scf`를 마친 후, 같은 `prefix/outdir`에서 `calculation='bands'`와 충분한 `nbnd`, `K_POINTS crystal_b` 경로를 사용한다. 이어서 `bands.x`는 path 결과를 plot-ready `filband.gnu` 1D table로 정리하며 energy는 eV이다.[10,19,36,37]

Path calculation의 `pw.x` fragment는 다음과 같다. `crystal_b`의 좌표는 reciprocal lattice fractional coordinate이고 각 줄의 마지막 정수는 다음 special point까지의 분할 수이다. 아래 좌표와 분할 수는 물질별 표준 경로로 치환할 placeholder이며, 실제 파일에는 구조와 species card도 다시 포함한다.[6,10,19,36,37]

```fortran
&CONTROL
  calculation = 'bands'
  prefix      = 'si'
  pseudo_dir  = './pseudo'
  outdir      = './tmp'
/
&SYSTEM
  ! SCF와 같은 cell/species/cutoff를 사용한다.
  nbnd = <number_of_bands_to_plot>
/
&ELECTRONS
  conv_thr = <electronic_threshold>
/
! ATOMIC_SPECIES, CELL_PARAMETERS, ATOMIC_POSITIONS는 생략하지 않는다.
K_POINTS (crystal_b)
<number_of_special_points>
<kx_1> <ky_1> <kz_1> <points_to_next_1>
<kx_2> <ky_2> <kz_2> <points_to_next_2>
...
<kx_N> <ky_N> <kz_N> 1
```

그 결과를 읽는 `bands.x` 최소 template은 다음과 같다. `filband`는 base output이고 plot에 사용할 `.gnu` 이름은 설치본과 stdout에서 확인한다.[10,37]

```fortran
&BANDS
  prefix  = 'si'
  outdir  = './tmp'
  filband = 'si.bands.dat'
/
```

SIESTA의 `BandLines`와 `.bands`+`gnubands` 조합에 대응하지만, path coordinate의 단위와 special-point label을 그대로 복사해서는 안 된다. QE의 `crystal_b`는 reciprocal lattice fractional coordinate이고, SIESTA의 `BandLinesScale` 선택에 따라 coordinate 규약이 달라질 수 있다. Structure를 primitive/conventional cell 중 어느 것으로 표준화했는지도 band path와 함께 기록해야 한다.[7,10]

## 7. Projection, LDOS와 real-space field

### (1) Atomic-orbital PDOS

PDOS는 각 Kohn–Sham state를 reference atomic orbital에 투영해 energy별 weight를 합한 것이다. QE의 `projwfc.x`는 UPF에 든 atomic wavefunction을 orthogonalize한 뒤 Löwdin population과 PDOS를 계산한다. 이는 SIESTA의 실제 numerical atomic basis orbital에 대한 projection과 정의가 완전히 같지 않으므로, 두 코드의 orbital-resolved weight가 정량적으로 같아야 한다고 기대해서는 안 된다.[5,12]

`projwfc.x`는 wavefunction이 필요하므로 보통 조밀한 uniform mesh의 `nscf` 뒤에 실행한다. `filpdos.pdos_tot`과 `filpdos.pdos_atm#N(X)_wfc#M(l)`은 energy를 첫 열로 둔 **1D table**이고, energy는 eV, DOS는 states/eV이다. 후자의 `LDOS(E)` 열은 한 atomic wavefunction channel의 magnetic component $m$에 대한 PDOS 합을 뜻한다. 공간 좌표 $\mathbf r$의 local density of states와 같은 자료가 아니다.[8,12,38,39]

같은 NSCF dataset에서 orbital PDOS를 만드는 최소 template은 다음과 같다. Total DOS와 겹쳐 비교하려면 energy grid와 broadening convention을 맞춘다. `filpdos`는 한 파일 이름이 아니라 `.pdos_tot`과 atom/projector별 파일들의 prefix이다.[12,35,38,39]

```fortran
&PROJWFC
  prefix  = 'si'
  outdir  = './tmp'
  filpdos = 'si.pdos'
  Emin    = <lower_energy_eV>
  Emax    = <upper_energy_eV>
  DeltaE  = <energy_step_eV>
  ngauss  = 0
  degauss = <broadening_Ry>
/
```

SIESTA `SystemLabel.PDOS`/`.PDOS.xml`은 SIESTA basis orbital 전체의 projection을 XML 계열 자료로 저장한다. QE 대응물은 `projwfc.x`의 atom·projector별 PDOS table과 `atomic_proj.xml`이다. SIESTA의 nonorthogonal orbital projection과 QE의 orthogonalized atomic reference projection이 다르므로, 원소·$l$ channel의 경향 비교에는 쓸 수 있어도 basis-independent observable로 취급할 수는 없다.[5,11,12]

### (2) LDOS와 ILDOS의 용어 구분

LDOS는 본래 energy와 위치에 함께 의존하는 $D(\mathbf r,E)$이다. QE와 SIESTA의 filename·column name은 이 말을 서로 다른 축으로 적분한 결과에도 사용하므로, “PLDOS”라는 한 표현으로 묶으면 자료 차원을 잃는다.[12–14]

| 목적 | QE 기능과 자료형 | SIESTA 대응 | 해석 |
| --- | --- | --- | --- |
| 원자·궤도별 PDOS | `projwfc.x`의 `pdos_atm...`, **energy 1D table** | `SystemLabel.PDOS(.xml)` | orbital/projector weight를 energy별로 합산 |
| 특정 energy의 real-space LDOS | `pp.x plot_num=3`, **1D/2D/3D spatial field** [14,40] | 직접 대응 없음 | $D(\mathbf r,E)$ 또는 energy grid별 공간장 |
| Energy-window ILDOS | `pp.x plot_num=10`, **FFT real-space grid** [14,41] | `SystemLabel.LDOS` | $\int_{E_{\min}}^{E_{\max}}D(\mathbf r,E)\,dE$ |

따라서 SIESTA의 `SystemLabel.LDOS`를 QE로 옮길 때 가장 가까운 기본 기능은 `projwfc.x`의 `LDOS(E)` 열이 아니라 `pp.x plot_num=10`이다. 위치별 map이 필요하면 orbital PDOS table이 아니라 `pp.x`의 spatial-field 경로를 사용한다. 현재 문서에서 `plot_num=3`은 energy-resolved LDOS, `plot_num=10`은 energy window에 적분한 ILDOS이며, 이 selector와 energy 범위는 설치본 문서에서 다시 확인한다.[12–14,40,41]

### (3) Charge density와 potential

`pp.x`는 두 단계로 동작한다. `&INPUTPP`가 `prefix.save`에서 물리량을 추출해 `filplot` intermediate file을 만들고, `&PLOT`이 이를 line, plane 또는 3D region으로 sampling해 외부 형식으로 쓴다. `iflag=1`은 1D line, `iflag=2`는 2D plane, `iflag=3`은 3D field이며, 3D는 XCrySDen XSF 또는 Gaussian Cube로 내보낼 수 있다. `filplot` 자체와 최종 `fileout`을 구분해야 한다.[14,15]

Valence pseudocharge density를 3D Gaussian Cube로 내보내는 독립 template은 다음과 같다. `output_format=6`의 의미와 허용 조합은 version에 민감하므로 설치본 `INPUT_PP.html`에서 다시 확인한다.[14,15]

```fortran
&INPUTPP
  prefix   = 'si'
  outdir   = './tmp'
  filplot  = 'si.rho.filplot'
  plot_num = 0
/
&PLOT
  nfile          = 1
  filepp(1)      = 'si.rho.filplot'
  weight(1)      = 1.0
  iflag          = 3
  output_format  = 6
  fileout        = 'si.rho.cube'
/
```

Local Kohn–Sham potential energy $V_{\mathrm{bare}}+V_H+V_{\mathrm{xc}}$를 3D XSF로 내보낼 때에는 `plot_num=1`을 쓴다. `output_format=5`는 현재 3D XCrySDen 형식 선택이며, 이 숫자도 설치본 문서를 기준으로 한다.[14,15,42]

```fortran
&INPUTPP
  prefix   = 'si'
  outdir   = './tmp'
  filplot  = 'si.vks.filplot'
  plot_num = 1
/
&PLOT
  nfile          = 1
  filepp(1)      = 'si.vks.filplot'
  weight(1)      = 1.0
  iflag          = 3
  output_format  = 5
  fileout        = 'si.vks.xsf'
/
```

SIESTA `.VH`에 가까운 electrostatic potential energy $V_{\mathrm{bare}}+V_H$가 필요하면 별도 run에서 `plot_num=11`을 선택한다. `plot_num=1` 결과에서 exchange–correlation (XC) 성분을 사후에 임의로 빼는 것과 같은 절차로 간주하지 않는다.[14–16,42]

```fortran
&INPUTPP
  prefix   = 'si'
  outdir   = './tmp'
  filplot  = 'si.ves.filplot'
  plot_num = 11
/
&PLOT
  nfile          = 1
  filepp(1)      = 'si.ves.filplot'
  weight(1)      = 1.0
  iflag          = 3
  output_format  = 6
  fileout        = 'si.ves.cube'
/
```

Energy-window ILDOS는 `plot_num=10`과 `emin/emax`를 사용한다. 두 energy는 eV placeholder이며, Fermi level을 0으로 옮긴 plot 범위를 그대로 복사하지 말고 saved calculation의 energy zero와 원하는 window를 확인한다.[14,41]

```fortran
&INPUTPP
  prefix   = 'si'
  outdir   = './tmp'
  filplot  = 'si.ildos.filplot'
  plot_num = 10
  emin     = <lower_energy_eV>
  emax     = <upper_energy_eV>
/
&PLOT
  nfile          = 1
  filepp(1)      = 'si.ildos.filplot'
  weight(1)      = 1.0
  iflag          = 3
  output_format  = 6
  fileout        = 'si.ildos.cube'
/
```

| 물리량 | `pp.x plot_num` | SIESTA의 가까운 출력 | 내용 |
| --- | ---: | --- | --- |
| Valence pseudocharge density | 0 | `SaveRho` → `.RHO` | 적분값이 electron 수인 density |
| Local Kohn–Sham effective potential | 1 | `SaveTotalPotential` → `.VT` | $V_{\mathrm{bare}}+V_H+V_{\mathrm{xc}}$ |
| Electrostatic potential energy | 11 | `SaveElectrostaticPotential` → `.VH` | $V_{\mathrm{bare}}+V_H$ |

여기서 QE potential output은 electron이 느끼는 energy 차원이므로 volt 단위의 scalar potential과 부호·전하 인자를 혼동하면 안 된다. SIESTA의 `.VH`와 `.VT`도 real-space mesh field이지만 native binary/Network Common Data Form (NetCDF) 또는 American Standard Code for Information Interchange (ASCII) 선택을 가지며, `g2c_ng`로 Cube에 변환할 수 있다. 두 코드의 grid를 비교할 때에는 cell, origin, grid order, spin component와 pseudo/all-electron density 여부를 먼저 맞춘다.[14–16]

### (4) 산출물의 차원·단위·형식 검산

같은 “output”이라도 scalar log, energy table, path table, FFT field와 restart payload는 서로 다른 자료이다. Plot script나 parser를 쓰기 전에 다음 네 열을 함께 검사한다.[8–10,12,14–17,28]

| 산출물 | 독립 축·자료 차원 | 대표 단위 | 저장 형식과 최소 검산 |
| --- | --- | --- | --- |
| `pw.x` total energy | configuration마다 scalar | Ry | stdout text; 마지막 값이 수렴한 step인지 확인 |
| 원자 force | 원자마다 Cartesian 3-vector | Ry/Bohr | stdout text; atom ordering과 최대 성분 확인 |
| Stress | Cartesian $3\times3$ tensor | Ry/Bohr$^3$, kbar | stdout text; pressure scalar와 tensor 부호를 구분 |
| `data-file-schema.xml` | 구조·$k$-point·전자상태 metadata | field별 schema 단위 | XML; QE version/schema와 `prefix` 확인 |
| charge/wavefunction payload | FFT 3D grid 또는 $k$별 coefficient array | internal atomic units | 구현 의존 자료; 직접 해석보다 documented reader 사용 |
| `fildos` | energy 1D table | eV, states/eV | text; energy zero, spin column, 적분 범위 확인 |
| `filband.gnu` | path coordinate 1D × band index | energy eV | text; special-point 위치와 band ordering 확인 |
| `pdos_atm...` | energy 1D × projector/spin column | eV, states/eV | text; atom·$l,m$ label과 broadening 확인 |
| `pp.x`, `iflag=1` | real-space line 1D | 선택한 field의 atomic unit | gnuplot형 table; line origin·direction·length 확인 |
| `pp.x`, `iflag=2` | real-space plane 2D | 선택한 field의 atomic unit | 2D table/XSF; plane basis와 sampling 확인 |
| `pp.x`, `iflag=3`, density/potential | real-space 3D FFT-sampled field | density 또는 potential-energy atomic unit | XSF/Cube; cell, origin, voxel order, field component 확인 |
| `pp.x plot_num=10` | energy window를 적분한 real-space 3D field | integrated-density atomic unit | XSF/Cube; `emin/emax`와 energy reference 확인 |

파일 확장자만으로 물리량을 판정하지 않는다. 예를 들어 Cube는 density와 potential을 모두 담을 수 있고, energy 1D table의 첫 열이 eV라고 해서 두 번째 열도 energy인 것은 아니다.[9,10,12,14]

## 8. 재현성과 version 경계

QE workflow의 연결 key는 `prefix`, `outdir`, pseudopotential 사본과 cell/$k$-point convention이다. `scf` 뒤의 `nscf`, `bands`, `dos.x`, `projwfc.x`, `pp.x`가 서로 다른 directory나 오래된 `prefix.save`를 읽으면 입력 text만으로는 오류를 발견하기 어렵다. 각 단계에서 upstream file hash, QE version, executable, input, stdout 종료 상태와 생성된 table/grid의 단위까지 묶어 보존해야 한다.[8,17]

Version에 민감한 세부 사항은 특히 다음과 같다.

- Online `INPUT_*.html`의 변수·default·output filename은 설치본과 다를 수 있다. 설치된 source tree의 `Doc/INPUT_*.html`과 executable이 출력한 version을 함께 확인한다.
- `prefix.save`의 restart payload 이름과 배치는 구현에 따라 달라질 수 있다. 후속 처리는 documented executable이나 XML schema를 통한다.
- Pseudopotential library의 “latest” 이름보다 dataset version과 checksum이 재현 단위이다.
- DOS/PDOS의 broadening, energy zero, spin convention과 band path는 plot에 드러나지 않을 수 있으므로 결과 표와 함께 기록한다.

SIESTA에서 옮긴 계산을 검증할 때는 한 번에 모든 설정을 바꾸지 않는다. 먼저 같은 구조, functional, electron count와 가능한 한 동등한 pseudopotential을 맞춘 뒤 각각의 basis/grid를 수렴시킨다. 그 다음 total energy의 절대값보다 energy difference, force, stress, band dispersion, integrated charge처럼 같은 정의를 가진 양을 비교한다. Plane-wave와 local-orbital basis의 차이, Pulay 성분, projection 정의의 차이를 하나의 “코드 오차”로 합치지 않는 것이 핵심이다.[3–5]

## 9. 요약

- QE는 `pw.x`가 만든 `prefix.save`를 `dos.x`, `bands.x`, `projwfc.x`, `pp.x`가 읽는 executable pipeline이다.
- `pw.x` 입력은 순서가 있는 namelist와 card로 구성하며, `ecutwfc`·`ecutrho`·$k$-mesh는 SIESTA의 atomic-orbital basis와 `MeshCutoff`에 일대일 대응하지 않는다.
- UPF는 NC·US·PAW를 담을 수 있다. Library version, checksum, functional, relativistic level, valence configuration과 수렴한 cutoff를 함께 기록한다.
- `relax`는 fixed-cell ion relaxation, `vc-relax`는 variable-cell relaxation이다. QE의 `ev.x`는 $E(V)$ fitting 도구이며 volume scan을 자동 실행하는 SIESTA-like EOS WorkChain은 기본 `pw.x` mode에 없다.
- Total DOS와 PDOS는 energy 축의 1D table이고, charge density·potential·real-space LDOS는 FFT grid field이다. `projwfc.x`의 `LDOS(E)` column과 `pp.x`의 spatial LDOS/ILDOS를 구분한다.
- 표준 출력은 사람이 검토하고, 자동 후처리는 XML/save dataset과 documented exporter를 사용한다. 단위와 installed version을 각 단계에서 다시 확인한다.

## 10. 참고문헌

1. Quantum ESPRESSO Foundation, “Documentation,” *Quantum ESPRESSO* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/documentation/).
2. P. Giannozzi et al., “QUANTUM ESPRESSO: a modular and open-source software project for quantum simulations of materials,” *Journal of Physics: Condensed Matter* **21**, 395502 (2009). [DOI](https://doi.org/10.1088/0953-8984/21/39/395502).
3. P. Giannozzi et al., “Advanced capabilities for materials modelling with Quantum ESPRESSO,” *Journal of Physics: Condensed Matter* **29**, 465901 (2017). [DOI](https://doi.org/10.1088/1361-648X/aa8f79).
4. J. M. Soler et al., “The SIESTA method for ab initio order-N materials simulation,” *Journal of Physics: Condensed Matter* **14**, 2745–2779 (2002). [DOI](https://doi.org/10.1088/0953-8984/14/11/302).
5. A. García et al., “Siesta: Recent developments and applications,” *The Journal of Chemical Physics* **152**, 204108 (2020). [DOI](https://doi.org/10.1063/5.0005077).
6. Quantum ESPRESSO Foundation, “pw.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_PW.html).
7. SIESTA Project, “SIESTA user manual: k-point sampling, band-structure analysis, and structural relaxation,” *SIESTA Documentation 5.4* (2026년 9월 확인). [공식 문서](https://docs.siesta-project.org/projects/siesta/en/5.4/reference/siesta.html).
8. Quantum ESPRESSO Foundation, “PWscf User’s Guide: Data files,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/pw_user_guide/node9.html).
9. Quantum ESPRESSO Foundation, “dos.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_DOS.html).
10. Quantum ESPRESSO Foundation, “bands.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_BANDS.html).
11. SIESTA Project, “DOS and projected DOS,” *SIESTA Documentation* (2026년 9월 확인). [공식 문서](https://docs.siesta-project.org/projects/siesta/en/stable/analysis_visualization/dos-pdos.html).
12. Quantum ESPRESSO Foundation, “projwfc.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_PROJWFC.html).
13. SIESTA Project, “Local density of states,” *SIESTA User Manual 5.4* (2026년 9월 확인). [공식 문서](https://docs.siesta-project.org/projects/siesta/en/5.4/reference/siesta.html#local-density-of-states).
14. Quantum ESPRESSO Foundation, “pp.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_PP.html).
15. C. W. Lee, “Charge density & visualization,” *Quantum ESPRESSO: Theory + Hands-On* (2026년 9월 확인). [교육 자료](https://chaewoon11.github.io/qe-tutorial/chapters/charge/).
16. SIESTA Project, “Output of charge densities and potentials on the grid,” *SIESTA User Manual 5.4* (2026년 9월 확인). [공식 문서](https://docs.siesta-project.org/projects/siesta/en/5.4/reference/siesta.html#output-of-charge-densities-and-potentials-on-the-grid).
17. PAOFLOW Developers, “PAOFLOW.inputs.read_QE_xml,” *PAOFLOW Documentation* (2026년 9월 확인). [Parser 문서](https://paoflow.org/en/latest/_modules/PAOFLOW/inputs/read_QE_xml.html).
18. P. Das, “Density of States calculation,” *Quantum Espresso Tutorial* (2026년 9월 확인). [교육 자료](https://coteo-cbpf.github.io/Quantum-Espresso-tutorial/hands-on/dos/).
19. Quantum ESPRESSO Foundation, “PW example01: total energy and band structure,” *Quantum ESPRESSO source repository* (2026년 9월 확인). [공식 예제](https://gitlab.com/QEF/q-e/-/blob/master/PW/examples/example01/README).
20. University of Illinois Urbana-Champaign, “Module 2: Quantum Espresso Walkthrough,” *MSE 404 Electronic Materials* (2026). [강의 자료](https://courses.grainger.illinois.edu/MSE404ELA/sp2026/6.DFT-walkthrough.pdf).
21. Quantum ESPRESSO Foundation, “Unified Pseudopotential Format,” *Quantum ESPRESSO Pseudopotentials* (2026년 9월 확인). [형식 명세](https://pseudopotentials.quantum-espresso.org/home/unified-pseudopotential-format).
22. Quantum ESPRESSO Foundation, “Pseudopotentials,” *Quantum ESPRESSO* (2026년 9월 확인). [공식 안내](https://www.quantum-espresso.org/pseudopotentials/).
23. G. Prandini et al., “Precision and efficiency in solid-state pseudopotential calculations,” *npj Computational Materials* **4**, 72 (2018). [DOI](https://doi.org/10.1038/s41524-018-0127-2).
24. H. J. Monkhorst and J. D. Pack, “Special points for Brillouin-zone integrations,” *Physical Review B* **13**, 5188–5192 (1976). [DOI](https://doi.org/10.1103/PhysRevB.13.5188).
25. C. W. Lee, “Brillouin-zone sampling & smearing,” *Quantum ESPRESSO: Theory + Hands-On* (2026년 9월 확인). [교육 자료](https://chaewoon11.github.io/qe-tutorial/chapters/brillouin-zone).
26. M. J. van Setten et al., “The PseudoDojo: Training and grading a 85 element optimized norm-conserving pseudopotential table,” *Computer Physics Communications* **226**, 39–54 (2018). [DOI](https://doi.org/10.1016/j.cpc.2018.01.012).
27. A. Dal Corso, “Pseudopotentials periodic table: From H to Pu,” *Computational Materials Science* **95**, 337–350 (2014). [DOI](https://doi.org/10.1016/j.commatsci.2014.07.043).
28. Quantum ESPRESSO Foundation, “PWscf reference output: total energy, forces, and stress,” *Quantum ESPRESSO source repository* (2026년 9월 확인). [공식 예제 출력](https://github.com/QEF/q-e_old/blob/master/PHonon/examples/GRID_recover_example/reference/alas.scf.out).
29. C. W. Lee, “Structural optimization,” *Quantum ESPRESSO: Theory + Hands-On* (2026년 9월 확인). [교육 자료](https://chaewoon11.github.io/qe-tutorial/chapters/relaxation).
30. Quantum ESPRESSO Foundation, “2 Compilation,” *PWscf User’s Guide* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/pw_user_guide/node6.html).
31. S. de Gironcoli, “First steps with a periodic DFT code: Quantum ESPRESSO,” SISSA tutorial (2011). [강의 자료](https://www.people.sissa.it/~degironc/2011/tutorial_surface.pdf).
32. ASE Developers, “ase.eos,” *Atomic Simulation Environment Documentation* (2026년 9월 확인). [공식 source documentation](https://docs.ase-lib.org/_modules/ase/eos.html).
33. AiiDA SIESTA Developers, “Equation Of State workflow,” *AiiDA SIESTA Plugin Documentation* (2026년 9월 확인). [공식 문서](https://docs.siesta-project.org/projects/aiida-siesta/en/latest/workflows/eos.html).
34. Quantum ESPRESSO Foundation, “`ev.x` source: E(V) data fitting,” *Quantum ESPRESSO 7.5 source repository*, tag `qe-7.5` (2026년 9월 확인). [공식 source](https://gitlab.com/QEF/q-e/-/blob/qe-7.5/PW/tools/ev.f90).
35. SCM, “Quantum ESPRESSO Properties,” *AMS 2026.1 Documentation* (2026년 9월 확인). [Interface documentation](https://www.scm.com/doc/QuantumEspresso/properties.html).
36. AiiDA Developers, “Workflows: band structure with Quantum ESPRESSO,” *AiiDA Tutorials* (2026년 9월 확인). [공식 교육 문서](https://aiida-tutorials.readthedocs.io/en/main/sections/running_processes/workflows.html).
37. P. Das, “Band structure calculation,” *Quantum Espresso Tutorial* (2026년 9월 확인). [교육 자료](https://coteo-cbpf.github.io/Quantum-Espresso-tutorial/hands-on/bands/).
38. P. Das, “Projected density of states,” *Quantum Espresso Tutorial* (2026년 9월 확인). [교육 자료](https://pranabdas.github.io/espresso/hands-on/pdos/).
39. C. W. Lee, “Density of states & PDOS,” *Quantum ESPRESSO: Theory + Hands-On* (2026년 9월 확인). [교육 자료](https://chaewoon11.github.io/qe-tutorial/chapters/dos).
40. C. Wolf, “misbehaving pp.x for plot_num 3,” *Quantum ESPRESSO users mailing list* (2020). [실행 사례](https://lists.quantum-espresso.org/pipermail/users/2020-April/044268.html).
41. G. Fratesi, “Re: question regarding ILDOS plots in PP.x,” *Quantum ESPRESSO users mailing list* (2015). [답변](https://lists.quantum-espresso.org/pipermail/users/2015-May/032171.html).
42. Computational Materials Physics, “Work function,” educational tutorial (2022). [강의 자료](https://compmatphys.org/wp-content/uploads/2022/09/work-function.pdf).
