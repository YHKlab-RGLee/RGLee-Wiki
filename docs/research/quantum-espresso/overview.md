---
description: Si 예제로 Quantum ESPRESSO의 입력 작성, 수렴 시험, 구조 최적화와 전자구조 및 공간 분포 분석을 따라가는 실습 안내
---

# Quantum ESPRESSO: Overview

Quantum ESPRESSO (QE)는 density functional theory (DFT)에 기반한 전자구조 계산 프로그램 모음이다. 이 글에서는 Si 결정 하나를 대상으로 입력 파일을 만들고, 계산 결과를 확인한 뒤 구조 최적화와 후처리로 이어 간다. DFT의 기본 개념은 알고 있다고 가정하며, QE에서 **어떤 파일을 준비하고 어느 프로그램에 넘겨야 하는지**에 집중한다.[1,2,3]

설치 과정은 다루지 않는다. 아래 명령과 입력은 QE 7.5 문서를 바탕으로 구성한 실습 예이며, 이 문서를 작성하면서 QE를 실행하지는 않았다. 제시한 cutoff, 격자와 종료 기준은 출발값이다. 선택한 pseudopotential과 필요한 정확도에 맞는 값은 4절의 수렴 시험으로 결정한다.

## 1. Si 계산의 모형과 진행 순서

QE의 `pw.x`는 Kohn–Sham 파동함수를 plane wave basis로 전개한다. 파동함수에 포함할 평면파의 범위는 `ecutwfc`로 제한하고, 전하 밀도와 퍼텐셜을 표현하는 범위는 `ecutrho`로 정한다. 원자핵과 내부 전자의 효과는 pseudopotential로 주어진다. 따라서 구조만 입력한다고 계산 모형이 완성되는 것은 아니다. Pseudopotential, 두 cutoff와 Brillouin zone의 $k$점 표본을 함께 정해야 한다.[2,4,5,3]

실습 대상은 원자 두 개를 포함하는 diamond Si primitive cell이다. 비자성 계산을 수행하며 spin–orbit coupling은 포함하지 않는다. 처음에는 격자와 원자를 고정한 채 self-consistent field (SCF) 계산으로 전하 밀도를 수렴시킨다. 그다음 수치 조건을 확정하고 구조를 최적화한다. 최종 구조에서 다시 얻은 전하 밀도가 이후 전자구조 분석의 출발점이다.[5,3,6]

`pw.x`는 사람이 읽는 표준 출력과 후속 프로그램이 읽는 저장 자료를 함께 만든다. 저장 위치를 정하는 `outdir`, 계산 자료를 구분하는 `prefix`가 후처리 입력에도 반복해서 등장하는 이유이다. 다음 표는 이 글에서 실제로 사용할 프로그램과 결과의 관계를 보여 준다.[7,8,9,10,11,12,13,14]

| 단계 | 프로그램 | 읽는 자료 | 확인할 결과 |
| --- | --- | --- | --- |
| 전하 밀도 수렴·구조 최적화 | `pw.x` | 구조와 계산 조건을 적은 입력, pseudopotential | 에너지·힘·응력, 최종 구조, 저장 자료 |
| 전체 상태 밀도 | `dos.x` | 조밀한 $k$점 격자의 고유값 | 에너지별 상태 수 표 |
| 원자 궤도 투영 | `projwfc.x` | 고유값과 파동함수 | 원자·궤도별 상태 밀도 표 |
| 공간 분포 | `pp.x` | 전하 밀도, 퍼텐셜 또는 파동함수 | 선·평면·입체 격자의 값 |
| 밴드 분산 | `pw.x`, `bands.x` | 수렴 밀도와 역공간 경로 | 경로별 밴드 에너지 표 |
| 에너지–부피 곡선 맞춤 | `ev.x` | 여러 부피에서 계산한 에너지 표 | 평형 부피와 체적 탄성률 |

후처리는 표준 출력을 서로 연결하는 shell pipe가 아니다. 같은 저장 자료를 후속 프로그램이 다시 읽는 과정이다. 이 글에서는 조밀한 격자가 필요한 상태 밀도·투영·공간 분석을 먼저 마치고 밴드 경로 계산을 마지막에 한다. 서로 다른 $k$점 집합의 결과를 같은 분석에 섞지 않기 위한 순서이다.[7,15,12,13,14]

## 2. Pseudopotential과 작업 폴더

### (1) Si 파일의 선택과 입수

QE는 Unified Pseudopotential Format (UPF) 파일을 읽는다. UPF는 파일 형식의 이름이며, 계산 방법 하나를 뜻하지 않는다. Norm-conserving (NC), ultrasoft (US), projector augmented-wave (PAW) 자료를 담을 수 있으므로 `.UPF`라는 확장자만으로 종류를 판단하지 않는다.[2,16,17]

[QE의 pseudopotential 안내](https://www.quantum-espresso.org/pseudopotentials/)에서 검증된 배포처로 이동한다. 이 실습에서는 Perdew–Burke–Ernzerhof (PBE) 교환·상관 함수에 맞는 Si 파일을 선택하고, 상대론 처리는 scalar-relativistic 자료로 통일한다. Standard Solid-State Pseudopotentials (SSSP)는 여러 배포처의 자료를 검사해 원소별 파일과 권장 cutoff를 제공하므로 시작점을 찾기 좋다. 선택한 collection의 버전, Si 항목의 실제 파일 이름, 권장 파동함수·전하 밀도 cutoff를 함께 적어 둔다.[17,18]

다른 선택지로는 NC 자료를 제공하는 PseudoDojo와 US·PAW 자료를 제공하는 PSlibrary가 있다. 어느 배포처를 택하든 아래 계산 도중 파일을 바꾸지 않는다. 파일을 바꾸면 valence 구성과 기준 에너지가 달라질 수 있어 이전 수렴 시험을 그대로 적용할 수 없다.[16,17,18,19,20]

| 파일에서 확인할 항목 | 실습에 적용할 내용 |
| --- | --- |
| 원소·valence 구성 | Si이며 의도한 valence 전자를 포함하는가 |
| 교환·상관 함수 | 선택한 PBE 모형과 일치하는가 |
| 상대론 처리 | 이번 비자성 예제의 scalar-relativistic 조건에 맞는가 |
| NC·US·PAW 구분 | 해당 자료에 권장된 두 cutoff는 얼마인가 |
| 원자 파동함수 정보 | 뒤의 원자 궤도 투영에 필요한 정보가 포함되는가 |
| 배포 버전·원본 파일명 | 나중에 같은 자료를 다시 식별할 수 있는가 |

UPF에는 원자 방사형 격자, 퍼텐셜, 투영자와 원자 파동함수 등의 정보가 들어 있다. 특히 US·PAW에서는 전하 밀도의 보강 성분을 표현해야 하므로 `ecutrho`를 `ecutwfc`의 고정 배수로 정하는 관행만 믿지 말고 배포처 권고와 수렴 시험을 따른다.[4,5,16,18]

### (2) 파일 이름과 상대 경로

작업 폴더를 하나 만들고 내려받은 Si UPF를 그 안의 `pseudo/`에 둔다. 아래 예제의 `Si.UPF`는 **사용자가 선택한 파일의 로컬 이름**이다. 원본을 이 이름으로 복사해 사용하거나, 이후 `ATOMIC_SPECIES`의 파일 이름을 실제 다운로드 이름으로 바꾸면 된다. 두 방법을 섞지 않는다.[5,3]

```text
si-tutorial/
├── pseudo/
│   └── Si.UPF
├── si.scf.in
└── tmp/
```

모든 명령은 `si-tutorial/` 안에서 수행하는 것으로 설명한다. `pseudo_dir='./pseudo'`와 `outdir='./tmp'`도 이 위치를 기준으로 한다. 후속 입력을 다른 폴더에서 실행한다면 상대 경로가 같은 저장 위치를 가리키는지 다시 확인해야 한다.[5,7,3]

다운로드한 원본 파일명·버전과 함께 `sha256sum pseudo/Si.UPF`로 얻은 식별값을 기록하면, 이름만 같고 내용이 다른 파일을 구분하기 쉽다. 이는 실습 파일 관리 방법이며 별도의 QE 입력 문법은 아니다.

## 3. 첫 SCF 입력과 출력 읽기

### (1) 완전한 `si.scf.in`

다음은 생략된 블록이 없는 `pw.x` 입력이다. 격자 벡터는 Å, 원자 좌표는 해당 벡터에 대한 분율 좌표로 적었다. 시작 격자는 cubic lattice parameter를 $5.431\ \text{Å}$로 놓은 예이며, 평형값을 미리 정답으로 가정하지 않는다. `50/400 Ry`와 $8\times8\times8$ 격자도 문법을 설명하기 위한 출발값이다. 선택한 UPF의 권장 cutoff가 더 크다면 먼저 그 값으로 바꾼다.[5,3,18]

```fortran
&CONTROL
  calculation = 'scf'
  prefix      = 'si'
  pseudo_dir  = './pseudo'
  outdir      = './tmp'
  tprnfor     = .true.
  tstress     = .true.
  disk_io     = 'low'
/
&SYSTEM
  ibrav       = 0
  nat         = 2
  ntyp        = 1
  ecutwfc     = 50.0
  ecutrho     = 400.0
  occupations = 'fixed'
/
&ELECTRONS
  conv_thr    = 1.0d-10
  mixing_beta = 0.7
/
ATOMIC_SPECIES
Si  28.085  Si.UPF

ATOMIC_POSITIONS (crystal)
Si  0.00  0.00  0.00
Si  0.25  0.25  0.25

K_POINTS (automatic)
8 8 8  0 0 0

CELL_PARAMETERS (angstrom)
0.0000  2.7155  2.7155
2.7155  0.0000  2.7155
2.7155  2.7155  0.0000
```

입력 앞부분의 `&CONTROL`, `&SYSTEM`, `&ELECTRONS`는 Fortran namelist이며 각각 `/`로 닫는다. 순서대로 계산 종류와 파일 경로, 구조와 전자계, 전자 반복 수렴을 정한다. 뒤의 `ATOMIC_SPECIES` 등은 card이며 `/`로 닫지 않는다. `ATOMIC_SPECIES`의 `Si` 표식이 원자 위치와 UPF를 연결한다. `nat=2`는 셀 안의 원자 수, `ntyp=1`은 원자종의 수이다.[5,3]

`ibrav=0`은 격자 벡터 세 개를 직접 제공한다는 뜻이다. `crystal` 좌표 $(f_1,f_2,f_3)$는 위치 $\mathbf r=f_1\mathbf a_1+f_2\mathbf a_2+f_3\mathbf a_3$를 나타낸다. 여기서 $\mathbf a_i$는 `CELL_PARAMETERS`의 각 행이다. 분율 좌표 `0.25 0.25 0.25`를 Å 단위 위치로 읽으면 전혀 다른 구조가 된다.[5,3]

`K_POINTS (automatic)`의 앞 세 정수는 각 역격자 방향의 분할 수이고, 뒤 세 정수는 QE의 0/1 이동 플래그이다. 이 예제는 모두 0으로 고정한다. 격자 수렴 시험에서도 먼저 이동 플래그를 유지해야 분할 수의 효과를 비교하기 쉽다. `K_POINTS gamma`는 $\Gamma$점만 사용하는 별도 선택이며, 여기의 Si 결정 예제를 대신하는 기본값이 아니다.[5,21,22]

### (2) 실행 명령과 수렴 판정

입력과 출력 이름을 분리해 다음과 같이 실행한다. 아래 명령은 독자가 수행할 절차이며 실행 결과를 제시한 것이 아니다.[5,3]

```bash
pw.x -in si.scf.in > si.scf.out
```

`si.scf.out`은 처음부터 한 번 읽는다. 구조·원자종·전자 수가 의도대로 해석되었는지 확인한 다음 전자 반복의 수렴 여부와 최종 에너지를 찾는다. 반복 중 에너지가 출력되었다는 사실과 SCF가 종료 기준을 만족했다는 사실은 다르다. `! total energy` 줄을 추출하더라도 수렴 메시지와 함께 읽는다.[3,23]

다음 검색은 긴 출력에서 관련 부분을 찾는 용도이다. 구조 최적화 출력에는 이런 줄이 여러 번 나타나므로, 검색 결과의 마지막 줄 하나만 보고 계산 성공을 판정하지 않는다.

```bash
rg -n 'convergence|!.*total energy|Forces acting|total stress|JOB DONE' si.scf.out
```

| 확인 대상 | 출력의 단위·형태 | 이 단계에서 읽을 내용 |
| --- | --- | --- |
| 전체 에너지 | Ry, 구조 하나당 스칼라 | 수렴한 계산의 값을 기록한다 |
| 원자별 힘 | Ry/Bohr, 원자마다 3성분 | 구조를 바꿀 필요가 있는지 판단한다 |
| 응력 | Ry/Bohr$^3$ 및 kbar, $3\times3$ 표 | 원자 힘이 작아도 셀에 잔류 응력이 있는지 확인한다 |
| 고유값 | 출력에 표시된 eV | 점유 상태와 나중에 계산할 비점유 상태의 범위를 구분한다 |

이는 `tprnfor`와 `tstress`를 켠 이유이기도 하다. 에너지 하나만으로는 원자 위치와 셀 크기가 모두 적절한지 알 수 없다. 단위는 각 출력의 머리글을 따른다. 특히 후처리 표는 에너지를 eV로 쓰므로 SCF 전체 에너지의 Ry와 구분한다.[5,3,23]

### (3) 다음 단계에 남겨야 할 자료

`./tmp/si.save/`에는 구조와 전자상태 정보를 담는 `data-file-schema.xml` 등이 생긴다. Extensible Markup Language (XML)는 구조화된 자료 형식이다. 그 밖의 전하 밀도·파동함수 저장 방식과 파일 배치는 구현에 따라 달라질 수 있으므로 저장 폴더에서 일부 파일만 골라 이동하지 않는다. 후처리에는 같은 `prefix/outdir`를 넘기고 프로그램이 필요한 자료를 읽게 한다.[7,15]

표준 출력은 계산을 사람이 확인하는 기록이고, 저장 자료는 후속 계산의 입력이다. 따라서 `si.scf.out`만 남겨서는 뒤의 투영이나 공간 분포 계산을 재개할 수 없다. 반대로 저장 자료만 보존하고 입력·출력을 버리면 어떤 구조와 수렴 조건으로 만들었는지 확인하기 어렵다.[7,15,14]

## 4. Cutoff와 $k$점의 수렴 시험

첫 SCF가 끝났다고 계산 조건이 확정된 것은 아니다. SCF 수렴은 **주어진 기저와 $k$점 안에서 전자 밀도가 일관되어 있다**는 뜻이다. 기저나 적분 격자를 더 정밀하게 했을 때 목표 물성이 안정적인지는 별도로 확인한다.[5,3,18,22]

`si.scf.in`을 복사해 한 종류의 조건만 바꾼다. 예를 들어 `si.cut60.in`에서는 `ecutwfc=60`, `ecutrho=480`을 시험하고, `si.k10.in`에서는 cutoff를 고정한 채 `K_POINTS`를 `10 10 10 0 0 0`으로 바꾼다. 이 숫자들은 비교 파일을 만드는 예시이며 합격 기준이 아니다. 각 파일의 `prefix`도 `si_cut60`, `si_k10`처럼 바꾸면 결과를 구분할 수 있다.

```bash
pw.x -in si.cut60.in > si.cut60.out
pw.x -in si.k10.in > si.k10.out
```

실제로는 배포처 권장값부터 cutoff를 단계적으로 높여 변화를 기록한다. 첫 시험에서 두 cutoff를 함께 올렸다면, 이후 `ecutwfc`를 고정하고 `ecutrho`만 더 올려 전하 밀도 격자의 영향을 분리한다. 파동함수 기저가 충분해도 전하 밀도 표현이 부족하면 힘·응력이 원하는 수준까지 안정되지 않을 수 있다.[5,3,18]

| 시험 | 유지할 조건 | 바꿀 조건 | 비교할 양 |
| --- | --- | --- | --- |
| 파동함수 기저 | 구조, UPF, $k$점 | `ecutwfc`, 충분한 `ecutrho` | 에너지 차이·힘·응력 |
| 전하 밀도 표현 | 구조, UPF, `ecutwfc`, $k$점 | `ecutrho` | 힘·응력과 에너지 변화 |
| 역공간 적분 | 구조, UPF, 수렴된 cutoff | $k$점 분할 수 | 에너지 차이·압력, 필요한 전자구조량 |

비교를 원자당 에너지로 표현하려면 각 시험의 셀 에너지 차이를 같은 원자 수로 나눈다. 이 실습은 두 원자 셀을 유지하므로 가장 정밀한 시험의 에너지를 $E_{\mathrm{ref}}$, 시험 에너지를 $E_i$라 할 때 원자당 차이는 다음과 같다.

$$
\Delta e_i=\frac{E_i-E_{\mathrm{ref}}}{2}.
$$

이 값은 수치 조건에 따른 변화량이며 실제 물질의 응집 에너지가 아니다. 비교하는 구조·UPF·교환상관 모형은 같아야 한다. 목표가 평형 부피라면 에너지뿐 아니라 압력의 안정성을, 목표가 상태 밀도 곡선이라면 그 곡선의 $k$점 의존성도 확인한다.[3,18,22]

에너지 오차가 허용 범위에 들어온 조건을 `si.scf.in`에 반영하고, 그 조건을 뒤의 모든 입력에 사용한다. primitive cell을 다른 셀 표현으로 바꾸면 같은 `8 8 8`도 같은 역공간 간격을 뜻하지 않는다. 이 실습에서는 동일한 두 원자 셀을 사용한다.[5,21,22]

## 5. 구조 최적화와 에너지–부피 곡선

### (1) 원자 위치만 바꾸는 `relax`

`relax`는 셀을 고정하고 원자 위치를 최적화한다. 수렴 조건을 반영한 `si.scf.in`을 `si.relax.in`으로 복사한 뒤 `&CONTROL`의 계산 종류를 바꾸고 원자 최적화 종료 기준을 추가한다. 다음은 **수정할 항목만 보인 조각**이다. 기존 구조·원자종·cutoff·$k$점과 `&ELECTRONS`는 모두 유지한다.[5,6]

```fortran
  calculation  = 'relax'
  prefix       = 'si_relax'
  etot_conv_thr = 1.0d-5
  forc_conv_thr = 1.0d-4
```

그리고 `&ELECTRONS`의 `/` 다음, 첫 card 앞에 아래 블록을 추가한다.[5,6]

```fortran
&IONS
  ion_dynamics = 'bfgs'
/
```

여기서 `'bfgs'`는 Broyden–Fletcher–Goldfarb–Shanno (BFGS) 최적화 선택이다. `conv_thr`는 각 구조에서의 전자 수렴 기준이고, `etot_conv_thr`와 `forc_conv_thr`는 원자 최적화의 에너지·힘 종료 기준이다. 제시한 수치는 실습용이며 두 계층의 오차가 목표 물성에 충분히 작은지 확인해야 한다.[5,6]

```bash
pw.x -in si.relax.in > si.relax.out
```

처음의 이상적인 Si 구조에서는 대칭 때문에 원자 위치 변화가 거의 없을 수 있다. 원자 최적화 과정을 관찰하려면 별도의 연습 파일에서 두 번째 원자의 분율 좌표를 `0.26 0.25 0.25`처럼 조금 변위시켜 시작할 수 있다. 이 변위는 연습용 설정이며 최적화된 구조가 아니다. 각 원자 단계의 힘과 마지막 좌표를 읽고, 전자 수렴과 원자 최적화 종료를 모두 확인한다.[5,6]

### (2) 셀도 바꾸는 `vc-relax`와 최종 SCF

평형 격자 크기를 구하려면 `vc-relax`를 사용한다. 변위를 주지 않은 Si 입력을 기준으로 `si.vc-relax.in`을 만들고 앞의 `relax` 설정을 적용하되, `calculation='vc-relax'`, `prefix='si_vc'`로 바꾼다. `&IONS` 뒤에는 아래 블록을 추가한다. `cell_dofree='all'`은 이 벌크 연습에서 셀 변형을 허용하는 선택이다.[5,6]

```fortran
&CELL
  cell_dynamics  = 'bfgs'
  press          = 0.0
  press_conv_thr = 0.5
  cell_dofree    = 'all'
/
```

`press`와 `press_conv_thr`의 단위는 kbar이다. 셀이 바뀌는 계산에서는 힘이 작다는 이유만으로 종료 상태를 받아들이지 말고 최종 응력과 압력도 확인한다. slab처럼 일부 길이를 유지해야 하는 계에는 이 셀 자유도를 그대로 적용하지 않는다.[5,6]

```bash
pw.x -in si.vc-relax.in > si.vc-relax.out
```

최적화가 끝나면 출력의 **마지막 셀과 원자 좌표를 한 쌍으로** 옮겨 `si.final.scf.in`을 만든다. 좌표 머리글의 단위도 함께 옮긴다. 초기 입력의 `angstrom`이나 `crystal` 표식을 결과의 숫자 앞에 무조건 붙이면 안 된다. `calculation='scf'`, `prefix='si_final'`로 설정하고 `&IONS`, `&CELL`, 원자 최적화용 종료 기준은 제거한다. 나머지 조건은 앞에서 수렴시킨 값을 유지한다.[5,6]

```bash
pw.x -in si.final.scf.in > si.final.scf.out
```

이 최종 고정 구조 계산의 에너지·힘·응력을 다시 읽는다. 셀이 변하면 같은 cutoff에서도 평면파 기저가 달라지므로 최적화 도중 값만으로 최종 정밀도를 판단하지 않는다. 이후의 입력에는 `si.final.scf.in`의 구조를 사용한다. 아래 후처리가 읽을 저장 자료는 이제 `prefix='si_final'`, `outdir='./tmp'`로 통일된다.[5,6,12]

### (3) 여러 부피의 에너지와 EOS

Equation of state (EOS)는 여러 부피에서 얻은 에너지를 함수에 맞추어 평형 부피와 체적 탄성률을 구하는 방법이다. `vc-relax`가 목표 압력에서 구조 하나를 찾는 계산이라면, EOS에는 서로 다른 부피의 계산점이 필요하다. QE의 `ev.x`는 그 점들을 맞추는 도구이며 부피별 `pw.x` 계산을 대신 실행하지 않는다.[24,25,26,27]

`si.final.scf.in`을 기준으로 셀 벡터 세 개에 같은 길이 배율 $s$를 곱해 `si.eos-s098.in`, `si.eos-s100.in`, `si.eos-s102.in`처럼 파일을 만든다. 파일명 예시의 배율은 각각 0.98, 1.00, 1.02이다. 실제 곡선 맞춤에는 예상 최소점의 양쪽을 포함하도록 더 많은 점을 선택한다. 각 점의 `prefix`를 구분하고 UPF, cutoff, 점유 방식과 $k$점 설정은 유지한다.[3,25,26]

분율 좌표와 셀 모양을 유지하는 등방적 변형에서는 기준 부피 $V_{\mathrm{ref}}$와 새 부피 $V$가 다음 관계를 갖는다.

$$
V=s^3V_{\mathrm{ref}}.
$$

따라서 길이를 2% 늘리는 것과 부피를 2% 늘리는 것은 다르다. 이 관계는 세 격자 벡터에 같은 $s$를 곱하는 기하학적 결과이다. 원자 내부 좌표를 추가로 완화할 필요가 있으면 각 부피에서 `relax`를 수행한다. 각 점에 영압 `vc-relax`를 적용하면 의도한 부피 표본이 유지되지 않는다.[5,6,25]

각 출력에서 수렴한 셀 에너지와 실제 셀 부피를 모아 `si.eos.dat`에 저장한다. 이번 실습은 **첫 열에 두 원자 셀의 부피(Bohr$^3$), 둘째 열에 그 셀의 전체 에너지(Ry)**를 쓰며 머리글은 넣지 않는다. `pw.x` 출력의 `unit-cell volume`에서 `(a.u.)^3`으로 표시된 값을 읽고, 같은 계산의 수렴 에너지와 짝지어 한 줄씩 적는다. 원자당 에너지와 셀 전체 부피를 섞지 않는다.[27,28]

```bash
pw.x -in si.eos-s098.in > si.eos-s098.out
pw.x -in si.eos-s100.in > si.eos-s100.out
pw.x -in si.eos-s102.in > si.eos-s102.out
# 나머지 부피의 계산을 마친 뒤 si.eos.dat를 준비한다.
ev.x
```

`ev.x`가 묻는 단위, 입력 방식, EOS 종류, 입력 파일, 출력 파일에 차례로 다음 다섯 줄을 응답한다. `au`는 여기서 부피 열의 Bohr$^3$ 단위에 대응하고 `1`은 `birch1`을 선택한다.[27,28]

```text
au
noncubic
1
si.eos.dat
si.eos.fit
```

`noncubic`은 이 호출에서 **첫 열을 부피로 읽게 하는 선택**이며, Si의 결정 대칭을 비입방이라고 선언한 것이 아니다. `fcc`를 고르면 첫 열을 격자 상수로 해석하므로 이미 부피를 적은 이 파일에는 사용하지 않는다. 결과 파일 `si.eos.fit`의 머리글에서 평형 부피와 체적 탄성률 및 단위를 읽고, 아래 자료에서 계산 에너지와 맞춘 에너지의 차이를 확인한다.[27,28]

부피 $V$와 셀 에너지 $E(V)$를 일관된 단위로 맞추면 평형 부피 $V_0$의 체적 탄성률 $B_0$는 곡률로 해석할 수 있다.

$$
B_0=V_0\left.\frac{\partial^2E}{\partial V^2}\right|_{V_0}.
$$

이는 영압 평형점에서의 관계이다. 실제 $B_0$는 유한한 계산점과 선택한 EOS 함수로 추정하므로, 최소점이 표본 범위 안에 있는지, 계산 에너지와 맞춘 곡선의 잔차가 작은지, 표본 범위를 바꾸어도 결과가 안정적인지 확인한다. 에너지 곡선이 얕으면 작은 수치 오차도 곡률에 영향을 줄 수 있어 4절의 수렴 시험이 선행되어야 한다.[25,26]

## 6. 조밀한 격자와 DOS·원자 궤도 투영

### (1) `si.nscf.in`의 준비

Density of states (DOS)는 에너지 구간마다 상태가 얼마나 존재하는지 나타낸다. 매끄러운 DOS를 얻으려면 SCF 에너지에 충분했던 격자보다 더 조밀한 $k$점 표본이 필요할 수 있다. 전하 밀도는 이미 수렴했으므로 non-self-consistent field (NSCF) 계산에서 그 밀도를 고정하고 추가 고유값과 파동함수를 구한다.[8,12,29]

`si.final.scf.in`을 `si.nscf.in`으로 복사한다. `&CONTROL`에서 `calculation='nscf'`로 바꾸고, `&SYSTEM`에 `nbnd=12`를 추가한다. `prefix='si_final'`, `outdir='./tmp'`, 최종 구조, UPF, cutoff와 `occupations='fixed'`는 유지한다. `nbnd`는 계산할 밴드 수이며, 여기의 12는 비점유 상태를 포함하기 위한 출발값이다. 관심 에너지 상한을 충분히 덮는지는 출력에서 확인한다.[5,12,13]

`K_POINTS` 부분은 다음으로 교체한다. 이 블록은 전체 입력이 아니라 기존 card의 대체 내용이다.[5,12]

```fortran
K_POINTS (automatic)
12 12 12  0 0 0
```

```bash
pw.x -in si.nscf.in > si.nscf.out
```

`si.nscf.out`에서 의도한 $k$점과 밴드 수를 읽었는지 확인한다. 이후 `dos.x`는 저장된 고유값을 사용하며 파동함수 자체는 요구하지 않지만, `projwfc.x`와 공간 상태 분석에는 파동함수가 필요하다. 여기서는 처음의 `disk_io='low'` 설정을 유지하고 저장 자료를 지우지 않는다.[7,8,10,12,14]

### (2) 전체 DOS와 에너지 축

이번 실습은 Gaussian broadening으로 DOS를 표시한다. Si의 SCF 점유를 `fixed`로 유지하는 것과, 후처리에서 이산 고유값을 폭이 있는 곡선으로 표현하는 것은 서로 다른 설정이다. 다음은 `dos.x`에 넘길 **완전한 입력 파일** `si.dos.in`이다.[8,29]

```fortran
&DOS
  prefix  = 'si_final'
  outdir  = './tmp'
  fildos  = 'si.dos.dat'
  ngauss  = 0
  degauss = 0.01
  DeltaE  = 0.02
/
```

`degauss=0.01`은 Ry 단위의 폭이고 `DeltaE=0.02`는 eV 단위의 출력 에너지 간격이다. 두 수치는 역할과 단위가 다르다. `Emin/Emax`를 생략해 우선 계산된 밴드 범위를 확인한 뒤 필요한 구간을 eV로 지정한다. 작은 `DeltaE`만으로 부족한 $k$점 표본을 보완할 수는 없다.[8,12,29]

```bash
dos.x -in si.dos.in > si.dos.out
```

`si.dos.dat`의 머리글을 읽고 첫 열을 에너지(eV), 해당 DOS 열을 states/eV로 그린다. 표는 공간 격자가 아니라 에너지 하나를 독립 변수로 하는 1차원 자료이다. 스핀 계산으로 확장하면 열 구성이 달라지므로 비자성 예제의 열 번호를 그대로 적용하지 않는다.[8,12,29]

DOS 원자료의 에너지 축과 그림에 사용할 기준을 구분한다. 원문 Si 예제도 원자료의 에너지 축 위에 Fermi 에너지를 따로 표시한다.[8,12] 여기서 그림 좌표를 $E_{\mathrm{plot}}=E-E_{\mathrm{zero}}$로 정의했다면, 역변환은 $E=E_{\mathrm{plot}}+E_{\mathrm{zero}}$이다. 이후 `emin/emax`를 정할 때에는 이 좌표 변환으로 원자료의 에너지를 복원한다. 이는 에너지 축 정의에서 직접 따르는 변환이며, 프로그램이 그림의 이동량을 자동으로 알아낸다는 뜻은 아니다.

대안인 tetrahedron 방법을 쓰려면 `pw.x`의 자동 균일 격자와 `occupations='tetrahedra'`를 사용하고 후처리의 `degauss`를 제거하는 경로를 별도로 구성한다. 본문의 주 실습은 위 Gaussian 설정으로 통일한다.[8,10,12]

### (3) 원자 궤도별 PDOS

Projected density of states (PDOS)는 전체 상태를 원자 궤도 성분으로 나눈 것이다. `projwfc.x`는 UPF에 포함된 원자 파동함수를 직교화해 투영에 사용한다. 따라서 PDOS는 원자 주변 공간을 단순히 잘라 적분한 값이 아니라 선택한 투영 함수에 따른 분석이다.[10,29,14,30]

`si.nscf.in`을 다시 실행할 필요 없이 같은 저장 자료를 읽는다. 다음을 **완전한 후처리 입력** `si.pdos.in`으로 저장한다. DOS와 폭·에너지 간격을 같게 두어 곡선을 비교한다.[10,29,14]

```fortran
&PROJWFC
  prefix  = 'si_final'
  outdir  = './tmp'
  filpdos = 'si.pdos'
  ngauss  = 0
  degauss = 0.01
  DeltaE  = 0.02
/
```

```bash
projwfc.x -in si.pdos.in > si.pdos.out
```

`si.pdos`는 단일 결과 파일명이 아니라 출력 이름의 앞부분이다. `si.pdos.pdos_tot`과 `si.pdos.pdos_atm#N(Si)_wfc#M(l)` 같은 파일을 확인한다. $N$은 원자 번호, $M$은 UPF의 원자 파동함수 번호, $l$ 표식은 s·p 등의 각운동량 채널을 가리킨다. 실제 포함된 궤도와 파일 수는 사용한 UPF에 따라 읽는다.[10,14]

비자성 원자별 파일의 열 구조는 다음과 같다. 이 블록은 출력 머리글의 의미를 설명하는 것으로 수치 계산 결과가 아니다.[10,14]

```text
E(eV)  LDOS(E)  PDOS_1(E) ... PDOS_(2l+1)(E)
```

이때 `LDOS(E)` 열은 그 원자 파동함수 채널의 여러 자기양자수 성분을 합한 값이다. 다음 절에서 설명할 위치 $\mathbf r$에 따른 local density of states (LDOS)와 이름만 보고 혼동하지 않는다. 이 파일에는 공간 좌표 축이 없으며, 모든 DOS 열의 단위는 states/eV이다.[10,14]

DOS와 PDOS를 겹쳐 볼 때에는 동일한 에너지 이동과 같은 폭을 적용한다. 전체 DOS와 원자 투영의 합이 어떤 관계를 보이는지 확인하되, 투영 함수가 모든 상태를 완전히 표현한다고 미리 가정하지 않는다. 관심 범위에 비점유 밴드가 부족하다면 먼저 `nbnd`를 늘려 NSCF와 두 후처리를 다시 수행한다.[10,29,14,30]

## 7. 전하 밀도·퍼텐셜·공간 LDOS

### (1) 전하 밀도를 입체 격자로 내보내기

앞 절의 표는 에너지별 상태 수를 나타냈다. 이번에는 **값이 셀의 어느 위치에 분포하는지**를 본다. `pp.x`의 `&INPUTPP`는 원하는 물리량을 추출하고, `&PLOT`은 그 값을 외부에서 읽을 형식으로 쓴다. 추출 중간 파일 `filplot`과 최종 출력 `fileout`은 서로 다른 파일이다.[11,31]

아래는 전하 밀도를 Gaussian Cube로 쓰는 **완전한 입력** `si.rho.in`이다. 이미 수렴한 밀도를 읽으며 새 SCF는 필요하지 않다. 후속 공간 상태 분석까지 끝내기 전에는 아직 밴드 경로 계산으로 넘어가지 않는다.[11,31]

```fortran
&INPUTPP
  prefix   = 'si_final'
  outdir   = './tmp'
  filplot  = 'si.rho.filplot'
  plot_num = 0
/
&PLOT
  nfile         = 1
  filepp(1)     = 'si.rho.filplot'
  weight(1)     = 1.0
  iflag         = 3
  output_format = 6
  fileout       = 'si.rho.cube'
/
```

```bash
pp.x -in si.rho.in > si.rho.out
```

`si.rho.out`에서 추출과 파일 쓰기가 끝났는지 확인하고, `si.rho.cube`를 Cube를 지원하는 시각화 도구로 연다. 파일에 포함된 셀과 원자 위치를 먼저 확인한 다음 등값면이나 단면을 본다. `plot_num=0`의 자료는 pseudo 전하 밀도이며, 핵 근처의 all-electron 밀도로 해석하지 않는다. 밀도는 전하량 자체가 아니라 전자 수에 해당하는 양으로 정규화된다.[11,31,16]

### (2) 같은 격자에 저장하는 퍼텐셜

퍼텐셜도 `pp.x`로 내보낼 수 있다. `si.rho.in`을 복사해 아래 표의 항목을 바꾸되, `filplot`과 `filepp(1)`의 이름은 반드시 서로 같게 바꾼다. 나머지 `&PLOT`을 유지하면 두 결과 모두 3차원 Cube가 된다.[11,31,32]

| 입력 파일 | `plot_num` | 중간 파일 | `fileout` | 물리량 |
| --- | ---: | --- | --- | --- |
| `si.vks.in` | 1 | `si.vks.filplot` | `si.vks.cube` | $V_{\mathrm{bare}}+V_H+V_{\mathrm{xc}}$ |
| `si.ves.in` | 11 | `si.ves.filplot` | `si.ves.cube` | $V_{\mathrm{bare}}+V_H$ |

$V_{\mathrm{bare}}$는 국소 이온 퍼텐셜, $V_H$는 Hartree 항, $V_{\mathrm{xc}}$는 교환·상관 항이다. `plot_num=1`이 내보내는 것은 이들의 국소 합이며 비국소 투영자 연산자 자체를 공간 스칼라장으로 저장한다는 뜻은 아니다. 두 파일의 차이를 해석할 때 포함된 항부터 구분한다.[11,31,32]

```bash
pp.x -in si.vks.in > si.vks.out
pp.x -in si.ves.in > si.ves.out
```

QE가 내보내는 퍼텐셜은 전자가 느끼는 **에너지** 차원이다. 별도 표시가 없으면 Rydberg 원자 단위를 따르므로 이를 곧바로 volt 단위 전위로 읽지 않는다. Cube 확장자는 격자 저장 형식을 뜻할 뿐, 그 안의 값이 밀도인지 퍼텐셜인지 결정하지 않는다.[5,11,31,32]

### (3) 에너지별 LDOS와 구간 적분 ILDOS

공간 LDOS $D(\mathbf r,E)$는 위치 $\mathbf r$와 에너지 $E$를 함께 갖는 상태 밀도이다. 한 에너지에서 공간 분포를 볼 때는 `plot_num=3`, 정해진 구간의 분포를 모아 볼 때는 integrated local density of states (ILDOS)를 계산하는 `plot_num=10`을 선택한다.[11,33]

에너지 하한과 상한을 각각 $E_1$, $E_2$라 하고, 이 글에서는 에너지 구간을 합친 공간 분포 $I$를 다음 적분으로 정의한다. 이는 앞의 LDOS 정의에서 에너지 축을 적분한 표기이다.

$$
I(\mathbf r;E_1,E_2)=\int_{E_1}^{E_2}D(\mathbf r,E)\,dE.
$$

$I$는 에너지 축을 적분한 공간 분포이다. 원자 궤도 투영 표의 `LDOS(E)`와 달리 이 결과에는 실제 공간 격자가 있다. 파동함수와 $k$점 표본을 합산하므로 앞의 조밀한 NSCF 자료를 사용하고, 관심 에너지 구간이 `nbnd`로 확보한 범위 안에 있는지 확인한다.[10,11,14,33]

먼저 `si.rho.in`을 `si.ildos.in`으로 복사한다. `plot_num=10`으로 바꾸고 중간 파일과 최종 파일을 각각 `si.ildos.filplot`, `si.ildos.cube`로 고친다. `&INPUTPP`에는 DOS에서 선택한 에너지 구간을 `emin`, `emax`로 추가한다.[11,34] 예를 들어 **원자료의 에너지 기준에서** 0–2 eV 구간을 시험하려면 다음 조각을 사용한다. 이 구간은 특정 Si 밴드의 위치를 예측한 값이 아니다.

```fortran
  plot_num = 10
  emin     = 0.0
  emax     = 2.0
```

```bash
pp.x -in si.ildos.in > si.ildos.out
```

`si.ildos.cube`를 전하 밀도와 같은 셀·단면에서 비교하면 선택한 에너지 구간의 상태가 어디에 기여하는지 살펴볼 수 있다. 이 비교에서는 위에서 정의한 에너지 구간을 함께 표시한다.[11,31] 위 적분 정의에 따르면 구간 밖 기여가 빠지므로 전체 전하 밀도와 같은 적분값을 전제할 수 없다.

한 에너지의 공간 LDOS가 필요하면 `si.ldos.in`에 다음 **완전한 추출 전용 입력**을 사용한다. 예시 에너지 1 eV는 실제 DOS를 읽은 뒤 관심 값으로 바꾼다. `emin=emax`를 명시해 한 에너지를 선택하고, `degauss_ldos`의 단위는 여기서 **eV**임에 주의한다.[11,33]

```fortran
&INPUTPP
  prefix         = 'si_final'
  outdir         = './tmp'
  filplot        = 'si.ldos.filplot'
  plot_num       = 3
  emin           = 1.0
  emax           = 1.0
  degauss_ldos    = 0.1
  use_gauss_ldos = .true.
/
```

```bash
pp.x -in si.ldos.in > si.ldos.out
```

LDOS는 에너지별 중간 파일을 만들 수 있다. `si.ldos.out`의 `Writing data to file` 줄에서 실제 이름을 읽는다. 그 이름을 `si.rho.in`의 `filepp(1)` 자리에 넣고, 첫 블록을 빈 `&INPUTPP`로 바꾸며 `fileout='si.ldos.cube'`로 정한 `si.ldos.export.in`을 만든다. 이 입력은 추출된 한 에너지의 자료만 변환한다.[11,31,33]

```fortran
&INPUTPP
/
```

위 블록만으로 내보내기가 끝나는 것은 아니다. 그 뒤에는 방금 설명한 `&PLOT` 전체가 있어야 한다. `pp.x -in si.ldos.export.in > si.ldos.export.out`으로 변환하고, 선택한 에너지·폭과 중간 파일이 일치하는지 확인한다. 여러 에너지를 요청했다면 각 파일을 구분해 변환해야 한다.[11,31,33]

### (4) 공간 격자와 출력 차원

`pw.x`는 Fast Fourier transform (FFT)을 사용해 평면파 표현과 실공간 격자 사이를 오간다. `ecutrho`와 연관된 계산 격자의 크기는 SCF 출력에서 확인할 수 있다. `pp.x`가 내보내는 공간 표본을 더 촘촘하게 보이게 만드는 것과 원래 전자구조 계산의 cutoff를 수렴시키는 것은 다르다.[4,5,11,31]

| 원하는 자료 | `pp.x` 선택 | 출력에서 확인할 축 |
| --- | --- | --- |
| 선을 따른 변화 | `iflag=1` | 시작점, 선 방향·길이, 위치별 값 |
| 한 단면 | `iflag=2` | 평면을 정하는 두 방향, 격자 수와 값 |
| 입체 분포 | `iflag=3` | 셀, 원점, 세 격자 방향·격자 수, 값 |

본문 예제는 `iflag=3`, `output_format=6`으로 셀 전체의 Cube를 내보낸다. XCrySDen Structure File (XSF)이 필요하면 지원 조합을 확인하고 `output_format=5`를 사용한다. 선이나 임의 평면으로 바꾸려면 `iflag`만 고치는 데서 그치지 말고 해당 형식에 필요한 원점·방향 벡터와 표본 수를 함께 정의한다.[11,31]

격자 파일을 배열로 읽을 때에는 원점, 축 벡터, 축마다의 점 수와 저장 순서를 유지한다. 비직교 셀의 배열 인덱스 세 개를 그대로 Cartesian 좌표 세 개로 읽으면 단면 방향과 거리 해석이 달라진다. 전하 밀도·퍼텐셜·LDOS는 같은 모양의 배열이어도 단위가 다르며, 공간 LDOS는 부피와 에너지당 상태 수인 반면 ILDOS는 에너지 적분 후의 양이다.[5,11,31]

## 8. 마지막 단계의 밴드 경로 계산

### (1) 최종 밀도와 역공간 경로

밴드 분산은 에너지 적분용 균일 격자 대신 선택한 경로에서 고유값을 구한다. DOS·PDOS·공간 분석을 끝냈으면 `si.final.scf.in`으로 SCF를 다시 수행해 시작 밀도를 준비한다. 그 입력을 `si.bands.in`으로 복사해 `calculation='bands'`, `nbnd=12`로 설정한다. 최종 구조와 `prefix/outdir`는 그대로 유지한다.[5,9,12,13]

`K_POINTS`는 아래 경로로 교체한다. 이 실습은 입력 원리를 보여 주기 위해 $\Gamma$에서 역격자 분율 좌표 $(0.5,0,0.5)$까지의 한 구간만 택한다. 완전한 표준 고대칭 경로를 제시한 것은 아니다. 세 좌표는 3절에서 정의한 셀의 역격자 벡터에 대한 계수이며, 다른 셀의 경로를 가져오면 좌표 변환이 필요하다.[5,9,13]

```fortran
K_POINTS (crystal_b)
2
0.0 0.0 0.0  40
0.5 0.0 0.5   1
```

`crystal_b`의 첫 정수는 제공할 끝점 수이고, 각 행 마지막 수는 다음 끝점까지 생성할 경로 표본을 지정한다. 위 블록은 `si.bands.in`의 일부이며 나머지 namelist와 구조 card를 생략하면 안 된다. 이 경로를 SCF의 적분 격자로 대신 사용하지 않는다.[5,13]

```bash
pw.x -in si.final.scf.in > si.bands-scf.out
pw.x -in si.bands.in > si.bands.out
```

이 시점의 저장 고유값과 파동함수는 경로 계산 결과이다. 다시 DOS나 공간 LDOS를 계산하려면 6절의 조밀한 NSCF를 먼저 수행한다. 파일 이름이 여전히 `si_final`이라고 해서 이전 균일 격자의 자료가 그대로 남아 있다고 가정하지 않는다.[7,15,12,13]

### (2) `bands.x` 결과 읽기

다음은 `bands.x`용 **완전한 입력** `si.bands-post.in`이다. 밴드 고유값을 새로 계산하는 단계가 아니라 `pw.x`의 경로 결과를 정리하는 단계이다.[9,13]

```fortran
&BANDS
  prefix  = 'si_final'
  outdir  = './tmp'
  filband = 'si.bands.dat'
/
```

```bash
bands.x -in si.bands-post.in > si.bands-post.out
```

`si.bands.dat.gnu`는 경로 좌표와 에너지(eV)를 그리기 위한 자료이다. 이를 에너지별 상태 수 표인 DOS와 구분한다. 첫 축은 선택한 경로를 따라 이동하는 좌표이고, 밴드마다 곡선이 생긴다. 출력에서 끝점 위치와 밴드 수를 확인한 뒤 같은 에너지 기준을 적용해 DOS와 함께 해석한다.[9,13]

이 한 구간만으로 전체 Brillouin zone의 밴드 극값을 모두 찾았다고 결론 내리지는 않는다. 연구용 밴드 그림은 실제 결정과 셀 규약에 맞는 경로를 정하고, 관심 비점유 범위와 경로 표본 수도 별도로 확보해야 한다.[5,35,13]

## 9. 요약

- 하나의 Si 입력을 출발점으로 삼고 UPF·cutoff·$k$점 조건을 먼저 확정한다. SCF 수렴과 수치 조건의 수렴은 별도 확인 사항이다.
- 구조를 최적화한 뒤 마지막 셀과 원자 좌표로 고정 구조 SCF를 다시 수행한다. 이후 모든 분석은 그 최종 구조를 사용한다.
- 조밀한 NSCF 자료로 DOS와 PDOS를 만들고, 같은 자료가 필요한 공간 분석까지 마친 뒤 밴드 경로 계산으로 넘어간다.
- 에너지 표, 경로 표, 공간 격자는 서로 다른 자료이다. 파일명뿐 아니라 독립 축·단위·에너지 기준을 함께 읽는다.
- 재현에 필요한 묶음은 입력, UPF 식별 정보, 프로그램 버전, 표준 출력과 후처리에 필요한 저장 자료이다.

## 10. 참고문헌

1. Quantum ESPRESSO Foundation, “Documentation,” *Quantum ESPRESSO* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/documentation/).
2. P. Giannozzi et al., “QUANTUM ESPRESSO: a modular and open-source software project for quantum simulations of materials,” *Journal of Physics: Condensed Matter* **21**, 395502 (2009). [DOI](https://doi.org/10.1088/0953-8984/21/39/395502).
3. University of Illinois Urbana-Champaign, “Module 2: Quantum Espresso Walkthrough,” *MSE 404 Electronic Materials* (2026). [강의 자료](https://courses.grainger.illinois.edu/MSE404ELA/sp2026/6.DFT-walkthrough.pdf).
4. P. Giannozzi et al., “Advanced capabilities for materials modelling with Quantum ESPRESSO,” *Journal of Physics: Condensed Matter* **29**, 465901 (2017). [DOI](https://doi.org/10.1088/1361-648X/aa8f79).
5. Quantum ESPRESSO Foundation, “pw.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_PW.html).
6. C. W. Lee, “Structural optimization,” *Quantum ESPRESSO: Theory + Hands-On* (2026년 9월 확인). [교육 자료](https://chaewoon11.github.io/qe-tutorial/chapters/relaxation), [원본 계산 예제](https://github.com/chaewoon11/qe-tutorial/tree/master/code/04-relaxation).
7. Quantum ESPRESSO Foundation, “PWscf User’s Guide: Data files,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/pw_user_guide/node9.html).
8. Quantum ESPRESSO Foundation, “dos.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_DOS.html).
9. Quantum ESPRESSO Foundation, “bands.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_BANDS.html).
10. Quantum ESPRESSO Foundation, “projwfc.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_PROJWFC.html).
11. Quantum ESPRESSO Foundation, “pp.x: Input File Description, version 7.5,” *Quantum ESPRESSO Documentation* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/INPUT_PP.html).
12. P. Das, “Density of States calculation,” *Quantum Espresso Tutorial* (2026년 9월 확인). [교육 자료](https://pranabdas.github.io/espresso/hands-on/dos/).
13. P. Das, “Band structure calculation,” *Quantum Espresso Tutorial* (2026년 9월 확인). [교육 자료](https://coteo-cbpf.github.io/Quantum-Espresso-tutorial/hands-on/bands/).
14. P. Das, “Projected density of states,” *Quantum Espresso Tutorial* (2026년 9월 확인). [교육 자료](https://pranabdas.github.io/espresso/hands-on/pdos/).
15. PAOFLOW Developers, “PAOFLOW.inputs.read_QE_xml,” *PAOFLOW Documentation* (2026년 9월 확인). [Parser 문서](https://paoflow.org/en/latest/_modules/PAOFLOW/inputs/read_QE_xml.html).
16. Quantum ESPRESSO Foundation, “Unified Pseudopotential Format,” *Quantum ESPRESSO Pseudopotentials* (2026년 9월 확인). [형식 명세](https://pseudopotentials.quantum-espresso.org/home/unified-pseudopotential-format).
17. Quantum ESPRESSO Foundation, “Pseudopotentials,” *Quantum ESPRESSO* (2026년 9월 확인). [공식 안내](https://www.quantum-espresso.org/pseudopotentials/).
18. G. Prandini et al., “Precision and efficiency in solid-state pseudopotential calculations,” *npj Computational Materials* **4**, 72 (2018). [DOI](https://doi.org/10.1038/s41524-018-0127-2).
19. M. J. van Setten et al., “The PseudoDojo: Training and grading a 85 element optimized norm-conserving pseudopotential table,” *Computer Physics Communications* **226**, 39–54 (2018). [DOI](https://doi.org/10.1016/j.cpc.2018.01.012).
20. A. Dal Corso, “Pseudopotentials periodic table: From H to Pu,” *Computational Materials Science* **95**, 337–350 (2014). [DOI](https://doi.org/10.1016/j.commatsci.2014.07.043).
21. H. J. Monkhorst and J. D. Pack, “Special points for Brillouin-zone integrations,” *Physical Review B* **13**, 5188–5192 (1976). [DOI](https://doi.org/10.1103/PhysRevB.13.5188).
22. C. W. Lee, “Brillouin-zone sampling & smearing,” *Quantum ESPRESSO: Theory + Hands-On* (2026년 9월 확인). [교육 자료](https://chaewoon11.github.io/qe-tutorial/chapters/brillouin-zone).
23. Quantum ESPRESSO Foundation, “PWscf reference output: total energy, forces, and stress,” *Quantum ESPRESSO source repository* (2026년 9월 확인). [공식 예제 출력](https://github.com/QEF/q-e_old/blob/master/PHonon/examples/GRID_recover_example/reference/alas.scf.out).
24. Quantum ESPRESSO Foundation, “2 Compilation,” *PWscf User’s Guide* (2026년 9월 확인). [공식 문서](https://www.quantum-espresso.org/Doc/pw_user_guide/node6.html).
25. S. de Gironcoli, “First steps with a periodic DFT code: Quantum ESPRESSO,” SISSA tutorial (2011). [강의 자료](https://www.people.sissa.it/~degironc/2011/tutorial_surface.pdf).
26. ASE Developers, “ase.eos,” *Atomic Simulation Environment Documentation* (2026년 9월 확인). [공식 source documentation](https://docs.ase-lib.org/_modules/ase/eos.html).
27. Quantum ESPRESSO Foundation, “`ev.x` source: E(V) data fitting,” *Quantum ESPRESSO 7.5 source repository*, tag `qe-7.5` (2026년 9월 확인). [공식 source](https://gitlab.com/QEF/q-e/-/blob/qe-7.5/PW/tools/ev.f90).
28. Computational Materials Physics, “geometry optimization : E(V) and EOS,” educational project (2022), p. 2. [실습 자료](https://www.compmatphys.org/wp-content/uploads/2022/10/project_05b_EV-and-EOS.pdf).
29. SCM, “Quantum ESPRESSO Properties,” *AMS 2026.1 Documentation* (2026년 9월 확인). [Interface documentation](https://www.scm.com/doc/QuantumEspresso/properties.html).
30. C. W. Lee, “Density of states & PDOS,” *Quantum ESPRESSO: Theory + Hands-On* (2026년 9월 확인). [교육 자료](https://chaewoon11.github.io/qe-tutorial/chapters/dos).
31. C. W. Lee, “Charge density & visualization,” *Quantum ESPRESSO: Theory + Hands-On* (2026년 9월 확인). [교육 자료](https://chaewoon11.github.io/qe-tutorial/chapters/charge), [원본 입력·격자 출력](https://github.com/chaewoon11/qe-tutorial/tree/master/code/07-charge).
32. Computational Materials Physics, “Work function,” educational tutorial (2022). [강의 자료](https://compmatphys.org/wp-content/uploads/2022/09/work-function.pdf).
33. C. Wolf, “misbehaving pp.x for plot_num 3,” *Quantum ESPRESSO users mailing list* (2020). [실행 사례](https://lists.quantum-espresso.org/pipermail/users/2020-April/044268.html).
34. G. Fratesi, “Re: question regarding ILDOS plots in PP.x,” *Quantum ESPRESSO users mailing list* (2015). [답변](https://lists.quantum-espresso.org/pipermail/users/2015-May/032171.html).
35. AiiDA Developers, “Workflows: band structure with Quantum ESPRESSO,” *AiiDA Tutorials* (2026년 9월 확인). [공식 교육 문서](https://aiida-tutorials.readthedocs.io/en/main/sections/running_processes/workflows.html).
