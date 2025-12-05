import networkx as nx

# -------------------- 전역 지표 계산 함수 : CC(클러스터링 계수), APL(평균 경로 길이), DIAM(지름) --------------------
def calculate_global(G) :

  # ---------- 네트워크 유효성 검사 ----------
  if not isinstance(G, nx.Graph) :
    raise TypeError('입력한 네트워크는 networkx.Graph 형태여야 합니다')
