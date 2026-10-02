# Banking Customer & Marketing Analytics

A portfolio-grade exploratory data analysis and customer intelligence pipeline built with Python, Pandas, NumPy, Matplotlib, and Seaborn. This project explores customer demographics, financial behaviors, and marketing touchpoints to uncover data-driven insights into term deposit subscription outcomes.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Dataset](#4-dataset)
5. [Technologies Used](#5-technologies-used)
6. [Dataset Features / Data Dictionary](#6-dataset-features--data-dictionary)
7. [Data Cleaning](#7-data-cleaning)
8. [Exploratory Data Analysis](#8-exploratory-data-analysis)
9. [Business Questions](#9-business-questions)
10. [Key Insights](#10-key-insights)
11. [Project Structure](#11-project-structure)
12. [How to Run](#12-how-to-run)
13. [Future Improvements](#13-future-improvements)

---

## 1. Project Overview

In the retail banking industry, direct marketing campaigns are essential for promoting financial products such as fixed-term deposits. However, broad untargeted telemarketing campaigns incur substantial operational costs, customer fatigue, and low conversion rates. 

This project delivers an end-to-end data analytics pipeline focused on the **UCI Bank Marketing dataset** (comprising 45,211 customer records). It systematically ingests, validates, cleans, and explores customer demographic attributes, financial health indicators, and campaign contact histories to identify high-converting customer segments and operational efficiencies without relying on black-box machine learning models.

---

## 2. Problem Statement

A Portuguese retail banking institution conducted direct marketing campaigns (primarily phone calls) to sell term deposits. The bank faces two core challenges:

1. **Low Baseline Conversion**: Across 45,211 recorded client interactions, the baseline subscription rate is approximately 11.7%, meaning over 88% of calls do not result in a sale.
2. **Resource Inefficiency**: Marketing representatives spend valuable call time reaching out to customer groups with high debt burdens or low willingness to invest, rather than focusing on receptive customer profiles and effective communication channels.

---

## 3. Objectives

- **Robust Data Pipeline**: Ingest and validate the semicolon-delimited dataset, handling quotation formatting anomalies automatically.
- **Data Integrity & Preprocessing**: Clean anomalies, verify numeric ranges, audit missing/"unknown" values, and preserve legitimate financial patterns (e.g., overdraft accounts).
- **Comprehensive Demographic & Financial Profiling**: Segment clients by age brackets, occupation, education, and net account balance.
- **Campaign Touchpoint Evaluation**: Evaluate the relationship between conversion rates and marketing channels (cellular vs. telephone), call duration, and prior campaign history.
- **Empirical Business Answers**: Programmatically answer 10 fundamental business questions to inform marketing and customer acquisition strategies.
- **Portfolio-Quality Visualizations**: Generate 14 production-ready, publication-grade analytical charts saved directly to disk.

---

## 4. Dataset

- **Source**: UCI Machine Learning Repository — Bank Marketing Dataset (Moro et al., 2014).
- **Scale**: 45,211 customer interaction records across 17 attributes.
- **File Location**: `data/bank-full.csv`
- **Format**: Semicolon-separated (`sep=";"`) with double-quoted string fields.

---

## 5. Technologies Used

- **Python 3**: Core programming language.
- **Pandas**: High-performance data manipulation, filtering, aggregation, and grouping.
- **NumPy**: Numerical operations, quantile estimations, and vectorization.
- **Matplotlib**: Low-level charting engine, layout control, and file exports.
- **Seaborn**: Statistical data visualizations, modern themes, and categorical distributions.
- **Pathlib / OS**: Robust, cross-platform file path resolution.

---

## 6. Dataset Features / Data Dictionary

Every attribute present in the dataset is defined below:

| # | Column Name | Data Type | Description | Values / Range |
|---|-------------|-----------|-------------|----------------|
| 1 | `age` | Numeric (int) | Age of the customer in years | 18 to 95 |
| 2 | `job` | Categorical | Type of occupation | admin., blue-collar, entrepreneur, housemaid, management, retired, self-employed, services, student, technician, unemployed, unknown |
| 3 | `marital` | Categorical | Marital status of the customer | married, single, divorced (includes widowed) |
| 4 | `education` | Categorical | Highest educational attainment | primary, secondary, tertiary, unknown |
| 5 | `default` | Binary (yes/no) | Has credit currently in default? | no, yes |
| 6 | `balance` | Numeric (int) | Average yearly bank account balance in EUR | -8,019 to 102,127 |
| 7 | `housing` | Binary (yes/no) | Has an active housing mortgage loan? | no, yes |
| 8 | `loan` | Binary (yes/no) | Has an active personal loan? | no, yes |
| 9 | `contact` | Categorical | Communication channel used for contact | cellular, telephone, unknown |
| 10 | `day` | Numeric (int) | Last contact day of the month | 1 to 31 |
| 11 | `month` | Categorical | Last contact month of the year | jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec |
| 12 | `duration` | Numeric (int) | Duration of the last phone call in seconds | 0 to 4,918 seconds |
| 13 | `campaign` | Numeric (int) | Total number of contacts performed during this campaign for this client | 1 to 63 |
| 14 | `pdays` | Numeric (int) | Days elapsed after previous campaign contact (-1 means not previously contacted) | -1 to 871 |
| 15 | `previous` | Numeric (int) | Number of contacts performed prior to this campaign for this client | 0 to 275 |
| 16 | `poutcome` | Categorical | Outcome of the previous marketing campaign | failure, nonexistent/other, success, unknown |
| 17 | `y` | Binary (yes/no) | **Target Variable**: Indicates whether the customer subscribed to a term deposit | no, yes |
| 18 | `age_group` | Categorical (Derived) | **Derived Feature**: Generational age cohort engineered during data cleaning | 18-25, 26-35, 36-45, 46-55, 56-65, 66+ |

> [!NOTE]
> **Source vs. Cleaned Dataset Dimensions**: The raw source dataset contains **17 columns**. During preprocessing, a single derived feature, `age_group`, is engineered to facilitate demographic cohort analysis, resulting in **18 columns** in `outputs/cleaned_data/bank_cleaned.csv`.

---

## 7. Data Cleaning

The preprocessing routines in `src/data_cleaning.py` adhere to strict financial data integrity rules:

1. **Non-Destructive Processing**: The raw dataset is preserved; all transformations operate on in-memory deep copies.
2. **Quotation & Delimiter Normalization**: Automatically unwraps outer-line quotations and normalizes column headers.
3. **Deduplication**: Audited the entire dataset for duplicate records (0 duplicate rows found).
4. **Data Type Casting**: Enforced appropriate integer types on `age`, `balance`, `day`, `duration`, `campaign`, `pdays`, and `previous`.
5. **Legitimate Negative Balance Preservation**: Retained 3,766 accounts (8.33%) with negative balances, as overdraft facilities are valid bank account states and removing them would bias liquidity analyses.
6. **Informative "Unknown" Handling**: Retained categorical "unknown" values in `job` (0.64%), `education` (4.11%), `contact` (28.80%), and `poutcome` (81.75%) rather than imputing mode values, preserving true survey non-response dynamics.
7. **Feature Engineering (18th Column)**: Engineered an 18th column, `age_group`, binned into 6 demographic cohorts (`18-25`, `26-35`, `36-45`, `46-55`, `56-65`, `66+`). This accounts for the transition from 17 raw columns to 18 cleaned columns.
8. **Export**: Exported the structured clean data to `outputs/cleaned_data/bank_cleaned.csv`.

---

## 8. Exploratory Data Analysis

### A. Customer Demographics
- **Age**: Average customer age is 40.9 years (median: 39 years). The bulk of the customer base falls between 26 and 55 years old.
- **Occupation**: The top three occupations are Blue-collar (21.5%), Management (20.9%), and Technician (16.8%). Students (2.1%) and Retired individuals (5.0%) represent small demographic slices.
- **Education**: 51.3% hold secondary education, 29.4% hold tertiary education, and 15.2% primary education.

### B. Financial Profile
- **Account Balance**: Highly right-skewed with a mean of EUR 1,362.27 and median of EUR 448.00. 8.33% of accounts operate in overdraft status (negative balance).
- **Debt Burden**: 55.6% of clients hold a housing mortgage loan, and 16.0% have personal loans. Only 1.8% of clients have credit defaults on record.

### C. Campaign Dynamics
- **Contact Channels**: 64.8% were reached via mobile cellular, 6.4% via landline telephone, and 28.8% had an unknown contact method.
- **Call Duration**: Averages 258.2 seconds (~4.3 minutes, median: 180 seconds).
- **Prior History**: 81.7% of clients (`pdays = -1`) were newly targeted prospects with no recorded history from prior marketing campaigns.

---

## 9. Business Questions

All 10 core business questions are programmatically computed by `src/analysis.py`:

| # | Business Question | Programmatic Finding |
|---|-------------------|----------------------|
| **Q1** | What percentage of customers subscribed to a term deposit? | **11.70%** (5,289 of 45,211 customers subscribed). |
| **Q2** | Which job categories have the highest subscription rate? | **Students (28.68%)** and **Retired (22.79%)** had the highest conversion rates, compared to Blue-collar workers at 7.27%. |
| **Q3** | Which education groups have the highest subscription rate? | **Tertiary education (15.01%)** had the highest rate, followed by Secondary (10.56%) and Primary (8.63%). |
| **Q4** | How does housing loan status relate to subscription? | Clients **without a housing loan subscribed at 16.70%**, more than double those with a housing loan (7.70%). |
| **Q5** | How does personal loan status relate to subscription? | Clients **without personal loans subscribed at 12.66%**, compared to only 6.68% for those with personal loans. |
| **Q6** | Which contact method has the highest subscription rate? | **Cellular contact achieved 14.92%**, Telephone reached 13.42%, while Unknown contact was lowest at 4.07%. |
| **Q7** | How does previous campaign outcome relate to the current outcome? | Clients with prior **"success" converted at 64.73%**, versus 12.61% for "failure" and 9.16% for "unknown". |
| **Q8** | Which age group has the highest subscription rate? | The **66+ age group led at 42.61%**, followed by the **18-25 cohort at 23.95%**. Mid-career clients (36-45) were lowest at 9.39%. |
| **Q9** | What is the average balance of customers who subscribed vs. those who did not? | Subscribed clients (y="yes") held an average balance of **EUR 1,804.27** (median: EUR 733.00), versus **EUR 1,303.71** (median: EUR 417.00) for non-subscribers (y="no"). Subscribed customers held on average **EUR 500.56 (+38.4%) higher** balances. |
| **Q10** | How does call duration relate to subscription? | Subscribed customers (y="yes") had an average call duration of **537.29 seconds / 8.95 mins** (median: 426.00s / 7.10 mins) versus **221.18 seconds / 3.69 mins** (median: 164.00s / 2.73 mins) for non-subscribers (y="no"). Calls resulting in subscription were on average **316.1s (+142.9%) longer**. |

---

## 10. Key Insights

1. **Prior Relationship is the Strongest Indicator**: Clients who had a positive outcome ("success") in a preceding marketing initiative subscribed at **64.73%**—over five times the baseline rate. Nurturing existing happy customers yields the highest return on campaign spend.
2. **Debt Constrains Liquidity for Term Deposits**: Clients burdened with housing loans (7.70% conversion) or personal loans (6.68% conversion) converted at approximately half the rate of debt-free clients (16.70% and 12.66% respectively). Marketing fixed savings to clients with active amortizing debt creates friction.
3. **The "Bimodal" Age Opportunity**: Young adults (`18-25` at 23.94%) and seniors (`66+` at 42.46%) subscribe at rates far exceeding mid-career individuals (`36-45` at 9.05%). Seniors seek capital preservation and stable deposit interest, while young savers start building long-term assets.
4. **Channel Matters**: Unknown/missing contact channels yield a dismal 4.07% conversion. Transitioning prospects to direct mobile cellular contact improves responsiveness to 14.92%.

---

## 11. Project Structure

```
Banking-Customer-Analytics/
│
├── data/
│   └── bank-full.csv                  # Raw UCI Bank Marketing dataset
│
├── src/
│   ├── __init__.py                    # Package initialization
│   ├── data_loading.py                # CSV stream unrolling, inspection, and schema validation
│   ├── data_cleaning.py               # Preprocessing, type conversions, domain checks, CSV export
│   ├── analysis.py                    # Demographic, financial, marketing, and business question analytics
│   └── visualization.py               # 14 publication-quality visual charting scripts
│
├── outputs/
│   ├── cleaned_data/
│   │   └── bank_cleaned.csv           # Cleaned dataset (with engineered age_group)
│   ├── charts/                        # 14 High-resolution (300 DPI) figures
│   │   ├── 01_age_distribution.png
│   │   ├── 02_job_distribution.png
│   │   ├── 03_balance_distribution.png
│   │   ├── 04_education_distribution.png
│   │   ├── 05_housing_loan_distribution.png
│   │   ├── 06_personal_loan_distribution.png
│   │   ├── 07_subscription_distribution.png
│   │   ├── 08_subscription_by_age_group.png
│   │   ├── 09_subscription_by_job.png
│   │   ├── 10_subscription_by_education.png
│   │   ├── 11_subscription_by_contact.png
│   │   ├── 12_subscription_by_previous_outcome.png
│   │   ├── 13_balance_vs_subscription.png
│   │   └── 14_call_duration_vs_subscription.png
│   ├── reports/
│   │   └── business_insights.txt      # Automatically generated text insights summary
│   └── powerbi/                       # Power BI portfolio kit
│       ├── bank_powerbi.csv           # Power BI-ready dataset (45,211 rows × 18 columns)
│       ├── data_dictionary.csv        # Comprehensive 18-column business data dictionary
│       ├── POWER_BI_DASHBOARD_GUIDE.md# Complete 3-page dashboard & DAX specification
│       ├── README_POWERBI.md          # Step-by-step setup, visual guide & screenshot export
│       └── POWER_BI_CHECKLIST.md      # Development & QA tracking checklist
│
├── main.py                            # Pipeline runner coordinating sections [1] through [9]
├── requirements.txt                   # Minimal Python package dependencies
├── README.md                          # Comprehensive documentation
└── .gitignore                         # Python .gitignore configuration
```

---

## 12. How to Run

### Step 1: Clone or Open Project
Ensure your terminal working directory is the project root:
```bash
cd Banking-Customer-Analytics
```

### Step 2: Install Dependencies
Create and activate an isolated virtual environment, then install requirements:
```bash
# Optional: create virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate  # On macOS/Linux

pip install -r requirements.txt
```

### Step 3: Run Analytics Pipeline
Execute the end-to-end driver:
```bash
python main.py
```

The pipeline executes through sections `[1]` to `[9]`, outputting logs to the console and generating all artifacts in `outputs/`.

---

## 13. Future Improvements

- **Interactive Dashboarding**: Build an interactive Streamlit or Power BI dashboard to enable non-technical stakeholders to slice metrics dynamically.
- **RFM / Customer Lifetime Value Modeling**: Expand demographic segmentation into Recency, Frequency, and Monetary (RFM) scorecards.
- **A/B Testing Framework**: Implement statistical hypothesis testing (Chi-Square test of independence, Mann-Whitney U test) to establish confidence intervals for conversion uplifts across communication channels.
- **Multi-Touch Attribution**: Analyze the impact of contact cadence (`campaign` frequency vs. `pdays` lag) to identify optimal contact fatigue thresholds.
