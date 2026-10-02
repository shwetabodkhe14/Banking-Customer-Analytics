"""
Data Cleaning and Preprocessing Module for Banking Customer Analytics
"""

import os
from pathlib import Path
import pandas as pd

NUMERIC_COLUMNS = ["age", "balance", "day", "duration", "campaign", "pdays", "previous"]
CATEGORICAL_COLUMNS = [
    "job", "marital", "education", "default", "housing", "loan",
    "contact", "month", "poutcome", "y"
]


def clean_dataset(
    df: pd.DataFrame,
    save_output: bool = True,
    output_path: str = "outputs/cleaned_data/bank_cleaned.csv"
) -> pd.DataFrame:
    """
    Perform rigorous data cleaning on the banking dataset:
    - Preserves the original DataFrame via deep copy
    - Strips whitespace from categorical columns and standardizes text
    - Identifies and reports missing and 'unknown' values
    - Validates and enforces correct numeric data types
    - Validates realistic ranges for domain variables
    - Removes duplicate records if detected
    - Retains legitimate negative bank balances (overdraft accounts)
    - Exports cleaned dataset to CSV
    """
    print("\n" + "=" * 60)
    print("DATA CLEANING & PREPROCESSING")
    print("=" * 60)

    # 1. Preserve original dataset
    df_clean = df.copy(deep=True)
    initial_rows = len(df_clean)

    # 2. Check and remove duplicate rows
    duplicates = int(df_clean.duplicated().sum())
    if duplicates > 0:
        print(f"Found {duplicates} duplicate records. Removing duplicate rows...")
        df_clean = df_clean.drop_duplicates()
    else:
        print("Duplicate Check: 0 duplicate records found. Integrity verified.")

    # 3. Clean and standardize categorical columns
    print("\nStandardizing categorical columns...")
    for col in CATEGORICAL_COLUMNS:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip().str.lower()

    # 4. Enforce numeric data types and validate ranges
    print("\nConverting and validating numeric columns...")
    for col in NUMERIC_COLUMNS:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
            nan_count = int(df_clean[col].isnull().sum())
            if nan_count > 0:
                print(f"Warning: {nan_count} non-numeric values coerced to NaN in '{col}'.")

    # 5. Domain range validation
    print("\nValidating domain value ranges:")
    # Age check (must be positive, typically 18+)
    invalid_age = df_clean[df_clean["age"] < 18]
    print(f"   - Age < 18: {len(invalid_age)} records (Min Age: {df_clean['age'].min()}, Max Age: {df_clean['age'].max()})")

    # Negative balance check
    neg_balance_count = int((df_clean["balance"] < 0).sum())
    neg_balance_pct = (neg_balance_count / len(df_clean)) * 100
    print(f"   - Negative Balances (Overdrafts): {neg_balance_count:,} accounts ({neg_balance_pct:.2f}%). Retained as legitimate.")

    # Call duration check
    neg_duration = int((df_clean["duration"] < 0).sum())
    print(f"   - Negative Call Duration: {neg_duration} records")

    # Campaign contacts check
    zero_campaign = int((df_clean["campaign"] < 1).sum())
    print(f"   - Campaign contacts < 1: {zero_campaign} records")

    # 6. Audit 'unknown' values in categorical columns
    print("\nAuditing 'unknown' values across categorical attributes:")
    unknown_audit = {}
    for col in CATEGORICAL_COLUMNS:
        if col in df_clean.columns:
            cnt = int((df_clean[col] == "unknown").sum())
            pct = (cnt / len(df_clean)) * 100
            unknown_audit[col] = (cnt, pct)
            if cnt > 0:
                print(f"   - {col:12s}: {cnt:>6,} records ({pct:5.2f}%) are 'unknown'")

    print("   Note: 'unknown' values are retained as informative categories rather than artificially imputed.")

    # 7. Derived Feature Engineering (age_group)
    # The source dataset contains 17 columns. We engineer an 18th column, 'age_group',
    # to facilitate demographic cohort analysis across discrete age brackets.
    print("\nFeature Engineering (Derived Attributes):")
    age_bins = [17, 25, 35, 45, 55, 65, 120]
    age_labels = ["18-25", "26-35", "36-45", "46-55", "56-65", "66+"]
    df_clean["age_group"] = pd.cut(df_clean["age"], bins=age_bins, labels=age_labels)
    print(f"   - Derived Column Added: 'age_group' with 6 cohorts: {age_labels}")
    print(f"   - Column Count Transition: {len(df.columns)} source columns -> {len(df_clean.columns)} columns in cleaned dataset.")

    # 8. Save cleaned dataset
    if save_output:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        df_clean.to_csv(out_file, index=False)
        print(f"\nCleaned dataset successfully saved to: {output_path}")
        print(f"Final Cleaned Dataset Dimensions: {df_clean.shape[0]:,} rows x {df_clean.shape[1]} columns (17 source + 1 derived feature 'age_group')")

    return df_clean


if __name__ == "__main__":
    from data_loading import load_dataset
    raw_df = load_dataset("data/bank-full.csv")
    cleaned_df = clean_dataset(raw_df)
