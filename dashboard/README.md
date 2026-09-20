# MediCore Interactive Dashboard

This folder contains the deployable Plotly Dash application for the MediCore Healthcare Analytics portfolio project.

## Live dashboard

https://web-production-d29b6.up.railway.app/

## Management views

1. Executive Overview
2. Hospital Performance
3. No-show Analysis
4. Patient Experience
5. Readmission & Risk
6. Revenue & Collections

## Global filters

The application supports:

- Hospital
- Department
- Year
- Encounter type

The dashboard reads validated synthetic CSV files from `data/raw` and does not modify the source data.

## Run locally

From the project root:

```bash
pip install -r requirements.txt
python dashboard/app.py
```

Open:

```text
http://127.0.0.1:8050
```

## Application design

`dashboard/app.py` contains the page navigation, filter logic, KPI calculations, charts, and tables.

The web dashboard exists alongside Power BI for a specific portfolio reason:

- **Power BI** demonstrates enterprise reporting and semantic/report-layer skills.
- **Plotly Dash** makes the analytical work directly accessible through a deployed web application.

This avoids duplicating the same responsibility across tools while allowing reviewers to inspect the project without requiring Power BI Desktop.
