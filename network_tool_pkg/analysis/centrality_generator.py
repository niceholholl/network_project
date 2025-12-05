import networkx as nx
import numpy as np

# -------------------- 네트워크에 대해 직접 구현된 다양한 중심성 지표를 계산하는 클래스 --------------------

class CentralityCalculator :

  # ---------- 클래스 속성 설정 ----------

  def __init__(self, G) :

    if not isinstance(G, nx.Graph) :
      raise TypeError('입력한 네트워크의 형태가 올바르지 않습니다. networkx.Graph 형태로 입력하십시오.')

    if len(G.nodes()) == 0 :
      raise ValueError('입력한 네트워크는 빈 그래프입니다. 다른 네트워크를 입력하십시오.')

    if len(G.edges()) == 0 :
      raise ValueError('입력한 네트워크는 엣지가 존재하지 않습니다. 중심성 지표를 계산할 수 없습니다.')
    
    self.G = G
    self.N = len(G.nodes())
    self.nodes = list(G.nodes())

  # ---------- 보조 메서드 (인접 행렬) ----------

  def get_adjacency_matrix(self) :

    N = self.N
    A = np.zeros((N,N))
    node_to_index = {node: i for i, node in enumerate(self.nodes)}

    for i, n in enumerate(self.nodes) :
      for nhb in self.G.neighbors(n) :
        j = node_to_index[nhb]
        A[i][j] = 1

    return A

  # ---------- Degree Centrality ----------

  def calculate_degree_centrality(self) :
    
    N = self.N
    d_cen = {}

    if N <= 1 :
      raise ValueError('degree centrality를 계산할 수 없습니다. 네트워크의 노드가 2개 이상이어야 합니다. 현재 노드 수 = {}'.format(N))

    for n in self.G.nodes() :
      d = len(self.G[n])
      d_cen[n] = (d/(N-1))

    return d_cen

  # ---------- Closeness Centrality ----------

  def calculate_closeness_centrality(self) :

    N = self.N
    c_cen = {}

    if N <= 1 :
      raise ValueError('closeness centrality를 계산할 수 없습니다. 네트워크의 노드가 2개 이상이어야 합니다. 현재 노드 수 = {}'.format(N))

    try :
      shortdic = dict(nx.shortest_path(self.G))
      
    except nx.NetworkXNoPath : 
      # shortest_path 내장 함수 사용에 있어 disconnected network 발생 시 networkx 내장 함수 사용으로 안전하게 처리
      return nx.closeness_centrality(self.G)

    for n in self.G.nodes() :

      dist_sum = 0
      reachable_count = 0

      for m in self.G.nodes() :
        if n == m :
          continue

        try :
          dist = len(shortdic[n][m]) - 1
          dist_sum += dist
          reachable_count += 1
          
        except KeyError :
          # shortest_path 내장 함수 사용에 있어 disconnected network 발생 시 networkx 내장 함수 사용으로 안전하게 처리
          return nx.closeness_centrality(self.G)

      c_cen[n] = reachable_count / dist_sum

    return c_cen
    
  # ---------- Harmonic Centrality ----------

  def calculate_harmonic_centrality(self) :

    N = self.N
    h_cen = {}

    if N <= 1 :
      raise ValueError('harmonic centrality를 계산할 수 없습니다. 네트워크의 노드가 2개 이상이어야 합니다. 현재 노드 수 = {}'.format(N))

    try : 
      shortdic = dict(nx.shortest_path(self.G))
      
    except nx.NetworkXNoPath :
      # shortest_path 내장 함수 사용에 있어 disconnected network 발생 시 networkx 내장 함수 사용으로 안전하게 처리
      return nx.harmonic_centrality(self.G)

    for n in self.G.nodes() :
      
      h_sum = 0
      reachable_count = 0

      for m in self.G.nodes() :
        if n == m :
          continue

        try :
          dist = len(shortdic[n][m]) - 1
          
        except KeyError :
          # shortest_path 내장 함수 사용에 있어 disconnected network 발생 시 networkx 내장 함수 사용으로 안전하게 처리
          return nx.harmonic_centrality(self.G)

        if dist > 0 :
          h_sum += 1 / dist
          reachable_count += 1

      h_cen[n] = h_sum / (N-1)

    return h_cen

  # ---------- Betweenness Centrality ----------

  def calculate_betweenness_centrality(self) :

    N = self.N
    nodes = self.nodes
    normalizer = 1/((N-1)*(N-2))
    b_cen = {n : 0 for n in nodes}    

    if N <= 2 :
      raise ValueError('betweenness centrality를 계산할 수 없습니다. 네트워크의 노드가 3개 이상이어야 합니다. 현재 노드 수 = {}'.format(N))


    for source in nodes :
      for target in nodes :
        if source == target :
          continue

        try :
          paths = list(nx.all_shortest_paths(self.G, source, target))
          
        except nx.NetworkXNoPath :
          # all_shortest_paths 내장 함수 사용에 있어 disconnected network 발생 시 networkx 내장 함수 사용으로 안전하게 처리
          return nx.betweenness_centrality(self.G)

        if not paths :
          continue

        for path in paths :
          for n in path[1:-1]:
            b_cen[n] += 1/len(paths)

    for node in nodes :
          b_cen[node] *= normalizer

    return b_cen

  # ---------- Eigenvector Centrality ----------

  def calculate_eigenvector_centrality(self, max_iter = 100, tol = 1e-6) :

    nodes = self.nodes
    iter_count = 0
    old_cen = {n : 1 for n in nodes}

    while iter_count < max_iter :
      new_cen = {}

      for n in nodes :
        s = 0
        
        for nhb in self.G.neighbors(n) :
          s += old_cen[nhb]

        new_cen[n] = s

      norm = sum(v**2 for v in new_cen.values()) ** 0.5

      if norm == 0 :
        return {n : 0 for n in nodes}

      new_cen = {n : (val/norm) for n, val in new_cen.items()}

      threshold = max(abs(new_cen[n] - old_cen[n]) for n in nodes)

      if threshold < tol :
        break

      old_cen = new_cen
      iter_count += 1

    return new_cen

  # ---------- Eigenvector Centrality (matrix) ----------

  def calculate_eigenvector_centrality_matrix(self, max_iter = 100, tol = 1e-6) :

    N = self.N
    nodes = self.nodes
    iter_count = 0
    old_cen = np.ones(N)
    A = self.get_adjacency_matrix()

    while iter_count < max_iter :
      new_cen = A @ old_cen

      norm_value = np.sqrt(np.sum(new_cen**2))

      if norm_value == 0 :
        new_cen = np.zeros(N)
        break

      new_cen = new_cen / norm_value

      threshold = np.max(np.abs(new_cen - old_cen))

      if threshold < tol :
        break

      old_cen = new_cen
      iter_count += 1

    return new_cen
