---
description: Quantum ESPRESSO의 프로그램별 입출력, 핵심 입력 변수, 구조 최적화와 전자구조·실공간 후처리를 정리한 참조 안내
---

# Quantum ESPRESSO: Overview

Quantum ESPRESSO (QE)는 density functional theory (DFT)에 기반한 전자구조 계산 프로그램 모음이다. 이 문서는 `pw.x`의 입력·저장 자료와 분석 프로그램의 연결을 정리한다. 계산 목적별로 필요한 선행 자료, 입력 변수, 출력 파일과 단위를 찾아볼 수 있도록 구성했다.[1,2,3]

입력 문법은 QE 7.5를 기준으로 한다. Si는 문법과 파일 이름을 설명하는 예시이며, 수치 설정은 검증된 권장값이 아니다. 예제는 비자성·scalar-relativistic 계산을 가정하고 spin–orbit coupling을 포함하지 않는다. 설치와 실행 성능은 범위에 포함하지 않으며, 문서 작성 중 QE 계산을 실행하지 않았다.

## 1. 프로그램 구성

### (1) 전자구조 계산

`pw.x`는 Kohn–Sham 파동함수를 plane wave basis로 전개하고 pseudopotential로 원자핵과 내부 전자의 효과를 다룬다. Self-consistent field (SCF)는 전하 밀도를 수렴시키며, non-self-consistent field (NSCF)는 수렴 밀도를 고정한 상태에서 지정한 $k$점의 전자상태를 구한다. `relax`와 `vc-relax`는 전자 계산에 구조 최적화를 결합한다.[2,4,5,3,6]

Pseudopotential 파일에는 Unified Pseudopotential Format (UPF)을 사용한다.[7,8] 다음 파일명은 본문의 예시 명명법이다. `.in`은 직접 작성하는 입력이며 `.out`은 표준 출력을 저장한 이름이다. `prefix='si'`, `outdir='./tmp'`이면 후속 계산은 `tmp/si.save/` 등을 통해 자료를 읽는다.[5,9,3]

| 계산 단계 | 코드 | 입력값(파일) | 결과(파일) |
| --- | --- | --- | --- |
| 고정 구조 SCF | `pw.x` | `si.scf.in`, `pseudo/Si.UPF` | `si.scf.out`: 에너지·힘·응력; `tmp/si.save/`: 수렴 밀도·전자상태 |
| 고정 셀 원자 최적화 | `pw.x` | `si.relax.in`, UPF | `si.relax.out`: 최종 원자 좌표; `tmp/si_relax.save/` |
| 셀·원자 최적화 | `pw.x` | `si.vc-relax.in`, UPF | `si.vc-relax.out`: 최종 셀·좌표; `tmp/si_vc.save/` |
| 균일 $k$점의 NSCF | `pw.x` | `si.nscf.in`, SCF 저장 자료, UPF | `si.nscf.out`, `tmp/si.save/`: 지정 격자의 고유값·파동함수 |
| 경로상의 밴드 계산 | `pw.x` | `si.bands.in`, SCF 저장 자료, UPF | `si.bands.out`, `tmp/si.save/`: 경로상의 고유값·파동함수 |

SCF에서 NSCF로 가는 분기와 SCF에서 밴드 경로로 가는 분기는 독립적이다. 균일 격자는 상태 합산·적분에, 밴드 경로는 선택한 역공간 선상의 분산에 사용한다.[5,10,11]

### (2) 후처리

Density of states (DOS)는 에너지별 상태 수이며, projected density of states (PDOS)는 원자 궤도 성분으로 투영한 상태 밀도이다. 실공간 local density of states (LDOS)는 위치와 에너지를 함께 갖는다. Equation of state (EOS) 분석은 부피별 에너지 자료에서 평형 부피와 체적 탄성률을 추정한다.[12,13,14,15,16,17]

| 계산 단계 | 코드 | 입력값(파일) | 결과(파일) |
| --- | --- | --- | --- |
| 전체 DOS | `dos.x` | `si.dos.in`, 균일 NSCF의 `tmp/si.save/` | `si.dos.dat`: 에너지·DOS·적분 DOS; `si.dos.out` |
| 밴드 정리 | `bands.x` | `si.bands-post.in`, 경로 계산의 `tmp/si.save/` | `si.bands.dat`, `si.bands.dat.gnu`; `si.bands-post.out` |
| 원자·궤도 PDOS | `projwfc.x` | `si.pdos.in`, 균일 NSCF의 고유값·파동함수 | `si.pdos.pdos_tot`, `si.pdos.pdos_atm#N(Si)_wfc#M(l)`; `si.pdos.out` |
| 전하 밀도·퍼텐셜 | `pp.x` | `si.rho.in` 등, SCF 저장 자료 | `si.rho.filplot`: 추출 자료; `si.rho.cube`: 공간 격자; `si.rho.out` |
| 공간 LDOS·에너지 구간 적분 | `pp.x` | `si.ldos.in` 또는 `si.ildos.in`, 균일 NSCF 자료 | 에너지별 중간 파일 또는 `si.ildos.filplot`; 변환 후 `.cube` |
| EOS 함수 맞춤 | `ev.x` | `si.ev.in`: 대화 응답; `si.eos.dat`: 부피·에너지 | `si.eos.fit`: 맞춤 결과; `si.ev.out` |

후처리 프로그램은 `.out`의 문장을 입력으로 읽는 것이 아니라 저장된 전자상태나 지정한 자료 파일을 읽는다. `dos.x`는 파동함수 자체를 요구하지 않지만, `projwfc.x`와 공간 상태 분석에는 파동함수가 필요하다.[9,12,13,14,10,15]

## 2. 입출력 파일

### (1) 입력 문법

Namelist의 `!` 뒤는 주석이며, card 설명은 별도 주석 행에 둔다. `1.0d-10`의 `d`는 Fortran 배정밀도 지수 표기이다. 입력은 `&CONTROL`, `&SYSTEM`, `&ELECTRONS` 순서의 namelist와 구조·원자종·$k$점 card로 구성한다. 구조 최적화에서는 card 앞에 `&IONS`, 필요하면 `&CELL`을 추가한다. Namelist는 `/`로 닫고 문자열은 따옴표로 감싼다.[5,3]

### (2) SCF 입력

아래 `si.scf.in`은 두 원자 diamond Si primitive cell의 입력 구성을 보여 준다. 셀은 Å, 원자 위치는 분율 좌표이다. Conventional cubic lattice parameter를 5.431 Å로 놓았으며, 이 값이나 cutoff `50/400 Ry`, $8\times8\times8$ 격자를 평형값·수렴값으로 전제하지 않는다. `Si.UPF`는 선택한 파일의 로컬 이름이며 [3절](#3-pseudopotential)의 선택 조건을 만족하는 실제 파일로 준비한다. 입력 행의 규약과 전자 수렴·혼합의 의미는 다음 주석과 같다.[5,3,18,19]

```fortran
&CONTROL  ! 계산 종류·입출력 제어
  calculation = 'scf'  ! 고정 구조에서 밀도를 자기일관되게 수렴
  prefix      = 'si'  ! 읽고 쓸 저장 자료의 식별자; 후속 계산과 일치
  pseudo_dir  = './pseudo'  ! ATOMIC_SPECIES의 UPF 파일을 찾을 디렉터리
  outdir      = './tmp'  ! 전자상태 저장 디렉터리; 후처리도 같은 경로 사용
  tprnfor     = .true.  ! 각 원자의 힘을 계산·출력 (Ry/Bohr)
  tstress     = .true.  ! 응력 텐서와 압력을 계산·출력
  disk_io     = 'low'  ! 계산 종료 시 후처리용 파동함수를 디스크에 저장
/  ! &CONTROL 끝
&SYSTEM  ! 셀·원자 수·전자계의 표현
  ibrav       = 0  ! Bravais 유형 대신 CELL_PARAMETERS의 세 벡터로 셀 지정
  nat         = 2  ! ATOMIC_POSITIONS에 적을 원자 행 2개
  ntyp        = 1  ! ATOMIC_SPECIES에 정의할 원자종 행 1개
  ecutwfc     = 50.0  ! 파동함수 plane wave의 운동에너지 상한 50 Ry
  ecutrho     = 400.0  ! 밀도·퍼텐셜 표현의 운동에너지 상한 400 Ry
  occupations = 'fixed'  ! 밴드갭을 가진 비자성 절연체의 고정 점유
/  ! &SYSTEM 끝
&ELECTRONS  ! 전자 반복과 밀도 혼합
  conv_thr    = 1.0d-10  ! 셀 전체의 추정 SCF 에너지 오차가 1e-10 Ry 미만이면 수렴
  mixing_beta = 0.7  ! 새 밀도의 반영 강도 0.7; 낮추면 밀도 갱신을 완화
/  ! &ELECTRONS 끝
! 원자종 card: 이름, 질량(원자 질량 단위), pseudo_dir 안의 UPF 파일
ATOMIC_SPECIES
! 유일한 원자종 Si; 질량 28.085; 사용자가 선택한 UPF의 로컬 이름
Si  28.085  Si.UPF

! 위치 card: 세 셀 벡터를 기준으로 한 무차원 분율 좌표
ATOMIC_POSITIONS (crystal)
! 원자 1: 원점
Si  0.00  0.00  0.00
! 원자 2: (a1 + a2 + a3)/4
Si  0.25  0.25  0.25

! 균일 k점 격자 자동 생성
K_POINTS (automatic)
! b1,b2,b3 방향 각각 8분할; 뒤 세 0은 각 방향 이동 없음
8 8 8  0 0 0

! 셀 card: 각 행은 하나의 셀 벡터의 Cartesian 성분 (Å)
CELL_PARAMETERS (angstrom)
! a1 = (0, a/2, a/2), a = 5.431 Å
0.0000  2.7155  2.7155
! a2 = (a/2, 0, a/2)
2.7155  0.0000  2.7155
! a3 = (a/2, a/2, 0)
2.7155  2.7155  0.0000
```

Card의 원자종 이름 `Si`는 `ATOMIC_SPECIES`와 `ATOMIC_POSITIONS`에서 일치해야 한다. 분율 좌표 $(u,v,w)$는 $\mathbf r=u\mathbf a_1+v\mathbf a_2+w\mathbf a_3$를 뜻한다. `K_POINTS`의 뒤 세 이동 표식은 `0`이면 이동 없음, `1`이면 해당 격자 간격의 절반만큼 이동이다.[5,3]

예제의 `pseudo_dir='./pseudo'`, `outdir='./tmp'`는 실행 작업 폴더를 기준으로 한다. 같은 자료를 읽는 `pw.x`와 후처리 입력에는 일치하는 `prefix/outdir`를 지정한다.[5,9,3]

```text
qe-work/
├── pseudo/Si.UPF
├── si.scf.in
├── si.scf.out
└── tmp/si.save/
```

**같은 `prefix/outdir`를 쓰는 NSCF와 밴드 계산은 저장 전자상태를 갱신한다.** DOS 분기와 밴드 분기를 함께 보존하려면 각 분기에서 별도의 `outdir`로 SCF부터 수행하고, 그 경로를 해당 분기의 모든 입력에 일관되게 사용한다. 아래 예제는 각 분기를 독립적으로 읽을 수 있도록 모두 `si`와 `./tmp`라는 이름을 사용한다. 여러 예제를 이어 실행할 때는 필요한 선행 자료가 현재 저장되어 있는지 확인한다.[9,20,10,11]

### (3) 표준 출력

표준 출력은 입력 해석, 반복 수렴, 계산 물리량을 확인하는 기록이다. 에너지 줄이 존재한다는 사실만으로 계산의 수렴을 판정하지 않는다. 구조 최적화에서는 전자 수렴과 구조 최적화 종료를 각각 확인한다.[3,5,21,6]

| 물리량·상태 | `si.scf.out` 등의 검색 표식 | 형태·단위 |
| --- | --- | --- |
| 전체 에너지 | `!`와 `total energy` | 계산 셀 전체의 에너지, Ry |
| 원자 힘 | `Forces acting on atoms`, `force =` | 원자마다 3성분, Ry/Bohr |
| 응력·압력 | `total stress`, `P=` | $3\times3$ 응력: Ry/Bohr$^3$와 kbar; 압력: kbar |
| 셀 부피 | `unit-cell volume` | Bohr$^3$, 출력 표기는 `(a.u.)^3` |
| 밴드 고유값 | `bands (ev)` 등 해당 머리글 | $k$점별 에너지, eV |
| 수렴·종료 | `convergence`, `JOB DONE` | 수렴 메시지와 정상 종료를 별도 확인 |

힘과 응력은 `tprnfor`, `tstress` 설정에 연결된다. `! total energy`는 셀 에너지이며 DOS 표의 에너지 축과 물리적 의미도 단위도 다르다.[5,3,21]

### (4) 저장 자료

`tmp/si.save/data-file-schema.xml`은 구조와 전자상태 정보를 담는 Extensible Markup Language (XML) 메타데이터이다. 전하 밀도·파동함수 등에는 별도의 저장 자료가 필요하며 바이너리 파일의 배치·형식은 구현에 의존할 수 있다. 저장 디렉터리의 일부 파일만 임의로 옮기기보다 사용한 `outdir`의 필요한 자료를 함께 보존하고 QE의 후속 프로그램으로 읽는다.[9,20]

| 산출물 | 형식·독립 변수 | 사용 목적 |
| --- | --- | --- |
| `si.scf.out` | 사람이 읽는 텍스트 | 구조·수렴·물리량 확인 |
| `tmp/si.save/data-file-schema.xml` | XML 구조화 자료 | 구조·계산 및 전자상태 메타데이터 |
| `outdir`의 밀도·파동함수 자료 | QE 저장 자료 | NSCF·밴드·투영·공간 후처리 |
| `si.dos.dat`, `si.pdos.pdos_*` | 에너지별 텍스트 열 | 에너지 축의 상태 수 |
| `si.bands.dat.gnu` | 경로 좌표와 에너지 | 밴드 분산 |
| `si.rho.filplot` | `pp.x` 중간 자료 | 추출한 물리량의 형식 변환 |
| `si.rho.cube` 또는 `.xsf` | 셀·원자·공간 격자 | 실공간 값의 시각화·분석 |

`.out`만으로 파동함수 투영을 재개할 수 없고, `.cube`만으로 어떤 cutoff·UPF로 계산했는지 복원할 수도 없다. 따라서 입력·UPF 식별 정보·프로그램 버전·표준 출력과 후처리용 저장 자료를 함께 관리한다.[9,20,15,22]

## 3. Pseudopotential

### (1) UPF의 내용과 종류

UPF는 파일 형식이다. Norm-conserving (NC), ultrasoft (US), projector augmented-wave (PAW) 자료를 담을 수 있으므로 확장자만으로 종류를 판단하지 않는다. 파일에는 원소·valence 구성·교환상관 정보와 방사형 격자, 퍼텐셜, 투영자, 원자 파동함수 등의 자료가 들어 있다.[2,7,23,8]

| 확인 항목 | 계산에 연결되는 의미 |
| --- | --- |
| 원소와 valence 구성 | 명시적으로 계산하는 전자의 범위 |
| 교환·상관 함수 | 함께 사용할 계산 모형의 일관성 |
| 상대론 처리 | Scalar-relativistic 또는 fully relativistic 자료의 선택 |
| NC·US·PAW 구분 | 필요한 표현과 권장 cutoff |
| 원자 파동함수 | `projwfc.x`가 사용하는 투영 함수 |
| 배포 버전·원본 파일명 | 자료 식별과 재현성 |

US·PAW의 보강 성분까지 표현하려면 밀도 cutoff도 확인해야 한다. `ecutrho`를 `ecutwfc`의 고정 배수로만 정하지 말고 배포처 권고와 목표 물성의 수렴 시험을 함께 사용한다.[4,5,7,8]

### (2) 배포처와 선택

[QE pseudopotential 안내](https://www.quantum-espresso.org/pseudopotentials/)는 배포처의 출발점이다. Standard Solid-State Pseudopotentials (SSSP)는 여러 자료의 정확도·효율을 검증하여 원소별 파일과 권장 cutoff를 제공한다. PseudoDojo는 NC 자료를, PSlibrary는 US·PAW 자료를 제공한다.[23,8,24,25]

Si 입력 예제에서는 Perdew–Burke–Ernzerhof (PBE) 교환·상관 함수와 scalar-relativistic 조건에 맞는 UPF를 선택한다. 다원소계에서도 의도한 교환상관 모형과 상대론 조건을 점검한다. UPF를 바꾸면 valence 구성과 기준 에너지가 달라질 수 있으므로 이전 에너지 비교와 수렴 시험을 그대로 이어 쓰지 않는다.[7,23,8,24,25]

`ATOMIC_SPECIES`의 `Si.UPF`는 실제 파일명으로 바꾸거나, 선택한 원본을 그 로컬 이름으로 복사해 사용한다. 원본 이름·배포 버전과 `sha256sum pseudo/Si.UPF`의 식별값을 기록하면 이름이 같은 서로 다른 자료를 구분할 수 있다. 이 기록은 파일 관리 규칙이며 QE 입력 문법이 아니다.

## 4. 계산 설정

### (1) Cutoff와 SCF

`ecutwfc`는 파동함수 기저를, `ecutrho`는 전하 밀도·퍼텐셜 표현을 제한한다. `conv_thr`는 연속 SCF 총에너지의 단순 차이가 아니라 추정 에너지 오차의 기준이며 셀 전체에 적용한다. `mixing_beta`는 기존 밀도를 새 결과로 갱신하는 강도이다. 값을 낮추면 새 결과의 반영이 줄어 진동하는 SCF의 안정화에 도움이 될 수 있다. 실제 Broyden 혼합은 이전 반복의 이력도 사용하므로 `0.7`을 매 반복의 단순한 70:30 산술 평균식으로 해석하지 않는다.[5,18,19,26]

`conv_thr`를 만족하는 것은 그 기저와 $k$점에서 전자 반복이 수렴했다는 뜻이다. 기저와 적분 격자의 오차는 별도의 수렴 시험으로 평가한다.[4,5,3,8]

| 시험 | 고정할 조건 | 변경할 조건 | 비교할 결과 |
| --- | --- | --- | --- |
| 파동함수 기저 | 구조·UPF·$k$점, 충분한 밀도 cutoff | `ecutwfc` | 에너지 차이·힘·응력 |
| 전하 밀도 표현 | 구조·UPF·$k$점·`ecutwfc` | `ecutrho` | 힘·응력과 에너지 |
| Brillouin zone 적분 | 구조·UPF·수렴 cutoff | $k$점 분할 수 | 에너지·압력·목표 전자구조량 |

배포처 권장값에서 시작해 값을 높이되, 두 cutoff를 함께 올린 시험 뒤에는 `ecutrho`의 영향도 분리한다. 비교 파일은 `si.cut60.in/out`, `si.k10.in/out`처럼 식별하고 서로 다른 `prefix`로 결과를 보존할 수 있다. 목표가 평형 부피라면 에너지뿐 아니라 압력 안정성도 필요하다.[3,5,8]

원자당 변화량을 비교할 때, 동일한 $N$원자 셀에서 시험 에너지 $E_i$와 가장 정밀한 기준 에너지 $E_{\mathrm{ref}}$로 다음을 정의한다.

$$
\Delta e_i=\frac{E_i-E_{\mathrm{ref}}}{N}.
$$

이는 수치 설정에 따른 셀 에너지 차이를 원자 수로 나눈 값이며 응집 에너지의 정의가 아니다. 모든 비교에서 구조·UPF·교환상관 모형을 유지한다.[3,8]

### (2) $k$점

`K_POINTS (automatic)`의 분할 수와 이동 표식은 함께 기록한다. 셀 표현을 바꾸면 같은 분할 수가 같은 역공간 간격을 뜻하지 않는다. 밴드 경로의 `crystal_b` 표본은 균일 적분 격자를 대신하지 않는다.[5,27,18]

### (3) 점유수

`occupations='fixed'`는 예제의 절연체 점유 설정이다. 금속의 부분 점유에는 `occupations='smearing'`과 방식·폭을 지정하며, $k$점과 폭의 영향을 함께 검사한다. SCF의 점유 폭과 후처리 DOS의 곡선 폭은 별개의 설정이다.[5,18,12,10]

| 용도 | 설정 위치 | 핵심 선택 |
| --- | --- | --- |
| 고정 점유 | `pw.x &SYSTEM` | `occupations='fixed'` |
| Smearing 점유 | `pw.x &SYSTEM` | `occupations='smearing'`, `smearing`, `degauss`(Ry) |
| Gaussian DOS | `dos.x &DOS` | `ngauss=0`, `degauss`(Ry), `DeltaE`(eV) |
| Tetrahedron DOS | 균일 격자의 `pw.x`와 후처리 | `occupations='tetrahedra'`; 후처리의 `degauss` 생략 |

Tetrahedron과 Gaussian 입력을 임의로 혼합하지 않는다. 아래 분석 예제는 `fixed` 점유의 NSCF와 명시적 Gaussian 후처리를 사용한다. 출력 에너지 간격만 줄여서는 부족한 $k$점 표본이나 비점유 밴드를 보완할 수 없다.[12,13,10]

## 5. 구조 최적화

### (1) `relax`와 `vc-relax`

`relax`는 셀을 고정하고 원자 위치를 최적화한다. `vc-relax`는 허용한 셀 자유도도 변화시킨다. 입력은 [2절](#2)의 구조·UPF·수렴 설정을 바탕으로 만들며, 선행 SCF 파일이 필수인 후처리와 달리 자체 전자 계산을 수행한다.[5,6,3]

`etot_conv_thr`는 연속 구조 단계의 셀 전체 에너지 차이에 적용하고 `forc_conv_thr`는 원자별 힘 성분에 적용한다. 두 조건을 함께 만족해야 원자 최적화가 끝난다. 이는 각 구조에서 전자 밀도를 수렴시키는 `conv_thr`와 별개의 기준이다.[5,28]

`si.relax.in`의 `&CONTROL`에서 바꿀 값은 다음과 같다. 구조·UPF·cutoff와 전자 수렴 설정은 유지한다.[5,6,28]

| 변수 | 입력값 | 의미·단위 |
| --- | --- | --- |
| `calculation` | `'relax'` | 고정 셀에서 원자 위치 최적화 |
| `prefix` | `'si_relax'` | SCF 예제와 구분할 저장 자료 식별자 |
| `etot_conv_thr` | `1.0d-5` | 연속 구조 단계의 에너지 차이 허용치, Ry |
| `forc_conv_thr` | `1.0d-4` | 모든 원자 힘 성분의 절댓값 허용치, Ry/Bohr |

`&ELECTRONS` 다음에는 아래 `&IONS`를 추가한다. `bfgs`는 Broyden–Fletcher–Goldfarb–Shanno (BFGS) 최적화이다.[5,6]

```fortran
&IONS  ! 원자 최적화 설정
  ion_dynamics = 'bfgs'  ! BFGS로 원자 위치를 갱신
/  ! &IONS 끝
```

`si.vc-relax.in`에서는 `calculation='vc-relax'`, `prefix='si_vc'`를 사용하고 `&IONS` 다음에 아래를 추가한다. `all`은 셀 변형을 허용하는 벌크 예시이며, 일부 길이를 고정해야 하는 계의 설정으로 간주하지 않는다.[5,6]

```fortran
&CELL  ! 셀 최적화 설정
  cell_dynamics  = 'bfgs'  ! BFGS로 셀 벡터를 갱신; vc-relax에서 사용
  press          = 0.0  ! 목표 외부 압력 0 kbar
  press_conv_thr = 0.5  ! 목표 압력에 대한 수렴 허용치 0.5 kbar
  cell_dofree    = 'all'  ! 셀의 길이·각도를 모두 최적화 대상으로 허용
/  ! &CELL 끝
```

결과는 각각의 `.out`에서 최종 좌표와 힘, 셀을 바꾼 경우 셀·응력까지 확인한다. 최종 셀과 좌표를 단위 머리글과 함께 새 `si.scf.in`에 반영하고 고정 구조 SCF를 수행하면 후속 분석의 공통 자료를 만들 수 있다. 셀이 바뀌면 같은 cutoff에서도 기저가 달라지므로 최종 구조의 에너지·힘·응력을 다시 확인한다.[5,6,10]

### (2) EOS

EOS에는 서로 다른 부피의 수렴 에너지 표가 필요하다. `ev.x`는 그 표를 함수에 맞추는 도구이며 `pw.x`의 부피별 계산을 대신 실행하지 않는다. 목표 압력의 구조 하나를 찾는 `vc-relax`와 구분한다.[29,16,17,30]

기준 셀의 세 벡터에 같은 배율 $s$를 곱하고 분율 좌표를 유지하면 부피는 $V=s^3V_{\mathrm{ref}}$이다. 각 부피에서 `si.eos-s098.in`, `si.eos-s100.in` 같은 별도 입력·`prefix`를 사용하고 UPF·cutoff·점유 방식과 $k$점 조건을 일관되게 유지한다. 내부 좌표 완화가 필요하면 각 고정 부피에서 `relax`를 사용한다. 영압 `vc-relax`는 의도한 부피 표본을 유지하지 않는다.[5,6,16]

`si.eos.dat`는 **머리글 없이 첫 열에 셀 부피(Bohr$^3$), 둘째 열에 같은 셀의 전체 에너지(Ry)**를 적은 파일이다. 각 `pw.x` 출력의 `unit-cell volume`과 수렴한 `! total energy`를 짝지으며, 원자당 에너지와 셀 부피를 섞지 않는다. 예상 최소점 양쪽을 포함한 여러 부피를 사용한다.[30,6,16]

QE 7.5의 대화 응답을 다음 `si.ev.in`에 저장하면 지정 파일로 입출력을 연결할 수 있다. 선택은 `au` 단위, 직접 부피 입력인 `noncubic`, `birch1`에 해당하는 `1`, 자료 파일, 결과 파일 순서이다.[30,6]

| 응답 행 | 입력값 | 해석 |
| --- | --- | --- |
| 1 | `au` | 부피 입력 단위 Bohr$^3$; 에너지는 Ry |
| 2 | `noncubic` | 첫 열을 셀 부피로 읽음 |
| 3 | `1` | `birch1` EOS 함수 선택 |
| 4 | `si.eos.dat` | 부피·전체 에너지의 두 열 자료 파일 |
| 5 | `si.eos.fit` | 맞춤 결과를 기록할 파일 |

`noncubic`은 여기서 첫 열을 부피로 해석하는 입력 방식이다. Si의 결정 대칭을 바꾸는 선언이 아니다. `fcc`를 선택하면 첫 열을 격자 상수로 읽으므로 위 부피 파일에 적용하면 안 된다. `si.eos.fit`의 머리글에서 평형 부피·체적 탄성률과 단위를 확인하고 계산 에너지와 맞춘 에너지의 차이를 검사한다.[30,6]

영압 평형 부피 $V_0$에서 셀 에너지 $E(V)$의 곡률과 체적 탄성률 $B_0$의 관계는 다음과 같다.

$$
B_0=V_0\left.\frac{\partial^2E}{\partial V^2}\right|_{V_0}.
$$

에너지·부피 단위는 일관되게 사용한다. 실제 맞춤은 유한한 표본과 선택한 EOS 함수에 의존하므로 최소점의 포함 여부, 잔차와 부피 범위 의존성을 확인한다. 얕은 에너지 곡선에서는 작은 수치 오차도 곡률에 영향을 준다.[16,17]

## 6. 전자구조

### (1) DOS

필요한 선행 자료는 관심 구조의 SCF 밀도와 **균일 격자의 NSCF 고유값**이다. DOS에는 SCF 에너지보다 조밀한 $k$점 표본이 필요할 수 있다. `si.nscf.in`은 [2절](#2)의 구조·UPF·cutoff·`prefix/outdir`를 유지하고 아래 두 값을 바꾼 입력이다.[5,12,10]

| 위치·변수 | 입력값 | 의미 |
| --- | --- | --- |
| `&CONTROL calculation` | `'nscf'` | 저장된 SCF 밀도를 고정하고 새 $k$점의 상태 계산 |
| `&SYSTEM nbnd` | `12` | 각 $k$점에서 12개 밴드 계산; 관심 비점유 에너지까지 덮는지 확인할 예시값 |

`K_POINTS`는 DOS 적분용 격자로 교체한다.[5,10]

```fortran
! DOS 적분용 균일 격자; SCF 입력의 K_POINTS를 대체
K_POINTS (automatic)
! 세 역격자 방향 각각 12분할; 뒤 세 0은 이동 없음
12 12 12  0 0 0
```

`si.dos.in`은 다음과 같다. NSCF의 `occupations='fixed'`를 유지하면서 DOS 표현에는 별도로 Gaussian 폭을 지정한 예이다.[12,10]

```fortran
&DOS  ! 전체 DOS 후처리 설정
  prefix  = 'si'  ! 선행 pw.x 계산의 저장 자료 식별자
  outdir  = './tmp'  ! 선행 pw.x 저장 자료를 읽을 경로
  fildos  = 'si.dos.dat'  ! 에너지·전체 DOS·적분 DOS를 기록할 파일
  ngauss  = 0  ! 각 고유값을 단순 Gaussian으로 넓혀 DOS를 구성
  degauss = 0.01  ! Gaussian 폭 0.01 Ry; 출력 에너지 간격과 별개
  DeltaE  = 0.02  ! 출력 에너지 축의 간격 0.02 eV
/  ! &DOS 끝
```

`degauss`는 Ry, `DeltaE`는 eV이다. 출력 구간을 지정하려면 `Emin`, `Emax`를 eV로 추가한다. 비자성 `si.dos.dat`는 에너지(eV), DOS(states/eV), 적분 DOS의 열을 제공하며 실제 머리글을 함께 읽는다. 스핀 계산은 열 구성이 달라진다.[12,31]

DOS 원자료의 에너지와 Fermi 에너지 등을 영점으로 옮긴 그림 축은 구분한다.[12,11] 그림 축을 $E_{\mathrm{plot}}=E-E_{\mathrm{zero}}$로 정의했다면 역변환은 $E=E_{\mathrm{plot}}+E_{\mathrm{zero}}$이다. 같은 계산의 LDOS 입력 구간을 그림에서 고를 때 이 역변환으로 원자료 값을 복원한다. 이는 좌표 정의에서 따르는 관계이며, 그림에서 이동한 에너지를 입력에 그대로 쓰는 규칙이 아니다.

### (2) 밴드

필요한 선행 자료는 관심 구조의 SCF 밀도이다. DOS용 NSCF를 먼저 수행할 필요는 없다. `si.bands.in`은 [2절](#2)의 구조·UPF·cutoff·`prefix/outdir`를 유지하고 다음 값을 바꾼 입력이다.[5,32,11,33]

| 위치·변수 | 입력값 | 의미 |
| --- | --- | --- |
| `&CONTROL calculation` | `'bands'` | 저장된 SCF 밀도에서 경로상의 고유값 계산 |
| `&SYSTEM nbnd` | `12` | 경로의 각 $k$점에서 12개 밴드 계산; 표시할 에너지 범위에 맞춰 선택 |

`K_POINTS`에는 균일 격자 대신 경로를 지정한다.[5,11]

```fortran
! 밴드 경로 card: 역격자 벡터에 대한 무차원 좌표
K_POINTS (crystal_b)
! 경로 끝점은 두 개
2
! 시작점 Γ; 다음 끝점까지 40개의 경로 표본을 생성
0.0 0.0 0.0  40
! 끝점 0.5*b1 + 0.5*b3; 마지막 정수는 마지막 점에서 사용하지 않음
0.5 0.0 0.5   1
```

위 경로는 입력 원리를 설명하는 한 구간이며 표준 고대칭 경로 전체가 아니다. 첫 정수는 끝점 수이다. 마지막 열은 다음 끝점까지의 표본 수이며 마지막 끝점에서는 사용하지 않는다. 좌표는 사용한 셀의 역격자 벡터에 대한 계수이다. 다른 셀 표현의 경로를 가져오면 좌표 변환이 필요하다.[5,11]

`bands.x`는 경로의 고유값을 새로 구하지 않고 `pw.x` 결과를 정리한다. 다음 `si.bands-post.in`을 사용한다.[32,11]

```fortran
&BANDS  ! 밴드 정리 설정
  prefix  = 'si'  ! 선행 pw.x 계산의 저장 자료 식별자
  outdir  = './tmp'  ! 선행 pw.x 저장 자료를 읽을 경로
  filband = 'si.bands.dat'  ! 정리된 밴드 자료명; .gnu 파일도 이 이름에서 파생
/  ! &BANDS 끝
```

`si.bands.dat.gnu`의 두 열은 경로 좌표와 밴드 에너지(eV)이며, 밴드별 곡선을 그리는 자료이다. 첫 축은 DOS의 에너지 축과 다르다. 끝점 위치·밴드 수를 확인하고 DOS와 비교할 때 같은 에너지 이동을 적용한다. 한 경로만으로 전체 Brillouin zone의 극값을 모두 찾았다고 해석하지 않는다.[32,11,33]

### (3) PDOS

필요한 선행 자료는 관심 구조의 SCF와 균일 NSCF의 **고유값·파동함수**이다. DOS 절과 같은 NSCF 설정을 사용할 수 있으며 `dos.x` 실행 결과 자체는 필요하지 않다. `projwfc.x`는 UPF의 원자 파동함수에 투영하므로, PDOS는 선택한 투영 함수에 따른 분석이다.[13,15,10]

다음 `si.pdos.in`은 [DOS 입력](#1-dos)과 같은 폭·간격을 사용한다. `disk_io='low'`로 보존한 파동함수와 동일한 `prefix/outdir`를 읽는다.[5,9,13,15]

```fortran
&PROJWFC  ! 원자 궤도 투영 설정
  prefix  = 'si'  ! 선행 pw.x 계산의 저장 자료 식별자
  outdir  = './tmp'  ! 선행 pw.x 저장 자료를 읽을 경로
  filpdos = 'si.pdos'  ! 원자·궤도별 PDOS 출력 파일명의 공통 앞부분
  ngauss  = 0  ! 각 고유값을 단순 Gaussian으로 넓혀 DOS를 구성
  degauss = 0.01  ! Gaussian 폭 0.01 Ry; 출력 에너지 간격과 별개
  DeltaE  = 0.02  ! 출력 에너지 축의 간격 0.02 eV
/  ! &PROJWFC 끝
```

`filpdos`는 파일명의 앞부분이다. `si.pdos.pdos_tot`과 `si.pdos.pdos_atm#N(Si)_wfc#M(l)`이 생성되며, $N$은 원자 번호, $M$은 원자 파동함수 번호, $l$ 표식은 s·p 등의 채널이다. 실제 궤도·파일 수는 UPF에 따라 확인한다. 비자성 원자별 파일의 열은 다음과 같다.[13,15]

```text
E(eV)  LDOS(E)  PDOS_1(E) ... PDOS_(2l+1)(E)
```

여기서 `LDOS(E)`는 해당 원자 파동함수의 자기양자수 성분들을 합한 열이다. 위치 좌표가 있는 실공간 LDOS가 아니며 DOS 열의 단위는 states/eV이다. 전체 DOS와 비교할 때 에너지 기준·폭을 맞추되, 원자 투영 함수가 모든 상태를 완전히 표현한다고 전제하지 않는다.[13,15,10]

## 7. 실공간 물리량

### (1) 전하 밀도와 퍼텐셜

`pp.x`의 `&INPUTPP`는 물리량을 추출하고 `&PLOT`은 외부 형식으로 변환한다. `filplot`은 중간 파일, `fileout`은 최종 파일이다. 전하 밀도·퍼텐셜에는 수렴 SCF 자료를 사용하고, 에너지별 상태 분석에는 해당 범위를 덮는 균일 NSCF 고유값·파동함수를 준비한다.[14,22,15,34]

| 물리량 | `plot_num` | 값의 의미·단위 | 예시 출력 |
| --- | ---: | --- | --- |
| 전하 밀도 | 0 | Pseudo 전자 수 밀도, Bohr$^{-3}$ | `si.rho.cube` |
| 국소 유효 퍼텐셜 | 1 | $V_{\mathrm{bare}}+V_H+V_{\mathrm{xc}}$, Ry | `si.vks.cube` |
| 정전기 퍼텐셜 에너지 | 11 | $V_{\mathrm{bare}}+V_H$, Ry | `si.ves.cube` |
| 공간 LDOS | 3 | 위치·에너지별 상태 밀도; 출력 정규화 확인 | 에너지별 중간 파일 → `si.ldos.cube` |
| Integrated local density of states (ILDOS) | 10 | 에너지 구간을 합친 공간 분포 | `si.ildos.cube` |

$V_{\mathrm{bare}}$는 국소 이온 퍼텐셜, $V_H$는 Hartree 항, $V_{\mathrm{xc}}$는 교환·상관 항이다. 이들은 전자가 느끼는 에너지이며 volt 단위 전위로 곧바로 읽지 않는다. `plot_num=1`은 비국소 연산자 자체를 스칼라장으로 내보내는 선택이 아니다. `plot_num=0`도 핵 근처의 all-electron 밀도를 뜻하지 않는다.[5,14,7,22,35]

다음 `si.rho.in`은 수렴 SCF 저장 자료의 전하 밀도를 3차원 Gaussian Cube로 쓴다. 두 namelist의 `filplot`과 `filepp(1)`은 같은 중간 파일을 지정한다.[14,22,36]

```fortran
&INPUTPP  ! 저장 전자상태에서 물리량 추출
  prefix   = 'si'  ! 선행 pw.x 계산의 저장 자료 식별자
  outdir   = './tmp'  ! 선행 pw.x 저장 자료를 읽을 경로
  filplot  = 'si.rho.filplot'  ! 추출한 물리량을 보존할 중간 파일의 이름
  plot_num = 0  ! pseudo 전자 수 밀도 추출 (Bohr^-3)
/  ! &INPUTPP 끝
&PLOT  ! 추출 자료를 외부 격자 형식으로 변환
  nfile         = 1  ! 합성에 사용할 중간 파일은 1개
  filepp(1)     = 'si.rho.filplot'  ! 읽을 첫 중간 파일; INPUTPP의 filplot과 연결
  weight(1)     = 1.0  ! 첫 파일에 곱할 무차원 가중치 1; 값을 그대로 출력
  iflag         = 3  ! 3차원 공간 자료를 출력
  output_format = 6  ! 3차원 자료를 Gaussian Cube 형식으로 저장
  fileout       = 'si.rho.cube'  ! 변환한 공간 격자의 최종 파일명
/  ! &PLOT 끝
```

퍼텐셜 입력도 같은 두 블록을 사용하며 아래 항목을 모두 바꾼다. 추출은 SCF 저장 자료를 읽으므로 전하 밀도 Cube를 먼저 만들 필요는 없다.[14,22,35]

| 입력 파일 | `plot_num` | `filplot`과 `filepp(1)` | `fileout` |
| --- | ---: | --- | --- |
| `si.vks.in` | 1 | `si.vks.filplot` | `si.vks.cube` |
| `si.ves.in` | 11 | `si.ves.filplot` | `si.ves.cube` |

Cube 확장자는 저장 형식이며 물리량을 결정하지 않는다. 파일의 셀·원자·격자와 `plot_num` 및 단위를 함께 기록해야 전하 밀도와 퍼텐셜을 구분할 수 있다.[14,22,35]

### (2) LDOS와 ILDOS

LDOS는 지정 에너지에서 상태의 공간 분포를, ILDOS는 지정 에너지 구간의 공간 분포를 다룬다. QE의 `plot_num=3`과 `10`을 각각 사용한다. 입력 에너지·폭이 eV라는 사실만으로 격자 값의 에너지 정규화도 eV당이라고 해석해서는 안 된다. 격자 값을 정량 비교할 때에는 사용 버전의 출력 규약과 공간·에너지 정규화를 함께 확인한다.[14,34]

`si.ildos.in`은 다음과 같다. 선행 자료는 [6절 DOS](#1-dos)의 균일 NSCF와 보존한 파동함수이며, 관심 구간은 `nbnd`가 확보한 에너지 범위 안에 있어야 한다. 예시의 0–2 eV는 **원자료 에너지 기준**의 구간이며 Si의 특정 밴드를 지칭하지 않는다. `emin/emax`는 `&INPUTPP` 안에 둔다.[5,14,15,37]

```fortran
&INPUTPP  ! 저장 전자상태에서 물리량 추출
  prefix   = 'si'  ! 선행 pw.x 계산의 저장 자료 식별자
  outdir   = './tmp'  ! 선행 pw.x 저장 자료를 읽을 경로
  filplot  = 'si.ildos.filplot'  ! 추출한 물리량을 보존할 중간 파일의 이름
  plot_num = 10  ! emin–emax 구간의 상태를 적분한 공간 분포
  emin     = 0.0  ! 구간 하한 0.0 eV; 원자료 에너지 기준
  emax     = 2.0  ! 구간 상한 2.0 eV; 원자료 에너지 기준
/  ! &INPUTPP 끝
&PLOT  ! 추출 자료를 외부 격자 형식으로 변환
  nfile         = 1  ! 합성에 사용할 중간 파일은 1개
  filepp(1)     = 'si.ildos.filplot'  ! 읽을 첫 중간 파일; INPUTPP의 filplot과 연결
  weight(1)     = 1.0  ! 첫 파일에 곱할 무차원 가중치 1; 값을 그대로 출력
  iflag         = 3  ! 3차원 공간 자료를 출력
  output_format = 6  ! 3차원 자료를 Gaussian Cube 형식으로 저장
  fileout       = 'si.ildos.cube'  ! 변환한 공간 격자의 최종 파일명
/  ! &PLOT 끝
```

한 에너지의 LDOS는 다음 `si.ldos.in`으로 추출한다. `emin=emax`로 한 에너지를 지정하며, `degauss_ldos`는 `dos.x`의 `degauss`와 달리 **eV**이다. 예시 에너지·폭은 관심 분석에 맞게 바꾼다.[14,34]

```fortran
&INPUTPP  ! 저장 전자상태에서 물리량 추출
  prefix         = 'si'  ! 선행 pw.x 계산의 저장 자료 식별자
  outdir         = './tmp'  ! 선행 pw.x 저장 자료를 읽을 경로
  filplot        = 'si.ldos.filplot'  ! 추출한 물리량을 보존할 중간 파일의 이름
  plot_num       = 3  ! 에너지별 공간 LDOS 추출
  emin           = 1.0  ! 구간 하한 1.0 eV; 원자료 에너지 기준
  emax           = 1.0  ! 구간 상한 1.0 eV; 원자료 에너지 기준
  degauss_ldos    = 0.1  ! LDOS의 에너지 퍼짐 폭 0.1 eV; dos.x degauss의 Ry와 구분
/  ! &INPUTPP 끝
```

LDOS 중간 파일에는 에너지별 이름이 붙을 수 있다. `si.ldos.out`의 `Writing data to file`에서 실제 파일명을 읽고, 선택한 에너지의 파일을 `si.ldos.selected.filplot`이라는 로컬 이름으로 복사했다고 가정하면 다음 `si.ldos.export.in`으로 변환할 수 있다. 빈 `&INPUTPP`는 재추출을 생략하고 `&PLOT`에서 저장된 자료를 읽게 한다.[14,22,34]

```fortran
&INPUTPP  ! 빈 블록: 추출 생략, 아래 PLOT에서 중간 파일을 읽음
/  ! &INPUTPP 끝
&PLOT  ! 추출 자료를 외부 격자 형식으로 변환
  nfile         = 1  ! 합성에 사용할 중간 파일은 1개
  filepp(1)     = 'si.ldos.selected.filplot'  ! 앞에서 선택·복사한 LDOS 중간 파일
  weight(1)     = 1.0  ! 첫 파일에 곱할 무차원 가중치 1; 값을 그대로 출력
  iflag         = 3  ! 3차원 공간 자료를 출력
  output_format = 6  ! 3차원 자료를 Gaussian Cube 형식으로 저장
  fileout       = 'si.ldos.cube'  ! 변환한 공간 격자의 최종 파일명
/  ! &PLOT 끝
```

### (3) 격자 출력

Fast Fourier transform (FFT) 격자는 plane wave 표현을 실공간으로 옮기는 계산 격자이다. `ecutrho`와 관련된 원래 격자의 정확도와 후처리의 표본 수는 구분한다. 더 촘촘한 출력만으로 원래 계산의 cutoff 오차가 줄어들지는 않는다.[4,5,14,22]

| 필요한 자료 | `&PLOT` 선택 | 함께 지정·확인할 항목 |
| --- | --- | --- |
| 3차원 Cube | `iflag=3`, `output_format=6` | 셀·원점·세 격자 방향과 값 |

격자를 배열로 읽을 때에도 축마다의 점 수·벡터·원점·저장 순서를 유지한다. 비직교 셀의 세 배열 인덱스는 Cartesian 좌표 자체가 아니다. 같은 배열 형식이라도 밀도·퍼텐셜·LDOS의 단위는 서로 다르다.[5,14,22]

## 8. 요약

- 입력 문법은 namelist와 card로 나뉘며 구조·좌표·단위와 `prefix/outdir`를 함께 관리한다.
- SCF 수렴, cutoff·$k$점 수렴, 원자·셀 최적화 종료는 서로 다른 확인 대상이다.
- DOS·PDOS에는 균일 NSCF 자료를, 밴드 분산에는 SCF에서 출발한 경로 계산 자료를 사용한다.
- `pp.x`의 물리량 선택과 격자 형식 선택을 구분하고, 에너지 표와 실공간 분포의 축·단위를 확인한다.
- EOS는 여러 부피의 에너지 계산과 함수 맞춤으로 구성하며, `ev.x`의 입력 단위와 첫 열의 의미를 명시한다.

## 9. 참고문헌

1. Quantum ESPRESSO Foundation, “Documentation,” *Quantum ESPRESSO* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/documentation/).
2. P. Giannozzi et al., “QUANTUM ESPRESSO: a modular and open-source software project for quantum simulations of materials,” *Journal of Physics: Condensed Matter* **21**, 395502 (2009). [DOI](https://doi.org/10.1088/0953-8984/21/39/395502).
3. University of Illinois Urbana-Champaign, “Module 2: Quantum Espresso Walkthrough,” *MSE 404 Electronic Materials* (2026). [강의 자료](https://courses.grainger.illinois.edu/MSE404ELA/sp2026/6.DFT-walkthrough.pdf).
4. P. Giannozzi et al., “Advanced capabilities for materials modelling with Quantum ESPRESSO,” *Journal of Physics: Condensed Matter* **29**, 465901 (2017). [DOI](https://doi.org/10.1088/1361-648X/aa8f79).
5. Quantum ESPRESSO Foundation, “pw.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_PW.html).
6. S. Cottenier, “geometry optimization : E(V) and EOS,” *Computational Materials Physics* (2022), pp. 1–5. [강의 자료](https://www.compmatphys.org/wp-content/uploads/2022/10/project_05b_EV-and-EOS.pdf).
7. Quantum ESPRESSO Foundation, “Unified Pseudopotential Format,” *Quantum ESPRESSO Pseudopotentials* (2026년 9월 확인). [형식 명세](https://pseudopotentials.quantum-espresso.org/home/unified-pseudopotential-format).
8. G. Prandini et al., “Precision and efficiency in solid-state pseudopotential calculations,” *npj Computational Materials* **4**, 72 (2018). [DOI](https://doi.org/10.1038/s41524-018-0127-2).
9. Quantum ESPRESSO Foundation, “PWscf User’s Guide: Data files,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/pw_user_guide/node9.html).
10. SCM, “Quantum ESPRESSO Properties,” *AMS 2026.1 Documentation* (2026년 9월 확인). [Interface documentation](https://www.scm.com/doc/QuantumEspresso/properties.html).
11. R. González, C. Pinilla and C. Espejo, “Quantum ESPRESSO Hands-on session,” *ICTP SMR3966* (2024), based on the MaX School tutorial by P. Delugas et al. (2021). [강의 자료](https://indico.ictp.it/event/10504/session/0/contribution/2/material/slides/0.pdf).
12. Quantum ESPRESSO Foundation, “dos.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_DOS.html).
13. Quantum ESPRESSO Foundation, “projwfc.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_PROJWFC.html).
14. Quantum ESPRESSO Foundation, “pp.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_PP.html).
15. AiiDA Developers, “ProjwfcParser,” *aiida-quantumespresso* (2026년 9월 확인). [원본 parser](https://github.com/aiidateam/aiida-quantumespresso/blob/main/src/aiida_quantumespresso/parsers/projwfc.py).
16. S. de Gironcoli, “First steps with a periodic DFT code: Quantum ESPRESSO,” SISSA tutorial (2011). [강의 자료](https://www.people.sissa.it/~degironc/2011/tutorial_surface.pdf).
17. ASE Developers, “ase.eos,” *Atomic Simulation Environment Documentation* (2026년 9월 확인). [공식 source documentation](https://docs.ase-lib.org/_modules/ase/eos.html).
18. S. Narasimhan, “How to do simple calculations with Quantum ESPRESSO,” JNCASR slides reproduced in *Quantum ESPRESSO workshop — Spring 2018*, pp. 57–65. [기관 배포 강의 자료](https://bpb-us-e1.wpmucdn.com/sites.psu.edu/dist/1/89076/files/2018/05/QE-intro-phzted.pdf).
19. E. Menendez, “Fundamentos teóricos de Quantum-ESPRESSO,” *Tutorial Quantum-ESPRESSO, Chihuahua* (2009), pp. 13–15, Universidad de Chile. [강의 자료](https://www.gnm.cl/uploads/Cursos/tutchihuac2.pdf).
20. PAOFLOW Developers, “PAOFLOW.inputs.read_QE_xml,” *PAOFLOW Documentation* (2026년 9월 확인). [Parser 문서](https://paoflow.org/en/latest/_modules/PAOFLOW/inputs/read_QE_xml.html).
21. Quantum ESPRESSO Foundation, “PWscf reference output: total energy, forces, and stress,” *Quantum ESPRESSO source repository* (2026년 9월 확인). [공식 예제 출력](https://github.com/QEF/q-e_old/blob/master/PHonon/examples/GRID_recover_example/reference/alas.scf.out).
22. B. Grosso et al., “Visualization of electronic density,” *Computer Physics Communications* **195**, 1–13 (2015), Appendix A. [DOI](https://doi.org/10.1016/j.cpc.2015.04.003), [기관 원문](https://carbonlab.net.technion.ac.il/files/2016/06/Grosso-Computer-physics-communications-2015-Visualization-of-electronic-denisty.pdf).
23. Quantum ESPRESSO Foundation, “Pseudopotentials,” *Quantum ESPRESSO* (2026년 9월 확인). [공식 안내](https://www.quantum-espresso.org/pseudopotentials/).
24. M. J. van Setten et al., “The PseudoDojo: Training and grading a 85 element optimized norm-conserving pseudopotential table,” *Computer Physics Communications* **226**, 39–54 (2018). [DOI](https://doi.org/10.1016/j.cpc.2018.01.012).
25. A. Dal Corso, “Pseudopotentials periodic table: From H to Pu,” *Computational Materials Science* **95**, 337–350 (2014). [DOI](https://doi.org/10.1016/j.commatsci.2014.07.043).
26. Quantum ESPRESSO Foundation, “Troubleshooting: Self-consistency is slow or does not converge,” *PWscf User’s Guide* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/pw_user_guide/node21.html).
27. H. J. Monkhorst and J. D. Pack, “Special points for Brillouin-zone integrations,” *Physical Review B* **13**, 5188–5192 (1976). [DOI](https://doi.org/10.1103/PhysRevB.13.5188).
28. F. Giustino, “Automatic optimization of atomic coordinates,” *An introduction to density functional theory for experimentalists*, Tutorial 3.1, PARADIM School, Cornell (2016), pp. 2–6. [강의 자료](https://www.paradim.org/sites/default/files/2019-05/Automatic_Optimization_and_Elastic_Constants.pdf).
29. Quantum ESPRESSO Foundation, “2 Compilation,” *PWscf User’s Guide* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/pw_user_guide/node6.html).
30. Quantum ESPRESSO Foundation, “`ev.x` source: E(V) data fitting,” *Quantum ESPRESSO 7.5 source repository*, tag `qe-7.5` (2026년 9월 확인). [공식 source](https://gitlab.com/QEF/q-e/-/blob/qe-7.5/PW/tools/ev.f90).
31. AiiDA Developers, “DosParser,” *aiida-quantumespresso* (2026년 9월 확인). [원본 parser](https://github.com/aiidateam/aiida-quantumespresso/blob/main/src/aiida_quantumespresso/parsers/dos.py).
32. Quantum ESPRESSO Foundation, “bands.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_BANDS.html).
33. AiiDA Developers, “Workflows: band structure with Quantum ESPRESSO,” *AiiDA Tutorials* (2026년 9월 확인). [공식 교육 문서](https://aiida-tutorials.readthedocs.io/en/main/sections/running_processes/workflows.html).
34. C. Wolf, “misbehaving pp.x for plot_num 3,” *Quantum ESPRESSO users mailing list* (2020). [실행 사례](https://lists.quantum-espresso.org/pipermail/users/2020-April/044268.html).
35. Computational Materials Physics, “Work function,” educational tutorial (2022). [강의 자료](https://compmatphys.org/wp-content/uploads/2022/09/work-function.pdf).
36. L. Groß, *GenLocDip: A program to calculate local electric dipole moments via Atoms-In-Molecules (AIM) analysis*, version 0.4 (2016), §5.3, pp. 8–9, Universität Hamburg. [프로그램 매뉴얼](https://www.chemie.uni-hamburg.de/institute/ac/arbeitsgruppen/herrmann/software/genlocdip/manual.pdf).
37. G. Fratesi, “Re: question regarding ILDOS plots in PP.x,” *Quantum ESPRESSO users mailing list* (2015). [답변](https://lists.quantum-espresso.org/pipermail/users/2015-May/032171.html).
