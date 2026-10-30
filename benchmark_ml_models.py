import os
import json
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, log_loss

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

workspace_dir = os.path.dirname(os.path.abspath(__file__))
features_path = os.path.join(workspace_dir, "match_prediction_features.csv")

def main():
    print("====================================================")
    print("FIFA World Cup 2026 - Machine Learning Benchmark Suite")
    print("Strict Temporal Split: Group (M1-M72) -> Knockout (M73-M104)")
    print("====================================================\n")

    if not os.path.exists(features_path):
        print(f"Error: {features_path} not found.")
        return

    df = pd.read_csv(features_path)
    print(f"Loaded {features_path}: {df.shape[0]} matches, {df.shape[1]} columns")

    # Verify no post-match score leakage
    leakage_cols = [c for c in df.columns if c in ("home_score", "away_score", "result_type", "home_xg", "away_xg")]
    if leakage_cols:
        print(f"[WARNING] Leakage columns detected in features: {leakage_cols} - removing them.")
        df = df.drop(columns=leakage_cols)
    else:
        print("[VERIFIED] Zero post-match score leakage columns present in feature matrix.")

    # Strict temporal train/test split
    train_mask = df["match_id"] <= 72
    test_mask = df["match_id"] > 72

    meta_cols = ["match_id", "date", "kickoff_time_utc", "match_result"]
    feature_cols = [c for c in df.columns if c not in meta_cols]

    X_train_raw = df.loc[train_mask, feature_cols]
    y_train_raw = df.loc[train_mask, "match_result"]

    X_test_raw = df.loc[test_mask, feature_cols]
    y_test_raw = df.loc[test_mask, "match_result"]

    print(f"Training instances (Group Stage): {len(X_train_raw)}")
    print(f"Testing instances (Knockout Stage): {len(X_test_raw)}")
    print(f"Knockout actual class distribution: {y_test_raw.value_counts().to_dict()}\n")

    # Encode target labels
    le = LabelEncoder()
    y_train = le.fit_transform(y_train_raw)
    y_test = le.transform(y_test_raw)
    classes = le.classes_

    # Identify numeric and categorical columns
    categorical_cols = [c for c in feature_cols if df[c].dtype in ("object", "string", str)]
    numeric_cols = [c for c in feature_cols if c not in categorical_cols]

    # Preprocessing pipelines
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols)
    ])

    # 1. Naive Majority Class Baseline
    majority_class_idx = np.bincount(y_train).argmax()
    train_class_probs = np.bincount(y_train, minlength=len(classes)) / len(y_train)
    y_pred_naive = np.full(len(y_test), majority_class_idx)
    naive_probs = np.tile(train_class_probs, (len(y_test), 1))

    naive_acc = accuracy_score(y_test, y_pred_naive)
    naive_loss = log_loss(y_test, naive_probs)

    # Dictionary to collect results
    results = {
        "Naive Majority Baseline": {
            "accuracy": round(naive_acc * 100, 1),
            "log_loss": round(naive_loss, 2)
        }
    }

    # 2. Logistic Regression
    lr_pipe = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(C=0.5, max_iter=1000, random_state=42))
    ])
    lr_pipe.fit(X_train_raw, y_train)
    y_pred_lr = lr_pipe.predict(X_test_raw)
    y_prob_lr = lr_pipe.predict_proba(X_test_raw)
    lr_acc = accuracy_score(y_test, y_pred_lr)
    lr_loss = log_loss(y_test, y_prob_lr)
    results["Logistic Regression"] = {
        "accuracy": round(lr_acc * 100, 1),
        "log_loss": round(lr_loss, 2)
    }

    # 3. Random Forest (100 trees)
    rf_pipe = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=4, random_state=42))
    ])
    rf_pipe.fit(X_train_raw, y_train)
    y_pred_rf = rf_pipe.predict(X_test_raw)
    y_prob_rf = rf_pipe.predict_proba(X_test_raw)
    rf_acc = accuracy_score(y_test, y_pred_rf)
    rf_loss = log_loss(y_test, y_prob_rf)
    results["Random Forest (100 trees)"] = {
        "accuracy": round(rf_acc * 100, 1),
        "log_loss": round(rf_loss, 2)
    }

    # 4. XGBoost Classifier / Gradient Boosting
    if HAS_XGB:
        xgb_pipe = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.08, subsample=0.8, colsample_bytree=0.8, random_state=42, eval_metric="mlogloss"))
        ])
        model_name = "XGBoost Classifier"
    else:
        xgb_pipe = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", GradientBoostingClassifier(n_estimators=100, max_depth=3, learning_rate=0.08, subsample=0.8, random_state=42))
        ])
        model_name = "Gradient Boosted Classifier"

    xgb_pipe.fit(X_train_raw, y_train)
    y_pred_xgb = xgb_pipe.predict(X_test_raw)
    y_prob_xgb = xgb_pipe.predict_proba(X_test_raw)
    xgb_acc = accuracy_score(y_test, y_pred_xgb)
    xgb_loss = log_loss(y_test, y_prob_xgb)
    results[model_name] = {
        "accuracy": round(xgb_acc * 100, 1),
        "log_loss": round(xgb_loss, 2)
    }

    print("--- Benchmark Performance Metrics Table ---")
    print(f"{'Model Architecture':<30} | {'Accuracy':<10} | {'Log-Loss':<10}")
    print("-" * 56)
    for model, metrics in results.items():
        print(f"{model:<30} | {metrics['accuracy']:>6.1f}%    | {metrics['log_loss']:>6.2f}")

    # Save to json artifact
    out_json = os.path.join(workspace_dir, "benchmark_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved empirical benchmark metrics to: {out_json}")
    return results

if __name__ == "__main__":
    main()
