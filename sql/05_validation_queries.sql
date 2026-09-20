-- Expected portfolio checkpoints
SELECT COUNT(*) FROM dim_hospital;
SELECT COUNT(*) FROM dim_department;
SELECT COUNT(*) FROM dim_doctor;
SELECT COUNT(*) FROM dim_patient;
SELECT COUNT(*) FROM fact_appointments;
SELECT COUNT(*) FROM fact_encounters;
SELECT COUNT(*) FROM fact_billing;
SELECT COUNT(*) FROM fact_patient_feedback;

-- Executive financial checkpoint
SELECT ROUND(SUM(billed_amount)/10000000.0,2) AS billed_cr,
       ROUND(SUM(insurance_paid+patient_paid)/10000000.0,2) AS collected_cr,
       ROUND(SUM(outstanding_amount)/10000000.0,2) AS outstanding_cr,
       ROUND(100.0*SUM(insurance_paid+patient_paid)/NULLIF(SUM(billed_amount),0),2) AS collection_rate_pct
FROM fact_billing;
