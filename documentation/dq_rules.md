# Data Quality Rules

## Structural
- Row counts must match expected portfolio volumes.
- Primary identifiers must be unique within their dimension/fact grain where applicable.
- Required foreign keys should resolve to the corresponding dimension where the business rule requires it.

## Completeness
- Missing patient insurance is intentional and represents uninsured patients.
- Missing appointment cancellation reason is expected for non-cancelled appointments.
- Missing billing insurance is intentional for uninsured encounters.

## Business rules
- Appointment dates cannot precede patient registration.
- No-show flag must agree with appointment status.
- Billing consistency: billed = insurance_paid + patient_paid + outstanding_amount + financial_difference where the source definition requires the financial difference field.
- Readmission flag is evaluated using the 30-day business rule.
- Negative wait/consultation durations are invalid.

## Validation philosophy
Intentional missingness is documented rather than blindly imputed. Validation is performed before analytical aggregation.
