import os
import csv
import sys

workspace_dir = os.path.dirname(os.path.abspath(__file__))

def load_csv(filename):
    path = os.path.join(workspace_dir, filename)
    if not os.path.exists(path):
        print(f"Error: Missing expected file: {filename}")
        sys.exit(1)
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = [row for row in reader]
        return headers, rows

def main():
    print("====================================================")
    print("FIFA World Cup 2026 - Live Results & Updated Stats - Integrity Verification")
    print("====================================================\n")

    # Load all tables
    teams_headers, teams = load_csv("teams.csv")
    venues_headers, venues = load_csv("venues.csv")
    stages_headers, stages = load_csv("tournament_stages.csv")
    referees_headers, referees = load_csv("referees.csv")
    matches_headers, matches = load_csv("matches.csv")
    players_headers, players = load_csv("squads_and_players.csv")
    events_headers, events = load_csv("match_events.csv")
    detailed_headers, detailed = load_csv("matches_detailed.csv")
    lineups_headers, lineups = load_csv("match_lineups.csv")

    errors = 0

    # 1. Row counts assertions
    print("[1/6] Verifying row counts...")
    if len(teams) != 48:
        print(f"[FAIL] Error: Expected exactly 48 teams, got {len(teams)}.")
        errors += 1
    else:
        print("  [OK] Found exactly 48 qualified teams.")

    if len(venues) != 16:
        print(f"[FAIL] Error: Expected exactly 16 stadiums, got {len(venues)}.")
        errors += 1
    else:
        print("  [OK] Found exactly 16 host venues.")

    if len(players) != 1248:
        print(f"[FAIL] Error: Expected exactly 1248 players (48 teams * 26 players), got {len(players)}.")
        errors += 1
    else:
        print("  [OK] Found exactly 1248 registered squad players.")

    if len(matches) != 89:
        print(f"[FAIL] Error: Expected exactly 89 matches, got {len(matches)}.")
        errors += 1
    else:
        print("  [OK] Found exactly 89 matches.")

    # 2. Key Uniqueness
    print("\n[2/6] Verifying primary key uniqueness...")
    def check_pks(rows, name):
        pks = [row[0] for row in rows]
        if len(pks) != len(set(pks)):
            print(f"[FAIL] Error: Duplicate primary keys found in {name}.")
            return 1
        return 0

    errors += check_pks(teams, "teams.csv")
    errors += check_pks(venues, "venues.csv")
    errors += check_pks(stages, "tournament_stages.csv")
    errors += check_pks(referees, "referees.csv")
    errors += check_pks(matches, "matches.csv")
    errors += check_pks(players, "squads_and_players.csv")
    errors += check_pks(events, "match_events.csv")
    errors += check_pks(lineups, "match_lineups.csv")
    if errors == 0:
        print("  [OK] All primary keys are unique.")

    # 3. Sets for quick lookup
    team_ids = {row[0] for row in teams}
    venue_ids = {row[0] for row in venues}
    stage_ids = {row[0] for row in stages}
    referee_ids = {row[0] for row in referees}
    match_ids = {row[0] for row in matches}
    player_ids = {row[0] for row in players}

    # Map player to team for validation
    player_to_team = {row[0]: row[1] for row in players}

    # 4. Referential Integrity
    print("\n[3/6] Verifying referential integrity (foreign keys)...")
    
    # Players
    for row in players:
        p_id, t_id = row[0], row[1]
        if t_id not in team_ids:
            print(f"[FAIL] Error: Player {p_id} references non-existent team_id {t_id}.")
            errors += 1

    # Matches
    for row in matches:
        m_id, stg_id, ven_id, home_id, away_id, ref_id = row[0], row[3], row[4], row[5], row[6], row[12]
        if stg_id not in stage_ids:
            print(f"[FAIL] Error: Match {m_id} references non-existent stage_id {stg_id}.")
            errors += 1
        if ven_id not in venue_ids:
            print(f"[FAIL] Error: Match {m_id} references non-existent venue_id {ven_id}.")
            errors += 1
        if home_id != "" and home_id not in team_ids:
            print(f"[FAIL] Error: Match {m_id} references non-existent home_team_id {home_id}.")
            errors += 1
        if away_id != "" and away_id not in team_ids:
            print(f"[FAIL] Error: Match {m_id} references non-existent away_team_id {away_id}.")
            errors += 1
        if ref_id not in referee_ids:
            print(f"[FAIL] Error: Match {m_id} references non-existent referee_id {ref_id}.")
            errors += 1
        potm_id = row[13] if len(row) > 13 else ""
        if potm_id != "" and potm_id not in player_ids:
            print(f"[FAIL] Error: Match {m_id} references non-existent player_of_the_match_id {potm_id}.")
            errors += 1

    # Events
    for row in events:
        e_id, m_id, t_id, p_id = row[0], row[1], row[4], row[5]
        if m_id not in match_ids:
            print(f"[FAIL] Error: Event {e_id} references non-existent match_id {m_id}.")
            errors += 1
        if t_id not in team_ids:
            print(f"[FAIL] Error: Event {e_id} references non-existent team_id {t_id}.")
            errors += 1
        if p_id not in player_ids:
            print(f"[FAIL] Error: Event {e_id} references non-existent player_id {p_id}.")
            errors += 1

    # Lineups Referential & Consistency Check
    match_lineups_count = {}
    match_starters_count = {}
    player_match_lineup_exists = {}
    
    for row in lineups:
        l_id, m_id, p_id, t_id, is_start, pos, mins = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        if m_id not in match_ids:
            print(f"[FAIL] Error: Lineup {l_id} references non-existent match_id {m_id}.")
            errors += 1
        if p_id not in player_ids:
            print(f"[FAIL] Error: Lineup {l_id} references non-existent player_id {p_id}.")
            errors += 1
        if t_id not in team_ids:
            print(f"[FAIL] Error: Lineup {l_id} references non-existent team_id {t_id}.")
            errors += 1
            
        # Verify player belongs to the team
        if p_id in player_to_team and player_to_team[p_id] != t_id:
            print(f"[FAIL] Error: Lineup {l_id} links player {p_id} to team {t_id}, but player belongs to team {player_to_team[p_id]}.")
            errors += 1
            
        # Track counts per match and team
        match_lineups_count.setdefault((m_id, t_id), 0)
        match_lineups_count[(m_id, t_id)] += 1
        
        if is_start == "1":
            match_starters_count.setdefault((m_id, t_id), 0)
            match_starters_count[(m_id, t_id)] += 1
            
        player_match_lineup_exists[(m_id, p_id)] = int(mins)

    if errors == 0:
        print("  [OK] Relational integrity is 100% correct.")

    # 5. Status & Scores Logic
    print("\n[4/6] Verifying match status and score logic...")
    completed_match_ids = set()
    for row in matches:
        m_id, h_score, a_score, status, h_xg, a_xg = row[0], row[7], row[8], row[9], row[10], row[11]
        if status == "Completed":
            completed_match_ids.add(m_id)
            if h_score == "" or a_score == "" or h_xg == "" or a_xg == "":
                print(f"[FAIL] Error: Match {m_id} is Completed but has empty scores or xG.")
                errors += 1
        elif status == "Scheduled":
            if h_score != "" or a_score != "" or h_xg != "" or a_xg != "":
                print(f"[FAIL] Error: Match {m_id} is Scheduled but has score or xG values filled.")
                errors += 1
    if errors == 0:
        print("  [OK] Match scores and statuses match perfectly.")

    # 6. Detailed Match Alignment
    print("\n[5/6] Verifying matches_detailed.csv alignment...")
    if len(detailed) != len(matches):
        print(f"[FAIL] Error: Row count mismatch in matches_detailed ({len(detailed)}) vs matches ({len(matches)}).")
        errors += 1
    else:
        # Check matching columns for sample
        for idx in range(len(matches)):
            norm = matches[idx]
            det = detailed[idx]
            if norm[0] != det[0] or norm[1] != det[1] or norm[9] != det[13]:
                print(f"[FAIL] Error: Alignment discrepancy at match index {idx} (ID: {norm[0]}).")
                errors += 1
                break
    if errors == 0:
        print("  [OK] Denormalized views map correctly.")

    # 7. Lineup Structure and Playtime Validation
    print("\n[6/8] Verifying match_lineups.csv structure and minutes...")
    for m_id in completed_match_ids:
        # Get home and away teams for this match
        match_row = [m for m in matches if m[0] == m_id][0]
        home_team_id, away_team_id = match_row[5], match_row[6]
        
        for team_id in [home_team_id, away_team_id]:
            # Each team must have exactly 26 players registered in the lineup for a match
            count = match_lineups_count.get((m_id, team_id), 0)
            if count != 26:
                print(f"[FAIL] Error: Match {m_id}, Team {team_id} has {count} players in lineup (expected exactly 26).")
                errors += 1
                
            # Each team must have exactly 11 starting players
            starters = match_starters_count.get((m_id, team_id), 0)
            if starters != 11:
                print(f"[FAIL] Error: Match {m_id}, Team {team_id} has {starters} starters (expected exactly 11).")
                errors += 1

    # Check that players with events have minutes played > 0
    for row in events:
        m_id, p_id = row[1], row[5]
        if m_id in completed_match_ids:
            mins_played = player_match_lineup_exists.get((m_id, p_id), 0)
            if mins_played <= 0:
                print(f"[FAIL] Error: Player {p_id} has events in Match {m_id} but has {mins_played} minutes played in lineups.")
                errors += 1

    if errors == 0:
        print("  [OK] Match lineups structure is 100% correct and aligned with match events.")

    # 8. Match Team Stats Validation
    print("\n[7/8] Verifying match_team_stats.csv...")
    stats_path = os.path.join(workspace_dir, "match_team_stats.csv")
    if os.path.exists(stats_path):
        stats_headers, stats = load_csv("match_team_stats.csv")
        match_stats_map = {}
        for row in stats:
            s_mid, s_tid = row[0], row[1]
            if s_mid not in match_ids:
                print(f"[FAIL] Error: match_team_stats row references non-existent match_id {s_mid}.")
                errors += 1
            if s_tid not in team_ids:
                print(f"[FAIL] Error: match_team_stats row references non-existent team_id {s_tid}.")
                errors += 1
            
            try:
                m_id_int = int(s_mid)
                pos_pct = int(row[2]) if row[2] != "" else None
                match_stats_map.setdefault(m_id_int, []).append(pos_pct)
            except ValueError:
                pass
                
        # Grouped validations
        for m_id, poss_list in match_stats_map.items():
            if len(poss_list) != 2:
                print(f"[FAIL] Error: Match {m_id} has {len(poss_list)} rows in match_team_stats (expected exactly 2).")
                errors += 1
            else:
                p1, p2 = poss_list[0], poss_list[1]
                if p1 is not None and p2 is not None:
                    total = p1 + p2
                    # FIFA 2026 uses a three-way possession split: Team A%, Team B%, and "In Contest".
                    # The two team percentages typically sum to 85-100%, with the remainder being contested ball time.
                    if total > 100 or total < 80:
                        print(f"[FAIL] Error: Match {m_id} possession percentages ({p1}% and {p2}%) sum to {total}%, outside valid range [80-100%].")
                        errors += 1
                        
        if errors == 0:
            print(f"  [OK] match_team_stats.csv has {len(stats)} rows with valid FK references, row counts, and possession totals.")
    else:
        print("  [SKIP] match_team_stats.csv not found (optional table).")

    # Final report
    print("\n[8/8] Summary:")
    if errors == 0:
        print("SUCCESS: The dataset passed all relational integrity constraints!")
        sys.exit(0)
    else:
        print(f"FAILED: Found {errors} database constraint violations.")
        sys.exit(1)


if __name__ == "__main__":
    main()
