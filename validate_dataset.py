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
    print("FIFA World Cup 2026 Dataset- Live & Updated Stats - Integrity Verification")
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
    ps_headers, ps_rows = load_csv("player_stats.csv")

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

    if len(matches) not in (96, 100, 102, 104):
        print(f"[FAIL] Error: Expected 96, 100, 102, or 104 matches, got {len(matches)}.")
        errors += 1
    else:
        print(f"  [OK] Found valid match count: {len(matches)}.")

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
    errors += check_pks(ps_rows, "player_stats.csv")
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
        m_id, stg_id, ven_id, home_id, away_id, ref_id = row[0], row[3], row[4], row[5], row[6], row[15]
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
        if ref_id != "" and ref_id not in referee_ids:
            print(f"[FAIL] Error: Match {m_id} references non-existent referee_id {ref_id}.")
            errors += 1
        potm_id = row[16] if len(row) > 16 else ""
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
        m_id, h_score, a_score, status, h_xg, a_xg = row[0], row[7], row[8], row[11], row[13], row[14]
        result_type = row[12]
        h_pen, a_pen = row[9], row[10]
        if status == "Completed":
            completed_match_ids.add(m_id)
            if h_score == "" or a_score == "" or h_xg == "" or a_xg == "":
                print(f"[FAIL] Error: Match {m_id} is Completed but has empty scores or xG.")
                errors += 1
            # Validate result_type
            if result_type not in ('Regular', 'AET', 'Penalties'):
                print(f"[FAIL] Error: Match {m_id} is Completed but has invalid result_type '{result_type}'.")
                errors += 1
            # If Penalties, penalty scores must be filled
            if result_type == 'Penalties':
                if h_pen == "" or a_pen == "":
                    print(f"[FAIL] Error: Match {m_id} has result_type=Penalties but empty penalty scores.")
                    errors += 1
            # If not Penalties, penalty scores must be empty
            if result_type != 'Penalties':
                if h_pen != "" or a_pen != "":
                    print(f"[FAIL] Error: Match {m_id} has penalty scores but result_type is not Penalties.")
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
            if norm[0] != det[0] or norm[1] != det[1] or norm[11] != det[15]:
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
    # (Skip penalty shootout events — players may take penalties without having played)
    for row in events:
        m_id, p_id, e_type = row[1], row[5], row[3]
        if e_type in ('Penalty Shootout Goal', 'Penalty Shootout Miss'):
            continue
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

    # 8. Player Stats Validation
    print("\n[8/9] Verifying player_stats.csv...")
    ps_path = os.path.join(workspace_dir, "player_stats.csv")
    if os.path.exists(ps_path):
        # a. Row count: should have exactly 1248 rows
        print(f"  Found {len(ps_rows)} player statistics rows.")
        if len(ps_rows) != 1248:
            print(f"[FAIL] Error: Expected exactly 1248 rows in player_stats.csv, got {len(ps_rows)}.")
            errors += 1

        # b. Uniqueness of player_id (checked via PK check, but double verifying here)
        ps_ids = set()
        for row in ps_rows:
            pid = row[0]
            if pid in ps_ids:
                print(f"[FAIL] Error: Duplicate player_id in player_stats: {pid}")
                errors += 1
            ps_ids.add(pid)
        if errors == 0:
            print("  [OK] Player IDs are unique.")

        # c. Referential integrity
        for row in ps_rows:
            pid, pname, tid = row[0], row[1], row[2]
            if pid not in player_ids:
                print(f"[FAIL] Error: player_stats row references non-existent player_id {pid}.")
                errors += 1
            if tid not in team_ids:
                print(f"[FAIL] Error: player_stats row references non-existent team_id {tid}.")
                errors += 1

        # d. Value constraints (no negative numbers, and outfield/goalkeeper rules)
        player_positions = {row[0]: row[3] for row in players}

        for row in ps_rows:
            pid = row[0]
            pos = player_positions.get(pid, "")

            # Check Goalkeeper rules
            saves_val = row[16]
            conceded_val = row[17]
            cs_val = row[15]

            if pos != "GK":
                if saves_val != "" or conceded_val != "" or cs_val != "":
                    print(f"[FAIL] Error: Outfield player {pid} ({pos}) has non-NULL goalkeeper statistics: saves='{saves_val}', conceded='{conceded_val}', clean_sheets='{cs_val}'.")
                    errors += 1
            else:
                if saves_val == "" or conceded_val == "" or cs_val == "":
                    print(f"[FAIL] Error: Goalkeeper {pid} has NULL goalkeeper statistics.")
                    errors += 1

            # Validate that all unverified columns are NULL (empty)
            null_cols = [9, 10, 18]
            for col_idx in null_cols:
                if row[col_idx] != "":
                    print(f"[FAIL] Error: Player {pid} has non-NULL value '{row[col_idx]}' in unverified column index {col_idx}.")
                    errors += 1

            # Check that numeric columns contain no negative values
            numeric_cols = [4, 5, 6, 7, 8, 11, 12, 13, 14]
            if pos == "GK":
                numeric_cols += [15, 16, 17]
            for col_idx in numeric_cols:
                val = row[col_idx]
                if val != "":
                    try:
                        int_val = int(val)
                        if int_val < 0:
                            print(f"[FAIL] Error: Player {pid} has negative value {int_val} in column index {col_idx}.")
                            errors += 1
                    except ValueError:
                        print(f"[FAIL] Error: Player {pid} has non-integer value '{val}' in numeric column index {col_idx}.")
                        errors += 1

        # e. Alignment with match_events: goals, assists, yellow_cards, red_cards
        ps_lookup = {row[0]: row for row in ps_rows}
        ev_counts = {}
        for row in events:
            e_mid, e_pid, e_type = row[1], row[5], row[3]
            if e_mid not in completed_match_ids:
                continue
            # Skip penalty shootout events — they don't count toward player goal tallies
            if e_type in ('Penalty Shootout Goal', 'Penalty Shootout Miss'):
                continue
            ev_counts.setdefault(e_pid, {"Goal": 0, "Assist": 0, "Yellow Card": 0, "Red Card": 0})
            if e_type in ev_counts[e_pid]:
                ev_counts[e_pid][e_type] += 1

        for pid, counts in ev_counts.items():
            ps_row = ps_lookup.get(pid)
            if not ps_row:
                print(f"[FAIL] Error: Player {pid} has events but does not exist in player_stats.csv.")
                errors += 1
                continue
            
            ps_goals = int(ps_row[7]) if ps_row[7] != "" else 0
            ps_assists = int(ps_row[8]) if ps_row[8] != "" else 0
            ps_yellows = int(ps_row[11]) if ps_row[11] != "" else 0
            ps_reds = int(ps_row[12]) if ps_row[12] != "" else 0
            ps_ogs = int(ps_row[14]) if ps_row[14] != "" else 0

            expected_goals = max(0, counts["Goal"] - ps_ogs)
            if ps_goals != expected_goals:
                print(f"[FAIL] Error: Player {pid} goals={ps_goals} but expected {expected_goals} (events={counts['Goal']}, ogs={ps_ogs}).")
                errors += 1
            if ps_assists != counts["Assist"]:
                print(f"[FAIL] Error: Player {pid} assists={ps_assists} but expected {counts['Assist']}.")
                errors += 1
            if ps_yellows != counts["Yellow Card"]:
                print(f"[FAIL] Error: Player {pid} yellow_cards={ps_yellows} but expected {counts['Yellow Card']}.")
                errors += 1
            if ps_reds != counts["Red Card"]:
                print(f"[FAIL] Error: Player {pid} red_cards={ps_reds} but expected {counts['Red Card']}.")
                errors += 1

        # f. Alignment with match_lineups: minutes_played, matches_played, matches_started
        lu_counts = {}
        for row in lineups:
            m_id, p_id, is_start, mins = row[1], row[2], row[4], row[6]
            if m_id not in completed_match_ids:
                continue
            lu_counts.setdefault(p_id, {"played": 0, "started": 0, "minutes": 0})
            mins_val = int(mins)
            if mins_val > 0:
                lu_counts[p_id]["played"] += 1
                lu_counts[p_id]["minutes"] += mins_val
                if is_start == "1":
                    lu_counts[p_id]["started"] += 1

        for row in ps_rows:
            pid = row[0]
            ps_played = int(row[4]) if row[4] != "" else 0
            ps_started = int(row[5]) if row[5] != "" else 0
            ps_mins = int(row[6]) if row[6] != "" else 0

            expected = lu_counts.get(pid, {"played": 0, "started": 0, "minutes": 0})
            if ps_played != expected["played"]:
                print(f"[FAIL] Error: Player {pid} matches_played={ps_played} but lineups say {expected['played']}.")
                errors += 1
            if ps_started != expected["started"]:
                print(f"[FAIL] Error: Player {pid} matches_started={ps_started} but lineups say {expected['started']}.")
                errors += 1
            if ps_mins != expected["minutes"]:
                print(f"[FAIL] Error: Player {pid} minutes_played={ps_mins} but lineups say {expected['minutes']}.")
                errors += 1

        if errors == 0:
            print("  [OK] player_stats.csv passes all integrity checks.")
    else:
        print("  [FAIL] player_stats.csv not found.")
        errors += 1

    # Final report
    print("\n[9/9] Summary:")
    if errors == 0:
        print("SUCCESS: The dataset passed all relational integrity constraints!")
        sys.exit(0)
    else:
        print(f"FAILED: Found {errors} database constraint violations.")
        sys.exit(1)


if __name__ == "__main__":
    main()
