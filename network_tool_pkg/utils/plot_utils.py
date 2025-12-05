import numpy as np
import matplotlib.pyplot as plt

# -------------------- Degree 비교 플롯을 위한 함수 --------------------
def plot_degree_hist(ax, original, models, model_name) :

  bins = range(max(original) + 2)

  # ---------- 원본 히스토그램 생성 ----------

  original_hist = np.histogram(original, bins = bins, density = True)[0]
  ax.plot(original_hist, label = 'Original', marker = 'o', 
