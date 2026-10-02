# Power BI Dashboard Specification & Implementation Guide
## Banking Customer & Marketing Analytics

**Project Location**: `C:\projects\Banking-Customer-Analytics`  
**Data Source**: `outputs/powerbi/bank_powerbi.csv` (45,211 rows × 18 columns)  
**Target Audience**: Executive Leadership, Hiring Managers, Portfolio Reviewers, Academic Viva Examiners  

---

## 1. Executive Summary & Architecture

This guide provides the complete blueprint for constructing an enterprise-grade, portfolio-ready 3-page interactive Power BI dashboard. The underlying data represents 45,211 retail banking customer interactions from the UCI Bank Marketing campaign, tracking term deposit subscription decisions alongside demographic, financial, and campaign touchpoint attributes.

### Single-Table Data Model
Because this project analyzes customer interactions at the interaction/campaign level, the data architecture utilizes a **clean, single-table flat model** (`bank_powerbi`). 
- **No artificial star-schema fragmentation** or unnecessary 1-to-1 dimension relationships.
- All analytical measures are organized in a dedicated DAX Measures table or directly within `bank_powerbi`.
- High query performance and instant slicer cross-filtering across all 3 pages.

---

## 2. Power BI Data Types & Field Formatting

When importing `bank_powerbi.csv` via Power Query, ensure that column data types are configured as follows:

| Column Name | Power BI Data Type | Format String | Description / Categorical Role |
| :--- | :--- | :--- | :--- |
| `age` | Whole Number (Int64) | `0` | Customer age in years (18 - 95) |
| `job` | Text | — | Occupation category (12 categories) |
| `marital` | Text | — | Marital status (married, single, divorced) |
| `education` | Text | — | Education level (primary, secondary, tertiary, unknown) |
| `default` | Text | — | Credit default indicator (no, yes) |
| `balance` | Whole Number (Int64) | `€#,##0;-(€#,##0)` | Yearly bank balance in EUR (includes overdrafts) |
| `housing` | Text | — | Housing loan status (no, yes) |
| `loan` | Text | — | Personal loan status (no, yes) |
| `contact` | Text | — | Outreach channel (cellular, telephone, unknown) |
| `day` | Whole Number (Int64) | `0` | Last contact day of month (1 - 31) |
| `month` | Text | — | Last contact month (jan - dec) |
| `duration` | Whole Number (Int64) | `#,##0` | Call duration in seconds |
| `campaign` | Whole Number (Int64) | `0` | Contacts in current campaign |
| `pdays` | Whole Number (Int64) | `0` | Days elapsed after prior campaign (-1 = none) |
| `previous` | Whole Number (Int64) | `0` | Contacts in previous campaigns |
| `poutcome` | Text | — | Prior campaign outcome (failure, other, success, unknown) |
| `y` | Text | — | **Target variable** (no, yes) — **Must remain Text / Categorical** |
| `age_group` | Text | — | **Derived 18th column** (18-25, 26-35, 36-45, 46-55, 56-65, 66+) |

> [!IMPORTANT]
> **Field Role**: Keep `y` formatted strictly as a **Text/Categorical** field. Never convert `y` to numeric binary during load; use dynamic DAX measures (`CALCULATE`, `COUNTROWS`) to compute subscription counts and rates.

---

## 3. Core DAX Measures Specification

Create a dedicated measure table or add the following DAX calculations directly to the model. Every measure evaluates dynamically against active slicers and page filters.

### 1. Total Customers
```dax
Total Customers = 
COUNTROWS('bank_powerbi')
```
*Format*: `#,##0`

### 2. Subscribed Customers
```dax
Subscribed Customers = 
CALCULATE(
    COUNTROWS('bank_powerbi'),
    'bank_powerbi'[y] = "yes"
)
```
*Format*: `#,##0`

### 3. Subscription Rate
```dax
Subscription Rate = 
DIVIDE(
    [Subscribed Customers],
    [Total Customers],
    0
)
```
*Format*: `0.0%` (or `0.00%`)

### 4. Average Balance
```dax
Average Balance = 
AVERAGE('bank_powerbi'[balance])
```
*Format*: `€#,##0`

### 5. Median Balance
```dax
Median Balance = 
MEDIAN('bank_powerbi'[balance])
```
*Format*: `€#,##0`

### 6. Average Call Duration (Seconds & Minutes)
```dax
Average Call Duration = 
AVERAGE('bank_powerbi'[duration])
```
*Format*: `#,##0.0` sec

```dax
Average Call Duration (Minutes) = 
DIVIDE(
    [Average Call Duration],
    60,
    0
)
```
*Format*: `0.0` mins

### 7. Average Campaign Contacts
```dax
Average Campaign Contacts = 
AVERAGE('bank_powerbi'[campaign])
```
*Format*: `0.0`

### 8. Previously Contacted Customers
```dax
Previously Contacted Customers = 
CALCULATE(
    COUNTROWS('bank_powerbi'),
    'bank_powerbi'[pdays] <> -1
)
```
*Format*: `#,##0`

### 9. Previous Campaign Success Rate
```dax
Previous Campaign Success Rate = 
VAR SuccessCount = 
    CALCULATE(
        COUNTROWS('bank_powerbi'),
        'bank_powerbi'[poutcome] = "success"
    )
RETURN
    DIVIDE(
        SuccessCount,
        [Total Customers],
        0
    )
```
*Format*: `0.0%`

### 10. Loan Portfolio Measures
```dax
Housing Loan Customers = 
CALCULATE(
    COUNTROWS('bank_powerbi'),
    'bank_powerbi'[housing] = "yes"
)
```
*Format*: `#,##0`

```dax
Personal Loan Customers = 
CALCULATE(
    COUNTROWS('bank_powerbi'),
    'bank_powerbi'[loan] = "yes"
)
```
*Format*: `#,##0`

### 11. Comparative Split Measures (Subscribed vs. Non-Subscribed)
```dax
Avg Balance Subscribed = 
CALCULATE(
    AVERAGE('bank_powerbi'[balance]),
    'bank_powerbi'[y] = "yes"
)
```

```dax
Avg Balance Not Subscribed = 
CALCULATE(
    AVERAGE('bank_powerbi'[balance]),
    'bank_powerbi'[y] = "no"
)
```

```dax
Avg Duration Subscribed (Minutes) = 
CALCULATE(
    DIVIDE(AVERAGE('bank_powerbi'[duration]), 60, 0),
    'bank_powerbi'[y] = "yes"
)
```

```dax
Avg Duration Not Subscribed (Minutes) = 
CALCULATE(
    DIVIDE(AVERAGE('bank_powerbi'[duration]), 60, 0),
    'bank_powerbi'[y] = "no"
)
```

---

## 4. 3-Page Dashboard Blueprint

### PAGE 1 — EXECUTIVE OVERVIEW

- **Page Name**: `Executive Overview`
- **Canvas Size**: 16:9 Standard (`1280 × 720` px)
- **Header Banner**:
  - **Title**: `Banking Customer & Marketing Analytics`
  - **Subtitle**: `Customer Profile, Financial Behavior & Term Deposit Campaign Analysis`

#### Top KPI Cards (Horizontal Layout across top)
1. **Total Customers**: Card visual displaying `[Total Customers]` (`45,211`)
2. **Subscribed Customers**: Card visual displaying `[Subscribed Customers]` (`5,289`)
3. **Subscription Rate**: Card visual displaying `[Subscription Rate]` (`11.7%`)
4. **Average Balance**: Card visual displaying `[Average Balance]` (`€1,362`)
5. **Average Call Duration**: Card visual displaying `[Average Call Duration (Minutes)]` (`4.3 mins`)

#### Main Analytical Visuals
1. **Donut Chart — Campaign Subscription Outcome**:
   - *Legend*: `y` (`yes`, `no`)
   - *Values*: `[Total Customers]`
   - *Colors*: Subscribed = `#059669` (Emerald), Not Subscribed = `#DC2626` (Crimson)
   - *Detail labels*: Category and percent of total (`11.7%` vs `88.3%`)

2. **Clustered Column Chart — Customer Volume by Age Group**:
   - *X-Axis*: `age_group` (Sorted by age order: `18-25`, `26-35`, `36-45`, `46-55`, `56-65`, `66+`)
   - *Y-Axis*: `[Total Customers]`
   - *Data Labels*: On (`#,##0`)

3. **Clustered Bar Chart — Customer Volume by Job Category**:
   - *Y-Axis*: `job` (Sorted descending by customer count)
   - *X-Axis*: `[Total Customers]`
   - *Data Labels*: On

4. **Clustered Column Chart — Subscription Rate by Age Group**:
   - *X-Axis*: `age_group`
   - *Y-Axis*: `[Subscription Rate]`
   - *Constant Line*: Overall baseline `11.7%` dashed line in `#1E3A8A`
   - *Data Labels*: On (`0.0%`)

5. **Clustered Bar Chart — Subscription Rate by Job Category**:
   - *Y-Axis*: `job` (Sorted descending by `[Subscription Rate]`)
   - *X-Axis*: `[Subscription Rate]`
   - *Constant Line*: Overall baseline `11.7%` dashed line
   - *Data Labels*: On (`0.0%`)

#### Interactive Slicers Panel (Left or Top Filter Bar)
- `Job` (Dropdown or tile list)
- `Education` (Horizontal tiles)
- `Marital Status` (Dropdown)
- `Housing Loan` (`yes`/`no` buttons)
- `Personal Loan` (`yes`/`no` buttons)
- `Contact Method` (Dropdown)
- `Age Group` (Horizontal tiles)

---

### PAGE 2 — CUSTOMER & FINANCIAL ANALYSIS

- **Page Name**: `Customer & Financial Analysis`
- **Header Banner**: `Customer Demographics & Financial Liquidity Profile`

#### Top KPI Cards
1. **Average Balance**: `[Average Balance]` (`€1,362.27`)
2. **Median Balance**: `[Median Balance]` (`€448.00`)
3. **Housing Loan Customers**: `[Housing Loan Customers]` (`25,130` / `55.6%`)
4. **Personal Loan Customers**: `[Personal Loan Customers]` (`7,244` / `16.0%`)

#### Core Visuals
1. **Area / Column Chart — Age Distribution**:
   - *X-Axis*: `age`
   - *Y-Axis*: `[Total Customers]`
2. **Bar Chart — Education Level Breakdown**:
   - *X-Axis*: `education`
   - *Y-Axis*: `[Total Customers]`
   - *Data Labels*: Total count and percentage
3. **Treemap / Bar Chart — Job Distribution**:
   - *Category*: `job`
   - *Values*: `[Total Customers]`
4. **Column Chart — Balance Brackets / Distribution**:
   - Grouping negative overdraft balances vs. positive balance tiers
5. **Donut Chart — Housing Loan Distribution**:
   - *Legend*: `housing` (`yes`, `no`)
   - *Values*: `[Total Customers]`
6. **Donut Chart — Personal Loan Distribution**:
   - *Legend*: `loan` (`yes`, `no`)
   - *Values*: `[Total Customers]`
7. **Bar Chart — Subscription Rate by Education**:
   - *Y-Axis*: `education`
   - *X-Axis*: `[Subscription Rate]` (Tertiary `15.0%`, Secondary `10.6%`, Primary `8.6%`)
8. **Horizontal Bar Chart — Average Balance by Job Category**:
   - *Y-Axis*: `job` (Sorted descending by `[Average Balance]`)
   - *X-Axis*: `[Average Balance]`

#### Slicers
- `Age Group`, `Job`, `Education`, `Marital`, `Housing`, `Loan`

---

### PAGE 3 — MARKETING CAMPAIGN PERFORMANCE

- **Page Name**: `Marketing Campaign Performance`
- **Header Banner**: `Campaign Channel Effectiveness & Engagement Dynamics`

#### Top KPI Cards
1. **Average Call Duration**: `[Average Call Duration (Minutes)]` (`4.3 mins` / `258.2s`)
2. **Average Campaign Contacts**: `[Average Campaign Contacts]` (`2.8 contacts`)
3. **Previously Contacted Customers**: `[Previously Contacted Customers]` (`8,257` / `18.3%`)
4. **Previous Campaign Success Rate**: `[Previous Campaign Success Rate]` (`3.3%` overall; `64.7%` when reached)

#### Core Visuals
1. **Column Chart — Subscription Rate by Contact Communication Channel**:
   - *X-Axis*: `contact` (`cellular`, `telephone`, `unknown`)
   - *Y-Axis*: `[Subscription Rate]`
   - Cellular (`14.9%`), Telephone (`13.4%`), Unknown (`4.1%`)
2. **Column Chart — Subscription Rate by Previous Campaign Outcome (`poutcome`)**:
   - *X-Axis*: `poutcome` (`success`, `other`, `failure`, `unknown`)
   - *Y-Axis*: `[Subscription Rate]`
   - Highlights prior success conversion (`64.7%`)
3. **Clustered Bar Chart — Call Duration: Subscribed vs. Not Subscribed**:
   - *X-Axis*: `y` (`yes`, `no`)
   - *Values*: `[Average Call Duration (Minutes)]`
   - Demonstrates `8.95 mins` (yes) vs `3.69 mins` (no)
4. **Clustered Bar Chart — Account Balance: Subscribed vs. Not Subscribed**:
   - *X-Axis*: `y` (`yes`, `no`)
   - *Values*: `[Average Balance]`
   - Displays `€1,804.27` (yes) vs `€1,303.71` (no)
5. **Line / Column Chart — Subscription Rate by Campaign Contact Frequency**:
   - *X-Axis*: `campaign` (binned 1, 2, 3, 4, 5, 6+)
   - *Y-Axis*: `[Subscription Rate]`
   - Demonstrates diminishing returns after 2-3 calls
6. **Donut / Bar Chart — Previous Campaign Outcome Distribution**:
   - *Legend*: `poutcome`
   - *Values*: `[Total Customers]`

#### Slicers
- `Contact`, `Poutcome`, `Campaign`, `Month`, `Age Group`, `Job`

---

## 5. Verified Empirical Business Findings Reference

When presenting or configuring tooltips, reference these **exact calculations verified from the completed Python pipeline**:

| Metric / Dimension | Subgroup | Verified Finding | Portfolio Presentation Note |
| :--- | :--- | :--- | :--- |
| **Overall Campaign Conversion** | All Customers | **11.70%** (5,289 / 45,211) | Baseline conversion benchmark |
| **Age Cohort Conversion** | `66+` Years | **42.61%** (320 / 751) | Highest converting demographic |
| | `18-25` Years | **23.95%** (320 / 1,336) | Second highest converting demographic |
| | `56-65` Years | **14.12%** (586 / 4,149) | Above-average conversion |
| | `26-35` Years | **12.00%** (1,869 / 15,571) | Near baseline conversion |
| | `36-45` Years | **9.39%** (1,301 / 13,856) | Below-average conversion |
| | `46-55` Years | **9.35%** (893 / 9,548) | Lowest converting age cohort |
| **Job Role Conversion** | `student` | **28.68%** (269 / 938) | Highest conversion rate |
| | `retired` | **22.79%** (516 / 2,264) | Second highest conversion rate |
| | `unemployed` | **15.50%** (202 / 1,303) | Moderate conversion rate |
| | `management` | **13.76%** (1,301 / 9,458) | High-volume professional group |
| | `admin.` | **12.20%** (631 / 5,171) | Typical conversion rate |
| | `blue-collar` | **7.27%** (708 / 9,732) | Lowest converting occupation |
| **Housing Loan Impact** | Without Housing Loan | **16.70%** (3,354 / 20,081) | Over 2x higher than mortgage holders |
| | With Housing Loan | **7.70%** (1,935 / 25,130) | Debt burden depresses savings |
| **Personal Loan Impact** | Without Personal Loan | **12.66%** (4,805 / 37,967) | Strong conversion |
| | With Personal Loan | **6.68%** (484 / 7,244) | Severe conversion drag |
| **Contact Communication** | `cellular` | **14.92%** (4,369 / 29,285) | Primary and most effective channel |
| | `telephone` | **13.42%** (390 / 2,906) | Stable landline channel |
| | `unknown` | **4.07%** (530 / 13,020) | Inefficient contact touchpoint |
| **Prior Campaign Outcome** | Prior `success` | **64.73%** (978 / 1,511) | Single strongest predictor in dataset |
| | Prior `other` | **16.68%** (307 / 1,840) | Modest re-engagement conversion |
| | Prior `failure` | **12.61%** (618 / 4,901) | Above unknown baseline |
| | Prior `unknown` | **9.16%** (3,386 / 36,959) | Newly targeted prospects |
| **Account Balance Profile** | Subscribed (`y = "yes"`) | **EUR 1,804.27** (Median: EUR 733.00) | **+EUR 500.56 (+38.4%) higher** |
| | Not Subscribed (`y = "no"`) | **EUR 1,303.71** (Median: EUR 417.00) | Lower baseline liquidity |
| **Call Duration Profile** | Subscribed (`y = "yes"`) | **537.29 s** (~8.95 mins; Median: 426s) | **+316.1s (+142.9%) longer** |
| | Not Subscribed (`y = "no"`) | **221.18 s** (~3.69 mins; Median: 164s) | Shorter call duration |

> [!CAUTION]
> **Analytical Rigor & Academic Non-Causality Rule**:
> Always describe these findings as **empirical associations or observed relationships in historical campaign data**. Do NOT assert causal claims (e.g., do not say *"long calls cause customers to subscribe"* or *"giving loans prevents deposits"*). State clearly: *"Subscribing clients had substantially longer average call durations (8.95 vs. 3.69 mins) and higher account balances in this dataset."*

---

## 6. Dashboard Visual Design & UI System

### Color Palette
- **Canvas / Page Background**: Off-white `#F8F9FA`
- **Visual Card Background**: Pure White `#FFFFFF` with 4px border radius and 1px border (`#E2E8F0`)
- **Primary Accent / Brand Color**: Deep Navy `#1E3A8A`
- **Positive / Conversion Outcome**: Emerald Green `#059669`
- **Negative / Non-Conversion Outcome**: Crimson Red `#DC2626`
- **Secondary / Supporting Categorical**: Slate Blue `#3B82F6`, Amber `#D97706`, Purple `#7C3AED`
- **Primary Typography**: Charcoal `#1F2937`
- **Muted Typography / Axis Labels**: Cool Gray `#6B7280`

### Visual Hierarchy & Spacing
- Maintain a consistent 12px gutter between cards.
- KPI cards must have uniform height (90px) and display bold large callout values (24pt font) with clean labels below (10pt font).
- Eliminate gridlines from bar and column charts or set to subtle light gray (`#E5E7EB`).
- Format all numeric values with standard commas (`#,##0`), currency with euro symbol (`€#,##0.00`), and percentages with one decimal (`0.0%`).
