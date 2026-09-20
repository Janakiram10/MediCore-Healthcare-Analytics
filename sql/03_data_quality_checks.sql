-- MediCore DQ checks

-- 1. Appointment status/no-show consistency
SELECT status, no_show, COUNT(*)
FROM fact_appointments
GROUP BY status, no_show
ORDER BY status, no_show;

-- 2. Patient registration vs appointment date
SELECT COUNT(*) AS invalid_appointments
FROM fact_appointments a
JOIN dim_patient p USING (patient_id)
JOIN dim_date d ON d.date_id = a.appointment_date_id
WHERE d.full_date < p.registration_date;

-- 3. Negative operational durations
SELECT COUNT(*) AS invalid_waits FROM fact_encounters WHERE wait_time_minutes < 0;
SELECT COUNT(*) AS invalid_consultation_times FROM fact_encounters WHERE consultation_time_minutes < 0;

-- 4. Billing reconciliation
SELECT COUNT(*) AS financial_consistency_failures
FROM fact_billing
WHERE ABS(billed_amount - (insurance_paid + patient_paid + outstanding_amount + COALESCE(financial_difference,0))) > 0.01;

-- 5. Intentional insurance missingness
SELECT
  COUNT(*) FILTER (WHERE insurance_id IS NULL) AS missing_insurance,
  COUNT(*) AS total_patients
FROM dim_patient;
