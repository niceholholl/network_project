import numpy as np

# -------------------- 앙상블 평균화 함수 : 중심성 및 전역 지표 결과를 노드 및 지표별로 평균화하는 함수 --------------------
def ensemble_average(results_list) :

  # ---------- 입력 유효성 및 리스트 형태 확인 (예외 처리) ----------

  if not isinstance(results_list, list) :
    raise TypeError('ensemble_average 함수의 입력은 리스트 형태여야 합니다.')

  if not results_list :
    raise ValueError('ensemble_average 함수의 입력이 비어있습니다. 시뮬레이션 결과가 없습니다.')

  # ---------- 리스트 내부의 딕셔너리를 정렬 ---------- 

  # try :
  #   sorted_keys = sorted(results_list[0].keys())

  # except Exception as e :
  #   raise RuntimeError('[ensemble_average] 정렬 과정에서 오류가 발생하였습니다. 오류 : {}'.format(e))

  # # ---------- None 제거 후 평균 ---------- 

  # averaged_values = []

  # for key in sorted_keys :
  #   vals = [result[key] for result in results_list if result[key] is not None]

  #   if len(vals) == 0 :
  #     averaged_values.append(None)
  #   else : 
  #     averaged_values.append(float(np.mean(vals)))
  # ---------- 리스트 내부의 딕셔너리를 정렬 ---------- 
  try :
      sorted_keys = sorted(results_list[0].keys())

  except Exception as e :
      # 만약 results_list[0]이 None이면 에러가 나므로, 첫 번째 유효한 딕셔너리를 찾도록 수정할 수도 있지만,
      # 여기서는 기존 코드 구조를 유지합니다.
      raise RuntimeError('[ensemble_average] 정렬 과정에서 오류가 발생하였습니다. 오류 : {}'.format(e))

  # ---------- None 및 NaN 제거 후 평균 ---------- 

  averaged_values = []

  for key in sorted_keys :
      # 1. 'None'인 값은 제거 (기존 로직 유지)
      # 2. float(np.mean(vals)) 대신 np.nanmean을 사용합니다.
      
      # 🌟🌟🌟 수정된 부분: np.nan이 아니며, None도 아닌 유효한 값만 선택 🌟🌟🌟
      # vals = [result[key] for result in results_list if result[key] is not None]  <-- 이전 코드

      vals = []
      for result in results_list:
          value = result[key]
          # None이 아니고, np.nan도 아니며 (np.isnan으로 확인), float이나 int 타입인 유효한 값만 선택
          if value is not None and not np.isnan(value) and (isinstance(value, (int, float, np.number))):
                vals.append(value)
      # 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
      if len(vals) == 0 :
          averaged_values.append(None)
      else : 
          # 🌟 수정: np.mean 대신 np.nanmean을 사용하여 NaN 값을 자동으로 무시하고 평균을 계산합니다.
          # float() 캐스팅을 제거하고, 리스트 내부에 NaN이 포함되어 있을 경우를 대비합니다.
          averaged_values.append(np.nanmean(vals)) 
          
  return averaged_values
