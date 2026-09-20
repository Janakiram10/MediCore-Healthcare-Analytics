# MediCore Dash Dashboard

This is the primary interactive dashboard for the MediCore Healthcare Analytics portfolio project.

## Run

From the project root:

```bash
pip install -r dashboard/requirements.txt
python dashboard/app.py
```

Then open `http://127.0.0.1:8050`.

## Design

One Python file (`dashboard/app.py`) contains the complete dashboard, navigation, filters, KPI cards, charts, and tables.

Sections:

1. Executive Overview
2. Hospital Performance
3. No-show Analysis
4. Patient Experience
5. Readmission & Risk
6. Revenue & Collections

The dashboard reads the validated CSV files in `data/raw` and does not modify them.
