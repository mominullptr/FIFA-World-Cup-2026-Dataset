# FIFA World Cup 2026 Dataset- Live & Updated Stats — Matches, Squads, Players, Stats & Live Results

## 🔗 Dataset Links
* **Kaggle:** [FIFA World Cup 2026 Dataset](https://www.kaggle.com/datasets/mominullptr/fifa-world-cup-2026-dataset)
* **GitHub:** [FIFA-World-Cup-2026-Dataset](https://github.com/mominullptr/FIFA-World-Cup-2026-Dataset)
* **Hugging Face:** [fifa-world-cup-2026-dataset](https://huggingface.co/datasets/Mominullptr/fifa-world-cup-2026-dataset)

**The most complete and actively updated FIFA World Cup 2026 dataset on Kaggle.** A clean, authentic, relational dataset covering the entire tournament (June 11 – July 19, 2026) with the first-ever 48-team format. Includes real match results updated daily, 1,248 players across all 48 squads, expected goals (xG), minute-by-minute match events, and per-team match statistics sourced from FIFA.com and verified providers.

> **Why this dataset?** Unlike other World Cup datasets, this one is (1) updated daily with real match results as games are played, (2) fully relational with normalized foreign keys for SQL/database modeling, (3) contains zero synthetic data — every stat is sourced and traceable, and (4) includes advanced metrics like xG, match team stats, and VAR events.

---

## 🏆 Tournament Status

- **Tournament:** FIFA World Cup 2026
- **Format:** 48 Teams
- **Current Stage:** Round of 16
- **Matches Completed:** 92
- **Updated After:** Every Completed Match
- **Validation:** Relational integrity verified before every release

---

## 👥 Community Recognition

The FIFA World Cup 2026 Dataset has started gaining traction within the data science and developer community.

- Mentioned by **Software with Nick** in an Instagram reel highlighting useful datasets for AI, machine learning, and data science projects.
- Featured in a LinkedIn post that reached **22,000+ professionals**, generating significant engagement from the data community.
- Shared and discussed by developers building World Cup prediction models, dashboards, SQL projects, and sports analytics applications.
- Continuously updated after every completed FIFA World Cup 2026 match.

### Featured Mentions

**Software with Nick (Instagram)**
- 📹 https://www.instagram.com/softwarewithnick/reel/DaSkFRqx1e1/

**LinkedIn Community Post**
- 🔗 https://www.linkedin.com/feed/update/urn:li:activity:7473374635284422658/

---

##  Key Features

* **Real-World Group Configurations**: Reflects the actual 12 groups (Groups A to L) with zero qualifiers placeholders.
* **Geographical & Altitude Details**: Includes coordinates (Latitude/Longitude) and exact elevations in meters for all 16 host stadiums in the USA, Canada, and Mexico.
* **Granular Player Data**: Features 1,248 players (26-man squads for all 48 teams) with market values in Euros, national team caps, positions, and club teams.
* **Live Expected Goals (xG)**: Includes expected goals metrics for all completed matches.
* **Match Events**: Logs every goal, assist, card, and VAR review chronologically by minute.
* **Match Team Stats**: Per-team per-match statistics (possession, shots, corners, etc.) sourced from verified providers.
* **Interactive Updater**: Built-in interactive console application to easily record daily match outcomes and populate events without breaking database normalization.

---

## Database Schema

```mermaid
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
        float latitude
        float longitude
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
        string kickoff_time_utc
        int stage_id FK
        int venue_id FK
        int home_team_id FK
        int away_team_id FK
        int home_score
        int away_score
        string status
        float home_xg
        float away_xg
        int referee_id FK
    }
    SQUADS_AND_PLAYERS {
        int player_id PK
        int team_id FK
        string player_name
        string position
        string club_team
        int market_value_eur
        int caps
        string date_of_birth
        int height_cm
        int goals
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
        int is_starting_xi
        string tactical_position
        int minutes_played
    }
    PLAYER_STATS {
        int player_id PK, FK
        string player_name
        int team_id FK
        int matches_played
        int matches_started
        int minutes_played
        int goals
        int assists
        int yellow_cards
        int red_cards
        int penalty_scored
        int own_goals
        int saves
        int goals_conceded
        int clean_sheets
        string data_source
        string last_verified
    }

    TEAMS ||--o{ MATCHES : "hosts/visitors"
    TEAMS ||--o{ SQUADS_AND_PLAYERS : "roster"
    VENUES ||--o{ MATCHES : "hosts"
    TOURNAMENT_STAGES ||--o{ MATCHES : "stage"
    REFEREES ||--o{ MATCHES : "officiates"
    MATCHES ||--o{ MATCH_EVENTS : "contains"
    SQUADS_AND_PLAYERS ||--o{ MATCH_EVENTS : "triggers"
    MATCHES ||--o{ MATCH_LINEUPS : "lineups"
    SQUADS_AND_PLAYERS ||--o{ MATCH_LINEUPS : "plays_in"
    TEAMS ||--o{ MATCH_LINEUPS : "lineups"
    SQUADS_AND_PLAYERS ||--|| PLAYER_STATS : "has"
    TEAMS ||--o{ PLAYER_STATS : "has"
    MATCH_TEAM_STATS {
        int match_id FK
        int team_id FK
        int possession_pct
        int total_shots
        int shots_on_target
        int corners
        int fouls
        int offsides
        int saves
        string data_source
        string last_updated
    }
    MATCHES ||--o{ MATCH_TEAM_STATS : "stats"
    TEAMS ||--o{ MATCH_TEAM_STATS : "stats"
```

---

##  CSV Files Description

1. **`teams.csv`**: Information on all 48 participating countries.
2. **`venues.csv`**: Geolocation, capacities, and elevation details of all 16 stadiums.
3. **`tournament_stages.csv`**: Lookup table for stages (Group Stage, Round of 32, etc.).
4. **`referees.csv`**: International referees with their historical card-per-game stats.
5. **`matches.csv`**: Match outcomes, dates, times, scores, xG metrics, and statuses using relational IDs (`stage_id`, `venue_id`, etc.) for clean database modeling.
6. **`matches_detailed.csv`**: A denormalized, user-friendly version of `matches.csv` that displays human-readable names (e.g. `home_team_name`, `stadium_name`, `city`, `referee_name`) instead of IDs. Ideal for quick analysis without SQL joins!
7. **`squads_and_players.csv`**: Detailed player registries (1,248 rows) containing verified player names (preserved with native accents), positions, clean club teams, market values, international caps, dates of birth (in YYYY-MM-DD format), heights in centimeters, and international goals.
8. **`match_events.csv`**: Time-series game events (goals, assists, cards, VAR reviews) mapped to matches and players.
9. **`match_team_stats.csv`**: Per-team per-match statistics (possession %, shots, shots on target, corners, fouls, offsides, saves) with `data_source` and `last_updated` columns for full traceability. Only populated with verified data from authentic sources (FIFA, Sofascore, FBref, etc.).
10. **`match_lineups.csv`**: Tactical lineups for all completed matches: starting XI (11 players per team) and substitutes with actual minutes played.
11. **`player_stats.csv`**: Cumulative tournament statistics for each player (1,248 rows), updated continuously as matches conclude. Outfield players have goalkeeper-specific fields set to NULL, and unverified advanced metrics (such as shots or key passes) are kept NULL to preserve dataset authenticity.

---

## 📋 Data Integrity Policy

> **Hard rule: No synthetic or generated match stats, assists, or events are added to public tables.**

- All match results, events, and statistics are sourced from verified, authentic providers.
- New fields (e.g., assists, team stats) are only populated when confirmed from real sources.
- The `data_source` column in `match_team_stats.csv` provides full traceability.
- If verified data is unavailable for a match, that match is simply omitted from optional tables rather than filled with generated values.


---

## 🛠️ Installation & Usage

To generate the initial CSV dataset or regenerate it back to its default start state:
```bash
python generate_dataset.py
```

### Daily Match Updates
As matches conclude every day, you can update the datasets interactively. The script will guide you step-by-step to record final scores, xG, and select players for goals, cards, and VAR reviews:
```bash
python update_dataset.py
```

### SQLite Database Generation
For researchers and SQL query design, you can package all normalized CSV files into a single, query-optimized SQLite relational database file:
```bash
python generate_sqlite.py
```

---

## 🏷️ Citation

If you use this dataset in your research, publications, or projects, please cite it using the academic metadata provided in [CITATION.cff](file:///c:/Users/ASUS/.gemini/antigravity/scratch/fifa-wc2026-dataset/CITATION.cff) or using the format below:

```bibtex
@dataset{fifa_world_cup_2026,
  author = {MD Mominul Islam},
  title = {FIFA World Cup 2026 Dataset- Live & Updated Stats},
  year = {2026},
  publisher = {Kaggle}
}
```

---

## 📄 License
This project is licensed under the **Creative Commons Zero v1.0 Universal** (CC0-1.0) Public Domain Dedication. Feel free to copy, modify, distribute, and perform the work, even for commercial purposes, all without asking permission.

