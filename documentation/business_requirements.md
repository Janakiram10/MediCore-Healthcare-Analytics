# MediCore Health Network — Business Requirements

## Objective
Create a centralized healthcare analytics solution for executive, operations, finance, patient-experience, and clinical decision support.

## Stakeholders
CEO, CFO, COO, hospital managers, department heads, finance, patient experience, operations, and analytics teams.

## Core business questions
- Which hospitals and departments carry the highest patient volume?
- Where are waiting-time pressures highest?
- How are billed, collected, and outstanding amounts distributed?
- Which insurance segments have collection-risk exposure?
- How does waiting time relate to patient satisfaction?
- Which diagnosis groups show higher 30-day readmission rates?
- Which appointment segments have higher no-show exposure?

## Scope
The portfolio solution uses synthetic data for 8 hospitals, 44 departments, 600 doctors, 100,000 patients, 500,000 appointments, 300,000 encounters, 300,000 billing records, and 210,000 feedback records.

## Success criteria
1. Reproducible PostgreSQL analytical views.
2. Explicit data-quality rules and validation.
3. Executive Power BI dashboard using the validated views.
4. Business findings documented with no unsupported causal claims.
5. Project structure suitable for GitHub portfolio review.
