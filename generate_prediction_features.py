import os
import csv
import json
from datetime import datetime

# Get current workspace directory
workspace_dir = os.path.dirname(os.path.abspath(__file__))

def load_csv(filename):
    path = os.path.join(workspace_dir, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def safe_float(val, default=0.0):
    if not val or val.strip() == "":
        return default
    try:
        return float(val)
    except ValueError:
        return default

def safe_int(val, default=0):
    if not val or val.strip() == "":
        return default
    try:
        return int(val)
    except ValueError:
        return default

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        return None

def main():
    # Load all tables
    matches = load_csv("matches.csv")
    teams = load_csv("teams.csv")
    venues = load_csv("venues.csv")
    referees = load_csv("referees.csv")
    match_team_stats = load_csv("match_team_stats.csv")
    players = load_csv("squads_and_players.csv")

    # Map team details by team_id
    team_map = {}
    for t in teams:
        tid = int(t['team_id'])
        team_map[tid] = {
            'team_name': t['team_name'],
            'fifa_code': t['fifa_code'],
            'confederation': t['confederation'],
            'fifa_rank': safe_int(t['fifa_ranking_pre_tournament']),
            'elo': safe_float(t['elo_rating'])
        }

    # Map venue details by venue_id
    venue_map = {}
    for v in venues:
        vid = int(v['venue_id'])
        venue_map[vid] = {
            'stadium_name': v['stadium_name'],
            'city': v['city'],
            'country': v['country'],
            'capacity': safe_int(v['capacity']),
            'elevation': safe_float(v['elevation_meters'])
        }

    # Map referee details by referee_id
    referee_map = {}
    total_ref_cards = 0.0
    ref_count = 0
    for r in referees:
        rid = int(r['referee_id'])
        avg_cards = safe_float(r['avg_cards_per_game'])
        referee_map[rid] = {
            'name': r['name'],
            'avg_cards': avg_cards
        }
        if avg_cards > 0:
            total_ref_cards += avg_cards
            ref_count += 1
    global_avg_ref_cards = total_ref_cards / ref_count if ref_count > 0 else 4.0

    # Calculate squad metrics per team
    # average age, total caps, total market value, average market value
    team_players = {}
    for p in players:
        tid = int(p['team_id'])
        if tid not in team_players:
            team_players[tid] = []
        team_players[tid].append(p)

    team_squad_metrics = {}
    for tid in team_map.keys():
        squad = team_players.get(tid, [])
        if not squad:
            team_squad_metrics[tid] = {
                'avg_age': 26.5,  # default placeholder
                'total_caps': 0,
                'total_value': 0.0,
                'avg_value': 0.0
            }
            continue

        total_caps = sum(safe_int(p['caps']) for p in squad)
        total_value = sum(safe_float(p['market_value_eur']) for p in squad)
        avg_value = total_value / len(squad)

        # Age calculation relative to reference date (2026-06-11)
        ref_date = datetime(2026, 6, 11)
        total_age = 0.0
        valid_birth_dates = 0
        for p in squad:
            dob = parse_date(p['date_of_birth'])
            if dob:
                age = (ref_date - dob).days / 365.25
                total_age += age
                valid_birth_dates += 1
        avg_age = total_age / valid_birth_dates if valid_birth_dates > 0 else 26.5

        team_squad_metrics[tid] = {
            'avg_age': avg_age,
            'total_caps': total_caps,
            'total_value': total_value,
            'avg_value': avg_value
        }

    # Group team stats by (match_id, team_id)
    stats_map = {}
    for ts in match_team_stats:
        mid = int(ts['match_id'])
        tid = int(ts['team_id'])
        stats_map[(mid, tid)] = {
            'possession': safe_float(ts['possession_pct'], 50.0),
            'shots': safe_int(ts['total_shots']),
            'shots_on_target': safe_int(ts['shots_on_target']),
            'corners': safe_int(ts['corners']),
            'fouls': safe_int(ts['fouls']),
            'offsides': safe_int(ts['offsides']),
            'saves': safe_int(ts['saves'])
        }

    # Sort matches chronologically to calculate sequential rolling averages
    sorted_matches = sorted(matches, key=lambda m: (parse_date(m['date']) or datetime.min, safe_int(m['match_id'])))

    # Track team histories
    team_history = {tid: [] for tid in team_map.keys()}

    feature_headers = [
        "match_id", "date", "kickoff_time_utc", "stage_id", "is_knockout",
        "home_team_id", "home_team_name", "home_fifa_code", "home_confederation",
        "away_team_id", "away_team_name", "away_fifa_code", "away_confederation",
        "venue_id", "stadium_name", "venue_city", "venue_country", "venue_capacity", "venue_elevation_meters",
        "referee_id", "referee_name", "referee_avg_cards",
        "home_fifa_rank", "away_fifa_rank", "home_elo", "away_elo",
        "home_is_host", "away_is_host",
        "home_squad_avg_age", "away_squad_avg_age",
        "home_squad_total_caps", "away_squad_total_caps",
        "home_squad_total_value_eur", "away_squad_total_value_eur",
        "home_squad_avg_value_eur", "away_squad_avg_value_eur",
        "home_rest_days", "away_rest_days",
        "home_prev_avg_goals_scored", "home_prev_avg_goals_conceded",
        "away_prev_avg_goals_scored", "away_prev_avg_goals_conceded",
        "home_prev_avg_possession", "away_prev_avg_possession",
        "home_prev_avg_shots", "away_prev_avg_shots",
        "home_prev_avg_shots_on_target", "away_prev_avg_shots_on_target",
        "home_prev_avg_saves", "away_prev_avg_saves",
        "home_prev_avg_corners", "away_prev_avg_corners",
        "home_prev_avg_fouls", "away_prev_avg_fouls",
        "home_prev_avg_offsides", "away_prev_avg_offsides",
        "home_prev_avg_xg_scored", "home_prev_avg_xg_conceded",
        "away_prev_avg_xg_scored", "away_prev_avg_xg_conceded",
        # Target variables
        "home_score", "away_score", "result_type", "home_xg", "away_xg", "match_result"
    ]

    feature_rows = []

    for m in sorted_matches:
        if not m['home_team_id'] or not m['away_team_id']:
            continue
        mid = int(m['match_id'])
        m_date = parse_date(m['date'])
        h_id = int(m['home_team_id'])
        a_id = int(m['away_team_id'])
        vid = int(m['venue_id'])
        rid = safe_int(m['referee_id'])
        stage_id = int(m['stage_id'])

        # Basic Stage/Knockout info
        is_knockout = 1 if stage_id > 1 else 0

        # Referee info
        ref_info = referee_map.get(rid, {'name': 'Unknown', 'avg_cards': global_avg_ref_cards})

        # Team details
        h_team = team_map.get(h_id, {'team_name': 'Unknown', 'fifa_code': '', 'confederation': '', 'fifa_rank': 100, 'elo': 1500.0})
        a_team = team_map.get(a_id, {'team_name': 'Unknown', 'fifa_code': '', 'confederation': '', 'fifa_rank': 100, 'elo': 1500.0})

        # Venue details
        venue_info = venue_map.get(vid, {'stadium_name': '', 'city': '', 'country': '', 'capacity': 50000, 'elevation': 0.0})

        # Host country indicator
        home_country = venue_info['country']
        def check_is_host(team_name, country_code):
            if team_name == 'Mexico' and country_code == 'MEX':
                return 1
            if team_name == 'USA' and country_code == 'USA':
                return 1
            if team_name == 'Canada' and country_code == 'CAN':
                return 1
            return 0
        h_is_host = check_is_host(h_team['team_name'], home_country)
        a_is_host = check_is_host(a_team['team_name'], home_country)

        # Squad metrics
        h_squad = team_squad_metrics.get(h_id, {'avg_age': 26.5, 'total_caps': 0, 'total_value': 0.0, 'avg_value': 0.0})
        a_squad = team_squad_metrics.get(a_id, {'avg_age': 26.5, 'total_caps': 0, 'total_value': 0.0, 'avg_value': 0.0})

        # Calculate rest days
        h_history = team_history[h_id]
        a_history = team_history[a_id]

        h_rest_days = 10.0  # default for first match
        if h_history and m_date:
            last_match_date = h_history[-1]['date']
            if last_match_date:
                h_rest_days = (m_date - last_match_date).days

        a_rest_days = 10.0  # default for first match
        if a_history and m_date:
            last_match_date = a_history[-1]['date']
            if last_match_date:
                a_rest_days = (m_date - last_match_date).days

        # Calculate rolling stats (averages of all matches played *before* this one in the tournament)
        def get_rolling_stats(history):
            if not history:
                return {
                    'goals_scored': 0.0, 'goals_conceded': 0.0,
                    'possession': 50.0, 'shots': 12.0, 'shots_on_target': 4.0,
                    'saves': 3.0, 'corners': 5.0, 'fouls': 12.0, 'offsides': 2.0,
                    'xg_scored': 1.3, 'xg_conceded': 1.3
                }
            
            n = len(history)
            return {
                'goals_scored': sum(item['goals_scored'] for item in history) / n,
                'goals_conceded': sum(item['goals_conceded'] for item in history) / n,
                'possession': sum(item['possession'] for item in history) / n,
                'shots': sum(item['shots'] for item in history) / n,
                'shots_on_target': sum(item['shots_on_target'] for item in history) / n,
                'saves': sum(item['saves'] for item in history) / n,
                'corners': sum(item['corners'] for item in history) / n,
                'fouls': sum(item['fouls'] for item in history) / n,
                'offsides': sum(item['offsides'] for item in history) / n,
                'xg_scored': sum(item['xg_scored'] for item in history) / n,
                'xg_conceded': sum(item['xg_conceded'] for item in history) / n
            }

        h_rolling = get_rolling_stats(h_history)
        a_rolling = get_rolling_stats(a_history)

        # Get actual target values if match is completed
        home_score = ""
        away_score = ""
        result_type = ""
        home_xg = ""
        away_xg = ""
        match_result = ""

        is_completed = m['status'].strip() == 'Completed'
        if is_completed:
            home_score = safe_int(m['home_score'])
            away_score = safe_int(m['away_score'])
            result_type = m['result_type'].strip()
            home_xg = safe_float(m['home_xg'])
            away_xg = safe_float(m['away_xg'])

            if home_score > away_score:
                match_result = 'H'
            elif away_score > home_score:
                match_result = 'A'
            else:
                match_result = 'D'

        row = [
            mid, m['date'], m['kickoff_time_utc'], stage_id, is_knockout,
            h_id, h_team['team_name'], h_team['fifa_code'], h_team['confederation'],
            a_id, a_team['team_name'], a_team['fifa_code'], a_team['confederation'],
            vid, venue_info['stadium_name'], venue_info['city'], venue_info['country'], venue_info['capacity'], venue_info['elevation'],
            rid, ref_info['name'], ref_info['avg_cards'],
            h_team['fifa_rank'], a_team['fifa_rank'], h_team['elo'], a_team['elo'],
            h_is_host, a_is_host,
            h_squad['avg_age'], a_squad['avg_age'],
            h_squad['total_caps'], a_squad['total_caps'],
            h_squad['total_value'], a_squad['total_value'],
            h_squad['avg_value'], a_squad['avg_value'],
            h_rest_days, a_rest_days,
            h_rolling['goals_scored'], h_rolling['goals_conceded'],
            a_rolling['goals_scored'], a_rolling['goals_conceded'],
            h_rolling['possession'], a_rolling['possession'],
            h_rolling['shots'], a_rolling['shots'],
            h_rolling['shots_on_target'], a_rolling['shots_on_target'],
            h_rolling['saves'], a_rolling['saves'],
            h_rolling['corners'], a_rolling['corners'],
            h_rolling['fouls'], a_rolling['fouls'],
            h_rolling['offsides'], a_rolling['offsides'],
            h_rolling['xg_scored'], h_rolling['xg_conceded'],
            a_rolling['xg_scored'], a_rolling['xg_conceded'],
            # Target labels
            home_score, away_score, result_type, home_xg, away_xg, match_result
        ]
        feature_rows.append(row)

        # Update historical trackers for future matches ONLY if the current match is completed
        if is_completed:
            h_stats = stats_map.get((mid, h_id), {'possession': 50.0, 'shots': 12, 'shots_on_target': 4, 'corners': 5, 'fouls': 12, 'offsides': 2, 'saves': 3})
            a_stats = stats_map.get((mid, a_id), {'possession': 50.0, 'shots': 12, 'shots_on_target': 4, 'corners': 5, 'fouls': 12, 'offsides': 2, 'saves': 3})

            # Append current match performance to team's history
            team_history[h_id].append({
                'date': m_date,
                'goals_scored': home_score,
                'goals_conceded': away_score,
                'xg_scored': home_xg,
                'xg_conceded': away_xg,
                'possession': h_stats['possession'],
                'shots': h_stats['shots'],
                'shots_on_target': h_stats['shots_on_target'],
                'saves': h_stats['saves'],
                'corners': h_stats['corners'],
                'fouls': h_stats['fouls'],
                'offsides': h_stats['offsides']
            })

            team_history[a_id].append({
                'date': m_date,
                'goals_scored': away_score,
                'goals_conceded': home_score,
                'xg_scored': away_xg,
                'xg_conceded': home_xg,
                'possession': a_stats['possession'],
                'shots': a_stats['shots'],
                'shots_on_target': a_stats['shots_on_target'],
                'saves': a_stats['saves'],
                'corners': a_stats['corners'],
                'fouls': a_stats['fouls'],
                'offsides': a_stats['offsides']
            })

    # Write output prediction features dataset
    out_path = os.path.join(workspace_dir, "match_prediction_features.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(feature_headers)
        writer.writerows(feature_rows)

    print(f"Successfully generated prediction feature dataset at: {out_path}")
    print(f"Total rows (matches): {len(feature_rows)}")
    print(f"Features computed per match: {len(feature_headers) - 6}")

if __name__ == "__main__":
    main()
