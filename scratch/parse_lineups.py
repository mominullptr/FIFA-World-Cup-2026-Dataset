import json
import os

workspace_dir = os.path.dirname(os.path.abspath(__file__))
overrides_path = os.path.join(workspace_dir, "lineup_event_overrides.json")

with open(overrides_path, "r", encoding="utf-8") as f:
    overrides = json.load(f)

# Match 74: Brazil vs Japan (2-1)
overrides["74"] = {
  "home_team_id": 9,
  "away_team_id": 22,
  "home_lineup": [
    {"player_id": 209, "player_name": "Ramsés Alisson", "is_starting_xi": 1, "position": "GK", "minutes_played": 90, "cards": []},
    {"player_id": 221, "player_name": "Luiz Danilo", "is_starting_xi": 1, "position": "RB", "minutes_played": 90, "cards": [["Yellow Card", 48]]},
    {"player_id": 212, "player_name": "MARQUINHOSMarcos", "is_starting_xi": 1, "position": "CB", "minutes_played": 90, "cards": []},
    {"player_id": 211, "player_name": "Gabriel Gabriel Magalhaes", "is_starting_xi": 1, "position": "CB", "minutes_played": 90, "cards": []},
    {"player_id": 224, "player_name": "Douglas Douglas Santos", "is_starting_xi": 1, "position": "LB", "minutes_played": 90, "cards": []},
    {"player_id": 213, "player_name": "Henrique", "is_starting_xi": 1, "position": "DM", "minutes_played": 90, "cards": [["Yellow Card", 14]]},
    {"player_id": 216, "player_name": "GUIMARAESBruno Bruno", "is_starting_xi": 1, "position": "CM", "minutes_played": 90, "cards": [["Yellow Card", 90]]},  # Booked in 90+7' (represented as 90)
    {"player_id": 228, "player_name": "Lucas Lucas Paqueta", "is_starting_xi": 1, "position": "CM", "minutes_played": 46, "cards": []},
    {"player_id": 234, "player_name": "Vitor Rayan", "is_starting_xi": 1, "position": "RF", "minutes_played": 90, "cards": []},
    {"player_id": 217, "player_name": "Matheus Matheus Cunha", "is_starting_xi": 1, "position": "CF", "minutes_played": 66, "cards": []},
    {"player_id": 215, "player_name": "José Vinicius", "is_starting_xi": 1, "position": "LF", "minutes_played": 90, "cards": []},
    {"player_id": 227, "player_name": "Felipe Endrick", "is_starting_xi": 0, "position": "FW", "minutes_played": 44, "cards": []},
    {"player_id": 230, "player_name": "MARTINELLIGabriel Gabriel", "is_starting_xi": 0, "position": "FW", "minutes_played": 24, "cards": []},
    {"player_id": 225, "player_name": "Henrique Fabinho", "is_starting_xi": 0, "position": "MF", "minutes_played": 1, "cards": []},
    {"player_id": 226, "player_name": "Danilo Danilo Santos", "is_starting_xi": 0, "position": "MF", "minutes_played": 1, "cards": []}
  ],
  "away_lineup": [
    {"player_id": 547, "player_name": "Zion Suzuki", "is_starting_xi": 1, "position": "GK", "minutes_played": 90, "cards": []},
    {"player_id": 568, "player_name": "Takehiro Tomiyasu", "is_starting_xi": 1, "position": "CB", "minutes_played": 90, "cards": []},
    {"player_id": 549, "player_name": "Shogo Taniguchi", "is_starting_xi": 1, "position": "CB", "minutes_played": 90, "cards": []},
    {"player_id": 567, "player_name": "Hiroki Ito", "is_starting_xi": 1, "position": "CB", "minutes_played": 90, "cards": []},
    {"player_id": 556, "player_name": "Ritsu Doan", "is_starting_xi": 1, "position": "RM", "minutes_played": 66, "cards": []},
    {"player_id": 570, "player_name": "Kaishu Sano", "is_starting_xi": 1, "position": "CM", "minutes_played": 90, "cards": [["Yellow Card", 12]]},
    {"player_id": 561, "player_name": "Daichi Kamada", "is_starting_xi": 1, "position": "CM", "minutes_played": 78, "cards": [["Yellow Card", 45]]},
    {"player_id": 559, "player_name": "Keito Nakamura", "is_starting_xi": 1, "position": "LM", "minutes_played": 66, "cards": []},
    {"player_id": 560, "player_name": "Junya Ito", "is_starting_xi": 1, "position": "RF", "minutes_played": 78, "cards": []},
    {"player_id": 564, "player_name": "Ayase Ueda", "is_starting_xi": 1, "position": "CF", "minutes_played": 90, "cards": []},
    {"player_id": 557, "player_name": "Daizen Maeda", "is_starting_xi": 1, "position": "LF", "minutes_played": 90, "cards": []},  # Subbed off at 90+7'
    {"player_id": 571, "player_name": "Junnosuke Suzuki", "is_starting_xi": 0, "position": "DF", "minutes_played": 24, "cards": [["Yellow Card", 84]]},
    {"player_id": 548, "player_name": "Yukinari Sugawara", "is_starting_xi": 0, "position": "DF", "minutes_played": 24, "cards": []},
    {"player_id": 553, "player_name": "Ao Tanaka", "is_starting_xi": 0, "position": "MF", "minutes_played": 12, "cards": []},
    {"player_id": 552, "player_name": "Shuto Machino", "is_starting_xi": 0, "position": "FW", "minutes_played": 12, "cards": []},
    {"player_id": 565, "player_name": "Koki Ogawa", "is_starting_xi": 0, "position": "FW", "minutes_played": 1, "cards": []}
  ]
}

# Match 75: Germany vs Paraguay (1-1, aet 1-1, penalties 3-4)
overrides["75"] = {
  "home_team_id": 17,
  "away_team_id": 14,
  "home_lineup": [
    {"player_id": 417, "player_name": "Manuel Peter Neuer", "is_starting_xi": 1, "position": "GK", "minutes_played": 120, "cards": []},
    {"player_id": 422, "player_name": "Joshua Walter Kimmich", "is_starting_xi": 1, "position": "RB", "minutes_played": 120, "cards": []},
    {"player_id": 420, "player_name": "Jonathan Glao Tah", "is_starting_xi": 1, "position": "CB", "minutes_played": 120, "cards": []},
    {"player_id": 418, "player_name": "Antonio Ruediger", "is_starting_xi": 1, "position": "CB", "minutes_played": 110, "cards": [["Yellow Card", 110]]},
    {"player_id": 434, "player_name": "Nathaniel Christopher Brown", "is_starting_xi": 1, "position": "LB", "minutes_played": 120, "cards": []},
    {"player_id": 439, "player_name": "Felix Kalu Nmecha", "is_starting_xi": 1, "position": "CM", "minutes_played": 46, "cards": []},
    {"player_id": 421, "player_name": "Aleksandar Pavlovic", "is_starting_xi": 1, "position": "CM", "minutes_played": 79, "cards": []},
    {"player_id": 435, "player_name": "Leroy Aziz Sane", "is_starting_xi": 1, "position": "RW", "minutes_played": 88, "cards": []},
    {"player_id": 423, "player_name": "Kai Lukas Havertz", "is_starting_xi": 1, "position": "AM", "minutes_played": 120, "cards": [["Yellow Card", 106]]},
    {"player_id": 433, "player_name": "Florian Richard Wirtz", "is_starting_xi": 1, "position": "LW", "minutes_played": 110, "cards": []},
    {"player_id": 442, "player_name": "Deniz Undav", "is_starting_xi": 1, "position": "CF", "minutes_played": 63, "cards": []},
    {"player_id": 424, "player_name": "Leon Christoph Goretzka", "is_starting_xi": 0, "position": "MF", "minutes_played": 74, "cards": []},
    {"player_id": 426, "player_name": "Jamal Musiala", "is_starting_xi": 0, "position": "MF", "minutes_played": 57, "cards": [["Yellow Card", 115]]},
    {"player_id": 419, "player_name": "Waldemar Anton", "is_starting_xi": 0, "position": "DF", "minutes_played": 41, "cards": []},
    {"player_id": 427, "player_name": "Nick Woltemade", "is_starting_xi": 0, "position": "FW", "minutes_played": 32, "cards": []},
    {"player_id": 436, "player_name": "Nadiem Amiri", "is_starting_xi": 0, "position": "MF", "minutes_played": 10, "cards": []},
    {"player_id": 440, "player_name": "Malick Thiaw", "is_starting_xi": 0, "position": "DF", "minutes_played": 10, "cards": []}
  ],
  "away_lineup": [
    {"player_id": 350, "player_name": "Orlando Daniel Gill", "is_starting_xi": 1, "position": "GK", "minutes_played": 120, "cards": []},
    {"player_id": 342, "player_name": "Juan Jose Caceres", "is_starting_xi": 1, "position": "RB", "minutes_played": 99, "cards": []},
    {"player_id": 353, "player_name": "Gustavo Raul Gomez", "is_starting_xi": 1, "position": "CB", "minutes_played": 120, "cards": []},
    {"player_id": 351, "player_name": "Jose Maria Canale", "is_starting_xi": 1, "position": "CB", "minutes_played": 120, "cards": []},
    {"player_id": 344, "player_name": "Júnior Osmar Ignacio Alonso", "is_starting_xi": 1, "position": "LB", "minutes_played": 120, "cards": [["Yellow Card", 120]]},  # 120+2' represented as 120
    {"player_id": 348, "player_name": "Miguel Angel Almiron", "is_starting_xi": 1, "position": "RM", "minutes_played": 91, "cards": []},
    {"player_id": 354, "player_name": "Damián Josue Bobadilla", "is_starting_xi": 1, "position": "CM", "minutes_played": 99, "cards": []},
    {"player_id": 352, "player_name": "Adrián Andrés Cubas", "is_starting_xi": 1, "position": "CM", "minutes_played": 120, "cards": [["Yellow Card", 65]]},
    {"player_id": 361, "player_name": "Matias Galarza", "is_starting_xi": 1, "position": "LM", "minutes_played": 120, "cards": [["Yellow Card", 117]]},
    {"player_id": 359, "player_name": "Gabriel Avalos", "is_starting_xi": 1, "position": "CF", "minutes_played": 55, "cards": []},
    {"player_id": 357, "player_name": "Julio Cesar Enciso", "is_starting_xi": 1, "position": "CF", "minutes_played": 57, "cards": []},
    {"player_id": 362, "player_name": "Gustavo Ruben Caballero", "is_starting_xi": 0, "position": "MF", "minutes_played": 65, "cards": []},
    {"player_id": 349, "player_name": "Mauricio Mauricio", "is_starting_xi": 0, "position": "MF", "minutes_played": 63, "cards": []},
    {"player_id": 340, "player_name": "Victor Gustavo Velazquez", "is_starting_xi": 0, "position": "DF", "minutes_played": 29, "cards": []},
    {"player_id": 347, "player_name": "Arnaldo Antonio Sanabria", "is_starting_xi": 0, "position": "FW", "minutes_played": 21, "cards": []},
    {"player_id": 358, "player_name": "Braian Oscar Ojeda", "is_starting_xi": 0, "position": "MF", "minutes_played": 21, "cards": []},
    {"player_id": 343, "player_name": "Fabián Cornelio Balbuena", "is_starting_xi": 0, "position": "DF", "minutes_played": 1, "cards": []}  # 120+2' sub
  ]
}

# Match 76: Netherlands vs Morocco (1-1, aet 1-1, penalties 2-3)
overrides["76"] = {
  "home_team_id": 21,
  "away_team_id": 10,
  "home_lineup": [
    {"player_id": 521, "player_name": "Bart Verbruggen", "is_starting_xi": 1, "position": "GK", "minutes_played": 120, "cards": []},
    {"player_id": 526, "player_name": "Paul Jan-Paul Van Hecke", "is_starting_xi": 1, "position": "CB", "minutes_played": 120, "cards": []},
    {"player_id": 524, "player_name": "Virgil Van Dijk", "is_starting_xi": 1, "position": "CB", "minutes_played": 120, "cards": []},
    {"player_id": 525, "player_name": "Nathan Benjamin Ake", "is_starting_xi": 1, "position": "CB", "minutes_played": 71, "cards": [["Yellow Card", 71]]},
    {"player_id": 542, "player_name": "Denzel Justus Morris Dumfries", "is_starting_xi": 1, "position": "RM", "minutes_played": 120, "cards": []},
    {"player_id": 528, "player_name": "Ryan Jiro Gravenberch", "is_starting_xi": 1, "position": "CM", "minutes_played": 86, "cards": []},
    {"player_id": 541, "player_name": "Frenkie De Jong", "is_starting_xi": 1, "position": "CM", "minutes_played": 110, "cards": []},
    {"player_id": 535, "player_name": "Micky Van De Ven", "is_starting_xi": 1, "position": "LM", "minutes_played": 86, "cards": []},
    {"player_id": 544, "player_name": "Crysencio Jilbert Sylverio Cir Summerville", "is_starting_xi": 1, "position": "RF", "minutes_played": 120, "cards": []},
    {"player_id": 539, "player_name": "Brian Ebenezer Adjei Brobbey", "is_starting_xi": 1, "position": "CF", "minutes_played": 71, "cards": []},
    {"player_id": 531, "player_name": "Cody Mathés Gakpo", "is_starting_xi": 1, "position": "LF", "minutes_played": 113, "cards": []},
    {"player_id": 540, "player_name": "Teun Koopmeiners", "is_starting_xi": 0, "position": "MF", "minutes_played": 49, "cards": []},
    {"player_id": 529, "player_name": "Wout François Maria Weghorst", "is_starting_xi": 0, "position": "FW", "minutes_played": 49, "cards": []},
    {"player_id": 546, "player_name": "Quinten Ryan Crispito Timber", "is_starting_xi": 0, "position": "MF", "minutes_played": 34, "cards": []},
    {"player_id": 545, "player_name": "Jorrel Evan Hato", "is_starting_xi": 0, "position": "DF", "minutes_played": 34, "cards": []},
    {"player_id": 523, "player_name": "Marten Elco De Roon", "is_starting_xi": 0, "position": "MF", "minutes_played": 10, "cards": []},
    {"player_id": 527, "player_name": "Justin Dean Kluivert", "is_starting_xi": 0, "position": "MF", "minutes_played": 7, "cards": []}
  ],
  "away_lineup": [
    {"player_id": 235, "player_name": "Yassine Bounou", "is_starting_xi": 1, "position": "GK", "minutes_played": 120, "cards": []},
    {"player_id": 236, "player_name": "Achraf Hakimi", "is_starting_xi": 1, "position": "RB", "minutes_played": 120, "cards": []},
    {"player_id": 248, "player_name": "Issa Laye Lucas Jean Diop", "is_starting_xi": 1, "position": "CB", "minutes_played": 120, "cards": [["Yellow Card", 47]]},
    {"player_id": 252, "player_name": "Chadi Riad", "is_starting_xi": 1, "position": "CB", "minutes_played": 75, "cards": []},
    {"player_id": 237, "player_name": "Noussair Mazraoui", "is_starting_xi": 1, "position": "LB", "minutes_played": 120, "cards": []},
    {"player_id": 240, "player_name": "Ayyoub Bouaddi", "is_starting_xi": 1, "position": "CM", "minutes_played": 79, "cards": []},
    {"player_id": 258, "player_name": "Neil Yoni El Aynaoui", "is_starting_xi": 1, "position": "CM", "minutes_played": 120, "cards": []},
    {"player_id": 244, "player_name": "Brahim Diaz", "is_starting_xi": 1, "position": "RW", "minutes_played": 79, "cards": []},
    {"player_id": 242, "player_name": "Azz-Eddine Ounahi", "is_starting_xi": 1, "position": "AM", "minutes_played": 86, "cards": []},
    {"player_id": 257, "player_name": "Bilal El Khannouss", "is_starting_xi": 1, "position": "LW", "minutes_played": 86, "cards": []},
    {"player_id": 245, "player_name": "Ismael Saibari", "is_starting_xi": 1, "position": "CF", "minutes_played": 120, "cards": []},
    {"player_id": 260, "player_name": "Anass Salah Eddine", "is_starting_xi": 0, "position": "DF", "minutes_played": 45, "cards": []},
    {"player_id": 249, "player_name": "Samir El Mourabet", "is_starting_xi": 0, "position": "MF", "minutes_played": 41, "cards": []},
    {"player_id": 250, "player_name": "Gessime Ben Youssef Mustapha Yassine", "is_starting_xi": 0, "position": "MF", "minutes_played": 41, "cards": []},
    {"player_id": 243, "player_name": "Soufiane Rahimi", "is_starting_xi": 0, "position": "FW", "minutes_played": 34, "cards": []},
    {"player_id": 241, "player_name": "Chemsdine Talbi", "is_starting_xi": 0, "position": "MF", "minutes_played": 34, "cards": []}
  ]
}

with open(overrides_path, "w", encoding="utf-8") as f:
    json.dump(overrides, f, indent=2, ensure_ascii=False)

print("Successfully updated lineup_event_overrides.json with matches 74, 75, and 76!")
