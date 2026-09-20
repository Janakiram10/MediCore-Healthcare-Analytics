# MediCore Health Network — Healthcare Revenue, Patient Flow \& Operational Intelligence

**Portfolio case study | Advanced Data Analyst | PostgreSQL + Python/Pandas + Power BI**

> Fictional/synthetic healthcare network created for portfolio demonstration. No real patient data is used.

## Business problem

MediCore operates multiple hospitals and needs a unified view of patient flow, appointment behavior, operational performance, revenue/collections, patient experience, and 30-day readmissions.

## Solution

A PostgreSQL analytical layer produces validated business views. Python supports data-quality and statistical analysis. Power BI provides the executive decision layer.

## Dataset

* 8 hospitals
* 44 departments
* 600 doctors
* 100,000 patients
* 500,000 appointments
* 300,000 encounters
* 300,000 billing records
* 210,000 patient-feedback records
* Analysis period: 2024–2025

## Key validated KPIs

|KPI|Result|
|-|-:|
|Total appointments|500,000|
|Total encounters|300,000|
|Total billed|₹178.13 Cr|
|Total collected|₹111.98 Cr|
|Outstanding|₹33.01 Cr|
|Collection rate|62.86%|
|No-show rate|9.81%|
|Avg satisfaction|74.61|
|Avg wait|62.18 min|
|30-day readmission|3.65%|

## Analytical areas

1. Executive performance
2. Appointment/no-show behavior
3. Revenue and collections
4. Hospital operations
5. Patient experience
6. 30-day readmission

## Power BI

The PBIP report contains one polished **Executive Overview** page with 10 KPI cards and 6 analytical visuals. The report definition has been programmatically arranged for a 1920×1080 canvas.

## Project structure

```text
MediCore\\\_Healthcare\\\_Analytics/
├── README.md
├── data/raw/
├── data/validation/
├── documentation/
├── notebooks/
├── python/
├── sql/
├── MediCore\\\_Healthcare\\\_Analytics.pbip
├── MediCore\\\_Healthcare\\\_Analytics.Report/
└── MediCore\\\_Healthcare\\\_Analytics.SemanticModel/
```

## Important analytical note

Observed associations are reported as associations. The project avoids unsupported causal claims. The no-show regression showed limited explanatory power, so it is positioned as segmentation/risk analysis rather than a strong prediction engine.

## How to open

Open `MediCore\\\_Healthcare\\\_Analytics.pbip` with Power BI Desktop. The PBIP report is the editable report-definition source.



