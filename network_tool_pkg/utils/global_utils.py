import networkx as nx
import numpy as np

# LCC 상태 진단을 위해 해당 모듈을 불러옴
from network_tool_pkg.analysis.centrality_generator import CentralityCalculator
from network_tool_pkg.analysis.random_nets_generator import RandomNetGenerator

# -------------------- 주어진 그래프에서 가장 큰 연결 구성요소 (LCC) 추출하여 반환 ---------------
def get_largest_connected_component(G):

  if G.number_of_nodes() == 0 :
    return G

  # ---------- LCC 만들기 ----------
  
  # nx.connected_components 이용 : 각 구성요소의 노드 집합을 반환하는 generator
  
  components = nx.connected_components(G)
  largest_component_nodes = max(components, key=len)
  
  return G.subgraph(largest_component_nodes).copy()
  




# -------------------- 전역 지표 계산 함수 : CC(클러스터링 계수), APL(평균 경로 길이), DIAM(지름) --------------------
def calculate_global(G) :

  # ---------- 네트워크 유효성 검사 ----------
  
  if not isinstance(G, nx.Graph) :
    raise TypeError('입력한 네트워크의 형태가 올바르지 않습니다. networkx.Graph 형태로 입력하십시오.')

  if G.number_of_nodes() == 0:
    return {'CC' : np.nan, 'APL' : np.nan, 'DIAM' : np.nan}

  # ---------- 전역 지표 생성 : CC ----------

  # 클러스터링 계수 ~ connected 상관없이 반환 가능
  cc = nx.average_clustering(G)

  # ---------- 네트워크 Connected 여부 판단 ----------

  if nx.is_connected(G) :
    apl = nx.average_shortest_path_length(G)
    diam = nx.diameter(G)
    return {'CC' : cc, 'APL' : apl, 'DIAM' : diam}

  # ---------- Disonnected 네트워크에서는 LCC 사용 ----------
  
  G_lcc = get_largest_connected_component(G)

  if G_lcc.number_of_nodes() <= 1 :
    return {"CC": cc, "APL": np.nan, "DIAM": np.nan}

  if G_lcc.number_of_edges() == 0 :
    return {"CC": cc, "APL": np.nan, "DIAM": np.nan}

  apl = nx.average_shortest_path_length(G_lcc)
  diam = nx.diameter(G_lcc)

  return {'CC' : cc, 'APL' : apl, 'DIAM' : diam}





# -------------------- LCC 노드 수 진단 함수 --------------------
def diagnose_lcc_size(G_original, generator, ER_P) :
  
  N_origin = G_original.number_of_nodes()

  nets = {'Original' : G_original, 
          'ER' : generator.create_er_net(ER_P), 
          'Configuration' : generator.create_configuration_net(),
          'Chung-Lu' : generator.create_chunglu_net()}

  print("\n--- 🔬 LCC 노드 수 진단 결과 (총 노드 : {}) ---".format(N_origin))

  lcc_sizes = {}
  
  for name, G in nets.items() :
    LCC = get_largest_connected_component(G)
    size = LCC.number_of_nodes()
    lcc_sizes[name] = size
    
    print('{} LCC 노드 수 : {}'.format(name, size))

  print('------------------------------------------')

  # ---------- 원본 대비 지나치게 작은 경우 경고 ----------
  
  for name in ["ER", "Configuration", "Chung-Lu"] :
    if lcc_sizes[name] < 0.8 * N_origin :
      print('{} 모델의 LCC({})가 원본 대비 매우 작습니다. APL과 DIAM 값이 비정상일 수 있습니다.'.format(name, lcc_sizes[name]))

  return(lcc_sizes['Original'], lcc_sizes['ER'], lcc_sizes['Configuration'], lcc_sizes['Chung-Lu'])
    



            
# -------------------- 네트워크 그래프 기초통계 함수 --------------------
def basic_network_stats(G) :
  
  stats = {}

  # ---------- 기본 정보 ----------

  num_nodes = G.number_of_nodes()
  num_edges = G.number_of_edges()
  
  stats['num_nodes'] = G.number_of_nodes()
  stats['num_edges'] = G.number_of_edges()

  # ---------- Degree 정보 ----------
  
  degrees = [d for n, d in G.degree()]

  if degrees :      
    stats['degree_average'] = round(np.mean(degrees), 3)
    stats['degree_max'] = int(np.max(degrees))
    stats['degree_min'] = int(np.min(degrees))

  else :
    stats['degree_average'] = None
    stats['degree_max'] = None
    stats['degree_min'] = None 

  # ---------- Density 정보 ----------
  
  stats['density'] = round(nx.density(G), 3)

  # ---------- 연결 구성요소 정보 ----------

  if num_nodes == 0 :
    stats['num_connected_components'] = 0
    stats['largest_cc_size'] = 0
    stats['average_shortest_path_length'] = None
    stats['diameter'] = None
    stats['average_clustering'] = None
    return stats

  components = list(nx.connected_components(G))
  stats['num_connected_components'] = len(components)

  largest_cc_nodes = max(components, key = len)
  stats['largest_cc_size'] = len(largest_cc_nodes)

  # ---------- LCC 기반 경로 길이 및 지름 정보 ----------
    
  G_lcc = G.subgraph(largest_cc_nodes).copy()

  if G_lcc.number_of_nodes() > 1 and G_lcc.number_of_edges() > 0 :
    stats['average_shortest_path_length'] = round(nx.average_shortest_path_length(G_lcc), 3)
    stats['diameter'] = nx.diameter(G_lcc)

  else :
    stats['average_shortest_path_length'] = None
    stats['diameter'] = None

  # ---------- 클러스터링 계수 ----------

  try :
    stats['average_clustering'] = round(nx.average_clustering(G), 3)

  except Exception :
    stats['average_clustering'] = None
  
  return stats  
