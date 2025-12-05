import networkx as nx
import numpy as np
import random
import itertools

# -------------------- 네트워크에 대해 다양한 랜덤 모델을 생성하는 클래스 --------------------

class RandomNetGenerator:

  # ---------- 클래스 속성 설정 ----------

  def __init__(self, N_nodes, initial_degrees):
    
    self.N = N_nodes
    self.degrees = initial_degrees # Configuration/Chung-Lu에 필요
    self.total_degree = sum(initial_degrees) if initial_degrees else 0

  # ---------- 보조 메서드 (선호적 연결 대상 선택, BA 모델) ----------

  def choose_target_node(self, existing_nodes, graph) :

    degrees = [graph.degree(n) for n in existing_nodes]
    total_degree = sum(degrees)

    if total_degree == 0 :
      return random.choice(existing_nodes)

    probs = [d / total_degree for d in degrees]
    
    cumulative_weights = []
    cum_sum = 0

    for w in probs :
      cum_sum += w
      cumulative_weights.append(cum_sum)

    total = sum(probs)
    r = random.uniform(0, total)
    
    for i, cw in enumerate(cumulative_weights) :

      if r <= cw :
        return existing_nodes[i]

    return existing_nodes[-1]
        
  # ====================================================================
  # 1. ER Model (G(N, p)) 구현
  # ====================================================================
    
  def create_er_net(self, p) :

    # ---------- 확률 p 검증 (예외 처리)  ----------

    if not (0 <= p <= 1) :
      raise ValueError(f"Error: {p}가 0과 1 사이 값이 아닙니다.")
            
    G_er = nx.Graph()
    G_er.add_nodes_from(range(self.N))

    # ---------- itertools.combinations를 사용하여 모든 가능한 노드쌍을 효율적으로 탐색 ---------
        
    for i, j in itertools.combinations(G_er.nodes, 2):
      if random.random() < p:
        G_er.add_edge(i, j)
                
    return G_er

  # ====================================================================
  # 2. Configuration Model 구현
  # ====================================================================
      
  def create_configuration_net(self) :

    degree_sequence = self.degrees
    ERR_MENT = 'network_pkg.utils.degree_utils.create_degree_sequence()로 전처리를 먼저 실행하십시오.'

    # ---------- degree sequence 검증 (예외 처리)  ----------

    if not isinstance(degree_sequence, list) :
      raise TypeError('입력한 degree sequence의 형태가 올바르지 않습니다. ' + ERR_MENT)

    if len(degree_sequence) == 0 :
      raise ValueError('입력한 degree sequence는 빈 list 입니다. ' + ERR_MENT)

    for degree in degree_sequence :
      if not isinstance(degree, int) :
        raise ValueError('입력한 degree sequence에는 정수 형태만 포함되어야합니다. ' + ERR_MENT)
      
      if degree < 0 :
        raise ValueError('입력한 degree sequence에 음수 degree가 포함되어 있습니다. ' + ERR_MENT)

    # ---------- stub list 생성 ----------

    stub_list = []

    for node, degree in enumerate(degree_sequence) :
      stub_list.extend([node] * degree)

    if len(stub_list) % 2 == 1 :
      raise ValueError('stub의 합({})이 홀수입니다. '.format(len(stub_list)) + ERR_MENT)

    # ---------- stub list 무작위화 ----------

    random.shuffle(stub_list)

    # ---------- Configuration 그래프 생성 및 노드 추가 ----------

    G_config = nx.MultiGraph()
    G_config.add_nodes_from(range(self.N))
    
    while len(stub_list) > 1 :
      node1 = stub_list.pop()
      node2 = stub_list.pop()

      if node1 != node2 :
        G_config.add_edge(node1, node2)
      else :
        pass

    # ---------- MultiGraph로 생성한 configuraion 모델을 simple graph로 변경 ----------

    return nx.Graph(G_config)
    
  # ====================================================================
  # 3. Chung-Lu Model 구현
  # ====================================================================
  
  def create_chunglu_net(self) :

    degree_sequence = self.degrees
    n = len(degree_sequence)

    G_chu = nx.Graph()
    G_chu.add_nodes_from(range(n))

    total_degree = sum(degree_sequence)

    if total_degree == 0 :
      raise ValueError('데이터 오류입니다. 올바른 네트워크를 사용하세요.)
                       
    for i in range(n) :
      for j in range(i+1, n) :
        p_ij = (degree_sequence[i] * degree_sequence[j]) / total_degree

        if p_ij > 1 :
          p_ij = (degree_sequence[i] * degree_sequence[j]) / (max(degree_sequence) ** 2)

        p_ij = max(0, min(1, p_ij))

        if random.random() < p_ij :
          G_chu.add_edge(i, j)

    return G_chu
  
  # ====================================================================
  # 4. BA Model 구현
  # ====================================================================
    
  def create_ba_net(self, m) :

    m0 = 5

    # ---------- m 값 검증 (예외 처리) ----------

    if not isinstance(m, int) :
      raise TypeError('BA 모델의 새로운 엣지 수 m은 정수 형태여야 합니다.')

    if m < 1 :
      raise ValueError('BA 모델의 새로운 엣지 수 m은 1 이상의 정수여야 합니다. 현재 m 값 = {}'.format(m))
    
    if m > m0 :
      raise ValueError('BA 모델의 새로운 엣지 수 m은 초기 노드 수로 설정된 5보다 클 수 없습니다. 현재 m 값 = {}'.format(m))

    # ---------- 초기 그래프 및 노드 설정 ----------

    G_ba = nx.complete_graph(m0)
    next_node = m0
    n_total = self.N

    # ---------- 성장 + 선호적 연결 루프 ----------

    while next_node < n_total :
      targets = set()

      while len(targets) < m :
        chosen = self.choose_target_node(list(G_ba.nodes()), G_ba)

        if chosen not in targets :
          targets.add(chosen)

      G_ba.add_node(next_node)

      for target in targets :
        G_ba.add_edge(next_node, target)

      next_node += 1

    return G_ba
