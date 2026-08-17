import os
import csv
import sqlite3

workspace_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(workspace_dir, "sqlite_fifa_world_cup_2026.db")

# List of CSV files and target table names (Ordered for FK creation)
csv_files = {
    "teams": "teams.csv",
    "venues": "venues.csv",
    "tournament_stages": "tournament_stages.csv",
    "referees": "referees.csv",
    "squads_and_players": "squads_and_players.csv",
    "matches": "matches.csv",
    "match_events": "match_events.csv",
    "match_team_stats": "match_team_stats.csv",
    "match_lineups": "match_lineups.csv",
    "player_stats": "player_stats.csv"
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

    # Explicit Schemas with Data Types, Primary Keys, and Foreign Keys
    table_ddl = {
        "teams": """
            CREATE TABLE teams (
                team_id INTEGER PRIMARY KEY,
                team_name TEXT NOT NULL,
                fifa_code TEXT NOT NULL,
                group_letter TEXT NOT NULL,
                confederation TEXT NOT NULL,
                fifa_ranking_pre_tournament INTEGER,
                elo_rating REAL,
                manager_name TEXT
            );
        """,
        "venues": """
            CREATE TABLE venues (
                venue_id INTEGER PRIMARY KEY,
                stadium_name TEXT NOT NULL,
                city TEXT NOT NULL,
                country TEXT NOT NULL,
                capacity INTEGER,
                latitude REAL,
                longitude REAL,
                elevation_meters INTEGER
            );
        """,
        "tournament_stages": """
            CREATE TABLE tournament_stages (
                stage_id INTEGER PRIMARY KEY,
                stage_name TEXT NOT NULL,
                is_knockout INTEGER
            );
        """,
        "referees": """
            CREATE TABLE referees (
                referee_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT NOT NULL,
                avg_cards_per_game REAL
            );
        """,
        "squads_and_players": """
            CREATE TABLE squads_and_players (
                player_id INTEGER PRIMARY KEY,
                team_id INTEGER NOT NULL,
                player_name TEXT NOT NULL,
                position TEXT NOT NULL,
                club_team TEXT,
                market_value_eur INTEGER,
                caps INTEGER,
                date_of_birth TEXT,
                height_cm INTEGER,
                goals INTEGER,
                FOREIGN KEY (team_id) REFERENCES teams(team_id)
            );
        """,
        "matches": """
            CREATE TABLE matches (
                match_id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                kickoff_time_utc TEXT NOT NULL,
                stage_id INTEGER NOT NULL,
                venue_id INTEGER NOT NULL,
                home_team_id INTEGER NOT NULL,
                away_team_id INTEGER NOT NULL,
                home_score INTEGER,
                away_score INTEGER,
                home_penalty_score INTEGER,
                away_penalty_score INTEGER,
                status TEXT NOT NULL,
                result_type TEXT,
                home_xg REAL,
                away_xg REAL,
                referee_id INTEGER NOT NULL,
                player_of_the_match_id INTEGER,
                FOREIGN KEY (stage_id) REFERENCES tournament_stages(stage_id),
                FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
                FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
                FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
                FOREIGN KEY (referee_id) REFERENCES referees(referee_id),
                FOREIGN KEY (player_of_the_match_id) REFERENCES squads_and_players(player_id)
            );
        """,
        "match_events": """
            CREATE TABLE match_events (
                event_id INTEGER PRIMARY KEY,
                match_id INTEGER NOT NULL,
                minute INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                team_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                FOREIGN KEY (team_id) REFERENCES teams(team_id),
                FOREIGN KEY (player_id) REFERENCES squads_and_players(player_id)
            );
        """,
        "match_team_stats": """
            CREATE TABLE match_team_stats (
                match_id INTEGER NOT NULL,
                team_id INTEGER NOT NULL,
                possession_pct REAL,
                total_shots INTEGER,
                shots_on_target INTEGER,
                corners INTEGER,
                fouls INTEGER,
                offsides INTEGER,
                saves INTEGER,
                player_of_the_match TEXT,
                data_source TEXT,
                last_updated TEXT,
                PRIMARY KEY (match_id, team_id),
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                FOREIGN KEY (team_id) REFERENCES teams(team_id)
            );
        """,
        "match_lineups": """
            CREATE TABLE match_lineups (
                lineup_id INTEGER PRIMARY KEY,
                match_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                team_id INTEGER NOT NULL,
                is_starting_xi INTEGER NOT NULL,
                tactical_position TEXT NOT NULL,
                minutes_played INTEGER NOT NULL,
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                FOREIGN KEY (team_id) REFERENCES teams(team_id),
                FOREIGN KEY (player_id) REFERENCES squads_and_players(player_id)
            );
        """,
        "player_stats": """
            CREATE TABLE player_stats (
                player_id INTEGER PRIMARY KEY,
                player_name TEXT NOT NULL,
                team_id INTEGER NOT NULL,
                position TEXT NOT NULL,
                matches_played INTEGER NOT NULL,
                matches_started INTEGER NOT NULL,
                minutes_played INTEGER NOT NULL,
                goals INTEGER NOT NULL,
                assists INTEGER NOT NULL,
                shots INTEGER,
                shots_on_target INTEGER,
                yellow_cards INTEGER NOT NULL,
                red_cards INTEGER NOT NULL,
                penalty_goals INTEGER NOT NULL,
                own_goals INTEGER NOT NULL,
                clean_sheets INTEGER,
                saves INTEGER,
                goals_conceded INTEGER,
                average_rating REAL,
                data_source TEXT,
                last_verified TEXT,
                FOREIGN KEY (player_id) REFERENCES squads_and_players(player_id),
                FOREIGN KEY (team_id) REFERENCES teams(team_id)
            );
        """
    }

    # Convert each CSV to a table
    for table_name, csv_name in csv_files.items():
        csv_path = os.path.join(workspace_dir, csv_name)
        if os.path.exists(csv_path):
            try:
                with open(csv_path, "r", newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                    cursor.execute(table_ddl[table_name])
                    
                    placeholders = ", ".join(["?"] * len(headers))
                    col_names = ", ".join([f'"{h}"' for h in headers])
                    cursor.executemany(f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})", reader)
                    
                print(f"  [OK] Converted {csv_name} to constrained table '{table_name}'")
            except Exception as e:
                print(f"  [ERROR] Failed to convert {csv_name}: {e}")
        else:
            print(f"  [SKIP] Optional or missing file: {csv_name}")
            
    # Create analytical views
    print("\nCreating analytical views 'vw_match_summaries' and 'vw_team_goal_summary'...")
    try:
        cursor.execute("DROP VIEW IF EXISTS vw_match_summaries;")
        cursor.execute("""
            CREATE VIEW vw_match_summaries AS
            SELECT 
                m.match_id,
                m.date,
                s.stage_name,
                v.stadium_name,
                v.city,
                ht.team_name AS home_team,
                at.team_name AS away_team,
                m.home_score,
                m.away_score,
                m.home_xg,
                m.away_xg,
                r.name AS referee_name
            FROM matches m
            JOIN tournament_stages s ON m.stage_id = s.stage_id
            JOIN venues v ON m.venue_id = v.venue_id
            JOIN teams ht ON m.home_team_id = ht.team_id
            JOIN teams at ON m.away_team_id = at.team_id
            JOIN referees r ON m.referee_id = r.referee_id;
        """)
        print("  [OK] View 'vw_match_summaries' created successfully.")

        cursor.execute("DROP VIEW IF EXISTS vw_team_goal_summary;")
        cursor.execute("""
            CREATE VIEW vw_team_goal_summary AS
            SELECT 
                t.team_id,
                t.team_name,
                t.confederation,
                COUNT(DISTINCT m.match_id) AS matches_played,
                COALESCE(pg.player_goals, 0) AS player_goals,
                COALESCE(pog.own_goals_conceded, 0) AS own_goals_conceded,
                COALESCE(oog.opponent_own_goals, 0) AS opponent_own_goals,
                COALESCE(mg.total_goals_scored, 0) AS total_goals_scored,
                COALESCE(mga.total_goals_conceded, 0) AS total_goals_conceded,
                COALESCE(mg.total_goals_scored, 0) - COALESCE(mga.total_goals_conceded, 0) AS goal_difference
            FROM teams t
            LEFT JOIN matches m ON m.home_team_id = t.team_id OR m.away_team_id = t.team_id
            LEFT JOIN (
                SELECT team_id, SUM(goals) AS player_goals 
                FROM player_stats 
                GROUP BY team_id
            ) pg ON t.team_id = pg.team_id
            LEFT JOIN (
                SELECT team_id, SUM(own_goals) AS own_goals_conceded 
                FROM player_stats 
                GROUP BY team_id
            ) pog ON t.team_id = pog.team_id
            LEFT JOIN (
                SELECT 
                    t_sub.team_id,
                    SUM(CASE WHEN m_sub.home_team_id = t_sub.team_id THEN m_sub.home_score ELSE m_sub.away_score END) AS total_goals_scored
                FROM teams t_sub
                JOIN matches m_sub ON m_sub.home_team_id = t_sub.team_id OR m_sub.away_team_id = t_sub.team_id
                WHERE m_sub.status = 'Completed'
                GROUP BY t_sub.team_id
            ) mg ON t.team_id = mg.team_id
            LEFT JOIN (
                SELECT 
                    t_sub.team_id,
                    SUM(CASE WHEN m_sub.home_team_id = t_sub.team_id THEN m_sub.away_score ELSE m_sub.home_score END) AS total_goals_conceded
                FROM teams t_sub
                JOIN matches m_sub ON m_sub.home_team_id = t_sub.team_id OR m_sub.away_team_id = t_sub.team_id
                WHERE m_sub.status = 'Completed'
                GROUP BY t_sub.team_id
            ) mga ON t.team_id = mga.team_id
            LEFT JOIN (
                SELECT 
                    CASE WHEN m_sub.home_team_id = me.team_id THEN m_sub.away_team_id ELSE m_sub.home_team_id END AS benefiting_team_id,
                    COUNT(*) AS opponent_own_goals
                FROM match_events me
                JOIN matches m_sub ON me.match_id = m_sub.match_id
                WHERE me.event_type = 'Own Goal'
                GROUP BY benefiting_team_id
            ) oog ON t.team_id = oog.benefiting_team_id
            GROUP BY t.team_id;
        """)
        print("  [OK] View 'vw_team_goal_summary' created successfully.")
    except Exception as e:
        print(f"  [ERROR] Failed to create views: {e}")

    # Check foreign key integrity
    cursor.execute("PRAGMA foreign_key_check;")
    fk_violations = cursor.fetchall()
    if fk_violations:
        print(f"\n[WARNING] Foreign key violations found: {len(fk_violations)}")
        for v in fk_violations:
            print("  ", v)
    else:
        print("\n[VERIFIED] 0 Foreign Key Violations in SQLite DB!")

    # Create indexes for optimal query speed
    print("\nCreating indexes for query speed optimization...")
    try:
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_team ON squads_and_players(team_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_match_teams ON matches(home_team_id, away_team_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_match ON match_events(match_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_team_stats_match ON match_team_stats(match_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_lineups_match ON match_lineups(match_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_lineups_player ON match_lineups(player_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ps_player ON player_stats(player_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ps_team ON player_stats(team_id);")
        conn.commit()
        print("  [OK] Indexes successfully generated.")
    except Exception as e:
        print(f"  [WARNING] Index creation encountered errors: {e}")
        
    conn.close()
    print(f"\n[SUCCESS] SQLite Relational Database created at:\n{db_path}")

if __name__ == "__main__":
    build_db()
