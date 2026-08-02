---
title: "(5) Memory Device: Basics"
description: 시스템 메모리 계층과 셀 어레이, word line·bit line, 주변회로, sense amplifier와 칩 구조를 연결해 설명하는 공통 기초
status: verified
last_verified: 2026-08-01
---

# (5) Memory Device: Basics

Memory device는 정보를 구별 가능한 물리 상태로 저장하고, 주소와 제어 신호에 따라 그 상태를 쓰거나 읽는 소자 또는 집적회로이다. 실제 시스템에서 “메모리”라는 말은 cache, main memory, storage처럼 서로 다른 역할을 맡는 **시스템 계층**과 셀 어레이·주변회로·입출력 회로를 포함하는 **칩 내부 구조**를 함께 가리킨다.[1,2]

이 글은 이후 static random-access memory (SRAM), dynamic random-access memory (DRAM), NAND Flash와 그 밖의 메모리 기술을 각각 다루기 위한 공통 기반이다. 개별 셀 회로, 저장 상태, 판독·쓰기 물리, refresh와 program–erase 동작은 다루지 않는다. 대신 **시스템에서 맡는 역할**과 **칩 내부의 공간적 조직**을 분리한 뒤, 두 관점이 주소와 데이터 경로에서 어떻게 이어지는지 설명한다.

## 1. 메모리 계층과 역할

### (1) 먼저 구분할 두 가지 계층

메모리 문헌에서 같은 “계층”이라는 말이 서로 다른 두 관계에 쓰이므로 먼저 구분해야 한다.[1–4]

| 구분 | 답하려는 질문 | 대표 순서 |
| --- | --- | --- |
| 시스템 메모리 계층 | 프로세서의 요청을 어느 수준에서 처리하는가? | register → cache → main memory → storage |
| 칩 내부 조직 | 한 메모리 칩 안에서 셀과 회로가 어떻게 묶이는가? | cell → row·column → subarray → bank → chip |

첫 번째는 서로 다른 저장 수준 사이에서 자료를 복사하고 이동하는 관계이다. 두 번째는 하나의 집적회로를 구성하는 물리적 포함 관계이다. 따라서 cell이 cache의 “윗단”이나 “아랫단”에 있는 것이 아니다. Cache를 구현한 칩 또는 macro 안에도 cell–array–bank에 해당하는 내부 조직이 존재할 수 있다.[1–4]

<figure markdown="span">
  ![Register, CPU cache, main memory, storage가 차례로 연결된 시스템 메모리 계층](images/computer-memory-hierarchy.svg)
  <figcaption markdown="1">
    그림 1. 시스템 역할로 구분한 메모리 계층. Register와 CPU cache, main memory, storage 사이에서 자료가 이동하며, 오른쪽으로 갈수록 일반적으로 용량과 보존성이 커지고 접근 지연이 길어진다. 이는 정성적 경향이며 제품별 수치를 뜻하지 않는다.
    출처: Gernot Heiser, “Caches,” *COMP9242 2025 T3 W03 Part 1: HW Considerations*, slide 5, UNSW Sydney, CC BY 4.0. 원본에서 해당 계층 흐름을 발췌하고, 이 글의 네 가지 시스템 역할에 맞추어 `“Disk” Cache`를 생략한 뒤 storage 위치를 조정함.[13]
  </figcaption>
</figure>

그림 1은 “어디에 더 빨리 접근하는가”를 보여주는 시스템 관점이다. 프로세서가 필요한 자료를 위쪽 수준에서 찾으면 접근이 끝나고, 없으면 아래쪽 수준에서 더 큰 단위의 자료를 가져와 위쪽에 복사한다. 아래로 갈수록 무조건 한 종류의 기술만 사용해야 한다는 규칙은 아니며, 구체적인 구현은 시스템에 따라 달라진다.[1,2]

### (2) 각 수준의 역할

| 시스템 수준 | 주된 역할 | 흔한 구현 기술 | 인접 수준과 주로 이동하는 단위 |
| --- | --- | --- | --- |
| register | 현재 명령이 직접 사용하는 피연산자와 상태 보관 | flip-flop, register file | word |
| L1/L2/L3 cache | 가까운 하위 수준의 일부 자료를 복제하여 평균 접근 지연 감소 | 주로 SRAM | cache line |
| main memory | 실행 중인 프로그램과 작업 자료의 큰 주소 공간 제공 | 주로 DRAM | cache line, burst |
| secondary storage | 프로그램과 자료를 전원 제거 뒤에도 보존 | NAND Flash 기반 SSD, HDD | page·block, sector |
| archival storage | 장기 보관과 백업 | magnetic tape, optical media, 원격 저장소 | 큰 block, object |

`cache`, `main memory`, `storage`는 **시스템 역할**이고 SRAM, DRAM, NAND Flash는 **구현 기술**이다. 특정 기술과 역할을 같은 말로 취급하면 안 된다. 예를 들어 SRAM은 cache 외에도 scratchpad와 buffer를 구현할 수 있으므로 “SRAM은 cache이다”보다 “cache는 흔히 SRAM으로 구현된다”가 정확하다.[1,2]

!!! warning "[Interpretation Caveat]"
    `primary memory` 또는 “주기억 장치”는 문헌에 따라 main memory만 뜻하기도 하고, 프로세서가 직접 다루는 register·cache·main memory를 넓게 묶기도 한다. 이 글에서는 모호성을 피하기 위해 **main memory**를 실행 중인 자료를 담는 계층, **storage**를 전원이 꺼져도 자료를 보존하는 계층으로 구분한다.[1,2]

### (3) 계층이 필요한 이유와 지역성

이상적인 메모리는 빠르고, 용량이 크고, 집적 밀도가 높고, 전원이 없어도 정보를 유지하며, 비트당 비용과 접근 에너지가 작아야 한다. 현실의 한 가지 기술이 이 조건을 모두 만족하지 못하므로, 컴퓨터는 작고 빠른 수준을 프로세서 가까이에 두고 크고 느린 수준을 그 아래에 배치한다.[1,2]

Cache는 main memory의 모든 내용을 담는 별도 주소 공간이 아니라, 가까운 시점에 다시 사용할 가능성이 높은 일부 block을 복제한다. 같은 자료를 곧 다시 쓰는 temporal locality와 인접 주소를 함께 쓰는 spatial locality가 높으면 위쪽 수준에서 요청이 적중할 가능성이 커지고 평균 접근 시간이 줄어든다.[1,2]

두 계층의 단순한 평균 접근 시간은

$$
t_\mathrm{avg}
=
t_\mathrm{cache}
+
\left(1-h\right)t_\mathrm{miss}
$$

로 쓸 수 있다. $h$는 cache hit rate, $t_\mathrm{cache}$는 cache를 확인하는 시간, $t_\mathrm{miss}$는 miss 뒤 하위 수준에서 block을 가져오는 추가 시간이다. 실제 다단계 계층에서는 각 수준의 적중률, 대기 행렬, 병렬성, 주소 변환과 데이터 이동 시간을 함께 고려한다.[1,2]

## 2. Bit, cell, word와 주소

### (1) 저장 단위와 외부 조직

**Bit**는 두 논리값 가운데 하나를 나타내는 정보 단위이고, **memory cell**은 하나 이상의 bit를 물리 상태로 저장하는 최소 반복 구조이다. **Word**는 한 주소 또는 한 번의 논리적 접근으로 함께 취급하는 bit 묶음이다. 셀당 저장 bit 수, 내부에서 동시에 활성화되는 행 너비, 외부 입출력 word 너비는 서로 다를 수 있다.[3,4,6]

메모리의 외부 조직을 $D\times W$로 쓰면 $D$는 주소 가능한 word의 개수인 depth, $W$는 word당 bit 수인 width이다. 이때 논리 용량은

$$
C_\mathrm{logical}=D\,W
$$

이다. 주소 bit 수가 $A$이고 모든 조합을 사용하면 $D=2^A$이므로 $C_\mathrm{logical}=2^A W$이다. 오류 정정 부호, spare row·column, tag와 내부 관리 정보는 사용자에게 보이는 논리 용량보다 큰 물리 용량을 요구할 수 있다.[1,6,11,12]

### (2) 내부 어레이 용량

한 셀이 $b_\mathrm{cell}$ bit를 저장하고, 어레이가 $N_\mathrm{row}$개 행과 $N_\mathrm{col}$개 열로 이루어지면 원시 저장 용량은

$$
C_\mathrm{array}
=
N_\mathrm{row}N_\mathrm{col}b_\mathrm{cell}
$$

이다. 실제 칩은 여러 subarray와 bank를 가지므로

$$
C_\mathrm{chip,raw}
=
N_\mathrm{bank}
N_\mathrm{subarray/bank}
N_\mathrm{row}
N_\mathrm{col}
b_\mathrm{cell}
$$

처럼 계층별 반복 수를 곱해 생각할 수 있다. 이 식은 논리 구조를 세는 식이며, spare 영역·주변회로 면적·배선 면적을 포함한 die 면적 식은 아니다.[3,4,6]

### (3) 행 주소와 열 주소

큰 어레이에서는 주소를 bank, row와 column 선택 정보로 나눈다. Row decoder는 이진 행 주소를 받아 보통 한 개의 word line을 활성화하고, column decoder 또는 column multiplexer는 활성화된 행에서 외부로 보낼 일부 열을 선택한다. 따라서 “행 하나를 내부에서 감지하는 너비”는 “칩의 DQ pin으로 한 번에 전달하는 너비”보다 훨씬 클 수 있다.[1,3,4,6]

## 3. Cell array, word line과 bit line

### (1) 이차원 어레이의 공통 구조

반도체 메모리는 동일한 셀을 행과 열로 반복 배치하여 저장 밀도를 높인다. 같은 행의 셀은 선택 신호를 공유하고, 같은 열의 셀은 판독·쓰기 경로를 공유한다. 셀을 단순하게 반복하는 대신 decoder, sense amplifier와 write driver 같은 비교적 복잡한 회로를 여러 셀이 나누어 사용하므로 전체 bit당 면적을 줄일 수 있다.[3–5]

<figure markdown="span">
  ![행과 열로 배열된 메모리 셀, row decoder, sense amplifier와 column decoder의 대표 배치](images/memory-cell-array.svg)
  <figcaption markdown="1">
    그림 2. 대표적인 이차원 메모리 셀 어레이의 조직. 파란 격자는 셀 어레이, 왼쪽의 초록 블록은 row decoder, 빨간 블록은 열마다 연결된 sense amplifier, 아래쪽 초록 블록은 column decoder를 나타낸다. 주소가 행과 열 선택으로 나뉘고, 선택 회로와 판독 회로를 여러 셀이 공유한다는 관계를 보여주는 개념도이다. 특정 DRAM 제품의 실제 배치도나 셀 동작 순서를 뜻하지 않는다.
    출처: HandigeHarry, “DRAM,” Wikimedia Commons, public domain; 일반 구조를 설명하는 영문 레이블을 추가하여 수정.[14]
  </figcaption>
</figure>

어레이는 다음 세 부분의 결합으로 이해하면 된다.

| 부분 | 질문 | 대표 회로 |
| --- | --- | --- |
| 저장 | 어느 반복 소자가 정보를 보존하는가? | memory cell |
| 선택 | 많은 셀 중 어느 행·열을 연결하는가? | row decoder, word-line driver, column mux, selector |
| 판독·쓰기 | 셀 신호를 어떻게 논리값으로 바꾸고 입력을 전달하는가? | precharge, sense amplifier, write driver |

### (2) Word line

**Word line (WL)**은 같은 행의 셀에 분배되는 선택선이다. 행이 길어질수록 하나의 WL에 연결되는 셀 수와 배선의 저항·정전용량이 커지므로, 큰 메모리는 predecoder, local decoder와 단계적 word-line driver를 사용하고 어레이를 여러 subarray로 나눈다.[3–5]

`word line`의 `word`가 곧 외부 데이터 word 전체를 뜻하지는 않는다. WL 하나를 켜면 물리적으로 긴 한 행이 동시에 bit line에 연결될 수 있지만, 그중 일부 열만 column mux를 거쳐 외부 word 또는 burst로 전달된다.[3,4,6]

### (3) Bit line

**Bit line (BL)**은 같은 열의 여러 셀이 공유하는 판독·쓰기선이다. 많은 셀이 하나의 BL과 판독 회로를 공유하면 셀마다 주변회로를 두는 경우보다 면적을 줄일 수 있지만, BL의 기생 정전용량과 저항이 증가하여 신호 전달과 판독이 어려워진다.[3–5]

`bit line`은 공통 구조를 가리키는 이름이다. 실제로 전달하는 물리량, 기준 신호의 구성과 필요한 선의 수는 메모리 기술마다 다르며 각 기술 문서에서 별도로 다룬다.

### (4) 왜 subarray와 bank로 나누는가

하나의 거대한 어레이는 WL과 BL이 길어져 RC 지연, 동적 에너지와 판독 부담이 커진다. 이를 줄이기 위해 가까운 셀과 local peripheral circuit를 **subarray** 또는 **mat**으로 묶고, 여러 subarray를 **bank**로 조직한다. 짧은 배선은 빠른 감지에 유리하지만 decoder와 sense amplifier를 더 많이 복제해야 하므로, 메모리 설계는 셀 밀도와 접근 시간·에너지 사이에서 분할 크기를 정한다.[2–4]

## 4. 주변회로와 sense amplifier

**Peripheral circuit**는 반복 셀 자체가 아니라 셀을 선택하고, 읽고, 쓰고, 초기화하고, 외부 신호와 연결하는 회로의 총칭이다. 실제 배치에서는 칩 가장자리에만 있는 것이 아니라 subarray 사이에 반복되기도 하므로, `peripheral`은 기능적 구분이지 반드시 die의 바깥 테두리를 뜻하지 않는다.[3,4,6]

### (1) 주소 해독과 선택 회로

| 회로 | 입력 | 기능 |
| --- | --- | --- |
| address buffer·latch | 외부 주소 | 주소를 내부 timing에 맞춰 보존하고 분배 |
| bank decoder | bank 주소 | 접근할 bank 선택 |
| row predecoder·decoder | 행 주소 | 많은 WL 가운데 대상 행 선택 |
| word-line driver | decoder 출력 | 긴 WL을 필요한 전압과 속도로 구동 |
| column decoder·mux | 열 주소 | 감지된 행 가운데 외부로 전달할 열 선택 |

Row decoder는 주소를 one-hot 선택으로 바꾸고, word-line driver는 큰 WL 부하를 실제로 충·방전한다. Column decoder는 보통 셀 한 개를 직접 켜기보다 이미 감지된 여러 열 가운데 일부를 global data line에 연결한다. 두 기능을 모두 단순히 “주소 decoder”라고 부르면 행 전체 활성화와 외부 word 선택을 구분하기 어렵다.[3,4,6]

### (2) Precharge, equalization과 write driver

**Precharge circuit**는 접근 전에 BL을 정해진 초기 상태로 만들고, **equalization circuit**는 한 쌍의 선을 사용하는 구조에서 초기 차이를 줄인다. **Write driver**는 입력 데이터를 선택된 열의 전기적 신호로 변환한다. 필요한 초기값, 전압·전류 크기와 timing은 셀 기술에 따라 달라진다.[3–5]

### (3) Sense amplifier의 세 역할

**Sense amplifier (SA)**는 BL에 나타난 작은 아날로그 신호를 신뢰할 수 있는 논리값으로 변환하는 판독 회로이다. 핵심 역할은 다음과 같이 나눌 수 있다.[3–5]

1. **판별:** 셀 신호와 보수선 또는 기준 신호의 차이를 감지한다.
2. **증폭과 래치:** 작은 차이를 뒤쪽 디지털 회로가 처리할 수 있는 수준으로 바꾸고 보존한다.
3. **구동:** 판독값을 local data line 또는 더 긴 전역 데이터선으로 전달한다.

큰 어레이에서는 셀 BL에 직접 붙은 local SA와 더 긴 global data line을 구동하는 global 또는 secondary SA가 구분될 수 있다. 문헌과 제조사마다 `primary`, `secondary`, `local`, `global` 명칭은 다르므로, 이름보다 **어느 배선에 연결되고 어느 범위의 셀이 공유하는지**를 확인해야 한다.[1,3,4,6]

!!! warning "[Interpretation Caveat]"
    Sense amplifier의 입력 물리량, 기준 신호, 허용 offset과 noise margin은 셀 기술에 따라 달라진다. 이 페이지의 공통 블록도를 특정 기술의 실제 감지 회로로 해석하지 않는다.[3–5]

### (4) 제어, 입출력, 전원과 신뢰성 회로

메모리 칩에는 셀 어레이와 SA 외에도 다음 기능 블록이 필요하다.[4,6,11,12]

| 기능군 | 대표 블록 | 하는 일 |
| --- | --- | --- |
| 명령·timing | command decoder, control logic, mode register, clock circuit | 외부 명령을 내부 선택·판독·쓰기 timing으로 변환 |
| 입력 경로 | DQ receiver, input register, write FIFO, write driver | 외부 데이터를 내부 쓰기 경로로 전달 |
| 출력 경로 | read latch, output driver, serializer, data strobe 회로 | 내부 판독값을 외부 DQ timing에 맞춰 전달 |
| 유지 관리 | technology-specific controller | 기술별 유지·검사 동작 관리 |
| 전원 | regulator, charge pump, level shifter | 셀과 선택선에 필요한 내부 전압 생성 |
| 수율·신뢰성 | spare row·column, fuse·remap, error-correcting code (ECC) | 결함 위치 대체와 오류 검출·정정 |

제품에 따라 각 블록의 존재와 위치는 다르다. On-die ECC와 redundancy가 있으면 외부에 보이는 주소와 실제 물리 셀이 일대일로 대응하지 않을 수 있다.[11,12]

## 5. 공통 읽기와 쓰기의 신호 경로

### (1) 공통 읽기 경로

다음 순서는 개별 셀의 판독 원리가 아니라, 주소를 선택한 뒤 데이터를 칩 밖으로 내보내기까지 각 기능 블록이 동작하는 순서를 나타낸다.[3–6]

1. 외부 또는 상위 제어기가 주소와 read 명령을 보낸다.
2. 입력 회로가 주소·명령을 latch하고 bank와 row·column 정보를 나눈다.
3. Row decoder와 WL driver가 대상 행을 선택한다.
4. 선택된 셀이 BL의 전압 또는 전류를 바꾼다.
5. Local SA가 작은 신호를 판별하고 논리값으로 래치한다.
6. Column mux가 필요한 열만 global data line에 연결한다.
7. Global SA, read latch와 output driver가 데이터를 DQ pin 또는 on-chip bus로 보낸다.

이 경로에서 셀 하나의 고유 전환 시간만 측정하면 칩의 read latency를 얻을 수 없다. 주소 해독, WL·BL RC, 감지, 열 선택, 전역 배선과 입출력 timing이 모두 전체 지연에 포함된다.[3,4]

### (2) 공통 쓰기 경로

쓰기에서는 입력 데이터가 읽기와 반대 방향으로 이동한다.[3,4]

1. 주소, write 명령과 입력 데이터를 latch한다.
2. Bank와 row를 선택하고 필요한 열만 column mux로 연결한다.
3. Write driver가 선택된 데이터선에 입력 신호를 전달한다.
4. 선택된 셀이 입력에 대응하는 상태로 바뀐다.
5. 쓰기 종료 뒤 선택선을 해제하고 데이터선을 다음 접근 상태로 돌린다.

셀 상태를 실제로 바꾸는 물리 과정, 쓰기 단위와 완료 판정은 기술마다 다르므로 이 글의 범위에 포함하지 않는다.

## 6. 메모리 칩에서 시스템까지

### (1) Cell에서 chip까지

메모리 칩 내부의 대표 계층은 다음과 같다.[1,4,6]

| 계층 | 구성 | 공유하거나 담당하는 자원 |
| --- | --- | --- |
| cell | 한 개의 저장 소자와 필요한 접근 소자 | 한 개 이상의 물리 상태 |
| row·column | WL 또는 BL을 공유하는 셀 집합 | 행 선택선 또는 열 데이터선 |
| subarray·mat | 작은 이차원 셀 어레이 | local row decoder, precharge, local SA |
| bank | 여러 subarray와 bank I/O | local data path와 bank-level control |
| chip·die | 여러 bank와 공통 주변회로 | 명령·주소·DQ interface, 전원과 timing |
| package | 하나 이상의 die와 외부 단자 | 전기적·기계적 연결 |

`subarray`, `mat`, `bank`의 정확한 경계와 명칭은 기술과 제조사에 따라 달라진다. 공통 원리는 긴 WL·BL과 큰 부하를 제한하기 위해 어레이를 분할하고, local circuit에서 감지한 데이터를 더 좁은 global path로 모은다는 점이다.[3,4,6]

### (2) Chip에서 memory controller까지

외장 DRAM 시스템에서는 chip 위의 계층이 더 이어진다.[1,4]

| 계층 | 정의 | 병렬성과 공유 관계 |
| --- | --- | --- |
| rank | 같은 명령을 받아 lockstep으로 동작하는 chip 묶음 | 여러 chip이 함께 한 데이터 word 제공 |
| module | chip과 배선을 실장한 기판 | 하나 이상의 rank 포함 가능 |
| channel | controller와 module이 사용하는 명령·주소·데이터 연결 | 서로 다른 channel은 독립 전송 가능 |
| memory controller | 상위 요청을 메모리 interface 명령과 timing으로 변환 | 주소 매핑, 대기 행렬과 scheduling |

Rank는 물리적 module과 같은 말이 아니다. 한 module에 여러 rank가 있을 수 있고, 한 channel에는 여러 module 또는 package가 연결될 수 있다. 반대로 고대역폭 적층 메모리처럼 packaging과 channel 구성이 다른 제품에서는 DIMM 중심 설명을 그대로 적용할 수 없다.[1,4]

### (3) 외부 주소와 물리 위치

프로세서의 물리 주소가 곧 칩 내부 row·column 번호는 아니다. Memory controller의 주소 매핑은 주소 bit를 channel, rank, bank, row와 column으로 나누고, 칩 내부에서는 다시 subarray 선택과 redundancy remap이 적용될 수 있다. 이 매핑은 병렬성, 접근 지역성, 오류 위치 해석과 보안 특성에 영향을 주지만 제품별 세부 물리 매핑은 공개되지 않을 수 있다.[1,4,6,11,12]

## 7. 성능·신뢰성 정량 지표

메모리 기술을 비교할 때에는 “빠르다” 또는 “고밀도이다”라는 표현만으로는 부족하다. 각 지표의 측정 경계와 단위를 함께 밝혀야 한다. 특히 read와 write의 특성이 서로 다르고 내부 병렬성이 큰 메모리에서는 cell, array, chip과 system 수준의 수치를 섞지 않아야 한다.[1,7–9]

| 정량 지표 | 정의해야 할 내용 | 흔한 해석 오류 |
| --- | --- | --- |
| capacity | 사용자 bit인지 raw physical bit인지 | ECC·spare를 무시 |
| density | bit/cell, bit/mm², cell area 가운데 기준 | 셀 면적과 die 전체 밀도를 동일시 |
| read latency | 요청 시작부터 어느 출력 유효 시점까지인지 | cell sensing과 interface 지연을 혼합 |
| write latency | 요청 수락부터 지정한 쓰기 완료 조건까지의 경계 | read와 같은 단위로 가정 |
| bandwidth | 단위 시간당 유효 데이터량과 동시 요청 수 | 짧은 지연의 역수로 단순 환산 |
| energy per access | 데이터 단위, 주변회로와 I/O 포함 범위 | cell switching energy를 chip energy로 사용 |
| retention time | 온도·전원·허용 오류 조건에서 정보 유지 시간 | 조건 없이 기술 간 직접 비교 |
| endurance | 판정 기준을 넘기기 전 허용되는 쓰기 cycle | 제품 수명과 동일시 |
| error rate | raw bit error인지 ECC 이후 오류인지 | 수정 전후 오류율을 직접 비교 |

!!! info "[Measurement]"
    한 번의 read 구간을 $[t_0,t_1]$, 공급선 집합을 $k$라 하면 배경을 뺀 읽기 에너지는

    $$
    E_\mathrm{read}
    =
    \sum_k
    \int_{t_0}^{t_1}
    V_k(t)\left[I_{k,\mathrm{read}}(t)-I_{k,\mathrm{bg}}(t)\right]dt
    $$

    로 정의할 수 있다. Write도 같은 방식으로 $E_\mathrm{write}$를 구하되, 기술별 내부 보조 동작을 포함하는지 명시한다. 지연은

    $$
    t_\mathrm{read}=t_\mathrm{data\ valid}-t_\mathrm{request\ accepted}
    $$

    처럼 시작·종료 사건을 식으로 선언한다. Cell, array core, chip I/O와 controller 포함 system 가운데 어느 경계를 측정했는지, 데이터 단위, 공급전압, 온도, 접근 무늬와 오류 판정 기준을 함께 보고한다.[1,8,9]

!!! warning "[Interpretation Caveat]"
    Retention은 한 번 쓴 상태가 조건 안에서 얼마나 오래 남는지, endurance는 반복 쓰기를 몇 회 견디는지 나타낸다. 두 지표는 서로 다른 물리량이며, 셀·어레이·칩 가운데 측정 경계와 실패 판정을 먼저 통일해야 비교할 수 있다.[7–9]

## 8. 요약

- 시스템 메모리 계층은 register → cache → main memory → storage의 역할 관계이고, 칩 내부 조직은 cell → subarray → bank → chip의 포함 관계이다.
- Cache·main memory·storage는 시스템 역할이며 SRAM·DRAM·NAND Flash는 이를 구현하는 기술 이름이다.
- 메모리 셀은 물리 상태를 저장하고, WL은 행을 선택하며, BL은 같은 열의 셀이 공유하는 판독·쓰기 경로이다.
- 큰 어레이는 WL·BL 부하를 제한하고 병렬성을 얻기 위해 subarray와 bank로 나뉜다.
- 주변회로에는 주소 decoder, WL driver, precharge·equalization, SA, write driver, control·I/O, 전원과 신뢰성 회로가 포함된다.
- Local SA는 셀에 가까운 데이터선을 판독하고, global 또는 secondary SA는 더 긴 내부 전역 배선과 I/O를 구동한다.
- 메모리를 비교할 때에는 cell·array·chip·system 경계, 데이터 단위, read/write·retention·endurance의 정의와 측정 조건을 함께 밝혀야 한다.

## 9. 참고문헌

1. Y. Kim and O. Mutlu, “Memory Systems,” in *Computing Handbook, Third Edition: Computer Science and Software Engineering*, T. F. Gonzalez, J. Diaz-Herrera, and A. Tucker, eds., Chapter 18, CRC Press (2014). [저자 제공 PDF](https://people.inf.ethz.ch/omutlu/pub/memory-systems-introduction_computing-handbook14.pdf).
2. J.-C. Franchitti, *Introduction to Computer Science*, Section 5.5 “Memory Hierarchy,” OpenStax (2024). [공식 공개 교재](https://openstax.org/books/introduction-computer-science/pages/5-5-memory-hierarchy).
3. D. Harris, “Lecture 11: Memory,” *Introduction to CMOS VLSI Design (E158)*, Harvey Mudd College, based on Stanford EE271 by M. Horowitz. [강의 자료 PDF](https://pages.hmc.edu/harris/class/e158/01/lect11.pdf).
4. K. K. Chang, *Understanding and Improving the Latency of DRAM-Based Memory Systems*, Ph.D. dissertation, Carnegie Mellon University (2017). [대학 저장소 PDF](https://research.ece.cmu.edu/safari/thesis/kchang_dissertation.pdf).
5. NPTEL, “Basics of DRAM Cell and Access Time Consideration” and “SRAM and DRAM Peripherals,” *Semiconductor Memories*, Lectures 28 and 30. [공식 강의 자료](https://archive.nptel.ac.in/content/storage2/courses/117101058/Slides/29.5.htm).
6. Micron Technology, *256Mb: x4, x8, x16 DDR SDRAM*, Rev. S, “Functional Block Diagrams” (2015). [데이터시트 사본 PDF](https://cms.nacsemi.com/content/AuthDatasheets/MICT-S-A0000713834-1.pdf).
7. J. S. Meena, S. M. Sze, U. Chand, and T.-Y. Tseng, “Overview of Emerging Nonvolatile Memory Technologies,” *Nanoscale Research Letters* **9**, 526 (2014). [DOI: 10.1186/1556-276X-9-526](https://doi.org/10.1186/1556-276X-9-526).
8. G. Sun, J. Zhao, M. Poremba, C. Xu, and Y. Xie, “Memory That Never Forgets: Emerging Nonvolatile Memory and the Implication for Architecture Design,” *National Science Review* **5**, 577–592 (2018). [DOI: 10.1093/nsr/nwx082](https://doi.org/10.1093/nsr/nwx082).
9. S. R. Sundara Raman, “A Review on Non-Volatile and Volatile Emerging Memory Technologies,” in *Computer Memory and Data Storage*, A. Seyedi, ed., IntechOpen (2024). [DOI: 10.5772/intechopen.110617](https://doi.org/10.5772/intechopen.110617).
10. J. Guo, “A Low-Voltage Sense Amplifier with Two-Stage Operational Amplifier Clamping for Flash Memory,” *Journal of Semiconductors* **38**, 045001 (2017). [DOI: 10.1088/1674-4926/38/4/045001](https://doi.org/10.1088/1674-4926/38/4/045001).
11. K. Cho, W. Kang, H. Cho, C. Lee, and S. Kang, “A Survey of Repair Analysis Algorithms for Memories,” *ACM Computing Surveys* **49**(3), Article 47 (2016). [DOI: 10.1145/2971481](https://doi.org/10.1145/2971481).
12. R. Rooney and N. Koyle, *Micron DDR5 SDRAM: New Features*, Micron Technology, Rev. A (2019). [공식 기술 문서 PDF](https://www.micron.com/content/dam/micron/global/public/products/white-paper/ddr5-new-features-white-paper.pdf).
13. G. Heiser, “Caches,” *COMP9242 2025 T3 W03 Part 1: HW Considerations*, slide 5, UNSW Sydney (2025), CC BY 4.0. [강의 자료와 재사용 조건](https://cgi.cse.unsw.edu.au/~cs9242/25/lectures/03a-hw.pdf).
14. HandigeHarry, “DRAM,” Wikimedia Commons (2008), public domain. [원본 파일과 재사용 조건](https://commons.wikimedia.org/wiki/File:DRAM.svg).
