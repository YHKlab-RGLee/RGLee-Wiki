---
title: "Build SIESTA"
description: TGM 클러스터에서 Intel oneAPI toolchain과 격리된 의존성으로 SIESTA 5.4.2를 CMake 빌드하고 검증하는 절차
status: verified
last_verified: 2026-08-27
---

# Build SIESTA

이 문서는 TGM 클러스터에서 SIESTA/TranSIESTA를 Intel oneAPI compiler, Intel MPI와 Math Kernel Library (MKL)로 빌드한 재현 기록이다. 2026년 8월 27일에 공식 tag 목록에서 확인한 최신 안정판은 SIESTA 5.4.2이며, 아래 결과는 tag `5.4.2`의 commit `e486d120`을 대상으로 한다.[1,2] 공식 CMake 절차는 source·build directory를 분리하고, compiler·MPI·linear algebra library가 한 toolchain에 속하는지 configure 요약에서 확인하도록 요구한다.[2,3]

모든 source, 중간 파일, 로컬 의존성 및 설치 결과는 저장소의 `experiment/build_siesta/` 아래에 두었다. `/home/tgmadmin`, system prefix, 다른 사용자의 directory와 root 권한은 사용하지 않았다. 이 원칙은 재현을 위한 편의가 아니라, 이미 설치된 계산 프로그램과 compiler module을 변경하지 않는 작업 경계이다.

## 1. 빌드 범위와 환경

### (1) 검증 환경

실제 빌드에 사용한 환경은 다음과 같다. Module의 patch version이 달라지면 ABI와 library 경로도 달라질 수 있으므로 명칭만 같다고 가정하지 않고 `module list`, compiler version과 `MKLROOT`를 함께 기록한다.[2,3]

| 항목 | 이 클러스터에서 확인한 값 | 역할 |
| --- | --- | --- |
| 운영 환경 | Linux x86-64, TGM cluster | build 및 MPI 시험 환경 |
| CMake | 3.22.2 | SIESTA가 요구하는 CMake 3.20 이상 충족 |
| Intel compiler module | `compiler/2023.1.0` | `ifort`, `icc`, `icpc` 제공 |
| Intel compiler 식별값 | 2021.9.0.20230302 | CMake가 실제 검출한 compiler version |
| Intel MPI module | `mpi/2021.12.1` | `mpiifort`, `mpiicc`, `mpiicpc`, `mpiexec` 제공 |
| Intel MKL module | `mkl/2023.1.0` | BLAS, LAPACK, ScaLAPACK과 Intel MPI BLACS 제공 |
| SIESTA source | tag `5.4.2`, commit `e486d120` | 빌드 대상 |
| 격리 작업 경로 | `experiment/build_siesta/` | source, build, install과 시험 출력의 유일한 작업 공간 |

작업을 시작할 때 현재 shell의 module과 compiler wrapper를 확인한다. 다음 명령은 module을 전역 설치하거나 다른 session을 바꾸지 않으며, 현재 shell에서 필요한 module만 추가한다.

```bash
module load compiler/2023.1.0
module load mkl/2023.1.0
module load mpi/2021.12.1

module list
cmake --version
mpiifort --version
printf 'MKLROOT=%s\n' "$MKLROOT"
```

Conda 환경이 `CC`, `FC`, compile flag 또는 `CMAKE_PREFIX_PATH`를 미리 정의한 경우 CMake 탐색 결과가 module stack과 섞일 수 있다. 이 문서의 configure 명령은 해당 변수만 명시적으로 제거하고 compiler wrapper와 로컬 prefix를 다시 지정한다. 로그인 shell 전체의 설정을 수정할 필요는 없다.

### (2) 격리 directory

저장소 root를 `WIKI_ROOT`, 실험 경로를 `SIESTA_WORK`로 정의한다. 두 변수는 이 shell에만 존재하며 `$HOME`이나 system directory를 대신 사용하지 않는다.

```bash
export WIKI_ROOT=/home2/rong/00.Development/0.GitHub/00.SANDBOX/DOC/wiki
export SIESTA_WORK="$WIKI_ROOT/experiment/build_siesta"

mkdir -p "$SIESTA_WORK"
cd "$SIESTA_WORK"
```

최종 directory 구조는 다음과 같다. 이전 configure가 실패해도 새 build directory를 사용했기 때문에 성공한 결과를 덮어쓰지 않았다.

```text
experiment/build_siesta/
├── siesta-5.4.2/             # source와 custom toolchain
├── netcdf-fortran-4.5.3/     # 의존성 source
├── netcdf-fortran-build/     # 의존성 build
├── netcdf-fortran-install/   # Intel Fortran용 netcdf.mod와 libnetcdff
├── libxc-5.2.2/              # 의존성 source
├── libxc-build/              # 의존성 build
├── libxc-install/            # Intel Fortran용 Libxc module과 library
├── build-prod/               # 최종 SIESTA build와 CTest 결과
└── install-prod/             # 최종 설치 prefix
```

## 2. Source와 Fortran 의존성

### (1) SIESTA source

공식 repository를 안정판 tag로 고정하고 submodule을 함께 받는다. `master`의 날짜별 snapshot보다 tag와 commit을 기록해야 같은 source를 다시 선택할 수 있다.[1,2]

```bash
cd "$SIESTA_WORK"
git clone --branch 5.4.2 --depth 1 --recurse-submodules \
  https://gitlab.com/siesta-project/siesta.git siesta-5.4.2

git -C siesta-5.4.2 rev-parse HEAD
git -C siesta-5.4.2 submodule status --recursive
```

기존 기록의 `config/cmake/toolchains` 경로는 현재 5.4.2 source tree에 존재하지 않는다. 현재 경로는 `cmake/toolchains`이며, option 이름은 `SIESTA_TOOLCHAIN`이다. 공식 문서는 이 option에 toolchain 이름 또는 전체 경로를 줄 수 있다고 설명한다.[2,3]

### (2) compiler module ABI 점검

Fortran `.mod` file은 일반적인 C header처럼 compiler 사이에서 호환된다고 가정할 수 없다. 이 클러스터의 system `netcdf.mod`와 `xc_f03_lib_m.mod`는 GNU Fortran으로 만들어져 Intel Fortran compile 단계에서 읽히지 않았다. NetCDF-Fortran은 NetCDF-C와 별도 package이며 `nf-config --fc`로 빌드 compiler를 확인할 수 있다.[4,5]

```bash
nf-config --fc
nf-config --includedir
pkg-config --modversion libxcf03
```

Package metadata만 확인하면 실제 `.mod` parse 오류를 놓칠 수 있다. 다음 최소 program은 NetCDF Fortran module을 읽고 symbol을 link할 수 있는지 함께 검사한다.

```fortran
program probe_netcdf
  use netcdf
  implicit none
  print *, trim(nf90_inq_libvers())
end program probe_netcdf
```

```bash
mpiifort probe_netcdf.f90 \
  $(nf-config --fflags) $(nf-config --flibs) \
  -o probe_netcdf
./probe_netcdf
```

이 환경에서는 `nf-config --fc`가 `gfortran`을 반환했다. 따라서 system NetCDF-C 4.8.1은 읽기 전용 의존성으로 재사용하되, 같은 source version인 NetCDF-Fortran 4.5.3과 Libxc 5.2.2의 Fortran interface를 Intel compiler로 `SIESTA_WORK` 안에 다시 설치했다. 다른 환경에서 위 명령이 선택한 Fortran compiler와 일치하고 작은 module compile probe가 통과한다면 이 절의 재빌드는 생략할 수 있다.

### (3) NetCDF-Fortran 로컬 빌드

NetCDF-Fortran은 NetCDF-C 이후에 빌드하며 C와 Fortran compiler를 명시해야 한다.[4,5] 이 클러스터의 NetCDF-C에는 parallel I/O가 없고 SZIP write 시험은 runtime library와 맞지 않았으므로, SIESTA에 필요하지 않은 SZIP write 시험만 끈 상태로 46개 시험을 통과시켰다.

```bash
cd "$SIESTA_WORK"
git clone --branch v4.5.3 --depth 1 \
  https://github.com/Unidata/netcdf-fortran.git netcdf-fortran-4.5.3

env -u CC -u FC -u FFLAGS -u LDFLAGS -u CMAKE_PREFIX_PATH \
  CC=mpiicc FC=mpiifort \
  cmake -S netcdf-fortran-4.5.3 -B netcdf-fortran-build \
    -DCMAKE_INSTALL_PREFIX="$SIESTA_WORK/netcdf-fortran-install" \
    -DnetCDF_INCLUDE_DIR=/usr/include \
    -DHAVE_SZIP_WRITE=FALSE \
    -DBUILD_TESTING=ON

cmake --build netcdf-fortran-build --parallel 8
ctest --test-dir netcdf-fortran-build --output-on-failure
cmake --install netcdf-fortran-build
```

### (4) Libxc 로컬 빌드

Libxc는 C library와 Fortran 2003 interface를 같은 Intel toolchain으로 만든다. 이 절차에서는 shared library와 시험을 켰고 18,634개 시험이 모두 통과했다.[6,7]

```bash
cd "$SIESTA_WORK"
git clone --branch 5.2.2 --depth 1 \
  https://gitlab.com/libxc/libxc.git libxc-5.2.2

env -u CC -u FC -u CFLAGS -u FFLAGS -u LDFLAGS \
  CC=mpiicc FC=mpiifort \
  cmake -S libxc-5.2.2 -B libxc-build \
    -DCMAKE_INSTALL_PREFIX="$SIESTA_WORK/libxc-install" \
    -DBUILD_SHARED_LIBS=ON \
    -DENABLE_FORTRAN=ON \
    -DBUILD_TESTING=ON

cmake --build libxc-build --parallel 8
ctest --test-dir libxc-build --output-on-failure
cmake --install libxc-build
```

## 3. Intel toolchain

### (1) 개선한 toolchain file

기존 성공 사례는 MKL 2022.1의 절대 경로를 직접 적었다. 이번에는 SIESTA가 제공하는 `intel.cmake`의 compiler flag를 재사용하고, 현재 module이 설정한 `MKLROOT`에서 ScaLAPACK을 찾도록 바꾸었다. 이 방법은 module patch version이 바뀔 때 toolchain file의 절대 경로를 고치는 범위를 줄인다. 단, Intel MPI용 BLACS인 `mkl_blacs_intelmpi_lp64`는 다른 MPI 구현으로 임의 교체할 수 없다.[3,8]

`$SIESTA_WORK/siesta-5.4.2/cmake/toolchains/intel_tgm.cmake`를 다음과 같이 둔다.

```cmake
# TGM cluster toolchain for Intel compiler, Intel MPI, and MKL.
include("${CMAKE_CURRENT_LIST_DIR}/intel.cmake")

if(NOT DEFINED ENV{MKLROOT} OR "$ENV{MKLROOT}" STREQUAL "")
  message(FATAL_ERROR "MKLROOT is not set; load the cluster MKL module first")
endif()

set(SCALAPACK_LIBRARY
  "-L$ENV{MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lmkl_blacs_intelmpi_lp64 -lpthread -lm -ldl"
  CACHE STRING "ScaLAPACK and dependent MKL libraries")
```

`SCALAPACK_LIBRARY`는 LP64 integer interface, sequential MKL core와 Intel MPI BLACS를 하나의 link line으로 고정한다. 반면 CMake가 검출한 BLAS/LAPACK은 Intel threaded MKL이었다. 두 경로가 동시에 link되므로 성능 측정 전에는 계산 node에서 `MKL_NUM_THREADS`와 MPI rank 수를 명시해 oversubscription을 피해야 한다.[2,8]

### (2) 원래 명령과 달라진 점

| 항목 | 기존 명령 | 이번 절차 |
| --- | --- | --- |
| source 지정 | build directory에서 `cmake ..` | `cmake -S ... -B ...`로 위치를 명시 |
| 설치 prefix | `/home/tgmadmin/...` | `experiment/build_siesta/install-prod` |
| compiler | `FC=mpiifort`만 지정 | `CC`, `CXX`, `FC`를 같은 Intel MPI stack으로 지정 |
| toolchain | MKL version 절대 경로 | `MKLROOT`를 사용한 `intel_tgm.cmake` |
| build 유형 | 기본값 의존 | `Release` 명시 |
| 의존성 | system 탐색에 맡김 | Intel ABI로 빌드한 NetCDF-Fortran과 Libxc를 우선 탐색 |
| 격리 | 외부 application directory 설치 | source·build·install을 모두 실험 directory로 한정 |

## 4. SIESTA configure와 빌드

### (1) 로컬 prefix 우선순위

로컬 `nf-config`와 `pkg-config` metadata가 system의 GNU Fortran module보다 먼저 검색되도록 환경을 설정한다. 이 설정은 현재 shell에만 적용한다.

```bash
export PATH="$SIESTA_WORK/netcdf-fortran-install/bin:$PATH"
export PKG_CONFIG_PATH="$SIESTA_WORK/libxc-install/lib64/pkgconfig:$SIESTA_WORK/netcdf-fortran-install/lib64/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
export LD_LIBRARY_PATH="$SIESTA_WORK/libxc-install/lib64:$SIESTA_WORK/netcdf-fortran-install/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

### (2) configure

다음 명령이 최종 `build-prod`와 `install-prod`를 만들었다. `CMAKE_PREFIX_PATH`에는 semicolon으로 두 prefix를 전달하며, Conda에서 상속될 수 있는 compiler와 flag 변수는 `env -u`로 제거한다.

```bash
cd "$WIKI_ROOT"

env -u CC -u CXX -u FC -u F77 -u F90 \
    -u CFLAGS -u CXXFLAGS -u FFLAGS -u LDFLAGS \
    -u CMAKE_PREFIX_PATH \
  CC=mpiicc CXX=mpiicpc FC=mpiifort \
  cmake -S "$SIESTA_WORK/siesta-5.4.2" \
        -B "$SIESTA_WORK/build-prod" \
    -DCMAKE_INSTALL_PREFIX="$SIESTA_WORK/install-prod" \
    -DCMAKE_BUILD_TYPE=Release \
    -DSIESTA_TOOLCHAIN=intel_tgm \
    -DSIESTA_WITH_MPI=ON \
    -DSIESTA_WITH_LIBXC=ON \
    -DNetCDF_ROOT="$SIESTA_WORK/netcdf-fortran-install" \
    -DCMAKE_PREFIX_PATH="$SIESTA_WORK/netcdf-fortran-install;$SIESTA_WORK/libxc-install" \
    -DPython3_EXECUTABLE=/usr/bin/python3 \
    -DCMAKE_AR=/usr/bin/ar \
    -DCMAKE_RANLIB=/usr/bin/ranlib
```

Configure 성공 여부는 마지막 `Configuring done`만으로 판단하지 않는다. 다음 항목이 실제 경로와 일치해야 한다.[2,3]

| 확인 항목 | 기대값 |
| --- | --- |
| Fortran/C/C++ compiler | `mpiifort`, `mpiicc`, `mpiicpc`, 모두 Intel 2021.9 계열 |
| MPI interface | Intel MPI 2021.12, `mpi_f08` |
| BLAS/LAPACK/ScaLAPACK | MKL 2023.1 및 `mkl_blacs_intelmpi_lp64` |
| NetCDF Fortran | `$SIESTA_WORK/netcdf-fortran-install/lib64/libnetcdff.so` |
| Libxc Fortran | `$SIESTA_WORK/libxc-install/lib64/libxcf03.so` |
| 병렬 기능 | `SIESTA_WITH_MPI=ON` |
| 주요 기능 | NetCDF, Libxc, FFTW, DFTD3, ELSI, flook `ON` |

Configure 후에는 cache도 검색해 system Fortran module이 다시 섞이지 않았는지 확인한다. 출력의 NetCDF-Fortran과 Libxc 경로가 반드시 `$SIESTA_WORK` 아래여야 한다.

```bash
rg '^(CMAKE_(Fortran|C|CXX)_COMPILER|NetCDF_Fortran_|LIBXC_|SIESTA_WITH_)' \
  "$SIESTA_WORK/build-prod/CMakeCache.txt"
```

### (3) build와 install

```bash
cmake --build "$SIESTA_WORK/build-prod" --parallel 8
cmake --install "$SIESTA_WORK/build-prod"

find "$SIESTA_WORK/install-prod/bin" -maxdepth 1 -type f \
  -printf '%f\n' | sort
```

Release build와 install은 성공했으며 `install-prod/bin`에 `siesta`, `tbtrans`, `phtrans`, `tscontour`를 포함한 executable 95개가 설치되었다. TranSIESTA는 별도 `transiesta` executable이 아니라 `siesta` 안에 통합된 수송 계산 경로이며, 후처리는 `tbtrans`가 담당한다.[2,9]

설치된 executable의 runtime path에는 `netcdf-fortran-install/lib64`와 `libxc-install/lib64`의 절대 경로가 포함된다. 따라서 `install-prod`만 다른 위치로 복사하는 것은 이 빌드의 배포 절차가 아니다. 이동이 필요하면 두 로컬 의존성을 함께 보존하거나 새 prefix에서 다시 configure·build하고 CTest를 반복한다.

## 5. 시험과 결과

### (1) 시험 방법

공식 문서는 먼저 `ctest -L simple`을 실행하고 필요하면 전체 CTest로 넓히도록 안내한다.[2,10] 이 빌드는 `ruamel.yaml`을 가진 `/usr/bin/python3`를 사용해 실행 성공뿐 아니라 reference 수치 비교도 수행했다.

```bash
# 빠른 핵심 회귀 시험: MPI 4 ranks와 verify 단계 포함
ctest --test-dir "$SIESTA_WORK/build-prod" \
  -L simple --output-on-failure --parallel 2

# 전체 시험은 작업 directory 경합을 피하도록 순차 실행
ctest --test-dir "$SIESTA_WORK/build-prod" \
  --output-on-failure --parallel 1
```

로그인 node나 제한된 container에서는 Intel MPI Hydra가 listening socket을 만들지 못할 수 있다. 이때 나타나는 `cannot open socket (Operation not permitted)`는 SIESTA 계산 실패가 아니다. 이 문서의 MPI 결과는 socket 사용이 허용된 실제 클러스터 실행 조건에서 얻었다.

!!! info "[Measurement]"
    같은 `build-prod`에서 CTest의 exit status와 test count를 기록했다. `simple`은 118/118개가 통과했다. 전체 시험은 순차 실행에서 749/757개, 즉 98.94%가 통과했다. 실패한 8개는 모두 executable이 정상 종료한 뒤 reference tolerance를 벗어난 수치 비교 단계이다. 따라서 “기능 실행 성공”과 “공식 reference 수치 일치”를 서로 다른 판정으로 보고한다.

### (2) 성공한 기능

| 기능 또는 구성 요소 | build/configure | 실행 또는 검증 | 판정 근거 |
| --- | --- | --- | --- |
| SIESTA Release executable | 성공 | 핵심 및 전체 회귀 계산 실행 | build 100%, `siesta` 설치 |
| MPI와 `mpi_f08` | 성공 | 4-rank 회귀 시험 실행 | `simple` 118/118 통과 |
| MKL BLAS/LAPACK/ScaLAPACK | 성공 | BLAS·LAPACK·BLACS symbol probe와 solver 시험 | CMake probe 및 MRRR 시험 통과 |
| NetCDF | 성공 | NetCDF-Fortran 46/46, SIESTA NetCDF write 시험 통과 | `write_ncdf_mpi4` 통과 |
| Libxc와 LibGridXC | 성공 | Libxc 18,634/18,634, LibGridXC MPI/Libxc 시험 통과 | 로컬 Intel module 사용 |
| ELSI–ELPA | 성공 | 1-stage·2-stage와 native ELPA 시험 통과 | solver 계산과 verify 모두 통과 |
| ELSI–PEXSI | 성공 | PEXSI 단위 시험과 SIESTA integration 통과 | 순차 전체 시험에서 verify 통과 |
| ELSI–OMM·NTPoly | 성공 | 각 Fortran 및 SIESTA solver 시험 통과 | 내부 ELSI solver 사용 |
| DFTD3 | 성공 | `dftd3_mpi4` 계산과 verify 통과 | source submodule build |
| FFTW, flook | 성공 | configure 및 관련 dependency 시험 통과 | FFTW 검출, Lua 시험 실행 성공 |
| TranSIESTA | 성공 | 2-terminal x/z, 3-terminal, chain 계산 실행 | 핵심 두 시험 verify 통과, 나머지 실행 성공 |
| TBtrans·PHtrans | 성공 | build/install 및 전체 TBtrans chain 실행 | `tbtrans`, `phtrans` 설치, TBtrans 시험 통과 |
| QMMM·TDDFT·spin–orbit | 성공 | 각 회귀 계산 실행 | 핵심 시험과 다수 전체 시험 통과 |

### (3) 비통과와 비활성 기능

| 항목 | 상태 | 해석 또는 조치 |
| --- | --- | --- |
| 전체 CTest reference 비교 8개 | 749/757 통과 | 8개 모두 계산은 정상 종료했으나 energy 또는 force가 제공 tolerance를 벗어남 |
| Fe spin 계열 4개 | reference 불일치 | collinear/noncollinear Fe 계산의 일부 energy·force 값 차이이며 실행 실패는 아님 |
| FePt spin–orbit 1개 | reference 불일치 | `Ebs`, `Ekin` 중 일부가 tolerance를 벗어남 |
| charge mixing 1개 | reference 불일치 | 일부 energy와 force 값이 reference tolerance를 벗어남 |
| TranSIESTA 3-terminal 1개 | reference 불일치 | 실행은 성공했고 `Ebs=-2621.949585` eV, reference는 `-2621.918160` eV |
| flook Lua H2O 1개 | reference 불일치 | 나머지 값은 일치했으나 `Max_force=0.002266` eV/Å, reference는 0 |
| OpenMP | 의도적으로 비활성 | MPI build를 우선해 `SIESTA_WITH_OPENMP=OFF` 유지 |
| native PEXSI | 비활성 | `SIESTA_WITH_PEXSI=OFF`이나 ELSI 내부 PEXSI는 build 및 시험 성공 |
| external ELPA | 비활성 | ELSI가 제공한 internal ELPA를 사용해 solver 시험 성공 |
| Wannier90, CheSS | 비활성 | 외부 library를 추가하지 않아 각각 `OFF`; 이 문서의 목표 범위 밖 |
| NetCDF parallel I/O | 비활성 | system NetCDF-C가 `NetCDF_PARALLEL=FALSE`; serial NetCDF I/O는 성공 |
| SZIP write | 의도적으로 비활성 | system SZIP runtime과 시험 불일치로 NetCDF-Fortran에서만 끔; SIESTA에 필수 아님 |

!!! warning "[Interpretation Caveat]"
    99%의 CTest 통과율은 이 compiler·library 조합에서 회귀 reference와 비교한 결과이며 다른 CPU, compiler flag 또는 library version의 물리적 정확도를 보증하지 않는다. 특히 custom toolchain의 `-xHost`는 build node의 instruction set에 최적화하므로 더 오래된 compute node에서 실행하면 안 된다. 이기종 node가 섞인 cluster에서는 공통 architecture flag로 바꾸고 다시 시험해야 한다.[2,3]

### (4) 실패 후 해결 기록

| 단계 | 관찰된 오류 | 원인 | 해결 |
| --- | --- | --- | --- |
| Libxc compile | `xc_f03_lib_m.mod`를 읽지 못함 | system module이 GNU Fortran ABI | Libxc 5.2.2를 Intel compiler로 격리 빌드 |
| NetCDF compile | `netcdf.mod`를 읽지 못함 | `nf-config --fc`가 `gfortran` | NetCDF-Fortran 4.5.3을 Intel compiler로 격리 빌드 |
| configure | `ifort: command not found` | 최소화한 `PATH`에서 Intel compiler directory 누락 | module이 제공한 compiler 경로 유지 |
| configure link | `libimf.so`를 찾지 못함 | Intel compiler runtime path 누락 | compiler module의 `LD_LIBRARY_PATH` 유지 |
| MPI CTest | Hydra `cannot open socket` | 제한된 sandbox의 socket 정책 | 실제 cluster MPI 실행 조건에서 재시험 |
| 전체 병렬 CTest | TBtrans 입력 복사 경합과 추가 verify 불일치 | 여러 시험이 공유 작업 파일을 병렬 사용 | 최종 전체 판정은 `--parallel 1`로 수행 |

## 6. 다른 환경에 적용

### (1) 바꿔야 하는 값

이 문서는 일반 Linux에서 compiler와 수치 library를 처음 설치하는 안내가 아니다. 이미 compiler, MPI, BLAS/LAPACK/ScaLAPACK과 CMake가 준비된 환경에서 다음 대응 관계를 바꾸는 기준을 제공한다.[2,3]

| TGM cluster 값 | 다른 환경에서 확인할 값 |
| --- | --- |
| `compiler/2023.1.0`, `mpi/2021.12.1`, `mkl/2023.1.0` | site가 제공하는 서로 호환되는 compiler·MPI·linear algebra module |
| `mpiifort`, `mpiicc`, `mpiicpc` | 해당 MPI로 감싼 Fortran·C·C++ compiler wrapper |
| `mkl_blacs_intelmpi_lp64` | MPI 구현과 integer model에 맞는 ScaLAPACK/BLACS library |
| `/usr/bin/nc-config` | 설치된 NetCDF-C의 feature와 prefix |
| 로컬 `nf-config` | 선택한 Fortran compiler로 만든 NetCDF-Fortran |
| 로컬 Libxc 5.2.2 | SIESTA가 지원하며 같은 Fortran compiler로 만든 Libxc |
| `--parallel 8` | compile node의 허용 CPU와 memory에 맞는 값 |
| `-xHost` | 모든 실행 node가 지원하는 공통 CPU architecture flag |

GNU/OpenMPI 환경에서는 Intel toolchain과 MKL BLACS line을 그대로 복사하지 않는다. 예를 들어 `FC=mpifort`, `CC=mpicc`, `CXX=mpicxx`와 해당 OpenMPI용 ScaLAPACK을 같은 stack에서 선택하고, SIESTA가 제공하는 GNU 계열 toolchain 또는 site toolchain을 사용한다. 중요한 조건은 compiler 이름 자체가 아니라 Fortran module, MPI wrapper와 BLACS 구현의 일관성이다.[2,3,8]

### (2) 최소 판정 순서

1. `module list`, wrapper version, `MKLROOT` 또는 BLAS/ScaLAPACK 경로를 기록한다.
2. `nf-config --fc`와 Libxc Fortran module이 선택한 compiler와 호환되는지 작은 compile probe로 확인한다.
3. CMake summary에서 실제 compiler와 모든 dependency path를 읽는다.
4. build와 install을 서로 다른 격리 directory에서 수행한다.
5. `ctest -L simple`을 먼저 통과시킨 뒤 전체 시험을 순차 실행한다.
6. 계산 실행 실패와 reference tolerance 불일치를 구분해 기록한다.

## 7. 요약

- SIESTA 5.4.2를 Intel oneAPI 2023.1, Intel MPI 2021.12와 MKL 2023.1 stack으로 `experiment/build_siesta` 안에 격리 빌드하고 설치했다.
- GNU Fortran으로 만들어진 system NetCDF와 Libxc module은 Intel Fortran에서 재사용하지 않고 같은 version을 로컬 재빌드했다.
- SIESTA, TranSIESTA, TBtrans, MPI, MKL, NetCDF, Libxc, DFTD3와 ELSI의 ELPA·PEXSI·OMM·NTPoly 경로가 build되었다.
- 핵심 CTest는 118/118개가 통과했고 전체 순차 시험은 749/757개가 통과했다. 남은 8개는 모두 정상 계산 뒤의 reference 수치 비교 실패이다.
- 다른 환경에서는 이 명령의 절대 library 이름을 복사하지 말고 compiler–MPI–BLACS와 Fortran module ABI가 한 stack인지 먼저 확인한다.

## 8. 참고문헌

1. SIESTA Project, “Tags,” *SIESTA GitLab repository* (2026년 8월 확인). [공식 tag 목록](https://gitlab.com/siesta-project/siesta/-/tags).
2. SIESTA Project, “Building Siesta with CMake,” *SIESTA Documentation* (2026년 8월 확인). [공식 문서](https://docs.siesta-project.org/projects/siesta/en/latest/installation/build-manually.html).
3. Kitware, “cmake-toolchains(7),” *CMake Documentation* (2026년 8월 확인). [공식 문서](https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html).
4. Unidata, “Building the NetCDF-4.2 and Later Fortran Libraries,” *NetCDF-Fortran Documentation* (2026년 8월 확인). [공식 문서](https://docs.unidata.ucar.edu/netcdf-c/4.8.1/building_netcdf_fortran.html).
5. Unidata, “NetCDF-Fortran,” *GitHub repository* (2026년 8월 확인). [공식 repository](https://github.com/Unidata/netcdf-fortran).
6. Libxc developers, “Libxc,” *GitLab repository* (2026년 8월 확인). [공식 repository](https://gitlab.com/libxc/libxc).
7. M. A. L. Marques, M. J. T. Oliveira, and T. Burnus, “Libxc: A library of exchange and correlation functionals for density functional theory,” *Computer Physics Communications* **183**, 2272–2281 (2012). [DOI](https://doi.org/10.1016/j.cpc.2012.05.007).
8. Intel, “Using the ILP64 Interface vs. LP64 Interface,” *Intel oneAPI MKL Developer Reference* (2026년 8월 확인). [공식 문서](https://www.intel.com/content/www/us/en/docs/onemkl/developer-guide-linux/2024-2/using-the-ilp64-interface-vs-lp64-interface.html).
9. N. Papior et al., “Improvements on non-equilibrium and transport Green function techniques: The next-generation transiesta,” *Computer Physics Communications* **212**, 8–24 (2017). [DOI](https://doi.org/10.1016/j.cpc.2016.09.022).
10. SIESTA Project, “High performance computing,” *SIESTA Documentation* (2026년 8월 확인). [공식 문서](https://docs.siesta-project.org/projects/siesta/en/stable/hpc/index.html).
