"""
Banking Customer & Marketing Analytics
Main Pipeline Runner

Coordinates data loading, validation, cleaning, statistical analysis,
visualization, and report generation.
"""

import sys
from pathlib import Path
import pandas as pd

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loading import load_dataset, validate_dataset
from src.data_cleaning import clean_dataset
from src.analysis import (
    analyze_demographics,
    analyze_financial_profile,
    analyze_marketing,
    analyze_target,
    answer_business_questions,
    generate_business_insights_report
)
from src.visualization import generate_all_visualizations


def print_banner(title: str):
    """Print standard section banner."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    print("=" * 60)
    print("BANKING CUSTOMER & MARKETING ANALYTICS")
    print("=" * 60)

    # ----------------------------------------------------
    # [1] DATA LOADING
    # ----------------------------------------------------
    print_banner("[1] DATA LOADING")
    data_path = PROJECT_ROOT / "data" / "bank-full.csv"
    raw_df = load_dataset(str(data_path))

    # ----------------------------------------------------
    # [2] DATA VALIDATION
    # ----------------------------------------------------
    print_banner("[2] DATA VALIDATION")
    validation_summary = validate_dataset(raw_df)

    # ----------------------------------------------------
    # [3] DATA CLEANING
    # ----------------------------------------------------
    print_banner("[3] DATA CLEANING")
    cleaned_path = PROJECT_ROOT / "outputs" / "cleaned_data" / "bank_cleaned.csv"
    cleaned_df = clean_dataset(raw_df, save_output=True, output_path=str(cleaned_path))

    # ----------------------------------------------------
    # [4] CUSTOMER ANALYSIS
    # ----------------------------------------------------
    print_banner("[4] CUSTOMER ANALYSIS")
    demographics = analyze_demographics(cleaned_df)
    
    print("\nA. Age Profile:")
    for k, v in demographics["age_stats"].items():
        print(f"   - {k.capitalize():8s}: {v}")

    print("\nB. Customer Count by Age Group:")
    print(demographics["age_group_distribution"])

    print("\nC. Job Distribution (Top 5 categories):")
    print(demographics["job_distribution"].head(5))

    print("\nD. Education Distribution:")
    print(demographics["education_distribution"])

    print("\nE. Mean Account Balance by Top Job Roles:")
    print(demographics["balance_by_job"].head(5))

    # ----------------------------------------------------
    # [5] FINANCIAL ANALYSIS
    # ----------------------------------------------------
    print_banner("[5] FINANCIAL ANALYSIS")
    financial = analyze_financial_profile(cleaned_df)

    print("\nA. Account Balance Statistics (EUR):")
    b_stat = financial["balance_summary"]
    print(f"   - Mean Balance    : EUR {b_stat['mean']:,.2f}")
    print(f"   - Median Balance  : EUR {b_stat['median']:,.2f}")
    print(f"   - Std Deviation   : EUR {b_stat['std']:,.2f}")
    print(f"   - Minimum Balance : EUR {b_stat['min']:,.2f}")
    print(f"   - Maximum Balance : EUR {b_stat['max']:,.2f}")
    print(f"   - 25th Percentile : EUR {b_stat['q25']:,.2f}")
    print(f"   - 75th Percentile : EUR {b_stat['q75']:,.2f}")
    print(f"   - Overdraft Accts : {b_stat['negative_balance_count']:,} ({b_stat['negative_balance_pct']}%)")

    print("\nB. Loan Portfolio Breakdown:")
    print("Housing Loans:")
    print(financial["housing_loan"])
    print("\nPersonal Loans:")
    print(financial["personal_loan"])
    print("\nCredit in Default:")
    print(financial["credit_default"])

    # ----------------------------------------------------
    # [6] MARKETING ANALYSIS
    # ----------------------------------------------------
    print_banner("[6] MARKETING ANALYSIS")
    marketing = analyze_marketing(cleaned_df)

    print("\nA. Contact Method Distribution:")
    print(marketing["contact_method"])

    print("\nB. Campaign Contacts Summary:")
    for k, v in marketing["campaign_contacts"].items():
        print(f"   - {k.capitalize():8s}: {v}")

    print("\nC. Call Duration Summary:")
    print(f"   - Mean Duration   : {marketing['duration_seconds']['mean']} seconds ({marketing['duration_minutes']['mean']} minutes)")
    print(f"   - Median Duration : {marketing['duration_seconds']['median']} seconds ({marketing['duration_minutes']['median']} minutes)")

    print("\nD. Prior Campaign Exposure:")
    p_exp = marketing["previous_campaign_exposure"]
    print(f"   - Previously Contacted Clients : {p_exp['previously_contacted_count']:,} ({p_exp['previously_contacted_pct']}%)")
    print(f"   - New Campaign Contacts        : {p_exp['new_contacts_count']:,} ({p_exp['new_contacts_pct']}%)")

    print("\nE. Previous Campaign Outcome Distribution:")
    print(marketing["poutcome_distribution"])

    # ----------------------------------------------------
    # [7] TARGET ANALYSIS
    # ----------------------------------------------------
    print_banner("[7] TARGET ANALYSIS")
    target = analyze_target(cleaned_df)
    t_sum = target["overall_target"]

    print(f"\nA. Overall Target Variable (y) Distribution:")
    print(f"   - Subscribed (yes)     : {t_sum['subscribed_yes']:,} ({t_sum['overall_subscription_rate_pct']}%)")
    print(f"   - Not Subscribed (no)  : {t_sum['not_subscribed_no']:,} ({100 - t_sum['overall_subscription_rate_pct']:.2f}%)")

    print("\nB. Subscription Rate by Age Group:")
    print(target["subscription_by_age_group"])

    print("\nC. Subscription Rate by Job Category (Top 5 & Bottom 3):")
    job_rates = target["subscription_by_job"]
    print("--- Top 5 ---")
    print(job_rates.head(5))
    print("--- Bottom 3 ---")
    print(job_rates.tail(3))

    print("\nD. Subscription Rate by Housing Loan:")
    print(target["subscription_by_housing"])

    print("\nE. Subscription Rate by Previous Campaign Outcome:")
    print(target["subscription_by_poutcome"])

    # ----------------------------------------------------
    # [8] VISUALIZATION
    # ----------------------------------------------------
    print_banner("[8] VISUALIZATION")
    charts_dir = PROJECT_ROOT / "outputs" / "charts"
    charts_generated = generate_all_visualizations(cleaned_df, output_dir=str(charts_dir))
    print(f"Total Charts Successfully Generated: {len(charts_generated)}")

    # ----------------------------------------------------
    # [9] BUSINESS INSIGHTS
    # ----------------------------------------------------
    print_banner("[9] BUSINESS INSIGHTS")
    business_questions = answer_business_questions(cleaned_df)

    print("\nANSWERS TO THE 10 STRATEGIC BUSINESS QUESTIONS:")
    for q_key, item in business_questions.items():
        print(f"\n[{q_key}] {item['question']}")
        print(f"   --> {item['answer_summary']}")

    # Compile all analytical outputs for the report generator
    analysis_package = {
        "demographics": demographics,
        "financial": financial,
        "marketing": marketing,
        "target": target,
        "business_questions": business_questions
    }

    report_path = PROJECT_ROOT / "outputs" / "reports" / "business_insights.txt"
    generate_business_insights_report(cleaned_df, analysis_package, output_path=str(report_path))

    print("\n" + "=" * 60)
    print("ANALYTICS PIPELINE EXECUTION COMPLETE")
    print("=" * 60)
    print(f"Cleaned Data Output : {cleaned_path}")
    print(f"Charts Directory    : {charts_dir} ({len(charts_generated)} figures)")
    print(f"Report Output       : {report_path}")


if __name__ == "__main__":
    main()