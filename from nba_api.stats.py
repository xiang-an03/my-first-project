import matplotlib.pyplot as plt
import pandas as pd
import time
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, teamyearbyyearstats

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

def fetch_and_show_ae_full_dashboard():
    print(">>> 正在連線 NBA 數據庫...")
    try:
        ae_id = players.find_players_by_full_name("Anthony Edwards")[0]['id']
        
        print(">>> 正在計算個人場均數據...")
        career = playercareerstats.PlayerCareerStats(player_id=ae_id)
        df = career.season_totals_regular_season.get_data_frame()
        
        df['PPG'] = (df['PTS'] / df['GP']).round(1)
        df['RPG'] = (df['REB'] / df['GP']).round(1)
        df['APG'] = (df['AST'] / df['GP']).round(1)
       
        print(">>> 正在同步球隊勝率...")
        wolf_id = df['TEAM_ID'].iloc[0] 
        team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=wolf_id)
        team_df = team_stats.get_data_frames()[0]
       
        win_col = [c for c in team_df.columns if 'PCT' in c and 'W' in c][0]
        win_rate_map = dict(zip(team_df['YEAR'], team_df[win_col]))
        df['Win_Rate'] = df['SEASON_ID'].map(win_rate_map)

        print(">>> 正在生成圖表視窗...")
        fig, ax1 = plt.subplots(figsize=(12, 7))
        
        line_pts = ax1.plot(df['SEASON_ID'], df['PPG'], color='blue', marker='o', linewidth=3, label='場均得分')
        line_reb = ax1.plot(df['SEASON_ID'], df['RPG'], color='green', marker='s', linestyle='--', label='場均籃板')
        line_ast = ax1.plot(df['SEASON_ID'], df['APG'], color='orange', marker='^', linestyle=':', label='場均助攻')
        ax1.set_ylabel('球員數據 (PTS/REB/AST)', fontsize=12)
        ax1.set_ylim(0, 35)

        ax2 = ax1.twinx()
        line_win = ax2.plot(df['SEASON_ID'], df['Win_Rate'], color='red', marker='D', linewidth=2, label='球隊勝率')
        ax2.set_ylabel('球隊勝率 (Win %)', color='red', fontsize=12)
        ax2.set_ylim(0, 1.0)

        for i in range(len(df)):
            ax1.text(i, df['PPG'].iloc[i] + 0.8, f"{df['PPG'].iloc[i]}", ha='center', color='blue', fontweight='bold')
            ax1.text(i, df['RPG'].iloc[i] + 0.5, f"{df['RPG'].iloc[i]}", ha='center', color='green')
            ax1.text(i, df['APG'].iloc[i] + 0.5, f"{df['APG'].iloc[i]}", ha='center', color='orange')
            ax2.text(i, df['Win_Rate'].iloc[i] + 0.02, f"{df['Win_Rate'].iloc[i]:.1%}", ha='center', color='red')

        all_lines = line_pts + line_reb + line_ast + line_win
        all_labels = [l.get_label() for l in all_lines]
        ax1.legend(all_lines, all_labels, loc='upper left')

        plt.title('Anthony Edwards 生涯數據 vs 球隊勝率', fontsize=16)
        plt.grid(True, alpha=0.2)
        plt.tight_layout()

        print(">>> 視窗已彈出！")
        plt.show()

    except Exception as e:
        print(f"\n❌ 程式出錯: {e}")

if __name__ == "__main__":
    fetch_and_show_ae_full_dashboard()