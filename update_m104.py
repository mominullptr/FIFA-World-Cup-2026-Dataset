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
        if match_id == "104":
            row[7] = "1"       # home_score
            row[8] = "0"       # away_score
            row[9] = ""        # home_penalty_score
            row[10] = ""       # away_penalty_score
            row[11] = "Completed"
            row[12] = "AET"
            row[13] = "0.52"   # home_xg
            row[14] = "0.09"   # away_xg
            row[15] = "20"     # referee_id (Slavko Vinčić)
            row[16] = "735"    # player_of_the_match_id (Ferran Torres)
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
        if match_id == "104":
            row[11] = "1"      # home_score
            row[12] = "0"      # away_score
            row[13] = ""       # home_penalty_score
            row[14] = ""       # away_penalty_score
            row[15] = "Completed"
            row[16] = "AET"
            row[17] = "0.52"   # home_xg
            row[18] = "0.09"   # away_xg
            row[19] = "Unai Simón"                     # home_goalkeeper
            row[20] = "Damián Emiliano Martínez"       # away_goalkeeper
            row[21] = "Ferran Torres"                  # player_of_the_match_name
            row[22] = "Slavko Vinčić"                  # referee_name
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
    
    # Check if Match 104 events are already in rows
    for row in rows:
        if row[1] == "104":
            print("Events for Match 104 already appended.")
            return

    start_event_id = int(rows[-1][0]) + 1
    
    new_events = [
        # Match 104 (Spain 29, Argentina 37)
        (104, 40, "Yellow Card", 37, 942),       # Lisandro Martínez (40')
        (104, 52, "Yellow Card", 37, 941),       # Leandro Paredes (52')
        (104, 83, "Yellow Card", 37, 960),       # Enzo Fernández (83')
        (104, 92, "Yellow Card", 37, 949),       # Cristian Romero (92')
        (104, 93, "Yellow Card", 37, 960),       # Enzo Fernández (93')
        (104, 93, "Red Card", 37, 960),          # Enzo Fernández (sent off 93')
        (104, 106, "Goal", 29, 735),             # Ferran Torres (106')
        (104, 106, "Assist", 29, 745),           # Nico Williams (106')
        (104, 111, "Yellow Card", 37, 956),      # Alexis Mac Allister (111')
        (104, 120, "Red Card", 37, 941)          # Leandro Paredes (sent off after final whistle 120')
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
    
    # Check if Match 104 lineups are already in rows
    for row in rows:
        if row[1] == "104":
            print("Lineups for Match 104 already appended.")
            return

    start_lineup_id = int(rows[-1][0]) + 1
    
    # Match 104 players
    m104_players = [
        # Spain (29)
        # Starting XI
        (751, 29, 1, "GK", 120),  # Unai Simón
        (740, 29, 1, "DEF", 120), # Pedro Porro
        (750, 29, 1, "DEF", 120), # Pau Cubarsi
        (742, 29, 1, "DEF", 99),  # Aymeric Laporte (subbed out at 99')
        (752, 29, 1, "DEF", 120), # Marc Cucurella
        (744, 29, 1, "MID", 120), # Rodrigo Rodri
        (736, 29, 1, "MID", 62),  # Fabian Ruiz (subbed out at 62')
        (743, 29, 1, "MID", 75),  # Alejandro Baena (subbed out at 75')
        (738, 29, 1, "FWD", 75),  # Daniel Olmo (subbed out at 75')
        (747, 29, 1, "FWD", 120), # Lamine Yamal
        (749, 29, 1, "FWD", 62),  # Mikel Oyarzabal (subbed out at 62')
        # Active Subs
        (735, 29, 0, "FWD", 58),  # Ferran Torres (subbed in at 62')
        (748, 29, 0, "MID", 58),  # Pedro Pedri (subbed in at 62')
        (745, 29, 0, "FWD", 45),  # Nico Williams (subbed in at 75')
        (734, 29, 0, "MID", 45),  # Mikel Merino (subbed in at 75')
        (732, 29, 0, "DEF", 21),  # Eric Garcia (subbed in at 99')
        # Unused Subs (10 players)
        (729, 29, 0, "GK", 0),
        (730, 29, 0, "DEF", 0),
        (731, 29, 0, "DEF", 0),
        (733, 29, 0, "DEF", 0),
        (737, 29, 0, "MID", 0),
        (739, 29, 0, "FWD", 0),
        (741, 29, 0, "GK", 0),
        (746, 29, 0, "MID", 0),
        (753, 29, 0, "FWD", 0),
        (754, 29, 0, "FWD", 0),

        # Argentina (37)
        # Starting XI
        (959, 37, 1, "GK", 120),  # Damián Emiliano Martínez
        (940, 37, 1, "DEF", 57),  # Gonzalo Montiel (subbed out at 57')
        (949, 37, 1, "DEF", 69),  # Cristian Romero (subbed out at 69')
        (942, 37, 1, "DEF", 43),  # Lisandro Martínez (subbed out at 43')
        (939, 37, 1, "DEF", 120), # Nicolás Tagliafico
        (943, 37, 1, "MID", 69),  # Rodrigo De Paul (subbed out at 69')
        (960, 37, 1, "MID", 93),  # Enzo Fernández (sent off at 93')
        (956, 37, 1, "MID", 120), # Alexis Mac Allister
        (951, 37, 1, "MID", 45),  # Nicolás González (subbed out at 45')
        (946, 37, 1, "FWD", 120), # Lionel Messi
        (945, 37, 1, "FWD", 101), # Julián Álvarez (subbed out at 101')
        # Active Subs
        (955, 37, 0, "DEF", 77),  # Nicolás Otamendi (subbed in at 43')
        (941, 37, 0, "MID", 75),  # Leandro Paredes (subbed in at 45')
        (962, 37, 0, "DEF", 63),  # Nahuel Molina (subbed in at 57')
        (961, 37, 0, "DEF", 51),  # Facundo Medina (subbed in at 69')
        (953, 37, 0, "FWD", 51),  # Giuliano Simeone (subbed in at 69')
        (938, 37, 0, "DEF", 19),  # Marcos Senesi (subbed in at 101')
        # Unused Subs (9 players)
        (937, 37, 0, "GK", 0),
        (944, 37, 0, "MID", 0),
        (947, 37, 0, "MID", 0),
        (948, 37, 0, "GK", 0),
        (950, 37, 0, "MID", 0),
        (952, 37, 0, "FWD", 0),
        (954, 37, 0, "FWD", 0),
        (957, 37, 0, "FWD", 0),
        (958, 37, 0, "FWD", 0)
    ]
    
    for pid, tid, is_start, pos, mins in m104_players:
        rows.append([str(start_lineup_id), "104", str(pid), str(tid), str(is_start), pos, str(mins)])
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
    
    # Check if Match 104 stats are already in rows
    for row in rows:
        if row[0] == "104":
            print("Stats for Match 104 already appended.")
            return

    new_stats = [
        # match_id,team_id,possession_pct,total_shots,shots_on_target,corners,fouls,offsides,saves,player_of_the_match,data_source,last_updated
        ("104", "29", "65", "20", "12", "9", "21", "4", "0", "Ferran Torres", "Sofascore", "2026-07-19"),
        ("104", "37", "35", "2", "0", "4", "25", "1", "11", "Ferran Torres", "Sofascore", "2026-07-19")
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
    
    m104 = {
        "group": "Final",
        "date": "July 19, 2026",
        "home_team": "Spain",
        "away_team": "Argentina",
        "score": "1–0",
        "home_goals": [
          {
            "scorer": "Ferran Torres",
            "minute": "106'",
            "assist": "Nico Williams"
          }
        ],
        "away_goals": []
    }
    
    # Avoid duplicate appends if script is run twice
    match_keys = [(m['home_team'], m['away_team']) for m in data]
    
    if ("Spain", "Argentina") not in match_keys:
        data.append(m104)
        print("Appended Spain vs Argentina to JSON")
        
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
    print("All CSV and JSON files updated successfully for Match 104!")

if __name__ == "__main__":
    main()
