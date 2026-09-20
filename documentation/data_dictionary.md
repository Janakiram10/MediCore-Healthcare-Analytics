# MediCore — Data Dictionary (summary)

| Table | Grain | Main purpose |
|---|---|---|
| dim_date | one row/date | calendar and fiscal analysis |
| dim_hospital | one row/hospital | hospital master |
| dim_department | one row/department | department master |
| dim_doctor | one row/doctor | provider master |
| dim_patient | one row/patient | patient master |
| dim_insurance | one row/plan | payer/plan master |
| dim_diagnosis | one row/diagnosis | diagnosis reference |
| fact_appointments | one row/appointment | scheduling and no-show analysis |
| fact_encounters | one row/encounter | patient flow and operations |
| fact_billing | one row/bill | revenue and collections |
| fact_patient_feedback | one row/feedback | patient experience |

Detailed column definitions can be read directly from the CSV headers and PostgreSQL source tables included in the project.
