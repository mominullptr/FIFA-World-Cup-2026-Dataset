import os
import shutil
import sys
from huggingface_hub import HfApi

workspace_dir = os.path.dirname(os.path.abspath(__file__))
dist_dir = os.path.join(workspace_dir, "hf_dist")

def main():
    print("====================================================")
    print("FIFA World Cup 2026 - Deploying clean files to Hugging Face")
    print("====================================================\n")

    # 1. Re-create clean hf_dist directory
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)

    # 2. List files to copy
    files_to_copy = [
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
        "match_prediction_features.csv",
        "fifa_world_cup_2026.db",
        "schema_relationships.md"
    ]

    print("Copying clean dataset files...")
    for filename in files_to_copy:
        src = os.path.join(workspace_dir, filename)
        dst = os.path.join(dist_dir, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  [OK] Copied: {filename}")
        else:
            print(f"  [ERROR] Missing required file {filename}")
            sys.exit(1)


    # Copy README.md with frontmatter
    readme_src = os.path.join(workspace_dir, "README.md")
    readme_dst = os.path.join(dist_dir, "README.md")
    if os.path.exists(readme_src):
        with open(readme_src, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Add YAML frontmatter to README if not present
        frontmatter = "---\ntitle: FIFA World Cup 2026 Dataset- Live & Updated Stats\nemoji: ⚽\ncolorFrom: blue\ncolorTo: green\nsdk: static\npinned: false\n---\n\n"
        if not content.strip().startswith("---"):
            content = frontmatter + content
            
        with open(readme_dst, "w", encoding="utf-8") as f:
            f.write(content)
        print("  [OK] Added YAML frontmatter and copied README.md")

    # 3. Determine commit message
    message = "Update matchday results"
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])

    # 4. Upload to Hugging Face
    token = os.environ.get("HF_TOKEN")
    repo_id = os.environ.get("HF_REPO_ID")
    
    try:
        api = HfApi(token=token)
        if not repo_id:
            username = api.whoami()["name"]
            repo_id = f"{username}/fifa-world-cup-2026-dataset"
    except Exception:
        if not repo_id:
            repo_id = "Mominullptr/fifa-world-cup-2026-dataset"

    print(f"\nTarget Repository: {repo_id}")
    
    try:
        api = HfApi(token=token)
        print("Creating repository if it doesn't exist...")
        api.create_repo(repo_id=repo_id, repo_type="dataset", exist_ok=True)
        
        print("Uploading files to Hugging Face Hub...")
        api.upload_folder(
            folder_path=dist_dir,
            repo_id=repo_id,
            repo_type="dataset",
            commit_message=message,
        )
        print(f"\n[SUCCESS] Deployment successful! Check progress at: https://huggingface.co/datasets/{repo_id}")
    except Exception as e:
        print(f"\n[ERROR] Failed to deploy to Hugging Face: {e}")
        print("Please ensure your token has write permissions and you are logged in.")
        sys.exit(1)

if __name__ == "__main__":
    main()
