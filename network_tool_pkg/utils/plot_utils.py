import numpy as np
import matplotlib.pyplot as plt

# -------------------- Degree 비교 플롯을 위한 함수 --------------------
def plot_degree_hist(ax, original, model, model_name, bar_alpha = 0.35, original_color = 'blue', model_color = 'red') :

  # 1. 🌟 FIX: max(original)이 실패할 경우를 대비하여 0보다 큰지 확인
  if not original:
      return # 데이터가 없으면 함수 종료

  # 2. Histogram 계산 (Y축 데이터)
  bins = range(max(original) + 2)
  original_hist = np.histogram(original, bins = bins, density = True)[0]
  
  # UnboundLocalError를 피하고 올바른 길이를 사용
  k = np.arange(len(original_hist)) 
  
  # ---------- 원본 bar + line 생성 ----------
  ax.bar(k - 0.2, original_hist, width = 0.4, alpha = bar_alpha, color = original_color, label = 'Original (bar)')
  ax.plot(k - 0.2, original_hist, color = original_color, linewidth = 2, label = 'Original (line)')

  # ---------- 랜덤 모델 bar + line 생성 ----------

  ax.bar(k + 0.2, model, width = 0.4, alpha = bar_alpha, color = model_color, label = '{} (bar)'.format(model_name))
  ax.plot(k + 0.2, model, color = model_color, linestyle = '--', linewidth = 2, label = '{} (line)'.format(model_name))

  # ---------- 데코레이션 ----------

  ax.set_xlabel(r'Degree $k$')
  ax.set_ylabel(r'$P(k)$')
  ax.set_title('Original vs {}'.format(model_name))
  ax.legend()
  ax.grid(alpha = 0.4)
  # ax.axvline(x=0, color='grey', linewidth=1.5, linestyle='--')

# -------------------- Degree 평균 히스토그램 계산을 위한 함수 --------------------
def average_hist(degree_lists, fixed_max_degree) : 
    
    # 🌟 수정: bins 범위를 앙상블의 max 대신, 고정된 fixed_max_degree를 사용하도록 강제
    bins_range = range(fixed_max_degree + 2) 

    return np.mean([np.histogram(degree_list, bins = bins_range, density = True)[0] 
                    for degree_list in degree_lists], axis = 0)