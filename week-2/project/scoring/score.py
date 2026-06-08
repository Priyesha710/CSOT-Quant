"""
Scoring script for Week 2 Project.
Computes R-squared between predicted and actual target values.

Usage:
    python score.py --predictions submission.csv --actuals actual_targets.csv

Both CSVs must have columns: id, predicted_target (or target for actuals).
"""

import argparse
import sys

import numpy as np
import pandas as pd


def compute_r2(actual: np.ndarray, predicted: np.ndarray) -> float:
    ss_res = np.sum((actual - predicted) ** 2)
    ss_tot = np.sum((actual - np.mean(actual)) ** 2)
    if ss_tot == 0:
        return 0.0
    return 1.0 - (ss_res / ss_tot)


def validate_submission(submission: pd.DataFrame, actuals: pd.DataFrame) -> list[str]:
    errors = []

    if 'id' not in submission.columns:
        errors.append("Submission missing 'id' column")
    if 'predicted_target' not in submission.columns:
        errors.append("Submission missing 'predicted_target' column")

    if errors:
        return errors

    if submission['predicted_target'].isnull().any():
        n_null = submission['predicted_target'].isnull().sum()
        errors.append(f"Submission has {n_null} NaN values in predicted_target")

    if np.isinf(submission['predicted_target']).any():
        n_inf = np.isinf(submission['predicted_target']).sum()
        errors.append(f"Submission has {n_inf} Inf values in predicted_target")

    if submission['id'].duplicated().any():
        n_dup = submission['id'].duplicated().sum()
        errors.append(f"Submission has {n_dup} duplicate ID rows")

    if actuals['id'].duplicated().any():
        n_dup = actuals['id'].duplicated().sum()
        errors.append(f"Actuals file has {n_dup} duplicate ID rows")

    expected_ids = set(actuals['id'].values)
    submitted_ids = set(submission['id'].values)

    missing = expected_ids - submitted_ids
    if missing:
        errors.append(f"Missing {len(missing)} IDs in submission")

    extra = submitted_ids - expected_ids
    if extra:
        errors.append(f"Found {len(extra)} unexpected IDs in submission")

    if len(submission) != len(actuals):
        errors.append(
            f"Submission row count ({len(submission)}) does not match actuals row count ({len(actuals)})"
        )

    return errors


def main():
    parser = argparse.ArgumentParser(description="Score predictions using R-squared")
    parser.add_argument("--predictions", required=True, help="Path to submission CSV")
    parser.add_argument("--actuals", required=True, help="Path to actuals CSV (with 'target' column)")
    args = parser.parse_args()

    submission = pd.read_csv(args.predictions)
    actuals = pd.read_csv(args.actuals)

    if 'target' in actuals.columns:
        actuals = actuals.rename(columns={'target': 'predicted_target'})
    elif 'predicted_target' not in actuals.columns:
        print("Error: actuals file must have 'target' or 'predicted_target' column")
        sys.exit(1)

    errors = validate_submission(submission, actuals)
    if errors:
        print("Submission validation failed:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    merged = actuals.merge(submission, on='id', suffixes=('_actual', '_predicted'))
    actual_values = merged['predicted_target_actual'].values
    predicted_values = merged['predicted_target_predicted'].values

    r2 = compute_r2(actual_values, predicted_values)

    print(f"Submission validated successfully.")
    print(f"Number of predictions: {len(merged)}")
    print(f"R-squared score: {r2:.6f}")

    if r2 < 0:
        print("Note: Negative R² means predictions are worse than predicting the mean.")
    elif r2 < 0.01:
        print("Note: R² near zero — model barely outperforms mean prediction.")


if __name__ == "__main__":
    main()
