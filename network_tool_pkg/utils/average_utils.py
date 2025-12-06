import numpy as np

# -------------------- 앙상블 평균화 함수 : 중심성 및 전역 지표 결과를 노드 및 지표별로 평균화하는 함수 --------------------
def ensemble_average(results_list) :

  # ---------- 입력 유효성 및 리스트 형태 확인 (예외 처리) ----------

  if not isinstance(results_list, list) :
    raise TypeError('ensemble_average 함수의 입력은 리스트 형태여야 합니다.')

  if not results_list :
    raise ValueError('ensemble_average 함수의 입력이 비어있습니다. 시뮬레이션 결과가 없습니다.')

  # ---------- 딕셔너리 유효성 확인 (예외 처리) ----------
  
  first_valid = None
  
  for item in results_list :
    
    if isinstance(item, dict) :
      first_valid = item
      break

  if first_valid is None :
    raise ValueError('[ensemble_average] 정렬 과정에서 오류가 발생하였습니다.')

  # ---------- 리스트 내부의 딕셔너리를 정렬 ----------

  sorted_keys = sorted(first_valid.keys())

  # ----------  Key 값 추출 및 평균 (None 및 NaN 제거) ---------- 

  averaged_values = []

  for key in sorted_keys :
    valid_vals = []

    for result in results_list :
      if not isinstance(result, dict) :
        continue

      value = result.get(key, None)

      if value is None :
        continue
      if isinstance(value, (list, dict)) :
        continue

      if isinstance(value, (int, float, np.number)) :
        if not np.isnan(value) :
          valid_vals.append(value)
    
    if len(valid_vals) == 0 :
      averaged_values.append(None)
    else :
      averaged_values.append(float(np.mean(valid_vals)))

  return averaged_values
