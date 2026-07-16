import os
import csv
import math
import json

# Get current workspace directory
workspace_dir = os.path.dirname(os.path.abspath(__file__))

def safe_float(val, default=0.0):
    if not val or val.strip() == "":
        return default
    try:
        return float(val)
    except ValueError:
        return default

def safe_int(val, default=0):
    if not val or val.strip() == "":
        return default
    try:
        return int(val)
    except ValueError:
        return default

def train_poisson(X, y, epochs=2000, lr=0.05, l2=0.05):
    n_features = len(X[0])
    w = [0.0] * n_features
    # Standardize/initialize
    w[0] = math.log(sum(y) / len(y)) if sum(y) > 0 else 0.0
    
    for epoch in range(epochs):
        grad = [0.0] * n_features
        for i in range(len(X)):
            x_i = X[i]
            y_i = y[i]
            dot = sum(w[k] * x_i[k] for k in range(n_features))
            pred = math.exp(dot)
            # Clip prediction to avoid overflows
            pred = min(max(pred, 1e-5), 20.0)
            error = pred - y_i
            for k in range(n_features):
                grad[k] += error * x_i[k]
        
        # Gradient descent update with L2 regularization
        for k in range(n_features):
            w[k] -= lr * (grad[k] / len(X) + l2 * w[k])
            
    return w

def train_linear(X, y, epochs=2000, lr=0.05, l2=0.05):
    n_features = len(X[0])
    w = [0.0] * n_features
    w[0] = sum(y) / len(y) if len(y) > 0 else 0.0
    
    for epoch in range(epochs):
        grad = [0.0] * n_features
        for i in range(len(X)):
            x_i = X[i]
            y_i = y[i]
            pred = sum(w[k] * x_i[k] for k in range(n_features))
            error = pred - y_i
            for k in range(n_features):
                grad[k] += error * x_i[k]
                
        for k in range(n_features):
            w[k] -= lr * (grad[k] / len(X) + l2 * w[k])
            
    return w

def build_features(row, is_home):
    # Retrieve base data
    h_elo = safe_float(row['home_elo'])
    a_elo = safe_float(row['away_elo'])
    h_rank = safe_float(row['home_fifa_rank'])
    a_rank = safe_float(row['away_fifa_rank'])
    h_val = safe_float(row['home_squad_total_value_eur'])
    a_val = safe_float(row['away_squad_total_value_eur'])
    
    h_form_goals = safe_float(row['home_prev_avg_goals_scored'])
    h_form_conceded = safe_float(row['home_prev_avg_goals_conceded'])
    a_form_goals = safe_float(row['away_prev_avg_goals_scored'])
    a_form_conceded = safe_float(row['away_prev_avg_goals_conceded'])
    
    h_form_xg = safe_float(row['home_prev_avg_xg_scored'])
    h_form_xg_conceded = safe_float(row['home_prev_avg_xg_conceded'])
    a_form_xg = safe_float(row['away_prev_avg_xg_scored'])
    a_form_xg_conceded = safe_float(row['away_prev_avg_xg_conceded'])
    
    # Calculate features symmetric to home or away perspective
    if is_home:
        elo_diff = (h_elo - a_elo) / 100.0
        rank_diff = (a_rank - h_rank) / 10.0 # positive if home is better (lower rank)
        val_ratio = math.log(max(h_val, 1.0) / max(a_val, 1.0))
        goals_diff = h_form_goals - a_form_conceded
        xg_diff = h_form_xg - a_form_xg_conceded
    else:
        elo_diff = (a_elo - h_elo) / 100.0
        rank_diff = (h_rank - a_rank) / 10.0
        val_ratio = math.log(max(a_val, 1.0) / max(h_val, 1.0))
        goals_diff = a_form_goals - h_form_conceded
        xg_diff = a_form_xg - h_form_xg_conceded
        
    return [1.0, elo_diff, rank_diff, val_ratio, goals_diff, xg_diff]

def poisson_prob(k, lam):
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return (math.exp(-lam) * (lam**k)) / math.factorial(k)

def main():
    features_csv_path = os.path.join(workspace_dir, "match_prediction_features.csv")
    if not os.path.exists(features_csv_path):
        print(f"Error: {features_csv_path} does not exist.")
        return

    with open(features_csv_path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    # Split into completed training matches (match_id <= 102) and scheduled matches (103, 104)
    train_rows = []
    predict_rows = []
    for r in reader:
        mid = safe_int(r['match_id'])
        if mid <= 102:
            train_rows.append(r)
        elif mid in [103, 104]:
            predict_rows.append(r)

    print(f"Loaded {len(train_rows)} completed matches for training.")
    print(f"Loaded {len(predict_rows)} scheduled matches for prediction.")

    # Build Training Sets
    # We double the training size by treating each match from both Home and Away perspectives
    X_goals = []
    y_goals = []
    X_xg = []
    y_xg = []

    for r in train_rows:
        h_score = safe_int(r['home_score'])
        a_score = safe_int(r['away_score'])
        h_xg_val = safe_float(r['home_xg'])
        a_xg_val = safe_float(r['away_xg'])

        # Home perspective
        X_goals.append(build_features(r, is_home=True))
        y_goals.append(h_score)
        X_xg.append(build_features(r, is_home=True))
        y_xg.append(h_xg_val)

        # Away perspective
        X_goals.append(build_features(r, is_home=False))
        y_goals.append(a_score)
        X_xg.append(build_features(r, is_home=False))
        y_xg.append(a_xg_val)

    # Train Models
    print("Training Poisson Regression for Goals Scored...")
    w_goals = train_poisson(X_goals, y_goals)
    print(f"Goals Model Coefficients: Intercept: {w_goals[0]:.4f}, Elo Diff: {w_goals[1]:.4f}, Rank Diff: {w_goals[2]:.4f}, Val Ratio: {w_goals[3]:.4f}, Form Goals: {w_goals[4]:.4f}, Form xG: {w_goals[5]:.4f}")

    print("Training Linear Ridge Regression for Expected Goals (xG)...")
    w_xg = train_linear(X_xg, y_xg)
    print(f"xG Model Coefficients: Intercept: {w_xg[0]:.4f}, Elo Diff: {w_xg[1]:.4f}, Rank Diff: {w_xg[2]:.4f}, Val Ratio: {w_xg[3]:.4f}, Form Goals: {w_xg[4]:.4f}, Form xG: {w_xg[5]:.4f}")

    # Generate predictions for semi-finals
    predictions = {}
    for r in predict_rows:
        mid = safe_int(r['match_id'])
        h_name = r['home_team_name']
        a_name = r['away_team_name']

        # Get features
        x_home = build_features(r, is_home=True)
        x_away = build_features(r, is_home=False)

        # Predict expected goals (lambda)
        lambda_h = math.exp(sum(w_goals[k] * x_home[k] for k in range(len(w_goals))))
        lambda_a = math.exp(sum(w_goals[k] * x_away[k] for k in range(len(w_goals))))

        # Predict xG
        pred_xg_h = max(0.0, sum(w_xg[k] * x_home[k] for k in range(len(w_xg))))
        pred_xg_a = max(0.0, sum(w_xg[k] * x_away[k] for k in range(len(w_xg))))

        # Compute match outcome probabilities (H, D, A)
        prob_h = 0.0
        prob_d = 0.0
        prob_a = 0.0
        score_probs = []

        for h in range(11):
            p_h = poisson_prob(h, lambda_h)
            for a in range(11):
                p_a = poisson_prob(a, lambda_a)
                p_score = p_h * p_a
                
                if h > a:
                    prob_h += p_score
                elif h == a:
                    prob_d += p_score
                else:
                    prob_a += p_score
                
                score_probs.append((f"{h}-{a}", p_score))

        # Normalize score probabilities just in case
        total_p = sum(p for s, p in score_probs)
        prob_h /= total_p
        prob_d /= total_p
        prob_a /= total_p
        score_probs = [(s, p / total_p) for s, p in score_probs]

        # Get top 5 scorelines
        score_probs.sort(key=lambda item: item[1], reverse=True)
        top_scores = [{"score": s, "prob": round(p, 4)} for s, p in score_probs[:5]]

        # Predicted exact score is the most likely scoreline
        pred_score_str = top_scores[0]["score"]
        pred_score_h, pred_score_a = map(int, pred_score_str.split('-'))

        # Advancing probability (including extra-time/penalties simulation based on ELO)
        # Log-odds probability of home team winning a tiebreaker
        h_elo = safe_float(r['home_elo'])
        a_elo = safe_float(r['away_elo'])
        elo_diff = h_elo - a_elo
        prob_tiebreaker_h = 1.0 / (1.0 + math.exp(-0.002 * elo_diff))
        
        adv_prob_h = prob_h + prob_d * prob_tiebreaker_h
        adv_prob_a = 1.0 - adv_prob_h

        advancing_team = h_name if adv_prob_h >= 0.5 else a_name

        predictions[f"match_{mid}"] = {
            "match_id": mid,
            "date": r['date'],
            "kickoff_time_utc": r['kickoff_time_utc'],
            "venue": r['stadium_name'] + ", " + r['venue_city'],
            "referee": r['referee_name'],
            "home_team": h_name,
            "away_team": a_name,
            "home_fifa_code": r['home_fifa_code'],
            "away_fifa_code": r['away_fifa_code'],
            "home_elo": h_elo,
            "away_elo": a_elo,
            "home_fifa_rank": safe_int(r['home_fifa_rank']),
            "away_fifa_rank": safe_int(r['away_fifa_rank']),
            "home_prob": round(prob_h, 4),
            "draw_prob": round(prob_d, 4),
            "away_prob": round(prob_a, 4),
            "home_predicted_xg": round(pred_xg_h, 2),
            "away_predicted_xg": round(pred_xg_a, 2),
            "predicted_home_score": pred_score_h,
            "predicted_away_score": pred_score_a,
            "advancing_team": advancing_team,
            "advancing_prob": round(max(adv_prob_h, adv_prob_a), 4),
            "most_likely_scores": top_scores
        }

    # Print out results
    for mid, pred in predictions.items():
        print(f"\n=========================================")
        print(f"Match {pred['match_id']}: {pred['home_team']} vs. {pred['away_team']}")
        print(f"Venue: {pred['venue']} | Referee: {pred['referee']}")
        print(f"Win Probability: {pred['home_team']} {pred['home_prob']*100:.1f}% | Draw {pred['draw_prob']*100:.1f}% | {pred['away_team']} {pred['away_prob']*100:.1f}%")
        print(f"Expected Goals (xG): {pred['home_team']} {pred['home_predicted_xg']:.2f} vs {pred['away_team']} {pred['away_predicted_xg']:.2f}")
        print(f"Predicted Score: {pred['predicted_home_score']} - {pred['predicted_away_score']}")
        print(f"Advancing Team: {pred['advancing_team']} ({pred['advancing_prob']*100:.1f}%)")
        print(f"Top 3 Scorelines:")
        for s in pred['most_likely_scores'][:3]:
            print(f"  - {s['score']}: {s['prob']*100:.1f}%")
            
    # Write output to predictions.json in assets folders
    out_dir_root = os.path.join(workspace_dir, "assets")
    out_dir_docs = os.path.join(workspace_dir, "docs", "assets")
    
    os.makedirs(out_dir_root, exist_ok=True)
    os.makedirs(out_dir_docs, exist_ok=True)
    
    path_root = os.path.join(out_dir_root, "predictions.json")
    path_docs = os.path.join(out_dir_docs, "predictions.json")
    
    with open(path_root, "w", encoding="utf-8") as f:
        json.dump(predictions, f, indent=2)
    with open(path_docs, "w", encoding="utf-8") as f:
        json.dump(predictions, f, indent=2)
        
    print(f"\nSuccessfully wrote predictions.json to root assets and docs assets!")

if __name__ == "__main__":
    main()
