import numpy as np

# -------------------- 앙상블 평균화 함수 : 중심성 및 전역 지표 결과를 노드 및 지표별로 평균화하는 함수 --------------------
def ensemble_average(results_list) :

  # ---------- 입력 유효성 및 리스트 형태 확인 (예외 처리) ----------

  if not isinstance(results_list, list) :
    raise TypeError('ensemble_average 함수의 입력은 리스트 형태여야 합니다.')

  if not results_list :
    raise ValueError('ensemble_average 함수의 입력이 비어있습니다. 시뮬레이션 결과가 없습니다.')

  # ---------- 리스트 내부의 딕셔너리를 Numpy 배열로 변환 ---------- 

  try :
    values_array = np.array([list(dict(sorted(result.items())).values()) for result in results_list])

  except Exception as e :
    raise RuntimeError('Numpy 배열로 변환하는 데 실패하였습니다. 오류 : {}'.format(e))
  
  # ---------- Numpy 배열 평균 계산 (노드 및 지표별 평균) ----------

  return np.mean(values_array, axis = 0)
