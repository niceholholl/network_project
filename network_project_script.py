import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# ---------- 프로젝트 패키지에 필요한 모듈 가져오기 ----------

# 데이터 전처리 함수
from network_tool_pkg.utils.preprocessing import preprocess_network
from network_tool_pkg.utils.degree_utils import create_degree_sequence, preprocess_stub
from network_tool_pkg.utils.average_utils import average_centrality

# 중심성 및 랜덤 모델 생성 클래스
from network_tool_pkg.analysis.centrality_generator import CentralityCalculator
from network_tool_pkg.analysis.radom_nets_generator import RandomNetGenerator

# ====================================================================
# 1. 데이터 준비
# ====================================================================

# 🚨 파일 로드 경로 (Google Drive 경로의 Collab 환경 가정)
# FILE_PATH = '/content/drive/MyDrive/data/friendship/6'

# 🚨 원본 네트워크 로드 (load_network_from_file 함수를 통해 data를 network 형태로 변경 ~ data_loader_script.py 참조)
# G_original = load_network_from_file(FILE_PATH)

# 테스트 및 예시를 위해 karate club network의 데이터를 G_original에 할당
G_original = nx.karate_club_graph()

# ---------- 데이터 전처리 실행 ----------

# 네트워크 전처리
G_project = preprocess_network(G_original)

# degree sequence 전처리
degrees = create_degree_sequence(G_project)

# degree sequence 보정 (stub 합 짝수 보정)
degrees_project = preprocess_stub(degrees)

print('----- 1단계 : 데이터 전처리가 완료되었습니다 -----')

# ====================================================================
# 2. 제너레이터 설정
# ====================================================================

N = G_project.number_of_nodes()
NUM_SIMULATIONS = 100 
ER_P = 0.08
BA_M = 2

# ---------- 클래스 인스턴스화 ----------

# 제너레이터 클래스 인스턴스화
generator = RandomNetGenerator(N_nodes = N, initial_degrees = degrees_project)

# 중심성 계산 클래스 인스턴스화
original_calc = CentralityCalculator(G_project)

print('----- 2단계 : 랜덤 모델 생성기의 설정이 완료되었습니다 -----')

# ====================================================================
# 3. 원본 분포 계산 및 무작위 앙상블 생성
# ====================================================================

# ---------- 원본 네트워크의 Centrality 계산 ----------

# 🚨 해당 분석에서는 Betweenness Centrality와 Closeness Centrality 두 개를 이용하여 비교
original_btw = original_calc.calculate_betweenness_centrality()
original_cls = original_calc.calculate_closeness_centrality()

# ---------- 앙상블 시뮬레이션 초기화 ----------

# 🚨 해당 분석에서는 BA 모델을 제외한 나머지 세 개만을 비교
# Betweenness Centrality 저장 리스트
er_btw_list = []
cf_btw_list = []
cl_btw_list = []

# Closeness Centrality 저장 리스트
er_cls_list = []
cf_cls_list = []
cl_cls_list = []

# ---------- 앙상블 시뮬레이션 시작 ----------

print('----- {}회 앙상블 시뮬레이션 시작 -----'.format(NUM_SIMULATIONS))

for i in range(NUM_SIMULATIONS) :

  # 모델 생성
  G_er = generator.create_er_net(ER_P)
  G_cf = generator.create_configuration_net()
  G_cl = generator.create_chunglu_net()

  # 각 모델의 계산기 인스턴스
  calc_er = CentralityCalculator(G_er)
  calc_cf = CentralityCalculator(G_cf)
  calc_cl = CentralityCalculator(G_cl)

  # Betweenness Centrality 계산 및 저장
  er_btw_list.append(calc_er.calculate_betweenness_centrality())
  cf_btw_list.append(calc_cf.calculate_betweenness_centrality())
  cl_btw_list.append(calc_cl.calculate_betweenness_centrality())

  # Closeness Centrality 계산 및 저장
  er_cls_list.append(calc_er.calculate_closeness_centrality())
  cf_cls_list.append(calc_cf.calculate_closeness_centrality())
  cl_cls_list.append(calc_cl.calculate_closeness_centrality())

print('----- {}회 앙상블 시뮬레이션 완료 -----'.format(NUM_SIMULATIONS))
print('----- 3단계 : 원본 분포 계산 및 무작위 앙상블 생성이 완료되었습니다 -----')

# ====================================================================
# 4. 중심성 지표 비교 (평균화 작업)
# ====================================================================

nodes_sorted = sorted(G_project.nodes())

# Betweenness Centrality 평균화
original_btw_sorted = np.array([original_btw[n] for n in nodes_sorted])
avg_er_btw = average_centrality(er_btw_list)
avg_cf_btw = average_centrality(cf_btw_list)
avg_cl_btw = average_centrality(cl_btw_list)

# Closeness Centrality 평균화
original_cls_sorted = np.array([original_cls[n] for n in nodes_sorted])
avg_er_cls = average_centrality(er_cls_list)
avg_cf_cls = average_centrality(cf_cls_list)
avg_cl_cls = average_centrality(cl_cls_list)

print('----- 4단계 : 중심성 지표 비교를 위한 앙상블 평균화가 완료되었습니다 -----')

# ====================================================================
# 5. 시각화
# ====================================================================

# --------------------------------------------------------------------
# 🌟 (이후 Closeness, Betweenness Centrality 비교 플롯 추가)

