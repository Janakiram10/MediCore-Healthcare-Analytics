# 🏥 MediCore Healthcare Analytics

## Healthcare Revenue, Patient Flow & Operational Intelligence

**Advanced end-to-end Data Analyst portfolio project**

`PostgreSQL` • `SQL` • `Python` • `Pandas` • `Statistical Analysis` • `Power BI` • `Plotly Dash`

> **Portfolio disclaimer:** MediCore Health Network is a fictional healthcare organization created for this case study. All data is synthetic and no real patient information is used.

## 🔗 Live project

**Interactive management dashboard:** https://web-production-d29b6.up.railway.app/

The web dashboard contains six management views with hospital, department, year, and encounter-type filtering:

1. Executive Overview
2. Hospital Performance
3. No-show Analysis
4. Patient Experience
5. Readmission & Risk
6. Revenue & Collections

## 📌 Project overview

MediCore Healthcare Analytics simulates how a multi-hospital healthcare network can combine operational, financial, appointment, patient-experience, and readmission data into a validated decision-support system.

### Dataset scale

- 8 hospitals
- 44 departments
- 600 doctors
- 100,000 patients
- 500,000 appointments
- 300,000 encounters
- 300,000 billing records
- 210,000 patient-feedback records
- Analysis period: 2024–2025

## 🎯 Business problem

Management needs a unified analytical view to answer questions such as:

- How effectively is billed revenue being collected?
- Which hospitals and departments carry the highest operational pressure?
- What patterns are associated with appointment no-shows?
- Where are patients experiencing longer waiting times?
- How does patient satisfaction vary across the network?
- Which diagnosis groups show higher observed 30-day readmission rates?
- How do hospitals compare across revenue, utilization, experience, and risk metrics?

## 🧱 Analytics architecture

```text
Synthetic Healthcare Data
        │
        ▼
PostgreSQL Relational Model
        │
        ├── Data-quality checks
        ├── Validation queries
        └── Analytical views
        │
        ▼
Python / Pandas / Statistics
        │
        ├── KPI validation
        ├── Exploratory analysis
        └── No-show statistical analysis
        │
        ├───────────────┐
        ▼               ▼
Power BI          Plotly Dash
Executive         Interactive
Reporting         Management App
```

### Why each tool is used

**PostgreSQL** — relational modelling, business logic, reusable analytical views, data-quality checks, and KPI-ready query layers.

**Python / Pandas** — validation, exploratory analysis, statistical investigation, and independent KPI verification.

**Power BI** — executive reporting through a structured semantic/report layer.

**Plotly Dash** — a deployable interactive web application for portfolio review and management exploration.

## 📊 Validated headline KPIs

| KPI | Result |
|---|---:|
| Total appointments | 500,000 |
| Total encounters | 300,000 |
| Total billed | ₹178.13 Cr |
| Total collected | ₹111.98 Cr |
| Outstanding | ₹33.01 Cr |
| Collection rate | 62.86% |
| No-show rate | 9.81% |
| Avg satisfaction | 74.61 |
| Avg wait | 62.18 min |
| 30-day readmission | 3.65% |

Detailed KPI definitions are documented in [documentation/kpi_definitions.md](documentation/kpi_definitions.md).

## 🔎 Key business findings

- Longer appointment lead times were associated with higher raw no-show rates; the 31+ day group had a higher observed rate than same-day bookings.
- The multivariable no-show logistic model had low explanatory power (pseudo R² ≈ 0.0078), so the project treats it as segmentation/risk analysis rather than a production prediction model.
- Hospital collection rates were tightly clustered, making **absolute outstanding exposure** more operationally useful than small percentage differences.
- H005 had the highest encounter volume and the largest absolute outstanding exposure.
- H007 had the highest observed average wait time despite lower volume.
- Patient satisfaction declined as wait time increased, while complaint rates increased.
- Readmission-rate variation by diagnosis was modest, so elevated groups are framed as monitoring priorities rather than proven causal drivers.

Full evidence and interpretation: [documentation/business_insights.md](documentation/business_insights.md).

## 🧪 Analytical scope

The project covers:

1. Executive performance
2. Appointment utilization and no-show behavior
3. Revenue and collections
4. Hospital and department operations
5. Patient experience
6. 30-day readmission monitoring

## 📈 Power BI

The repository includes both editable **PBIP** project files and a retained **PBIX** export.

The Executive Overview contains:

- 10 KPI cards
- Total encounters by hospital
- Billed revenue by hospital
- Outstanding amount by hospital
- No-show appointments by category
- Patient satisfaction vs wait time
- 30-day readmission rate by diagnosis

See [documentation/powerbi_dashboard.md](documentation/powerbi_dashboard.md).

## 🌐 Plotly Dash

The Dash application provides a multi-page management experience with global filters and interactive charts/tables.

Source: [dashboard/app.py](dashboard/app.py)  
Run instructions: [dashboard/README.md](dashboard/README.md)

## 🗂️ Repository structure

```text
MediCore-Healthcare-Analytics/
├── README.md
├── PROJECT_STATUS.md
├── Procfile
├── requirements.txt
├── dashboard/
│   ├── app.py
│   ├── README.md
│   └── requirements.txt
├── data/
│   ├── raw/
│   └── validation/
├── documentation/
│   ├── business_requirements.md
│   ├── business_insights.md
│   ├── data_dictionary.md
│   ├── data_model.md
│   ├── dq_rules.md
│   ├── kpi_definitions.md
│   └── powerbi_dashboard.md
├── notebooks/
│   ├── 01_generate_dimensions.ipynb
│   ├── 02_generate_appointments.ipynb
│   ├── 03_generate_encounters.ipynb
│   └── 05_no_show_statistical_analysis.ipynb
├── python/
│   ├── validate_dataset.py
│   └── finish_powerbi_layout.py
├── sql/
│   ├── 01_database_setup.sql
│   ├── 02_load_data.sql
│   ├── 03_data_quality_checks.sql
│   ├── 04_views.sql
│   ├── 05_validation_queries.sql
│   └── 06_analytical_views.sql
├── MediCore_Healthcare_Analytics.pbip
├── MediCore_Healthcare_Analytics.Report/
└── MediCore_Healthcare_Analytics.SemanticModel/
```

## ▶️ Reproduce the project

### 1. Python environment

```bash
pip install -r requirements.txt
```

### 2. PostgreSQL layer

Run the SQL scripts in numerical order:

```text
sql/01_database_setup.sql
sql/02_load_data.sql
sql/03_data_quality_checks.sql
sql/04_views.sql
sql/05_validation_queries.sql
sql/06_analytical_views.sql
```

### 3. Database-backed notebook

The no-show analysis notebook reads PostgreSQL credentials from environment variables rather than storing credentials in source control.

Required variable:

```text
MEDICORE_DB_PASSWORD
```

Optional overrides:

```text
MEDICORE_DB_HOST
MEDICORE_DB_PORT
MEDICORE_DB_NAME
MEDICORE_DB_USER
```

### 4. Run the interactive dashboard

```bash
python dashboard/app.py
```

Then open:

```text
http://127.0.0.1:8050
```

### 5. Open Power BI

Open:

```text
MediCore_Healthcare_Analytics.pbip
```

Refresh the PostgreSQL connection if your local database is not already connected.

## ✅ Data quality and analytical discipline

The project includes explicit data-quality checks and validation logic.

Observed relationships are reported as **associations**, not causation. Statistical significance is not treated as equivalent to business importance, and the no-show model is not overstated as a strong predictive model.

This is intentional: the goal is a credible analytics case study, not an artificially inflated machine-learning demo.

## 📚 Documentation

- [Business requirements](documentation/business_requirements.md)
- [Business insights](documentation/business_insights.md)
- [Data dictionary](documentation/data_dictionary.md)
- [Data model](documentation/data_model.md)
- [Data-quality rules](documentation/dq_rules.md)
- [KPI definitions](documentation/kpi_definitions.md)
- [Power BI dashboard notes](documentation/powerbi_dashboard.md)
- [Project completion status](PROJECT_STATUS.md)
