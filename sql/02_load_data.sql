-- Run from psql after connecting to medicore_healthcare.
-- Update the Windows path to the local project folder before execution.

\copy dim_date FROM 'C:/Users/janak/MediCore_Healthcare_Analytics/data/raw/dim_date.csv' WITH (FORMAT csv, HEADER true);
\copy dim_hospital FROM 'C:/Users/janak/MediCore_Healthcare_Analytics/data/raw/dim_hospital.csv' WITH (FORMAT csv, HEADER true);
\copy dim_department FROM 'C:/Users/janak/MediCore_Healthcare_Analytics/data/raw/dim_department.csv' WITH (FORMAT csv, HEADER true);
\copy dim_doctor FROM 'C:/Users/janak/MediCore_Healthcare_Analytics/data/raw/dim_doctor.csv' WITH (FORMAT csv, HEADER true);
\copy dim_patient FROM 'C:/Users/janak/MediCore_Healthcare_Analytics/data/raw/dim_patient.csv' WITH (FORMAT csv, HEADER true);
\copy dim_insurance FROM 'C:/Users/janak/MediCore_Healthcare_Analytics/data/raw/dim_insurance.csv' WITH (FORMAT csv, HEADER true);
\copy dim_diagnosis FROM 'C:/Users/janak/MediCore_Healthcare_Analytics/data/raw/dim_diagnosis.csv' WITH (FORMAT csv, HEADER true);
\copy fact_appointments FROM 'C:/Users/janak/MediCore_Healthcare_Analytics/data/raw/fact_appointments.csv' WITH (FORMAT csv, HEADER true);
\copy fact_encounters FROM 'C:/Users/janak/MediCore_Healthcare_Analytics/data/raw/fact_encounters.csv' WITH (FORMAT csv, HEADER true);
\copy fact_billing FROM 'C:/Users/janak/MediCore_Healthcare_Analytics/data/raw/fact_billing.csv' WITH (FORMAT csv, HEADER true);
\copy fact_patient_feedback FROM 'C:/Users/janak/MediCore_Healthcare_Analytics/data/raw/fact_patient_feedback.csv' WITH (FORMAT csv, HEADER true);
