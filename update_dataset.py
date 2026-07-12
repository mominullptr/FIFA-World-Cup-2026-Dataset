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
            # France vs Spain
            row[5] = "33"    # home_team_id
            row[6] = "29"    # away_team_id
        elif match_id == "102":
            # England vs Argentina
            row[5] = "45"    # home_team_id
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
        elif match_id == "102":
            # England vs Argentina
            row[7] = "England"
            row[8] = "ENG"
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
    
    new_events = [
        # Match 99
        (99, "36", "Goal", 36, 931),
        (99, "36", "Assist", 36, 920),
        (99, "45+2", "Goal", 45, 1154),
        (99, "45+2", "Assist", 45, 1162),
        (99, "93", "Goal", 45, 1154),
        (99, "117", "Yellow Card", 36, 913),
        # Match 100
        (100, "10", "Goal", 37, 956),
        (100, "10", "Assist", 37, 946),
        (100, "44", "Yellow Card", 8, 189), # Breel Embolo (189)
        (100, "67", "Goal", 8, 193),
        (100, "67", "Assist", 8, 195),
        (100, "72", "Red Card", 8, 189),
        (100, "72", "VAR Review", 8, 189),
        (100, "97", "Yellow Card", 37, 952),
        (100, "98", "Yellow Card", 37, 958),
        (100, "112", "Goal", 37, 945),
        (100, "112", "Assist", 37, 957),
        (100, "114", "Yellow Card", 37, 957),
        (100, "120+1", "Goal", 37, 958)
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
    
    # Match 99 players (Norway (36) and England (45))
    m99_players = [
        # Norway
        (911, 36, 1, "GK", 120),
        (936, 36, 1, "FWD", 60),
        (913, 36, 1, "DEF", 120),
        (927, 36, 1, "DEF", 90),
        (915, 36, 1, "DEF", 90),
        (918, 36, 1, "MID", 120),
        (920, 36, 1, "MID", 120),
        (916, 36, 1, "MID", 120),
        (917, 36, 1, "FWD", 68),
        (919, 36, 1, "FWD", 105),
        (931, 36, 1, "MID", 68),
        (924, 36, 0, "MID", 60),
        (930, 36, 0, "FWD", 52),
        (932, 36, 0, "MID", 52),
        (926, 36, 0, "DEF", 30),
        (914, 36, 0, "DEF", 30),
        (921, 36, 0, "FWD", 15),
        (912, 36, 0, "MID", 0),
        (922, 36, 0, "GK", 0),
        (923, 36, 0, "GK", 0),
        (925, 36, 0, "DEF", 0),
        (928, 36, 0, "MID", 0),
        (929, 36, 0, "MID", 0),
        (933, 36, 0, "MID", 0),
        (934, 36, 0, "DEF", 0),
        (935, 36, 0, "DEF", 0),
        # England
        (1145, 45, 1, "GK", 120),
        (1147, 45, 1, "DEF", 86),
        (1150, 45, 1, "DEF", 120),
        (1149, 45, 1, "DEF", 120),
        (1146, 45, 1, "DEF", 89),
        (1148, 45, 1, "MID", 45),
        (1152, 45, 1, "MID", 120),
        (1162, 45, 1, "FWD", 71),
        (1154, 45, 1, "MID", 114),
        (1164, 45, 1, "FWD", 45),
        (1153, 45, 1, "FWD", 120),
        (1151, 45, 0, "FWD", 75),
        (1165, 45, 0, "MID", 75),
        (1168, 45, 0, "DEF", 49),
        (1169, 45, 0, "DEF", 34),
        (1161, 45, 0, "MID", 31),
        (1159, 45, 0, "DEF", 6),
        (1155, 45, 0, "FWD", 0),
        (1156, 45, 0, "DEF", 0),
        (1157, 45, 0, "GK", 0),
        (1158, 45, 0, "MID", 0),
        (1160, 45, 0, "MID", 0),
        (1163, 45, 0, "FWD", 0),
        (1166, 45, 0, "FWD", 0),
        (1167, 45, 0, "GK", 0),
        (1170, 45, 0, "DEF", 0)
    ]
    
    for pid, tid, is_start, pos, mins in m99_players:
        rows.append([str(start_lineup_id), "99", str(pid), str(tid), str(is_start), pos, str(mins)])
        start_lineup_id += 1

    # Match 100 players (Argentina (37) and Switzerland (8))
    m100_players = [
        # Argentina
        (959, 37, 1, "GK", 120),
        (962, 37, 1, "DEF", 85),
        (949, 37, 1, "DEF", 105),
        (942, 37, 1, "DEF", 120),
        (939, 37, 1, "DEF", 78),
        (941, 37, 1, "MID", 110),
        (943, 37, 1, "MID", 85),
        (960, 37, 1, "MID", 90),
        (956, 37, 1, "MID", 120),
        (946, 37, 1, "FWD", 120),
        (945, 37, 1, "FWD", 120),
        (951, 37, 0, "MID", 42),
        (940, 37, 0, "DEF", 35),
        (958, 37, 0, "FWD", 35),
        (952, 37, 0, "FWD", 30),
        (955, 37, 0, "DEF", 15),
        (957, 37, 0, "FWD", 10),
        (937, 37, 0, "GK", 0),
        (938, 37, 0, "DEF", 0),
        (944, 37, 0, "MID", 0),
        (947, 37, 0, "MID", 0),
        (948, 37, 0, "GK", 0),
        (950, 37, 0, "MID", 0),
        (953, 37, 0, "FWD", 0),
        (954, 37, 0, "FWD", 0),
        (961, 37, 0, "DEF", 0),
        # Switzerland
        (183, 8, 1, "GK", 120),
        (195, 8, 1, "DEF", 90),
        (187, 8, 1, "DEF", 120),
        (186, 8, 1, "DEF", 120),
        (188, 8, 1, "MID", 96),
        (192, 8, 1, "MID", 120),
        (190, 8, 1, "MID", 115),
        (197, 8, 1, "MID", 86),
        (204, 8, 1, "MID", 86),
        (193, 8, 1, "FWD", 86),
        (189, 8, 1, "FWD", 72),
        (184, 8, 0, "DEF", 34),
        (185, 8, 0, "DEF", 34),
        (205, 8, 0, "FWD", 34),
        (200, 8, 0, "DEF", 30),
        (196, 8, 0, "MID", 24),
        (199, 8, 0, "FWD", 5),
        (194, 8, 0, "GK", 0),
        (203, 8, 0, "GK", 0),
        (191, 8, 0, "MID", 0),
        (198, 8, 0, "FWD", 0),
        (201, 8, 0, "FWD", 0),
        (202, 8, 0, "MID", 0),
        (206, 8, 0, "DEF", 0),
        (207, 8, 0, "DEF", 0),
        (208, 8, 0, "FWD", 0)
    ]
    
    for pid, tid, is_start, pos, mins in m100_players:
        rows.append([str(start_lineup_id), "100", str(pid), str(tid), str(is_start), pos, str(mins)])
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
    
    new_stats = [
        # match_id,team_id,possession,shots,shots_on_target,corners,fouls,offsides,saves,potm_name,data_source,last_verified
        ("99", "36", "47", "13", "5", "7", "10", "1", "6", "", "Sofascore", "2026-07-12"),
        ("99", "45", "53", "14", "8", "4", "8", "5", "4", "Jude Victor William Bellingham", "Sofascore", "2026-07-12"),
        ("100", "37", "59", "23", "7", "8", "14", "4", "4", "Julián Alvarez", "Sofascore", "2026-07-12"),
        ("100", "8", "41", "13", "5", "2", "18", "3", "4", "", "Sofascore", "2026-07-12")
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
    
    # We want to check if France-Morocco (M97) and Spain-Belgium (M98) are already in there.
    # Since len(data) was 96, they are not. Let's add them as well to keep the JSON fully up to date!
    
    m97 = {
        "group": "Quarter-finals",
        "date": "July 9, 2026",
        "home_team": "France",
        "away_team": "Morocco",
        "score": "2–0",
        "home_goals": [
          {
            "scorer": "Kylian Mbappé",
            "minute": "60'",
            "assist": "Ousmane Dembélé"
          },
          {
            "scorer": "Bradley Barcola",
            "minute": "66'",
            "assist": "Kylian Mbappé"
          }
        ],
        "away_goals": []
    }
    
    m98 = {
        "group": "Quarter-finals",
        "date": "July 10, 2026",
        "home_team": "Spain",
        "away_team": "Belgium",
        "score": "2–1",
        "home_goals": [
          {
            "scorer": "Dani Olmo",
            "minute": "30'"
          },
          {
            "scorer": "Lamine Yamal",
            "minute": "88'"
          }
        ],
        "away_goals": [
          {
            "scorer": "Charles De Ketelaere",
            "minute": "41'",
            "assist": "Loïs Openda"
          }
        ]
    }
    
    m99 = {
        "group": "Quarter-finals",
        "date": "July 11, 2026",
        "home_team": "Norway",
        "away_team": "England",
        "score": "1–2",
        "home_goals": [
          {
            "scorer": "Andreas Schjelderup",
            "minute": "36'",
            "assist": "Martin Ødegaard"
          }
        ],
        "away_goals": [
          {
            "scorer": "Jude Bellingham",
            "minute": "45+2'",
            "assist": "Anthony Gordon"
          },
          {
            "scorer": "Jude Bellingham",
            "minute": "93'"
          }
        ]
    }
    
    m100 = {
        "group": "Quarter-finals",
        "date": "July 12, 2026",
        "home_team": "Argentina",
        "away_team": "Switzerland",
        "score": "3–1",
        "home_goals": [
          {
            "scorer": "Alexis Mac Allister",
            "minute": "10'",
            "assist": "Lionel Messi"
          },
          {
            "scorer": "Julián Alvarez",
            "minute": "112'",
            "assist": "José Manuel López"
          },
          {
            "scorer": "Lautaro Martínez",
            "minute": "120+1'"
          }
        ],
        "away_goals": [
          {
            "scorer": "Dan Ndoye",
            "minute": "67'",
            "assist": "Ricardo Rodríguez"
          }
        ]
    }
    
    # Avoid duplicate appends if script is run twice
    match_keys = [(m['home_team'], m['away_team']) for m in data]
    
    if ("France", "Morocco") not in match_keys:
        data.append(m97)
        print("Appended France vs Morocco to JSON")
    if ("Spain", "Belgium") not in match_keys:
        data.append(m98)
        print("Appended Spain vs Belgium to JSON")
    if ("Norway", "England") not in match_keys:
        data.append(m99)
        print("Appended Norway vs England to JSON")
    if ("Argentina", "Switzerland") not in match_keys:
        data.append(m100)
        print("Appended Argentina vs Switzerland to JSON")
        
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
