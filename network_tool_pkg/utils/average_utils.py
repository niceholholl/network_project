import numpy as np

# -------------------- 앙상블 평균화 함수 : 중심성 및 전역 지표 결과를 노드 및 지표별로 평균화하는 함수 --------------------
def ensemble_average(results_list) :

  # ---------- 입력 유효성 및 리스트 형태 확인 (예외 처리) ----------

  if not isinstance(results_list, list) :
    raise TypeError('[ensemble_average] 함수의 입력은 리스트 형태여야 합니다.')

  if not results_list :
    raise ValueError('[ensemble_average] 함수의 입력이 비어있습니다. 시뮬레이션 결과가 없습니다.')

  # ---------- 시각화 과정에서의 통일성 유지를 위해 리스트 내부에서 등장한 모든 key들의 union 생성 (예외 처리) ----------

  all_keys = set()

  for item in results_list :
    if isinstance(item, dict) :
      all_keys.update(item.keys())

  if not all_keys :
    raise ValueError('[ensemble_average] 유효한 key가 없습니다. 모든 결과가 비어있습니다.')

  # ---------- 리스트 내부의 딕셔너리를 정렬 ----------

  sorted_keys = sorted(all_keys)

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
      averaged_values.append(np.nan)
    else :
      averaged_values.append(float(np.mean(valid_vals)))

  return averaged_values
