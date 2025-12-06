import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# ---------- 프로젝트 패키지에 필요한 모듈 가져오기 ----------

# 데이터 전처리 함수
from network_tool_pkg.utils.preprocessing import preprocess_network
from network_tool_pkg.utils.degree_utils import create_degree_sequence, preprocess_stub
from network_tool_pkg.utils.average_utils import ensemble_average
from network_tool_pkg.utils.global_utils import calculate_global, get_largest_connected_component, diagnose_lcc_size
from network_tool_pkg.utils.plot_utils import plot_degree_hist, average_hist

# 중심성 및 랜덤 모델 생성 클래스
from network_tool_pkg.analysis.centrality_generator import CentralityCalculator
from network_tool_pkg.analysis.random_nets_generator import RandomNetGenerator

# 데이터 로더 (사용 시 주석 해제)
from data_loader_script import load_network_from_file

# ====================================================================
# 1. 데이터 준비
# ====================================================================

# 🚨 파일 로드 경로 (Google Drive 경로의 Collab 환경 가정, 사용 시 주석 해제)
# FILE_PATH = '/content/drive/MyDrive/data/friendship/6'
# FILE_PATH = "C:/network_pj/network_project/data/friendship/6"

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
ER_P = 0.14
# BA_M = 2 ~ BA 모델 미사용

# ---------- 클래스 인스턴스화 ----------

# 제너레이터 클래스 인스턴스화
print(f"DEBUG N-CHECK 1: 메인 스크립트의 최종 N 값 = {N}") # 👈 N=34가 나와야 함
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
  print(f"DEBUG P-CHECK: 현재 ER_P 값 = {ER_P}")
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
  # er_cls_list.append(calc_er.calculate_closeness_centrality())
  # cf_cls_list.append(calc_cf.calculate_closeness_centrality())
  # cl_cls_list.append(calc_cl.calculate_closeness_centrality())

  # degree 저장
  er_degree_list.append([d for _, d in G_er.degree()])
  cf_degree_list.append([d for _, d in G_cf.degree()])
  cl_degree_list.append([d for _, d in G_cl.degree()])
  
  graph_data_list = [
        (G_er, er_global_list, er_cls_list, calc_er, 'ER'), 
        (G_cf, cf_global_list, cf_cls_list, calc_cf, 'Configuration'), 
        (G_cl, cl_global_list, cl_cls_list, calc_cl, 'Chung-Lu')
    ]
  
      # 1. ER 모델 (LCC 보정 적용)
  try :
      G_er_safe = G_er 
      
      # 🌟 LCC 보정: 단절 확인 후 LCC 추출
      if not nx.is_connected(G_er):
          G_er_safe = get_largest_connected_component(G_er)
          print('[경고] {}/{}번째 ER 그래프가 disconnected이므로 LCC로 보정합니다.'.format(i + 1, NUM_SIMULATIONS))
      

      cls_scores = calc_er.calculate_closeness_centrality() 
      er_cls_list.append(cls_scores) # 유효한 점수를 저장
  
      # 🌟 안전 확인: LCC 추출 후에도 노드가 2개 미만이면 계산 불가
      if G_er_safe.number_of_nodes() < 2:
          raise ValueError("LCC 추출 후 노드 수가 2개 미만이어서 APL/DIAM 계산 불가.")
          
      er_global_list.append(calculate_global(G_er_safe))

  except ValueError : 
      # APL/DIAM 계산 불가 시 안전값(0)으로 대체 (CC는 계산 가능)
      safe_cc = nx.average_clustering(G_er) 
      print('[경고] {}/{}번째 ER 그래프의 APL/DIAM 계산 실패. NaN으로 처리합니다.'.format(i + 1, NUM_SIMULATIONS))
      er_global_list.append({'CC': safe_cc, 'APL': np.nan, 'DIAM': np.nan}) # None 대신 0으로 저장

  # 2. Configuration 모델 (LCC 보정 적용)
  try :
      G_cf_safe = G_cf
      if not nx.is_connected(G_cf):
          G_cf_safe = get_largest_connected_component(G_cf)
          print('[경고] {}/{}번째 CF 그래프가 disconnected이므로 LCC로 보정합니다.'.format(i + 1, NUM_SIMULATIONS))
      
      cls_scores = calc_cf.calculate_closeness_centrality() 
      cf_cls_list.append(cls_scores) # 유효한 점수를 저장

      if G_cf_safe.number_of_nodes() < 2:
          raise ValueError("LCC 추출 후 노드 수가 2개 미만이어서 APL/DIAM 계산 불가.")
          
      cf_global_list.append(calculate_global(G_cf_safe))

  except ValueError : 
      safe_cc = nx.average_clustering(G_cf)
      print('[경고] {}/{}번째 CF 그래프의 APL/DIAM 계산 실패. NaN으로 처리합니다.'.format(i + 1, NUM_SIMULATIONS))
      cf_global_list.append({'CC': safe_cc, 'APL': np.nan, 'DIAM': np.nan}) 


  # 3. Chung-Lu 모델 (LCC 보정 적용)
  try :
      G_cl_safe = G_cl
      if not nx.is_connected(G_cl):
          G_cl_safe = get_largest_connected_component(G_cl)
          print('[경고] {}/{}번째 CL 그래프가 disconnected이므로 LCC로 보정합니다.'.format(i + 1, NUM_SIMULATIONS))
      
      cls_scores = calc_cl.calculate_closeness_centrality() 
      cl_cls_list.append(cls_scores) # 유효한 점수를 저장

      if G_cl_safe.number_of_nodes() < 2:
          raise ValueError("LCC 추출 후 노드 수가 2개 미만이어서 APL/DIAM 계산 불가.")
          
      cl_global_list.append(calculate_global(G_cl_safe))

  except ValueError : 
      safe_cc = nx.average_clustering(G_cl)
      print('[경고] {}/{}번째 CL 그래프의 APL/DIAM 계산 실패. NaN으로 처리합니다.'.format(i + 1, NUM_SIMULATIONS))
      cl_global_list.append({'CC': safe_cc, 'APL': np.nan, 'DIAM': np.nan})

er_avg = ensemble_average(er_global_list)
print(f"DEBUG FINAL-APL: ER 모델 최종 APL 평균 = {er_avg[1]}")
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
diagnose_lcc_size(G_project, generator, ER_P)
# ====================================================================
# 6. 시각화
# ====================================================================

# ---------- 원본 네트워크 vs 랜덤 네트워크 모델 Degree 비교 및 시각화 ----------

k_max_orig = max(degrees_project) if degrees_project else 0 

# 2. 🌟 average_hist 함수 호출 시 k_max_orig 인자를 추가
avg_er_hist = average_hist(er_degree_list, k_max_orig) # 🌟 수정
avg_cf_hist = average_hist(cf_degree_list, k_max_orig) # 🌟 수정
avg_cl_hist = average_hist(cl_degree_list, k_max_orig) # 🌟 수정

fig, ax = plt.subplots(1, 3, figsize = (27, 5))

plot_degree_hist(ax[0], degrees_project, avg_er_hist, 'ER')
plot_degree_hist(ax[1], degrees_project, avg_cf_hist, 'Configuration')
plot_degree_hist(ax[2], degrees_project, avg_cl_hist, 'Chung-Lu')

plt.tight_layout()
plt.savefig('Degree_compare.pdf', bbox_inches = 'tight')
plt.close()

print('----- Degree Histogram 시각화가 완료되었습니다 -----')

# -----------------------------------------------------------
# Betweenness Centrality 비교 및 시각화 (분포 BAR PLOT으로 수정)

# 1. 모든 Betweenness 데이터를 합쳐 공통 Bins 설정
all_btw_scores = original_btw_sorted + avg_er_btw + avg_cf_btw + avg_cl_btw
bins_edges_btw = np.linspace(min(all_btw_scores), max(all_btw_scores), 30)
# 2. 각 모델의 확률 분포 (P(B)) 계산
P_B_original = np.histogram(original_btw_sorted, bins=bins_edges_btw, density=True)[0]
P_B_er_avg = np.histogram(avg_er_btw, bins=bins_edges_btw, density=True)[0]
P_B_cf_avg = np.histogram(avg_cf_btw, bins=bins_edges_btw, density=True)[0]
P_B_cl_avg = np.histogram(avg_cl_btw, bins=bins_edges_btw, density=True)[0]

# 3. X축 위치 및 너비 계산
bin_centers_btw = 0.5 * (bins_edges_btw[:-1] + bins_edges_btw[1:])
bar_width = 0.2 * (bin_centers_btw[1] - bin_centers_btw[0]) # 4개 막대 나열을 위해 조정

fig, ax = plt.subplots(1, 1, figsize = (12, 6))

# 4. 🌟 BAR PLOT으로 분포 비교
ax.bar(bin_centers_btw - bar_width * 1.5, P_B_original, width=bar_width, alpha=0.7, color='grey', label='Original')
ax.bar(bin_centers_btw - bar_width * 0.5, P_B_er_avg, width=bar_width, alpha=0.7, color='blue', label='ER')
ax.bar(bin_centers_btw + bar_width * 0.5, P_B_cf_avg, width=bar_width, alpha=0.7, color='red', label='Configuration')
ax.bar(bin_centers_btw + bar_width * 1.5, P_B_cl_avg, width=bar_width, alpha=0.7, color='green', label='Chung-Lu')

ax.set_title('Betweenness Centrality Distribution Comparison')
ax.set_xlabel('Betweenness Centrality Score')
ax.set_ylabel('Probability Density')
ax.grid(alpha = 0.4)
ax.axvline(x=0, color='grey', linewidth=1.5, linestyle='--')
ax.legend()
plt.tight_layout()
plt.savefig('Betweenness_compare.pdf', bbox_inches = 'tight')
plt.close()

print('----- Betweenness Centrality 시각화가 완료되었습니다 -----')

# -----------------------------------------------------------
# Closeness Centrality 비교 및 시각화 (분포 BAR PLOT으로 수정)

# 1. 모든 Closeness 데이터를 합쳐 공통 Bins 설정
# all_cls_scores = original_cls_sorted + avg_er_cls + avg_cf_cls + avg_cl_cls
# bins_edges_cls = np.linspace(min(all_cls_scores), max(all_cls_scores), 30)
# 1. 앙상블 리스트 평탄화 (리스트의 리스트를 단일 리스트로 만듦)
er_all_cls = [score for dist in er_cls_list for score in dist.values()]
cf_all_cls = [score for dist in cf_cls_list for score in dist.values()]
cl_all_cls = [score for dist in cl_cls_list for score in dist.values()]

# 2. 원본 값 추출 (클래스 인스턴스에서 원본 딕셔너리를 받았으므로)
# original_cls는 딕셔너리이므로 값만 추출
original_cls_values = list(original_cls.values()) 

# 3. 🌟 모든 데이터를 합쳐 최종 범위 설정 리스트 생성
all_cls_scores = original_cls_values + er_all_cls + cf_all_cls + cl_all_cls

min_val = np.min(all_cls_scores) 
max_val = np.max(all_cls_scores)

# 실제 데이터가 0.25에서 0.65 사이에 모두 포함되도록 안전 범위 설정
FIXED_MIN = 0.25
FIXED_MAX = 0.60

# 🌟 min/max 값이 FIXED_MIN/MAX를 벗어나지 않도록 조정
min_range = min(min_val, FIXED_MIN)
max_range = max(max_val, FIXED_MAX)

# bins_edges_cls를 고정된 범위로 재계산
bins_edges_cls = np.linspace(min_range, max_range, 30)

# 2. 각 모델의 확률 분포 (P(C)) 계산
P_C_original = np.histogram(original_cls_sorted, bins=bins_edges_cls, density=True)[0]
P_C_er_avg = np.histogram(avg_er_cls, bins=bins_edges_cls, density=True)[0]
P_C_cf_avg = np.histogram(avg_cf_cls, bins=bins_edges_cls, density=True)[0]
P_C_cl_avg = np.histogram(avg_cl_cls, bins=bins_edges_cls, density=True)[0]

# 3. X축 위치 및 너비 계산
bin_centers_cls = 0.5 * (bins_edges_cls[:-1] + bins_edges_cls[1:])
bar_width = 0.2 * (bin_centers_cls[1] - bin_centers_cls[0]) 

fig, ax = plt.subplots(1, 1, figsize = (12, 6))

# 4. 🌟 BAR PLOT으로 분포 비교
ax.bar(bin_centers_cls - bar_width * 1.5, P_C_original, width=bar_width, alpha=0.7, color='grey', label='Original')
ax.bar(bin_centers_cls - bar_width * 0.5, P_C_er_avg, width=bar_width, alpha=0.7, color='blue', label='ER')
ax.bar(bin_centers_cls + bar_width * 0.5, P_C_cf_avg, width=bar_width, alpha=0.7, color='red', label='Configuration')
ax.bar(bin_centers_cls + bar_width * 1.5, P_C_cl_avg, width=bar_width, alpha=0.7, color='green', label='Chung-Lu')

ax.set_xlim(left=0)
ax.set_title('Closeness Centrality Distribution Comparison')
ax.set_xlabel('Closeness Centrality Score')
ax.set_ylabel('Probability Density')
ax.grid(alpha = 0.4)
ax.legend()
ax.axvline(x=0, color='grey', linewidth=1.5, linestyle='--')
plt.tight_layout()
plt.savefig('Closeness_compare.pdf', bbox_inches = 'tight')
plt.close()

print('----- Closeness Centrality 시각화가 완료되었습니다 -----')

# ---------- 전역 지표 비교 및 시각화 ----------

fig, ax = plt.subplots(1, 3, figsize = (9, 5))

metric_names = list(original_global_metrics.keys())

original_vals = [original_global_metrics[m] for m in metric_names]
er_vals = er_global_metrics
cf_vals = cf_global_metrics
cl_vals = cl_global_metrics

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
