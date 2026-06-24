import os
import csv
import sqlite3

workspace_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(workspace_dir, "fifa_world_cup_2026.db")

# List of CSV files and target table names
csv_files = {
    "teams": "teams.csv",
    "venues": "venues.csv",
    "tournament_stages": "tournament_stages.csv",
    "referees": "referees.csv",
    "matches": "matches.csv",
    "squads_and_players": "squads_and_players.csv",
    "match_events": "match_events.csv",
    "match_team_stats": "match_team_stats.csv",
    "match_lineups": "match_lineups.csv"
}

def build_db():
    print("====================================================")
    print("FIFA World Cup 2026 - SQLite Database Builder")
    print("====================================================\n")
    
    # Remove existing db to rebuild clean
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("Removed existing database file.")
        except Exception as e:
            print(f"Error removing existing database: {e}")
            return
            
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enforce foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Convert each CSV to a table
    for table_name, csv_name in csv_files.items():
        csv_path = os.path.join(workspace_dir, csv_name)
        if os.path.exists(csv_path):
            try:
                with open(csv_path, "r", newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    
                    # Drop table if exists
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                    
                    # Create table dynamically
                    cols_str = ", ".join([f'"{h}" TEXT' for h in headers])
                    cursor.execute(f"CREATE TABLE {table_name} ({cols_str})")
                    
                    # Insert data rows
                    placeholders = ", ".join(["?"] * len(headers))
                    cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", reader)
                    
                print(f"  [OK] Converted {csv_name} to database table '{table_name}'")
            except Exception as e:
                print(f"  [ERROR] Failed to convert {csv_name}: {e}")
        else:
            print(f"  [SKIP] Optional or missing file: {csv_name}")
            
    # Create indexes for optimal query speed
    print("\nCreating indexes for query speed optimization...")
    try:
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_team ON squads_and_players(team_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_match_teams ON matches(home_team_id, away_team_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_match ON match_events(match_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_team_stats_match ON match_team_stats(match_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_lineups_match ON match_lineups(match_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_lineups_player ON match_lineups(player_id);")
        conn.commit()
        print("  [OK] Indexes successfully generated.")
    except Exception as e:
        print(f"  [WARNING] Index creation encountered errors: {e}")
        
    conn.close()
    print(f"\n[SUCCESS] SQLite Relational Database created at:\n{db_path}")

if __name__ == "__main__":
    build_db()
