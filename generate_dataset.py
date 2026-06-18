import os
import csv
import random

# Set random seed for reproducibility
random.seed(42)

# Define directories
output_dir = "C:\\Users\\ASUS\\.gemini\\antigravity\\scratch\\fifa-wc2026-dataset"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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
players_headers = ["player_id", "team_id", "player_name", "position", "club_team", "market_value_eur", "caps"]
star_players = {
    "Argentina": [
        ("Lionel Messi", "FWD", "Inter Miami", 10000000, 185),
        ("Lautaro Martínez", "FWD", "Inter Milan", 80000000, 62),
        ("Alexis Mac Allister", "MID", "Liverpool", 70000000, 28),
        ("Enzo Fernández", "MID", "Chelsea", 75000000, 24),
        ("Emiliano Martínez", "GK", "Aston Villa", 28000000, 39)
    ],
    "France": [
        ("Kylian Mbappé", "FWD", "Real Madrid", 180000000, 80),
        ("Antoine Griezmann", "FWD", "Atlético Madrid", 25000000, 129),
        ("Aurélien Tchouaméni", "MID", "Real Madrid", 90000000, 34),
        ("William Saliba", "DEF", "Arsenal", 80000000, 17),
        ("Mike Maignan", "GK", "AC Milan", 38000000, 18)
    ],
    "England": [
        ("Harry Kane", "FWD", "Bayern Munich", 110000000, 93),
        ("Jude Bellingham", "MID", "Real Madrid", 180000000, 32),
        ("Bukayo Saka", "FWD", "Arsenal", 130000000, 36),
        ("Declan Rice", "MID", "Arsenal", 110000000, 52),
        ("Jordan Pickford", "GK", "Everton", 22000000, 64)
    ],
    "Brazil": [
        ("Vinícius Júnior", "FWD", "Real Madrid", 150000000, 28),
        ("Rodrygo", "FWD", "Real Madrid", 100000000, 24),
        ("Bruno Guimarães", "MID", "Newcastle United", 85000000, 22),
        ("Marquinhos", "DEF", "Paris Saint-Germain", 55000000, 84),
        ("Alisson Becker", "GK", "Liverpool", 28000000, 65)
    ],
    "USA": [
        ("Christian Pulisic", "FWD", "AC Milan", 35000000, 68),
        ("Weston McKennie", "MID", "Juventus", 25000000, 53),
        ("Folarin Balogun", "FWD", "Monaco", 30000000, 12),
        ("Antonee Robinson", "DEF", "Fulham", 20000000, 41),
        ("Matt Turner", "GK", "Crystal Palace", 7000000, 40)
    ]
}

positions = ["GK", "DEF", "MID", "FWD"]
first_names = ["Daniel", "David", "Lucas", "Mateo", "Alex", "John", "Carlos", "Thomas", "Andrej", "James", 
               "Mohammed", "Ali", "Hassan", "Youssef", "Luis", "Juan", "Diego", "Marcus", "Samuel", "Oliver"]
last_names = ["Smith", "Jones", "Garcia", "Martinez", "Rodriguez", "Silva", "Santos", "Müller", "Schmidt", 
              "Kovacic", "Horvat", "Abdel", "Ibrahim", "Nakamura", "Sato", "Kim", "Lee", "Park", "Onyango"]
clubs = ["Real Madrid", "Barcelona", "Manchester City", "Arsenal", "Liverpool", "Bayern Munich", 
         "Paris Saint-Germain", "Juventus", "AC Milan", "Inter Milan", "Ajax", "Benfica", "Porto", 
         "Galatasaray", "Boca Juniors", "Flamengo", "Al Hilal", "Los Angeles FC", "Club América", "Kaizer Chiefs"]

players_data = []
player_id_counter = 1

# Map to quickly lookup players per team later
team_player_map = {}

for team in teams_data:
    team_id = team[0]
    team_name = team[1]
    rank = team[5]
    
    team_stars = star_players.get(team_name, [])
    added_count = 0
    team_player_map[team_id] = []
    
    # Add star players
    for name, pos, club, val, caps in team_stars:
        player_row = [player_id_counter, team_id, name, pos, club, val, caps]
        players_data.append(player_row)
        team_player_map[team_id].append(player_id_counter)
        player_id_counter += 1
        added_count += 1
        
    # Generate generic players to complete 26-man squads
    needed = 26 - added_count
    for i in range(needed):
        # Determine position based on index (roughly: 3 GKs, 9 DEFs, 9 MIDs, 5 FWDs)
        if i < 3 - added_count if added_count < 3 else 0:
            pos = "GK"
        elif i < 11:
            pos = "DEF"
        elif i < 20:
            pos = "MID"
        else:
            pos = "FWD"
            
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # Scale value and caps relationally
        base_val = max(100000, int(150000000 / (rank ** 0.85)))
        val = int(random.uniform(0.4, 1.6) * base_val)
        caps = int(random.uniform(5, 95))
        club = random.choice(clubs)
        
        player_row = [player_id_counter, team_id, name, pos, club, val, caps]
        players_data.append(player_row)
        team_player_map[team_id].append(player_id_counter)
        player_id_counter += 1

# ==========================================
# 6. MATCHES DATA
# ==========================================
matches_headers = ["match_id", "date", "kickoff_time_utc", "stage_id", "venue_id", "home_team_id", "away_team_id", "home_score", "away_score", "status", "home_xg", "away_xg", "referee_id"]
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

    # Round 2 Scheduled matches
    [25, "2026-06-18", "15:00", 1, 9, 1, 3, "", "", "Scheduled", "", ""],
    [26, "2026-06-18", "18:00", 1, 3, 4, 2, "", "", "Scheduled", "", ""],
    [27, "2026-06-18", "21:00", 1, 5, 5, 7, "", "", "Scheduled", "", ""],
    [28, "2026-06-18", "23:59", 1, 1, 8, 6, "", "", "Scheduled", "", ""],
    [29, "2026-06-19", "15:00", 1, 2, 9, 11, "", "", "Scheduled", "", ""],
    [30, "2026-06-19", "18:00", 1, 4, 12, 10, "", "", "Scheduled", "", ""],
    [31, "2026-06-19", "21:00", 1, 6, 13, 15, "", "", "Scheduled", "", ""],
    [32, "2026-06-19", "23:59", 1, 8, 16, 14, "", "", "Scheduled", "", ""],
    [33, "2026-06-20", "15:00", 1, 10, 17, 19, "", "", "Scheduled", "", ""],
    [34, "2026-06-20", "18:00", 1, 12, 20, 18, "", "", "Scheduled", "", ""],
    [35, "2026-06-20", "21:00", 1, 14, 21, 23, "", "", "Scheduled", "", ""],
    [36, "2026-06-20", "23:59", 1, 16, 24, 22, "", "", "Scheduled", "", ""],
    [37, "2026-06-21", "15:00", 1, 11, 25, 27, "", "", "Scheduled", "", ""],
    [38, "2026-06-21", "18:00", 1, 13, 28, 26, "", "", "Scheduled", "", ""],
    [39, "2026-06-21", "21:00", 1, 15, 29, 31, "", "", "Scheduled", "", ""],
    [40, "2026-06-21", "23:59", 1, 2, 32, 30, "", "", "Scheduled", "", ""],
    [41, "2026-06-22", "15:00", 1, 4, 33, 35, "", "", "Scheduled", "", ""],
    [42, "2026-06-22", "18:00", 1, 6, 36, 34, "", "", "Scheduled", "", ""],
    [43, "2026-06-22", "21:00", 1, 8, 37, 39, "", "", "Scheduled", "", ""],
    [44, "2026-06-22", "23:59", 1, 10, 40, 38, "", "", "Scheduled", "", ""],
    [45, "2026-06-23", "15:00", 1, 12, 41, 43, "", "", "Scheduled", "", ""],
    [46, "2026-06-23", "18:00", 1, 14, 44, 42, "", "", "Scheduled", "", ""],
    [47, "2026-06-23", "21:00", 1, 16, 45, 47, "", "", "Scheduled", "", ""],
    [48, "2026-06-23", "23:59", 1, 1, 48, 46, "", "", "Scheduled", "", ""],

    # Round 3 Scheduled matches (simultaneous group final matches)
    [49, "2026-06-24", "18:00", 1, 1, 4, 1, "", "", "Scheduled", "", ""],
    [50, "2026-06-24", "18:00", 1, 7, 2, 3, "", "", "Scheduled", "", ""],
    [51, "2026-06-24", "22:00", 1, 5, 8, 5, "", "", "Scheduled", "", ""],
    [52, "2026-06-24", "22:00", 1, 6, 6, 7, "", "", "Scheduled", "", ""],
    [53, "2026-06-25", "18:00", 1, 2, 12, 9, "", "", "Scheduled", "", ""],
    [54, "2026-06-25", "18:00", 1, 10, 10, 11, "", "", "Scheduled", "", ""],
    [55, "2026-06-25", "22:00", 1, 3, 16, 13, "", "", "Scheduled", "", ""],
    [56, "2026-06-25", "22:00", 1, 15, 14, 15, "", "", "Scheduled", "", ""],
    [57, "2026-06-26", "18:00", 1, 9, 20, 17, "", "", "Scheduled", "", ""],
    [58, "2026-06-26", "18:00", 1, 11, 18, 19, "", "", "Scheduled", "", ""],
    [59, "2026-06-26", "22:00", 1, 12, 24, 21, "", "", "Scheduled", "", ""],
    [60, "2026-06-26", "22:00", 1, 16, 22, 23, "", "", "Scheduled", "", ""],
    [61, "2026-06-27", "18:00", 1, 4, 28, 25, "", "", "Scheduled", "", ""],
    [62, "2026-06-27", "18:00", 1, 8, 26, 27, "", "", "Scheduled", "", ""],
    [63, "2026-06-27", "22:00", 1, 13, 32, 29, "", "", "Scheduled", "", ""],
    [64, "2026-06-27", "22:00", 1, 14, 30, 31, "", "", "Scheduled", "", ""],
    [65, "2026-06-28", "18:00", 1, 10, 36, 33, "", "", "Scheduled", "", ""],
    [66, "2026-06-28", "18:00", 1, 2, 34, 35, "", "", "Scheduled", "", ""],
    [67, "2026-06-28", "22:00", 1, 15, 40, 37, "", "", "Scheduled", "", ""],
    [68, "2026-06-28", "22:00", 1, 3, 38, 39, "", "", "Scheduled", "", ""],
    [69, "2026-06-29", "18:00", 1, 12, 44, 41, "", "", "Scheduled", "", ""],
    [70, "2026-06-29", "18:00", 1, 9, 42, 43, "", "", "Scheduled", "", ""],
    [71, "2026-06-29", "22:00", 1, 16, 48, 45, "", "", "Scheduled", "", ""],
    [72, "2026-06-29", "22:00", 1, 11, 46, 47, "", "", "Scheduled", "", ""]
]

# Assign referees relationally
for idx, match in enumerate(matches_data):
    referee_id = (idx % 16) + 1
    match.append(referee_id)

# ==========================================
# 7. MATCH EVENTS DATA GENERATOR
# ==========================================
events_headers = ["event_id", "match_id", "minute", "event_type", "team_id", "player_id"]
events_data = []
event_id_counter = 1

for match in matches_data:
    status = match[9]
    if status != "Completed":
        continue
        
    match_id = match[0]
    home_id = match[5]
    away_id = match[6]
    home_score = match[7]
    away_score = match[8]
    
    home_players = team_player_map[home_id]
    away_players = team_player_map[away_id]
    
    # Home goals
    goal_minutes = sorted(random.sample(range(1, 91), home_score)) if home_score > 0 else []
    for m in goal_minutes:
        player_id = random.choice(home_players)
        events_data.append([event_id_counter, match_id, m, "Goal", home_id, player_id])
        event_id_counter += 1
        
    # Away goals
    goal_minutes_away = sorted(random.sample(range(1, 91), away_score)) if away_score > 0 else []
    for m in goal_minutes_away:
        player_id = random.choice(away_players)
        events_data.append([event_id_counter, match_id, m, "Goal", away_id, player_id])
        event_id_counter += 1
        
    # Cards
    num_yellows = random.randint(1, 5)
    for _ in range(num_yellows):
        team_id = random.choice([home_id, away_id])
        players = home_players if team_id == home_id else away_players
        player_id = random.choice(players)
        events_data.append([event_id_counter, match_id, random.randint(5, 90), "Yellow Card", team_id, player_id])
        event_id_counter += 1
        
    # Red cards (10% chance)
    if random.random() < 0.10:
        team_id = random.choice([home_id, away_id])
        players = home_players if team_id == home_id else away_players
        player_id = random.choice(players)
        events_data.append([event_id_counter, match_id, random.randint(45, 90), "Red Card", team_id, player_id])
        event_id_counter += 1

    # VAR Review (15% chance)
    if random.random() < 0.15:
        team_id = random.choice([home_id, away_id])
        players = home_players if team_id == home_id else away_players
        player_id = random.choice(players)
        events_data.append([event_id_counter, match_id, random.randint(10, 85), "VAR Review", team_id, player_id])
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

detailed_matches_headers = [
    "match_id", "date", "kickoff_time_utc", "stage_name", 
    "stadium_name", "city", "country", 
    "home_team_name", "home_fifa_code", 
    "away_team_name", "away_fifa_code", 
    "home_score", "away_score", "status", "home_xg", "away_xg", "referee_name"
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
    
    stg_name = stage_lookup.get(stg_id, "Unknown")
    stadium, city, country = venue_lookup.get(ven_id, ("Unknown", "Unknown", "Unknown"))
    home_name, home_code = team_lookup.get(h_id, ("Unknown", "UNK"))
    away_name, away_code = team_lookup.get(a_id, ("Unknown", "UNK"))
    ref_name = referee_lookup.get(ref_id, "Unknown")
    
    detailed_matches_data.append([
        m_id, date, time, stg_name,
        stadium, city, country,
        home_name, home_code,
        away_name, away_code,
        h_score, a_score, status, h_xg, a_xg, ref_name
    ])

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

print("All 8 datasets generated successfully in:", output_dir)
