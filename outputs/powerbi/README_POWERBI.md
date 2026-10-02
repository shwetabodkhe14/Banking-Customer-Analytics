# Power BI Dashboard Setup & User Guide
## Banking Customer & Marketing Analytics

Welcome to the Power BI guide for the **Banking Customer & Marketing Analytics** project. This document outlines step-by-step instructions for loading data, establishing DAX measures, building the 3-page interactive dashboard, and exporting publication-ready visuals for your portfolio and GitHub repository.

---

## 1. How to Import `bank_powerbi.csv` into Power BI

1. Open **Power BI Desktop**.
2. On the **Home** tab ribbon, click **Get Data** > **Text/CSV**.
3. Navigate to:
   ```
   C:\projects\Banking-Customer-Analytics\outputs\powerbi\bank_powerbi.csv
   ```
4. In the preview dialog window:
   - **File Origin**: `65001: Unicode (UTF-8)`
   - **Delimiter**: `Comma`
   - **Data Type Detection**: `Based on first 200 rows`
5. Click **Transform Data** to open the **Power Query Editor**.

---

## 2. How to Verify & Set Data Types in Power Query

Review and confirm the column types in the **Transform** ribbon tab:

1. **Numeric Columns** (Set type to `Whole Number` / Int64):
   - `age`
   - `balance`
   - `day`
   - `duration`
   - `campaign`
   - `pdays`
   - `previous`
2. **Text / Categorical Columns** (Set type to `Text`):
   - `job`
   - `marital`
   - `education`
   - `default`
   - `housing`
   - `loan`
   - `contact`
   - `month`
   - `poutcome`
   - `y` *(Ensure this is Text; do NOT convert to True/False or integer)*
   - `age_group` *(Categorical cohort)*
3. Check row count: In Power Query, click **Transform** > **Count Rows** to verify all `45,211` rows are present.
4. Click **Home** > **Close & Apply** to load the dataset into the Power BI data model.

---

## 3. How to Create the DAX Measures

Organize your DAX formulas by creating a dedicated measures table or placing them directly on `bank_powerbi`:

1. On the **Home** ribbon, click **New Measure**.
2. Paste each formula and assign the corresponding format string in the **Measure tools** tab:

### Primary KPI Measures
```dax
Total Customers = COUNTROWS('bank_powerbi')
```
*(Format: Whole Number with comma `#,#`)*

```dax
Subscribed Customers = 
CALCULATE(
    COUNTROWS('bank_powerbi'), 
    'bank_powerbi'[y] = "yes"
)
```
*(Format: Whole Number with comma `#,#`)*

```dax
Subscription Rate = 
DIVIDE([Subscribed Customers], [Total Customers], 0)
```
*(Format: Percentage with 1 decimal `0.0%`)*

```dax
Average Balance = AVERAGE('bank_powerbi'[balance])
```
*(Format: Currency `€#,##0`)*

```dax
Median Balance = MEDIAN('bank_powerbi'[balance])
```
*(Format: Currency `€#,##0`)*

```dax
Average Call Duration = AVERAGE('bank_powerbi'[duration])
```

```dax
Average Call Duration (Minutes) = 
DIVIDE([Average Call Duration], 60, 0)
```
*(Format: Decimal Number `0.0`)*

```dax
Average Campaign Contacts = AVERAGE('bank_powerbi'[campaign])
```
*(Format: Decimal Number `0.0`)*

```dax
Previously Contacted Customers = 
CALCULATE(
    COUNTROWS('bank_powerbi'), 
    'bank_powerbi'[pdays] <> -1
)
```
*(Format: Whole Number `#,#`)*

```dax
Previous Campaign Success Rate = 
DIVIDE(
    CALCULATE(COUNTROWS('bank_powerbi'), 'bank_powerbi'[poutcome] = "success"), 
    [Total Customers], 
    0
)
```
*(Format: Percentage `0.0%`)*

---

## 4. How to Create the 3 Dashboard Pages

Rename the default page tab to `Executive Overview` and create two additional pages.

### Page 1: Executive Overview
- **Header**: Add a Text Box or Banner Shape across the top (`#1E3A8A` background or white background with dark blue title):
  - **Title**: `Banking Customer & Marketing Analytics`
  - **Subtitle**: `Customer Profile, Financial Behavior & Term Deposit Campaign Analysis`
- **KPI Cards** (top row): Place 5 Card visuals side-by-side:
  - Card 1: `[Total Customers]`
  - Card 2: `[Subscribed Customers]`
  - Card 3: `[Subscription Rate]`
  - Card 4: `[Average Balance]`
  - Card 5: `[Average Call Duration (Minutes)]`
- **Visuals**:
  1. **Donut Chart**: `y` as Legend, `[Total Customers]` as Values. (Green for `yes`, Red for `no`).
  2. **Clustered Column Chart**: `age_group` on X-axis, `[Total Customers]` on Y-axis.
  3. **Clustered Bar Chart**: `job` on Y-axis, `[Total Customers]` on X-axis.
  4. **Clustered Column Chart**: `age_group` on X-axis, `[Subscription Rate]` on Y-axis with a reference constant line at `11.7%`.
  5. **Clustered Bar Chart**: `job` on Y-axis, `[Subscription Rate]` on X-axis with a reference line at `11.7%`.
- **Slicers**: Add a filter bar on the left with slicers for `Job`, `Education`, `Marital Status`, `Housing Loan`, and `Age Group`.

### Page 2: Customer & Financial Analysis
- **Header**: `Customer Demographics & Financial Liquidity Profile`
- **KPI Cards**: `[Average Balance]`, `[Median Balance]`, `[Housing Loan Customers]`, `[Personal Loan Customers]`
- **Visuals**:
  1. **Histogram / Area Chart**: `age` vs. `[Total Customers]`
  2. **Bar Chart**: `education` distribution
  3. **Treemap / Bar Chart**: `job` distribution
  4. **Column Chart**: Account Balance tiers / distribution
  5. **Donut Chart**: `housing` loan proportion (`yes` vs. `no`)
  6. **Donut Chart**: `loan` personal loan proportion (`yes` vs. `no`)
  7. **Bar Chart**: `[Subscription Rate]` by `education`
  8. **Horizontal Bar Chart**: `[Average Balance]` by `job`
- **Slicers**: `Age Group`, `Job`, `Education`, `Marital`, `Housing`, `Loan`

### Page 3: Marketing Campaign Performance
- **Header**: `Marketing Campaign Effectiveness & Engagement Dynamics`
- **KPI Cards**: `[Average Call Duration (Minutes)]`, `[Average Campaign Contacts]`, `[Previously Contacted Customers]`, `[Previous Campaign Success Rate]`
- **Visuals**:
  1. **Column Chart**: `[Subscription Rate]` by `contact` method
  2. **Column Chart**: `[Subscription Rate]` by `poutcome` (prior campaign outcome)
  3. **Clustered Bar Chart**: Subscribed vs Not Subscribed (`y`) by `[Average Call Duration (Minutes)]`
  4. **Clustered Bar Chart**: Subscribed vs Not Subscribed (`y`) by `[Average Balance]`
  5. **Line Chart**: `[Subscription Rate]` by `campaign` contact frequency
  6. **Donut Chart**: `poutcome` distribution
- **Slicers**: `Contact`, `Poutcome`, `Campaign`, `Month`, `Age Group`, `Job`

---

## 5. How to Format the Dashboard for Portfolio Presentation

1. **Color Uniformity**:
   - Set Page Background to light gray/off-white (`#F8F9FA`).
   - Visual cards: Pure White (`#FFFFFF`) with subtle border (`#E2E8F0`) and 4px border radius.
   - Use Emerald (`#059669`) for positive outcomes (`y = yes`, success) and Crimson (`#DC2626`) for negative outcomes (`y = no`, failure).
2. **Typography**:
   - Font family: `Segoe UI` or `Din`
   - Visual Titles: Bold, 12pt, Charcoal (`#1F2937`)
   - Data Labels: 9pt or 10pt
3. **Data Labels**: Enable data labels on key bar and column charts; turn off redundant Y-axis titles when the visual title already conveys the metric.
4. **Tooltips**: Configure tooltips to display `[Total Customers]`, `[Subscribed Customers]`, and `[Subscription Rate]` when hovering over categories.

---

## 6. How to Export Dashboard Screenshots for GitHub

1. In Power BI Desktop, maximize your window or press `F11` (or View > Actual Size).
2. Navigate to Page 1:
   - Use Windows Snipping Tool (`Win + Shift + S`) or capture the window.
   - Save the image to:
     ```
     outputs/powerbi/screenshots/01_executive_overview.png
     ```
3. Repeat for Page 2 and Page 3:
   - `outputs/powerbi/screenshots/02_customer_financial_analysis.png`
   - `outputs/powerbi/screenshots/03_marketing_campaign_performance.png`
4. Add the images to your project `README.md` using standard markdown embeds:
   ```markdown
   ![Executive Overview](outputs/powerbi/screenshots/01_executive_overview.png)
   ```
5. Commit and push your `.pbix` file (or provide instructions) to GitHub.
