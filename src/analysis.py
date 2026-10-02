"""
Exploratory Data Analysis and Business Questions Module for Banking Customer Analytics
"""

import pandas as pd
import numpy as np


def analyze_demographics(df: pd.DataFrame) -> dict:
    """Analyze demographic distributions and customer segmentation."""
    results = {}

    # Age stats
    results["age_stats"] = {
        "mean": float(df["age"].mean()),
        "median": float(df["age"].median()),
        "std": float(df["age"].std()),
        "min": int(df["age"].min()),
        "max": int(df["age"].max()),
    }

    # Job distribution
    job_counts = df["job"].value_counts()
    job_pcts = df["job"].value_counts(normalize=True) * 100
    results["job_distribution"] = pd.DataFrame({
        "Count": job_counts,
        "Percentage (%)": job_pcts.round(2)
    })

    # Marital status distribution
    marital_counts = df["marital"].value_counts()
    marital_pcts = df["marital"].value_counts(normalize=True) * 100
    results["marital_distribution"] = pd.DataFrame({
        "Count": marital_counts,
        "Percentage (%)": marital_pcts.round(2)
    })

    # Education level distribution
    edu_counts = df["education"].value_counts()
    edu_pcts = df["education"].value_counts(normalize=True) * 100
    results["education_distribution"] = pd.DataFrame({
        "Count": edu_counts,
        "Percentage (%)": edu_pcts.round(2)
    })

    # Average balance by job
    results["balance_by_job"] = df.groupby("job")["balance"].agg(
        Mean_Balance="mean",
        Median_Balance="median",
        Customer_Count="count"
    ).round(2).sort_values(by="Mean_Balance", ascending=False)

    # Average balance by education
    results["balance_by_education"] = df.groupby("education")["balance"].agg(
        Mean_Balance="mean",
        Median_Balance="median",
        Customer_Count="count"
    ).round(2).sort_values(by="Mean_Balance", ascending=False)

    # Age group distribution
    if "age_group" in df.columns:
        age_grp_counts = df["age_group"].value_counts().sort_index()
        age_grp_pcts = (df["age_group"].value_counts(normalize=True).sort_index() * 100).round(2)
        results["age_group_distribution"] = pd.DataFrame({
            "Count": age_grp_counts,
            "Percentage (%)": age_grp_pcts
        })

    return results


def analyze_financial_profile(df: pd.DataFrame) -> dict:
    """Analyze financial profile: balances, housing loans, personal loans, defaults."""
    results = {}

    total_customers = len(df)
    balance_series = df["balance"]

    results["balance_summary"] = {
        "mean": float(balance_series.mean()),
        "median": float(balance_series.median()),
        "std": float(balance_series.std()),
        "min": float(balance_series.min()),
        "max": float(balance_series.max()),
        "q25": float(balance_series.quantile(0.25)),
        "q75": float(balance_series.quantile(0.75)),
        "negative_balance_count": int((balance_series < 0).sum()),
        "negative_balance_pct": round(float((balance_series < 0).mean() * 100), 2),
        "zero_balance_count": int((balance_series == 0).sum()),
        "positive_balance_count": int((balance_series > 0).sum()),
    }

    # Housing loan status
    housing_counts = df["housing"].value_counts()
    housing_pcts = (df["housing"].value_counts(normalize=True) * 100).round(2)
    results["housing_loan"] = pd.DataFrame({"Count": housing_counts, "Percentage (%)": housing_pcts})

    # Personal loan status
    loan_counts = df["loan"].value_counts()
    loan_pcts = (df["loan"].value_counts(normalize=True) * 100).round(2)
    results["personal_loan"] = pd.DataFrame({"Count": loan_counts, "Percentage (%)": loan_pcts})

    # Credit default status
    default_counts = df["default"].value_counts()
    default_pcts = (df["default"].value_counts(normalize=True) * 100).round(2)
    results["credit_default"] = pd.DataFrame({"Count": default_counts, "Percentage (%)": default_pcts})

    return results


def analyze_marketing(df: pd.DataFrame) -> dict:
    """Analyze campaign contacts, durations, contact methods, and previous outcomes."""
    results = {}

    # Contact method
    contact_counts = df["contact"].value_counts()
    contact_pcts = (df["contact"].value_counts(normalize=True) * 100).round(2)
    results["contact_method"] = pd.DataFrame({"Count": contact_counts, "Percentage (%)": contact_pcts})

    # Campaign contacts
    results["campaign_contacts"] = {
        "mean": round(float(df["campaign"].mean()), 2),
        "median": float(df["campaign"].median()),
        "max": int(df["campaign"].max()),
        "min": int(df["campaign"].min()),
    }

    # Call duration (seconds and minutes)
    results["duration_seconds"] = {
        "mean": round(float(df["duration"].mean()), 2),
        "median": float(df["duration"].median()),
        "std": round(float(df["duration"].std()), 2),
        "min": int(df["duration"].min()),
        "max": int(df["duration"].max()),
    }
    results["duration_minutes"] = {
        "mean": round(float(df["duration"].mean() / 60), 2),
        "median": round(float(df["duration"].median() / 60), 2),
    }

    # Previous campaign contacts and days passed
    previously_contacted = (df["pdays"] != -1).sum()
    results["previous_campaign_exposure"] = {
        "previously_contacted_count": int(previously_contacted),
        "previously_contacted_pct": round(float(previously_contacted / len(df) * 100), 2),
        "new_contacts_count": int((df["pdays"] == -1).sum()),
        "new_contacts_pct": round(float((df["pdays"] == -1).mean() * 100), 2),
    }

    # Previous campaign outcomes
    poutcome_counts = df["poutcome"].value_counts()
    poutcome_pcts = (df["poutcome"].value_counts(normalize=True) * 100).round(2)
    results["poutcome_distribution"] = pd.DataFrame({"Count": poutcome_counts, "Percentage (%)": poutcome_pcts})

    return results


def calculate_conversion_rate(df: pd.DataFrame, group_col: str, target_col: str = "y") -> pd.DataFrame:
    """Helper to calculate conversion/subscription rate grouped by a specific column."""
    agg_df = df.groupby(group_col)[target_col].agg(
        Total_Customers="count",
        Subscribed=lambda s: (s == "yes").sum(),
        Not_Subscribed=lambda s: (s == "no").sum(),
        Subscription_Rate_Pct=lambda s: round((s == "yes").mean() * 100, 2)
    ).sort_values(by="Subscription_Rate_Pct", ascending=False)
    return agg_df


def analyze_target(df: pd.DataFrame) -> dict:
    """Analyze target variable 'y' and subscription rates across multiple customer segments."""
    results = {}

    total = len(df)
    yes_count = int((df["y"] == "yes").sum())
    no_count = int((df["y"] == "no").sum())
    overall_rate = round((yes_count / total) * 100, 2)

    results["overall_target"] = {
        "total_records": total,
        "subscribed_yes": yes_count,
        "not_subscribed_no": no_count,
        "overall_subscription_rate_pct": overall_rate,
    }

    # Breakdown by various segments
    segments = ["age_group", "job", "education", "marital", "housing", "loan", "contact", "poutcome"]
    for seg in segments:
        if seg in df.columns:
            results[f"subscription_by_{seg}"] = calculate_conversion_rate(df, seg)

    return results


def answer_business_questions(df: pd.DataFrame) -> dict:
    """
    Programmatically answer the 10 core business questions with exact counts, percentages, and metrics.
    """
    answers = {}

    # Q1: What percentage of customers subscribed to a term deposit?
    total = len(df)
    yes_cnt = int((df["y"] == "yes").sum())
    no_cnt = int((df["y"] == "no").sum())
    sub_pct = round((yes_cnt / total) * 100, 2)
    answers["Q1"] = {
        "question": "What percentage of customers subscribed to a term deposit?",
        "total_customers": total,
        "subscribed_count": yes_cnt,
        "not_subscribed_count": no_cnt,
        "subscription_rate_pct": sub_pct,
        "answer_summary": f"{sub_pct}% of customers ({yes_cnt:,} of {total:,}) subscribed to a term deposit."
    }

    # Q2: Which job categories have the highest subscription rate?
    job_sub = calculate_conversion_rate(df, "job")
    top_jobs = job_sub.head(3)
    answers["Q2"] = {
        "question": "Which job categories have the highest subscription rate?",
        "table": job_sub,
        "top_job": job_sub.index[0],
        "top_rate_pct": float(job_sub.iloc[0]["Subscription_Rate_Pct"]),
        "answer_summary": (
            f"The job categories with the highest subscription rates are {job_sub.index[0]} "
            f"({job_sub.iloc[0]['Subscription_Rate_Pct']}%, {int(job_sub.iloc[0]['Subscribed'])}/{int(job_sub.iloc[0]['Total_Customers'])}), "
            f"followed by {job_sub.index[1]} ({job_sub.iloc[1]['Subscription_Rate_Pct']}%) and "
            f"{job_sub.index[2]} ({job_sub.iloc[2]['Subscription_Rate_Pct']}%)."
        )
    }

    # Q3: Which education groups have the highest subscription rate?
    edu_sub = calculate_conversion_rate(df, "education")
    answers["Q3"] = {
        "question": "Which education groups have the highest subscription rate?",
        "table": edu_sub,
        "top_education": edu_sub.index[0],
        "top_rate_pct": float(edu_sub.iloc[0]["Subscription_Rate_Pct"]),
        "answer_summary": (
            f"Customers with '{edu_sub.index[0]}' education had the highest subscription rate at "
            f"{edu_sub.iloc[0]['Subscription_Rate_Pct']}% ({int(edu_sub.iloc[0]['Subscribed']):,}/{int(edu_sub.iloc[0]['Total_Customers']):,}), "
            f"followed by '{edu_sub.index[1]}' ({edu_sub.iloc[1]['Subscription_Rate_Pct']}%)."
        )
    }

    # Q4: How does housing loan status relate to subscription?
    housing_sub = calculate_conversion_rate(df, "housing")
    no_h_rate = float(housing_sub.loc["no", "Subscription_Rate_Pct"])
    yes_h_rate = float(housing_sub.loc["yes", "Subscription_Rate_Pct"])
    answers["Q4"] = {
        "question": "How does housing loan status relate to subscription?",
        "table": housing_sub,
        "no_housing_rate": no_h_rate,
        "yes_housing_rate": yes_h_rate,
        "answer_summary": (
            f"Customers without a housing loan subscribed at {no_h_rate}% ({int(housing_sub.loc['no', 'Subscribed']):,}/{int(housing_sub.loc['no', 'Total_Customers']):,}), "
            f"which is more than double the subscription rate of customers with a housing loan ({yes_h_rate}%, {int(housing_sub.loc['yes', 'Subscribed']):,}/{int(housing_sub.loc['yes', 'Total_Customers']):,})."
        )
    }

    # Q5: How does personal loan status relate to subscription?
    loan_sub = calculate_conversion_rate(df, "loan")
    no_l_rate = float(loan_sub.loc["no", "Subscription_Rate_Pct"])
    yes_l_rate = float(loan_sub.loc["yes", "Subscription_Rate_Pct"])
    answers["Q5"] = {
        "question": "How does personal loan status relate to subscription?",
        "table": loan_sub,
        "no_loan_rate": no_l_rate,
        "yes_loan_rate": yes_l_rate,
        "answer_summary": (
            f"Customers without personal loans had a subscription rate of {no_l_rate}% ({int(loan_sub.loc['no', 'Subscribed']):,}/{int(loan_sub.loc['no', 'Total_Customers']):,}) "
            f"compared to only {yes_l_rate}% ({int(loan_sub.loc['yes', 'Subscribed']):,}/{int(loan_sub.loc['yes', 'Total_Customers']):,}) for customers with personal loans."
        )
    }

    # Q6: Which contact method has the highest subscription rate?
    contact_sub = calculate_conversion_rate(df, "contact")
    answers["Q6"] = {
        "question": "Which contact method has the highest subscription rate?",
        "table": contact_sub,
        "top_contact": contact_sub.index[0],
        "top_rate": float(contact_sub.iloc[0]["Subscription_Rate_Pct"]),
        "answer_summary": (
            f"'{contact_sub.index[0]}' communication yielded the highest subscription rate at {contact_sub.iloc[0]['Subscription_Rate_Pct']}% "
            f"({int(contact_sub.iloc[0]['Subscribed']):,}/{int(contact_sub.iloc[0]['Total_Customers']):,}), "
            f"followed by '{contact_sub.index[1]}' at {contact_sub.iloc[1]['Subscription_Rate_Pct']}%, "
            f"while 'unknown' contact had only {contact_sub.loc['unknown', 'Subscription_Rate_Pct']}%."
        )
    }

    # Q7: How does previous campaign outcome relate to the current outcome?
    poutcome_sub = calculate_conversion_rate(df, "poutcome")
    success_rate = float(poutcome_sub.loc["success", "Subscription_Rate_Pct"]) if "success" in poutcome_sub.index else 0.0
    failure_rate = float(poutcome_sub.loc["failure", "Subscription_Rate_Pct"]) if "failure" in poutcome_sub.index else 0.0
    unknown_rate = float(poutcome_sub.loc["unknown", "Subscription_Rate_Pct"]) if "unknown" in poutcome_sub.index else 0.0
    answers["Q7"] = {
        "question": "How does previous campaign outcome relate to the current outcome?",
        "table": poutcome_sub,
        "success_rate": success_rate,
        "failure_rate": failure_rate,
        "unknown_rate": unknown_rate,
        "answer_summary": (
            f"Clients with previous campaign outcome 'success' had a massive {success_rate}% subscription rate "
            f"({int(poutcome_sub.loc['success', 'Subscribed']):,}/{int(poutcome_sub.loc['success', 'Total_Customers']):,}), "
            f"compared to {failure_rate}% for 'failure' and {unknown_rate}% for 'unknown'."
        )
    }

    # Q8: Which age group has the highest subscription rate?
    age_grp_sub = calculate_conversion_rate(df, "age_group")
    top_age_grp = age_grp_sub.index[0]
    answers["Q8"] = {
        "question": "Which age group has the highest subscription rate?",
        "table": age_grp_sub,
        "top_age_group": str(top_age_grp),
        "top_rate": float(age_grp_sub.iloc[0]["Subscription_Rate_Pct"]),
        "answer_summary": (
            f"The '{top_age_grp}' age group had the highest subscription rate at {age_grp_sub.iloc[0]['Subscription_Rate_Pct']}% "
            f"({int(age_grp_sub.iloc[0]['Subscribed']):,}/{int(age_grp_sub.iloc[0]['Total_Customers']):,}), "
            f"followed by the '{age_grp_sub.index[1]}' group at {age_grp_sub.iloc[1]['Subscription_Rate_Pct']}%."
        )
    }

    # Q9: What is the average balance of customers who subscribed versus those who did not?
    bal_yes = df[df["y"] == "yes"]["balance"]
    bal_no = df[df["y"] == "no"]["balance"]
    bal_yes_mean = float(bal_yes.mean())
    bal_yes_median = float(bal_yes.median())
    bal_no_mean = float(bal_no.mean())
    bal_no_median = float(bal_no.median())
    diff_bal = bal_yes_mean - bal_no_mean
    pct_bal_diff = (diff_bal / bal_no_mean) * 100 if bal_no_mean != 0 else 0.0

    answers["Q9"] = {
        "question": "What is the average balance of customers who subscribed versus those who did not?",
        "mean_balance_subscribed": round(bal_yes_mean, 2),
        "median_balance_subscribed": round(bal_yes_median, 2),
        "mean_balance_not_subscribed": round(bal_no_mean, 2),
        "median_balance_not_subscribed": round(bal_no_median, 2),
        "difference_mean_balance": round(diff_bal, 2),
        "pct_higher": round(pct_bal_diff, 2),
        "answer_summary": (
            f"Customers who subscribed (y='yes') had an average balance of EUR {bal_yes_mean:,.2f} "
            f"(median: EUR {bal_yes_median:,.2f}), whereas customers who did not subscribe (y='no') "
            f"had an average balance of EUR {bal_no_mean:,.2f} (median: EUR {bal_no_median:,.2f}). "
            f"Subscribed customers held on average EUR {diff_bal:,.2f} (+{pct_bal_diff:.1f}%) higher balances."
        )
    }

    # Q10: How does call duration relate to subscription?
    dur_yes = df[df["y"] == "yes"]["duration"]
    dur_no = df[df["y"] == "no"]["duration"]
    dur_yes_mean = float(dur_yes.mean())
    dur_yes_median = float(dur_yes.median())
    dur_no_mean = float(dur_no.mean())
    dur_no_median = float(dur_no.median())
    dur_diff = dur_yes_mean - dur_no_mean
    dur_pct_diff = (dur_diff / dur_no_mean) * 100 if dur_no_mean != 0 else 0.0

    answers["Q10"] = {
        "question": "How does call duration relate to subscription?",
        "mean_duration_subscribed_sec": round(dur_yes_mean, 2),
        "median_duration_subscribed_sec": round(dur_yes_median, 2),
        "mean_duration_subscribed_min": round(dur_yes_mean / 60, 2),
        "mean_duration_not_subscribed_sec": round(dur_no_mean, 2),
        "median_duration_not_subscribed_sec": round(dur_no_median, 2),
        "mean_duration_not_subscribed_min": round(dur_no_mean / 60, 2),
        "difference_duration_sec": round(dur_diff, 2),
        "pct_longer": round(dur_pct_diff, 2),
        "answer_summary": (
            f"Subscribed customers (y='yes') had an average call duration of {dur_yes_mean:.2f} seconds / "
            f"{dur_yes_mean / 60:.2f} mins (median: {dur_yes_median:.2f} seconds / {dur_yes_median / 60:.2f} mins), compared to "
            f"{dur_no_mean:.2f} seconds / {dur_no_mean / 60:.2f} mins (median: {dur_no_median:.2f} seconds / {dur_no_median / 60:.2f} mins) "
            f"for non-subscribed customers (y='no'). Calls with clients who subscribed lasted on average "
            f"{dur_diff:.1f} seconds (+{dur_pct_diff:.1f}%) longer."
        )
    }

    return answers


def generate_business_insights_report(df: pd.DataFrame, results: dict, output_path: str = "outputs/reports/business_insights.txt") -> str:
    """
    Generate an empirical, data-driven business insights report based strictly on observed dataset values.
    Writes the report to outputs/reports/business_insights.txt.
    """
    from pathlib import Path
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    bq = results["business_questions"]
    dem = results["demographics"]
    fin = results["financial"]
    mkt = results["marketing"]
    tgt = results["target"]

    total = len(df)
    sub_cnt = bq["Q1"]["subscribed_count"]
    sub_pct = bq["Q1"]["subscription_rate_pct"]

    report_lines = [
        "=" * 70,
        "BANKING CUSTOMER & MARKETING ANALYTICS: BUSINESS INSIGHTS REPORT",
        "=" * 70,
        f"Total Records Analyzed: {total:,}",
        f"Dataset Attributes: {len(df.columns)} columns (17 raw source attributes + 1 derived feature 'age_group')",
        f"Overall Campaign Subscription Rate: {sub_pct}% ({sub_cnt:,} subscriptions)",
        "-" * 70,
        "",
        "1. EXECUTIVE SUMMARY & BENCHMARK PERFORMANCE",
        f"- The dataset indicates an overall term deposit subscription rate of {sub_pct}%.",
        f"- Out of {total:,} contacted banking clients, {sub_cnt:,} agreed to open a term deposit,",
        f"  while {total - sub_cnt:,} ({100 - sub_pct:.2f}%) did not subscribe.",
        "",
        "2. HIGHEST-PERFORMING CUSTOMER DEMOGRAPHICS",
        "- By Job Category:",
        f"  * The analysis shows that 'student' accounts achieved the highest subscription rate at {bq['Q2']['table'].loc['student', 'Subscription_Rate_Pct']}%,",
        f"    followed by 'retired' clients at {bq['Q2']['table'].loc['retired', 'Subscription_Rate_Pct']}%.",
        f"  * In contrast, high-volume segments like 'blue-collar' ({bq['Q2']['table'].loc['blue-collar', 'Subscription_Rate_Pct']}%) and",
        f"    'services' ({bq['Q2']['table'].loc['services', 'Subscription_Rate_Pct']}%) exhibited below-average conversion rates.",
        "- By Age Bracket (Engineered Feature 'age_group'):",
        f"  * Clients aged 66+ exhibited the highest subscription rate at {bq['Q8']['table'].loc['66+', 'Subscription_Rate_Pct']}%, followed by the 18-25 cohort ({bq['Q8']['table'].loc['18-25', 'Subscription_Rate_Pct']}%).",
        f"  * The primary working-age segment (36-45 years) demonstrated the lowest subscription rate at {bq['Q8']['table'].loc['36-45', 'Subscription_Rate_Pct']}%.",
        "- By Education Level:",
        f"  * Clients holding tertiary education had a subscription rate of {bq['Q3']['table'].loc['tertiary', 'Subscription_Rate_Pct']}%,",
        f"    outperforming secondary ({bq['Q3']['table'].loc['secondary', 'Subscription_Rate_Pct']}%) and primary education ({bq['Q3']['table'].loc['primary', 'Subscription_Rate_Pct']}%).",
        "",
        "3. IMPACT OF DEBT & LOAN PRODUCTS",
        "- Housing Loans:",
        f"  * The dataset reveals that customers without a housing loan subscribed at {bq['Q4']['no_housing_rate']}%,",
        f"    compared to only {bq['Q4']['yes_housing_rate']}% for clients with an active housing loan.",
        "- Personal Loans:",
        f"  * Similarly, customers without personal loans subscribed at {bq['Q5']['no_loan_rate']}%,",
        f"    compared to {bq['Q5']['yes_loan_rate']}% for clients with personal loans.",
        "  * The data indicates that existing debt obligations correlate strongly with lower willingness to commit capital to term deposits.",
        "",
        "4. MARKETING COMMUNICATION & CONTACT DYNAMICS",
        "- Communication Channel:",
        f"  * Cellular communication yielded a subscription rate of {bq['Q6']['table'].loc['cellular', 'Subscription_Rate_Pct']}%,",
        f"    compared to telephone ({bq['Q6']['table'].loc['telephone', 'Subscription_Rate_Pct']}%) and unknown contact methods ({bq['Q6']['table'].loc['unknown', 'Subscription_Rate_Pct']}%).",
        "- Call Duration Profile:",
        f"  * The data shows that customers who subscribed had an average contact duration of {bq['Q10']['mean_duration_subscribed_sec']:.2f} seconds",
        f"    ({bq['Q10']['mean_duration_subscribed_min']:.2f} minutes, median: {bq['Q10']['median_duration_subscribed_sec']:.2f} seconds).",
        f"  * In comparison, clients who did not subscribe averaged {bq['Q10']['mean_duration_not_subscribed_sec']:.2f} seconds",
        f"    ({bq['Q10']['mean_duration_not_subscribed_min']:.2f} minutes, median: {bq['Q10']['median_duration_not_subscribed_sec']:.2f} seconds).",
        f"  * Calls with subscribing clients were on average {bq['Q10']['difference_duration_sec']:.1f} seconds (+{bq['Q10']['pct_longer']:.1f}%) longer.",
        "  * (Note: This documents an observed correlation; duration is an outcome of an engaged conversation rather than an exogenous cause).",
        "",
        "5. PREVIOUS CAMPAIGN EXPOSURE & HISTORICAL OUTCOMES",
        f"  * The analysis shows that when a customer's prior campaign outcome was 'success', the current subscription rate reached {bq['Q7']['success_rate']}%.",
        f"  * By contrast, clients with prior 'failure' converted at {bq['Q7']['failure_rate']}%, and those with unknown/no prior history converted at {bq['Q7']['unknown_rate']}%.",
        "  * Prior successful engagement is the single strongest indicator of subscription in this dataset.",
        "",
        "6. FINANCIAL PROFILE & BALANCE DISTRIBUTION",
        f"  * Subscribed customers (y='yes') held an average balance of EUR {bq['Q9']['mean_balance_subscribed']:,.2f} (median: EUR {bq['Q9']['median_balance_subscribed']:,.2f}).",
        f"  * Non-subscribed clients (y='no') held an average balance of EUR {bq['Q9']['mean_balance_not_subscribed']:,.2f} (median: EUR {bq['Q9']['median_balance_not_subscribed']:,.2f}).",
        f"  * Subscribed clients held on average EUR {bq['Q9']['difference_mean_balance']:,.2f} (+{bq['Q9']['pct_higher']:.1f}%) higher balances.",
        "",
        "7. SUMMARY ANSWERS TO THE 10 STRATEGIC BUSINESS QUESTIONS"
    ]

    # Dynamically format every business question with exact question text and answer summary
    for q_key, item in bq.items():
        report_lines.append(f"  [{q_key}] {item['question']}")
        report_lines.append(f"       --> {item['answer_summary']}")
        report_lines.append("")

    report_lines.extend([
        "=" * 70,
        "END OF REPORT",
        "=" * 70
    ])

    report_text = "\n".join(report_lines)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Business insights report generated and saved: {out_file}")
    return report_text


def run_full_analysis(df: pd.DataFrame, generate_report: bool = True) -> dict:
    """Execute end-to-end analytical evaluations across all modules and optionally generate insights report."""
    print("\n" + "=" * 60)
    print("RUNNING EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    demographics = analyze_demographics(df)
    financial = analyze_financial_profile(df)
    marketing = analyze_marketing(df)
    target = analyze_target(df)
    business_questions = answer_business_questions(df)

    analysis_results = {
        "demographics": demographics,
        "financial": financial,
        "marketing": marketing,
        "target": target,
        "business_questions": business_questions
    }

    if generate_report:
        generate_business_insights_report(df, analysis_results)

    print("Demographic, financial, marketing, and conversion analyses completed.")
    return analysis_results


if __name__ == "__main__":
    from data_loading import load_dataset
    from data_cleaning import clean_dataset

    raw_data = load_dataset("data/bank-full.csv")
    clean_data = clean_dataset(raw_data, save_output=False)
    results = run_full_analysis(clean_data)
    print("\nSample Business Question Answers:")
    for q_key in ["Q1", "Q2", "Q4", "Q7", "Q9", "Q10"]:
        print(f"\n{q_key}: {results['business_questions'][q_key]['question']}")
        print(f"--> {results['business_questions'][q_key]['answer_summary']}")
