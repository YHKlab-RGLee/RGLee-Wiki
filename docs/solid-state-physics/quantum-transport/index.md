---
title: "4. Quantum transport"
description: 열린 양자계의 정상 상태 전자 수송 정식화와 Green's function 알고리즘 안내
status: verified
last_verified: 2026-08-04
---

# 4. Quantum transport

Quantum transport는 위상 결맞음을 유지하는 전자의 전파, 전극에 의한 열린 경계, 비평형 점유와 전류를 함께 다룬다. Nonequilibrium Green's function (NEGF)은 이 조건에서 상태, 점유와 전류를 연결하는 정식화이다. 이 주제 그룹은 물리적 정식화와 수치 알고리즘을 의존 순서에 따라 구분한다.

1. [4.1. NEGF formalism](negf-formalism.md) — 전극 self-energy, retarded·lesser Green's function, density matrix와 전류
2. [4.2. Surface Green's function](surface-greens-function.md) — 반무한 주기 전극의 표면 응답과 López Sancho repeated-doubling
3. [4.3. Recursive Green's function](recursive-greens-function.md) — block-tridiagonal 소자의 전진 소거·후진 복원과 Poisson–NEGF 계산

처음에는 `NEGF formalism`에서 $G^R$, $\Sigma^R$, $\Gamma$와 $G^<$의 역할을 구분한 뒤, 전극 계산과 소자 내부 계산을 각각 후속 문서에서 읽는 순서를 권한다.
