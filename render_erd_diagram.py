import subprocess, os
from PIL import Image, ImageChops

html_mermaid = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <style>
    body {
      background-color: #ffffff;
      font-family: 'Arial', sans-serif;
      margin: 20px;
    }
    .mermaid {
      background-color: #ffffff;
    }
  </style>
</head>
<body>
  <div class="mermaid">
erDiagram
    TEAMS {
        int team_id PK
        string team_name
        string fifa_code
        string group_letter
        string confederation
        int fifa_ranking_pre_tournament
        int elo_rating
        string manager_name
    }
    VENUES {
        int venue_id PK
        string stadium_name
        string city
        string country
        int capacity
        int elevation_meters
    }
    TOURNAMENT_STAGES {
        int stage_id PK
        string stage_name
        bool is_knockout
    }
    REFEREES {
        int referee_id PK
        string name
        string country
        float avg_cards_per_game
    }
    MATCHES {
        int match_id PK
        string date
        int stage_id FK
        int venue_id FK
        int home_team_id FK
        int away_team_id FK
        int home_score
        int away_score
        int referee_id FK
        float home_xg
        float away_xg
        string status
    }
    SQUADS_AND_PLAYERS {
        int player_id PK
        int team_id FK
        string player_name
        string position
        int height_cm
        string date_of_birth
        int caps
        int market_value_eur
    }
    MATCH_EVENTS {
        int event_id PK
        int match_id FK
        int minute
        string event_type
        int team_id FK
        int player_id FK
    }
    MATCH_LINEUPS {
        int lineup_id PK
        int match_id FK
        int player_id FK
        int team_id FK
        bool is_starting_xi
        int minutes_played
    }
    MATCH_TEAM_STATS {
        int match_id PK,FK
        int team_id PK,FK
        int possession_pct
        int shots
        int shots_on_target
        int fouls
        int saves
    }
    PLAYER_STATS {
        int player_id PK,FK
        int team_id FK
        int goals
        int assists
        int yellow_cards
        int red_cards
        int minutes_played
    }
    MATCHES_DETAILED {
        int match_id PK
        string home_team_name
        string away_team_name
        int home_score
        int away_score
    }
    MATCH_PREDICTION_FEATURES {
        int match_id PK
        float home_elo
        float away_elo
        int home_fifa_rank
        int away_fifa_rank
        float home_prev_avg_xg_scored
        float away_prev_avg_xg_scored
        string match_result
    }

    TEAMS ||--o{ MATCHES : "home / away"
    TEAMS ||--o{ SQUADS_AND_PLAYERS : "registers"
    VENUES ||--o{ MATCHES : "hosts"
    TOURNAMENT_STAGES ||--o{ MATCHES : "structures"
    REFEREES ||--o{ MATCHES : "officiates"
    MATCHES ||--o{ MATCH_EVENTS : "contains"
    MATCHES ||--o{ MATCH_LINEUPS : "fields"
    MATCHES ||--o{ MATCH_TEAM_STATS : "records"
    SQUADS_AND_PLAYERS ||--o{ MATCH_LINEUPS : "participates"
    SQUADS_AND_PLAYERS ||--o{ MATCH_EVENTS : "executes"
    SQUADS_AND_PLAYERS ||--o{ PLAYER_STATS : "accumulates"
  </div>
  <script>
    mermaid.initialize({ startOnLoad: true, theme: 'neutral' });
  </script>
</body>
</html>
"""

html_file = os.path.abspath('temp_erd_render.html')
png_file = os.path.abspath('fig2_erd_diagram.png')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_mermaid)

edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

edge_exe = None
for p in edge_paths:
    if os.path.exists(p):
        edge_exe = p
        break

cmd = [
    edge_exe,
    '--headless',
    '--disable-gpu',
    '--hide-scrollbars',
    '--force-device-scale-factor=2.0',
    '--window-size=2400,1800',
    f'--screenshot={png_file}',
    f'file:///{html_file.replace("\\", "/")}'
]

subprocess.run(cmd, check=True)

# Auto-crop white margins
img = Image.open(png_file).convert('RGB')
bg = Image.new(img.mode, img.size, (255, 255, 255))
diff = ImageChops.difference(img, bg)
bbox = diff.getbbox()
if bbox:
    left, upper, right, lower = bbox
    left = max(0, left - 20)
    upper = max(0, upper - 20)
    right = min(img.width, right + 20)
    lower = min(img.height, lower + 20)
    cropped = img.crop((left, upper, right, lower))
    cropped.save(png_file)
    print(f"[SUCCESS] Generated High-DPI ERD Diagram image: {png_file} ({cropped.size[0]}x{cropped.size[1]})")
