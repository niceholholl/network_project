import networkx as nx

# -------------------- 파일을 로드하여 네트워크 생성하는 함수 --------------------
def load_network_from_file(file_path) :

  # 🚨 파일 형식 : 각 줄이 'nodeA,nodeB' 형식으로 이루어진 경우에만 사용 가능
  # 🚨 프로젝트에 사용한 Ugandan friendship에 해당하는 'householdA,householdB'로 노드 이름을 변경

  G_load = nx.Graph()
  node_dict = {}
  idx = 1

  # ---------- 파일 형식에 맞춰 네트워크로 변경 (예외 처리) ----------
  
  try :
    with open(file_path, 'r') as f :
      lines = f.read().strip().split('\n')

    for line in lines :
      node_a, node_b = line.split(',')

      # ---------- 노드 이름 변경 ----------
      
      if node_a not in node_dict :
        node_dict[node_a] = 'household{:04d}'.format(idx)
        idx += 1

      if node_b not in node_dict :
        node_dict[node_b] = 'household{:04d}'.format(idx)
        idx += 1

      new_a = node_dict[node_a]
      new_b = node_dict[node_b]

      # ---------- self-loop 제거 ----------

      # 🚨 네트워크 분석의 편의성을 위해 self-loop를 제거함
      if new_a == new_b :
        print('[data loader] self-loop 발견 :', new_a)
        continue

      G_load.add_edge(new_a, new_b)

  except FileNotFoundError :
    raise FileNotFoundError('입력한 파일 경로가 잘못되었습니다. 파일 경로를 확인하십시오. 현재 경로 : {}'.format(file_path))

  except Exception as e :
    raise RuntimeError('입력한 파일 로드 중 오류가 발생하였습니다. 오류를 확인하십시오. 오류 발생 : {}'.format(e))
    
  return G_load
      
