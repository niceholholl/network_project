import networkx as nx
from network_tool_pkg.analysis.centrality_generator import CentralityCalculator
from network_tool_pkg.analysis.random_nets_generator import RandomNetGenerator

# -------------------- 전역 지표 계산 함수 : CC(클러스터링 계수), APL(평균 경로 길이), DIAM(지름) --------------------
def calculate_global(G) :

  # ---------- 네트워크 유효성 검사 ----------
  
  if not isinstance(G, nx.Graph) :
    raise TypeError('입력한 네트워크의 형태가 올바르지 않습니다. networkx.Graph 형태로 입력하십시오.')

  if len(G.nodes()) <= 1 :
    raise ValueError('전역 지표 계산이 불가능합니다. 노드 수가 1 이하입니다.')

  if len(G.edges()) == 0 :
    raise ValueError('전역 지표 계산이 불가능합니다. 엣지가 존재하지 않습니다.')

  if not nx.is_connected(G) :
    raise ValueError('입력한 네트워크의 형태가 connected graph가 아닙니다. 평균 경로 길이 및 지름 계산이 불가능합니다.')

  # ---------- 전역 지표 생성 ----------

  # 클러스터링 계수
  cc = nx.average_clustering(G)
  
  # 평균 경로 길이
  apl = nx.average_shortest_path_length(G)

  # 지름
  diam = nx.diameter(G)
  return {'CC' : cc, 'APL' : apl, 'DIAM' : diam}


# -------------------- 주어진 그래프에서 가장 큰 연결 구성요소 (LCC) 추출하여 반환 ---------------
def get_largest_connected_component(G):
    # 1. 모든 연결 구성요소 찾음 
    # nx.connected_components : 각 구성요소의 노드 집합을 반환하는 generator
    components = nx.connected_components(G)
    
    # 2. key=len을 사용하여 길이가 가장 긴(노드가 많은) 구성요소를 찾음 
    largest_component_nodes = max(components, key=len)
    
    # 3. 해당 노드들로 서브그래프를 만들고 복사본을 반환
    G_lcc = G.subgraph(largest_component_nodes).copy()
    
    return G_lcc

# -------------------- LCC 노드 수 진단 함수 --------------------
def diagnose_lcc_size(G_original, generator, ER_P):
    N_REF = G_original.number_of_nodes()
    G_er = generator.create_er_net(ER_P)
    G_config = generator.create_configuration_net()
    G_chunglu = generator.create_chunglu_net()
  
    # Original LCC
    LCC_original = get_largest_connected_component(G_original)
    N_original_lcc = len(LCC_original.nodes())
    
    # ER LCC
    LCC_er = get_largest_connected_component(G_er)
    N_er_lcc = len(LCC_er.nodes())
    
    # Configuration LCC
    LCC_config = get_largest_connected_component(G_config)
    N_config_lcc = len(LCC_config.nodes())
    
    # Chung-Lu LCC
    LCC_chunglu = get_largest_connected_component(G_chunglu)
    N_chunglu_lcc = len(LCC_chunglu.nodes())

    print("\n--- 🔬 LCC 노드 수 진단 결과 (총 노드: {}) ---".format(N_REF))
    print(f"Original LCC 노드 수: {N_original_lcc}")
    print(f"ER LCC 노드 수: {N_er_lcc}")
    print(f"Config LCC 노드 수: {N_config_lcc}")
    print(f"Chung-Lu LCC 노드 수: {N_chunglu_lcc}")
    print("---------------------------------------------")

    # 진단 결과를 바탕으로 경고 메시지 출력
    if N_er_lcc < 0.8 * 139: # 80% 미만으로 임계값 설정
        print(f"⚠️ 경고: ER LCC({N_er_lcc})가 원본 대비 매우 작습니다. APL/DIAM 값이 비정상일 수 있습니다.")
    
    if N_config_lcc < 0.8 * 139:
        print(f"⚠️ 경고: Config LCC({N_config_lcc})가 원본 대비 매우 작습니다. APL/DIAM 값이 비정상일 수 있습니다.")

    if N_chunglu_lcc < 0.8 * 139:
        print(f"⚠️ 경고: Chung-Lu LCC({N_chunglu_lcc})가 원본 대비 매우 작습니다. APL/DIAM 값이 비정상일 수 있습니다.")

    return N_original_lcc, N_er_lcc, N_config_lcc, N_chunglu_lcc