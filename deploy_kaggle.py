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
        "README.md",
        "dataset-metadata.json",
        "teams.csv",
        "venues.csv",
        "tournament_stages.csv",
        "referees.csv",
        "matches.csv",
        "matches_detailed.csv",
        "squads_and_players.csv",
        "match_events.csv"
    ]

    print("Copying clean dataset files...")
    for filename in files_to_copy:
        src = os.path.join(workspace_dir, filename)
        dst = os.path.join(dist_dir, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✓ Copied: {filename}")
        else:
            print(f"  ❌ Error: Missing required file {filename}")
            sys.exit(1)

    # 3. Determine version message
    message = "Update matchday results"
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])

    # 4. Trigger Kaggle CLI version upload targeting kaggle_dist
    # We use the python binary inside the virtualenv to execute the kaggle script
    venv_python = os.path.join(workspace_dir, "venv", "bin", "python")
    if not os.path.exists(venv_python):
        # Fallback to standard command execution if venv doesn't exist
        kaggle_cmd = ["kaggle", "datasets", "version", "-p", dist_dir, "-m", message]
    else:
        # Run using virtual environment python
        kaggle_cmd = [venv_python, "-m", "kaggle", "datasets", "version", "-p", dist_dir, "-m", message]

    print(f"\nRunning Kaggle CLI: {' '.join(kaggle_cmd)}")
    try:
        result = subprocess.run(kaggle_cmd, check=True, capture_output=True, text=True)
        print("\n--- Kaggle Output ---")
        print(result.stdout)
        print(result.stderr)
        print("---------------------")
        print("\n✨ Deployment successful! Check progress at: https://www.kaggle.com/datasets/mominullptr/fifa-world-cup-2026-dataset")
    except subprocess.CalledProcessError as e:
        print("\n❌ Error running Kaggle CLI:")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
