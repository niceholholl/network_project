import networkx as nx
import random
import numpy as np
import itertools

class RandomNetGenerator:
    """
    ER, Configuration, Chung-Lu 모델을 생성하는 클래스
    """
    def __init__(self, N_nodes, initial_degrees):
        # 프로젝트 공통 속성 초기화
        self.N = N_nodes
        self.degrees = initial_degrees # Configuration/Chung-Lu에 필요
        self.total_degree = sum(initial_degrees) if initial_degrees else 0
        
    # ====================================================================
    # 1. ER Model (G(N, p)) 구현
    # ====================================================================
    def create_er_net(self, p):
        if not (0 <= p <= 1):
            raise ValueError(f"Error: {p}가 0과 1 사이 값이 아닙니다.")
            
        G_er = nx.Graph()
        G_er.add_nodes_from(range(self.N))
        
        for i, j in itertools.combinations(G_er.nodes, 2):
            if random.random() < p:
                G_er.add_edge(i, j)
                
        return G_er

    # ====================================================================
    # 2. Configuration Model 구현 (G(N, k))
    # ====================================================================


    # ====================================================================
    # 3. Chung-Lu Model 구현
    # ====================================================================
  
        return chung_lu_net

