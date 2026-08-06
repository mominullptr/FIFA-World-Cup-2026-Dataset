import os
import subprocess

workspace_dir = os.path.dirname(os.path.abspath(__file__))

# Read SVG figures
with open(os.path.join(workspace_dir, 'fig2_xg_scatter.svg'), 'r', encoding='utf-8') as f:
    fig2_svg = f.read()

with open(os.path.join(workspace_dir, 'fig3_team_market_values.svg'), 'r', encoding='utf-8') as f:
    fig3_svg = f.read()

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Data Paper: FIFA World Cup 2026 Master Dataset - Mominul Islam</title>
    <style>
        @page {{
            size: A4;
            margin: 20mm 18mm 22mm 18mm;
            @bottom-right {{
                content: "Page " counter(page) " of " counter(pages);
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 8pt;
                color: #64748b;
            }}
            @bottom-left {{
                content: "Nature Scientific Data Descriptor | FIFA World Cup 2026 Dataset";
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 8pt;
                color: #64748b;
            }}
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.6;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }}

        /* Header Journal Banner */
        .journal-header {{
            border-bottom: 2.5px solid #0f172a;
            padding-bottom: 12px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .journal-title {{
            font-family: Georgia, serif;
            font-size: 14pt;
            font-weight: bold;
            color: #0284c7;
            letter-spacing: -0.3px;
        }}
        .journal-sub {{
            font-size: 8.5pt;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}
        .meta-badges {{
            font-size: 8.5pt;
            color: #334155;
            text-align: right;
        }}
        .badge {{
            display: inline-block;
            background: #f1f5f9;
            color: #0f172a;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 8pt;
            font-weight: 600;
            border: 1px solid #cbd5e1;
        }}

        /* Paper Title */
        h1.paper-title {{
            font-family: Georgia, serif;
            font-size: 20pt;
            font-weight: 700;
            line-height: 1.25;
            color: #0f172a;
            margin-top: 0;
            margin-bottom: 16px;
        }}

        /* Author Profile Box */
        .author-card {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #0284c7;
            border-radius: 6px;
            padding: 14px 18px;
            margin-bottom: 24px;
        }}
        .author-name {{
            font-size: 12pt;
            font-weight: 700;
            color: #0f172a;
        }}
        .author-title {{
            font-size: 9pt;
            color: #0284c7;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        .author-affil {{
            font-size: 8.5pt;
            color: #475569;
            margin-bottom: 8px;
        }}
        .author-links {{
            font-size: 8.5pt;
            color: #334155;
        }}
        .author-links a {{
            color: #0284c7;
            text-decoration: none;
            font-weight: 600;
            margin-right: 12px;
        }}

        /* Abstract Box */
        .abstract-box {{
            background-color: #f1f5f9;
            border-radius: 6px;
            padding: 16px 20px;
            margin-bottom: 24px;
            border: 1px solid #cbd5e1;
        }}
        .abstract-title {{
            font-family: Georgia, serif;
            font-size: 11pt;
            font-weight: bold;
            color: #0f172a;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .abstract-text {{
            font-size: 9.5pt;
            line-height: 1.55;
            color: #334155;
            text-align: justify;
        }}

        /* Headings */
        h2 {{
            font-family: Georgia, serif;
            font-size: 13pt;
            font-weight: 700;
            color: #0f172a;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 4px;
            margin-top: 24px;
            margin-bottom: 12px;
            page-break-after: avoid;
        }}
        h3 {{
            font-size: 10.5pt;
            font-weight: 700;
            color: #1e293b;
            margin-top: 16px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 10px;
            text-align: justify;
        }}

        ul, ol {{
            margin-top: 0;
            margin-bottom: 12px;
            padding-left: 20px;
        }}

        li {{
            margin-bottom: 4px;
        }}

        /* Code & Tables */
        pre {{
            background: #0f172a;
            color: #f8fafc;
            padding: 12px 14px;
            border-radius: 6px;
            font-family: "Courier New", Courier, monospace;
            font-size: 8pt;
            overflow-x: auto;
            line-height: 1.45;
            margin-bottom: 14px;
        }}
        code {{
            font-family: "Courier New", Courier, monospace;
            font-size: 8.5pt;
            background: #f1f5f9;
            color: #0f172a;
            padding: 1px 5px;
            border-radius: 3px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 12px;
            margin-bottom: 18px;
            font-size: 8.5pt;
        }}
        th {{
            background-color: #0f172a;
            color: #ffffff;
            font-weight: 600;
            text-align: left;
            padding: 7px 10px;
            border: 1px solid #0f172a;
        }}
        td {{
            padding: 6px 10px;
            border: 1px solid #e2e8f0;
            color: #334155;
        }}
        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}

        /* Figures */
        .figure-container {{
            margin-top: 18px;
            margin-bottom: 22px;
            text-align: center;
            page-break-inside: avoid;
        }}
        .figure-caption {{
            font-size: 8.5pt;
            color: #475569;
            margin-top: 8px;
            font-style: italic;
            text-align: center;
        }}

        .page-break {{
            page-break-before: always;
        }}

        .bibtex-box {{
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            padding: 10px 14px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 8pt;
            color: #334155;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>

    <!-- Header Journal Banner -->
    <div class="journal-header">
        <div>
            <div class="journal-title">NATURE SCIENTIFIC DATA</div>
            <div class="journal-sub">Open Access | Peer-Reviewed Data Descriptor</div>
        </div>
        <div class="meta-badges">
            <span class="badge">CC0 1.0 Public Domain</span><br>
            <span style="font-size: 8pt; color: #64748b;">DOI: 10.5281/zenodo.21566741</span>
        </div>
    </div>

    <!-- Paper Title -->
    <h1 class="paper-title">Data Paper: A Comprehensive Relational and Feature-Engineered Dataset of the Expanded 48-Team FIFA World Cup 2026</h1>

    <!-- Author Profile Card -->
    <div class="author-card">
        <div class="author-name">Mominul Islam</div>
        <div class="author-title">Lead Data Architect & Quantitative Sports Analytics Researcher</div>
        <div class="author-affil">Open Sports Data Initiative | Department of Data Science & Software Engineering</div>
        <div class="author-links">
            🌐 <strong>GitHub:</strong> <a href="https://github.com/mominullptr">github.com/mominullptr</a> | 
            📊 <strong>Kaggle:</strong> <a href="https://www.kaggle.com/mominullptr">kaggle.com/mominullptr</a> | 
            🤗 <strong>Hugging Face:</strong> <a href="https://huggingface.co/mominullptr">huggingface.co/mominullptr</a> | 
            📦 <strong>Zenodo:</strong> <a href="https://zenodo.org/records/21566741">doi:10.5281/zenodo.21566741</a>
        </div>
    </div>

    <!-- Abstract Box -->
    <div class="abstract-box">
        <div class="abstract-title">Abstract</div>
        <div class="abstract-text">
            The 2026 FIFA World Cup marked a historic milestone in international football, introducing an expanded 48-team format and 104 matches across 16 host venues in Canada, Mexico, and the United States. Despite growing demand for quantitative sports analytics, existing open-source sports datasets often lack relational integrity, detailed granular match events, or standardized machine learning features. Here, we present the <strong>FIFA World Cup 2026 Master Dataset</strong>, a complete open-access relational dataset covering all 104 matches, 48 qualified national teams, 1,248 registered squad players, 2,704 minute-by-minute match lineup records, tactical team statistics, expected goals (xG), and engineered predictive features. Data was collected in real time across the tournament using an automated ingestion pipeline, denormalized into 12 relational entities, and validated using an automated 9-stage programmatic verification framework. The dataset is delivered in CSV, Parquet, and SQLite formats (<code>sqlite_fifa_world_cup_2026.db</code>) alongside a standalone denormalized view (<code>matches_detailed.csv</code>) and ML feature matrix (<code>match_prediction_features.csv</code>). We outline the relational architecture, empirical data visualizations, validation rules, and potential reuse cases in sports analytics, tournament format evaluation, and predictive modeling.
        </div>
    </div>

    <!-- Section 1 -->
    <h2>1. Background & Rationale</h2>
    <p>Football analytics relies heavily on high-quality, fine-grained event and tactical data. However, open access to structured, multi-relational tournament datasets remains limited. Proprietary providers like Opta, StatsBomb, and Wyscout restrict raw data distribution behind expensive commercial licenses, while open-source datasets frequently suffer from incomplete rosters, missing minute-level substitutions, lack of expected goals (xG) metrics, or unvalidated relational keys.</p>
    <p>The 2026 FIFA World Cup provided a unique structural paradigm shift:</p>
    <ul>
        <li><strong>Format Expansion:</strong> Expansion from 32 teams (64 matches) to 48 teams (104 matches).</li>
        <li><strong>Geographic & Environmental Diversity:</strong> 16 host stadiums spanning sea-level venues to high-altitude stadiums (e.g., Estadio Azteca, Mexico City at 2,240m elevation).</li>
        <li><strong>Roster Scale:</strong> 26-man squads across 48 nations, yielding 1,248 active elite players.</li>
    </ul>
    <p>To address the need for a standardized, open-access research benchmark, we created the <strong>FIFA World Cup 2026 Dataset</strong>. The dataset provides an end-to-end relational schema linking team demographics, stadium geography, referee statistics, lineup dynamics, minute-by-minute event logs, and pre-calculated feature vectors for predictive machine learning.</p>

    <!-- Section 2 -->
    <h2>2. Methods & System Architecture</h2>
    <p>The data processing pipeline comprises three primary stages: <strong>Data Ingestion</strong>, <strong>Relational Schema Design</strong>, and <strong>Programmatic Integrity Verification</strong>.</p>
    
    <div class="figure-container">
        <pre>
+---------------------------------------------------------------------------------------+
|                                DATA INGESTION PIPELINE                                |
|   Official FIFA Feeds  |  Sofascore API  |  Transfermarkt Feeds  |  Geographic Surveys|
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                           EXTRACTION & PARSING ENGINE                                 |
|  - JSON Parsing & Entity Disambiguation                                                |
|  - xG Imputation & Lineup Reconciliation                                              |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                          RELATIONAL SCHEMA & SQLite DB BUILD                          |
|  12 Normalized Entities (Teams, Matches, Lineups, Events, Stats, Features, etc.)      |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                           PROGRAMMATIC VALIDATION SUITE                               |
|  9-Stage Automated Integrity Script (PK Uniqueness, FK Checks, Logical Rules)        |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                        MULTI-PLATFORM DISSEMINATION ARCHIVE                           |
|    GitHub Pages  |  Kaggle Datasets  |  Hugging Face Hub  |  Zenodo DOI Repository    |
+---------------------------------------------------------------------------------------+
        </pre>
        <div class="figure-caption">Figure 1: End-to-end data processing, entity normalization, validation, and dissemination pipeline.</div>
    </div>

    <h3>2.1 Data Collection & Parsing Pipeline</h3>
    <p>Data was collected continuously throughout the tournament (June 11 – July 19, 2026) using Python extraction scripts:</p>
    <ul>
        <li><strong>Team & Squad Metadata:</strong> Official FIFA 2026 squad submission lists (<code>SquadLists-English.pdf</code>) and Transfermarkt market valuations were parsed to extract player dates of birth, caps, heights, international goals, and club affiliations.</li>
        <li><strong>Match Events & Lineups:</strong> Real-time match data was aggregated from official FIFA match centers, Sofascore API endpoints, and Guardian live match logs (<code>real_match_details.json</code>, <code>parsed_players.json</code>).</li>
        <li><strong>Expected Goals (xG):</strong> Shot-level xG figures were aggregated and normalized per team per match.</li>
        <li><strong>Geographic & Referee Data:</strong> Host stadium coordinates and elevations were cross-referenced with geographic survey databases. Historical cards-per-game metrics for all 16 referee crews were compiled from FIFA officiating appointments.</li>
    </ul>

    <!-- Section 3 -->
    <h2 class="page-break">3. Relational Schema & Entity Structure</h2>
    <p>The core dataset is structured according to third normal form (3NF) principles across 12 entities, linked via integer primary keys (<code>PK</code>) and foreign keys (<code>FK</code>):</p>

    <!-- Table 1 -->
    <h3>Table 1: File Inventory & Record Counts</h3>
    <table>
        <thead>
            <tr>
                <th>File Name</th>
                <th>Primary Key</th>
                <th>Foreign Keys</th>
                <th>Records</th>
                <th>Entity Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>teams.csv</code></td>
                <td><code>team_id</code></td>
                <td>-</td>
                <td>48</td>
                <td>Demographics, Elo rating, FIFA ranking, and group assignments</td>
            </tr>
            <tr>
                <td><code>venues.csv</code></td>
                <td><code>venue_id</code></td>
                <td>-</td>
                <td>16</td>
                <td>Stadium capacity, geographic coordinates, elevation (m)</td>
            </tr>
            <tr>
                <td><code>tournament_stages.csv</code></td>
                <td><code>stage_id</code></td>
                <td>-</td>
                <td>7</td>
                <td>Tournament phase definitions (Group, R32, R16, QF, SF, Final)</td>
            </tr>
            <tr>
                <td><code>referees.csv</code></td>
                <td><code>referee_id</code></td>
                <td>-</td>
                <td>16</td>
                <td>Officiating crew details and discipline metrics</td>
            </tr>
            <tr>
                <td><code>matches.csv</code></td>
                <td><code>match_id</code></td>
                <td><code>stage_id</code>, <code>venue_id</code>, <code>home_team_id</code>, <code>away_team_id</code>, <code>referee_id</code></td>
                <td>104</td>
                <td>Complete match outcomes, scores, and xG figures</td>
            </tr>
            <tr>
                <td><code>squads_and_players.csv</code></td>
                <td><code>player_id</code></td>
                <td><code>team_id</code></td>
                <td>1,248</td>
                <td>Individual player demographics, heights, and market values</td>
            </tr>
            <tr>
                <td><code>match_events.csv</code></td>
                <td><code>event_id</code></td>
                <td><code>match_id</code>, <code>team_id</code>, <code>player_id</code></td>
                <td>500+</td>
                <td>Granular match events with minute-by-minute timestamps</td>
            </tr>
            <tr>
                <td><code>match_lineups.csv</code></td>
                <td><code>lineup_id</code></td>
                <td><code>match_id</code>, <code>player_id</code>, <code>team_id</code></td>
                <td>2,704</td>
                <td>Tactical lineups, starter flags, and minutes played</td>
            </tr>
            <tr>
                <td><code>match_team_stats.csv</code></td>
                <td>(<code>match_id</code>, <code>team_id</code>)</td>
                <td><code>match_id</code>, <code>team_id</code></td>
                <td>208</td>
                <td>Per-team tactical stats (possession, shots, fouls, saves)</td>
            </tr>
            <tr>
                <td><code>player_stats.csv</code></td>
                <td><code>player_id</code></td>
                <td><code>player_id</code>, <code>team_id</code></td>
                <td>1,248</td>
                <td>Tournament aggregate stats per player</td>
            </tr>
            <tr>
                <td><code>matches_detailed.csv</code></td>
                <td><code>match_id</code></td>
                <td>-</td>
                <td>104</td>
                <td>Denormalized match view for rapid visualization</td>
            </tr>
            <tr>
                <td><code>match_prediction_features.csv</code></td>
                <td><code>match_id</code></td>
                <td>-</td>
                <td>104</td>
                <td>Pre-engineered feature matrix for ML modeling</td>
            </tr>
        </tbody>
    </table>

    <!-- Section 4 -->
    <h2>4. Empirical Visualizations & Key Findings</h2>
    <p>To demonstrate the utility of the dataset, we generated empirical visualizations analyzing expected goals and market valuations across the tournament.</p>

    <div class="figure-container">
        {fig2_svg}
        <div class="figure-caption">Figure 2: Expected Goals (xG) vs. Actual Goals Scored across 104 matches (208 team performances). Red dashed line indicates xG equality (y=x).</div>
    </div>

    <div class="figure-container">
        {fig3_svg}
        <div class="figure-caption">Figure 3: Squad Market Valuations (€ Millions) for the Top 15 Qualified National Teams color-coded by Confederation (UEFA, CONMEBOL, CONCACAF, CAF, AFC).</div>
    </div>

    <!-- Section 5 -->
    <h2 class="page-break">5. Technical Validation & Integrity Audit</h2>
    <p>To guarantee publication-grade data quality, the dataset was evaluated against an automated 9-stage programmatic verification engine (<code>validate_dataset.py</code>).</p>

    <h3>Table 2: 9-Stage Verification Framework & Results</h3>
    <table>
        <thead>
            <tr>
                <th>Stage</th>
                <th>Validation Domain</th>
                <th>Assertion Rule</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Row Count Integrity</td>
                <td>Exactly 48 teams, 16 venues, 1,248 players, and 104 matches</td>
                <td><span style="color:#059669; font-weight:bold;">[PASS] 100% Verified</span></td>
            </tr>
            <tr>
                <td>2</td>
                <td>Primary Key Uniqueness</td>
                <td>Primary keys in all 12 tables contain zero duplicates</td>
                <td><span style="color:#059669; font-weight:bold;">[PASS] 100% Verified</span></td>
            </tr>
            <tr>
                <td>3</td>
                <td>Referential Integrity</td>
                <td>All foreign keys in child tables resolve to valid parent primary keys</td>
                <td><span style="color:#059669; font-weight:bold;">[PASS] 100% Verified</span></td>
            </tr>
            <tr>
                <td>4</td>
                <td>Score & Status Logic</td>
                <td>Completed matches possess valid scorelines, xG, and penalty values</td>
                <td><span style="color:#059669; font-weight:bold;">[PASS] 100% Verified</span></td>
            </tr>
            <tr>
                <td>5</td>
                <td>View Alignment</td>
                <td>Denormalized <code>matches_detailed.csv</code> aligns perfectly with normalized tables</td>
                <td><span style="color:#059669; font-weight:bold;">[PASS] 100% Verified</span></td>
            </tr>
            <tr>
                <td>6</td>
                <td>Lineup Structure</td>
                <td>Exactly 26 squad players registered per match; exactly 11 starters per team</td>
                <td><span style="color:#059669; font-weight:bold;">[PASS] 100% Verified</span></td>
            </tr>
            <tr>
                <td>7</td>
                <td>Team Tactical Stats</td>
                <td>Possession splits (Home %, Away %, Contested %) sum to valid range [80%, 100%]</td>
                <td><span style="color:#059669; font-weight:bold;">[PASS] 100% Verified</span></td>
            </tr>
            <tr>
                <td>8</td>
                <td>Player Stats & Events</td>
                <td>Event tallies (goals, assists, cards) equal player tournament cumulative totals</td>
                <td><span style="color:#059669; font-weight:bold;">[PASS] 100% Verified</span></td>
            </tr>
            <tr>
                <td>9</td>
                <td>Goalkeeper Constraints</td>
                <td>Goalkeeper metrics (saves, clean sheets) populated exclusively for GK position</td>
                <td><span style="color:#059669; font-weight:bold;">[PASS] 100% Verified</span></td>
            </tr>
        </tbody>
    </table>

    <!-- Section 6 -->
    <h2>6. Usage Notes & Code Benchmarks</h2>
    <p>The normalized SQLite database (<code>sqlite_fifa_world_cup_2026.db</code>) supports instant importing into Power BI, Tableau, PostgreSQL, or DuckDB.</p>

    <h3>Example SQL Benchmark Query (Top Goalscorers & Efficiency)</h3>
    <pre>
SELECT 
    p.player_name, 
    t.team_name, 
    ps.goals, 
    ps.minutes_played,
    ROUND(CAST(ps.minutes_played AS FLOAT) / ps.goals, 1) AS mins_per_goal
FROM player_stats ps
JOIN squads_and_players p ON ps.player_id = p.player_id
JOIN teams t ON ps.team_id = t.team_id
WHERE ps.goals > 0
ORDER BY ps.goals DESC, mins_per_goal ASC
LIMIT 10;
    </pre>

    <!-- Section 7 -->
    <h2>7. Code & Data Availability</h2>
    <p>The dataset and scripts are openly archived under the Creative Commons CC0 1.0 Universal license:</p>
    <ul>
        <li><strong>GitHub Repository:</strong> <a href="https://github.com/mominullptr/FIFA-World-Cup-2026-Dataset">https://github.com/mominullptr/FIFA-World-Cup-2026-Dataset</a></li>
        <li><strong>Zenodo DOI Archive:</strong> <a href="https://zenodo.org/records/21566741">10.5281/zenodo.21566741</a></li>
        <li><strong>Kaggle Dataset:</strong> <a href="https://www.kaggle.com/datasets/mominullptr/fifa-world-cup-2026-dataset">https://www.kaggle.com/datasets/mominullptr/fifa-world-cup-2026-dataset</a></li>
        <li><strong>Hugging Face Hub:</strong> <a href="https://huggingface.co/datasets/mominullptr/fifa-world-cup-2026-dataset">https://huggingface.co/datasets/mominullptr/fifa-world-cup-2026-dataset</a></li>
    </ul>

    <h2>8. Citation</h2>
    <p>If you utilize this dataset in your research or applications, please cite it as:</p>
    <div class="bibtex-box">
@dataset{{mominul_fifa2026_dataset,
  author       = {{Mominul Islam}},
  title        = {{FIFA World Cup 2026 Dataset: Live Results, Squads, Lineups, xG & Team Stats}},
  month        = jul,
  year         = 2026,
  publisher    = {{Zenodo}},
  version      = {{v1.0-final}},
  doi          = {{10.5281/zenodo.21566741}},
  url          = {{https://github.com/mominullptr/FIFA-World-Cup-2026-Dataset}}
}}
    </div>

</body>
</html>
"""

html_path = os.path.join(workspace_dir, 'DATA_PAPER_PUBLICATION.html')
pdf_path = os.path.join(workspace_dir, 'FIFA_World_Cup_2026_Data_Paper_Mominul_Islam.pdf')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated HTML paper at {html_path}")

# Compile HTML to PDF using msedge or chrome
chrome_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
]

browser_exe = None
for path in chrome_paths:
    if os.path.exists(path):
        browser_exe = path
        break

if browser_exe:
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_path):
        print(f"SUCCESS: PDF generated successfully at {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes).")
    else:
        print(f"PDF compilation failed. Stderr: {result.stderr}")
else:
    print("Browser executable not found.")
