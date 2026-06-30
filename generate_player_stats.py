import os
import csv
import json
import unicodedata

workspace_dir = os.path.dirname(os.path.abspath(__file__))

def normalize_name(name):
    normalized = unicodedata.normalize('NFKD', name)
    ascii_bytes = normalized.encode('ascii', 'ignore')
    return ascii_bytes.decode('ascii').lower().strip()

def names_match(scorer, player_name):
    s_norm = normalize_name(scorer)
    p_norm = normalize_name(player_name)
    
    # Custom overrides for spelling variants
    if 'oh hyeon-gyu' in s_norm and 'hyeongyu oh' in p_norm:
        return True
    if 'mohebi' in s_norm and 'mohebbi' in p_norm:
        return True
    if 'al-amri' in s_norm and 'alamri' in p_norm:
        return True
    if 'al-arab' in s_norm and 'alarab' in p_norm:
        return True
        
    s_clean = s_norm.replace('-', ' ')
    p_clean = p_norm.replace('-', ' ')
    
    s_words = set(w for w in s_clean.split() if len(w) > 2)
    p_words = set(w for w in p_clean.split() if len(w) > 2)
    
    if not s_words: s_words = set(s_clean.split())
    if not p_words: p_words = set(p_clean.split())
    
    if s_words.issubset(p_words) or p_words.issubset(s_words):
        return True
    if s_words & p_words:
        return True
    return False

def load_csv(filename):
    path = os.path.join(workspace_dir, filename)
    with open(path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def clean_team_name(name):
    return name.replace('Czech Republic', 'Czechia').replace('T\u00fcrkiye', 'Turkey').replace('Türkiye', 'Turkey').strip()

def main():
    # Load dataset files
    players = load_csv("squads_and_players.csv")
    player_info = {int(r['player_id']): r for r in players}

    teams = load_csv("teams.csv")
    teams_by_name = {normalize_name(r['team_name']): r['team_id'] for r in teams}

    def get_team_id_by_name(name):
        clean = normalize_name(clean_team_name(name))
        for t_clean, tid in teams_by_name.items():
            if t_clean in clean or clean in t_clean:
                return int(tid)
        return None

    matches = load_csv("matches.csv")
    completed_matches = [m for m in matches if m['status'] == 'Completed']
    matches_by_id = {int(m['match_id']): m for m in completed_matches}

    def get_match_id(home_name, away_name):
        h_id = get_team_id_by_name(home_name)
        a_id = get_team_id_by_name(away_name)
        for m in completed_matches:
            if int(m['home_team_id']) == h_id and int(m['away_team_id']) == a_id:
                return int(m['match_id'])
        return None

    # Load team stats for goalkeeper saves
    team_stats = load_csv("match_team_stats.csv")
    team_saves = {}
    for r in team_stats:
        mid = int(r['match_id'])
        tid = int(r['team_id'])
        saves = int(r['saves']) if r['saves'] != "" else 0
        team_saves[(mid, tid)] = saves

    # Load lineups and filter for completed matches
    lineups = load_csv("match_lineups.csv")
    player_lineups = {}
    
    # Store lineups per player to aggregate minutes played and match counts
    # player_id -> list of (match_id, team_id, started, minutes_played)
    lineups_by_player = {}
    for r in lineups:
        mid = int(r['match_id'])
        if mid not in matches_by_id:
            continue
        pid = int(r['player_id'])
        tid = int(r['team_id'])
        started = int(r['is_starting_xi'])
        mins = int(r['minutes_played'])
        
        if pid not in lineups_by_player:
            lineups_by_player[pid] = []
        lineups_by_player[pid].append((mid, tid, started, mins))
        player_lineups[(mid, pid)] = {
            'team_id': tid,
            'started': started,
            'minutes_played': mins
        }

    # Load events and filter for completed matches
    events = load_csv("match_events.csv")
    events_by_player = {}
    for r in events:
        mid = int(r['match_id'])
        if mid not in matches_by_id:
            continue
        pid = int(r['player_id'])
        etype = r['event_type']
        
        if pid not in events_by_player:
            events_by_player[pid] = []
        events_by_player[pid].append((mid, etype))

    # Load real match details for own goals and penalties
    details_path = os.path.join(workspace_dir, "real_match_details.json")
    with open(details_path, "r", encoding="utf-8") as f:
        real_matches = json.load(f)

    own_goals_by_player = {}
    penalties_by_player = {}

    for m in real_matches:
        mid = get_match_id(m['home_team'], m['away_team'])
        if not mid:
            continue
            
        for is_home, goals_list in [(True, m.get('home_goals', [])), (False, m.get('away_goals', []))]:
            for g in goals_list:
                scorer = g['scorer']
                minute = g['minute']
                is_og = 'o.g.' in minute
                is_pen = 'pen.' in minute
                
                if not (is_og or is_pen):
                    continue
                    
                if is_home:
                    scorer_team_name = m['away_team'] if is_og else m['home_team']
                else:
                    scorer_team_name = m['home_team'] if is_og else m['away_team']
                    
                scorer_team_id = get_team_id_by_name(scorer_team_name)
                if not scorer_team_id:
                    continue
                    
                matched_pid = None
                for (lm_id, lp_id), l_info in player_lineups.items():
                    if lm_id == mid and l_info['team_id'] == scorer_team_id:
                        p_name = player_info[lp_id]['player_name']
                        if names_match(scorer, p_name):
                            matched_pid = lp_id
                            break
                            
                if matched_pid:
                    if is_og:
                        own_goals_by_player[matched_pid] = own_goals_by_player.get(matched_pid, 0) + 1
                    if is_pen:
                        penalties_by_player[matched_pid] = penalties_by_player.get(matched_pid, 0) + 1
                else:
                    print(f"Warning: Could not match scorer '{scorer}' in Match {mid} ({m['home_team']} vs {m['away_team']})")

    # Define schema headers for player_stats.csv
    headers = [
        "player_id", "player_name", "team_id", "position", "matches_played", "matches_started",
        "minutes_played", "goals", "assists", "shots", "shots_on_target",
        "yellow_cards", "red_cards", "penalty_goals", "own_goals",
        "clean_sheets", "saves", "goals_conceded", "average_rating",
        "data_source", "last_verified"
    ]

    rows = []
    for p in players:
        pid = int(p['player_id'])
        pname = p['player_name']
        tid = int(p['team_id'])
        ppos = p['position']

        # Get lineups details
        p_lineups = lineups_by_player.get(pid, [])
        matches_played = sum(1 for item in p_lineups if item[3] > 0)
        matches_started = sum(1 for item in p_lineups if item[2] == 1 and item[3] > 0)
        minutes_played = sum(item[3] for item in p_lineups)

        # Get events details
        p_events = events_by_player.get(pid, [])
        yellows = sum(1 for item in p_events if item[1] == "Yellow Card")
        reds = sum(1 for item in p_events if item[1] == "Red Card")
        assists = sum(1 for item in p_events if item[1] == "Assist")
        goal_events = sum(1 for item in p_events if item[1] == "Goal")

        ogs = own_goals_by_player.get(pid, 0)
        goals = max(0, goal_events - ogs)
        pens_scored = penalties_by_player.get(pid, 0)

        # Goalkeeper specific fields
        saves = ""
        goals_conceded = ""
        clean_sheets = ""

        if ppos == "GK":
            saves = 0
            goals_conceded = 0
            clean_sheets = 0
            
            # Goalkeepers only receive stats for matches they played
            for mid, ptid, started, mins in p_lineups:
                if mins > 0 and started == 1:
                    saves += team_saves.get((mid, ptid), 0)
                    
                    match_row = matches_by_id[mid]
                    h_score = int(match_row['home_score'])
                    a_score = int(match_row['away_score'])
                    h_tid = int(match_row['home_team_id'])
                    
                    match_conceded = a_score if ptid == h_tid else h_score
                    goals_conceded += match_conceded
                    
                    if match_conceded == 0:
                        clean_sheets += 1
            
            # If the goalkeeper has not played any match, saves, goals_conceded, clean_sheets should be 0
            # (which is already set above)
        
        row = {
            "player_id": pid,
            "player_name": pname,
            "team_id": tid,
            "position": ppos,
            "matches_played": matches_played,
            "matches_started": matches_started,
            "minutes_played": minutes_played,
            "goals": goals,
            "assists": assists,
            "shots": "",
            "shots_on_target": "",
            "yellow_cards": yellows,
            "red_cards": reds,
            "penalty_goals": pens_scored,
            "own_goals": ogs,
            "clean_sheets": clean_sheets,
            "saves": saves,
            "goals_conceded": goals_conceded,
            "average_rating": "",
            "data_source": "sofascore.com" if matches_played > 0 else "",
            "last_verified": "2026-07-01"
        }
        rows.append([row[h] for h in headers])

    # Sort rows by player_id
    rows.sort(key=lambda r: r[0])

    # Write output CSV
    output_path = os.path.join(workspace_dir, "player_stats.csv")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Successfully generated {len(rows)} player cumulative statistics rows in player_stats.csv")

if __name__ == "__main__":
    main()
