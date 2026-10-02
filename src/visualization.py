"""
Data Visualization Module for Banking Customer Analytics
Generates portfolio-quality visualizations using Matplotlib and Seaborn.
"""

import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless generation
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def setup_visualization_style():
    """Configure modern, aesthetic styling for all plots."""
    sns.set_theme(style="whitegrid", palette="deep")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "axes.labelweight": "medium",
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 11,
        "figure.titlesize": 15,
        "figure.autolayout": True
    })


def save_current_plot(filename: str, output_dir: str = "outputs/charts"):
    """Helper to save, format and close current figure."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    file_path = out_dir / filename
    plt.tight_layout()
    plt.savefig(file_path, dpi=300)
    plt.close()
    print(f"Chart generated and saved: {file_path}")


# ----------------------------------------------------
# 1. Demographic & Feature Distributions
# ----------------------------------------------------

def plot_age_distribution(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """01: Customer Age Distribution with KDE and mean/median indicators."""
    plt.figure(figsize=(9, 5))
    ax = sns.histplot(df["age"], bins=35, kde=True, color="#2b5c8f", edgecolor="white", alpha=0.7)
    
    mean_age = df["age"].mean()
    median_age = df["age"].median()
    plt.axvline(mean_age, color="#d9534f", linestyle="--", linewidth=2, label=f"Mean: {mean_age:.1f} yrs")
    plt.axvline(median_age, color="#5cb85c", linestyle="-", linewidth=2, label=f"Median: {median_age:.0f} yrs")

    plt.title("01. Customer Age Distribution")
    plt.xlabel("Age (Years)")
    plt.ylabel("Number of Customers")
    plt.legend(frameon=True)
    save_current_plot("01_age_distribution.png", output_dir)


def plot_job_distribution(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """02: Customer Job Distribution."""
    plt.figure(figsize=(10, 6))
    job_counts = df["job"].value_counts().sort_values(ascending=True)
    total = len(df)

    ax = job_counts.plot(kind="barh", color="#337ab7", edgecolor="white")
    for idx, (val, name) in enumerate(zip(job_counts, job_counts.index)):
        pct = (val / total) * 100
        ax.text(val + 100, idx, f"{val:,} ({pct:.1f}%)", va="center", fontsize=9)

    plt.title("02. Customer Distribution by Job Category")
    plt.xlabel("Customer Count")
    plt.ylabel("Job Category")
    plt.xlim(0, job_counts.max() * 1.18)
    save_current_plot("02_job_distribution.png", output_dir)


def plot_balance_distribution(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """03: Bank Balance Distribution (trimmed view for clarity + full quantile annotations)."""
    fig, (ax_box, ax_hist) = plt.subplots(2, 1, figsize=(10, 6), sharex=True, gridspec_kw={"height_ratios": [0.25, 0.75]})

    # Trim visualization window to 98th percentile for visual readability without removing data
    q98 = df["balance"].quantile(0.98)
    q02 = df["balance"].quantile(0.02)
    view_data = df[(df["balance"] >= q02) & (df["balance"] <= q98)]["balance"]

    sns.boxplot(x=view_data, ax=ax_box, color="#5bc0de")
    ax_box.set(xlabel="")
    ax_box.set_title("03. Customer Account Balance Distribution (98% Range View)")

    sns.histplot(view_data, ax=ax_hist, bins=50, kde=True, color="#0275d8", edgecolor="white")
    ax_hist.set_xlabel("Account Balance (EUR)")
    ax_hist.set_ylabel("Customer Count")

    mean_bal = df["balance"].mean()
    median_bal = df["balance"].median()
    ax_hist.axvline(mean_bal, color="#d9534f", linestyle="--", linewidth=2, label=f"Overall Mean: EUR {mean_bal:,.0f}")
    ax_hist.axvline(median_bal, color="#5cb85c", linestyle="-", linewidth=2, label=f"Overall Median: EUR {median_bal:,.0f}")
    ax_hist.legend(frameon=True)

    save_current_plot("03_balance_distribution.png", output_dir)


def plot_education_distribution(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """04: Education Level Distribution."""
    plt.figure(figsize=(8, 5))
    order = ["secondary", "tertiary", "primary", "unknown"]
    counts = df["education"].value_counts().reindex(order)
    total = len(df)

    ax = sns.barplot(x=counts.index, y=counts.values, hue=counts.index, palette="Blues_r", edgecolor="black", alpha=0.85, legend=False)
    for p in ax.patches:
        val = int(p.get_height())
        pct = (val / total) * 100
        ax.annotate(f"{val:,}\n({pct:.1f}%)", (p.get_x() + p.get_width() / 2., val / 2),
                    ha="center", va="center", color="white", fontweight="bold", fontsize=10)

    plt.title("04. Customer Distribution by Education Level")
    plt.xlabel("Education Level")
    plt.ylabel("Customer Count")
    save_current_plot("04_education_distribution.png", output_dir)


def plot_housing_loan_distribution(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """05: Housing Loan Distribution."""
    plt.figure(figsize=(7, 5))
    counts = df["housing"].value_counts()
    total = len(df)

    ax = sns.barplot(x=counts.index, y=counts.values, hue=counts.index, palette=["#d9534f", "#5cb85c"], edgecolor="black", legend=False)
    for p in ax.patches:
        val = int(p.get_height())
        pct = (val / total) * 100
        ax.annotate(f"{val:,} ({pct:.1f}%)", (p.get_x() + p.get_width() / 2., val + 400),
                    ha="center", va="bottom", fontweight="bold", fontsize=11)

    plt.title("05. Housing Loan Status Distribution")
    plt.xlabel("Has Housing Loan?")
    plt.ylabel("Customer Count")
    plt.ylim(0, max(counts.values) * 1.15)
    save_current_plot("05_housing_loan_distribution.png", output_dir)


def plot_personal_loan_distribution(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """06: Personal Loan Distribution."""
    plt.figure(figsize=(7, 5))
    counts = df["loan"].value_counts()
    total = len(df)

    ax = sns.barplot(x=counts.index, y=counts.values, hue=counts.index, palette=["#5cb85c", "#d9534f"], edgecolor="black", legend=False)
    for p in ax.patches:
        val = int(p.get_height())
        pct = (val / total) * 100
        ax.annotate(f"{val:,} ({pct:.1f}%)", (p.get_x() + p.get_width() / 2., val + 500),
                    ha="center", va="bottom", fontweight="bold", fontsize=11)

    plt.title("06. Personal Loan Status Distribution")
    plt.xlabel("Has Personal Loan?")
    plt.ylabel("Customer Count")
    plt.ylim(0, max(counts.values) * 1.15)
    save_current_plot("06_personal_loan_distribution.png", output_dir)


def plot_subscription_distribution(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """07: Target Variable (Term Deposit Subscription) Distribution."""
    plt.figure(figsize=(7, 5))
    counts = df["y"].value_counts()
    total = len(df)

    colors = ["#e74c3c", "#2ecc71"]
    ax = sns.barplot(x=counts.index, y=counts.values, hue=counts.index, palette=colors, edgecolor="black", legend=False)
    for p in ax.patches:
        val = int(p.get_height())
        pct = (val / total) * 100
        ax.annotate(f"{val:,}\n({pct:.1f}%)", (p.get_x() + p.get_width() / 2., val + 600),
                    ha="center", va="bottom", fontweight="bold", fontsize=11)

    plt.title("07. Term Deposit Subscription Distribution (Target Variable)")
    plt.xlabel("Subscribed to Term Deposit (y)")
    plt.ylabel("Customer Count")
    plt.ylim(0, max(counts.values) * 1.18)
    save_current_plot("07_subscription_distribution.png", output_dir)


# ----------------------------------------------------
# 2. Conversion / Subscription Rate Analyses
# ----------------------------------------------------

def plot_subscription_by_age_group(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """08: Subscription Rate by Age Group."""
    plt.figure(figsize=(9, 5))
    group_stats = df.groupby("age_group", observed=False)["y"].agg(
        Rate=lambda s: (s == "yes").mean() * 100,
        Total="count"
    )

    ax = sns.barplot(x=group_stats.index, y=group_stats["Rate"], hue=group_stats.index, palette="crest", edgecolor="black", legend=False)
    for idx, p in enumerate(ax.patches):
        rate = p.get_height()
        n = group_stats["Total"].iloc[idx]
        ax.annotate(f"{rate:.1f}%\n(n={n:,})", (p.get_x() + p.get_width() / 2., rate + 0.8),
                    ha="center", va="bottom", fontsize=10, fontweight="bold")

    overall_rate = (df["y"] == "yes").mean() * 100
    plt.axhline(overall_rate, color="red", linestyle="--", linewidth=1.5, label=f"Overall Avg ({overall_rate:.1f}%)")

    plt.title("08. Term Deposit Subscription Rate by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Subscription Rate (%)")
    plt.ylim(0, max(group_stats["Rate"]) * 1.25)
    plt.legend(loc="upper left")
    save_current_plot("08_subscription_by_age_group.png", output_dir)


def plot_subscription_by_job(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """09: Subscription Rate by Job Category."""
    plt.figure(figsize=(10, 6))
    job_stats = df.groupby("job")["y"].agg(
        Rate=lambda s: (s == "yes").mean() * 100,
        Total="count"
    ).sort_values(by="Rate", ascending=True)

    ax = job_stats["Rate"].plot(kind="barh", color="#1f77b4", edgecolor="black", alpha=0.85)
    for idx, (rate, (jname, row)) in enumerate(zip(job_stats["Rate"], job_stats.iterrows())):
        ax.text(rate + 0.5, idx, f"{rate:.1f}% (n={int(row['Total']):,})", va="center", fontsize=9)

    overall_rate = (df["y"] == "yes").mean() * 100
    plt.axvline(overall_rate, color="red", linestyle="--", linewidth=1.5, label=f"Overall Avg ({overall_rate:.1f}%)")

    plt.title("09. Term Deposit Subscription Rate by Job Role")
    plt.xlabel("Subscription Rate (%)")
    plt.ylabel("Job Category")
    plt.xlim(0, job_stats["Rate"].max() * 1.35)
    plt.legend(loc="lower right")
    save_current_plot("09_subscription_by_job.png", output_dir)


def plot_subscription_by_education(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """10: Subscription Rate by Education Level."""
    plt.figure(figsize=(8, 5))
    edu_stats = df.groupby("education")["y"].agg(
        Rate=lambda s: (s == "yes").mean() * 100,
        Total="count"
    ).sort_values(by="Rate", ascending=False)

    ax = sns.barplot(x=edu_stats.index, y=edu_stats["Rate"], hue=edu_stats.index, palette="Blues_r", edgecolor="black", legend=False)
    for idx, p in enumerate(ax.patches):
        rate = p.get_height()
        n = edu_stats["Total"].iloc[idx]
        ax.annotate(f"{rate:.1f}%\n(n={n:,})", (p.get_x() + p.get_width() / 2., rate + 0.5),
                    ha="center", va="bottom", fontsize=10, fontweight="bold")

    overall_rate = (df["y"] == "yes").mean() * 100
    plt.axhline(overall_rate, color="red", linestyle="--", linewidth=1.5, label=f"Overall Avg ({overall_rate:.1f}%)")

    plt.title("10. Term Deposit Subscription Rate by Education Level")
    plt.xlabel("Education Level")
    plt.ylabel("Subscription Rate (%)")
    plt.ylim(0, max(edu_stats["Rate"]) * 1.25)
    plt.legend(loc="upper right")
    save_current_plot("10_subscription_by_education.png", output_dir)


def plot_subscription_by_contact(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """11: Subscription Rate by Contact Communication Type."""
    plt.figure(figsize=(7, 5))
    contact_stats = df.groupby("contact")["y"].agg(
        Rate=lambda s: (s == "yes").mean() * 100,
        Total="count"
    ).sort_values(by="Rate", ascending=False)

    ax = sns.barplot(x=contact_stats.index, y=contact_stats["Rate"], hue=contact_stats.index, palette="viridis", edgecolor="black", legend=False)
    for idx, p in enumerate(ax.patches):
        rate = p.get_height()
        n = contact_stats["Total"].iloc[idx]
        ax.annotate(f"{rate:.1f}%\n(n={n:,})", (p.get_x() + p.get_width() / 2., rate + 0.4),
                    ha="center", va="bottom", fontsize=10, fontweight="bold")

    overall_rate = (df["y"] == "yes").mean() * 100
    plt.axhline(overall_rate, color="red", linestyle="--", linewidth=1.5, label=f"Overall Avg ({overall_rate:.1f}%)")

    plt.title("11. Subscription Rate by Contact Communication Channel")
    plt.xlabel("Contact Channel")
    plt.ylabel("Subscription Rate (%)")
    plt.ylim(0, max(contact_stats["Rate"]) * 1.3)
    plt.legend(loc="upper right")
    save_current_plot("11_subscription_by_contact.png", output_dir)


def plot_subscription_by_previous_outcome(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """12: Subscription Rate by Previous Campaign Outcome."""
    plt.figure(figsize=(8, 5))
    pout_stats = df.groupby("poutcome")["y"].agg(
        Rate=lambda s: (s == "yes").mean() * 100,
        Total="count"
    ).sort_values(by="Rate", ascending=False)

    colors = ["#27ae60", "#f39c12", "#e74c3c", "#95a5a6"]
    ax = sns.barplot(x=pout_stats.index, y=pout_stats["Rate"], hue=pout_stats.index, palette=colors, edgecolor="black", legend=False)
    for idx, p in enumerate(ax.patches):
        rate = p.get_height()
        n = pout_stats["Total"].iloc[idx]
        ax.annotate(f"{rate:.1f}%\n(n={n:,})", (p.get_x() + p.get_width() / 2., rate + 1.5),
                    ha="center", va="bottom", fontsize=10, fontweight="bold")

    overall_rate = (df["y"] == "yes").mean() * 100
    plt.axhline(overall_rate, color="black", linestyle="--", linewidth=1.5, label=f"Overall Avg ({overall_rate:.1f}%)")

    plt.title("12. Subscription Rate by Previous Marketing Campaign Outcome")
    plt.xlabel("Previous Campaign Outcome (poutcome)")
    plt.ylabel("Subscription Rate (%)")
    plt.ylim(0, max(pout_stats["Rate"]) * 1.25)
    plt.legend(loc="upper right")
    save_current_plot("12_subscription_by_previous_outcome.png", output_dir)


# ----------------------------------------------------
# 3. Financial and Behavioral Comparisons
# ----------------------------------------------------

def plot_balance_vs_subscription(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """13: Account Balance vs. Term Deposit Subscription."""
    fig, (ax_box, ax_bar) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1, 1]})

    # Left: Boxplot clipped to 95th percentile to avoid visual skew from extreme outliers
    clip_val = df["balance"].quantile(0.95)
    sns.boxplot(data=df[df["balance"] <= clip_val], x="y", y="balance", hue="y", palette=["#e74c3c", "#2ecc71"], ax=ax_box, legend=False)
    ax_box.set_title("Balance Distribution by Subscription (Clipped to 95th %ile)")
    ax_box.set_xlabel("Subscribed (y)")
    ax_box.set_ylabel("Balance (EUR)")

    # Right: Barplot of Mean and Median Balance
    agg_bal = df.groupby("y")["balance"].agg(["mean", "median"]).reset_index()
    agg_melt = agg_bal.melt(id_vars="y", value_vars=["mean", "median"], var_name="Metric", value_name="Balance")
    
    sns.barplot(data=agg_melt, x="y", y="Balance", hue="Metric", palette="Blues_d", ax=ax_bar)
    for p in ax_bar.patches:
        val = p.get_height()
        if not np.isnan(val) and val > 0:
            ax_bar.annotate(f"EUR {val:,.0f}", (p.get_x() + p.get_width() / 2., val + 25),
                            ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax_bar.set_title("Mean & Median Balance by Subscription")
    ax_bar.set_xlabel("Subscribed (y)")
    ax_bar.set_ylabel("Balance (EUR)")
    ax_bar.set_ylim(0, agg_melt["Balance"].max() * 1.2)

    save_current_plot("13_balance_vs_subscription.png", output_dir)


def plot_call_duration_vs_subscription(df: pd.DataFrame, output_dir: str = "outputs/charts"):
    """14: Call Duration vs. Subscription."""
    fig, (ax_kde, ax_bar) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1.1, 0.9]})

    # Left: KDE plot of duration in minutes (clipped to 25 mins)
    df_temp = df.copy()
    df_temp["duration_min"] = df_temp["duration"] / 60
    
    sns.kdeplot(data=df_temp[df_temp["duration_min"] <= 25], x="duration_min", hue="y",
                common_norm=False, fill=True, palette=["#e74c3c", "#2ecc71"], alpha=0.35, ax=ax_kde)
    ax_kde.set_title("Call Duration Density (Minutes)")
    ax_kde.set_xlabel("Duration (Minutes)")
    ax_kde.set_ylabel("Density")

    # Right: Average duration comparison
    agg_dur = df_temp.groupby("y")["duration_min"].agg(["mean", "median"]).reset_index()
    agg_melt = agg_dur.melt(id_vars="y", value_vars=["mean", "median"], var_name="Metric", value_name="Minutes")
    
    sns.barplot(data=agg_melt, x="y", y="Minutes", hue="Metric", palette="Greens_d", ax=ax_bar)
    for p in ax_bar.patches:
        val = p.get_height()
        if not np.isnan(val) and val > 0:
            ax_bar.annotate(f"{val:.1f} m", (p.get_x() + p.get_width() / 2., val + 0.2),
                            ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax_bar.set_title("Average & Median Call Duration")
    ax_bar.set_xlabel("Subscribed (y)")
    ax_bar.set_ylabel("Duration (Minutes)")
    ax_bar.set_ylim(0, agg_dur["mean"].max() * 1.25)

    save_current_plot("14_call_duration_vs_subscription.png", output_dir)


def generate_all_visualizations(df: pd.DataFrame, output_dir: str = "outputs/charts") -> list:
    """Generate and export all 14 required portfolio charts."""
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    setup_visualization_style()

    chart_functions = [
        ("01_age_distribution.png", plot_age_distribution),
        ("02_job_distribution.png", plot_job_distribution),
        ("03_balance_distribution.png", plot_balance_distribution),
        ("04_education_distribution.png", plot_education_distribution),
        ("05_housing_loan_distribution.png", plot_housing_loan_distribution),
        ("06_personal_loan_distribution.png", plot_personal_loan_distribution),
        ("07_subscription_distribution.png", plot_subscription_distribution),
        ("08_subscription_by_age_group.png", plot_subscription_by_age_group),
        ("09_subscription_by_job.png", plot_subscription_by_job),
        ("10_subscription_by_education.png", plot_subscription_by_education),
        ("11_subscription_by_contact.png", plot_subscription_by_contact),
        ("12_subscription_by_previous_outcome.png", plot_subscription_by_previous_outcome),
        ("13_balance_vs_subscription.png", plot_balance_vs_subscription),
        ("14_call_duration_vs_subscription.png", plot_call_duration_vs_subscription),
    ]

    generated_charts = []
    for filename, func in chart_functions:
        func(df, output_dir=output_dir)
        generated_charts.append(filename)

    print(f"\nAll {len(generated_charts)} charts successfully generated and saved to '{output_dir}'.")
    return generated_charts


if __name__ == "__main__":
    from data_loading import load_dataset
    from data_cleaning import clean_dataset

    raw_df = load_dataset("data/bank-full.csv")
    cleaned_df = clean_dataset(raw_df, save_output=False)
    generate_all_visualizations(cleaned_df)
