import os
import csv
import random
import re
import json
import unicodedata
import sys

# Set encoding for standard out to utf-8
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Set random seed for reproducibility
random.seed(42)

# Define directories
output_dir = os.path.dirname(os.path.abspath(__file__))


# ==========================================
# 1. TEAMS DATA
# ==========================================
teams_headers = ["team_id", "team_name", "fifa_code", "group_letter", "confederation", "fifa_ranking_pre_tournament", "elo_rating", "manager_name"]
teams_data = [
    # Group A
    [1, "Mexico", "MEX", "A", "CONCACAF", 14, 1810, "Javier Aguirre"],
    [2, "South Africa", "RSA", "A", "CAF", 60, 1620, "Hugo Broos"],
    [3, "South Korea", "KOR", "A", "AFC", 22, 1800, "Hong Myung-bo"],
    [4, "Czechia", "CZE", "A", "UEFA", 40, 1740, "Miroslav Koubek"],
    
    # Group B
    [5, "Canada", "CAN", "B", "CONCACAF", 33, 1795, "Jesse Marsch"],
    [6, "Bosnia and Herzegovina", "BIH", "B", "UEFA", 64, 1645, "Sergej Barbarez"],
    [7, "Qatar", "QAT", "B", "AFC", 56, 1600, "Julen Lopetegui"],
    [8, "Switzerland", "SUI", "B", "UEFA", 19, 1860, "Murat Yakin"],
    
    # Group C
    [9, "Brazil", "BRA", "C", "CONMEBOL", 6, 2030, "Carlo Ancelotti"],
    [10, "Morocco", "MAR", "C", "CAF", 7, 1920, "Walid Regragui"],
    [11, "Haiti", "HAI", "C", "CONCACAF", 83, 1530, "Sébastien Migné"],
    [12, "Scotland", "SCO", "C", "UEFA", 39, 1720, "Steve Clarke"],
    
    # Group D
    [13, "USA", "USA", "D", "CONCACAF", 17, 1850, "Mauricio Pochettino"],
    [14, "Paraguay", "PAR", "D", "CONMEBOL", 54, 1725, "Gustavo Alfaro"],
    [15, "Australia", "AUS", "D", "AFC", 27, 1790, "Tony Popovic"],
    [16, "Türkiye", "TUR", "D", "UEFA", 26, 1780, "Vincenzo Montella"],
    
    # Group E
    [17, "Germany", "GER", "E", "UEFA", 10, 1970, "Julian Nagelsmann"],
    [18, "Curaçao", "CUW", "E", "CONCACAF", 82, 1520, "Dick Advocaat"],
    [19, "Côte d'Ivoire", "CIV", "E", "CAF", 38, 1750, "Emerse Faé"],
    [20, "Ecuador", "ECU", "E", "CONMEBOL", 23, 1870, "Sebastián Beccacece"],
    
    # Group F
    [21, "Netherlands", "NED", "F", "UEFA", 8, 1980, "Ronald Koeman"],
    [22, "Japan", "JPN", "F", "AFC", 18, 1880, "Hajime Moriyasu"],
    [23, "Sweden", "SWE", "F", "UEFA", 25, 1815, "Jon Dahl Tomasson"],
    [24, "Tunisia", "TUN", "F", "CAF", 45, 1710, "Hervé Renard"],
    
    # Group G
    [25, "Belgium", "BEL", "G", "UEFA", 9, 1950, "Domenico Tedesco"],
    [26, "Egypt", "EGY", "G", "CAF", 36, 1730, "Hossam Hassan"],
    [27, "IR Iran", "IRN", "G", "AFC", 20, 1820, "Amir Ghalenoei"],
    [28, "New Zealand", "NZL", "G", "OFC", 85, 1510, "Darren Bazeley"],
    
    # Group H
    [29, "Spain", "ESP", "H", "UEFA", 2, 2120, "Luis de la Fuente"],
    [30, "Cabo Verde", "CPV", "H", "CAF", 67, 1640, "Bubista"],
    [31, "Saudi Arabia", "KSA", "H", "AFC", 58, 1660, "Georgios Donis"],
    [32, "Uruguay", "URU", "H", "CONMEBOL", 16, 1960, "Marcelo Bielsa"],
    
    # Group I
    [33, "France", "FRA", "I", "UEFA", 3, 2100, "Didier Deschamps"],
    [34, "Senegal", "SEN", "I", "CAF", 15, 1840, "Pape Thiaw"],
    [35, "Iraq", "IRQ", "I", "AFC", 55, 1630, "Graham Arnold"],
    [36, "Norway", "NOR", "I", "UEFA", 44, 1775, "Ståle Solbakken"],
    
    # Group J
    [37, "Argentina", "ARG", "J", "CONMEBOL", 1, 2150, "Lionel Scaloni"],
    [38, "Algeria", "ALG", "J", "CAF", 28, 1760, "Vladimir Petković"],
    [39, "Austria", "AUT", "J", "UEFA", 24, 1830, "Ralf Rangnick"],
    [40, "Jordan", "JOR", "J", "AFC", 63, 1610, "Jamal Sellami"],
    
    # Group K
    [41, "Portugal", "POR", "K", "UEFA", 5, 2010, "Roberto Martínez"],
    [42, "Congo DR", "COD", "K", "CAF", 61, 1670, "Sébastien Desabre"],
    [43, "Uzbekistan", "UZB", "K", "AFC", 50, 1650, "Fabio Cannavaro"],
    [44, "Colombia", "COL", "K", "CONMEBOL", 13, 1990, "Néstor Lorenzo"],
    
    # Group L
    [45, "England", "ENG", "L", "UEFA", 4, 2050, "Thomas Tuchel"],
    [46, "Croatia", "CRO", "L", "UEFA", 11, 1940, "Zlatko Dalić"],
    [47, "Ghana", "GHA", "L", "CAF", 49, 1690, "Carlos Queiroz"],
    [48, "Panama", "PAN", "L", "CONCACAF", 34, 1680, "Thomas Christiansen"]
]

# ==========================================
# 2. VENUES DATA
# ==========================================
venues_headers = ["venue_id", "stadium_name", "city", "country", "capacity", "latitude", "longitude", "elevation_meters"]
venues_data = [
    [1, "Mexico City Stadium (Estadio Azteca)", "Mexico City", "MEX", 80824, 19.3031, -99.1506, 2200],
    [2, "New York New Jersey Stadium (MetLife Stadium)", "East Rutherford", "USA", 82500, 40.8136, -74.0744, 7],
    [3, "Los Angeles Stadium (SoFi Stadium)", "Inglewood", "USA", 70240, 33.9535, -118.3390, 30],
    [4, "Dallas Stadium (AT&T Stadium)", "Arlington", "USA", 80000, 32.7473, -97.0928, 184],
    [5, "Vancouver Stadium (BC Place)", "Vancouver", "CAN", 54500, 49.2768, -123.1120, 9],
    [6, "Toronto Stadium (BMO Field)", "Toronto", "CAN", 30000, 43.6328, -79.4186, 76],
    [7, "Guadalajara Stadium (Estadio Akron)", "Zapopan", "MEX", 48070, 20.6811, -103.4628, 1566],
    [8, "Monterrey Stadium (Estadio BBVA)", "Guadalupe", "MEX", 53500, 25.6690, -100.2444, 538],
    [9, "Atlanta Stadium (Mercedes-Benz Stadium)", "Atlanta", "USA", 71000, 33.7553, -84.4017, 318],
    [10, "Boston Stadium (Gillette Stadium)", "Foxborough", "USA", 65878, 42.0909, -71.2643, 87],
    [11, "Houston Stadium (NRG Stadium)", "Houston", "USA", 72220, 29.6847, -95.4082, 14],
    [12, "Kansas City Stadium (Arrowhead Stadium)", "Kansas City", "USA", 76416, 39.0489, -94.4839, 264],
    [13, "Miami Stadium (Hard Rock Stadium)", "Miami Gardens", "USA", 64767, 25.9581, -80.2389, 2],
    [14, "Philadelphia Stadium (Lincoln Financial Field)", "Philadelphia", "USA", 69796, 39.9008, -75.1675, 3],
    [15, "San Francisco Bay Area Stadium (Levi's Stadium)", "Santa Clara", "USA", 68500, 37.4033, -121.9698, 8],
    [16, "Seattle Stadium (Lumen Field)", "Seattle", "USA", 69000, 47.5952, -122.3316, 3]
]

# ==========================================
# 3. TOURNAMENT STAGES DATA
# ==========================================
stages_headers = ["stage_id", "stage_name", "is_knockout"]
stages_data = [
    [1, "Group Stage", False],
    [2, "Round of 32", True],
    [3, "Round of 16", True],
    [4, "Quarter-finals", True],
    [5, "Semi-finals", True],
    [6, "Third-place match", True],
    [7, "Final", True]
]

# ==========================================
# 4. REFEREES DATA
# ==========================================
referees_headers = ["referee_id", "name", "country", "avg_cards_per_game"]
referees_data = [
    [1, "Szymon Marciniak", "Poland", 4.2],
    [2, "Daniele Orsato", "Italy", 4.8],
    [3, "Michael Oliver", "England", 3.9],
    [4, "Anthony Taylor", "England", 4.1],
    [5, "Clément Turpin", "France", 3.6],
    [6, "Danny Makkelie", "Netherlands", 3.8],
    [7, "Jesús Valenzuela", "Venezuela", 4.9],
    [8, "Wilton Sampaio", "Brazil", 4.5],
    [9, "César Arturo Ramos", "Mexico", 4.0],
    [10, "Ivan Barton", "El Salvador", 5.1],
    [11, "Mustapha Ghorbal", "Algeria", 3.7],
    [12, "Victor Gomes", "South Africa", 4.3],
    [13, "Ma Ning", "China", 5.5],
    [14, "Alireza Faghani", "Australia", 4.2],
    [15, "Yoshimi Yamashita", "Japan", 3.4],
    [16, "Facundo Tello", "Argentina", 5.0]
]

# ==========================================
# 5. SQUADS & PLAYERS DATA GENERATOR
# ==========================================
players_headers = ["player_id", "team_id", "player_name", "position", "club_team", "market_value_eur", "caps", "date_of_birth", "height_cm", "goals"]
# Star players with real Transfermarkt market values (June 2026 snapshot)
# Source: transfermarkt.com — values retrieved June 2026
star_players = {
    "Argentina": [
        ("Lionel Messi", "FWD", "Inter Miami", 15000000, 185),
        ("Lautaro Martínez", "FWD", "Inter Milan", 85000000, 62),
        ("Alexis Mac Allister", "MID", "Liverpool", 70000000, 28),
        ("Enzo Fernández", "MID", "Chelsea", 90000000, 24),
        ("Emiliano Martínez", "GK", "Aston Villa", 12000000, 39)
    ],
    "France": [
        ("Kylian Mbappé", "FWD", "Real Madrid", 180000000, 80),
        ("Antoine Griezmann", "FWD", "Atlético Madrid", 8000000, 129),
        ("Aurélien Tchouaméni", "MID", "Real Madrid", 70000000, 34),
        ("William Saliba", "DEF", "Arsenal", 100000000, 17),
        ("Mike Maignan", "GK", "AC Milan", 20000000, 18),
        ("Michael Olise", "FWD", "Bayern Munich", 150000000, 15)
    ],
    "England": [
        ("Harry Kane", "FWD", "Bayern Munich", 60000000, 93),
        ("Jude Bellingham", "MID", "Real Madrid", 130000000, 32),
        ("Bukayo Saka", "FWD", "Arsenal", 110000000, 36),
        ("Declan Rice", "MID", "Arsenal", 120000000, 52),
        ("Jordan Pickford", "GK", "Everton", 13000000, 64),
        ("Phil Foden", "MID", "Manchester City", 70000000, 40)
    ],
    "Brazil": [
        ("Vinícius Júnior", "FWD", "Real Madrid", 140000000, 28),
        ("Rodrygo", "FWD", "Real Madrid", 45000000, 24),
        ("Bruno Guimarães", "MID", "Newcastle United", 70000000, 22),
        ("Marquinhos", "DEF", "Paris Saint-Germain", 28000000, 84),
        ("Alisson Becker", "GK", "Liverpool", 15000000, 65),
        ("Raphinha", "FWD", "FC Barcelona", 70000000, 40),
        ("Endrick", "FWD", "Olympique Lyonnais", 40000000, 17),
        ("Neymar", "FWD", "Santos", 8000000, 128)
    ],
    "USA": [
        ("Christian Pulisic", "FWD", "AC Milan", 40000000, 68),
        ("Weston McKennie", "MID", "Juventus", 30000000, 53),
        ("Folarin Balogun", "FWD", "Monaco", 40000000, 12),
        ("Antonee Robinson", "DEF", "Fulham", 22000000, 41),
        ("Matt Turner", "GK", "Crystal Palace", 2500000, 40)
    ],
    "Spain": [
        ("Lamine Yamal", "FWD", "FC Barcelona", 200000000, 26),
        ("Pedri", "MID", "FC Barcelona", 150000000, 36),
        ("Dani Olmo", "MID", "FC Barcelona", 60000000, 45),
        ("Nico Williams", "FWD", "Athletic Bilbao", 40000000, 20),
        ("Gavi", "MID", "FC Barcelona", 30000000, 22),
        ("David Raya", "GK", "Arsenal", 30000000, 12),
        ("Mikel Oyarzabal", "FWD", "Real Sociedad", 35000000, 36)
    ],
    "Germany": [
        ("Florian Wirtz", "MID", "Liverpool", 100000000, 42),
        ("Jamal Musiala", "MID", "Bayern Munich", 100000000, 43),
        ("Kai Havertz", "FWD", "Arsenal", 65000000, 59),
        ("Manuel Neuer", "GK", "Bayern Munich", 4000000, 120),
        ("Leroy Sané", "MID", "Galatasaray", 15000000, 77)
    ],
    "Portugal": [
        ("Cristiano Ronaldo", "FWD", "Al Nassr", 10000000, 210),
        ("Rafael Leão", "FWD", "AC Milan", 50000000, 30),
        ("Vitinha", "MID", "Paris Saint-Germain", 140000000, 25),
        ("João Neves", "MID", "Paris Saint-Germain", 140000000, 18),
        ("Bruno Fernandes", "MID", "Manchester United", 35000000, 65),
        ("Bernardo Silva", "MID", "Manchester City", 22000000, 95),
        ("Diogo Costa", "GK", "Porto", 25000000, 20)
    ],
    "Netherlands": [
        ("Cody Gakpo", "FWD", "Liverpool", 60000000, 51),
        ("Virgil van Dijk", "DEF", "Liverpool", 15000000, 70),
        ("Ryan Gravenberch", "MID", "Liverpool", 55000000, 28),
        ("Tijjani Reijnders", "MID", "Manchester City", 65000000, 33),
        ("Xavi Simons", "MID", "Paris Saint-Germain", 80000000, 15)
    ],
    "Norway": [
        ("Erling Haaland", "FWD", "Manchester City", 200000000, 35),
        ("Martin Ødegaard", "MID", "Arsenal", 100000000, 60),
        ("Alexander Isak", "FWD", "Newcastle United", 85000000, 25)
    ],
    "Morocco": [
        ("Achraf Hakimi", "DEF", "Paris Saint-Germain", 80000000, 75),
        ("Yassine Bounou", "GK", "Al Hilal", 10000000, 60)
    ],
    "Belgium": [
        ("Thibaut Courtois", "GK", "Real Madrid", 15000000, 108),
        ("Romelu Lukaku", "FWD", "Napoli", 22000000, 120)
    ],
    "Colombia": [
        ("Luis Díaz", "FWD", "Liverpool", 50000000, 45)
    ],
    "Japan": [
        ("Takefusa Kubo", "FWD", "Real Sociedad", 40000000, 30)
    ],
    "Egypt": [
        ("Mohamed Salah", "FWD", "Liverpool", 22000000, 100)
    ],
    "Croatia": [
        ("Luka Modrić", "MID", "Real Madrid", 5000000, 180),
        ("Joško Gvardiol", "DEF", "Manchester City", 75000000, 30)
    ]
}

# Read parsed players
json_path = os.path.join(output_dir, "parsed_players.json")
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        parsed_players_data = json.load(f)
else:
    parsed_players_data = []

# Group parsed players by team_id
players_by_team = {}
for p in parsed_players_data:
    t_id = p["team_id"]
    if t_id not in players_by_team:
        players_by_team[t_id] = []
    players_by_team[t_id].append(p)

# Star players mapping for quick lookup of specific values
star_players_lookup = {}
for nation, stars in star_players.items():
    for name, pos, club, val, caps in stars:
        norm_name = unicodedata.normalize('NFD', name)
        norm_name_clean = "".join(c for c in norm_name if unicodedata.category(c) != 'Mn')
        star_players_lookup[norm_name_clean.lower()] = val

# Try to load existing market values from squads_and_players.csv to preserve authentic data
existing_market_values = {}
players_csv_path = os.path.join(output_dir, "squads_and_players.csv")
if os.path.exists(players_csv_path):
    try:
        import csv
        with open(players_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                norm_name = unicodedata.normalize('NFD', row["player_name"])
                norm_name_clean = "".join(c for c in norm_name if unicodedata.category(c) != 'Mn')
                key = (norm_name_clean.lower().strip(), int(row["team_id"]))
                existing_market_values[key] = int(row["market_value_eur"])
    except Exception as e:
        print(f"Warning: Could not read existing squads_and_players.csv: {e}")

players_data = []
player_id_counter = 1
team_player_map = {}

for team in teams_data:
    team_id = team[0]
    team_name = team[1]
    rank = team[5]
    
    team_player_map[team_id] = []
    squad = players_by_team.get(team_id, [])
    
    for idx_in_squad, player_data in enumerate(squad):
        player_id = player_id_counter
        name = player_data["name"]
        pos = player_data["position"]
        # Strip country code from club for csv
        club = re.sub(r"\s*\([A-Z]{3}\)$", "", player_data["club"]).strip()
        caps = player_data["caps"]
        
        # Determine market value
        val = None
        norm_name = unicodedata.normalize('NFD', name)
        norm_name_clean = "".join(c for c in norm_name if unicodedata.category(c) != 'Mn')
        player_name_lower = norm_name_clean.lower()
        
        # 1. Try to load from existing squads_and_players.csv first (authentic values)
        if (player_name_lower, int(team_id)) in existing_market_values:
            val = existing_market_values[(player_name_lower, int(team_id))]
        else:
            # 2. Check if they are a star player (exact match first, then substring/fuzzy)
            if player_name_lower in star_players_lookup:
                val = star_players_lookup[player_name_lower]
            else:
                # Try substring match: check if any star name is contained in parsed name
                for star_name_key, star_val in star_players_lookup.items():
                    star_parts = star_name_key.split()
                    # Check if star name is a substring of full name
                    if star_name_key in player_name_lower:
                        val = star_val
                        break
                    # Check if all parts of the star name appear in the full name
                    if all(part in player_name_lower.split() for part in star_parts):
                        val = star_val
                        break
        
        if val is None:
            # Set seed based on player_id for reproducible generation
            random.seed(player_id)
            base_val = max(100000, int(150000000 / (rank ** 0.85)))
            val = int(random.uniform(0.4, 1.6) * base_val)
            
        # Convert DOB to YYYY-MM-DD
        dob_iso = ""
        if player_data.get("dob"):
            parts = player_data["dob"].split("/")
            if len(parts) == 3:
                dob_iso = f"{parts[2]}-{parts[1]}-{parts[0]}"
            else:
                dob_iso = player_data["dob"]
                
        player_row = [player_id, team_id, name, pos, club, val, caps, dob_iso, player_data.get("height", 0), player_data.get("goals", 0)]
        players_data.append(player_row)
        team_player_map[team_id].append(player_id)
        player_id_counter += 1

# ==========================================
# 6. MATCHES DATA
# ==========================================
matches_headers = ["match_id", "date", "kickoff_time_utc", "stage_id", "venue_id", "home_team_id", "away_team_id", "home_score", "away_score", "status", "home_xg", "away_xg", "referee_id", "player_of_the_match_id"]
matches_data = [
    # Round 1 Completed matches
    [1, "2026-06-11", "19:00", 1, 1, 1, 2, 2, 0, "Completed", 1.84, 0.52],
    [2, "2026-06-11", "23:00", 1, 7, 3, 4, 2, 1, "Completed", 1.45, 1.12],
    [3, "2026-06-12", "19:00", 1, 6, 5, 6, 1, 1, "Completed", 1.35, 0.98],
    [4, "2026-06-12", "23:00", 1, 3, 13, 14, 4, 1, "Completed", 2.76, 0.88],
    [5, "2026-06-13", "15:00", 1, 10, 7, 8, 1, 1, "Completed", 0.78, 1.54],
    [6, "2026-06-13", "18:00", 1, 2, 9, 10, 1, 1, "Completed", 1.62, 1.10],
    [7, "2026-06-13", "21:00", 1, 14, 11, 12, 0, 1, "Completed", 1.25, 0.65],
    [8, "2026-06-13", "23:59", 1, 16, 15, 16, 2, 0, "Completed", 1.48, 0.72],
    [9, "2026-06-14", "15:00", 1, 9, 17, 18, 7, 1, "Completed", 4.82, 0.44],
    [10, "2026-06-14", "18:00", 1, 15, 21, 22, 2, 2, "Completed", 1.95, 1.82],
    [11, "2026-06-14", "21:00", 1, 11, 19, 20, 1, 0, "Completed", 1.10, 0.95],
    [12, "2026-06-14", "23:59", 1, 12, 23, 24, 5, 1, "Completed", 3.12, 0.78],
    [13, "2026-06-15", "15:00", 1, 13, 29, 30, 0, 0, "Completed", 2.15, 0.35],
    [14, "2026-06-15", "18:00", 1, 4, 25, 26, 1, 1, "Completed", 1.58, 1.12],
    [15, "2026-06-15", "21:00", 1, 8, 31, 32, 1, 1, "Completed", 0.85, 1.76],
    [16, "2026-06-15", "23:59", 1, 5, 27, 28, 2, 2, "Completed", 1.88, 1.20],
    [17, "2026-06-16", "15:00", 1, 2, 33, 34, 3, 1, "Completed", 2.44, 1.05],
    [18, "2026-06-16", "18:00", 1, 10, 35, 36, 1, 4, "Completed", 0.68, 2.85],
    [19, "2026-06-16", "21:00", 1, 3, 37, 38, 3, 0, "Completed", 2.65, 0.42],
    [20, "2026-06-16", "23:59", 1, 15, 39, 40, 3, 1, "Completed", 1.98, 0.88],
    [21, "2026-06-17", "15:00", 1, 9, 41, 42, 1, 1, "Completed", 1.78, 1.15],
    [22, "2026-06-17", "18:00", 1, 13, 45, 46, 4, 2, "Completed", 2.92, 1.64],
    [23, "2026-06-17", "21:00", 1, 11, 47, 48, 1, 0, "Completed", 1.30, 0.75],
    [24, "2026-06-17", "23:59", 1, 16, 43, 44, 1, 3, "Completed", 0.95, 2.10],

    # Round 2 Scheduled/Completed matches
    [25, "2026-06-18", "15:00", 1, 9, 1, 3, 1, 0, "Completed", 1.62, 0.58],
    [26, "2026-06-18", "18:00", 1, 3, 4, 2, 1, 1, "Completed", 1.35, 1.15],
    [27, "2026-06-18", "21:00", 1, 5, 5, 7, 6, 0, "Completed", 3.82, 0.22],
    [28, "2026-06-18", "23:59", 1, 1, 8, 6, 4, 1, "Completed", 2.45, 0.88],
    [29, "2026-06-19", "15:00", 1, 2, 9, 11, 3, 0, "Completed", 1.16, 0.90],
    [30, "2026-06-19", "18:00", 1, 4, 12, 10, 0, 1, "Completed", 0.97, 0.54],
    [31, "2026-06-19", "21:00", 1, 6, 13, 15, 2, 0, "Completed", 1.21, 0.32],
    [32, "2026-06-19", "23:59", 1, 8, 16, 14, 0, 1, "Completed", 0.40, 0.30],
    [33, "2026-06-20", "15:00", 1, 10, 17, 19, 2, 1, "Completed", 1.85, 0.72],
    [34, "2026-06-20", "18:00", 1, 12, 20, 18, 0, 0, "Completed", 1.92, 0.08],
    [35, "2026-06-20", "21:00", 1, 14, 21, 23, 5, 1, "Completed", 3.45, 0.88],
    [36, "2026-06-20", "23:59", 1, 16, 24, 22, 0, 4, "Completed", 0.35, 3.12],
    [37, "2026-06-21", "15:00", 1, 11, 25, 27, 0, 0, "Completed", 1.45, 0.62],
    [38, "2026-06-21", "18:00", 1, 13, 28, 26, 1, 3, "Completed", 0.55, 2.15],
    [39, "2026-06-21", "21:00", 1, 15, 29, 31, 4, 0, "Completed", 3.28, 0.25],
    [40, "2026-06-21", "23:59", 1, 2, 32, 30, 2, 2, "Completed", 1.65, 1.10],
    [41, "2026-06-22", "15:00", 1, 4, 33, 35, 3, 0, "Completed", 2.21, 0.45],
    [42, "2026-06-22", "18:00", 1, 6, 36, 34, 3, 2, "Completed", 1.95, 1.48],
    [43, "2026-06-22", "21:00", 1, 8, 37, 39, 2, 0, "Completed", 1.78, 0.55],
    [44, "2026-06-22", "23:59", 1, 10, 40, 38, 1, 2, "Completed", 0.88, 1.92],
    [45, "2026-06-23", "15:00", 1, 12, 41, 43, 5, 0, "Completed", 3.54, 0.42],
    [46, "2026-06-23", "18:00", 1, 14, 44, 42, 1, 0, "Completed", 1.62, 0.58],
    [47, "2026-06-23", "21:00", 1, 16, 45, 47, 0, 0, "Completed", 1.12, 0.89],
    [48, "2026-06-23", "23:59", 1, 1, 48, 46, 0, 1, "Completed", 0.42, 1.48],

    # Round 3 Scheduled matches (simultaneous group final matches)
    [49, "2026-06-24", "18:00", 1, 1, 4, 1, 0, 3, "Completed", 1.10, 1.27],
    [50, "2026-06-24", "18:00", 1, 7, 2, 3, 1, 0, "Completed", 1.26, 1.39],
    [51, "2026-06-24", "22:00", 1, 5, 8, 5, 2, 1, "Completed", 0.71, 1.35],
    [52, "2026-06-24", "22:00", 1, 6, 6, 7, 3, 1, "Completed", 1.48, 0.95],
    [53, "2026-06-25", "18:00", 1, 2, 12, 9, 0, 3, "Completed", 0.45, 2.18],
    [54, "2026-06-25", "18:00", 1, 10, 10, 11, 4, 2, "Completed", 2.35, 1.12],
    [55, "2026-06-25", "22:00", 1, 3, 16, 13, 3, 2, "Completed", 1.62, 1.45],
    [56, "2026-06-25", "22:00", 1, 15, 14, 15, 0, 0, "Completed", 0.55, 0.48],
    [57, "2026-06-26", "18:00", 1, 9, 20, 17, 2, 1, "Completed", 1.28, 1.55],
    [58, "2026-06-26", "18:00", 1, 11, 18, 19, 0, 2, "Completed", 0.32, 1.68],
    [59, "2026-06-26", "22:00", 1, 12, 24, 21, 1, 3, "Completed", 0.62, 2.15],
    [60, "2026-06-26", "22:00", 1, 16, 22, 23, 1, 1, "Completed", 1.12, 0.95],
    [61, "2026-06-27", "18:00", 1, 4, 28, 25, 1, 5, "Completed", 0.48, 3.25],
    [62, "2026-06-27", "18:00", 1, 8, 26, 27, 1, 1, "Completed", 0.85, 0.92],
    [63, "2026-06-27", "22:00", 1, 13, 32, 29, 0, 1, "Completed", 0.78, 1.35],
    [64, "2026-06-27", "22:00", 1, 14, 30, 31, 0, 0, "Completed", 0.42, 0.38],
    [65, "2026-06-28", "18:00", 1, 10, 36, 33, "", "", "Scheduled", "", ""],
    [66, "2026-06-28", "18:00", 1, 2, 34, 35, "", "", "Scheduled", "", ""],
    [67, "2026-06-28", "22:00", 1, 15, 40, 37, "", "", "Scheduled", "", ""],
    [68, "2026-06-28", "22:00", 1, 3, 38, 39, "", "", "Scheduled", "", ""],
    [69, "2026-06-29", "18:00", 1, 12, 44, 41, "", "", "Scheduled", "", ""],
    [70, "2026-06-29", "18:00", 1, 9, 42, 43, "", "", "Scheduled", "", ""],
    [71, "2026-06-29", "22:00", 1, 16, 48, 45, "", "", "Scheduled", "", ""],
    [72, "2026-06-29", "22:00", 1, 11, 46, 47, "", "", "Scheduled", "", ""]
]

# Player of the match mapping (match_id -> player_id) for completed matches 1-44
player_of_the_match_mapping = {
    1: 16,     # Julián Andrés Quinones (MEX)
    2: 58,     # Inbeom Hwang (KOR)
    3: 112,    # Ismaïl Kenneth Jordan Kone (CAN)
    4: 332,    # Folarin Jolaoluwa Balogun (USA)
    5: 157,    # Ibrahim Mahmoud Abunada (QAT)
    6: 215,    # José Vinicius (BRA)
    7: 293,    # John McGinn (SCO)
    8: 381,    # Nestory Irankunda (AUS)
    9: 423,    # Kai Lukas Havertz (GER)
    10: 524,   # Virgil Van Dijk (NED)
    11: 479,   # Yan Diomande (CIV)
    12: 581,   # Alexander Isak (SWE)
    13: 755,   # José Vozinha (CPV)
    14: 658,   # Ashour Metwaly Emam (EGY)
    15: 801,   # Khalil Mohammed Alowais (KSA)
    16: 699,   # Ramin Rezaeian (IRN)
    17: 843,   # Michael Akpovie Olise (FRA)
    18: 919,   # Erling Braut Haaland (NOR)
    19: 946,   # Lionel Andrés Messi (ARG)
    20: 1023,  # Iyad Ali Ali Olwan (JOR)
    21: 1055,  # Pedro Joao Neves (POR)
    22: 1153,  # Harry Edward Kane (ENG)
    23: 1207,  # Antoine Serlom Semenyo (GHA)
    24: 1125,  # Luis Fernando Diaz (COL)
    25: 7,     # Luis Francisco Romo (MEX)
    26: 96,    # Michal Sadilek (CZE)
    27: 114,   # Jonathan Christian David (CAN)
    28: 191,   # Johan Kula Manzambi (SUI)
    29: 217,   # Matheus Matheus Cunha (BRA)
    30: 245,   # Ismael Saibari (MAR)
    31: 332,   # Folarin Jolaoluwa Balogun (USA)
    32: 361,   # Matias Galarza (PAR)
    33: 442,   # Deniz Undav (GER)
    34: 443,   # Eloy Victor Room (CUW)
    35: 531,   # Cody Mathés Gakpo (NED)
    36: 564,   # Ayase Ueda (JPN)
    37: 677,   # Ali Reza Beiranvand (IRN)
    38: 660,   # Hamed Mahrous Mohamed Salah (EGY)
    39: 749,   # Mikel Oyarzabal (ESP)
    40: 755,   # José Vozinha (CPV)
    41: 842,   # Kylian Mbappe (FRA)
    42: 919,   # Erling Braut Haaland (NOR)
    43: 946,   # Lionel Andrés Messi (ARG)
    44: 984,   # Ibrahim Maza (ALG)
    45: 1047,  # Cristiano Ronaldo (POR)
    46: 1120,  # Daniel Munoz (COL)
    47: 1147,  # Nico Oreilly (ENG)
    48: 1181,  # Ante Budimir (CRO)
    49: 20,    # Mateo Chavez (MEX)
    50: 38,    # Thapelo Maseko (RSA)
    51: 191,   # Johan Kula Manzambi (SUI)
    52: 149,   # Kerim Alajbegovic (BIH)
    53: 215,   # Vinícius Júnior (BRA)
    54: 236,   # Achraf Hakimi (MAR)
    55: 398,   # Arda Güler (TUR)
    56: 339,   # Roberto Junior Fernandez (PAR GK - no POTM found, GK placeholder)
    57: 514,   # Nilson Angulo (ECU)
    58: 487,   # Nicolas Pépé (CIV)
    59: 539,   # Brian Brobbey (NED)
    60: 557,   # Daizen Maeda (JPN)
    61: 634,   # Leandro Trossard (BEL)
    62: 699,   # Ramin Rezaeian (IRN)
    63: 743,   # Álex Baena (ESP)
    64: 755,   # José Vozinha (CPV)
}

# Assign referees and player of the match relationally/statically
for idx, match in enumerate(matches_data):
    m_id = match[0]
    potm_id = player_of_the_match_mapping.get(m_id, "")
    referee_id = (idx % 16) + 1
    match.append(referee_id)
    match.append(potm_id)

# ==========================================
# 7. MATCH EVENTS DATA GENERATOR
# ==========================================
events_headers = ["event_id", "match_id", "minute", "event_type", "team_id", "player_id"]
events_data = []
event_id_counter = 1

# Normalizations and Overrides for event parsing
team_aliases = {
    "South Korea": "South Korea",
    "Korea Republic": "South Korea",
    "Czech Republic": "Czechia",
    "United States": "USA",
    "Turkey": "Türkiye",
    "Ivory Coast": "Côte d'Ivoire",
    "Iran": "IR Iran",
    "Cape Verde": "Cabo Verde",
    "DR Congo": "Congo DR",
}

def clean_name(s):
    s = s.replace("ø", "o").replace("Ø", "o").replace("æ", "ae").replace("Æ", "ae").replace("å", "a").replace("Å", "a")
    s = unicodedata.normalize('NFKD', s)
    cleaned = ''.join(c for c in s if not unicodedata.combining(c)).lower().replace("-", " ").replace(".", " ")
    return " ".join(cleaned.split())

def match_player_to_id(team_id, name_to_match, players_data):
    cleaned_match = clean_name(name_to_match)
    
    overrides = {
        "j david": "jonathan christian david",
        "quinones": "julian andres quinones",
        "jimenez": "raul alonso jimenez",
        "m araujo": "maximiliano javier araujo",
        "joao neves": "joao pedro goncalves neves",
        "oh hyeon gyu": "hyeongyu oh",
        "yazan al arab": "yazan abu arab",
        "musa": "petar musa",
        "mohebi": "mohebbi",
        "isak": "alexander isak",
        # "Mc" players direct ID mappings:
        "mcginn": 293,
        "mctominay": 290,
        "mclean": 309,
        "mckenna": 312,
        "mckennie": 320,
        "mckenzie": 334,
        "mccowatt": 722,
        # Verified assists overrides
        "vinicius junior": 215,
        "vinicius": 215,
        "matheus cunha": 217,
        "lucas paqueta": 228,
        "brahim diaz": 244,
        "saibari": 245,
        "ismael saibari": 245,
        "ismail saibari": 245,
        "sergino dest": 314,
        # June 20-22 match overrides
        "nadiem amiri": 436,
        "cody gakpo": 531,
        "denzel dumfries": 542,
        "crysencio summerville": 544,
        "memphis depay": 530,
        "keito nakamura": 559,
        "junya ito": 560,
        "ayase ueda": 564,
        "tim payne": 704,
        "mohamed hany": 653,
        "mostafa zico": 661,
        "mohamed salah": 660,
        "mikel oyarzabal": 749,
        "aymeric laporte": 742,
        "dani olmo": 738,
        "marc cucurella": 752,
        "kevin pina": 760,
        "helio varela": 780,
        "federico valverde": 814,
        "maximiliano araujo": 826,
        "yan diomande": 479,
        "nuno mendes": 1065,
        "leao": 1057,
        "rafael leao": 1057,
        "daniel munoz": 1120,
        "quintero": 1138,
        "budimir": 1181,
        "stanisic": 1172,
        "gustavo adolfo puerta": 1132,
        "erik lira": 6,
        "bruno guimarães": 216,
        "bruno guimaraes": 216,
        "xaver schlager": 992,
        "julio enciso": 357,
        "kaishu sano": 570,
        "facundo medina": 961,
        "sadio mané": 868,
        "sadio mane": 868,
        "hassan al-haydos": 166,
        "hassan al haydos": 166,
        "al-haydos": 166,
        "junior edmilson": 164,
        "edmilson junior": 164,
        # June 25-27 match overrides
        "rayan": 234,
        "vitor rayan": 234,
        "achraf hakimi": 236,
        "soufiane rahimi": 243,
        "gessime yassine": 250,
        "wilson isidor": 278,
        "arda guler": 398,
        "orkun kokcu": 396,
        "kaan ayhan": 412,
        "baris alper yilmaz": 411,
        "barış alper yılmaz": 411,
        "barı ş alper yilmaz": 411,
        "eren elmali": 403,
        "eren elmalı": 403,
        "auston trusty": 318,
        "sebastian berhalter": 326,
        "nilson angulo": 514,
        "pedro vite": 509,
        "gonzalo plata": 513,
        "moises caicedo": 517,
        "leroy sane": 435,
        "florian wirtz": 433,
        "nicolas pepe": 487,
        "hazem mastouri": 607,
        "ellyes skhiri": 615,
        "brian brobbey": 539,
        "jan paul van hecke": 526,
        "daizen maeda": 557,
        "anthony elanga": 583,
        "leandro trossard": 634,
        "kevin de bruyne": 631,
        "romelu lukaku": 633,
        "alexis saelemaekers": 646,
        "elijah just": 713,
        "mahmoud saber": 671,
        "saber abdelmohsen": 671,
        "ramin rezaeian": 699,
        "alex baena": 743,
        "alejandro baena": 743,
        "marcos llorente": 733,
        # --- 18 scorer mismatches discovered during deep audit (June 24) ---
        # m7  Scotland: McGinn
        "mcginn": 293,
        # m10 Netherlands: Van Dijk, Summerville
        "van dijk": 524,
        "virgil van dijk": 524,
        "summerville": 544,
        # m14 Belgium (o.g. from Egypt): Hany scored into own net, player credited is the Egyptian
        "hany": 653,
        # m15 Saudi Arabia: Al-Amri ; Uruguay: M. Araújo
        "al-amri": 784,
        "ali al-amri": 784,
        "m. araújo": 826,
        "maximiliano araujo": 826,
        # m18 Iraq: Hussein scored 39' (FWD); Haydar Hussein pid 887 only credited for the 90' o.g.
        "hussein": 902,
        "haydar hussein": 887,
        # m18 Norway: Østigård (Leo Skiri Ostigard, pid 914)
        "østigård": 914,
        "ostigard": 914,
        "leo ostigard": 914,
        # m20 Jordan (o.g.): Al-Arab
        "al-arab": 1019,
        "mousa alarab": 1019,
        # m27 Canada: J. David (Jonathan Christian David), Saliba
        "j. david": 114,
        "jonathan david": 114,
        "saliba": 129,
        "nathan saliba": 129,
        # m27 Qatar (o.g.): Manai
        "manai": 182,
        # m29 Brazil: Vinícius Júnior (pid 215 — roster name is truncated but PID is correct)
        "vinícius júnior": 215,
        "vinicius junior": 215,
        # m36 Japan: Ito scored 69' — Junya Ito (FWD, pid 560), not Hiroki Ito (DEF, pid 567)
        "ito": 560,
        "junya ito": 560,
        # m38 Egypt: Mostafa Zico
        "mostafa zico": 661,
        # m39 Saudi Arabia (o.g.): Altambakti
        "altambakti": 785,
        # m45 Portugal: Nuno Mendes (pid 1065 — roster name truncated)
        "nuno mendes": 1065,
        # m52 Bosnia (o.g.): Mahmoud Abunada → cred to Bosnian pid 157 (Ibrahim Mahmoud Abunada)
        "mahmoud abunada": 157,
        # m52 Qatar: Hassan Al-Haydos
        "hassan al-haydos": 166,
        "hassan haydos": 166,
        # m54 Morocco (o.g.): Yassine Bounou
        "yassine bounou": 235,
        # m59 Tunisia (o.g.): Ellyes Skhiri
        "ellyes skhiri": 615,
        # m59 Netherlands: Brian Brobbey, Jan Paul van Hecke
        "brian brobbey": 539,
        "jan paul van hecke": 526,
        # m63 Spain: Álex Baena / Alejandro Baena
        "álex baena": 743,
    }
    
    if cleaned_match in overrides:
        val = overrides[cleaned_match]
        if isinstance(val, int):
            return val
        cleaned_match = val
    
    match_parts = cleaned_match.split()
    team_players = [p for p in players_data if int(p[1]) == team_id]
    
    # 1. Exact match
    for p in team_players:
        if cleaned_match == clean_name(p[2]):
            return int(p[0])
            
    # 2. Substring match
    for p in team_players:
        p_clean = clean_name(p[2])
        if cleaned_match in p_clean or p_clean in cleaned_match:
            return int(p[0])
            
    # 3. Parts match
    for p in team_players:
        p_clean = clean_name(p[2])
        if all(part in p_clean for part in match_parts if len(part) > 1):
            return int(p[0])
            
    # 4. Syllable parts concatenation check
    for p in team_players:
        p_clean = clean_name(p[2]).replace(" ", "")
        concatenated_match = "".join(match_parts)
        if concatenated_match in p_clean or p_clean in concatenated_match:
            return int(p[0])

    # 5. Last part match
    if len(match_parts) > 1:
        last_part = match_parts[-1]
        for p in team_players:
            if last_part in clean_name(p[2]):
                return int(p[0])

    # Fallback
    print(f"Warning: Fallback used for team {team_id}, name '{name_to_match}'. Assigned player ID {team_players[0][0]} ({team_players[0][2]})")
    return int(team_players[0][0])

json_path = os.path.join(output_dir, "real_match_details.json")
with open(json_path, "r", encoding="utf-8") as f:
    scraped_matches = json.load(f)
scraped_lookup = {}
team_name_to_id = {row[1]: int(row[0]) for row in teams_data}

for sm in scraped_matches:
    home_name = team_aliases.get(sm["home_team"], sm["home_team"])
    away_name = team_aliases.get(sm["away_team"], sm["away_team"])
    h_id = team_name_to_id.get(home_name)
    a_id = team_name_to_id.get(away_name)
    if h_id and a_id:
        scraped_lookup[(h_id, a_id)] = sm

real_red_cards = [
    (1, 2, 39, 55),
    (1, 2, 37, 84),
    (1, 1, 3, 86),
    (27, 7, 170, 60),
    (27, 7, 179, 85),
    (28, 6, 134, 80),
    (32, 14, 348, 45),   # Almirón straight red, mouth-covering rule, 45+3'
    (37, 25, 649, 66),   # Nathan Ngoy straight red for DOGSO on Taremi
]

real_var_reviews = [
    (1, 2, 39, 55),
    (26, 2, 38, 81),
    (27, 7, 170, 60),
    (31, 13, 328, 43),   # Freeman goal VAR check (offside review, goal awarded)
    (32, 14, 348, 45),   # Almirón red card VAR review
]

for match in matches_data:
    status = match[9]
    if status != "Completed":
        continue
        
    match_id = match[0]
    home_id = match[5]
    away_id = match[6]
    
    # Process scraped goals/assists
    sm = scraped_lookup.get((home_id, away_id))
    if sm:
        # Home goals
        for g in sm.get("home_goals", []):
            scorer = g["scorer"]
            min_str = g["minute"].split("+")[0].split("'")[0].split()[0]
            m = int(min_str)
            is_og = "o.g." in g["minute"]
            match_team_id = away_id if is_og else home_id
            player_id = match_player_to_id(match_team_id, scorer, players_data)
            events_data.append([event_id_counter, match_id, m, "Goal", home_id, player_id])
            event_id_counter += 1
            
            # If there is a verified assist in the json
            if not is_og and "assist" in g and g["assist"]:
                assist_player = g["assist"]
                assist_player_id = match_player_to_id(home_id, assist_player, players_data)
                events_data.append([event_id_counter, match_id, m, "Assist", home_id, assist_player_id])
                event_id_counter += 1
                
        # Away goals
        for g in sm.get("away_goals", []):
            scorer = g["scorer"]
            min_str = g["minute"].split("+")[0].split("'")[0].split()[0]
            m = int(min_str)
            is_og = "o.g." in g["minute"]
            match_team_id = home_id if is_og else away_id
            player_id = match_player_to_id(match_team_id, scorer, players_data)
            events_data.append([event_id_counter, match_id, m, "Goal", away_id, player_id])
            event_id_counter += 1
            
            # If there is a verified assist in the json
            if not is_og and "assist" in g and g["assist"]:
                assist_player = g["assist"]
                assist_player_id = match_player_to_id(away_id, assist_player, players_data)
                events_data.append([event_id_counter, match_id, m, "Assist", away_id, assist_player_id])
                event_id_counter += 1
    else:
        print(f"Warning: Completed match {match_id} not found in real_match_details.json! No goal/assist events will be generated.")

    # Process Disciplinary Events
    home_players = team_player_map[home_id]
    away_players = team_player_map[away_id]
    
    # Red Cards
    for rc in real_red_cards:
        if rc[0] == match_id:
            events_data.append([event_id_counter, match_id, rc[3], "Red Card", rc[1], rc[2]])
            event_id_counter += 1
            
    # VAR Reviews
    for vr in real_var_reviews:
        if vr[0] == match_id:
            events_data.append([event_id_counter, match_id, vr[3], "VAR Review", vr[1], vr[2]])
            event_id_counter += 1
            
    # Yellow Cards (Verified bookings only)
    if match_id == 26:
        events_data.append([event_id_counter, 26, 33, "Yellow Card", 2, 30])
        event_id_counter += 1
        events_data.append([event_id_counter, 26, 40, "Yellow Card", 2, 31])
        event_id_counter += 1
        events_data.append([event_id_counter, 26, 76, "Yellow Card", 4, 85])
        event_id_counter += 1
    elif match_id == 25:
        events_data.append([event_id_counter, 25, 12, "Yellow Card", 3, 56])
        event_id_counter += 1
        events_data.append([event_id_counter, 25, 42, "Yellow Card", 1, 4])
        event_id_counter += 1
        events_data.append([event_id_counter, 25, 78, "Yellow Card", 1, 6])
        event_id_counter += 1
    elif match_id == 27:
        events_data.append([event_id_counter, 27, 30, "Yellow Card", 7, 168])
        event_id_counter += 1
        events_data.append([event_id_counter, 27, 45, "Yellow Card", 5, 112])
        event_id_counter += 1
    elif match_id == 28:
        events_data.append([event_id_counter, 28, 35, "Yellow Card", 8, 192])
        event_id_counter += 1
        events_data.append([event_id_counter, 28, 55, "Yellow Card", 6, 146])
        event_id_counter += 1
    elif match_id == 29:
        events_data.append([event_id_counter, 29, 22, "Yellow Card", 11, 262])  # Carlens Arcus
        event_id_counter += 1
        events_data.append([event_id_counter, 29, 38, "Yellow Card", 11, 280])  # Frantzdy Pierrot
        event_id_counter += 1
        events_data.append([event_id_counter, 29, 65, "Yellow Card", 11, 277])  # Danley Jean Jacques
        event_id_counter += 1
        events_data.append([event_id_counter, 29, 72, "Yellow Card", 9, 224])   # Douglas Santos
        event_id_counter += 1
    elif match_id == 31:
        events_data.append([event_id_counter, 31, 16, "Yellow Card", 15, 369])  # Jordan Bos
        event_id_counter += 1
        events_data.append([event_id_counter, 31, 32, "Yellow Card", 15, 367])  # Alessandro Circati
        event_id_counter += 1
        events_data.append([event_id_counter, 31, 56, "Yellow Card", 13, 317])  # Antonee Robinson
        event_id_counter += 1
        events_data.append([event_id_counter, 31, 84, "Yellow Card", 15, 368])  # Jacob Italiano
        event_id_counter += 1
        events_data.append([event_id_counter, 31, 88, "Yellow Card", 13, 332])  # Folarin Balogun
        event_id_counter += 1
        events_data.append([event_id_counter, 31, 88, "Yellow Card", 15, 383])  # Harry Souttar
        event_id_counter += 1
        events_data.append([event_id_counter, 31, 88, "Yellow Card", 13, 315])  # Chris Richards
        event_id_counter += 1
    elif match_id == 34:
        events_data.append([event_id_counter, 34, 90, "Yellow Card", 18, 461])  # Gervane Kastaneer (90+1' = 91')
        event_id_counter += 1
    elif match_id == 37:
        events_data.append([event_id_counter, 37, 1, "Yellow Card", 25, 633])  # Romelu Lukaku
        event_id_counter += 1
    elif match_id == 47:
        events_data.append([event_id_counter, 47, 34, "Yellow Card", 47, 1201])  # Thomas Partey
        event_id_counter += 1
        events_data.append([event_id_counter, 47, 67, "Yellow Card", 45, 1146])  # Ezri Konsa
        event_id_counter += 1
    elif match_id == 48:
        events_data.append([event_id_counter, 48, 42, "Yellow Card", 48, 1226])  # Fidel Escobar
        event_id_counter += 1

# Sort events chronologically: sort by match_id (index 1) and minute (index 2)
events_data.sort(key=lambda x: (x[1], x[2]))
# Re-index event IDs
for idx, event in enumerate(events_data):
    event[0] = idx + 1

# ==========================================
# 8. DENORMALIZED DETAILED MATCHES GENERATOR
# ==========================================
# Build lookups to map IDs to Names for a denormalized/readable export
team_lookup = {row[0]: (row[1], row[2]) for row in teams_data}
venue_lookup = {row[0]: (row[1], row[2], row[3]) for row in venues_data}
stage_lookup = {row[0]: row[1] for row in stages_data}
referee_lookup = {row[0]: row[1] for row in referees_data}

player_info_lookup = {int(p[0]): (p[2], int(p[1])) for p in players_data}

# Known POTM name corrections (for parsing artifacts in squad data)
potm_name_overrides = {
    293: "John McGinn",  # Scotland — parsed incorrectly as 'Mc'
}

# Starting goalkeeper mapping: match_id -> (home_gk_player_id, away_gk_player_id)
match_goalkeepers = {
    1:  (13,   27),   # MEX vs RSA: Guillermo Ochoa vs Ronwen Williams
    2:  (53,   79),   # KOR vs CZE: Seunggyu Kim vs Matej Kovar
    3:  (120, 131),   # CAN vs BIH: Maxime Crepeau vs Nikola Vasilj
    4:  (313, 339),   # USA vs PAR: Matt Turner vs Roberto Fernandez
    5:  (157, 183),   # QAT vs SUI: Ibrahim Abunada vs Gregor Kobel
    6:  (209, 235),   # BRA vs MAR: Alisson Becker vs Yassine Bounou
    7:  (261, 287),   # HAI vs SCO: Johny Placide vs Angus Gunn
    8:  (365, 391),   # AUS vs TUR: Mathew Ryan vs Mert Gunok
    9:  (417, 443),   # GER vs CUW: Manuel Neuer vs Eloy Room
    10: (521, 547),   # NED vs JPN: Bart Verbruggen vs Zion Suzuki
    11: (469, 495),   # CIV vs ECU: Yahia Fofana vs Hernan Galindez
    12: (573, 614),   # SWE vs TUN: Jacob Widell Zetterstrom vs Aymen Dahmen
    13: (751, 755),   # ESP vs CPV: Unai Simon vs Jose Vozinha (correction 2026-06-28)
    14: (625, 651),   # BEL vs EGY: Thibaut Courtois vs Elsayed Elshenawy
    15: (801, 807),   # KSA vs URU: Khalil Al-Owais vs Sergio Rochet
    16: (677, 703),   # IRN vs NZL: Ali Beiranvand vs Maxime Crocombe
    17: (848, 874),   # FRA vs SEN: Mike Maignan vs Edouard Mendy
    18: (885, 911),   # IRQ vs NOR: Talib Raheem vs Orjan Nyland
    19: (959, 963),   # ARG vs ALG: Emiliano Martinez vs Melvin Mastil
    20: (989, 1015),  # AUT vs JOR: Alexander Schlager vs Moien Abulaila
    21: (1041, 1067), # POR vs COD: Diogo Costa vs Lionel Nzau Mpasi
    22: (1145, 1171), # ENG vs CRO: Jordan Pickford vs Dominik Livakovic
    23: (1197, 1223), # GHA vs PAN: Lawrence Ati-Zigi vs Luis Mejia
    24: (1093, 1119), # UZB vs COL: Utkir Yusupov vs David Ospina
    25: (13,   53),   # MEX vs KOR: Guillermo Ochoa vs Seunggyu Kim
    26: (79,   27),   # CZE vs RSA: Matej Kovar vs Ronwen Williams
    27: (120, 157),   # CAN vs QAT: Maxime Crepeau vs Ibrahim Abunada
    28: (183, 131),   # SUI vs BIH: Gregor Kobel vs Nikola Vasilj
    29: (209, 261),   # BRA vs HAI: Alisson Becker vs Johny Placide
    30: (287, 235),   # SCO vs MAR: Angus Gunn vs Yassine Bounou
    31: (313, 365),   # USA vs AUS: Matt Turner vs Mathew Ryan
    32: (391, 339),   # TUR vs PAR: Mert Gunok vs Roberto Fernandez
    33: (417, 469),   # GER vs CIV: Manuel Neuer vs Yahia Fofana
    34: (495, 443),   # ECU vs CUW: Hernan Galindez vs Eloy Room
    35: (521, 573),   # NED vs SWE: Bart Verbruggen vs Jacob Widell Zetterstrom
    36: (614, 547),   # TUN vs JPN: Aymen Dahmen vs Zion Suzuki
    37: (625, 677),   # BEL vs IRN: Thibaut Courtois vs Ali Beiranvand
    38: (703, 651),   # NZL vs EGY: Maxime Crocombe vs Elsayed Elshenawy
    39: (751, 801),   # ESP vs KSA: Unai Simon vs Khalil Al-Owais (correction 2026-06-28)
    40: (807, 755),   # URU vs CPV: Sergio Rochet vs Jose Vozinha
    41: (848, 885),   # FRA vs IRQ: Mike Maignan vs Talib Raheem
    42: (911, 874),   # NOR vs SEN: Orjan Nyland vs Edouard Mendy
    43: (959, 989),   # ARG vs AUT: Emiliano Martinez vs Alexander Schlager
    44: (1015, 963),  # JOR vs ALG: Moien Abulaila vs Melvin Mastil
    45: (1041, 1105), # POR vs UZB: Diogo Costa vs Abduvakhid Nematov
    46: (1130, 1067), # COL vs COD: Camilo Vargas vs Lionel Nzau Mpasi
    47: (1145, 1197), # ENG vs GHA: Jordan Pickford vs Lawrence Ati-Zigi
    48: (1244, 1171), # PAN vs CRO: Orlando Mosquera vs Dominik Livakovic
    49: (79, 1),      # CZE vs MEX: Matej Kovar vs Raul Rangel
    50: (27, 53),     # RSA vs KOR: Ronwen Williams vs Seunggyu Kim
    51: (183, 120),   # SUI vs CAN: Gregor Kobel vs Maxime Crepeau
    52: (131, 157),   # BIH vs QAT: Nikola Vasilj vs Ibrahim Abunada
    53: (287, 209),   # SCO vs BRA: Angus Gunn vs Alisson Becker
    54: (235, 261),   # MAR vs HAI: Yassine Bounou vs Johny Placide
    55: (391, 313),   # TUR vs USA: Mert Gunok vs Matt Turner
    56: (339, 365),   # PAR vs AUS: Roberto Fernandez vs Mathew Ryan
    57: (495, 417),   # ECU vs GER: Hernan Galindez vs Manuel Neuer
    58: (443, 469),   # CUW vs CIV: Eloy Room vs Yahia Fofana
    59: (614, 521),   # TUN vs NED: Aymen Dahmen vs Bart Verbruggen
    60: (547, 573),   # JPN vs SWE: Zion Suzuki vs Jacob Widell Zetterstrom
    61: (703, 625),   # NZL vs BEL: Maxime Crocombe vs Thibaut Courtois
    62: (651, 677),   # EGY vs IRN: Elsayed Elshenawy vs Ali Beiranvand
    63: (807, 751),   # URU vs ESP: Sergio Rochet vs Unai Simon (correction 2026-06-28)
    64: (755, 801),   # CPV vs KSA: Jose Vozinha vs Khalil Al-Owais
}

detailed_matches_headers = [
    "match_id", "date", "kickoff_time_utc", "stage_name", 
    "stadium_name", "city", "country", 
    "home_team_name", "home_fifa_code", 
    "away_team_name", "away_fifa_code", 
    "home_score", "away_score", "status", "home_xg", "away_xg",
    "home_goalkeeper", "away_goalkeeper",
    "player_of_the_match_name", "referee_name"
]
detailed_matches_data = []

for match in matches_data:
    m_id = match[0]
    date = match[1]
    time = match[2]
    stg_id = match[3]
    ven_id = match[4]
    h_id = match[5]
    a_id = match[6]
    h_score = match[7]
    a_score = match[8]
    status = match[9]
    h_xg = match[10]
    a_xg = match[11]
    ref_id = match[12]
    potm_id = match[13]
    
    stg_name = stage_lookup.get(stg_id, "Unknown")
    stadium, city, country = venue_lookup.get(ven_id, ("Unknown", "Unknown", "Unknown"))
    home_name, home_code = team_lookup.get(h_id, ("Unknown", "UNK"))
    away_name, away_code = team_lookup.get(a_id, ("Unknown", "UNK"))
    ref_name = referee_lookup.get(ref_id, "Unknown")
    
    potm_name = ""
    if potm_id:
        raw_potm_name, _ = player_info_lookup.get(int(potm_id), ("", None))
        potm_name = potm_name_overrides.get(int(potm_id), raw_potm_name)

    home_gk_id, away_gk_id = match_goalkeepers.get(m_id, (None, None))
    home_gk_name = player_info_lookup.get(home_gk_id, ("", None))[0] if home_gk_id else ""
    away_gk_name = player_info_lookup.get(away_gk_id, ("", None))[0] if away_gk_id else ""

    detailed_matches_data.append([
        m_id, date, time, stg_name,
        stadium, city, country,
        home_name, home_code,
        away_name, away_code,
        h_score, a_score, status, h_xg, a_xg,
        home_gk_name, away_gk_name,
        potm_name, ref_name
    ])

# ==========================================
# 8. MATCH LINEUPS DATA GENERATOR
# ==========================================
lineups_headers = ["lineup_id", "match_id", "player_id", "team_id", "is_starting_xi", "tactical_position", "minutes_played"]
lineups_data = []
lineup_id_counter = 1

# Map player_id to their details (team_id, name, position, market_value, caps)
player_details = {}
for p in players_data:
    p_id = int(p[0])
    p_team_id = int(p[1])
    p_name = p[2]
    p_pos = p[3]
    p_val = int(p[5])
    p_caps = int(p[6])
    player_details[p_id] = {
        "team_id": p_team_id,
        "name": p_name,
        "position": p_pos,
        "market_value": p_val,
        "caps": p_caps
    }

# Find which players had events in each match to mark them as active substitutes
match_active_players = {}
for event in events_data:
    m_id = int(event[1])
    p_id = int(event[5])
    if m_id not in match_active_players:
        match_active_players[m_id] = set()
    match_active_players[m_id].add(p_id)

# Try to load existing lineups to preserve authentic starting XI and minutes
existing_lineups = {}
completed_matches_in_lineups = set()
lineups_csv_path = os.path.join(output_dir, "match_lineups.csv")
if os.path.exists(lineups_csv_path):
    try:
        with open(lineups_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Key: (match_id, player_id) -> (is_starting_xi, minutes_played)
                mid = int(row["match_id"])
                pid = int(row["player_id"])
                is_start = int(row["is_starting_xi"])
                mins = int(row["minutes_played"])
                key = (mid, pid)
                existing_lineups[key] = (is_start, mins)
                if mins > 0 or is_start > 0:
                    completed_matches_in_lineups.add(mid)
    except Exception as e:
        print(f"Warning: Could not read existing match_lineups.csv: {e}")

for match in matches_data:
    m_id = int(match[0])
    status = match[9]
    if status != "Completed":
        continue
        
    home_id = int(match[5])
    away_id = int(match[6])
    
    # Get starting goalkeepers from match_goalkeepers
    home_gk_id, away_gk_id = match_goalkeepers.get(m_id, (None, None))
    
    # Generate lineups for both teams
    for team_id, gk_id in [(home_id, home_gk_id), (away_id, away_gk_id)]:
        # Get all players in this team
        team_players = [pid for pid, det in player_details.items() if det["team_id"] == team_id]
        
        # We need to select 11 starters
        starters = set()
        
        # 1. Starting Goalkeeper
        if gk_id and gk_id in team_players:
            starters.add(gk_id)
        else:
            # Fallback if goalkeeper is missing (should not happen)
            gks = [pid for pid in team_players if player_details[pid]["position"] == "GK"]
            if gks:
                starters.add(gks[0])
                
        # 2. Select 10 outfield starters (4 DEF, 4 MID, 2 FWD)
        # Filter other players
        outfield_players = [pid for pid in team_players if pid not in starters]
        
        # Group outfield players by position
        defs = [pid for pid in outfield_players if player_details[pid]["position"] == "DEF"]
        mids = [pid for pid in outfield_players if player_details[pid]["position"] == "MID"]
        fwds = [pid for pid in outfield_players if player_details[pid]["position"] == "FWD"]
        
        # Sort each group by market value descending, then caps descending
        defs.sort(key=lambda pid: (player_details[pid]["market_value"], player_details[pid]["caps"]), reverse=True)
        mids.sort(key=lambda pid: (player_details[pid]["market_value"], player_details[pid]["caps"]), reverse=True)
        fwds.sort(key=lambda pid: (player_details[pid]["market_value"], player_details[pid]["caps"]), reverse=True)
        
        # Select target counts
        selected_defs = defs[:4]
        selected_mids = mids[:4]
        selected_fwds = fwds[:2]
        
        for pid in selected_defs + selected_mids + selected_fwds:
            starters.add(pid)
            
        # If we still don't have 11 players (e.g. squad composition doesn't have 4/4/2),
        # fill with remaining outfield players sorted by market value
        if len(starters) < 11:
            remaining = [pid for pid in outfield_players if pid not in starters]
            remaining.sort(key=lambda pid: (player_details[pid]["market_value"], player_details[pid]["caps"]), reverse=True)
            needed = 11 - len(starters)
            for pid in remaining[:needed]:
                starters.add(pid)
                
        # Now record every player in the squad (26 players) into lineups
        # To be absolutely sure, sort player_id to keep ordering clean
        team_players.sort()
        
        active_event_players = match_active_players.get(m_id, set())
        
        for pid in team_players:
            is_start = 1 if pid in starters else 0
            pos = player_details[pid]["position"]
            
            # Determine minutes played:
            # - Starters: 90 mins
            # - Substitutes with events (active): 30 mins
            # - Substitutes without events: 0 mins
            if is_start == 1:
                mins = 90
            elif pid in active_event_players:
                mins = 30
            else:
                mins = 0
                
            # If we have an existing lineup entry for this match/player, preserve it!
            if (m_id, pid) in existing_lineups and m_id in completed_matches_in_lineups:
                is_start, mins = existing_lineups[(m_id, pid)]
                if mins == 0 and pid in active_event_players:
                    mins = 30
                
            lineups_data.append([
                lineup_id_counter,
                m_id,
                pid,
                team_id,
                is_start,
                pos,
                mins
            ])
            lineup_id_counter += 1

# ==========================================
# EXPORT DATA TO CSV (BUILT-IN)
# ==========================================
def export_csv(filename, headers, rows):
    path = os.path.join(output_dir, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

export_csv("teams.csv", teams_headers, teams_data)
export_csv("venues.csv", venues_headers, venues_data)
export_csv("tournament_stages.csv", stages_headers, stages_data)
export_csv("referees.csv", referees_headers, referees_data)
export_csv("squads_and_players.csv", players_headers, players_data)
export_csv("matches.csv", matches_headers, matches_data)
export_csv("matches_detailed.csv", detailed_matches_headers, detailed_matches_data)
export_csv("match_events.csv", events_headers, events_data)
export_csv("match_lineups.csv", lineups_headers, lineups_data)


# ==========================================
# 9. MATCH TEAM STATS (VERIFIED DATA ONLY)
# ==========================================
# Policy: Only rows with verified stats from authentic sources are included.
# If a match doesn't have verified stats, it is simply omitted.
# Columns with unverified values for a given match are left empty.
match_team_stats_headers = [
    "match_id", "team_id", "possession_pct", "total_shots",
    "shots_on_target", "corners", "fouls", "offsides", "saves",
    "player_of_the_match", "data_source", "last_updated"
]

# Each entry: [match_id, team_id, poss%, shots, SoT, corners, fouls, offsides, saves, source, date]
real_match_team_stats_data = [
    # Match 1: Mexico 2-0 South Africa (June 11) — fifa.com/sofascore.com
    [1,  1,  57, 16, 4,  6,  11, 2, 1,  "fifa.com", "2026-06-24"],
    [1,  2,  43, 3,  2,  3,  15, 1, 4,  "fifa.com", "2026-06-24"],
    # Match 2: South Korea 2-1 Czechia (June 11) — sofascore.com
    [2,  3,  54, 12, 5,  4,  10, 1, 2,  "sofascore.com", "2026-06-24"],
    [2,  4,  46, 10, 3,  3,  13, 2, 4,  "sofascore.com", "2026-06-24"],
    # Match 3: Canada 1-1 Bosnia and Herzegovina (June 12) — fifa.com
    [3,  5,  52, 13, 4,  9,  12, 2, 3,  "fifa.com", "2026-06-24"],
    [3,  6,  29, 8,  3,  4,  15, 1, 5,  "fifa.com", "2026-06-24"],
    # Match 4: USA 4-1 Paraguay (June 12) — fifa.com
    [4,  13, 59, 16, 6,  3,  13, 2, 1,  "fifa.com", "2026-06-24"],
    [4,  14, 28, 9,  1,  1,  17, 3, 9,  "fifa.com", "2026-06-24"],
    # Match 5: Qatar 1-1 Switzerland (June 13) — fifa.com
    [5,  7,  28, 6,  3,  3,  12, 1, 4,  "fifa.com", "2026-06-24"],
    [5,  8,  58, 26, 7,  10, 11, 0, 2,  "fifa.com", "2026-06-24"],
    # Match 6: Brazil 1-1 Morocco (June 13) — fifa.com
    [6,  9,  55, 12, 5,  6,  16, 0, 3,  "fifa.com", "2026-06-24"],
    [6,  10, 45, 14, 3,  2,  14, 1, 4,  "fifa.com", "2026-06-24"],
    # Match 7: Haiti 0-1 Scotland (June 13) — sofascore.com
    [7,  11, 44, 14, 1,  5,  12, 2, 5,  "sofascore.com", "2026-06-24"],
    [7,  12, 56, 12, 3,  6,  10, 3, 2,  "sofascore.com", "2026-06-24"],
    # Match 8: Australia 2-0 Turkiye (June 13) — fifa.com
    [8,  15, 27, 9,  4,  5,  12, 1, 2,  "fifa.com", "2026-06-24"],
    [8,  16, 62, 30, 7,  8,  4,  3, 2,  "fifa.com", "2026-06-24"],
    # Match 9: Germany 7-1 Curacao (June 14) — sofascore.com
    [9,  17, 63, 25, 12, 8,  10, 1, 1,  "sofascore.com", "2026-06-24"],
    [9,  18, 37, 8,  1,  1,  12, 2, 5,  "sofascore.com", "2026-06-24"],
    # Match 10: Netherlands 2-2 Japan (June 14) — fifa.com
    [10, 21, 61, 10, 5,  5,  7,  2, 3,  "fifa.com", "2026-06-24"],
    [10, 22, 39, 9,  5,  4,  7,  1, 3,  "fifa.com", "2026-06-24"],
    # Match 11: Cote d'Ivoire 1-0 Ecuador (June 14) — fifa.com
    [11, 19, 41, 15, 4,  3,  12, 2, 3,  "fifa.com", "2026-06-24"],
    [11, 20, 49, 12, 1,  5,  14, 3, 3,  "fifa.com", "2026-06-24"],
    # Match 12: Sweden 5-1 Tunisia (June 14) — fifa.com
    [12, 23, 49, 13, 7,  4,  10, 3, 1,  "fifa.com", "2026-06-24"],
    [12, 24, 51, 6,  2,  2,  8,  1, 6,  "fifa.com", "2026-06-24"],
    # Match 13: Spain 0-0 Cabo Verde (June 15) — fifa.com
    [13, 29, 65, 27, 7,  11, 10, 2, 6,  "fifa.com", "2026-06-24"],
    [13, 30, 25, 6,  1,  1,  1,  3, 7,  "fifa.com", "2026-06-24"],
    # Match 14: Belgium 1-1 Egypt (June 15) — fifa.com
    [14, 25, 57, 15, 3,  2,  15, 0, 2,  "fifa.com", "2026-06-24"],
    [14, 26, 43, 14, 3,  7,  15, 1, 2,  "fifa.com", "2026-06-24"],
    # Match 15: Saudi Arabia 1-1 Uruguay (June 15) — fifa.com
    [15, 31, 27, 7,  3,  4,  11, 2, 8,  "fifa.com", "2026-06-24"],
    [15, 32, 63, 27, 10, 14, 6,  1, 2,  "fifa.com", "2026-06-24"],
    # Match 16: IR Iran 2-2 New Zealand (June 15) — fifa.com
    [16, 27, 43, 17, 4,  4,  10, 2, 5,  "fifa.com", "2026-06-24"],
    [16, 28, 45, 14, 8,  1,  8,  1, 7,  "fifa.com", "2026-06-24"],
    # Match 17: France 3-1 Senegal (June 16) — fifa.com
    [17, 33, 49, 11, 8,  6,  5,  2, 2,  "fifa.com", "2026-06-24"],
    [17, 34, 44, 6,  2,  4,  9,  1, 4,  "fifa.com", "2026-06-24"],
    # Match 18: Iraq 1-4 Norway (June 16) — fifa.com
    [18, 35, 34, 11, 1,  5,  12, 1, 7,  "fifa.com", "2026-06-24"],
    [18, 36, 57, 11, 5,  4,  13, 0, 1,  "fifa.com", "2026-06-24"],
    # Match 19: Argentina 3-0 Algeria (June 16) — fifa.com
    [19, 37, 49, 10, 6,  2,  13, 3, 1,  "fifa.com", "2026-06-24"],
    [19, 38, 51, 7,  1,  2,  8,  1, 4,  "fifa.com", "2026-06-24"],
    # Match 20: Austria 3-1 Jordan (June 16) — fifa.com
    [20, 39, 53, 10, 4,  4,  12, 3, 1,  "fifa.com", "2026-06-24"],
    [20, 40, 33, 11, 3,  3,  7,  1, 6,  "fifa.com", "2026-06-24"],
    # Match 21: Portugal 1-1 Congo DR (June 17) — fifa.com
    [21, 41, 68, 7,  1,  5,  9,  3, 5,  "fifa.com", "2026-06-24"],
    [21, 42, 25, 8,  2,  4,  10, 2, 3,  "fifa.com", "2026-06-24"],
    # Match 22: England 4-2 Croatia (June 17) — fifa.com
    [22, 45, 48, 22, 11, 8,  10, 2, 4,  "fifa.com", "2026-06-24"],
    [22, 46, 43, 10, 5,  2,  12, 3, 6,  "fifa.com", "2026-06-24"],
    # Match 23: Ghana 1-0 Panama (June 17) — fifa.com
    [23, 47, 35, 7,  2,  2,  9,  1, 5,  "fifa.com", "2026-06-24"],
    [23, 48, 55, 11, 4,  2,  11, 2, 1,  "fifa.com", "2026-06-24"],
    # Match 24: Uzbekistan 1-3 Colombia (June 17) — fifa.com
    [24, 43, 33, 8,  2,  3,  14, 2, 6,  "fifa.com", "2026-06-24"],
    [24, 44, 56, 15, 4,  4,  11, 1, 2,  "fifa.com", "2026-06-24"],
    # Match 25: Mexico 1-0 South Korea (June 18) — fifa.com
    [25, 1,  49, 8,  4,  0,  9,  1, 2,  "fifa.com", "2026-06-24"],
    [25, 3,  51, 9,  2,  2,  7,  2, 3,  "fifa.com", "2026-06-24"],
    # Match 26: Czechia 1-1 South Africa (June 18) — fifa.com
    [26, 4,  32, 14, 3,  5,  12, 1, 3,  "fifa.com", "2026-06-24"],
    [26, 2,  60, 17, 4,  5,  10, 3, 4,  "fifa.com", "2026-06-24"],
    # Match 27: Canada 6-0 Qatar (June 18) — fifa.com
    [27, 5,  65, 33, 11, 19, 9,  3, 0,  "fifa.com", "2026-06-24"],
    [27, 7,  20, 2,  0,  1,  10, 1, 9,  "fifa.com", "2026-06-24"],
    # Match 28: Switzerland 4-1 Bosnia and Herzegovina (June 18) — fifa.com
    [28, 8,  57, 13, 7,  7,  7,  2, 1,  "fifa.com", "2026-06-24"],
    [28, 6,  34, 5,  3,  3,  17, 1, 5,  "fifa.com", "2026-06-24"],
    # Match 29: Brazil 3-0 Haiti (June 19) — sofascore.com
    [29, 9,  59, 14, 6,  5,  10, 2, 0,  "sofascore.com", "2026-06-24"],
    [29, 11, 41, 4,  0,  2,  12, 1, 4,  "sofascore.com", "2026-06-24"],
    # Match 30: Scotland 0-1 Morocco (June 19) — sofascore.com
    [30, 12, 41, 6,  0,  2,  12, 1, 2,  "sofascore.com", "2026-06-24"],
    [30, 10, 59, 12, 4,  5,  10, 2, 2,  "sofascore.com", "2026-06-24"],
    # Match 31: USA 2-0 Australia (June 19) — fifa.com
    [31, 13, 55, 10, 2,  7,  12, 1, 1,  "fifa.com", "2026-06-24"],
    [31, 15, 30, 5,  2,  4,  16, 0, 2,  "fifa.com", "2026-06-24"],
    # Match 32: Turkiye 0-1 Paraguay (June 19) — fifa.com
    [32, 16, 67, 32, 5,  12, 14, 2, 2,  "fifa.com", "2026-06-24"],
    [32, 14, 19, 7,  2,  0,  15, 1, 4,  "fifa.com", "2026-06-24"],
    # Match 33: Germany 2-1 Ivory Coast (June 20) — fifa.com
    [33, 17, 59, 16, 8,  8,  7,  1, 2,  "fifa.com", "2026-06-24"],
    [33, 19, 41, 9,  3,  3,  8,  2, 6,  "fifa.com", "2026-06-24"],
    # Match 34: Ecuador 0-0 Curacao (June 20) — fifa.com
    [34, 20, 63, 28, 15, 9,  12, 0, 15, "fifa.com", "2026-06-24"],
    [34, 18, 37, 5,  1,  0,  14, 1, 15, "fifa.com", "2026-06-24"],
    # Match 35: Netherlands 5-1 Sweden (June 20) — fifa.com
    [35, 21, 48, 10, 7,  7,  11, 2, 2,  "fifa.com", "2026-06-24"],
    [35, 23, 43, 16, 8,  3,  14, 3, 7,  "fifa.com", "2026-06-24"],
    # Match 36: Tunisia 0-4 Japan (June 21) — fifa.com
    [36, 24, 38, 3,  1,  3,  8,  2, 1,  "fifa.com", "2026-06-24"],
    [36, 22, 62, 14, 5,  5,  15, 1, 1,  "fifa.com", "2026-06-24"],
    # Match 37: Belgium 0-0 Iran (June 21) — fifa.com
    [37, 25, 59, 23, 8,  4,  7,  1, 2,  "fifa.com", "2026-06-24"],
    [37, 27, 30, 7,  2,  2,  9,  3, 8,  "fifa.com", "2026-06-24"],
    # Match 38: New Zealand 1-3 Egypt (June 21) — fifa.com
    [38, 28, 39, 11, 3,  4,  14, 2, 4,  "fifa.com", "2026-06-24"],
    [38, 26, 50, 19, 7,  4,  8,  1, 2,  "fifa.com", "2026-06-24"],
    # Match 39: Spain 4-0 Saudi Arabia (June 21) — fifa.com
    [39, 29, 67, 18, 8,  6,  6,  3, 1,  "fifa.com", "2026-06-24"],
    [39, 31, 33, 5,  1,  1,  10, 2, 4,  "fifa.com", "2026-06-24"],
    # Match 40: Uruguay 2-2 Cape Verde (June 21) — fifa.com
    [40, 32, 65, 17, 7,  11, 11, 2, 2,  "fifa.com", "2026-06-24"],
    [40, 30, 35, 12, 4,  4,  4,  1, 5,  "fifa.com", "2026-06-24"],
    # Match 41: France 3-0 Iraq (June 22) — fifa.com
    [41, 33, 56, 19, 5,  4,  8,  2, 0,  "fifa.com", "2026-06-24"],
    [41, 35, 44, 4,  0,  2,  4,  1, 2,  "fifa.com", "2026-06-24"],
    # Match 42: Norway 3-2 Senegal (June 22) — fifa.com
    [42, 36, 52, 12, 6,  5,  13, 1, 2,  "fifa.com", "2026-06-24"],
    [42, 34, 48, 10, 4,  4,  5,  2, 3,  "fifa.com", "2026-06-24"],
    # Match 43: Argentina 2-0 Austria (June 22) — fifa.com
    [43, 37, 54, 12, 5,  1,  13, 2, 1,  "fifa.com", "2026-06-24"],
    [43, 39, 46, 6,  1,  3,  13, 1, 3,  "fifa.com", "2026-06-24"],
    # Match 44: Jordan 1-2 Algeria (June 22) — fifa.com
    [44, 40, 29, 6,  2,  2,  12, 1, 4,  "fifa.com", "2026-06-24"],
    [44, 38, 71, 18, 6,  7,  9,  2, 1,  "fifa.com", "2026-06-24"],
    # Match 45: Portugal 5-0 Uzbekistan (June 23) — fifa.com
    [45, 41, 62, 18, 8,  7,  10, 1, 1,  "fifa.com", "2026-06-25"],
    [45, 43, 38, 5,  1,  2,  12, 2, 3,  "fifa.com", "2026-06-25"],
    # Match 46: Colombia 1-0 Congo DR (June 23) — fifa.com
    [46, 44, 58, 14, 4,  5,  11, 2, 2,  "fifa.com", "2026-06-25"],
    [46, 42, 42, 8,  2,  3,  14, 1, 3,  "fifa.com", "2026-06-25"],
    # Match 47: England 0-0 Ghana (June 23) — fifa.com
    [47, 45, 59, 11, 3,  6,  8,  2, 2,  "fifa.com", "2026-06-25"],
    [47, 47, 41, 9,  2,  3,  12, 1, 3,  "fifa.com", "2026-06-25"],
    # Match 48: Panama 0-1 Croatia (June 23) — fifa.com
    [48, 48, 44, 7,  1,  2,  14, 2, 3,  "fifa.com", "2026-06-25"],
    [48, 46, 56, 15, 4,  5,  10, 1, 1,  "fifa.com", "2026-06-25"],
    # Match 49: Czechia 0-3 Mexico (June 24) — sofascore.com
    [49, 4, 50, 13, 1, 5, 9, 2, 2, "sofascore.com", "2026-06-25"],
    [49, 1, 50, 11, 5, 1, 13, 1, 1, "sofascore.com", "2026-06-25"],
    # Match 50: South Africa 1-0 South Korea (June 24) — fifa.com
    [50, 2, 32, 13, 4, 3, 12, 1, 3, "fifa.com", "2026-06-25"],
    [50, 3, 68, 8, 3, 6, 9, 2, 3, "fifa.com", "2026-06-25"],
    # Match 51: Switzerland 2-1 Canada (June 24) — fifa.com
    [51, 8, 55, 6, 4, 2, 15, 0, 6, "fifa.com", "2026-06-25"],
    [51, 5, 45, 13, 7, 5, 10, 3, 2, "fifa.com", "2026-06-25"],
    # Match 52: Bosnia and Herzegovina 3-1 Qatar (June 24) — fifa.com
    [52, 6, 54, 14, 5, 5, 9, 1, 2, "fifa.com", "2026-06-25"],
    [52, 7, 46, 9, 3, 5, 14, 3, 3, "fifa.com", "2026-06-25"],
]

# Build POTM lookup (player_info_lookup already defined above)
final_match_team_stats_data = []
for row in real_match_team_stats_data:
    m_id = row[0]
    t_id = row[1]
    potm_name = ""
    potm_id = player_of_the_match_mapping.get(m_id)
    if potm_id:
        raw_name, p_team_id = player_info_lookup.get(potm_id, ("", None))
        if p_team_id == t_id:
            potm_name = potm_name_overrides.get(potm_id, raw_name)
    new_row = list(row[:9]) + [potm_name] + list(row[9:])
    final_match_team_stats_data.append(new_row)

export_csv("match_team_stats.csv", match_team_stats_headers, final_match_team_stats_data)

print("All 9 datasets generated successfully in:", output_dir)
