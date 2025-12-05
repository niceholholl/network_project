import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# ---------- 프로젝트 패키지에 필요한 모듈 가져오기 ----------

# 데이터 전처리 함수
from network_tool_pkg.utils.preprocessing import preprocess_network
from network_tool_pkg.utils.degree_utils import create_degree_sequence, preprocess_stub
from network_tool_pkg.utils.average_utils import ensemble_average
from network_tool_pkg.utils.global_utils import calculate_global
from network_tool_pkg.utils.plot_utils import plot_degree_hist, average_hist

# 중심성 및 랜덤 모델 생성 클래스
from network_tool_pkg.analysis.centrality_generator import CentralityCalculator
from network_tool_pkg.analysis.random_nets_generator import RandomNetGenerator

# 데이터 로더 (사용 시 주석 해제)
# from data_loader_script import load_network_from_file

# ====================================================================
# 1. 데이터 준비
# ====================================================================

# 🚨 파일 로드 경로 (Google Drive 경로의 Collab 환경 가정, 사용 시 주석 해제)
# FILE_PATH = '/content/drive/MyDrive/data/friendship/6'

# 🚨 원본 네트워크 로드 (load_network_from_file 함수를 통해 data를 network 형태로 변경 ~ data_loader_script.py 참조)
# G_original = load_network_from_file(FILE_PATH)

# 테스트 및 예시를 위해 karate club network의 데이터를 G_original에 할당 (미사용 시 주석 설정)
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
# BA_M = 2 ~ BA 모델 미사용

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

# 네트워크 특징 비교를 위한 전역 지표 저장 리스트
er_global_list = []
cf_global_list = []
cl_global_list = []

# 네트워크 시각화를 위한 degree 저장 리스트
er_degree_list = []
cf_degree_list = []
cl_degree_list = []

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

  # degree 저장
  er_degree_list.append([d for _, d in G_er.degree()])
  cf_degree_list.append([d for _, d in G_cf.degree()])
  cl_degree_list.append([d for _, d in G_cl.degree()])

  # 전역 지표 계산 및 저장
  # 🚨 예외 처리로 disconnected 체크 및 해당 인덱스 출력
  # 🚨 랜덤 모델 일부 네트워크가 disconnected 되면 일부 전역 지표(APL, DIAM) 계산 불가
  # 🚨 이 값들을 None으로 채우고, 지표의 평균 및 분포 계산시 결과가 흔들릴 수 있음
  
  try :
    er_global_list.append(calculate_global(G_er))
  except ValueError :
    print('[경고] {}/{}번째 ER 그래프가 diconnected 입니다. 평균 경로 길이와 지름은 None으로 대체합니다.'.format(i, NUM_SIMULATIONS))
    er_global_list.append({'CC': nx.average_clustering(G_er), 'APL': None, 'DIAM': None})

  try :
    cf_global_list.append(calculate_global(G_cf))
  except ValueError :
    print('[경고] {}/{}번째 Configuration 그래프가 diconnected 입니다. 평균 경로 길이와 지름은 None으로 대체합니다.'.format(i, NUM_SIMULATIONS))
    cf_global_list.append({'CC': nx.average_clustering(G_cf), 'APL': None, 'DIAM': None})

  try :
    cl_global_list.append(calculate_global(G_cl))
  except ValueError :
    print('[경고] {}/{}번째 Chung-Lu 그래프가 diconnected 입니다. 평균 경로 길이와 지름은 None으로 대체합니다.'.format(i, NUM_SIMULATIONS))
    cl_global_list.append({'CC': nx.average_clustering(G_cl), 'APL': None, 'DIAM': None})

print('----- {}회 앙상블 시뮬레이션 완료 -----'.format(NUM_SIMULATIONS))
print('----- 3단계 : 원본 분포 계산 및 무작위 앙상블 생성이 완료되었습니다 -----')

# ====================================================================
# 4. 중심성 지표 계산 (평균화 작업)
# ====================================================================

nodes_sorted = sorted(G_project.nodes())

# Betweenness Centrality 평균화
original_btw_sorted = np.array([original_btw[n] for n in nodes_sorted])
avg_er_btw = ensemble_average(er_btw_list)
avg_cf_btw = ensemble_average(cf_btw_list)
avg_cl_btw = ensemble_average(cl_btw_list)

# Closeness Centrality 평균화
original_cls_sorted = np.array([original_cls[n] for n in nodes_sorted])
avg_er_cls = ensemble_average(er_cls_list)
avg_cf_cls = ensemble_average(cf_cls_list)
avg_cl_cls = ensemble_average(cl_cls_list)

print('----- 4단계 : 중심성 지표 비교를 위한 앙상블 평균화가 완료되었습니다 -----')

# ====================================================================
# 5. 전역 지표 계산
# ====================================================================

# 원본 네트워크의 전역 지표 계산
original_global_metrics = calculate_global(G_project)

# 랜덤 모델 네트워크의 전역 지표 계산
er_global_metrics = ensemble_average(er_global_list)
cf_global_metrics = ensemble_average(cf_global_list)
cl_global_metrics = ensemble_average(cl_global_list)

print('----- 5단계 : 전역 지표 비교를 위한 계산이 완료되었습니다 -----')

# ====================================================================
# 6. 시각화
# ====================================================================

# ---------- 원본 네트워크 vs 랜덤 네트워크 모델 Degree 비교 및 시각화 ----------

avg_er_hist = average_hist(er_degree_list)
avg_cf_hist = average_hist(cf_degree_list)
avg_cl_hist = average_hist(cl_degree_list)

fig, ax = plt.subplots(1, 3, figsize = (27, 5))

plot_degree_hist(ax[0], degrees_project, avg_er_hist, 'ER')
plot_degree_hist(ax[1], degrees_project, avg_cf_hist, 'Configuration')
plot_degree_hist(ax[2], degrees_project, avg_cl_hist, 'Chung-Lu')

plt.tight_layout()
plt.savefig('Degree_compare.pdf', bbox_inches = 'tight')
plt.close()

print('----- Degree Histogram 시각화가 완료되었습니다 -----')

# ---------- Betweennes Centrality 비교 및 시각화 ----------

fig, ax = plt.subplots(1, 1, figsize = (9, 5))

ax.plot(nodes_sorted, original_btw_sorted, color = 'grey', label = 'Original')
ax.plot(nodes_sorted, avg_er_btw, linestyle = '--', color = 'blue', label = 'ER')
ax.plot(nodes_sorted, avg_cf_btw, linestyle = '--', color = 'red', label = 'Configuration')
ax.plot(nodes_sorted, avg_cl_btw, linestyle = '--', color = 'green', label = 'Chung-Lu')

ax.set_title('Betweenness Centrality: Original vs Random Models')
ax.set_xlabel('Node ID')
ax.set_ylabel('Betweenness Centrality')
ax.grid(alpha = 0.4)
ax.legend()

plt.tight_layout()
plt.savefig('Betweenness_compare.pdf', bbox_inches = 'tight')
plt.close()

print('----- Betweenness Centrality 시각화가 완료되었습니다 -----')

# ---------- Closeness Centrality 비교 및 시각화 ----------

fig, ax = plt.subplots(1, 1, figsize = (9, 5))

ax.plot(nodes_sorted, original_cls_sorted, color = 'grey', label = 'Original')
ax.plot(nodes_sorted, avg_er_cls, linestyle = '--', color = 'blue', label = 'ER')
ax.plot(nodes_sorted, avg_cf_cls, linestyle = '--', color = 'red', label = 'Configuration')
ax.plot(nodes_sorted, avg_cl_cls, linestyle = '--', color = 'green', label = 'Chung-Lu')

ax.set_title('Closeness Centrality: Original vs Random Models')
ax.set_xlabel('Node ID')
ax.set_ylabel('Closeness Centrality')
ax.grid(alpha = 0.4)
ax.legend()

plt.tight_layout()
plt.savefig('Closeness_compare.pdf', bbox_inches = 'tight')
plt.close()

print('----- Closeness Centrality 시각화가 완료되었습니다 -----')

# ---------- 전역 지표 비교 및 시각화 ----------

fig, ax = plt.subplots(1, 3, figsize = (9, 5))

metric_names = list(original_global_metrics.keys())

original_vals = [original_global_metrics[m] for m in metric_names]
er_vals = [er_global_metrics[m] for m in metric_names]
cf_vals = [cf_global_metrics[m] for m in metric_names]
cl_vals = [cl_global_metrics[m] for m in metric_names]

models = ['Original', 'ER', 'Config', 'Chung-Lu']
colors = ['black', 'blue', 'red', 'green']
x_single = 0

for i, metric in enumerate(metric_names) :
  x_pos = np.arange(len(models))
  y_vals = [original_vals[i], er_vals[i], cf_vals[i], cl_vals[i]]

  for j, (x,y) in enumerate(zip(x_pos, y_vals)) :
    ax[i].scatter(x, y, color = colors[j], s = 120)
    ax[i].text(x, y, '{:.2f}'.format(y), ha = 'center', va = 'center', fontsize = 6, color = 'white')

  ax[i].set_xticks(x_pos)
  ax[i].set_xticklabels(models, rotation = 20)
  ax[i].set_ylabel('{} value'.format(metric))
  ax[i].set_title('{} Comparison'.format(metric))
  ax[i].grid(alpha = 0.4)

plt.tight_layout()
plt.savefig('Global_compare.pdf', bbox_inches = 'tight')
plt.close()

print('----- 전역 지표(클러스터링 계수, 평균 경로 길이, 지름) 시각화가 완료되었습니다 -----')
print('----- 6단계 : 해당 프로젝트의 최종 시각화가 완료되었습니다 -----')

    







            







