import networkx as nx

# -------------------- 네트워크 전처리 함수 : 원본 네트워크를 랜덤 모델 생성 및 분석에 용이하도록 변경해주는 함수 --------------------
def preprocess_network(G) :

  # ---------- 전처리 이전 네트워크 타입 확인 (예외 처리) ----------

  if not isinstance(G, nx.Graph) :
    raise TypeError('입력한 네트워크의 형태가 올바르지 않습니다. networkx.Graph 형태로 입력하십시오.')

  if len(G.nodes()) == 0 :
    raise ValueError('입력한 네트워크는 빈 그래프입니다. 다른 네트워크를 입력하십시오.')

  if len(G.edges()) == 0 :
    raise ValueError('입력한 네트워크는 엣지가 존재하지 않습니다. 전처리 및 랜덤 모델 생성이 불가능합니다.')

  # ---------- simple network 생성 ----------

  clean_G = nx.Graph()
  clean_G.add_nodes_from(G.nodes())

  # ---------- self-loop 제거 및 multi-edge 중복 삭제 ----------

  for node1, node2 in G.edges() :

    if node1 == node2 :
      print('[network preprocessing] self-loop 발견 : ({}, {}) → 제거'.format(node1, node2))
      continue

    if clean_G.has_edge(node1, node2) :
      print('[network preprocessing] multi-edge 발견 : ({}, {}) → 중복 제거'.format(node1, node2))
      continue

    clean_G.add_edge(node1, node2)

  # ---------- 고립 노드 제거 ----------

  isolated_nodes = []

  for node in clean_G.nodes() :

    if clean_G.degree(node) == 0 :
      isolated_nodes.append(node)

  if len(isolated_nodes) > 0 :
    print('[network preprocessing] isolated node 발견 : {} → 제거'.format(isolated_nodes))

    for node_isol in isolated_nodes :
      clean_G.remove_node(node_isol)

  # ---------- 전처리 이후 네트워크 타입 확인 (예외 처리) ----------

  if len(clean_G.nodes()) <= 1 :
    raise ValueError('전처리 이후 네트워크의 노드가 1개 이하입니다. 네트워크 분석 및 랜덤 모델 생성이 불가능합니다.')

  return clean_G
