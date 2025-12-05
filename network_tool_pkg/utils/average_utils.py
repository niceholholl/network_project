import numpy as np

# -------------------- 앙상블 평균화 함수 : 중심성 및 전역 지표 결과를 노드 및 지표별로 평균화하는 함수 --------------------
def ensemble_average(results_list) :

  # ---------- 입력 유효성 및 리스트 형태 확인 (예외 처리) ----------

  if not isinstance(results_list, list) :
    raise TypeError('ensemble_average 함수의 입력은 리스트 형태여야 합니다.')

  if not results_list :
    raise ValueError('ensemble_average 함수의 입력이 비어있습니다. 시뮬레이션 결과가 없습니다.')

  # ---------- 리스트 내부의 딕셔너리를 정렬 ---------- 

  try :
    sorted_keys = sorted(result_list[0].key())

  except Exception as e :
    raise RuntimeError('[ensemble_average] 정렬 과정에서 오류가 발생하였습니다. 오류 : {}'.format(e))

  # ---------- None 제거 후 평균 ---------- 

  averaged_values = []

  for key in sorted_keys :
    vals = [result[key] for result in results_list if result[key] is not None]

    if len(vals) == 0 :
      averaged_values.append(None)
    else : 
      averaged_values.append(float(np.mean(vals)))

  return averaged_values
