import os
import csv
import json

workspace_dir = r"c:\Users\ASUS\\.gemini\\antigravity\\scratch\\fifa-wc2026-dataset"
if not os.path.exists(workspace_dir):
    workspace_dir = os.path.dirname(os.path.abspath(__file__))

players_path = os.path.join(workspace_dir, "squads_and_players.csv")
teams_path = os.path.join(workspace_dir, "teams.csv")

with open(teams_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    teams_headers = next(reader)
    teams = {row[1]: int(row[0]) for row in reader}

print("Teams mapping:", teams)

target_teams = {9: "Brazil", 22: "Japan", 17: "Germany", 14: "Paraguay", 21: "Netherlands", 10: "Morocco"}

players_by_team = {t_id: [] for t_id in target_teams}

with open(players_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        t_id = int(row["team_id"])
        if t_id in target_teams:
            players_by_team[t_id].append((int(row["player_id"]), row["player_name"], row["position"]))

for t_id, t_name in target_teams.items():
    print(f"\n=== {t_name} (ID: {t_id}) ===")
    for p_id, p_name, p_pos in sorted(players_by_team[t_id], key=lambda x: x[1]):
        print(f"  {p_id}: {p_name} ({p_pos})")
