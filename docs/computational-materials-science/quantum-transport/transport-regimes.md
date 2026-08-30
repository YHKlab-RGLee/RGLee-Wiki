---
description: 길이 척도와 산란을 기준으로 ballistic, quasi-ballistic, diffusive 전자 수송을 구분하고 Landauer·Boltzmann·drift–diffusion 방정식의 관계를 설명
---

# Electronic transport regimes

전자 수송에서 **ballistic**, **quasi-ballistic**, **diffusive transport**는 서로 다른 물질 종류를 뜻하지 않는다. 같은 물질도 온도, 불순물, 소자 길이와 폭에 따라 다른 regime에 놓일 수 있다. 핵심은 운반자가 관측 구간을 지나는 동안 운동량을 충분히 잃는지, 접촉에서 주입된 분포를 유지하는지, 그리고 양자 위상을 보존하는지를 서로 다른 길이 척도로 비교하는 것이다.[1–4]

이 글은 저전계 정상 상태의 전자 수송을 기준으로 세 regime의 물리와 대표 지배 방정식을 정리한다. 이후 문서에서 사용하는 bulk mobility와 mean free path는 [Carrier mobility from first principles](carrier-mobility.md), 열린 경계와 transmission은 [NEGF formalism](negf-formalism.md), microscopic phonon scattering은 [Electron–phonon coupling](electron-phonon-coupling.md)을 따른다.

## 1. 길이 척도와 regime map

### (1) Transport mean free path

수송 방향의 특성 길이를 $L$이라 하고, 운동량을 이완시키는 평균 거리를 transport mean free path $\lambda_{\mathrm{mr}}$로 쓴다. 등방적 relaxation-time approximation (RTA)의 단순한 경우에는

$$
\lambda_{\mathrm{mr}}\simeq v\tau_{\mathrm{mr}}
$$

이다. $v$는 수송에 참여하는 상태의 속도이고 $\tau_{\mathrm{mr}}$는 momentum-relaxation time이다. 모든 충돌이 속도 방향을 같은 정도로 바꾸지는 않으므로, 충돌 사이의 평균 거리와 backscattering mean free path는 일반적으로 동일하지 않다. 실제 수송 분류에는 전류를 이완시키는 $\lambda_{\mathrm{mr}}$ 또는 $\lambda_{\mathrm{bs}}$를 사용해야 한다.[1–3,5]

두 길이의 비를 Knudsen-like number로 정의하면

$$
\mathrm{Kn}=\frac{\lambda_{\mathrm{mr}}}{L}
$$

이다. $\mathrm{Kn}\gg1$이면 내부 momentum-relaxing scattering이 드물고, $\mathrm{Kn}\ll1$이면 관측 구간 안에서 많은 산란이 일어난다. $\mathrm{Kn}\sim1$은 두 극한이 섞이는 crossover이다. 경계는 정확한 상수가 아니며, 폭 $W$, 접촉 형상, 산란의 각도·에너지 의존성과 관측량에 따라 달라진다.[1–5]

### (2) Phase coherence는 별도 축이다

Phase-coherence length $L_\phi$는 전자 파동의 상대 위상이 무작위화되기 전까지 유지되는 길이이다. Diffusive motion 안에서 phase-breaking time을 $\tau_\phi$라 하면

$$
L_\phi=\sqrt{D\tau_\phi}
$$

로 쓸 수 있다. $D$는 diffusion coefficient이다. 반면 충돌 없이 거의 직진하는 구간에서는 대응하는 비행 길이가 대략 $v\tau_\phi$로 바뀐다. Elastic impurity scattering은 운동량을 바꾸면서도 위상을 보존할 수 있으므로 $\lambda_{\mathrm{mr}}$와 $L_\phi$를 같은 길이로 놓으면 안 된다.[1,6]

따라서 `ballistic–diffusive`는 주로 momentum relaxation의 분류이고, `coherent–incoherent`는 위상 보존의 분류이다. 예를 들어

$$
\lambda_{\mathrm{mr}}\ll L\ll L_\phi
$$

이면 여러 elastic scattering을 겪는 **phase-coherent diffusive transport**가 가능하다. 이 regime에서는 평균 전류가 Ohmic하게 보여도 weak localization이나 conductance fluctuation 같은 간섭 보정이 나타날 수 있다.[1,6]

| 길이 척도 | 정의 | 지배하는 질문 | 혼동하기 쉬운 점 |
|---|---|---|---|
| $\lambda_F$ | 대표 운반자의 Fermi wavelength | 횡방향 mode와 양자 구속을 분해해야 하는가? | Mean free path가 아님 |
| $\lambda_{\mathrm{mr}}$ | 운동량 또는 전류 방향이 이완되는 거리 | Ballistic–diffusive 중 어느 쪽인가? | 단순 충돌 간 거리와 다를 수 있음 |
| $\lambda_E$ | 에너지 분포가 격자·bath와 이완되는 거리 | 국소 온도나 hot carrier를 정의할 수 있는가? | Momentum relaxation과 동일하지 않음 |
| $L_\phi$ | 위상 기억이 유지되는 거리 | 간섭과 coherent transmission이 남는가? | Diffusive transport에서도 길 수 있음 |
| $L$, $W$ | 수송 길이와 횡방향 폭 | 내부 산란과 경계 산란 중 무엇이 중요한가? | 하나의 `device size`로 합치면 geometry를 잃음 |

### (3) 세 regime의 첫 비교

| Regime | 대표 길이 관계 | 운반자 분포의 물리 | 저항의 주된 기원 | 대표 지배식 | 자연스러운 물리량 |
|---|---|---|---|---|---|
| Ballistic | $L\ll\lambda_{\mathrm{mr}}$ | 두 reservoir에서 주입된 전진·후진 분포가 내부에서 거의 섞이지 않음 | 접촉의 mode 수, barrier와 interface reflection | Landauer–Büttiker | $T(E)$, $M(E)$, $G$ |
| Quasi-ballistic | $L\sim\lambda_{\mathrm{mr}}$ | 주입 기억과 내부 scattering이 함께 남음 | 접촉 저항과 길이 의존 산란 저항의 공존 | 경계조건을 가진 BTE 또는 scattering NEGF | $T(E,L)$, backscattering, 비평형 $f$ |
| Diffusive | $L\gg\lambda_{\mathrm{mr}}$ | 많은 산란으로 방향 정보가 국소적으로 이완됨 | 체적 resistivity와 농도 구배 | BTE의 diffusive limit, drift–diffusion | $\sigma$, $\mu$, $D$, $\rho$ |

이 표는 모형 선택의 출발점이지 배타적인 판정표가 아니다. Energy-dependent mean free path가 넓게 분포하면 같은 소자에서 어떤 에너지의 운반자는 ballistic이고 다른 운반자는 diffusive일 수 있다. 횡방향으로 $W<\lambda_{\mathrm{mr}}<L$이면 경계와 내부 산란이 모두 중요한 좁은 채널의 quasi-ballistic size effect가 나타난다.[1–5]

## 2. 공통 출발점: Boltzmann transport equation

### (1) Phase-space 분포의 운동

Semiclassical Boltzmann transport equation (BTE)은 위치 $\mathbf r$, wave vector $\mathbf k$와 시간 $t$에 따른 분포 $f_n(\mathbf r,\mathbf k,t)$를 기술한다.

$$
\frac{\partial f_n}{\partial t}
+\mathbf v_{n\mathbf k}\cdot\nabla_{\mathbf r}f_n
+\frac{\mathbf F}{\hbar}\cdot\nabla_{\mathbf k}f_n
=\left.\frac{\partial f_n}{\partial t}\right|_{\mathrm{coll}}
$$

$n$은 band index, $\mathbf v_{n\mathbf k}=\hbar^{-1}\nabla_{\mathbf k}\varepsilon_{n\mathbf k}$는 group velocity, $\mathbf F$는 외력, 오른쪽 항은 collision operator이다. Ballistic limit에서는 device 내부의 collision term이 작고 경계에서 들어오는 분포가 중요하다. Diffusive limit에서는 collision term이 강하게 분포를 이완시키므로 그 낮은 차수 moment인 밀도와 전류만으로 닫힌 관계를 만들 수 있다. Quasi-ballistic regime에서는 streaming, collision과 열린 경계조건을 동시에 보존해야 한다.[2–4,7,8]

전류 밀도는 분포의 velocity moment이다.

$$
\mathbf J(\mathbf r)
=q\sum_n\int_{\mathrm{BZ}}\frac{d\mathbf k}{(2\pi)^d}
\mathbf v_{n\mathbf k}f_n(\mathbf r,\mathbf k)
$$

$q$는 부호를 포함한 운반자 전하이고 $d$는 공간 차원이다. 세 regime의 차이는 이 식 자체가 아니라, $f$를 접촉 주입으로 정하는지, collision equation으로 정하는지, 또는 두 효과를 함께 풀어야 하는지에 있다.[2–4,7]

### (2) 하나의 방정식과 서로 다른 경계조건

정상 상태의 단순한 확률 보존 RTA는

$$
\mathbf v\cdot\nabla_{\mathbf r}f
+\frac{\mathbf F}{\hbar}\cdot\nabla_{\mathbf k}f
=-\frac{f-\langle f\rangle_{\mathbf k}}{\tau_{\mathrm{mr}}}
$$

처럼 쓸 수 있다. $\langle f\rangle_{\mathbf k}$는 같은 에너지 껍질에서 각도 평균한 분포이며, 단순히 고정된 $f^0$로 이완시키는 식보다 입자 수 보존을 명시한다. 유한 conductor에서는 왼쪽 접촉이 $v_x>0$인 상태를, 오른쪽 접촉이 $v_x<0$인 상태를 공급하는 inflow boundary condition이 필요하다.[4,7,8]

$$
f(0,\mathbf k)=f_L(E)\quad(v_x>0),
\qquad
f(L,\mathbf k)=f_R(E)\quad(v_x<0)
$$

$L/\lambda_{\mathrm{mr}}$를 바꾸면 같은 kinetic equation이 Landauer형 ballistic conductance와 Boltzmann–Drude형 diffusive conductance 사이를 연속적으로 연결할 수 있다. 따라서 BTE를 `diffusive 전용`, Landauer를 `ballistic 전용`으로 절대적으로 나누기보다, 실제 구현이 유지하는 coherence, band structure, scattering self-energy와 boundary condition을 확인해야 한다.[2–5,7]

## 3. Ballistic transport

### (1) 접촉 주입과 transmission

Ballistic conductor에서는 운반자가 device 내부에서 momentum-relaxing scattering을 거의 겪지 않는다. 그렇다고 두 단자 저항이 0인 것은 아니다. Reservoir는 들어온 운반자를 흡수·열평형화하고, 접촉은 유한한 수의 propagating mode만 주입한다. 따라서 내부 electric field에 대한 local conductivity보다 한 접촉에서 주입된 flux가 반대 접촉에 도달할 transmission이 기본 물리량이다.[1–3,6]

두 reservoir의 electrochemical potential을 각각 $\mu_L$, $\mu_R$라 하면 Landauer 전류는

$$
I=\frac{g|q|}{h}\int dE\,
M(E)\mathcal T(E)
\left[f(E-\mu_L)-f(E-\mu_R)\right]
$$

이다. $g$는 식의 $M(E)$에 포함하지 않은 spin·valley degeneracy, $M(E)$는 한 방향으로 진행하는 mode 수, $\mathcal T(E)$는 mode 평균 transmission이다. Mode별 transmission을 명시하면 $M\mathcal T$ 대신 $\sum_mT_m(E)$를 쓴다.[2,3,5,6]

낮은 온도와 작은 bias에서

$$
G=\frac{gq^2}{h}\sum_mT_m(E_F)
$$

가 된다. 이상적인 열린 mode는 $T_m=1$이므로 mode 하나가 conductance quantum $gq^2/h$를 제공한다. 대응하는 two-terminal contact resistance는

$$
R_{\mathrm{contact}}
=\left(\frac{gq^2}{h}M\right)^{-1}
$$

이며 channel 안의 충돌 저항과 구분해야 한다. Four-terminal 측정에서는 voltage probe의 정의와 접촉 투과율에 따라 접촉항의 분리가 달라진다.[1,3,6]

### (2) Ballistic에서 보존되는 정보

Elastic ballistic model에서는 개별 운반자의 에너지가 scattering region을 통과하는 동안 보존되고, coherent 계산이면 phase도 보존된다. 그러나 `ballistic` 자체가 항상 `phase coherent`와 동의어인 것은 아니다. 위상 무작위화가 momentum backscattering 없이 일어나는 환경이나, 여러 incoherent ballistic segment를 reservoir처럼 연결한 모형도 가능하다.[1,3,6]

Ballistic conductance는 sample length에 비례하는 bulk resistivity로 환산하는 것이 자연스럽지 않다. $G$는 mode 수, band alignment, barrier, interface와 contact self-energy에 민감하다. 이 이유로 원자적 junction이나 짧은 channel은 [NEGF formalism](negf-formalism.md)의 open-boundary Green's function과 Landauer transmission으로 다룬다.[1–4]

## 4. Quasi-ballistic transport

### (1) 접촉 기억과 내부 산란의 공존

$L\sim\lambda_{\mathrm{mr}}$이면 운반자는 평균적으로 0회, 1회 또는 소수의 momentum-relaxing event를 겪는다. 전진 분포는 source injection의 기억을 유지하면서 일부가 반사되고, 후진 분포는 drain injection과 channel backscattering을 함께 포함한다. 따라서 위치마다 하나의 shifted Fermi distribution이나 local mobility를 가정하는 drift–diffusion closure가 충분하지 않을 수 있다.[1,4,5,7,8]

균일하고 저전계인 conductor에서 backscattering mean free path $\lambda_{\mathrm{bs}}(E)$를 사용하는 단순한 crossover model은

$$
\mathcal T(E,L)
\simeq\frac{\lambda_{\mathrm{bs}}(E)}
{L+\lambda_{\mathrm{bs}}(E)}
$$

이다. 이 식은

$$
\mathcal T\rightarrow1\quad(L\ll\lambda_{\mathrm{bs}}),
\qquad
\mathcal T\rightarrow\frac{\lambda_{\mathrm{bs}}}{L}
\quad(L\gg\lambda_{\mathrm{bs}})
$$

의 두 극한을 잇는다. Mode 수와 mean free path가 에너지 창 안에서 거의 일정하면 two-terminal resistance는

$$
R(L)\simeq
\frac{h}{gq^2M}
\left(1+\frac{L}{\lambda_{\mathrm{bs}}}\right)
$$

로 분해된다. 첫 항은 ballistic contact resistance이고 두 번째 항은 scattering으로 길이에 따라 증가하는 channel resistance이다.[4,5,9]

이 interpolation은 보편적인 exact law가 아니다. 균일한 산란, 이상적인 reservoir와 특정 backscattering 정의를 가정한다. 여러 barrier의 coherent interference, strongly energy-dependent scattering, 공간적으로 변하는 potential, inelastic energy relaxation과 mode mixing이 강하면 BTE를 실제 경계조건과 함께 풀거나 scattering self-energy를 포함한 nonequilibrium Green's function (NEGF)을 사용해야 한다.[3–5,7,9]

### (2) Nonlocal response

Diffusive limit에서는 한 점의 전류를 그 점의 electric field와 연결하지만, quasi-ballistic transport에서는 운반자가 평균 자유 행로 동안 주변 potential을 표본화한다. 일반적인 선형 응답은

$$
J_\alpha(\mathbf r)
=\int d\mathbf r'\,
\sigma_{\alpha\beta}(\mathbf r,\mathbf r')
E_\beta(\mathbf r')
$$

처럼 nonlocal conductivity kernel을 필요로 할 수 있다. $\sigma(\mathbf r,\mathbf r')$가 $\delta(\mathbf r-\mathbf r')$에 가깝게 국소화될 때만 $\mathbf J(\mathbf r)=\boldsymbol\sigma(\mathbf r)\mathbf E(\mathbf r)$가 회복된다. 이러한 nonlocality가 quasi-ballistic regime에서 local mobility와 voltage-drop 위치를 모호하게 만드는 근본 원인이다.[1,3,4,7]

## 5. Diffusive transport

### (1) 많은 산란과 local constitutive relation

$L\gg\lambda_{\mathrm{mr}}$이면 운반자의 초기 진행 방향은 관측 길이보다 짧은 범위에서 잊힌다. 약한 전기장과 공간적으로 천천히 변하는 조건에서는 BTE를 local equilibrium 주변에서 전개하여 Ohm·drift–diffusion 관계를 얻을 수 있다. Homogeneous conductor의 기본 관계는

$$
\mathbf J=\boldsymbol\sigma\mathbf E
$$

이고, RTA conductivity tensor는

$$
\sigma_{\alpha\beta}
=gq^2\sum_n\int_{\mathrm{BZ}}
\frac{d\mathbf k}{(2\pi)^d}
v_{n\mathbf k,\alpha}v_{n\mathbf k,\beta}
\tau_{n\mathbf k}
\left(-\frac{\partial f^0}{\partial\varepsilon}\right)
$$

로 쓸 수 있다. $g$는 degeneracy, $f^0$는 local equilibrium distribution이다. 이 식은 상태별 속도와 momentum relaxation을 Fermi window에서 평균하며, [Carrier mobility from first principles](carrier-mobility.md)의 iterative BTE는 RTA에서 생략한 scattering-in을 복원한다.[2,7,8]

등방적인 single-carrier system에서는

$$
\sigma=|q|n\mu,
\qquad
R_{\mathrm{channel}}=\rho\frac{L}{A},
\qquad
\rho=\sigma^{-1}
$$

이다. $n$은 carrier density, $\mu$는 drift mobility, $A$는 단면적이다. 2차원 재료에서는 $A$ 대신 폭 $W$와 sheet conductivity를 사용해야 한다. Diffusive regime의 식별 특징은 충분히 긴 균일 구간에서 channel resistance가 $L$에 비례한다는 점이다.[1–5]

### (2) Diffusion과 Einstein relation

농도 구배가 있으면 particle density는 continuity equation

$$
\frac{\partial n}{\partial t}+\nabla\cdot\boldsymbol\Gamma
=G-R
$$

을 따른다. $\boldsymbol\Gamma$는 particle flux, $G$와 $R$은 각각 generation과 recombination rate이다. 전기장이 없고 등방적인 경우 Fick law는

$$
\boldsymbol\Gamma=-D\nabla n
$$

이다. Nondegenerate carrier가 local thermal equilibrium에 있을 때 mobility와 diffusion coefficient는

$$
D=\frac{k_BT}{|q|}\mu
$$

로 연결된다. Degenerate system에서는 chemical-potential derivative 또는 thermodynamic density of states를 포함한 generalized Einstein relation이 필요하다.[2,7,8]

Diffusive라는 사실만으로 위상이 이미 사라졌다는 결론은 나오지 않는다. $\lambda_{\mathrm{mr}}\ll L_\phi$이면 elastic random walk의 여러 경로가 위상 간섭을 일으켜 classical Drude conductivity에 quantum correction을 더한다. 반대로 room-temperature bulk transport처럼 $L_\phi$가 짧고 국소 평균이 충분하면 classical drift–diffusion이 적절하다.[1,6]

## 6. Governing equation과 계산 방법 선택

### (1) 모형 계층

| 물리 질문 | 필요한 정보 | 대표 방정식·방법 | 직접 얻는 양 | 실패하기 쉬운 조건 |
|---|---|---|---|---|
| 이상적인 짧은 channel의 전류 | Contact distribution, mode, elastic transmission | Landauer–Büttiker, coherent NEGF | $I$, $G$, $T(E)$ | 강한 inelastic scattering을 생략할 때 |
| 소수 산란을 포함한 finite device | 공간·운동량 분포와 inflow boundary | Spatial BTE, Monte Carlo, scattering NEGF | $f(\mathbf r,\mathbf k)$, $I$, backscattering | Local mobility만 가정할 때 |
| 균일 bulk의 저전계 수송 | Band velocity와 collision operator | Linearized BTE, Kubo | $\sigma$, $\mu$, $D$ | Device contact를 bulk 계수로 대체할 때 |
| 긴 소자의 전위·농도 분포 | 국소 material coefficient와 electrostatics | Drift–diffusion + Poisson | $n(\mathbf r)$, $\phi(\mathbf r)$, $J$ | $L\sim\lambda_{\mathrm{mr}}$에서 local closure를 쓸 때 |

Landauer와 BTE는 서로 모순되는 전류 법칙이 아니다. Diffusive limit에서 transmission을 mean free path와 mode로 표현하면 Landauer conductance는 Boltzmann–Drude conductivity와 같은 길이 의존성을 준다. 반대로 적절한 inflow boundary condition을 가진 BTE는 scattering을 줄였을 때 ballistic conductance로 접근한다. Kubo는 평형계의 선형 응답이라는 다른 출발점에서 동일한 transport coefficient를 기술한다.[2–5,7,9]

### (2) 길이 의존성으로 regime 판정

두 단자 저항을 여러 길이에서 계산하거나 측정하면

$$
R_{2\mathrm T}(L)=R_c+\rho\frac{L}{A}
$$

로 접촉항과 diffusive slope를 분리할 수 있다. $R_c$는 두 접촉과 ballistic mode mismatch를 포함하며, $dR/dL=\rho/A$가 길이에 독립적인 구간이 bulk diffusive extraction window이다. 짧은 길이에서 곡률이 크거나 intercept가 지배적이면 quasi-ballistic 또는 ballistic correction을 무시할 수 없다.[2,4,5,10]

!!! info "[Measurement]"
    동일한 폭·접촉·carrier density와 온도에서 여러 $L$의 two-terminal resistance 또는 transmission을 구한다. $R(L)$의 선형 구간에서 $\rho=A\,dR/dL$를 추출하고, intercept로 $R_c$를 구한다. 독립적으로 계산한 $\lambda_{\mathrm{mr}}(E)$ 또는 $\lambda_{\mathrm{bs}}(E)$를 수송 에너지 창에서 평균하여 $\mathrm{Kn}=\lambda/L$를 보고한다. Ballistic 쪽에서는 $G/(gq^2/h)$로 유효 transmitted mode 수를, diffusive 쪽에서는 $\sigma=1/\rho$와 $\mu=\sigma/(|q|n)$를 함께 제시한다. Width, dimensional normalization, contact model, phase-breaking 처리와 포함한 scattering mechanism을 고정하지 않으면 서로 다른 길이의 결과를 한 직선으로 비교할 수 없다.

## 7. 적용 범위와 경계 사례

### (1) 하나의 mean free path가 충분하지 않은 경우

실제 band structure에서는 $\lambda(E,n,\mathbf k)$가 넓게 분포하며 acoustic phonon, polar optical phonon, impurity와 boundary scattering이 서로 다른 방향·에너지 의존성을 갖는다. 이때 단일 $\lambda$는 특정 관측량에 가중 평균한 유효값이다. Conductance, energy relaxation과 phase coherence는 서로 다른 평균을 요구하므로 한 실험에서 얻은 mean free path를 다른 문제에 그대로 넣으면 안 된다.[2,5,7,8]

### (2) 세 regime 밖의 물리

이 글의 분류는 weakly interacting quasiparticle의 저전계 수송을 전제로 한다. Electron–electron collision이 momentum-relaxing collision보다 훨씬 빠르면 hydrodynamic transport가 별도 regime으로 나타날 수 있다. 매우 긴 coherent disordered conductor에서는 Anderson localization이 classical diffusion을 깨뜨릴 수 있고, 높은 전기장에서는 분포가 local equilibrium에서 멀어져 hot-carrier와 velocity-saturation physics가 필요하다.[1,2,6–8]

!!! warning "[Interpretation Caveat]"
    `Ballistic`, `quasi-ballistic`, `diffusive`는 계산 방법의 이름이 아니라 물리적 길이 관계이다. Coherent NEGF에 dephasing self-energy를 추가할 수 있고, BTE에도 finite-device boundary condition을 주어 ballistic crossover를 풀 수 있다. 방법의 label만으로 포함된 scattering, phase breaking 또는 contact resistance를 추정하지 말고 실제 Hamiltonian, collision operator와 boundary condition을 확인해야 한다.[2–5,7]

## 8. 요약

- Ballistic–diffusive 분류의 기본 축은 $\mathrm{Kn}=\lambda_{\mathrm{mr}}/L$이며, phase coherence는 $L_\phi$라는 별도 축이다.
- Ballistic transport에서는 접촉이 주입한 mode와 transmission이 전류를 정하며, channel scattering이 없어도 유한한 two-terminal contact resistance가 남는다.
- Quasi-ballistic transport는 접촉 주입과 내부 backscattering이 함께 남는 crossover이다. Local mobility보다 경계조건을 가진 분포 함수 또는 $T(E,L)$가 자연스럽다.
- Diffusive transport에서는 많은 momentum-relaxing event 뒤에 local conductivity, mobility와 diffusion coefficient가 유효하고 균일한 channel resistance가 길이에 비례한다.
- Landauer, BTE와 drift–diffusion은 배타적인 이론이 아니라 transmission 수준, phase-space distribution 수준과 local moment 수준으로 이어지는 모형 계층이다.
- Regime을 보고할 때는 $L$, $W$, $\lambda_{\mathrm{mr}}$, $L_\phi$, 접촉 조건과 산란원을 함께 밝혀야 한다.

## 9. 참고문헌

1. C. W. J. Beenakker and H. van Houten, "Quantum Transport in Semiconductor Nanostructures," *Solid State Physics* **44**, 1–228 (1991). [DOI](https://doi.org/10.1016/S0081-1947(08)60091-0), [arXiv](https://arxiv.org/abs/cond-mat/0412664)
2. R. Claes, S. Poncé, G.-M. Rignanese, and G. Hautier, "Phonon-limited electronic transport through first principles," *Nature Reviews Physics* **7**, 73–90 (2025). [DOI](https://doi.org/10.1038/s42254-024-00795-0)
3. Y. Imry and R. Landauer, "Conductance viewed as transmission," *Reviews of Modern Physics* **71**, S306–S312 (1999). [DOI](https://doi.org/10.1103/RevModPhys.71.S306)
4. H. Geng, W.-Y. Deng, Y.-J. Ren, L. Sheng, and D.-Y. Xing, "Unified semiclassical approach to electronic transport from diffusive to ballistic regimes," *Chinese Physics B* **25**, 097201 (2016). [DOI](https://doi.org/10.1088/1674-1056/25/9/097201), [arXiv](https://arxiv.org/abs/1601.03485)
5. Y. A. Kruglyak, "Landauer–Datta–Lundstrom generalized transport model for nanoelectronics," *Journal of Nanoscience* **2014**, 725420 (2014). [DOI](https://doi.org/10.1155/2014/725420)
6. T. Schäpers, "Phase-Coherent Transport," in R. Waser (ed.), *Nanotechnology, Volume 3: Information Technology I* (Wiley-VCH, 2008), pp. 3–34. [ISBN](https://www.wiley-vch.de/en/areas-interest/natural-sciences/nanotechnology-volume-3-978-3-527-31738-7)
7. S. Poncé, W. Li, S. Reichardt, and F. Giustino, "First-principles calculations of charge carrier mobility and conductivity in bulk semiconductors and two-dimensional materials," *Reports on Progress in Physics* **83**, 036501 (2020). [DOI](https://doi.org/10.1088/1361-6633/ab6a43), [arXiv](https://arxiv.org/abs/1908.01733)
8. K. Rupp, C. Jungemann, S.-M. Hong, M. Bina, T. Grasser, and A. Jüngel, "A review of recent advances in the spherical harmonics expansion method for semiconductor device simulation," *Journal of Computational Electronics* **15**, 939–958 (2016). [DOI](https://doi.org/10.1007/s10825-016-0828-z)
9. C. Jeong, R. Kim, M. Luisier, S. Datta, and M. S. Lundstrom, "On Landauer versus Boltzmann and full band versus effective mass evaluation of thermoelectric transport coefficients," *Journal of Applied Physics* **107**, 023707 (2010). [DOI](https://doi.org/10.1063/1.3291120)
10. T. Markussen, M. Palsgaard, D. Stradi, T. Gunst, M. Brandbyge, and K. Stokbro, "Electron-phonon scattering from Green's function transport combined with molecular dynamics: Applications to mobility predictions," *Physical Review B* **95**, 245210 (2017). [DOI](https://doi.org/10.1103/PhysRevB.95.245210), [arXiv](https://arxiv.org/abs/1701.02883)
