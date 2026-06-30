import re
import csv
import os
import sys

workspace_dir = r"c:\Users\ASUS\.gemini\antigravity\scratch\fifa-wc2026-dataset"

# Load players
with open(os.path.join(workspace_dir, "squads_and_players.csv"), encoding="utf-8") as f:
    players = list(csv.DictReader(f))
player_map = {r["player_id"]: r for r in players}

# Map player name and team to ID
def normalize_name(name):
    import unicodedata
    name = name.replace("ø", "o").replace("Ø", "o").replace("æ", "ae").replace("Æ", "ae").replace("å", "a").replace("Å", "a").replace("ć", "c").replace("Ć", "c")
    n = unicodedata.normalize('NFKD', name)
    return "".join(c for c in n if not unicodedata.combining(c)).lower().strip()

player_by_team_name = {}
for p in players:
    tid = p["team_id"]
    pname = normalize_name(p["player_name"])
    player_by_team_name[(tid, pname)] = p["player_id"]
    parts = pname.split()
    if len(parts) > 1:
        player_by_team_name[(tid, parts[-1])] = p["player_id"]
        player_by_team_name[(tid, parts[0] + " " + parts[-1])] = p["player_id"]

# Load teams
with open(os.path.join(workspace_dir, "teams.csv"), encoding="utf-8") as f:
    teams = list(csv.DictReader(f))
team_id_to_name = {r["team_id"]: r["team_name"] for r in teams}
team_name_to_id = {r["team_name"].lower().strip(): r["team_id"] for r in teams}

team_aliases = {
    "south korea": "south korea",
    "korea republic": "south korea",
    "czech republic": "czechia",
    "united states": "usa",
    "turkey": "türkiye",
    "trkiye": "türkiye",
    "ivory coast": "cote d'ivoire",
    "côte d'ivoire": "cote d'ivoire",
    "cte d'ivoire": "cote d'ivoire",
    "iran": "ir iran",
    "ir iran": "ir iran",
    "cape verde": "cabo verde",
    "dr congo": "congo dr",
    "congo dr": "congo dr",
}

def get_team_id(name):
    name_clean = name.lower().strip()
    if name_clean in team_aliases:
        name_clean = team_aliases[name_clean]
    for t_name, t_id in team_name_to_id.items():
        t_norm = normalize_name(t_name)
        if name_clean == t_norm or name_clean == t_name.lower().strip():
            return t_id
    return None

def find_player_id(team_id, name):
    name_norm = normalize_name(name)
    if (team_id, name_norm) in player_by_team_name:
        return player_by_team_name[(team_id, name_norm)]
    for (tid, pname), pid in player_by_team_name.items():
        if tid != team_id:
            continue
        if name_norm in pname or pname in name_norm:
            return pid
    parts = name_norm.split()
    for (tid, pname), pid in player_by_team_name.items():
        if tid != team_id:
            continue
        if all(part in pname for part in parts if len(part) > 1):
            return pid
    return None

# match_id -> (home_gk_player_id, away_gk_player_id)
# Loaded dynamically from generate_dataset.py using regex
match_goalkeepers = {}
with open(os.path.join(workspace_dir, "generate_dataset.py"), encoding="utf-8") as f:
    gd_content = f.read()
    
# Extract match_goalkeepers dictionary
match_gk_block = re.search(r'match_goalkeepers = \{(.*?)\}', gd_content, re.DOTALL)
if match_gk_block:
    for line in match_gk_block.group(1).split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r'(\d+)\s*:\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', line)
        if m:
            mid = int(m.group(1))
            hgk = int(m.group(2))
            agk = int(m.group(3))
            match_goalkeepers[mid] = (hgk, agk)

print(f"Loaded {len(match_goalkeepers)} matches in match_goalkeepers mapping.")

# Match details map from matches.csv
with open(os.path.join(workspace_dir, "matches.csv"), encoding="utf-8") as f:
    matches = list(csv.DictReader(f))
matches_by_id = {int(m["match_id"]): m for m in matches}

def check_file(filename):
    with open(os.path.join(workspace_dir, filename), "r", encoding="utf-8") as f:
        text = f.read()
        
    pos = 0
    boxes = []
    patterns = [r'\{\{#invoke:[Ff]ootball box\|main', r'\{\{[Ff]ootballbox', r'\{\{[Ff]ootball box']
    
    while True:
        earliest_start = -1
        for pat in patterns:
            idx = re.search(pat, text[pos:])
            if idx:
                idx_pos = pos + idx.start()
                if earliest_start == -1 or idx_pos < earliest_start:
                    earliest_start = idx_pos
                    
        if earliest_start == -1:
            break
            
        brace_count = 0
        end_idx = earliest_start
        for i in range(earliest_start, len(text)):
            if text[i:i+2] == '{{':
                brace_count += 2
            elif text[i:i+2] == '}}':
                brace_count -= 2
                if brace_count == 0:
                    end_idx = i + 2
                    break
        boxes.append((text[earliest_start:end_idx], earliest_start, end_idx))
        pos = end_idx
        
    print(f"\nChecking {filename} (found {len(boxes)} boxes)...")
    for idx, (box, start, end) in enumerate(boxes):
        team1_match = re.search(r'\|\s*team1\s*=\s*([^\n]*)', box)
        team2_match = re.search(r'\|\s*team2\s*=\s*([^\n]*)', box)
        if not team1_match or not team2_match:
            continue
        team1_raw = team1_match.group(1).strip()
        team2_raw = team2_match.group(1).strip()
        
        # Clean team1 and team2
        # e.g., team1={{#invoke:flag|fb-rt|RSA}} -> RSA
        # team1={{flag|ENG}} -> ENG
        # team1=[[France national football team|France]] -> France
        def clean_team_name(raw):
            raw = raw.strip()
            # If there's a trailing | or closing brace that ends the parameter:
            # Let's search for patterns:
            # 1. {{#invoke:flag|fb-rt|XXX}} or {{#invoke:flag|fb|XXX}}
            m = re.search(r'fb-rt\|([A-Za-z0-9\s]+)', raw)
            if m:
                return m.group(1).strip()
            m = re.search(r'fb\|([A-Za-z0-9\s]+)', raw)
            if m:
                return m.group(1).strip()
            # 2. [[Team Name]] or [[Team Name|Team]]
            m = re.search(r'\[\[(?:[^\]|]+\|)?([^\]]+)\]\]', raw)
            if m:
                return m.group(1).strip()
            # 3. flagicon or flag template
            m = re.search(r'\{\{flag\|([A-Za-z0-9\s]+)\}\}', raw)
            if m:
                return m.group(1).strip()
            return raw
            
        t1_name = clean_team_name(team1_raw)
        t2_name = clean_team_name(team2_raw)
        
        # If t1_name has trailing closing brace or pipe, clean it
        t1_name = t1_name.split("}}")[0].split("|")[0].strip()
        t2_name = t2_name.split("}}")[0].split("|")[0].strip()
            
        home_id = get_team_id(t1_name)
        away_id = get_team_id(t2_name)
        
        found_match = None
        
        # Match using name lookups
        for m in matches:
            if m["status"] != "Completed":
                continue
            h_name_norm = normalize_name(team_id_to_name[m["home_team_id"]])
            a_name_norm = normalize_name(team_id_to_name[m["away_team_id"]])
            t1_norm = normalize_name(t1_name)
            t2_norm = normalize_name(t2_name)
            
            fifa_codes = {
                "rsa": "south africa", "can": "canada", "bih": "bosnia and herzegovina",
                "qat": "qatar", "sui": "switzerland", "bra": "brazil", "mar": "morocco",
                "hai": "haiti", "sco": "scotland", "usa": "usa", "tur": "turkiye",
                "ger": "germany", "civ": "cote d'ivoire", "ecu": "ecuador", "swe": "sweden",
                "tun": "tunisia", "jpn": "japan", "bel": "belgium", "egy": "egypt",
                "ksa": "saudi arabia", "uru": "uruguay", "irn": "ir iran", "nzl": "new zealand",
                "fra": "france", "sen": "senegal", "nor": "norway", "irq": "iraq",
                "alg": "algeria", "jor": "jordan", "arg": "argentina", "aut": "austria",
                "por": "portugal", "cod": "congo dr", "eng": "england", "cro": "croatia",
                "gha": "ghana", "pan": "panama", "uzb": "uzbekistan", "col": "colombia",
                "cpe": "cape verde", "cur": "curacao", "cze": "czechia", "par": "paraguay"
            }
            t1_lookup = fifa_codes.get(t1_norm, t1_norm)
            t2_lookup = fifa_codes.get(t2_norm, t2_norm)
            
            if (t1_lookup in h_name_norm or h_name_norm in t1_lookup) and (t2_lookup in a_name_norm or a_name_norm in t2_lookup):
                found_match = m
                break
                
        if not found_match:
            print(f"Box {idx+1}: Could not map teams '{t1_name}' vs '{t2_name}' to any completed match.")
            continue
            
        mid = int(found_match["match_id"])
        home_id = found_match["home_team_id"]
        away_id = found_match["away_team_id"]
        home_name = team_id_to_name[home_id]
        away_name = team_id_to_name[away_id]
        
        # Extract goalkeepers from the wikitext following the box
        next_box_pos = len(text)
        if idx + 1 < len(boxes):
            next_box_pos = boxes[idx+1][1]
            
        sub_text = text[end:next_box_pos]
        parts = sub_text.split('valign="top"')
        if len(parts) < 3:
            continue
            
        home_lineup_text = parts[1]
        away_lineup_text = parts[2]
        if len(parts) >= 4:
            away_lineup_text = parts[3]
            
        home_gk_match = re.search(r'GK\s*\|\|.*?\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', home_lineup_text)
        away_gk_match = re.search(r'GK\s*\|\|.*?\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', away_lineup_text)
        
        home_gk_name = home_gk_match.group(1).strip() if home_gk_match else None
        away_gk_name = away_gk_match.group(1).strip() if away_gk_match else None
        
        if not home_gk_name or not away_gk_name:
            continue
            
        home_gk_pid = find_player_id(home_id, home_gk_name)
        away_gk_pid = find_player_id(away_id, away_gk_name)
        
        expected_gks = match_goalkeepers.get(mid)
        if not expected_gks:
            print(f"Match {mid} ({home_name} vs {away_name}): No goalkeepers in match_goalkeepers mapping!")
            continue
            
        exp_home_gk, exp_away_gk = expected_gks
        
        discrepancy = False
        if str(exp_home_gk) != str(home_gk_pid):
            print(f"  [GK DISCREPANCY] Match {mid} ({home_name}): CSV GK ID={exp_home_gk} ({player_map.get(str(exp_home_gk), {}).get('player_name')}), Wiki GK ID={home_gk_pid} ({home_gk_name})")
            discrepancy = True
        if str(exp_away_gk) != str(away_gk_pid):
            print(f"  [GK DISCREPANCY] Match {mid} ({away_name}): CSV GK ID={exp_away_gk} ({player_map.get(str(exp_away_gk), {}).get('player_name')}), Wiki GK ID={away_gk_pid} ({away_gk_name})")
            discrepancy = True
            
        if not discrepancy:
            print(f"  [OK] Match {mid} ({home_name} vs {away_name}) goalkeepers match.")

for fn in ['group_j_raw.txt', 'group_k_raw.txt', 'group_l_raw.txt', 'round_of_32_raw.txt']:
    if os.path.exists(os.path.join(workspace_dir, fn)):
        check_file(fn)
