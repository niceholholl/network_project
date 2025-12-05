import networkx as nx

# -------------------- 전역 지표 계산 함수 : CC(클러스터링 계수), APL(평균 경로 길이), DIAM(지름) --------------------
def calculate_global(G) :

  # ---------- 네트워크 유효성 검사 ----------
  
  if not isinstance(G, nx.Graph) :
    raise TypeError('입력한 네트워크의 형태가 올바르지 않습니다. networkx.Graph 형태로 입력하십시오.')

  if len(G.nodes()) <= 1 :
    raise ValueError('전역 지표 계산이 불가합니다. 노드 수가 1 이하입니다.')

  if len(G.edges()) == 0 :
    raise ValueError('전역 지표 계산이 불가합니다. 엣지가 존재하지 않습니다.')

  # ---------- 클러스터링 계수 ----------
  
  cc = nx.average_clustering(G)

  # ---------- 평균 경로 길이, 지름 ----------

  #
