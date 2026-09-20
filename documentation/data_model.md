# MediCore — Analytical Data Model

## Architecture

```text
Synthetic source data
        │
        ▼
Raw relational tables / CSV assets
        │
        ▼
PostgreSQL validation and analytical layer
        │
        ├── data-quality checks
        ├── validation queries
        └── reusable analytical views
        │
        ▼
Python / Pandas / statistical analysis
        │
        ├───────────────┐
        ▼               ▼
Power BI          Plotly Dash
Executive         Interactive
reporting         management app
```

## Star-model tables

### Dimensions

- `dim_date`
- `dim_hospital`
- `dim_department`
- `dim_doctor`
- `dim_patient`
- `dim_insurance`
- `dim_diagnosis`

### Facts

- `fact_appointments` — one row per scheduled appointment
- `fact_encounters` — one row per encounter
- `fact_billing` — one row per bill
- `fact_patient_feedback` — one row per submitted feedback record

## Grain rules

Each fact table is analyzed at its stated grain. Metrics are calculated only after applying the relevant eligible population and filters.

Examples:

- No-show rate uses the eligible appointment population rather than all appointment statuses.
- Readmission rate uses admission encounters rather than all encounters.
- Revenue metrics aggregate billing records.
- Patient-experience metrics aggregate feedback records and join encounter wait-time context where required.

## Conformed dimensions

Patient, doctor, department, hospital, diagnosis, insurance, and date identifiers provide shared analytical dimensions across the corresponding facts.

This allows hospital-, department-, date-, diagnosis-, payer-, and patient-level analysis without mixing incompatible fact-table grains.

## Consumption layers

### Power BI

The Power BI report consumes prepared analytical structures for executive-level reporting and semantic presentation.

### Plotly Dash

The deployed Dash application reads the validated synthetic project files and applies equivalent business definitions through interactive management filters.

The two presentation layers serve different portfolio purposes rather than replacing the validated PostgreSQL/Python analytical foundation.
