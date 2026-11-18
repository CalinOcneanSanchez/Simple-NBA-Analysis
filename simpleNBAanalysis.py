
import pandas as pd

# NBA API
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster, leaguedashplayerstats

# find the Celtics team ID
celtics = [t for t in teams.get_teams() if t["abbreviation"] == "BOS"][0]

# retrieve the current Celtics roster
roster = commonteamroster.CommonTeamRoster(
    team_id=celtics["id"]
).get_data_frames()[0]

# retrieve Celtics player statistics per game
stats = leaguedashplayerstats.LeagueDashPlayerStats(
    season="2026-27",
    per_mode_detailed="PerGame",
    team_id_nullable=celtics["id"],
).get_data_frames()[0]

# rename columns
stats = stats.rename(columns={"PLAYER_NAME": "Player Name", "GP": "Gp", "MIN": "Min", "PTS": "Pts", "REB": "Reb", "AST": "Ast", "STL": "Stl", "BLK": "Blk","FG_PCT": "Fg%", "FG3_PCT": "Fg3%", "FT_PCT": "Ft%"})

# select columns to display
cols = ["Player Name", "Gp", "Min", "Pts", "Reb", "Ast", "Stl", "Blk", "Fg%", "Fg3%", "Ft%"]

# sort players by points per game
stats = stats.sort_values("Pts", ascending=False)

# ask the user to select a player
player_name = input("Enter a Celtics player's name: ")

# search for the selected player
player_stats = stats[
    stats["Player Name"].str.lower() == player_name.strip().lower()]

# display player statistics
if not player_stats.empty:
    print("\nPlayer Statistics")
    print(player_stats[cols].to_string(index=False))
else:
    print("\nPlayer not found. Please check the spelling.")

    print("\nAvailable Celtics Players:")
    print(roster["PLAYER"].to_string(index=False))
