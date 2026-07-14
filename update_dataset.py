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
    
    # Check if Match 101 events are already in rows
    for row in rows:
        if row[1] == "101":
            print("Events for Match 101 already appended.")
            return

    new_events = [
        # Match 101
        (101, "8", "Yellow Card", 33, 846),
        (101, "22", "VAR Review", 29, 747),
        (101, "22", "Goal", 29, 749),
        (101, "31", "Yellow Card", 29, 752),
        (101, "58", "Goal", 29, 740),
        (101, "58", "Assist", 29, 738),
        (101, "61", "VAR Review", 29, 747),
        (101, "86", "Yellow Card", 33, 842),
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
    
    # Check if Match 101 lineups are already in rows
    for row in rows:
        if row[1] == "101":
            print("Lineups for Match 101 already appended.")
            return

    # Match 101 players (France (33) and Spain (29))
    m101_players = [
        # France
        (848, 33, 1, "GK", 90),
        (837, 33, 1, "DEF", 90),
        (849, 33, 1, "DEF", 30),
        (836, 33, 1, "DEF", 90),
        (835, 33, 1, "DEF", 71),
        (840, 33, 1, "MID", 90),
        (846, 33, 1, "MID", 45),
        (839, 33, 1, "FWD", 90),
        (843, 33, 1, "FWD", 71),
        (844, 33, 1, "FWD", 57),
        (842, 33, 1, "FWD", 90),
        (858, 33, 0, "DEF", 60),
        (838, 33, 0, "MID", 45),
        (851, 33, 0, "DEF", 19),
        (856, 33, 0, "MID", 19),
        (852, 33, 0, "FWD", 33),
        (833, 33, 0, "GK", 0),
        (834, 33, 0, "DEF", 0),
        (841, 33, 0, "FWD", 0),
        (845, 33, 0, "MID", 0),
        (847, 33, 0, "DEF", 0),
        (850, 33, 0, "MID", 0),
        (853, 33, 0, "DEF", 0),
        (854, 33, 0, "FWD", 0),
        (855, 33, 0, "GK", 0),
        (857, 33, 0, "MID", 0),
        # Spain
        (751, 29, 1, "GK", 90),
        (740, 29, 1, "DEF", 84),
        (750, 29, 1, "DEF", 90),
        (742, 29, 1, "DEF", 90),
        (752, 29, 1, "DEF", 90),
        (744, 29, 1, "MID", 90),
        (736, 29, 1, "MID", 78),
        (738, 29, 1, "FWD", 78),
        (747, 29, 1, "FWD", 90),
        (749, 29, 1, "FWD", 74),
        (743, 29, 1, "MID", 84),
        (733, 29, 0, "DEF", 6),
        (748, 29, 0, "MID", 12),
        (734, 29, 0, "MID", 12),
        (735, 29, 0, "FWD", 16),
        (745, 29, 0, "FWD", 6),
        (729, 29, 0, "GK", 0),
        (730, 29, 0, "DEF", 0),
        (731, 29, 0, "DEF", 0),
        (732, 29, 0, "DEF", 0),
        (737, 29, 0, "MID", 0),
        (739, 29, 0, "FWD", 0),
        (741, 29, 0, "GK", 0),
        (746, 29, 0, "MID", 0),
        (753, 29, 0, "FWD", 0),
        (754, 29, 0, "FWD", 0),
    ]
    
    for pid, tid, is_start, pos, mins in m101_players:
        rows.append([str(start_lineup_id), "101", str(pid), str(tid), str(is_start), pos, str(mins)])
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
    
    # Check if Match 101 stats are already in rows
    for row in rows:
        if row[0] == "101":
            print("Stats for Match 101 already appended.")
            return

    new_stats = [
        # match_id,team_id,possession,shots,shots_on_target,corners,fouls,offsides,saves,potm_name,data_source,last_verified
        ("101", "33", "42", "10", "3", "2", "9", "4", "0", "", "Sofascore", "2026-07-14"),
        ("101", "29", "58", "10", "2", "1", "9", "5", "3", "Pedro Antonio Porro", "Sofascore", "2026-07-14")
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
    
    m101 = {
        "group": "Semi-finals",
        "date": "July 14, 2026",
        "home_team": "France",
        "away_team": "Spain",
        "score": "0–2",
        "home_goals": [],
        "away_goals": [
          {
            "scorer": "Mikel Oyarzabal",
            "minute": "22' (pen.)"
          },
          {
            "scorer": "Pedro Porro",
            "minute": "58'",
            "assist": "Dani Olmo"
          }
        ]
    }
    
    # Avoid duplicate appends if script is run twice
    match_keys = [(m['home_team'], m['away_team']) for m in data]
    
    if ("France", "Spain") not in match_keys:
        data.append(m101)
        print("Appended France vs Spain to JSON")
        
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
