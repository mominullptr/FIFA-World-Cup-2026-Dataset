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
    print("FIFA World Cup 2026 Dataset - Integrity Verification")
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

    if len(matches) != 72:
        print(f"[FAIL] Error: Expected exactly 72 matches, got {len(matches)}.")
        errors += 1
    else:
        print("  [OK] Found exactly 72 matches.")

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
    if errors == 0:
        print("  [OK] All primary keys are unique.")

    # 3. Sets for quick lookup
    team_ids = {row[0] for row in teams}
    venue_ids = {row[0] for row in venues}
    stage_ids = {row[0] for row in stages}
    referee_ids = {row[0] for row in referees}
    match_ids = {row[0] for row in matches}
    player_ids = {row[0] for row in players}

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
        if home_id not in team_ids:
            print(f"[FAIL] Error: Match {m_id} references non-existent home_team_id {home_id}.")
            errors += 1
        if away_id not in team_ids:
            print(f"[FAIL] Error: Match {m_id} references non-existent away_team_id {away_id}.")
            errors += 1
        if ref_id not in referee_ids:
            print(f"[FAIL] Error: Match {m_id} references non-existent referee_id {ref_id}.")
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

    if errors == 0:
        print("  [OK] Relational integrity is 100% correct.")

    # 5. Status & Scores Logic
    print("\n[4/6] Verifying match status and score logic...")
    for row in matches:
        m_id, h_score, a_score, status, h_xg, a_xg = row[0], row[7], row[8], row[9], row[10], row[11]
        if status == "Completed":
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

    # Final report
    print("\n[6/6] Summary:")
    if errors == 0:
        print("SUCCESS: The dataset passed all relational integrity constraints!")
        sys.exit(0)
    else:
        print(f"FAILED: Found {errors} database constraint violations.")
        sys.exit(1)


if __name__ == "__main__":
    main()
