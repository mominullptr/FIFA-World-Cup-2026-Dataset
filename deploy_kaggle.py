import os
import shutil
import subprocess
import sys

workspace_dir = os.path.dirname(os.path.abspath(__file__))
dist_dir = os.path.join(workspace_dir, "kaggle_dist")

def main():
    print("====================================================")
    print("FIFA World Cup 2026 - Deploying clean files to Kaggle")
    print("====================================================\n")

    # 1. Re-create clean kaggle_dist directory
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)

    # 2. List files to copy
    files_to_copy = [
        "dataset-metadata.json",
        "teams.csv",
        "venues.csv",
        "tournament_stages.csv",
        "referees.csv",
        "matches.csv",
        "matches_detailed.csv",
        "squads_and_players.csv",
        "match_events.csv",
        "match_team_stats.csv",
        "match_lineups.csv",
        "player_stats.csv",
        "fifa_world_cup_2026.db"
    ]

    print("Copying clean dataset files...")
    for filename in files_to_copy:
        src = os.path.join(workspace_dir, filename)
        dst = os.path.join(dist_dir, filename)
        if os.path.exists(src):
            if filename == "dataset-metadata.json":
                import json
                with open(src, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                readme_path = os.path.join(workspace_dir, "README.md")
                if os.path.exists(readme_path):
                    with open(readme_path, "r", encoding="utf-8") as f:
                        meta["description"] = f.read()
                with open(dst, "w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=2)
                print(f"  [OK] Injected description into and copied: {filename}")
            else:
                shutil.copy2(src, dst)
                print(f"  [OK] Copied: {filename}")
        else:
            print(f"  [ERROR] Missing required file {filename}")
            sys.exit(1)

    # 3. Determine version message
    message = "Update matchday results"
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])

    # 4. Trigger Kaggle CLI metadata update first to sync title, description, keywords, and file resource details
    dataset_id = "mominullptr/fifa-world-cup-2026-dataset"
    venv_kaggle = os.path.join(workspace_dir, "venv", "bin", "kaggle.exe")
    if os.path.exists(venv_kaggle):
        meta_cmd = [venv_kaggle, "datasets", "metadata", "-p", dist_dir, "--update", dataset_id]
        kaggle_cmd = [venv_kaggle, "datasets", "version", "-p", dist_dir, "-m", message]
    else:
        # Fallback to global command if venv doesn't exist
        meta_cmd = ["kaggle", "datasets", "metadata", "-p", dist_dir, "--update", dataset_id]
        kaggle_cmd = ["kaggle", "datasets", "version", "-p", dist_dir, "-m", message]

    print(f"\nRunning Kaggle CLI Metadata Update: {' '.join(meta_cmd)}")
    try:
        meta_result = subprocess.run(meta_cmd, check=True, capture_output=True, text=True)
        print("\n--- Kaggle Metadata Output ---")
        print(meta_result.stdout)
        print(meta_result.stderr)
        print("------------------------------")
    except subprocess.CalledProcessError as e:
        print("\n[WARNING] Error running Kaggle Metadata CLI (may not be critical):")
        print(e.stdout)
        print(e.stderr)

    print(f"\nRunning Kaggle CLI Version Upload: {' '.join(kaggle_cmd)}")

    try:
        result = subprocess.run(kaggle_cmd, check=True, capture_output=True, text=True)
        print("\n--- Kaggle Version Output ---")
        print(result.stdout)
        print(result.stderr)
        print("-----------------------------")
        print("\n[SUCCESS] Deployment successful! Check progress at: https://www.kaggle.com/datasets/mominullptr/fifa-world-cup-2026-dataset")
    except subprocess.CalledProcessError as e:
        print("\n[ERROR] Error running Kaggle Version CLI:")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
