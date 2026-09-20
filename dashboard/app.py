import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html, dash_table

# ============================================================
# MediCore Healthcare Analytics
# Single-file Plotly Dash portfolio dashboard
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"

COLORS = {
    "navy": "#0B1F3A",
    "blue": "#1769AA",
    "cyan": "#00A6C7",
    "green": "#1F9D72",
    "orange": "#E38B2C",
    "red": "#D9534F",
    "purple": "#6F52A3",
    "bg": "#F4F7FB",
    "card": "#FFFFFF",
    "text": "#182433",
    "muted": "#6B7785",
    "border": "#E1E7EF",
}


def money_cr(x):
    return f"₹{x / 1e7:,.2f} Cr"


def pct(x):
    return f"{x:.2f}%"


def safe_div(a, b):
    return (a / b * 100) if b else 0.0


def load_csv(name, usecols=None, parse_dates=None):
    path = RAW_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing dataset: {path}")
    return pd.read_csv(path, usecols=usecols, parse_dates=parse_dates)


# ------------------------------------------------------------
# Data loading
# ------------------------------------------------------------

date = load_csv("dim_date.csv")
hospital = load_csv("dim_hospital.csv")
department = load_csv("dim_department.csv")
diagnosis = load_csv("dim_diagnosis.csv")
insurance = load_csv("dim_insurance.csv")

appointments = load_csv("fact_appointments.csv", parse_dates=["scheduled_datetime"])
encounters = load_csv("fact_encounters.csv", parse_dates=[
    "scheduled_datetime", "arrival_datetime", "consultation_start_datetime", "discharge_datetime"
])
billing = load_csv("fact_billing.csv", parse_dates=["discharge_datetime", "bill_date", "full_date"])
feedback = load_csv("fact_patient_feedback.csv")

# Small dimensions for readable labels.
hosp_map = hospital.set_index("hospital_id")["hospital_name"].to_dict()
dept_map = department.set_index("department_id")["department_name"].to_dict()
diag_map = diagnosis.set_index("diagnosis_id")["diagnosis_name"].to_dict()
ins_map = insurance.set_index("insurance_id")["insurance_provider"].to_dict()

# Date maps. The source data has date_id as the business key.
date_small = date[["date_id", "full_date", "year", "month", "month_name", "quarter"]].copy()
date_small["full_date"] = pd.to_datetime(date_small["full_date"], errors="coerce")
date_map_year = date_small.set_index("date_id")["year"].to_dict()
date_map_full = date_small.set_index("date_id")["full_date"].to_dict()

appointments["year"] = appointments["appointment_date_id"].map(date_map_year)
appointments["hospital_name"] = appointments["hospital_id"].map(hosp_map)
appointments["department_name"] = appointments["department_id"].map(dept_map)

encounters["year"] = encounters["appointment_date_id"].map(date_map_year)
encounters["hospital_name"] = encounters["hospital_id"].map(hosp_map)
encounters["department_name"] = encounters["department_id"].map(dept_map)
encounters["diagnosis_name"] = encounters["diagnosis_id"].map(diag_map)

billing["year"] = billing["bill_date_id"].map(date_map_year)
billing["hospital_name"] = billing["hospital_id"].map(hosp_map)
billing["department_name"] = billing["department_id"].map(dept_map)
billing["insurance_provider"] = billing["insurance_id"].map(ins_map).fillna("Uninsured")

feedback["year"] = feedback["feedback_date_id"].map(date_map_year)
feedback["hospital_name"] = feedback["hospital_id"].map(hosp_map)
feedback["department_name"] = feedback["department_id"].map(dept_map)

# Feedback needs wait time from its encounter.
wait_lookup = encounters[["encounter_id", "wait_time_minutes"]]
feedback = feedback.merge(wait_lookup, on="encounter_id", how="left")
feedback["wait_category"] = pd.cut(
    feedback["wait_time_minutes"],
    bins=[-np.inf, 44.999, 59.999, 74.999, np.inf],
    labels=["<45 min", "45–59 min", "60–74 min", "75+ min"],
)

# Useful derived fields.
appointments["eligible_no_show"] = appointments["status"].isin(["Completed", "No-show"])
appointments["lead_time_band"] = pd.cut(
    appointments["lead_time_days"],
    bins=[-np.inf, 0, 3, 7, 14, 30, np.inf],
    labels=["Same day", "1–3 days", "4–7 days", "8–14 days", "15–30 days", "31+ days"],
)

# Readmission rate is defined on admissions only.
encounters["admission_flag"] = encounters["admission_flag"].astype(str).str.lower().isin(["true", "1", "yes"])
encounters["readmission_30d_flag"] = encounters["readmission_30d_flag"].astype(str).str.lower().isin(["true", "1", "yes"])

# Normalize complaint flag.
feedback["complaint_flag"] = feedback["complaint_flag"].astype(str).str.lower().isin(["true", "1", "yes"])

YEARS = sorted([int(x) for x in pd.Series(date["year"]).dropna().unique()])
HOSPITALS = sorted(hospital["hospital_name"].dropna().unique().tolist())
DEPARTMENTS = sorted(department["department_name"].dropna().unique().tolist())
ENCOUNTER_TYPES = sorted(encounters["encounter_type"].dropna().unique().tolist())

# ------------------------------------------------------------
# Filtering helpers
# ------------------------------------------------------------

def apply_filter(df, hospital_name, department_name, year):
    out = df
    if hospital_name and hospital_name != "All Hospitals" and "hospital_name" in out.columns:
        out = out[out["hospital_name"] == hospital_name]
    if department_name and department_name != "All Departments" and "department_name" in out.columns:
        out = out[out["department_name"] == department_name]
    if year and year != "All Years" and "year" in out.columns:
        out = out[out["year"] == int(year)]
    return out


def apply_encounter_type(df, encounter_type):
    if encounter_type and encounter_type != "All Encounter Types" and "encounter_type" in df.columns:
        return df[df["encounter_type"] == encounter_type]
    return df


def kpi_values(hn, dn, yr, et):
    a = apply_filter(appointments, hn, dn, yr)
    e = apply_encounter_type(apply_filter(encounters, hn, dn, yr), et)
    b = apply_encounter_type(apply_filter(billing, hn, dn, yr), et)
    f = apply_filter(feedback, hn, dn, yr)

    eligible = a[a["eligible_no_show"]]
    admissions = e[e["admission_flag"]]

    billed = b["billed_amount"].sum()
    collected = b["insurance_paid"].sum() + b["patient_paid"].sum()
    outstanding = b["outstanding_amount"].sum()

    return {
        "appointments": len(a),
        "encounters": len(e),
        "billed": billed,
        "collected": collected,
        "outstanding": outstanding,
        "collection_rate": safe_div(collected, billed),
        "no_show_rate": safe_div(eligible["no_show"].astype(bool).sum(), len(eligible)),
        "satisfaction": f["satisfaction_score"].mean() if len(f) else 0,
        "wait": e["wait_time_minutes"].mean() if len(e) else 0,
        "readmission_rate": safe_div(admissions["readmission_30d_flag"].sum(), len(admissions)),
    }


# ------------------------------------------------------------
# Plot helpers
# ------------------------------------------------------------

def base_layout(fig, title=None, height=330):
    fig.update_layout(
        title=title,
        height=height,
        margin=dict(l=20, r=20, t=55 if title else 20, b=45),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=COLORS["text"], family="Arial"),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, linecolor="#DDE3EA")
    fig.update_yaxes(gridcolor="#EDF1F5", zeroline=False)
    return fig


def empty_fig(message="No data for the selected filters"):
    fig = go.Figure()
    fig.add_annotation(text=message, x=0.5, y=0.5, showarrow=False, font=dict(size=16, color=COLORS["muted"]))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(height=330, paper_bgcolor="white", plot_bgcolor="white", margin=dict(l=10, r=10, t=20, b=10))
    return fig


def card(label, value, accent=COLORS["blue"]):
    return html.Div([
        html.Div(label, className="kpi-label"),
        html.Div(value, className="kpi-value", style={"borderLeft": f"4px solid {accent}", "paddingLeft": "12px"}),
    ], className="kpi-card")


def page_header(title, subtitle):
    return html.Div([
        html.H1(title, className="page-title"),
        html.Div(subtitle, className="page-subtitle"),
    ])


def chart_card(children):
    return html.Div(children, className="chart-card")


def table_card(title, df, page_size=10):
    return html.Div([
        html.Div(title, className="chart-title"),
        dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": c, "id": c} for c in df.columns],
            page_size=page_size,
            sort_action="native",
            style_table={"overflowX": "auto"},
            style_header={"backgroundColor": "#F0F4F8", "fontWeight": "700", "color": COLORS["text"], "border": "none"},
            style_cell={"padding": "10px", "fontFamily": "Arial", "fontSize": "13px", "border": "none", "borderBottom": "1px solid #EDF1F5"},
        ),
    ], className="chart-card")


# ------------------------------------------------------------
# App
# ------------------------------------------------------------

app = Dash(__name__, title="MediCore Healthcare Analytics")
server = app.server

app.index_string = """
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
        * { box-sizing: border-box; }
        body { margin: 0; font-family: Arial, sans-serif; background: #F4F7FB; color: #182433; }
        .app-shell { display: flex; min-height: 100vh; }
        .sidebar { width: 245px; background: #0B1F3A; color: white; padding: 22px 14px; position: fixed; top: 0; bottom: 0; left: 0; }
        .brand { font-size: 23px; font-weight: 800; padding: 0 12px 4px; }
        .brand-sub { color: #B9C7D8; font-size: 12px; padding: 0 12px 24px; }
        .nav-title { color: #7F93AC; font-size: 10px; text-transform: uppercase; letter-spacing: 1.2px; padding: 0 12px 9px; }
        .nav-btn { width: 100%; text-align: left; border: 0; background: transparent; color: #D7E0EA; padding: 11px 12px; margin: 2px 0; border-radius: 8px; cursor: pointer; font-size: 13px; }
        .nav-btn:hover { background: #17345B; }
        .nav-active { background: #1769AA !important; color: white !important; }
        .main { margin-left: 245px; width: calc(100% - 245px); padding: 24px 30px 40px; }
        .topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .synthetic { font-size: 11px; background: #E9F3FA; color: #1769AA; padding: 7px 10px; border-radius: 999px; font-weight: 700; }
        .filters { display: grid; grid-template-columns: 1.2fr 1.2fr .7fr 1fr; gap: 12px; background: white; padding: 15px; border: 1px solid #E1E7EF; border-radius: 12px; margin-bottom: 20px; }
        .filter-label { font-size: 11px; font-weight: 700; color: #6B7785; margin-bottom: 5px; }
        .page-title { font-size: 27px; margin: 0 0 5px; }
        .page-subtitle { color: #6B7785; font-size: 13px; margin-bottom: 20px; }
        .kpis { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 12px; }
        .kpi-card { background: white; border: 1px solid #E1E7EF; border-radius: 12px; padding: 15px 14px; min-height: 92px; }
        .kpi-label { color: #6B7785; font-size: 11px; font-weight: 700; margin-bottom: 9px; text-transform: uppercase; letter-spacing: .25px; }
        .kpi-value { font-size: 23px; font-weight: 800; white-space: nowrap; }
        .chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
        .chart-card { background: white; border: 1px solid #E1E7EF; border-radius: 12px; padding: 10px 12px 12px; margin-bottom: 14px; }
        .chart-title { font-weight: 800; font-size: 14px; padding: 8px 5px 3px; }
        .insight { background: #FFFFFF; border-left: 4px solid #1769AA; border-radius: 10px; padding: 13px 15px; border-top: 1px solid #E1E7EF; border-right: 1px solid #E1E7EF; border-bottom: 1px solid #E1E7EF; margin-bottom: 8px; font-size: 13px; line-height: 1.45; }
        .section-heading { font-size: 16px; font-weight: 800; margin: 18px 0 10px; }
        @media (max-width: 1100px) { .kpis { grid-template-columns: repeat(2, 1fr); } .filters { grid-template-columns: 1fr 1fr; } .chart-grid { grid-template-columns: 1fr; } .sidebar { width: 205px; } .main { margin-left: 205px; width: calc(100% - 205px); } }
    </style>
</head>
<body>
{%app_entry%}
<footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>
"""


def nav_button(label, value, active):
    return html.Button(label, id=f"nav-{value}", n_clicks=0, className="nav-btn nav-active" if active else "nav-btn")


app.layout = html.Div([
    dcc.Store(id="page-store", data="Executive Overview"),
    html.Div([
        html.Div([
            html.Div("♥ MediCore", className="brand"),
            html.Div("Healthcare Analytics", className="brand-sub"),
            html.Div("DASHBOARD", className="nav-title"),
            nav_button("Executive Overview", "exec", True),
            nav_button("Hospital Performance", "hospital", False),
            nav_button("No-show Analysis", "noshow", False),
            nav_button("Patient Experience", "experience", False),
            nav_button("Readmission & Risk", "readmission", False),
            nav_button("Revenue & Collections", "revenue", False),
            html.Div(style={"height": "25px"}),
            html.Div("PORTFOLIO", className="nav-title"),
            html.Div("Synthetic healthcare case study", style={"fontSize": "11px", "color": "#7F93AC", "padding": "0 12px", "lineHeight": "1.5"}),
        ], className="sidebar"),
        html.Div([
            html.Div([
                html.Div("MediCore Healthcare Network", style={"fontWeight": "800", "fontSize": "15px"}),
                html.Div("Healthcare Revenue • Patient Flow • Operations • Experience", style={"fontSize": "12px", "color": COLORS["muted"]}),
            ], className="topbar"),
            html.Div("Synthetic portfolio data — insights are based on the validated MediCore dataset", className="synthetic"),
            html.Div(style={"height": "12px"}),
            html.Div([
                html.Div([html.Div("Hospital", className="filter-label"), dcc.Dropdown(["All Hospitals"] + HOSPITALS, "All Hospitals", id="filter-hospital", clearable=False)]),
                html.Div([html.Div("Department", className="filter-label"), dcc.Dropdown(["All Departments"] + DEPARTMENTS, "All Departments", id="filter-department", clearable=False)]),
                html.Div([html.Div("Year", className="filter-label"), dcc.Dropdown(["All Years"] + YEARS, "All Years", id="filter-year", clearable=False)]),
                html.Div([html.Div("Encounter Type", className="filter-label"), dcc.Dropdown(["All Encounter Types"] + ENCOUNTER_TYPES, "All Encounter Types", id="filter-encounter", clearable=False)]),
            ], className="filters"),
            html.Div(id="page-content"),
        ], className="main"),
    ], className="app-shell"),
])


# Navigation callback: one file, one app, six dashboard sections.
@app.callback(
    Output("page-store", "data"),
    [Input("nav-exec", "n_clicks"), Input("nav-hospital", "n_clicks"), Input("nav-noshow", "n_clicks"),
     Input("nav-experience", "n_clicks"), Input("nav-readmission", "n_clicks"), Input("nav-revenue", "n_clicks")],
    prevent_initial_call=True,
)
def navigate(*clicks):
    from dash import ctx
    mapping = {
        "nav-exec": "Executive Overview",
        "nav-hospital": "Hospital Performance",
        "nav-noshow": "No-show Analysis",
        "nav-experience": "Patient Experience",
        "nav-readmission": "Readmission & Risk",
        "nav-revenue": "Revenue & Collections",
    }
    return mapping.get(ctx.triggered_id, "Executive Overview")


@app.callback(
    Output("page-content", "children"),
    [Input("page-store", "data"), Input("filter-hospital", "value"), Input("filter-department", "value"), Input("filter-year", "value"), Input("filter-encounter", "value")],
)
def render_page(page, hn, dn, yr, et):
    k = kpi_values(hn, dn, yr, et)
    common = page_header(page, "Interactive management view with hospital, department, year and encounter-type filters")

    if page == "Executive Overview":
        a = apply_filter(appointments, hn, dn, yr)
        e = apply_encounter_type(apply_filter(encounters, hn, dn, yr), et)
        b = apply_encounter_type(apply_filter(billing, hn, dn, yr), et)
        f = apply_filter(feedback, hn, dn, yr)
        ad = a[a["eligible_no_show"]]

        h_enc = e.groupby("hospital_name", as_index=False).size().rename(columns={"size": "encounters"}).sort_values("encounters", ascending=False)
        h_bill = b.groupby("hospital_name", as_index=False)["billed_amount"].sum().sort_values("billed_amount", ascending=False)
        h_out = b.groupby("hospital_name", as_index=False)["outstanding_amount"].sum().sort_values("outstanding_amount", ascending=False)
        ns = ad.groupby("booking_channel", as_index=False)["no_show"].sum().sort_values("no_show", ascending=False)
        ex = f.groupby("wait_category", observed=True, as_index=False).agg(satisfaction=("satisfaction_score", "mean"), complaint_rate=("complaint_flag", "mean"))
        ex["complaint_rate"] *= 100
        rr = e[e["admission_flag"]].groupby("diagnosis_name", as_index=False).agg(readmissions=("readmission_30d_flag", "sum"), admissions=("admission_flag", "size"))
        rr["readmission_rate"] = rr["readmissions"] / rr["admissions"] * 100
        rr = rr.sort_values("readmission_rate", ascending=False)

        charts = [
            chart_card(dcc.Graph(figure=base_layout(px.bar(h_enc, x="hospital_name", y="encounters", text_auto=True), "Total Encounters by Hospital"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(h_bill, x="hospital_name", y="billed_amount", text_auto=False), "Billed Revenue by Hospital"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(h_out, x="hospital_name", y="outstanding_amount", text_auto=False), "Outstanding Amount by Hospital"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(ns, x="booking_channel", y="no_show", text_auto=True), "No-show Appointments by Category"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(ex, x="wait_category", y="satisfaction", text_auto=".1f"), "Patient Satisfaction vs Wait Time"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(rr, x="diagnosis_name", y="readmission_rate", text_auto=".2f"), "30-Day Readmission Rate by Diagnosis"))),
        ]
        for c in charts:
            try:
                fig = c.children.figure
                fig.update_xaxes(tickangle=-25)
                fig.update_traces(marker_line_width=0)
            except Exception:
                pass
        insights = [
            f"Revenue: {money_cr(k['billed'])} billed, {money_cr(k['collected'])} collected and {money_cr(k['outstanding'])} outstanding; collection rate is {pct(k['collection_rate'])}.",
            f"Patient experience: average satisfaction is {k['satisfaction']:.2f} while average encounter wait is {k['wait']:.2f} minutes.",
            f"Appointment flow: no-show rate among completed + no-show eligible appointments is {pct(k['no_show_rate'])}.",
            f"Clinical: 30-day readmission rate among admissions is {pct(k['readmission_rate'])}.",
        ]
        return html.Div([common, html.Div([
            card("Total Appointments", f"{k['appointments']:,}", COLORS["blue"]), card("Total Encounters", f"{k['encounters']:,}", COLORS["cyan"]),
            card("Total Billed Amount", money_cr(k['billed']), COLORS["purple"]), card("Total Collected Amount", money_cr(k['collected']), COLORS["green"]), card("Outstanding Amount", money_cr(k['outstanding']), COLORS["orange"]),
            card("Collection Rate", pct(k['collection_rate']), COLORS["green"]), card("No-show Rate", pct(k['no_show_rate']), COLORS["red"]), card("Patient Satisfaction", f"{k['satisfaction']:.2f}", COLORS["purple"]),
            card("Avg. Wait", f"{k['wait']:.2f} min", COLORS["orange"]), card("30-Day Readmission", pct(k['readmission_rate']), COLORS["red"]),
        ], className="kpis"), html.Div([html.Div("Validated portfolio insights", className="section-heading")] + [html.Div(x, className="insight") for x in insights], style={"marginBottom": "8px"}), html.Div(charts, className="chart-grid")])

    if page == "Hospital Performance":
        e = apply_encounter_type(apply_filter(encounters, hn, dn, yr), et)
        b = apply_encounter_type(apply_filter(billing, hn, dn, yr), et)
        f = apply_filter(feedback, hn, dn, yr)
        h = e.groupby("hospital_name").agg(encounters=("encounter_id", "count"), avg_wait=("wait_time_minutes", "mean")).reset_index()
        hb = b.groupby("hospital_name").agg(billed=("billed_amount", "sum"), collected=("insurance_paid", "sum"), outstanding=("outstanding_amount", "sum")).reset_index()
        hf = f.groupby("hospital_name").agg(satisfaction=("satisfaction_score", "mean")).reset_index()
        out = h.merge(hb, on="hospital_name", how="left").merge(hf, on="hospital_name", how="left")
        out["collection_rate"] = out.apply(lambda r: safe_div(r["collected"], r["billed"]), axis=1)
        out = out.sort_values("encounters", ascending=False)
        display = out.copy()
        display["Billed Revenue"] = display.pop("billed").map(money_cr)
        display["Collected"] = display.pop("collected").map(money_cr)
        display["Outstanding"] = display.pop("outstanding").map(money_cr)
        display["Collection Rate"] = display.pop("collection_rate").map(pct)
        display["Avg Wait (min)"] = display.pop("avg_wait").round(2)
        display["Satisfaction"] = display.pop("satisfaction").round(2)
        display = display.rename(columns={"hospital_name": "Hospital", "encounters": "Encounters"})
        return html.Div([common, table_card("Hospital scorecard", display, 8), html.Div([
            chart_card(dcc.Graph(figure=base_layout(px.bar(out, x="hospital_name", y="avg_wait", text_auto=".1f"), "Average Wait by Hospital"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(out, x="hospital_name", y="collection_rate", text_auto=".2f"), "Collection Rate by Hospital"))),
        ], className="chart-grid")])

    if page == "No-show Analysis":
        a = apply_filter(appointments, hn, dn, yr)
        a = a[a["eligible_no_show"]]
        by_channel = a.groupby("booking_channel").agg(eligible=("appointment_id", "count"), no_shows=("no_show", "sum")).reset_index()
        by_channel["no_show_rate"] = by_channel["no_shows"] / by_channel["eligible"] * 100
        by_lead = a.groupby("lead_time_band", observed=True).agg(eligible=("appointment_id", "count"), no_shows=("no_show", "sum")).reset_index()
        by_lead["no_show_rate"] = by_lead["no_shows"] / by_lead["eligible"] * 100
        return html.Div([common, html.Div([
            chart_card(dcc.Graph(figure=base_layout(px.bar(by_channel, x="booking_channel", y="no_show_rate", text_auto=".2f"), "No-show Rate by Booking Channel"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(by_lead, x="lead_time_band", y="no_show_rate", text_auto=".2f"), "No-show Rate by Lead Time"))),
        ], className="chart-grid"), table_card("No-show channel detail", by_channel.rename(columns={"booking_channel": "Booking Channel", "eligible": "Eligible Appointments", "no_shows": "No-shows", "no_show_rate": "No-show Rate (%)"}).round(2), 10)])

    if page == "Patient Experience":
        f = apply_filter(feedback, hn, dn, yr)
        if f.empty:
            return html.Div([common, chart_card(dcc.Graph(figure=empty_fig()))])
        by_wait = f.groupby("wait_category", observed=True).agg(feedback=("feedback_id", "count"), satisfaction=("satisfaction_score", "mean"), rating=("overall_rating", "mean"), complaints=("complaint_flag", "sum")).reset_index()
        by_wait["complaint_rate"] = by_wait["complaints"] / by_wait["feedback"] * 100
        by_channel = f.groupby("feedback_channel").agg(satisfaction=("satisfaction_score", "mean"), complaints=("complaint_flag", "sum"), feedback=("feedback_id", "count")).reset_index()
        by_channel["complaint_rate"] = by_channel["complaints"] / by_channel["feedback"] * 100
        return html.Div([common, html.Div([
            chart_card(dcc.Graph(figure=base_layout(px.bar(by_wait, x="wait_category", y="satisfaction", text_auto=".2f"), "Satisfaction by Wait Category"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(by_wait, x="wait_category", y="complaint_rate", text_auto=".2f"), "Complaint Rate by Wait Category"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(by_channel, x="feedback_channel", y="satisfaction", text_auto=".2f"), "Satisfaction by Feedback Channel"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(by_channel, x="feedback_channel", y="complaint_rate", text_auto=".2f"), "Complaint Rate by Feedback Channel"))),
        ], className="chart-grid"), table_card("Patient experience detail", by_wait.rename(columns={"wait_category": "Wait Category", "feedback": "Feedback", "satisfaction": "Satisfaction", "rating": "Overall Rating", "complaints": "Complaints", "complaint_rate": "Complaint Rate (%)"}).round(2), 8)])

    if page == "Readmission & Risk":
        e = apply_encounter_type(apply_filter(encounters, hn, dn, yr), et)
        ad = e[e["admission_flag"]]
        by_diag = ad.groupby("diagnosis_name").agg(admissions=("encounter_id", "count"), readmissions=("readmission_30d_flag", "sum")).reset_index()
        by_diag["readmission_rate"] = by_diag["readmissions"] / by_diag["admissions"] * 100
        by_diag = by_diag.sort_values("readmission_rate", ascending=False)
        return html.Div([common, chart_card(dcc.Graph(figure=base_layout(px.bar(by_diag, x="diagnosis_name", y="readmission_rate", text_auto=".2f"), "30-Day Readmission Rate by Diagnosis", height=390))), table_card("Diagnosis readmission detail", by_diag.rename(columns={"diagnosis_name": "Diagnosis", "admissions": "Admissions", "readmissions": "30-Day Readmissions", "readmission_rate": "Readmission Rate (%)"}).round(2), 12)])

    if page == "Revenue & Collections":
        b = apply_encounter_type(apply_filter(billing, hn, dn, yr), et)
        by_type = b.groupby("encounter_type").agg(billed=("billed_amount", "sum"), collected=("insurance_paid", "sum"), outstanding=("outstanding_amount", "sum"), bills=("bill_id", "count")).reset_index()
        by_type["collection_rate"] = by_type["collected"] / by_type["billed"] * 100
        by_ins = b.groupby("insurance_provider").agg(billed=("billed_amount", "sum"), collected=("insurance_paid", "sum"), outstanding=("outstanding_amount", "sum"), bills=("bill_id", "count")).reset_index()
        by_ins["collection_rate"] = by_ins["collected"] / by_ins["billed"] * 100
        by_ins = by_ins.sort_values("outstanding", ascending=False)
        return html.Div([common, html.Div([
            chart_card(dcc.Graph(figure=base_layout(px.bar(by_type, x="encounter_type", y="billed", text_auto=False), "Billed Revenue by Encounter Type"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(by_type, x="encounter_type", y="outstanding", text_auto=False), "Outstanding by Encounter Type"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(by_ins, x="insurance_provider", y="outstanding", text_auto=False), "Outstanding by Insurance Provider"))),
            chart_card(dcc.Graph(figure=base_layout(px.bar(by_ins, x="insurance_provider", y="collection_rate", text_auto=".2f"), "Collection Rate by Insurance Provider"))),
        ], className="chart-grid"), table_card("Insurance collection detail", by_ins.rename(columns={"insurance_provider": "Insurance Provider", "billed": "Billed", "collected": "Collected", "outstanding": "Outstanding", "bills": "Bills", "collection_rate": "Collection Rate (%)"}).round(2), 10)])

    return html.Div([common, html.Div("Select a dashboard section from the left navigation.", className="insight")])


if __name__ == "__main__":
    host = os.getenv("MEDICORE_HOST", "127.0.0.1")
    port = int(os.getenv("MEDICORE_PORT", "8050"))
    debug = os.getenv("MEDICORE_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug)
