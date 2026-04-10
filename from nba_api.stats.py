from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import matplotlib.pyplot as plt
import pandas as pd
import time

# 解決 matplotlib 中文顯示問題 (如果需要)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] # Windows
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS'] # Mac
plt.rcParams['axes.unicode_minus'] = False # 解決負號顯示問題

def get_player_season_stats(player_name):
    print(f"正在搜尋球員：{player_name}...")
    
    nba_players = players.find_players_by_full_name(player_name)
    if not nba_players:
        return None
    
    player_id = nba_players[0]['id']
    time.sleep(1)

    # 1. 抓取生涯統計 (改回預設參數最保險)
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = career_stats.get_data_frames()[0]
    
    # 2. 手動計算場均數據 (這是最準確的做法)
    # 我們將 總得分(PTS) / 出賽場數(GP)
    df['AVG_PTS'] = df['PTS'] / df['GP']
    df['AVG_REB'] = df['REB'] / df['GP']
    df['AVG_AST'] = df['AST'] / df['GP']
    
    # 3. 只取我們要的欄位
    selected_stats = df[['SEASON_ID', 'AVG_PTS', 'AVG_REB', 'AVG_AST']]
    
    print("\n成功取得 Anthony Edwards 場均數據：")
    print(selected_stats)
    return selected_stats

def plot_stats(df, player_name):
    if df is None: return

    plt.figure(figsize=(10, 6))

    # 繪製三條線
    plt.plot(df['SEASON_ID'], df['AVG_PTS'], marker='o', color='blue', label='得分 (PTS)')
    plt.plot(df['SEASON_ID'], df['AVG_REB'], marker='s', color='green', label='籃板 (REB)')
    plt.plot(df['SEASON_ID'], df['AVG_AST'], marker='^', color='orange', label='助攻 (AST)')

    # 強制在每個點上顯示數值，這樣有沒有抓到資料一目了然
    for i in range(len(df)):
        plt.text(i, df['AVG_PTS'].iloc[i] + 0.5, f"{df['AVG_PTS'].iloc[i]:.1f}", ha='center', color='blue')
        plt.text(i, df['AVG_REB'].iloc[i] + 0.5, f"{df['AVG_REB'].iloc[i]:.1f}", ha='center', color='green')
        plt.text(i, df['AVG_AST'].iloc[i] + 0.5, f"{df['AVG_AST'].iloc[i]:.1f}", ha='center', color='orange')

    plt.title(f'{player_name} 生涯場均數據')
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.show()

# --- 主程式執行 ---
if __name__ == "__main__":
    player = "Anthony Edwards"
    stats_df = get_player_season_stats(player)
    
    if stats_df is not None:
        plot_stats(stats_df, player)