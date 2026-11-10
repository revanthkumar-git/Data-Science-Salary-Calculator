import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Data Science Salary Calculator", page_icon="💼", layout="wide")

DATA_FILE = Path(__file__).parent / "Salary_Calculator.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(DATA_FILE, sheet_name="Data")
    df["salary_year_avg"] = pd.to_numeric(df["salary_year_avg"], errors="coerce")
    df["salary_hour_avg"] = pd.to_numeric(df["salary_hour_avg"], errors="coerce")
    for col in ["job_title_short", "job_country", "job_schedule_type"]:
        df[col] = df[col].fillna("Not specified").astype(str).str.strip()
    return df

df = load_data()

st.title("💼 Data Science Salary Calculator")
st.caption("Explore salary estimates by job title, country and employment type.")
st.info("Salary estimates are medians calculated from the available job-posting records in this workbook. They are not guaranteed offers or official market rates.")

with st.sidebar:
    st.header("Dashboard filters")
    titles = sorted(df["job_title_short"].dropna().unique().tolist())
    countries = sorted(df["job_country"].dropna().unique().tolist())
    schedules = sorted(df["job_schedule_type"].dropna().unique().tolist())

    default_title = "Data Engineer" if "Data Engineer" in titles else titles[0]
    default_country = "United States" if "United States" in countries else countries[0]
    default_schedule = "Full-time" if "Full-time" in schedules else schedules[0]

    selected_title = st.selectbox("Job title", titles, index=titles.index(default_title))
    selected_country = st.selectbox("Country", countries, index=countries.index(default_country))
    selected_schedule = st.selectbox("Employment type", schedules, index=schedules.index(default_schedule))
    salary_basis = st.radio("Salary basis", ["Yearly", "Hourly"], horizontal=True)

salary_col = "salary_year_avg" if salary_basis == "Yearly" else "salary_hour_avg"
salary_label = "Annual salary" if salary_basis == "Yearly" else "Hourly salary"

filtered = df[
    (df["job_title_short"] == selected_title)
    & (df["job_country"] == selected_country)
    & (df["job_schedule_type"].str.contains(selected_schedule, case=False, na=False))
].copy()
filtered = filtered.dropna(subset=[salary_col])

# Keep the comparison aligned with the selected country and employment type.
country_schedule = df[
    (df["job_country"] == selected_country)
    & (df["job_schedule_type"].str.contains(selected_schedule, case=False, na=False))
].copy()
country_schedule = country_schedule.dropna(subset=[salary_col])

st.subheader("Your salary estimate")
c1, c2, c3 = st.columns(3)
if not filtered.empty:
    median_salary = filtered[salary_col].median()
    avg_salary = filtered[salary_col].mean()
    c1.metric(f"Median {salary_label.lower()}", f"${median_salary:,.0f}")
    c2.metric(f"Average {salary_label.lower()}", f"${avg_salary:,.0f}")
    c3.metric("Matching job records", f"{len(filtered):,}")
else:
    c1.metric(f"Median {salary_label.lower()}", "No data")
    c2.metric(f"Average {salary_label.lower()}", "No data")
    c3.metric("Matching job records", "0")
    st.warning("No records match all three selections with a reported salary. Try another filter combination.")

st.divider()
st.subheader(f"🌍 Salary map by country · {selected_title}")
map_data = df[
    (df["job_title_short"] == selected_title)
    & (df["job_schedule_type"].str.contains(selected_schedule, case=False, na=False))
].dropna(subset=[salary_col]).copy()
map_data = map_data.groupby("job_country", as_index=False)[salary_col].median()
# Plotly's country-name locations render a world choropleth without requiring a map token.
if not map_data.empty:
    map_fig = px.choropleth(
        map_data,
        locations="job_country",
        locationmode="country names",
        color=salary_col,
        hover_name="job_country",
        color_continuous_scale="Blues",
        labels={salary_col: salary_label, "job_country": "Country"},
        title=f"Median {salary_label.lower()} across countries"
    )
    map_fig.update_layout(height=520, margin=dict(l=0, r=0, t=45, b=0))
    st.plotly_chart(map_fig, use_container_width=True)
else:
    st.info("No country-level salary data is available for this selection.")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader(f"Salary by job title · {selected_country}")
    title_comparison = (
        country_schedule.groupby("job_title_short", as_index=False)[salary_col]
        .median()
        .sort_values(salary_col, ascending=False)
    )
    if not title_comparison.empty:
        fig = px.bar(
            title_comparison, x=salary_col, y="job_title_short", orientation="h",
            labels={salary_col: salary_label, "job_title_short": "Job title"},
            text_auto=",.0f"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=460, margin=dict(l=10,r=10,t=20,b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No salary data available for this comparison.")

with right:
    st.subheader(f"Salary by employment type · {selected_country}")
    type_comparison = (
        df[df["job_country"] == selected_country]
        .dropna(subset=[salary_col])
        .groupby("job_schedule_type", as_index=False)[salary_col]
        .median()
        .sort_values(salary_col, ascending=False)
    )
    if not type_comparison.empty:
        fig = px.bar(
            type_comparison, x=salary_col, y="job_schedule_type", orientation="h",
            labels={salary_col: salary_label, "job_schedule_type": "Employment type"},
            text_auto=",.0f"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=460, margin=dict(l=10,r=10,t=20,b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No salary data available for this comparison.")

with st.expander("View matching job records"):
    display_cols = [
        "job_title_short", "job_title", "job_country", "job_location",
        "job_schedule_type", "salary_rate", "salary_year_avg",
        "salary_hour_avg", "company_name", "job_via"
    ]
    st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)
    csv = filtered[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered records (CSV)", csv, "filtered_salary_records.csv", "text/csv")

st.caption("Source: the Excel workbook supplied for this project. Salary values are shown in the dataset's reported currency (USD in the source dataset).")
