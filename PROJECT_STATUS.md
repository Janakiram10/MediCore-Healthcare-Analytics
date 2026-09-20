# Project Completion Status

## Status: COMPLETE — MNC-ready portfolio baseline

### Completed analytical foundation

- Business requirements and stakeholder scope
- Star-schema analytical model
- Synthetic dimensions and fact datasets
- PostgreSQL database setup and analytical views
- Data-quality validation rules and validation queries
- No-show statistical analysis
- Revenue and collections analysis
- Operations and wait-time analysis
- Patient-experience analysis
- 30-day readmission analysis
- Power BI Executive Overview
- Plotly Dash interactive management application
- Six management dashboard views
- Global hospital, department, year, and encounter-type filters
- Business-insight documentation
- KPI-definition documentation
- Reproducibility instructions
- Credential sanitization for the database-backed analysis notebook
- Repository organization cleanup

### Deliberately not added

- Extra ML models after the no-show analysis showed limited explanatory power
- Decorative dashboard pages without a business purpose
- Unsupported causal claims
- Unnecessary healthcare tables that do not support the defined analysis
- Fabricated business-impact claims such as percentage improvements not measured by the dataset

### Portfolio positioning

The project is designed as an end-to-end Data Analyst case study where each technology has a distinct role:

- PostgreSQL — modelling, validation, business logic, analytical views
- Python — validation and statistical analysis
- Power BI — enterprise-style executive reporting
- Plotly Dash — deployed interactive portfolio experience

### Local user actions

For Power BI, open `MediCore_Healthcare_Analytics.pbip` and refresh the PostgreSQL connection if necessary.

For the Dash app, run `python dashboard/app.py` from the repository root.
