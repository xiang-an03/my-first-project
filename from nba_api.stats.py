import matplotlib.pyplot as plt
import pandas as pd

# 1. 準備數據 (2020-2026)
data = {
    'Season': ['20-21', '21-22', '22-23', '23-24', '24-25', '25-26'],
    'PPG': [19.3, 21.3, 24.6, 25.9, 27.6, 28.9],
    'RPG': [4.7, 4.8, 5.8, 5.4, 5.7, 5.0],
    'APG': [2.9, 3.8, 4.4, 5.1, 4.5, 3.7],
    'Win_Rate': [0.319, 0.561, 0.512, 0.683, 0.598, 0.588]
}
df = pd.DataFrame(data)

# 2. 設定圖表與字體 (避免中文亂碼)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

fig, ax1 = plt.subplots(figsize=(14, 7))

# 3. 繪製左軸：得分、籃板、助攻
# 得分用線，籃板與助攻用長條圖或不同線型區隔
line1 = ax1.plot(df['Season'], df['PPG'], color='blue', marker='o', linewidth=3, label='場均得分 (PTS)')
line2 = ax1.plot(df['Season'], df['RPG'], color='green', marker='s', linestyle='--', label='場均籃板 (REB)')
line3 = ax1.plot(df['Season'], df['APG'], color='orange', marker='^', linestyle=':', label='場均助攻 (AST)')

ax1.set_xlabel('賽季 (Season)', fontsize=12)
ax1.set_ylabel('球員數據數值', fontsize=12)
ax1.tick_params(axis='y')
ax1.grid(True, alpha=0.2)

# 4. 繪製右軸：球隊勝率
ax2 = ax1.twinx()
line4 = ax2.plot(df['Season'], df['Win_Rate'], color='red', marker='D', linewidth=2, label='球隊勝率 (Win %)')
ax2.set_ylabel('球隊勝率', color='red', fontsize=12)
ax2.set_ylim(0, 1.0) # 勝率範圍固定 0~1
ax2.tick_params(axis='y', labelcolor='red')

# 5. --- 核心需求：在圖表上顯示數值標籤 ---
def add_labels(ax, x_data, y_data, color, offset=0.5, is_percent=False):
    for x, y in zip(x_data, y_data):
        label = f'{y:.1f}' if not is_percent else f'{y:.1%}'
        ax.text(x, y + offset, label, ha='center', color=color, fontweight='bold', fontsize=10)

# 為每一條線加上標籤
add_labels(ax1, df['Season'], df['PPG'], 'blue', offset=0.8)   # 得分標籤
add_labels(ax1, df['Season'], df['RPG'], 'green', offset=0.5)  # 籃板標籤
add_labels(ax1, df['Season'], df['APG'], 'orange', offset=0.5) # 助攻標籤
add_labels(ax2, df['Season'], df['Win_Rate'], 'red', offset=0.02, is_percent=True) # 勝率標籤

# 6. 合併圖例
all_lines = line1 + line2 + line3 + line4
all_labels = [l.get_label() for l in all_lines]
ax1.legend(all_lines, all_labels, loc='upper left', frameon=True, shadow=True)

plt.title('Anthony Edwards 生涯各項數據與球隊勝率對照圖 (含數值標註)', fontsize=16)
fig.tight_layout()

# 儲存與顯示
plt.savefig('AE_Full_Stats.png', dpi=300)
plt.show()