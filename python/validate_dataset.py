from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
EXPECTED = {
    "dim_date.csv": 731, "dim_hospital.csv": 8, "dim_department.csv": 44, "dim_doctor.csv": 600,
    "dim_patient.csv": 100000, "fact_appointments.csv": 500000, "fact_encounters.csv": 300000,
    "fact_billing.csv": 300000, "fact_patient_feedback.csv": 210000,
}

for name, expected in EXPECTED.items():
    rows = sum(1 for _ in open(DATA/name, encoding="utf-8")) - 1
    print(f"{name}: {rows:,} rows | expected {expected:,} | {'PASS' if rows == expected else 'CHECK'}")

b = pd.read_csv(DATA/"fact_billing.csv")
financial_error = (b["billed_amount"] - (b["insurance_paid"] + b["patient_paid"] + b["outstanding_amount"] + b["financial_difference"])).abs().gt(0.01).sum()
print(f"Billing financial consistency failures: {financial_error}")

a = pd.read_csv(DATA/"fact_appointments.csv")
print("No-show consistency failures:", int(((a["no_show"] == 1) != (a["status"] == "No-show")).sum()))
