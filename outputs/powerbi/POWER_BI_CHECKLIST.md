# Power BI Implementation Checklist
## Banking Customer & Marketing Analytics

Use this interactive checklist to track the development, quality assurance, and portfolio readiness of your Power BI dashboard:

- [ ] **Import `bank_powerbi.csv`**
  - Navigate to `Get Data > Text/CSV` and select `outputs/powerbi/bank_powerbi.csv`.
  - Ensure encoding is set to UTF-8 and comma delimiter.

- [ ] **Verify 45,211 Rows**
  - Inspect Power Query row count to confirm all 45,211 customer interaction records loaded without truncation.

- [ ] **Verify 18 Columns**
  - Ensure all 18 attributes are present (`age`, `job`, `marital`, `education`, `default`, `balance`, `housing`, `loan`, `contact`, `day`, `month`, `duration`, `campaign`, `pdays`, `previous`, `poutcome`, `y`, `age_group`).

- [ ] **Verify `age_group`**
  - Verify that `age_group` is present as the derived 18th column with values: `18-25`, `26-35`, `36-45`, `46-55`, `56-65`, `66+`.

- [ ] **Set Data Types**
  - Verify numeric columns (`age`, `balance`, `day`, `duration`, `campaign`, `pdays`, `previous`) are typed as Whole Number.
  - Verify categorical columns (`job`, `marital`, `education`, `default`, `housing`, `loan`, `contact`, `month`, `poutcome`, `y`, `age_group`) are typed as Text.
  - Verify `y` is kept as a Text/Categorical field.

- [ ] **Create KPI Measures**
  - Create `[Total Customers]`, `[Subscribed Customers]`, and `[Subscription Rate]`.
  - Create `[Average Balance]` and `[Median Balance]`.
  - Create `[Average Call Duration]` and `[Average Call Duration (Minutes)]`.
  - Create `[Average Campaign Contacts]`, `[Previously Contacted Customers]`, and `[Previous Campaign Success Rate]`.
  - Create `[Housing Loan Customers]` and `[Personal Loan Customers]`.

- [ ] **Create Page 1: Executive Overview**
  - Configure title banner: *Banking Customer & Marketing Analytics*.
  - Add 5 top KPI cards (`Total Customers`, `Subscribed Customers`, `Subscription Rate`, `Average Balance`, `Average Call Duration`).
  - Add Donut Chart for subscription outcome (`y`).
  - Add Column Chart for customer volume by `age_group`.
  - Add Bar Chart for customer volume by `job`.
  - Add Column Chart for `Subscription Rate` by `age_group`.
  - Add Bar Chart for `Subscription Rate` by `job`.
  - Add Slicers (`Job`, `Education`, `Marital Status`, `Housing Loan`, `Personal Loan`, `Contact Method`, `Age Group`).

- [ ] **Create Page 2: Customer & Financial Analysis**
  - Configure header banner: *Customer & Financial Analysis*.
  - Add 4 KPI cards (`Average Balance`, `Median Balance`, `Housing Loan Customers`, `Personal Loan Customers`).
  - Add Age, Education, Job, Balance, Housing loan, and Personal loan distributions.
  - Add Subscription Rate by Education and Average Balance by Job.
  - Add Slicers (`Age Group`, `Job`, `Education`, `Marital`, `Housing`, `Loan`).

- [ ] **Create Page 3: Marketing Campaign Performance**
  - Configure header banner: *Marketing Campaign Performance*.
  - Add 4 KPI cards (`Average Call Duration`, `Average Campaign Contacts`, `Previously Contacted Customers`, `Previous Campaign Success Rate`).
  - Add Subscription Rate by Contact Channel and by Previous Campaign Outcome.
  - Add Subscribed vs. Not Subscribed comparisons for Call Duration and Balance.
  - Add Subscription Rate by Campaign Contact Frequency.
  - Add Campaign Outcome distribution.
  - Add Slicers (`Contact`, `Poutcome`, `Campaign`, `Month`, `Age Group`, `Job`).

- [ ] **Add Slicers & Interactivity**
  - Set slicer orientation (dropdowns, tiles, buttons) for clean visual layout.
  - Verify cross-filtering and highlight behavior across visual charts.

- [ ] **Format Visuals & UI**
  - Apply clean off-white background (`#F8F9FA`) and white visual cards.
  - Format numeric labels (`#,##0`), currency (`€#,##0`), and percentages (`0.0%`).
  - Set consistent font families and remove redundant axis titles.

- [ ] **Verify Calculations Against Python Results**
  - Confirm overall subscription rate displays exactly `11.7%`.
  - Confirm `student` conversion is `28.68%` and `retired` is `22.79%`.
  - Confirm `66+` conversion is `42.61%` and `18-25` is `23.95%`.
  - Confirm debt-free vs. mortgage conversion: `16.70%` vs `7.70%`.
  - Confirm average balance: `€1,804.27` (yes) vs `€1,303.71` (no).
  - Confirm average call duration: `537.29s / 8.95 mins` (yes) vs `221.18s / 3.69 mins` (no).

- [ ] **Take Dashboard Screenshots**
  - Capture high-resolution full-screen captures of all 3 pages.
  - Save images to `outputs/powerbi/screenshots/`.

- [ ] **Add Screenshots to GitHub README**
  - Embed the exported screenshots into the main project `README.md`.
  - Push `.pbix` and updated repository to GitHub for portfolio demonstration.
