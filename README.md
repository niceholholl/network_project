# 🕸️ 우간다 네트워크 구조 분석 및 랜덤 모델 비교 분석

본 프로젝트는 실제 **우간다 네트워크 데이터**의 구조적 특성을 분석하기 위해,
직접 구현한 네 가지 랜덤 네트워크 모델 (**Erdős–Rényi(ER), Configuration, Chung-Lu, Barabási–Albert(BA)**)의 앙상블 평균과 원본 데이터를 비교합니다. 

랜덤 모델 생성 함수를 포함한 네트워크 전처리, 중심성 계산 등의 기능은 Python 클래스 형태로 관리됩니다.

---

# Uganda 네트워크 데이터 설명
- 2013년 우간다 마유지 구의 빅토리아 호수에 인접한 17개 농촌 마을의 가구 간 인간관계 및 건강 상담 소셜 네트워크.
- 출처 : https://www.repository.cam.ac.uk/items/a9c9afcc-20e0-4466-8b0b-151cfd26f1a2 
- 사용 데이터 : close friends(친구데이터)
- 노드 : household (139개)
- 엣지 : relationship (640개)
- 사용파일 : 6 village
- 네트워크 형태 : Undirected network, Unweigthed network
- 데이터 수집 질문 :
 먼저 성씨(가문 이름)를 말한 다음, 당신과 매우 친한 친구 최대 10명의 이름(이름 중 두 번째 이름)을 말해주세요.
이 사람은 돈을 지불하지 않고도 당신이 어업이나 농업에 사용하는 도구를 빌릴 수 있을 만큼 편하게 부탁할 수 있는 사람이어야 합니다.
또한, 가까운 친구란 당신이 자주 만나는 사람을 의미합니다.
같은 가구(가족 구성원)는 포함하지 마세요.
가장 친한 사람부터 순서대로 이름을 말해주세요.
오직 같은 마을에 있는 사람만 이름을 적어주세요.
<img width="851" height="673" alt="image" src="https://github.com/user-attachments/assets/18dbf956-c89c-41ce-80e3-f39307764b07" />


## 🎯 (1) 프로젝트 목표

**데이터 기반 분석 :** 실제 네트워크의 **중심성 지표**(Closeness, Betweenness 등) 및 **구조적 특성**(Clustering Coefficient, Diameter 등)을 계산합니다.

**구조적 특이성 검증 :** 원본 네트워크와 네 가지 랜덤 네트워크 모델(**Erdős–Rényi(ER), Configuration, Chung-Lu, Barabási–Albert(BA)**)의 앙상블 평균을 비교하여, 우간다 네트워크의 구조가 **우연히** 발생했는지, 아니면 **특정 메커니즘**으로 형성되었는지 분석합니다.

**코드 모듈화 :** 모든 코드를 일정 형태에서 재사용 가능한 Python 패키지(**`network_tool_pkg`**) 형태로 구현합니다.

---

## 📂 (2) 프로젝트 구조 (Package Map)

본 프로젝트는 기능적 분리를 위해 **`network_tool_pkg`** 메인 패키지 아래에 
**`utils`**
와 **`analysis`** 두 서브 패키지를 가집니다.

(추후작성)

---

## 🛠️ (3) 핵심 구현 클래스 및 모델

## A. `CentralityCalculator` (in `centrality_generator.py`)

* **역할:** 그래프 $G$를 인스턴스로 받아, **직접 구현된** 5가지 중심성 지표 값을 계산합니다.
* **구현 지표:** Degree, Closeness, Harmonic, Betweenness, Eigenvector(Matrix).

## B. `RandomNetGenerator` (in `random_nets_generator.py`)

* **역할:** 입력받은 $N$과 $k$를 기반으로 네 가지 무작위 네트워크 모델을 생성합니다.
* **구현 모델:**
    | 모델 | 유형 | 핵심 원리 | 특징 구현 및 예외 처리 방식 |
    | :--- | :--- | :--- | :--- |
    | **ER Model** | $G(N, p)$ | 모든 노드 쌍이 확률 p로 독립적 연결 | 확률 p의 유효성 검사 | 
    | **Configuration** | $G(N, \mathbf{k})$ | 원본 네트워크의 차수 시퀀스를 완벽 보존 | 차수 시퀀스에 대한 검증 |
    | **Chung-Lu** | $G(N, \mathbf{k})$ | 노드 차수 곱에 비례하여 확률적으로 연결 | 간선 확률 p_ij가 1을 초과하지 않도록 보정 구현 |
    | **BA Model** | $G(N, m)$ | 성장 및 선호적 연결 메커니즘 | $m$값에 대한 범위 검증 |

---

## 💡 (4) 환경 설정 및 사용법

### 설치 요구 사항
```bash
pip install networkx numpy matplotlib scipy
```

### 패키지 불러오기
프로젝터 폴더를 클론한 후, 다음과 같이 클래스를 불러와 사용합니다.
```python
# analysis_script.py 에서
from random_nets import RandomNetGenerator 
import networkx as nx

# 1. 원본 데이터 로드 및 차수 시퀀스 추출
G_original = nx.karate_club_graph() # 또는 외부 데이터 G를 사용
degrees = [d for _, d in G_original.degree()]
N = G_original.number_of_nodes()

# 2. 클래스 인스턴스 생성
generator = RandomNetGenerator(N_nodes=N, initial_degrees=degrees)

# 3. 모델 생성 (앙상블 생성 루프에 사용)
G_er_sample = generator.create_er_net(p=0.08)
G_cm_sample = generator.create_config_model()
```

추후 수정

---

## ✨ (5) 핵심 분석 결과 요약

추후 작성

---

