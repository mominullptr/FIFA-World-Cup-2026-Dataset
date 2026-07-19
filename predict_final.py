import os
import csv
import math
import json
import random

workspace_dir = os.path.dirname(os.path.abspath(__file__))

def safe_float(val, default=0.0):
    if not val or str(val).strip() == "":
        return default
    try:
        return float(val)
    except ValueError:
        return default

def safe_int(val, default=0):
    if not val or str(val).strip() == "":
        return default
    try:
        return int(val)
    except ValueError:
        return default

def get_prior_completed_matches(team_id, current_match_id, matches):
    prior = []
    for m in matches:
        mid = safe_int(m['match_id'])
        if mid < current_match_id and m['status'].strip().lower() == 'completed':
            h_id = safe_int(m['home_team_id'])
            a_id = safe_int(m['away_team_id'])
            if h_id == team_id or a_id == team_id:
                prior.append(mid)
    return sorted(prior)

def get_goal_concentration(team_id, prior_mids, events):
    if not prior_mids:
        return 0.0
    player_goals = {}
    total_goals = 0
    for row in events:
        mid = safe_int(row['match_id'])
        if mid in prior_mids:
            if safe_int(row['team_id']) == team_id and row['event_type'].strip().lower() == 'goal':
                pid = safe_int(row['player_id'])
                player_goals[pid] = player_goals.get(pid, 0) + 1
                total_goals += 1
    if total_goals == 0:
        return 0.0
    sorted_goals = sorted(player_goals.values(), reverse=True)
    top2_goals = sum(sorted_goals[:2])
    return top2_goals / total_goals

def get_playmaker_assist_share(team_id, prior_mids, events):
    if not prior_mids:
        return 0.0
    player_assists = {}
    total_assists = 0
    for row in events:
        mid = safe_int(row['match_id'])
        if mid in prior_mids:
            if safe_int(row['team_id']) == team_id and row['event_type'].strip().lower() == 'assist':
                pid = safe_int(row['player_id'])
                player_assists[pid] = player_assists.get(pid, 0) + 1
                total_assists += 1
    if total_assists == 0:
        return 0.0
    max_assists = max(player_assists.values())
    return max_assists / total_assists

def get_lineup_stability(team_id, prior_mids, lineups):
    if len(prior_mids) < 2:
        return 1.0
    pm1 = prior_mids[-1]
    pm2 = prior_mids[-2]
    
    def get_starting_xi(mid):
        xi = set()
        for row in lineups:
            if safe_int(row['match_id']) == mid and safe_int(row['team_id']) == team_id:
                if str(row['is_starting_xi']).strip() == '1':
                    xi.add(safe_int(row['player_id']))
        return xi
    
    xi1 = get_starting_xi(pm1)
    xi2 = get_starting_xi(pm2)
    
    if not xi1 or not xi2:
        return 1.0
    
    intersection = len(xi1.intersection(xi2))
    union = len(xi1.union(xi2))
    return intersection / union

def get_goalkeeper_stats(team_id, prior_mids, team_stats, match_map):
    if not prior_mids:
        return 0.75, 0.0
    total_saves = 0
    total_conceded = 0
    total_opponent_xg = 0.0
    
    # Map stats by (match_id, team_id)
    stats_by_match_team = {}
    for row in team_stats:
        stats_by_match_team[(safe_int(row['match_id']), safe_int(row['team_id']))] = row
        
    for mid in prior_mids:
        m = match_map[mid]
        h_id = safe_int(m['home_team_id'])
        if h_id == team_id:
            conceded = safe_int(m['away_score'])
            opp_xg = safe_float(m['away_xg'])
        else:
            conceded = safe_int(m['home_score'])
            opp_xg = safe_float(m['home_xg'])
            
        ts_row = stats_by_match_team.get((mid, team_id))
        saves = safe_int(ts_row['saves']) if ts_row else 0
        
        total_saves += saves
        total_conceded += conceded
        total_opponent_xg += opp_xg
        
    save_pct = 0.75
    if (total_saves + total_conceded) > 0:
        save_pct = total_saves / (total_saves + total_conceded)
        
    goals_prevented = total_opponent_xg - total_conceded
    return save_pct, goals_prevented

def train_poisson(X, y, epochs=3000, lr=0.03, l2=0.03):
    n_features = len(X[0])
    w = [0.0] * n_features
    w[0] = math.log(sum(y) / len(y)) if sum(y) > 0 else 0.0
    
    for epoch in range(epochs):
        grad = [0.0] * n_features
        for i in range(len(X)):
            x_i = X[i]
            y_i = y[i]
            dot = sum(w[k] * x_i[k] for k in range(n_features))
            pred = math.exp(dot)
            pred = min(max(pred, 1e-5), 20.0)
            error = pred - y_i
            for k in range(n_features):
                grad[k] += error * x_i[k]
        
        for k in range(n_features):
            w[k] -= lr * (grad[k] / len(X) + l2 * w[k])
            
    return w

def train_linear(X, y, epochs=3000, lr=0.03, l2=0.03):
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

def poisson_prob(k, lam):
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return (math.exp(-lam) * (lam**k)) / math.factorial(k)

def poisson_sample(lam):
    if lam <= 0:
        return 0
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1

def get_gk_boost(team_id):
    # Shootout saving penalty boosts based on historical shootout strength
    if team_id == 37: return 0.05  # Argentina (Emiliano Martínez)
    if team_id == 33: return 0.03  # France (Mike Maignan)
    if team_id == 29: return 0.02  # Spain (Unai Simón)
    if team_id == 45: return 0.02  # England (Jordan Pickford)
    return 0.0

def main():
    # Load all datasets
    def load_csv(name):
        path = os.path.join(workspace_dir, name)
        with open(path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
            
    matches = load_csv("matches.csv")
    events = load_csv("match_events.csv")
    lineups = load_csv("match_lineups.csv")
    team_stats = load_csv("match_team_stats.csv")
    prediction_features = load_csv("match_prediction_features.csv")
    
    match_map = {safe_int(m['match_id']): m for m in matches}
    
    # Precompute advanced features for all matches
    print("Precomputing advanced features...")
    match_advanced_features = {}
    for row in prediction_features:
        mid = safe_int(row['match_id'])
        h_id = safe_int(row['home_team_id'])
        a_id = safe_int(row['away_team_id'])
        
        h_prior = get_prior_completed_matches(h_id, mid, matches)
        a_prior = get_prior_completed_matches(a_id, mid, matches)
        
        h_gc = get_goal_concentration(h_id, h_prior, events)
        a_gc = get_goal_concentration(a_id, a_prior, events)
        
        h_pa = get_playmaker_assist_share(h_id, h_prior, events)
        a_pa = get_playmaker_assist_share(a_id, a_prior, events)
        
        h_ls = get_lineup_stability(h_id, h_prior, lineups)
        a_ls = get_lineup_stability(a_id, a_prior, lineups)
        
        h_sp, h_gp = get_goalkeeper_stats(h_id, h_prior, team_stats, match_map)
        a_sp, a_gp = get_goalkeeper_stats(a_id, a_prior, team_stats, match_map)
        
        match_advanced_features[mid] = {
            'h_gc': h_gc, 'a_gc': a_gc,
            'h_pa': h_pa, 'a_pa': a_pa,
            'h_ls': h_ls, 'a_ls': a_ls,
            'h_sp': h_sp, 'a_sp': a_sp,
            'h_gp': h_gp, 'a_gp': a_gp
        }

    # Build feature builder helper
    def build_features(row, is_home):
        mid = safe_int(row['match_id'])
        adv = match_advanced_features[mid]
        
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
        
        if is_home:
            elo_diff = (h_elo - a_elo) / 100.0
            rank_diff = (a_rank - h_rank) / 10.0
            val_ratio = math.log(max(h_val, 1.0) / max(a_val, 1.0))
            goals_diff = h_form_goals - a_form_conceded
            xg_diff = h_form_xg - a_form_xg_conceded
            
            gc_diff = adv['h_gc'] - adv['a_gc']
            pa_diff = adv['h_pa'] - adv['a_pa']
            ls_diff = adv['h_ls'] - adv['a_ls']
            sp_diff = adv['h_sp'] - adv['a_sp']
            gp_diff = (adv['h_gp'] - adv['a_gp']) / 5.0
        else:
            elo_diff = (a_elo - h_elo) / 100.0
            rank_diff = (h_rank - a_rank) / 10.0
            val_ratio = math.log(max(a_val, 1.0) / max(h_val, 1.0))
            goals_diff = a_form_goals - h_form_conceded
            xg_diff = a_form_xg - h_form_xg_conceded
            
            gc_diff = adv['a_gc'] - adv['h_gc']
            pa_diff = adv['a_pa'] - adv['h_pa']
            ls_diff = adv['a_ls'] - adv['h_ls']
            sp_diff = adv['a_sp'] - adv['h_sp']
            gp_diff = (adv['a_gp'] - adv['h_gp']) / 5.0
            
        return [1.0, elo_diff, rank_diff, val_ratio, goals_diff, xg_diff, gc_diff, pa_diff, ls_diff, sp_diff, gp_diff]

    # We want to generate predictions for [101, 102, 104]
    prediction_targets = [101, 102, 104]
    predictions = {}
    random.seed(19)

    for target_mid in prediction_targets:
        # Find the row for this target match
        target_row = None
        for r in prediction_features:
            if safe_int(r['match_id']) == target_mid:
                target_row = r
                break
        if not target_row:
            print(f"Warning: Match {target_mid} not found in prediction features.")
            continue

        # Determine completed training matches prior to this match
        train_rows = []
        for r in prediction_features:
            mid = safe_int(r['match_id'])
            if mid < target_mid and r['home_score'].strip() != "":
                train_rows.append(r)

        print(f"\n=========================================")
        print(f"Training model for Match {target_mid} using {len(train_rows)} prior completed matches...")
        
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
            
        w_goals = train_poisson(X_goals, y_goals)
        w_xg = train_linear(X_xg, y_xg)
        
        # Predict target match
        r = target_row
        h_name = r['home_team_name']
        a_name = r['away_team_name']
        h_id = safe_int(r['home_team_id'])
        a_id = safe_int(r['away_team_id'])
        
        x_home = build_features(r, is_home=True)
        x_away = build_features(r, is_home=False)
        
        lambda_h = math.exp(sum(w_goals[k] * x_home[k] for k in range(len(w_goals))))
        lambda_a = math.exp(sum(w_goals[k] * x_away[k] for k in range(len(w_goals))))
        
        pred_xg_h = max(0.0, sum(w_xg[k] * x_home[k] for k in range(len(w_xg))))
        pred_xg_a = max(0.0, sum(w_xg[k] * x_away[k] for k in range(len(w_xg))))
        
        # Final modifier: matches in the final (104) are historically low scoring and tense.
        # Apply a 15% reduction in goal expectation.
        if target_mid == 104:
            print(f"Applying final stage down-scaling modifier (15% reduction) to Match 104 expected goals.")
            lambda_h *= 0.85
            lambda_a *= 0.85
            
        print(f"Expected Goals Lambda: {h_name} {lambda_h:.3f} vs {a_name} {lambda_a:.3f}")
        
        # Shootout parameters
        h_gk_boost = get_gk_boost(h_id)
        a_gk_boost = get_gk_boost(a_id)
        h_elo = safe_float(r['home_elo'])
        a_elo = safe_float(r['away_elo'])
        elo_diff = h_elo - a_elo
        
        # Base shootout probability from ELO
        base_shootout_prob = 1.0 / (1.0 + math.exp(-0.002 * elo_diff))
        shootout_home_win_prob = base_shootout_prob + (h_gk_boost - a_gk_boost)
        shootout_home_win_prob = min(max(shootout_home_win_prob, 0.1), 0.9)
        
        # Run Monte Carlo Simulation
        sim_runs = 10000
        home_wins = 0
        draws = 0
        away_wins = 0
        adv_home = 0
        adv_away = 0
        scores = {}
        
        for _ in range(sim_runs):
            g_h = poisson_sample(lambda_h)
            g_a = poisson_sample(lambda_a)
            
            score_str = f"{g_h}-{g_a}"
            scores[score_str] = scores.get(score_str, 0) + 1
            
            if g_h > g_a:
                home_wins += 1
                adv_home += 1
            elif g_a > g_h:
                away_wins += 1
                adv_away += 1
            else:
                draws += 1
                # Extra Time (30 mins): sample extra goals with 0.25 scale (30/90 = 0.33, scaled down for fatigue)
                et_g_h = poisson_sample(lambda_h * 0.25)
                et_g_a = poisson_sample(lambda_a * 0.25)
                
                total_h = g_h + et_g_h
                total_a = g_a + et_g_a
                
                if total_h > total_a:
                    adv_home += 1
                elif total_a > total_h:
                    adv_away += 1
                else:
                    # Shootout
                    if random.random() < shootout_home_win_prob:
                        adv_home += 1
                    else:
                        adv_away += 1
                        
        prob_h = home_wins / sim_runs
        prob_d = draws / sim_runs
        prob_a = away_wins / sim_runs
        adv_prob_h = adv_home / sim_runs
        adv_prob_a = adv_away / sim_runs
        
        # Scorelines sorted
        score_probs = [(s, count / sim_runs) for s, count in scores.items()]
        score_probs.sort(key=lambda item: item[1], reverse=True)
        top_scores = [{"score": s, "prob": round(p, 4)} for s, p in score_probs[:5]]
        
        pred_score_str = top_scores[0]["score"]
        pred_score_h, pred_score_a = map(int, pred_score_str.split('-'))
        
        advancing_team = h_name if adv_prob_h >= 0.5 else a_name
        advancing_prob = max(adv_prob_h, adv_prob_a)
        
        predictions[f"match_{target_mid}"] = {
            "match_id": target_mid,
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
            "advancing_prob": round(advancing_prob, 4),
            "most_likely_scores": top_scores
        }
        
    # Print out results to console
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
