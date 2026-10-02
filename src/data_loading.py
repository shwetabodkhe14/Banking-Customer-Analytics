"""
Data Loading and Validation Module for Banking Customer Analytics
"""

import io
import os
from pathlib import Path
import pandas as pd

EXPECTED_COLUMNS = [
    "age", "job", "marital", "education", "default", "balance",
    "housing", "loan", "contact", "day", "month", "duration",
    "campaign", "pdays", "previous", "poutcome", "y"
]


def load_dataset(file_path: str = "data/bank-full.csv") -> pd.DataFrame:
    """
    Load the UCI Bank Marketing dataset into a pandas DataFrame.
    Handles standard semicolon-separated CSV as well as outer-quote-wrapped formats.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")

    print(f"Loading dataset from: {file_path}")
    
    # 1. First attempt standard pandas read
    try:
        df = pd.read_csv(path, sep=";", quotechar='"')
    except Exception as e:
        print(f"Standard read failed ({e}). Inspecting file formatting...")
        df = None

    # 2. Inspect if the read resulted in a malformed single-column DataFrame
    if df is None or df.shape[1] < len(EXPECTED_COLUMNS):
        print("Detected non-standard CSV formatting (single column or insufficient columns).")
        print("Inspecting file structure to determine parsing configuration...")
        
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            first_line = f.readline().strip()
        
        # Check if lines are wrapped in outer quotes with doubled internal quotes
        if first_line.startswith('"') and first_line.endswith('"') and (';""' in first_line or ';' in first_line):
            print("Detected outer-quote wrapping with doubled interior quotes. Unwrapping line stream...")
            lines = []
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped.startswith('"') and stripped.endswith('"'):
                        unwrapped = stripped[1:-1].replace('""', '"')
                        lines.append(unwrapped + "\n")
                    else:
                        lines.append(line)
            df = pd.read_csv(io.StringIO("".join(lines)), sep=";", quotechar='"')
        else:
            # Fallback: attempt python engine with comma or semicolon autodetection
            print("Attempting fallback engine with automatic separator detection...")
            df = pd.read_csv(path, sep=None, engine="python")

    # 3. Clean up column names (strip whitespace and residual quotes)
    df.columns = [col.strip().strip('"').strip("'") for col in df.columns]

    # 4. Strict Validation of Column Count and Names
    if df.shape[1] != len(EXPECTED_COLUMNS):
        raise ValueError(
            f"Dataset loading error: Expected {len(EXPECTED_COLUMNS)} columns, but found {df.shape[1]}.\n"
            f"Found columns: {df.columns.tolist()}"
        )

    missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    # Reorder columns to expected order for consistency
    df = df[EXPECTED_COLUMNS]
    print(f"Dataset successfully loaded. Shape: {df.shape[0]:,} rows, {df.shape[1]} columns.")
    return df


def validate_dataset(df: pd.DataFrame) -> dict:
    """
    Perform comprehensive data validation on the loaded dataset and display summary metrics.
    """
    print("\n" + "=" * 60)
    print("DATA VALIDATION REPORT")
    print("=" * 60)

    # A. Shape
    print(f"\n1. Dataset Shape: {df.shape[0]:,} rows, {df.shape[1]} columns")

    # B. Column Names
    print(f"\n2. Column Names ({len(df.columns)}):")
    print(df.columns.tolist())

    # C. First 5 Rows
    print("\n3. First 5 Records:")
    print(df.head())

    # D. Dataframe Info
    print("\n4. Dataframe Information:")
    buffer = io.StringIO()
    df.info(buf=buffer)
    print(buffer.getvalue())

    # E. Numerical Descriptive Statistics
    print("\n5. Numerical Descriptive Statistics:")
    print(df.describe())

    # F. Missing Values
    missing = df.isnull().sum()
    print("\n6. Missing Values per Column:")
    print(missing)

    # G. Duplicate Count
    dup_count = int(df.duplicated().sum())
    print(f"\n7. Duplicate Records Count: {dup_count}")

    # H. Unique Values in Categorical Columns
    cat_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    if not cat_cols:
        cat_cols = [col for col in df.columns if df[col].dtype == "object" or str(df[col].dtype) == "str"]
    print(f"\n8. Unique Values in Categorical Columns ({len(cat_cols)} columns):")
    unique_summary = {}
    for col in cat_cols:
        uniques = df[col].dropna().unique().tolist()
        unique_summary[col] = len(uniques)
        display_uniques = uniques if len(uniques) <= 12 else uniques[:10] + ["..."]
        print(f"   - {col} ({len(uniques)} unique): {display_uniques}")

    validation_summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "duplicates": dup_count,
        "missing_total": int(missing.sum()),
        "categorical_columns": cat_cols,
    }
    return validation_summary


if __name__ == "__main__":
    data = load_dataset("data/bank-full.csv")
    validate_dataset(data)
