# MediCore — Analytical Data Model

## Architecture
Source systems → raw tables → validation/staging → analytical views → Power BI.

## Star-model tables
### Dimensions
- dim_date
- dim_hospital
- dim_department
- dim_doctor
- dim_patient
- dim_insurance
- dim_diagnosis

### Facts
- fact_appointments — one row per scheduled appointment
- fact_encounters — one row per encounter
- fact_billing — one row per bill
- fact_patient_feedback — one row per submitted feedback record

## Grain rules
The fact tables are analyzed at their stated grain. Aggregated Power BI views are used for the executive dashboard so that each row represents one analytical category at the view's defined level.

## Key relationships
patient, doctor, department, hospital, diagnosis, insurance, and date identifiers are used as conformed dimensions across the fact tables.
