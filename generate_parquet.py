import os
import duckdb

workspace_dir = os.path.dirname(os.path.abspath(__file__))
parquet_dir = os.path.join(workspace_dir, "parquet")
os.makedirs(parquet_dir, exist_ok=True)

csv_files = [
    "teams.csv",
    "venues.csv",
    "tournament_stages.csv",
    "referees.csv",
    "matches.csv",
    "squads_and_players.csv",
    "match_events.csv",
    "match_lineups.csv",
    "match_team_stats.csv",
    "player_stats.csv",
    "matches_detailed.csv",
    "match_prediction_features.csv",
    "match_prediction_features_X.csv",
    "match_prediction_targets_y.csv"
]

print("====================================================")
print("FIFA World Cup 2026 - Snappy Parquet Dataset Builder")
print("====================================================\n")

con = duckdb.connect()

for csv_name in csv_files:
    csv_path = os.path.join(workspace_dir, csv_name).replace("\\", "/")
    table_name = os.path.splitext(csv_name)[0]
    out_parquet = os.path.join(parquet_dir, f"{table_name}.parquet").replace("\\", "/")
    
    if os.path.exists(csv_path):
        query = f"""
            COPY (SELECT * FROM read_csv_auto('{csv_path}', header=True))
            TO '{out_parquet}' (FORMAT PARQUET, COMPRESSION SNAPPY);
        """
        con.execute(query)
        
        # Verify row count
        count_query = f"SELECT count(*) FROM read_parquet('{out_parquet}')"
        row_count = con.execute(count_query).fetchone()[0]
        size_bytes = os.path.getsize(out_parquet)
        print(f"  [OK] {csv_name:32s} -> {table_name}.parquet ({row_count:5d} rows, {size_bytes:7,d} bytes, Snappy)")
    else:
        print(f"  [FAIL] Missing CSV: {csv_name}")

con.close()
print(f"\n[SUCCESS] All Parquet files successfully generated in: {parquet_dir}")
