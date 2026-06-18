import os
import csv

# Directory and files
workspace_dir = r"C:\Users\ASUS\.gemini\antigravity\scratch\fifa-wc2026-dataset"
matches_path = os.path.join(workspace_dir, "matches.csv")
events_path = os.path.join(workspace_dir, "match_events.csv")
players_path = os.path.join(workspace_dir, "squads_and_players.csv")
teams_path = os.path.join(workspace_dir, "teams.csv")

def load_csv(path):
    if not os.path.exists(path):
        return [], []
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = [row for row in reader]
        return headers, rows

def save_csv(path, headers, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    print("====================================================")
    print("FIFA World Cup 2026 - Interactive Dataset Updater")
    print("====================================================\n")

    # Load data
    try:
        t_headers, teams = load_csv(teams_path)
        m_headers, matches = load_csv(matches_path)
        e_headers, events = load_csv(events_path)
        p_headers, players = load_csv(players_path)
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    # Map team IDs to Names
    team_map = {row[0]: row[1] for row in teams}
    # Map player IDs to Names and Roles
    player_map = {row[0]: (row[2], row[3]) for row in players}
    # Group players by team_id
    players_by_team = {}
    for row in players:
        p_id, t_id, name, pos = row[0], row[1], row[2], row[3]
        if t_id not in players_by_team:
            players_by_team[t_id] = []
        players_by_team[t_id].append((p_id, name, pos))

    # Find Scheduled matches
    scheduled_matches = [m for m in matches if m[9] == "Scheduled"]

    if not scheduled_matches:
        print("No matches are currently marked as 'Scheduled'. All games are completed!")
        return

    print("Scheduled Matches:")
    for idx, m in enumerate(scheduled_matches):
        m_id = m[0]
        date = m[1]
        home_name = team_map.get(m[5], "Unknown")
        away_name = team_map.get(m[6], "Unknown")
        print(f"[{idx + 1}] Match #{m_id} ({date}): {home_name} vs {away_name}")

    # Select Match
    try:
        choice = int(input("\nEnter the number of the match you want to complete: ")) - 1
        if choice < 0 or choice >= len(scheduled_matches):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    target_match = scheduled_matches[choice]
    m_id = target_match[0]
    home_id = target_match[5]
    away_id = target_match[6]
    home_name = team_map.get(home_id)
    away_name = team_map.get(away_id)

    print(f"\nUpdating: {home_name} vs {away_name}")
    
    # Input scores & xG
    try:
        home_score = int(input(f"Enter goals scored by {home_name}: "))
        away_score = int(input(f"Enter goals scored by {away_name}: "))
        home_xg = float(input(f"Enter Expected Goals (xG) for {home_name}: "))
        away_xg = float(input(f"Enter Expected Goals (xG) for {away_name}: "))
    except ValueError:
        print("Invalid input types. Scores must be integers and xG must be floats.")
        return

    # Update match values in matches.csv list
    for m in matches:
        if m[0] == m_id:
            m[7] = str(home_score)
            m[8] = str(away_score)
            m[9] = "Completed"
            m[10] = f"{home_xg:.2f}"
            m[11] = f"{away_xg:.2f}"
            break

    # Add Match Events
    new_events = []
    
    # Helper to add an event
    def add_event(team_id, team_name, default_type):
        print(f"\nSelect player from {team_name} for the event:")
        team_players = players_by_team.get(team_id, [])
        for p_idx, p in enumerate(team_players):
            print(f"[{p_idx + 1}] {p[1]} ({p[2]})")
            
        try:
            p_sel = int(input("Select player number: ")) - 1
            if p_sel < 0 or p_sel >= len(team_players):
                print("Invalid selection, skipping event.")
                return
            p_id = team_players[p_sel][0]
        except ValueError:
            print("Invalid input, skipping event.")
            return

        try:
            minute = int(input("Enter minute of event (1-90, or 90+ for extra time): "))
        except ValueError:
            minute = 45
            print("Defaulting minute to 45.")

        print("Select Event Type:")
        print(f"[1] {default_type}")
        print("[2] Yellow Card")
        print("[3] Red Card")
        print("[4] VAR Review")
        
        event_choices = {1: default_type, 2: "Yellow Card", 3: "Red Card", 4: "VAR Review"}
        try:
            evt_type_choice = int(input("Choice: "))
            evt_type = event_choices.get(evt_type_choice, default_type)
        except ValueError:
            evt_type = default_type

        new_events.append([None, m_id, minute, evt_type, team_id, p_id])

    # Prompt for Goals
    print("\n--- GOALS DETAILS ---")
    for g in range(home_score):
        print(f"\nGoal {g+1} for {home_name}:")
        add_event(home_id, home_name, "Goal")
    for g in range(away_score):
        print(f"\nGoal {g+1} for {away_name}:")
        add_event(away_id, away_name, "Goal")

    # Ask for Cards / Other events
    while True:
        more = input("\nDo you want to add another event (e.g. Card, VAR Review)? (y/n): ").strip().lower()
        if more != 'y':
            break
        team_choice = input(f"Which team? [1] {home_name} [2] {away_name}: ").strip()
        if team_choice == '1':
            add_event(home_id, home_name, "Yellow Card")
        elif team_choice == '2':
            add_event(away_id, away_name, "Yellow Card")
        else:
            print("Invalid team choice.")

    # Save match events
    if new_events:
        # Determine current max event_id
        max_event_id = 0
        if events:
            max_event_id = max(int(row[0]) for row in events)
        
        for ne in new_events:
            max_event_id += 1
            ne[0] = str(max_event_id)
            events.append(ne)
            
        # Re-sort events by match_id and minute
        # match_id is index 1, minute is index 2
        events.sort(key=lambda x: (int(x[1]), int(x[2])))
        # Reassign sequential event IDs
        for idx, row in enumerate(events):
            row[0] = str(idx + 1)

    # Load stages, venues, and referees to build the detailed matches
    try:
        stages_path = os.path.join(workspace_dir, "tournament_stages.csv")
        venues_path = os.path.join(workspace_dir, "venues.csv")
        referees_path = os.path.join(workspace_dir, "referees.csv")
        
        stg_headers, stages = load_csv(stages_path)
        ven_headers, venues = load_csv(venues_path)
        ref_headers, referees = load_csv(referees_path)
        
        # Build lookups
        team_lookup = {row[0]: (row[1], row[2]) for row in teams}
        venue_lookup = {row[0]: (row[1], row[2], row[3]) for row in venues}
        stage_lookup = {row[0]: row[1] for row in stages}
        referee_lookup = {row[0]: row[1] for row in referees}
        
        detailed_matches_headers = [
            "match_id", "date", "kickoff_time_utc", "stage_name", 
            "stadium_name", "city", "country", 
            "home_team_name", "home_fifa_code", 
            "away_team_name", "away_fifa_code", 
            "home_score", "away_score", "status", "home_xg", "away_xg", "referee_name"
        ]
        detailed_matches_data = []

        for match in matches:
            m_id_val = match[0]
            date_val = match[1]
            time_val = match[2]
            stg_id_val = match[3]
            ven_id_val = match[4]
            h_id_val = match[5]
            a_id_val = match[6]
            h_score_val = match[7]
            a_score_val = match[8]
            status_val = match[9]
            h_xg_val = match[10]
            a_xg_val = match[11]
            ref_id_val = match[12]
            
            stg_name = stage_lookup.get(stg_id_val, "Unknown")
            stadium, city, country = venue_lookup.get(ven_id_val, ("Unknown", "Unknown", "Unknown"))
            home_name_val, home_code_val = team_lookup.get(h_id_val, ("Unknown", "UNK"))
            away_name_val, away_code_val = team_lookup.get(a_id_val, ("Unknown", "UNK"))
            ref_name = referee_lookup.get(ref_id_val, "Unknown")
            
            detailed_matches_data.append([
                m_id_val, date_val, time_val, stg_name,
                stadium, city, country,
                home_name_val, home_code_val,
                away_name_val, away_code_val,
                h_score_val, a_score_val, status_val, h_xg_val, a_xg_val, ref_name
            ])
            
        detailed_path = os.path.join(workspace_dir, "matches_detailed.csv")
        save_csv(detailed_path, detailed_matches_headers, detailed_matches_data)
    except Exception as ex:
        print(f"Warning: Could not regenerate matches_detailed.csv: {ex}")

    # Save back to CSV
    save_csv(matches_path, m_headers, matches)
    save_csv(events_path, e_headers, events)
    print("\n====================================================")
    print("Success: Matches and Match Events updated relationally!")
    print("====================================================")

if __name__ == "__main__":
    main()

