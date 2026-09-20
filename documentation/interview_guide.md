# MediCore — Interview Walkthrough Guide

## 30-second project summary

MediCore Healthcare Analytics is an end-to-end healthcare analytics portfolio project built on synthetic data from a fictional network of eight hospitals. I designed a relational PostgreSQL analytics layer, validated and analyzed the data with Python and statistical methods, built an executive Power BI report, and deployed a multi-page Plotly Dash application. The project focuses on revenue and collections, appointment no-shows, hospital operations, patient experience, and 30-day readmissions.

## 60-second interview explanation

The business problem was that a multi-hospital network needed a unified view of financial, operational, appointment, patient-experience, and readmission performance.

I modeled the data around conformed healthcare dimensions and four major fact tables: appointments, encounters, billing, and patient feedback. PostgreSQL handles the core relational model, data-quality checks, validation queries, and reusable analytical views.

Python was used for independent validation and statistical investigation, especially the no-show analysis. An important outcome was that the multivariable logistic model had low explanatory power, with pseudo R² around 0.0078. Instead of overstating that as predictive machine learning, I positioned the analysis as segmentation and risk-pattern analysis.

For presentation, Power BI provides the executive reporting layer, while Plotly Dash provides an interactive deployed application with six management views and global filters.

The final project analyzes 500,000 appointments, 300,000 encounters, 300,000 billing records, and 210,000 feedback records across eight hospitals.

## 3-minute walkthrough

### 1. Business framing

The project was designed around six decision areas:

- executive performance
- appointment/no-show behavior
- revenue and collections
- hospital operations
- patient experience
- 30-day readmission

The aim was not simply to build charts. Each metric needed a clear business definition and an appropriate fact-table grain.

### 2. Data model

The analytical model uses shared dimensions such as date, hospital, department, doctor, patient, insurance, and diagnosis.

The primary facts are:

- appointments
- encounters
- billing
- patient feedback

Keeping the grain explicit prevents common analytical errors such as calculating readmission rates across non-admission encounters or mixing billing and encounter counts after an unsafe join.

### 3. SQL layer

PostgreSQL is the analytical foundation.

The SQL workflow contains:

- database setup
- data loading
- data-quality checks
- reusable business views
- validation queries
- analytical views

This keeps business logic reusable instead of embedding all calculations directly inside visualization tools.

### 4. Python and statistics

Python provides a second validation layer and handles statistical investigation.

For no-shows, I examined lead time, appointment type, booking channel, and hospital-level patterns. A multivariable logistic regression was also tested.

Although several variables were statistically significant because of the large sample, the overall model had limited explanatory power. That distinction between statistical significance and useful predictive performance is one of the analytical lessons from the project.

### 5. Business findings

Headline validated KPIs include:

- 500,000 appointments
- 300,000 encounters
- ₹178.13 Cr billed
- ₹111.98 Cr collected
- ₹33.01 Cr outstanding
- 62.86% collection rate
- 9.81% eligible-base no-show rate
- 74.61 average satisfaction
- 62.18-minute average wait
- 3.65% 30-day readmission rate

The project also found that longer wait-time groups showed lower satisfaction and higher complaint rates, while collection-rate differences between hospitals were relatively small compared with differences in absolute outstanding exposure.

### 6. Reporting layers

Power BI demonstrates enterprise-style executive reporting and semantic/report-layer skills.

Plotly Dash makes the analysis accessible through a deployed interactive management application covering:

- Executive Overview
- Hospital Performance
- No-show Analysis
- Patient Experience
- Readmission & Risk
- Revenue & Collections

### 7. What I would improve in a production environment

For a real organization I would add:

- governed production data pipelines
- role-based access controls
- PHI/PII protections
- automated data-quality monitoring
- incremental refresh
- source-system lineage
- formal KPI ownership
- alerting thresholds
- model monitoring if predictive models were introduced

The portfolio version intentionally avoids pretending synthetic data has real operational impact.

## Likely technical questions

### Why PostgreSQL if Power BI can transform data?

PostgreSQL centralizes reusable business logic and validation. It prevents the analytical rules from existing only inside a reporting file and makes the data layer easier to test and reuse.

### Why both Power BI and Plotly Dash?

They demonstrate different capabilities. Power BI represents enterprise BI/reporting, while Dash provides a deployable web experience that recruiters can access without Power BI Desktop.

### Why did you not build a stronger ML model for no-shows?

The tested variables had limited explanatory power. Adding more algorithms without stronger signal would make the project look more complex but not more analytically credible.

### Why is the no-show rate not calculated using every appointment?

Cancelled appointments are excluded because the KPI measures no-shows among appointments that reached an attendance/no-show outcome.

### Why is readmission calculated only on admissions?

A readmission metric requires an index admission. Including outpatient and other non-admission encounters in the denominator would distort the rate.

### Which revenue metric would you prioritize?

Both collection rate and absolute outstanding amount matter. In this dataset, hospital collection rates are tightly clustered, so absolute outstanding exposure provides more differentiation for prioritization.

### What is the biggest limitation?

The dataset is synthetic, so findings demonstrate analytical methodology rather than real-world healthcare performance or causal effects.

## Resume-ready project bullets

- Built an end-to-end healthcare analytics solution across 8 hospitals using PostgreSQL, Python, Power BI, and Plotly Dash, analyzing 500K appointments, 300K encounters, 300K billing records, and 210K patient-feedback records.
- Designed reusable SQL analytical views and data-quality validation for revenue, collections, patient flow, no-shows, satisfaction, wait times, and 30-day readmissions.
- Performed Python-based statistical analysis of appointment no-shows and correctly limited conclusions when multivariable logistic regression showed low explanatory power.
- Developed an executive Power BI report and deployed a six-view interactive Dash application with hospital, department, year, and encounter-type filtering.
- Documented KPI definitions, analytical grain, business insights, reproducibility steps, and limitations to make the project auditable and interview-ready.
