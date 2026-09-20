# MediCore — KPI Definitions

> Synthetic portfolio data. Definitions below document the business logic used by the project.

## Appointment KPIs

### Total Appointments
**Definition:** Count of appointment records after the selected dashboard filters.

### No-show Rate
**Definition:** No-show appointments divided by appointments eligible for the no-show calculation.

**Eligible base:** appointments whose status is either `Completed` or `No-show`.

```text
No-show Rate = No-show Appointments / (Completed + No-show Appointments) × 100
```

Cancelled appointments are excluded from this KPI denominator.

## Encounter KPIs

### Total Encounters
**Definition:** Count of encounter records after the selected filters.

### Average Wait Time
**Definition:** Mean of `wait_time_minutes` across filtered encounter records.

```text
Average Wait Time = Sum of Wait Time Minutes / Encounter Count
```

## Revenue KPIs

### Total Billed
**Definition:** Sum of `billed_amount`.

### Total Collected
**Definition:** Sum of insurance payments plus patient payments.

```text
Total Collected = Σ insurance_paid + Σ patient_paid
```

### Outstanding Amount
**Definition:** Sum of `outstanding_amount`.

### Collection Rate
**Definition:** Collected amount divided by billed amount.

```text
Collection Rate = Total Collected / Total Billed × 100
```

The project compares both percentage collection performance and absolute outstanding exposure because similar collection rates can still produce materially different financial exposure at different volumes.

## Patient Experience KPIs

### Average Patient Satisfaction
**Definition:** Mean of `satisfaction_score` across filtered patient-feedback records.

### Complaint Rate
**Definition:** Feedback records flagged as complaints divided by total feedback records for the evaluated segment.

## Readmission KPIs

### 30-Day Readmission Rate
**Definition:** Readmitted admissions divided by all admission encounters.

**Eligible base:** encounters where `admission_flag = true`.

```text
30-Day Readmission Rate =
Admissions with readmission_30d_flag = true
/
All Admissions
× 100
```

The metric is intentionally evaluated on admissions only, not all encounters.

## Interpretation principles

- KPI values are evaluated at the grain of their corresponding fact table.
- Dashboard filters change the eligible population before KPI aggregation.
- Association is not interpreted as causation.
- Statistical significance is considered alongside effect size and business relevance.
- Synthetic results are portfolio demonstrations and are not real healthcare benchmarks.
