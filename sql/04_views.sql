-- MediCore analytical views

CREATE OR REPLACE VIEW vw_executive_kpis AS
SELECT
 (SELECT COUNT(*) FROM fact_appointments) AS total_appointments,
 (SELECT COUNT(*) FROM fact_appointments WHERE status='Completed') AS completed_appointments,
 (SELECT COUNT(*) FROM fact_appointments WHERE no_show=1) AS no_show_appointments,
 (SELECT COUNT(*) FROM fact_appointments WHERE status='Cancelled') AS cancelled_appointments,
 ROUND(100.0 * (SELECT COUNT(*) FROM fact_appointments WHERE no_show=1) / NULLIF((SELECT COUNT(*) FROM fact_appointments WHERE status IN ('Completed','No-show')),0),2) AS no_show_rate_pct,
 (SELECT COUNT(*) FROM fact_encounters) AS total_encounters,
 (SELECT COALESCE(SUM(billed_amount),0) FROM fact_billing) AS total_billed_amount,
 (SELECT COALESCE(SUM(insurance_paid + patient_paid),0) FROM fact_billing) AS total_collected_amount,
 (SELECT COALESCE(SUM(outstanding_amount),0) FROM fact_billing) AS total_outstanding_amount,
 ROUND(100.0 * (SELECT COALESCE(SUM(insurance_paid + patient_paid),0) FROM fact_billing) / NULLIF((SELECT COALESCE(SUM(billed_amount),0) FROM fact_billing),0),2) AS collection_rate_pct,
 (SELECT AVG(wait_time_minutes) FROM fact_encounters) AS avg_wait_minutes,
 (SELECT AVG(satisfaction_score) FROM fact_patient_feedback) AS avg_satisfaction_score,
 ROUND(100.0 * (SELECT SUM(readmission_30d_flag) FROM fact_encounters WHERE admission_flag=1) / NULLIF((SELECT COUNT(*) FROM fact_encounters WHERE admission_flag=1),0),2) AS readmission_rate_pct;

CREATE OR REPLACE VIEW vw_hospital_performance AS
WITH e AS (SELECT hospital_id, COUNT(*) total_encounters, AVG(wait_time_minutes) avg_wait_minutes, AVG(consultation_time_minutes) avg_consultation_minutes,
                  ROUND(100.0*SUM(readmission_30d_flag)::numeric/NULLIF(SUM(admission_flag),0),2) readmission_rate_pct
           FROM fact_encounters GROUP BY hospital_id),
b AS (SELECT hospital_id, SUM(billed_amount) billed_amount, SUM(insurance_paid+patient_paid) collected_amount, SUM(outstanding_amount) outstanding_amount
      FROM fact_billing GROUP BY hospital_id),
f AS (SELECT hospital_id, AVG(satisfaction_score) avg_satisfaction_score FROM fact_patient_feedback GROUP BY hospital_id)
SELECT h.hospital_id,h.hospital_name,h.city,h.state,h.hospital_type,h.bed_capacity,
       e.total_encounters, ROUND(100.0*e.total_encounters/SUM(e.total_encounters) OVER (),2) encounter_share_pct,
       e.avg_wait_minutes,e.avg_consultation_minutes,b.billed_amount,b.collected_amount,b.outstanding_amount,
       ROUND(100.0*b.collected_amount/NULLIF(b.billed_amount,0),2) collection_rate_pct,f.avg_satisfaction_score,e.readmission_rate_pct
FROM dim_hospital h JOIN e USING(hospital_id) JOIN b USING(hospital_id) LEFT JOIN f USING(hospital_id);

CREATE OR REPLACE VIEW vw_no_show_analysis AS
SELECT 'Booking Channel' AS analysis_dimension, booking_channel AS category,
       COUNT(*) FILTER (WHERE status IN ('Completed','No-show')) AS eligible_appointments,
       COUNT(*) FILTER (WHERE no_show=1) AS no_show_count,
       ROUND(100.0*COUNT(*) FILTER (WHERE no_show=1)/NULLIF(COUNT(*) FILTER (WHERE status IN ('Completed','No-show')),0),2) AS no_show_rate_pct
FROM fact_appointments GROUP BY booking_channel;

CREATE OR REPLACE VIEW vw_patient_experience AS
SELECT CASE WHEN e.wait_time_minutes < 45 THEN '<45 min'
            WHEN e.wait_time_minutes < 60 THEN '45-59 min'
            WHEN e.wait_time_minutes < 75 THEN '60-74 min'
            ELSE '75+ min' END AS wait_category,
       COUNT(*) feedback_count, AVG(f.satisfaction_score) avg_satisfaction_score, AVG(f.overall_rating) avg_overall_rating,
       AVG(f.doctor_rating) avg_doctor_rating, AVG(f.wait_time_rating) avg_wait_time_rating, AVG(f.service_rating) avg_service_rating,
       SUM(CASE WHEN f.complaint_flag THEN 1 ELSE 0 END) complaint_count,
       ROUND(100.0*SUM(CASE WHEN f.complaint_flag THEN 1 ELSE 0 END)/NULLIF(COUNT(*),0),2) complaint_rate_pct
FROM fact_patient_feedback f JOIN fact_encounters e USING(encounter_id)
GROUP BY 1;

CREATE OR REPLACE VIEW vw_readmission AS
SELECT d.diagnosis_id,d.diagnosis_name,d.diagnosis_category,
       COUNT(*) FILTER (WHERE e.admission_flag=1) total_admissions,
       SUM(CASE WHEN e.admission_flag=1 THEN e.readmission_30d_flag ELSE 0 END) readmissions_30d,
       ROUND(100.0*SUM(CASE WHEN e.admission_flag=1 THEN e.readmission_30d_flag ELSE 0 END)/NULLIF(COUNT(*) FILTER (WHERE e.admission_flag=1),0),2) readmission_rate_pct
FROM fact_encounters e JOIN dim_diagnosis d USING(diagnosis_id)
GROUP BY d.diagnosis_id,d.diagnosis_name,d.diagnosis_category;

CREATE OR REPLACE VIEW vw_revenue_collections AS
SELECT 'Encounter Type' AS analysis_level, encounter_type AS category_id, encounter_type AS category_name, COUNT(*) total_bills,
       SUM(billed_amount) billed_amount, SUM(approved_amount) approved_amount, SUM(insurance_paid+patient_paid) collected_amount,
       SUM(outstanding_amount) outstanding_amount, ROUND(100.0*SUM(insurance_paid+patient_paid)/NULLIF(SUM(billed_amount),0),2) collection_rate_pct
FROM fact_billing GROUP BY encounter_type;
