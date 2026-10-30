import os
import sys
import shutil
import zipfile
import requests

workspace_dir = os.path.dirname(os.path.abspath(__file__))
zenodo_dist_dir = os.path.join(workspace_dir, "zenodo_dist")

RECORD_ID = "21596282"
BASE_URL = "https://zenodo.org/api"

def prepare_distribution():
    """Gathers all updated dataset files into a clean zenodo_dist directory."""
    if os.path.exists(zenodo_dist_dir):
        shutil.rmtree(zenodo_dist_dir)
    os.makedirs(zenodo_dist_dir, exist_ok=True)

    # 1. Copy SQLite database
    sqlite_src = os.path.join(workspace_dir, "sqlite_fifa_world_cup_2026.db")
    if os.path.exists(sqlite_src):
        shutil.copy2(sqlite_src, os.path.join(zenodo_dist_dir, "sqlite_fifa_world_cup_2026.db"))

    # 2. Copy CSV files
    csv_files = [
        "teams.csv", "venues.csv", "tournament_stages.csv", "referees.csv",
        "matches.csv", "squads_and_players.csv", "match_events.csv",
        "match_lineups.csv", "match_team_stats.csv", "player_stats.csv",
        "matches_detailed.csv", "match_prediction_features.csv"
    ]
    for f in csv_files:
        src = os.path.join(workspace_dir, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(zenodo_dist_dir, f))

    # 3. Create parquet zip and copy individual parquet files
    parquet_dir = os.path.join(workspace_dir, "parquet")
    zip_path = os.path.join(zenodo_dist_dir, "fifa_world_cup_2026_parquet_snappy.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in os.listdir(parquet_dir):
            if f.endswith(".parquet"):
                full_p = os.path.join(parquet_dir, f)
                zipf.write(full_p, arcname=f)
                # also copy individually
                shutil.copy2(full_p, os.path.join(zenodo_dist_dir, f))

    # 4. Copy Clean DOCX manuscript
    docx_src = os.path.join(workspace_dir, "FIFA_World_Cup_2026_Q1_Data_Descriptor.docx")
    if os.path.exists(docx_src):
        shutil.copy2(docx_src, os.path.join(zenodo_dist_dir, "FIFA_World_Cup_2026_Q1_Data_Descriptor.docx"))

    print(f"[OK] Zenodo distribution prepared at: {zenodo_dist_dir}")
    print(f"Total files prepared for Zenodo: {len(os.listdir(zenodo_dist_dir))}")

def upload_to_zenodo(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Creating a new version draft for Zenodo Record #{RECORD_ID}...")
    r = requests.post(f"{BASE_URL}/deposit/depositions/{RECORD_ID}/actions/newversion", headers=headers)
    if r.status_code != 201:
        print(f"[FAIL] Could not create new version: HTTP {r.status_code} -> {r.text}")
        return False
    
    new_data = r.json()
    new_dep_url = new_data["links"]["latest_draft"]
    new_dep_id = new_dep_url.split("/")[-1]
    
    # Get deposition details to retrieve bucket URL
    dep_res = requests.get(f"{BASE_URL}/deposit/depositions/{new_dep_id}", headers=headers)
    dep_json = dep_res.json()
    bucket_url = dep_json["links"]["bucket"]
    print(f"[OK] Created draft version ID: {new_dep_id}")
    print(f"Uploading files to bucket: {bucket_url} ...")

    for filename in os.listdir(zenodo_dist_dir):
        filepath = os.path.join(zenodo_dist_dir, filename)
        if os.path.isfile(filepath):
            print(f"  -> Uploading {filename} ({os.path.getsize(filepath):,} bytes)...")
            with open(filepath, "rb") as fp:
                up_res = requests.put(f"{bucket_url}/{filename}", data=fp, headers=headers)
                if up_res.status_code not in (200, 201):
                    print(f"     [WARNING] Upload issue on {filename}: HTTP {up_res.status_code}")
                else:
                    print(f"     [OK] Uploaded.")

    print(f"\n[SUCCESS] All files uploaded to Zenodo draft ID: {new_dep_id}")
    print(f"View and publish your deposit at: https://zenodo.org/uploads/{new_dep_id}")
    return True

if __name__ == "__main__":
    prepare_distribution()
    token = os.environ.get("ZENODO_TOKEN")
    if len(sys.argv) > 1:
        token = sys.argv[1]
    
    if token:
        upload_to_zenodo(token)
    else:
        print("\nNote: ZENODO_TOKEN not detected in arguments or environment.")
        print("To upload automatically via API:")
        print("  python deploy_zenodo.py <YOUR_ZENODO_PERSONAL_ACCESS_TOKEN>")
        print(f"Or drag-and-drop the files from '{zenodo_dist_dir}' directly on Zenodo via the 'New version' button.")
