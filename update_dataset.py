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
        if match_id == "99":
            # 99,2026-07-11,21:00,4,13,36,45,1,2,,,Completed,AET,0.77,0.96,5,1154
            row[7] = "1"     # home_score
            row[8] = "2"     # away_score
            row[9] = ""      # home_penalty_score
            row[10] = ""     # away_penalty_score
            row[11] = "Completed"
            row[12] = "AET"
            row[13] = "0.77" # home_xg
            row[14] = "0.96" # away_xg
            row[15] = "5"    # referee_id
            row[16] = "1154" # potm_player_id
        elif match_id == "100":
            # 100,2026-07-12,01:00,4,12,37,8,3,1,,,Completed,AET,2.0,0.53,17,945
            row[7] = "3"     # home_score
            row[8] = "1"     # away_score
            row[9] = ""      # home_penalty_score
            row[10] = ""     # away_penalty_score
            row[11] = "Completed"
            row[12] = "AET"
            row[13] = "2.0"  # home_xg
            row[14] = "0.53" # away_xg
            row[15] = "17"   # referee_id
            row[16] = "945"  # potm_player_id
        elif match_id == "101":
            # 101,2026-07-14,20:00,5,4,33,29,0,2,,,Completed,Regular,0.3,1.63,10,740
            row[5] = "33"    # home_team_id
            row[6] = "29"    # away_team_id
            row[7] = "0"     # home_score
            row[8] = "2"     # away_score
            row[9] = ""      # home_penalty_score
            row[10] = ""     # away_penalty_score
            row[11] = "Completed"
            row[12] = "Regular"
            row[13] = "0.3"  # home_xg
            row[14] = "1.63" # away_xg
            row[15] = "10"   # referee_id (Ivan Barton)
            row[16] = "740"  # potm_player_id (Pedro Antonio Porro)
        elif match_id == "102":
            # England vs Argentina
            row[5] = "45"    # home_team_id
            row[6] = "37"    # away_team_id
            row[7] = "1"     # home_score
            row[8] = "2"     # away_score
            row[9] = ""      # home_penalty_score
            row[10] = ""     # away_penalty_score
            row[11] = "Completed"
            row[12] = "Regular"
            row[13] = "0.54" # home_xg
            row[14] = "1.80" # away_xg
            row[15] = "6"    # referee_id (Danny Makkelie)
            row[16] = "946"  # potm_player_id (Lionel Andrés Messi)
        elif match_id == "103":
            # France vs England
            row[5] = "33"    # home_team_id
            row[6] = "45"    # away_team_id
        elif match_id == "104":
            # Spain vs Argentina
            row[5] = "29"    # home_team_id
            row[6] = "37"    # away_team_id

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
        if match_id == "99":
            # Norway vs England
            row[11] = "1"     # home_score
            row[12] = "2"     # away_score
            row[13] = ""      # home_penalty_score
            row[14] = ""      # away_penalty_score
            row[15] = "Completed"
            row[16] = "AET"
            row[17] = "0.77"  # home_xg
            row[18] = "0.96"  # away_xg
            row[19] = "Ørjan Haskjold Nyland"
            row[20] = "Jordan Lee Pickford"
            row[21] = "Jude Victor William Bellingham"
            row[22] = "Clément Turpin"
        elif match_id == "100":
            # Argentina vs Switzerland
            row[11] = "3"     # home_score
            row[12] = "1"     # away_score
            row[13] = ""      # home_penalty_score
            row[14] = ""      # away_penalty_score
            row[15] = "Completed"
            row[16] = "AET"
            row[17] = "2.0"   # home_xg
            row[18] = "0.53"  # away_xg
            row[19] = "Damián Emiliano Martinez"
            row[20] = "Gregor Kobel"
            row[21] = "Julián Alvarez"
            row[22] = "João Pinheiro"
        elif match_id == "101":
            # France vs Spain
            row[7] = "France"
            row[8] = "FRA"
            row[9] = "Spain"
            row[10] = "ESP"
            row[11] = "0"     # home_score
            row[12] = "2"     # away_score
            row[13] = ""      # home_penalty_score
            row[14] = ""      # away_penalty_score
            row[15] = "Completed"
            row[16] = "Regular"
            row[17] = "0.3"   # home_xg
            row[18] = "1.63"  # away_xg
            row[19] = "Mike Peterson Maignan"
            row[20] = "Unai Simon"
            row[21] = "Pedro Antonio Porro"
            row[22] = "Ivan Barton"
        elif match_id == "102":
            # England vs Argentina
            row[7] = "England"
            row[8] = "ENG"
            row[9] = "Argentina"
            row[10] = "ARG"
            row[11] = "1"     # home_score
            row[12] = "2"     # away_score
            row[13] = ""      # home_penalty_score
            row[14] = ""      # away_penalty_score
            row[15] = "Completed"
            row[16] = "Regular"
            row[17] = "0.54"  # home_xg
            row[18] = "1.80"  # away_xg
            row[19] = "Jordan Lee Pickford"
            row[20] = "Damián Emiliano Martinez"
            row[21] = "Lionel Andrés Messi"
            row[22] = "Danny Makkelie"
        elif match_id == "103":
            # France vs England
            row[7] = "France"
            row[8] = "FRA"
            row[9] = "England"
            row[10] = "ENG"
        elif match_id == "104":
            # Spain vs Argentina
            row[7] = "Spain"
            row[8] = "ESP"
            row[9] = "Argentina"
            row[10] = "ARG"

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
    
    start_event_id = int(rows[-1][0]) + 1
    
    # Check if Match 102 events are already in rows
    for row in rows:
        if row[1] == "102":
            print("Events for Match 102 already appended.")
            return

    new_events = [
        # Match 102
        (102, "37", "Yellow Card", 45, 1152),
        (102, "42", "Yellow Card", 37, 942),
        (102, "51", "Yellow Card", 37, 949),
        (102, "55", "Goal", 45, 1162),
        (102, "55", "Assist", 45, 1161),
        (102, "85", "Goal", 37, 960),
        (102, "85", "Assist", 37, 946),
        (102, "90+2", "Goal", 37, 958),
        (102, "90+2", "Assist", 37, 946),
    ]
    
    for mid, minute, etype, tid, pid in new_events:
        rows.append([str(start_event_id), str(mid), minute, etype, str(tid), str(pid)])
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
    
    start_lineup_id = int(rows[-1][0]) + 1
    
    # Check if Match 102 lineups are already in rows
    for row in rows:
        if row[1] == "102":
            print("Lineups for Match 102 already appended.")
            return

    # Match 102 players (England (45) and Argentina (37))
    m102_players = [
        # England (45)
        # Starting XI
        (1145, 45, 1, "GK", 90),
        (1149, 45, 1, "DEF", 90),
        (1150, 45, 1, "DEF", 90),
        (1168, 45, 1, "DEF", 82),
        (1169, 45, 1, "DEF", 90),
        (1148, 45, 1, "MID", 82),
        (1152, 45, 1, "MID", 90),
        (1161, 45, 1, "MID", 90),
        (1154, 45, 1, "MID", 90),
        (1153, 45, 1, "FWD", 90),
        (1162, 45, 1, "FWD", 72),
        # Active Subs
        (1146, 45, 0, "DEF", 18),
        (1147, 45, 0, "DEF", 8),
        (1159, 45, 0, "DEF", 8),
        (1155, 45, 0, "FWD", 0),
        (1166, 45, 0, "FWD", 0),
        # Unused Subs
        (1151, 45, 0, "FWD", 0),
        (1156, 45, 0, "DEF", 0),
        (1157, 45, 0, "GK", 0),
        (1158, 45, 0, "MID", 0),
        (1160, 45, 0, "MID", 0),
        (1163, 45, 0, "FWD", 0),
        (1164, 45, 0, "FWD", 0),
        (1165, 45, 0, "MID", 0),
        (1167, 45, 0, "GK", 0),
        (1170, 45, 0, "DEF", 0),

        # Argentina (37)
        # Starting XI
        (959, 37, 1, "GK", 90),
        (962, 37, 1, "DEF", 72),
        (949, 37, 1, "DEF", 90),
        (942, 37, 1, "DEF", 72),
        (939, 37, 1, "DEF", 81),
        (941, 37, 1, "MID", 64),
        (953, 37, 1, "FWD", 72),
        (960, 37, 1, "MID", 90),
        (956, 37, 1, "MID", 90),
        (945, 37, 1, "FWD", 90),
        (946, 37, 1, "FWD", 90),
        # Active Subs
        (951, 37, 0, "MID", 26),
        (955, 37, 0, "DEF", 18),
        (943, 37, 0, "MID", 18),
        (940, 37, 0, "DEF", 18),
        (958, 37, 0, "FWD", 9),
        # Unused Subs
        (937, 37, 0, "GK", 0),
        (938, 37, 0, "DEF", 0),
        (944, 37, 0, "MID", 0),
        (947, 37, 0, "MID", 0),
        (948, 37, 0, "GK", 0),
        (950, 37, 0, "MID", 0),
        (952, 37, 0, "FWD", 0),
        (954, 37, 0, "FWD", 0),
        (957, 37, 0, "FWD", 0),
        (961, 37, 0, "DEF", 0),
    ]
    
    for pid, tid, is_start, pos, mins in m102_players:
        rows.append([str(start_lineup_id), "102", str(pid), str(tid), str(is_start), pos, str(mins)])
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
    
    # Check if Match 102 stats are already in rows
    for row in rows:
        if row[0] == "102":
            print("Stats for Match 102 already appended.")
            return

    new_stats = [
        # match_id,team_id,possession,shots,shots_on_target,corners,fouls,offsides,saves,potm_name,data_source,last_verified
        ("102", "45", "36", "5", "2", "1", "11", "1", "3", "", "Sofascore", "2026-07-15"),
        ("102", "37", "64", "15", "5", "6", "15", "3", "1", "Lionel Andrés Messi", "Sofascore", "2026-07-15")
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
    
    m102 = {
        "group": "Semi-finals",
        "date": "July 15, 2026",
        "home_team": "England",
        "away_team": "Argentina",
        "score": "1–2",
        "home_goals": [
          {
            "scorer": "Anthony Gordon",
            "minute": "55'",
            "assist": "Morgan Rogers"
          }
        ],
        "away_goals": [
          {
            "scorer": "Enzo Fernández",
            "minute": "85'",
            "assist": "Lionel Messi"
          },
          {
            "scorer": "Lautaro Martínez",
            "minute": "90+2'",
            "assist": "Lionel Messi"
          }
        ]
    }
    
    # Avoid duplicate appends if script is run twice
    match_keys = [(m['home_team'], m['away_team']) for m in data]
    
    if ("England", "Argentina") not in match_keys:
        data.append(m102)
        print("Appended England vs Argentina to JSON")
        
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
    print("All CSV and JSON files updated successfully!")

if __name__ == "__main__":
    main()
