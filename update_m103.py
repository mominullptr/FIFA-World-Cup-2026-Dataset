import csv
import json
import os

workspace_dir = os.path.dirname(os.path.abspath(__file__))

def update_matches():
    matches_path = os.path.join(workspace_dir, "matches.csv")
    with open(matches_path, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    
    headers = reader[0]
    rows = reader[1:]
    
    for row in rows:
        match_id = row[0]
        if match_id == "103":
            row[7] = "4"       # home_score
            row[8] = "6"       # away_score
            row[9] = ""        # home_penalty_score
            row[10] = ""       # away_penalty_score
            row[11] = "Completed"
            row[12] = "Regular"
            row[13] = "2.88"   # home_xg
            row[14] = "2.88"   # away_xg
            row[15] = "7"      # referee_id (Jesús Valenzuela)
            row[16] = "1151"   # potm_player_id (Bukayo Ayoyinka Saka)
            break

    with open(matches_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print("Updated matches.csv")

def update_matches_detailed():
    matches_detailed_path = os.path.join(workspace_dir, "matches_detailed.csv")
    with open(matches_detailed_path, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    
    headers = reader[0]
    rows = reader[1:]
    
    for row in rows:
        match_id = row[0]
        if match_id == "103":
            row[11] = "4"      # home_score
            row[12] = "6"      # away_score
            row[13] = ""       # home_penalty_score
            row[14] = ""       # away_penalty_score
            row[15] = "Completed"
            row[16] = "Regular"
            row[17] = "2.88"   # home_xg
            row[18] = "2.88"   # away_xg
            row[19] = "Mike Peterson Maignan"     # home_goalkeeper
            row[20] = "Dean Bradley Henderson"    # away_goalkeeper
            row[21] = "Bukayo Ayoyinka Saka"      # player_of_the_match_name
            row[22] = "Jesús Valenzuela"           # referee_name
            break

    with open(matches_detailed_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print("Updated matches_detailed.csv")

def append_events():
    events_path = os.path.join(workspace_dir, "match_events.csv")
    with open(events_path, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    
    headers = reader[0]
    rows = reader[1:]
    
    # Check if Match 103 events are already in rows
    for row in rows:
        if row[1] == "103":
            print("Events for Match 103 already appended.")
            return

    start_event_id = int(rows[-1][0]) + 1
    
    new_events = [
        # Match 103
        (103, 3, "Goal", 45, 1148),        # Declan Rice
        (103, 18, "Goal", 45, 1146),       # Ezri Konsa
        (103, 18, "Assist", 45, 1148),     # Declan Rice
        (103, 37, "Goal", 45, 1151),       # Bukayo Saka
        (103, 37, "Assist", 45, 1155),     # Marcus Rashford
        (103, 46, "Goal", 45, 1151),       # Bukayo Saka (45+1')
        (103, 46, "Assist", 45, 1165),     # Eberechi Eze (45+1')
        (103, 48, "Goal", 33, 842),        # Kylian Mbappé
        (103, 48, "Assist", 33, 843),      # Michael Olise
        (103, 54, "Goal", 33, 844),        # Bradley Barcola
        (103, 54, "Assist", 33, 842),      # Kylian Mbappé
        (103, 66, "Goal", 33, 842),        # Kylian Mbappé
        (103, 66, "Assist", 33, 843),      # Michael Olise
        (103, 87, "Goal", 45, 1151),       # Bukayo Saka (pen.)
        (103, 96, "Goal", 33, 839),        # Ousmane Dembélé (90+6')
        (103, 96, "Assist", 33, 836),      # Dayot Upamecano (90+6')
        (103, 98, "Goal", 45, 1154)        # Jude Bellingham (90+8')
    ]
    
    for mid, minute, etype, tid, pid in new_events:
        rows.append([str(start_event_id), str(mid), str(minute), etype, str(tid), str(pid)])
        start_event_id += 1

    with open(events_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Appended events to match_events.csv, last event_id is {start_event_id - 1}")

def append_lineups():
    lineups_path = os.path.join(workspace_dir, "match_lineups.csv")
    with open(lineups_path, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    
    headers = reader[0]
    rows = reader[1:]
    
    # Check if Match 103 lineups are already in rows
    for row in rows:
        if row[1] == "103":
            print("Lineups for Match 103 already appended.")
            return

    start_lineup_id = int(rows[-1][0]) + 1
    
    # Match 103 players
    m103_players = [
        # France (33)
        # Starting XI
        (848, 33, 1, "GK", 90),   # Mike Maignan
        (834, 33, 1, "DEF", 90),  # Malo Gusto
        (847, 33, 1, "DEF", 45),  # Ibrahima Konate (subbed out at 46')
        (858, 33, 1, "DEF", 90),  # Maxence Lacroix
        (851, 33, 1, "DEF", 45),  # Theo Hernandez (subbed out at 46')
        (850, 33, 1, "MID", 90),  # Warren Zaire-Emery
        (846, 33, 1, "MID", 90),  # Adrien Rabiot
        (843, 33, 1, "FWD", 90),  # Michael Olise
        (856, 33, 1, "MID", 45),  # Rayan Cherki (subbed out at 46')
        (852, 33, 1, "FWD", 45),  # Desire Doue (subbed out at 46')
        (842, 33, 1, "FWD", 90),  # Kylian Mbappe
        # Active Subs
        (836, 33, 0, "DEF", 45),  # Dayot Upamecano (subbed in at 46')
        (835, 33, 0, "DEF", 45),  # Lucas Digne (subbed in at 46')
        (839, 33, 0, "FWD", 45),  # Ousmane Dembele (subbed in at 46')
        (844, 33, 0, "FWD", 45),  # Bradley Barcola (subbed in at 46')
        (837, 33, 0, "DEF", 1),   # Jules Kounde (subbed in at 90')
        # Unused Subs (10 players)
        (833, 33, 0, "GK", 0),
        (838, 33, 0, "MID", 0),
        (840, 33, 0, "MID", 0),
        (841, 33, 0, "FWD", 0),
        (845, 33, 0, "MID", 0),
        (849, 33, 0, "DEF", 0),
        (853, 33, 0, "DEF", 0),
        (854, 33, 0, "FWD", 0),
        (855, 33, 0, "GK", 0),
        (857, 33, 0, "MID", 0),

        # England (45)
        # Starting XI
        (1157, 45, 1, "GK", 90),  # Dean Henderson
        (1170, 45, 1, "DEF", 90), # Jarell Quansah
        (1146, 45, 1, "DEF", 90), # Ezri Konsa
        (1150, 45, 1, "DEF", 90), # Marc Guehi
        (1169, 45, 1, "DEF", 83), # Djed Spence (subbed out at 83')
        (1148, 45, 1, "MID", 90), # Declan Rice
        (1151, 45, 1, "FWD", 90), # Bukayo Saka
        (1165, 45, 1, "MID", 79), # Eberechi Eze (subbed out at 79')
        (1161, 45, 1, "MID", 90), # Morgan Rogers
        (1155, 45, 1, "FWD", 45), # Marcus Rashford (subbed out at 46')
        (1166, 45, 1, "FWD", 79), # Ivan Toney (subbed out at 79')
        # Active Subs
        (1163, 45, 0, "FWD", 45), # Ollie Watkins (subbed in at 46')
        (1154, 45, 0, "MID", 11), # Jude Bellingham (subbed in at 79')
        (1152, 45, 0, "MID", 11), # Elliot Anderson (subbed in at 79')
        (1168, 45, 0, "DEF", 7),  # Reece James (subbed in at 83')
        (1156, 45, 0, "DEF", 1),  # Trevoh Chalobah (subbed in at 90')
        # Unused Subs (10 players)
        (1145, 45, 0, "GK", 0),
        (1147, 45, 0, "DEF", 0),
        (1149, 45, 0, "DEF", 0),
        (1153, 45, 0, "FWD", 0),
        (1158, 45, 0, "MID", 0),
        (1159, 45, 0, "DEF", 0),
        (1160, 45, 0, "MID", 0),
        (1162, 45, 0, "FWD", 0),
        (1164, 45, 0, "FWD", 0),
        (1167, 45, 0, "GK", 0)
    ]
    
    for pid, tid, is_start, pos, mins in m103_players:
        rows.append([str(start_lineup_id), "103", str(pid), str(tid), str(is_start), pos, str(mins)])
        start_lineup_id += 1

    with open(lineups_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Appended lineups to match_lineups.csv, last lineup_id is {start_lineup_id - 1}")

def append_team_stats():
    stats_path = os.path.join(workspace_dir, "match_team_stats.csv")
    with open(stats_path, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    
    headers = reader[0]
    rows = reader[1:]
    
    # Check if Match 103 stats are already in rows
    for row in rows:
        if row[0] == "103":
            print("Stats for Match 103 already appended.")
            return

    new_stats = [
        # match_id,team_id,possession_pct,total_shots,shots_on_target,corners,fouls,offsides,saves,player_of_the_match,data_source,last_updated
        ("103", "33", "50", "18", "9", "4", "9", "1", "5", "", "Sofascore", "2026-07-18"),
        ("103", "45", "50", "21", "11", "7", "12", "2", "5", "Bukayo Ayoyinka Saka", "Sofascore", "2026-07-18")
    ]
    
    for row in new_stats:
        rows.append(list(row))

    with open(stats_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print("Appended stats to match_team_stats.csv")

def update_real_match_details_json():
    json_path = os.path.join(workspace_dir, "real_match_details.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    m103 = {
        "group": "Third-place match",
        "date": "July 18, 2026",
        "home_team": "France",
        "away_team": "England",
        "score": "4–6",
        "home_goals": [
          {
            "scorer": "Kylian Mbappé",
            "minute": "48'",
            "assist": "Michael Olise"
          },
          {
            "scorer": "Bradley Barcola",
            "minute": "54'",
            "assist": "Kylian Mbappé"
          },
          {
            "scorer": "Kylian Mbappé",
            "minute": "66'",
            "assist": "Michael Olise"
          },
          {
            "scorer": "Ousmane Dembélé",
            "minute": "90+6'",
            "assist": "Dayot Upamecano"
          }
        ],
        "away_goals": [
          {
            "scorer": "Declan Rice",
            "minute": "3'"
          },
          {
            "scorer": "Ezri Konsa",
            "minute": "18'",
            "assist": "Declan Rice"
          },
          {
            "scorer": "Bukayo Saka",
            "minute": "37'",
            "assist": "Marcus Rashford"
          },
          {
            "scorer": "Bukayo Saka",
            "minute": "45+1'",
            "assist": "Eberechi Eze"
          },
          {
            "scorer": "Bukayo Saka",
            "minute": "87' (pen.)"
          },
          {
            "scorer": "Jude Bellingham",
            "minute": "90+8'"
          }
        ]
    }
    
    # Avoid duplicate appends if script is run twice
    match_keys = [(m['home_team'], m['away_team']) for m in data]
    
    if ("France", "England") not in match_keys:
        data.append(m103)
        print("Appended France vs England to JSON")
        
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Updated real_match_details.json")

def main():
    update_matches()
    update_matches_detailed()
    append_events()
    append_lineups()
    append_team_stats()
    update_real_match_details_json()
    print("All CSV and JSON files updated successfully for Match 103!")

if __name__ == "__main__":
    main()
