# 🕸️ 우간다 네트워크 구조 분석 및 랜덤 모델 비교 분석 🕸️

본 프로젝트는 실제 **우간다 농촌 공동체(friendship) 네트워크 데이터**를 기반으로 실행합니다.

- 실제 네트워크의 구조적 특성을 측정
- 실제 네트워크와 랜덤 네트워크 모델과의 비교
- 구조가 **랜덤**인지, **메커니즘 기반 구조**인지를 검증

# 

랜덤 네트워크 모델

- ### **ER (Erdős–Rényi) model** 
- ### **Configuration model**
- ### **Chung-Lu model**
- ### **BA (Barabási–Albert) model**

#

본 프로젝트에서는 BA 랜덤 네트워크 모델을 제외한 나머지 세 모델을 이용합니다. 
모델별 앙상블 평균을 기반으로 **Degree 분포**, **Centrality 분포**, Global metrics(**클러스터링 계수, 평균 경로 길이, 지름**)를 분석합니다. 
또, 랜덤 모델 생성 함수를 포함한 네트워크 전처리, 중심성 계산 등의 기능은 Python 클래스 형태로 관리됩니다.

---

# 📄 목차 📄
1. [데이터 설명](#-데이터-설명-)
2. [프로젝트 목표](#-프로젝트-목표-)
3. [프로젝트 구조](#-프로젝트-구조-)
4. [핵심 클래스 설명](#-핵심-클래스-설명-)
5. [유틸리티 함수 설명](#-유틸리티-함수-설명-)
6. [환경 설정 및 실행 방법](#-환경-설정-및-실행-방법-)
7. [핵심 분석 결과](#-핵심-분석-결과-)
8. [결론](#-결론-)


---

# 🇺🇬 데이터 설명 🇺🇬

본 연구에 사용된 데이터는 **2013년 우간다 마유지 구의 빅토리아 호수에 인접한 17개 농촌 마을의 친구 관계 네트워크**입니다.

출처 (Cambridge Repository) :
https://www.repository.cam.ac.uk/items/a9c9afcc-20e0-4466-8b0b-151cfd26f1a2 

#

### 📌 네트워크 구성
- **노드** : households (139개)
- **엣지** : relationship (640개)
- **네트워크 형태** : Undirected, Unweighted
- 사용 데이터 : close friends (friendship)
- 사용 파일 : 6 village

#

### 📌 데이터 질문
> "당신이 매우 친한 친구 10명을 말해주세요.
> 같은 마을에 살며, 자주 만나고 도구를 빌려줄 정도로 친밀한 사람. 단, 같은 가족 구성원은 포함하지 마세요."

#

### 📌 네트워크의 개략적인 구조 (Overview)

<img width="851" height="673" alt="image" src="https://github.com/user-attachments/assets/18dbf956-c89c-41ce-80e3-f39307764b07" />

(현실 기반 네트워크로 연결 패턴이 비교적 높은 응집력과 일부 중심 허브 존재하는 구조)

---

# 🎯 프로젝트 목표 🎯

### ✔ 실제 네트워크의 구조적 특성 정량화
- Degree distribution  
- Betweenness / Closeness Centrality  
- Global metrics (Clustering coefficient, Average Path Length, Diameter)

#

### ✔ 실제 네트워크 vs 랜덤 네트워크 모델 비교
- 사용 모델
  - **ER**
  - **Configuration**
  - **Chung-Lu**
  - BA (모델 구현은 되어있으나 본 분석에서는 제외)
- 다양한 무작위 생성 모델이 원본 네트워크의 구조를 얼마나 재현하는지 평가 및 분석
  
#

### ✔ 패키지화된 모듈(`network_tool_pkg`) 구축
- 모든 코드를 일정 형태에서 재사용 가능한 Python 패키지 형태로 구현

---

# 📂 프로젝트 구조 📂

본 프로젝트는 기능적 분리를 위해 **`network_tool_pkg`** 메인 패키지 아래에 **`utils`** 와 **`analysis`** 두 서브 패키지를 가집니다.

```
📁 network_tool_pkg/
│
├── 📁 analysis/
│    ├── 📄 centrality_generator.py      # 중심성 직접 구현 클래스
│    ├── 📄 random_nets_generator.py     # ER / CF / CL / BA 랜덤 네트워크 생성기
│
├── 📁 utils/
│    ├── 📄 preprocessing.py             # 네트워크 데이터 전처리
│    ├── 📄 degree_utils.py              # Degree Sequence 생성 및 stub 보정
│    ├── 📄 average_utils.py             # 앙상블 평균 (NaN 값 안전 처리)
│    ├── 📄 global_utils.py              # CC, APL, DIAM 계산 및  LCC 진단
│    ├── 📄 plot_utils.py                # Degree distribution 시각화 함수
│
└── data_loader_script.py                # 외부 데이터 파일 로더 (외부 파일 → NetworkX)
```

---

# 🧠 핵심 클래스 설명 🧠

###  🟦 `CentralityCalculator`
직접 구현한 네트워크 중심성 계산 클래스 (centrality_generator.py)

| 중심성 | 설명 |
|-------|------|
| Degree | 연결 수 기반 |
| Closeness | 평균 거리 기반 |
| Harmonic | 거리 역수 |
| Betweenness | 최단경로 중개 정도 |
| Eigenvector | 영향력 기반 고유벡터 |

- networkx 대신 **직접 구현된 중심성 알고리즘**
- 비연결 네트워크 자동 예외 처리
- 일부 중심성 계산에서는 연결되지 않은 네트워크 해결을 위해 networkx 내장 함수 사용

#

###  🟥 `RandomNetGenerator`
네 가지 무작위 네트워크 모델 생성 클래스 (random_nets_generator.py)

| 모델 | 목적 | 구현 특징 |
|------|------|-----------|
| ER | 완전 무작위 연결 | p 값 검증, 모든 노드쌍 독립 |
| Configuration | degree 완전 보존 | stub-shuffle, self-loop 및 multi-edge 방지 |
| Chung-Lu | 기대 차수 보존 | pij = ki kj / (2m) 조정 |
| BA | 성장+선호 연결 | m 값 유효성 검사 |

- 본 프로젝트에서는 BA를 미사용 (구현은 되어있음)

---

# 🧰 유틸리티 함수 설명 🧰

### 🔧 `preprocessing.py`
**✔ `preprocess_network(G)`**
- 네트워크의 self-loop 제거 및 중복 edge 제거
- Simple Undirected Network 자동 구성
  
#

### 🔧 `degree_utils.py`
**✔ `create_degree_sequence(G)`** 
- 네트워크의 degree sequence 생성

**✔ `preprocess_stub(degree_list)`**
- stub 총합이 홀수인 경우를 최소 수정하여 짝수화
- Configuration model이 항상 생성 가능하도록 보정

#

### 🔧 `average_utils.py`
**✔ `ensemble_average(list_of_dicts)`**
- 랜덤 네트워크 모델의 결과(딕셔너리 리스트)를 key 단위로 평균
- 모든 등장 key에 대한 평균 수행
- None 및 NaN 자동 제거
- 반환값 : `[mean_CC, mean_APL, mean_DIAM]`

#

### 🔧 `global_utils.py`
**✔ `calculate_global(G)`**
- 연결 여부 자동 확인
- 연결되지 않은 네트워크를 LCC 기반으로 APL(평균 경로 길이), 지름(DIAM) 계산
- 구조 정보 보존을 위해 np.nan 사용
- 반환값 : `{'CC': value, 'APL': value or np.nan, 'DIAM': value or np.nan}`

**✔ `get_largest_connected_component(G)`**
- 네트워크에서 가장 큰 연결 구성요소(LCC)를 반환

**✔ `diagnose_lcc_size(G, generator, p)`**
- 사용된 랜덤 네트워크 모델의 LCC 크기가 원본 대비 너무 작으면 경고 출력

#

### 🔧 `plot_utils.py`
**✔ `plot_degree_hist(ax, original, model_avg, model_name)`**
- 원본 vs 랜덤 네트워크 모델 평균의 Degree Distribution을 한 그래프에 표시
- bar + line 결합형 시각화

**✔ `average_hist(degree_lists, k_max)`**
- 여러 네트워크의 degree histogram을 평균화

---

# 💡 환경 설정 및 실행 방법 💡

### (1) 필수 패키지 설치
**로컬(Python 환경)에서 실행 시**
```
pip install numpy networkx matplotlib scipy
```
**Google Colab에서 실행 시**
```
!pip install numpy networkx matplotlib scipy
```

#

### (2) 프로젝트 클론
**로컬(Python 환경)에서 실행 시**
```
git clone https://github.com/niceholholl/network_project.git
cd network_project
```
**Google Colab에서 실행 시**
```
!git clone https://github.com/niceholholl/network_project.git
%cd network_project
```

#

### (3) Google Drive 데이터 사용 및 작업 디렉토리 설정(선택)
**데이터 파일을 Google Drive에 저장한 경우**
```
from google.colab import drive
drive.mount('/content/drive')

FILE_PATH = '/content/drive/MyDrive/data/friendship/6'
```

```
import os
os.chdir("/content/network_project") 
os.getcwd()       
```
#

### (4) 분석 스크립트 실행
**로컬(Python 환경)에서 실행 시**
```
python network_project_script.py
```
**Google Colab에서 실행 시**
```
!python network_project_script.py
```
> ⚠️ 결과물(PDF 파일들)은 /content/network_project/ 폴더에 저장됩니다.

---

# 📊 핵심 분석 결과 📊

본 프로젝트에서는 우간다 공동체(friendship) 네트워크가  
**랜덤 네트워크 모델로 설명 가능한지**를 평가하기 위해  
ER, Configuration, Chung-Lu 모델과 비교 분석하였다.

#

### 🔹 Degree Distribution
- **ER 모델**은 완전 무작위 분포(Poisson 형태)로, 원본과 매우 다름.
- **Configuration 모델**은 degree를 그대로 보존하므로 가장 정확함.
- **Chung-Lu 모델**은 기대 차수 기반으로 Configuration과 유사한 형태 재현.

→ **결론**: 원본 네트워크는 ER 모델보다 Configuration, Chung-Lu 모델과 구조적으로 더 유사함.```

#

### 🔹 Betweenness
- **랜덤 모델 (ER/CF/CL)**: $C_B \approx 0$ 부근에 극단적으로 집중된 피크만 보여주며, 이는 중개 노드의 역할을 생성하는 데 실패했음을 의미함.

  
- **원본 네트워크**: 히스토그램에서 $0.20$ 및 $0.40$ 근처에 뚜렷한 아웃라이어 막대가 존재하며, 이는 정보 흐름을 통제하는 핵심 병목(Bottleneck) 노드가 존재함을 의미함. (노드 ID별 비교에서도 Original은 랜덤 모델 대비 훨씬 높은 피크를 보임.)

→ **결론**: 랜덤 모델은 원본 네트워크가 가진 구조적 불균일성과 계층적 통제 구조(Bottleneck)를 재현하지 못함.```

### 🔹 Closeness Centrality
- **ER 모델**은 $\mathbf{0.3}$ 근처에 매우 좁고 높은 피크를 형성하며, 모든 노드의 접근성이 유사해지는 비현실적인 균일성을 보임.
- **원본 네트워크**: ER 대비 분포가 훨씬 넓게 퍼져 접근성의 이질성이 큼.

→ **결론**: 모든 랜덤 모델은 원본 네트워크의 복잡하고 계층적인 Centrality 구조를 재현하지 못함.```

### 🔹 Global Metrics
- **Clustering Coefficient (CC)** :
  - 결과: 원본($\approx \mathbf{0.15}$)은 ER 모델($\approx \mathbf{0.07}$)에 비해 약 2배 높은 군집화를 보임
  - 의미: 우간다 공동체 네트워크에는 **무작위 우연으로는 설명되지 않는 강한 지역적 뭉침(파벌)**이 존재함.
- **Average Path Length (APL)** :
  - 결과: 원본 APL($\approx \mathbf{2.49}$)은 ER 모델 APL($\approx \mathbf{2.47}$)과 매우 유사하게 측정됨
  - 의미: 모든 모델이 **Small-World 특징**을 포착하여, APL은 구조적 차이를 구별하는 강력한 지표가 아니었다.
- **Diameter** :
  - 결과: 원본 Diameter($\approx \mathbf{5.00}$)는 ER 모델 Diameter($\approx \mathbf{4.11}$)보다 길게 나타난다.
  -

→ **결론**: 원본 네트워크는 강한 지역적 뭉침(높은 CC)을 가지며, Centrality 구조가 무작위 모델과 근본적으로 다르다.```

---

# ⭐️ 결론 ⭐️

종합하면 우간다 네트워크는…

### ✔ 단순한 무작위 구조(ER)로는 절대 설명되지 않으며
### ✔ degree 기반 모델(CF/CL)이 부분적으로는 유사하지만
### ✔ 중심성 구조(중앙 허브·중개 노드)는 어떤 랜덤 모델도 재현하지 못한다.

**따라서 이 네트워크는**
**공동체의 사회적 규칙·중심 인물·지역적 구조가 결합된 현실적인 사회 네트워크 형태**이며,
**단순 확률 모델 이상의 고차 메커니즘**을 반영한다고 볼 수 있다.

이 패키지는 이러한 구조적 특징을 비교·검증하기 위한
**재사용 가능한 네트워크 분석 도구**로 활용할 수 있다.
