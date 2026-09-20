-- MediCore Health Network
-- PostgreSQL reference schema. Synthetic portfolio data.

CREATE DATABASE medicore_healthcare;
-- Connect to medicore_healthcare before running the remaining statements.

CREATE TABLE IF NOT EXISTS dim_date (
    date_id integer PRIMARY KEY, full_date date, year integer, quarter varchar(10), month integer,
    month_name varchar(20), week integer, day integer, day_name varchar(20), is_weekend boolean, financial_year varchar(20)
);
CREATE TABLE IF NOT EXISTS dim_hospital (
    hospital_id varchar(10) PRIMARY KEY, hospital_name varchar(150), city varchar(100), state varchar(100),
    hospital_type varchar(50), bed_capacity integer, opening_year integer
);
CREATE TABLE IF NOT EXISTS dim_department (
    department_id varchar(10) PRIMARY KEY, department_name varchar(150), department_category varchar(100),
    hospital_id varchar(10), capacity_per_day integer
);
CREATE TABLE IF NOT EXISTS dim_doctor (
    doctor_id varchar(20) PRIMARY KEY, doctor_name varchar(150), specialization varchar(150), department_id varchar(10),
    hospital_id varchar(10), experience_years integer, employment_type varchar(50), joining_date date, doctor_status varchar(50)
);
CREATE TABLE IF NOT EXISTS dim_patient (
    patient_id varchar(20) PRIMARY KEY, first_name varchar(100), last_name varchar(100), gender varchar(20),
    date_of_birth date, city varchar(100), state varchar(100), registration_date date, insurance_id varchar(20), patient_status varchar(50)
);
CREATE TABLE IF NOT EXISTS dim_insurance (
    insurance_id varchar(20) PRIMARY KEY, insurance_provider varchar(150), plan_type varchar(100),
    coverage_percentage numeric(5,2), claim_processing_days integer, insurance_status varchar(50)
);
CREATE TABLE IF NOT EXISTS dim_diagnosis (
    diagnosis_id varchar(20) PRIMARY KEY, diagnosis_code varchar(20), diagnosis_name varchar(150), diagnosis_category varchar(100)
);

CREATE TABLE IF NOT EXISTS fact_appointments (
    appointment_id varchar(30) PRIMARY KEY, patient_id varchar(20), doctor_id varchar(20), department_id varchar(10), hospital_id varchar(10),
    appointment_type varchar(50), booking_channel varchar(50), lead_time_days integer, status varchar(30), no_show integer,
    cancellation_reason varchar(150), scheduled_datetime timestamp, insurance_id varchar(20), appointment_date_id integer
);
CREATE TABLE IF NOT EXISTS fact_encounters (
    encounter_id varchar(30) PRIMARY KEY, appointment_id varchar(30), patient_id varchar(20), doctor_id varchar(20), department_id varchar(10),
    hospital_id varchar(10), appointment_date_id integer, scheduled_datetime timestamp, encounter_type varchar(30), diagnosis_id varchar(20),
    arrival_datetime timestamp, consultation_start_datetime timestamp, wait_time_minutes integer, consultation_time_minutes integer,
    discharge_datetime timestamp, admission_flag integer, discharge_status varchar(50), readmission_30d_flag integer
);
CREATE TABLE IF NOT EXISTS fact_billing (
    bill_id varchar(30) PRIMARY KEY, encounter_id varchar(30), patient_id varchar(20), hospital_id varchar(10), department_id varchar(10),
    insurance_id varchar(20), encounter_type varchar(30), diagnosis_id varchar(20), billed_amount numeric(14,2), coverage_percentage numeric(5,2),
    approved_amount numeric(14,2), insurance_paid numeric(14,2), patient_paid numeric(14,2), outstanding_amount numeric(14,2),
    payment_status varchar(50), claim_status varchar(50), discharge_datetime_x timestamp, discharge_datetime_y timestamp, discharge_datetime timestamp,
    bill_date timestamp, bill_date_id integer, full_date date, financial_difference numeric(14,2)
);
CREATE TABLE IF NOT EXISTS fact_patient_feedback (
    feedback_id varchar(30) PRIMARY KEY, encounter_id varchar(30), patient_id varchar(20), doctor_id varchar(20), department_id varchar(10),
    hospital_id varchar(10), feedback_date_id integer, overall_rating integer, doctor_rating integer, wait_time_rating integer,
    service_rating integer, satisfaction_score numeric(10,2), complaint_flag boolean, feedback_channel varchar(50)
);
