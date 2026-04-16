import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# ---------------------------------------------------
# CONFIGURAÇÃO GERAL
# ---------------------------------------------------
st.set_page_config(
    page_title="Immigrant Economic Mobility",
    layout="wide"
)

# ---------------------------------------------------
# CONEXÃO COM O POSTGRESQL
# ---------------------------------------------------
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = "5433"
DATABASE = "immigrant_mobility_db"

engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# ---------------------------------------------------
# FUNÇÃO PARA BUSCAR DADOS
# ---------------------------------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM immigrant_data"
    return pd.read_sql(query, engine)

df = load_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("Filters")

selected_country = st.sidebar.multiselect(
    "Origin",
    sorted(df["country_of_origin"].unique()),
    default=sorted(df["country_of_origin"].unique())
)

selected_entry = st.sidebar.multiselect(
    "Entry Path",
    sorted(df["entry_type"].unique()),
    default=sorted(df["entry_type"].unique())
)

selected_profession = st.sidebar.multiselect(
    "Current Profession",
    sorted(df["current_profession"].unique()),
    default=sorted(df["current_profession"].unique())
)

filtered_df = df[
    (df["country_of_origin"].isin(selected_country)) &
    (df["entry_type"].isin(selected_entry)) &
    (df["current_profession"].isin(selected_profession))
]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("Immigrant Economic Mobility in the U.S.")
st.caption("BI-style dashboard built with PostgreSQL + SQL + Streamlit")

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total People", f"{len(filtered_df):,}")
kpi2.metric("Average Income", f"${filtered_df['annual_income'].mean():,.0f}")
kpi3.metric("Average Stress", f"{filtered_df['stress_level'].mean():.1f}")
kpi4.metric("Average Satisfaction", f"{filtered_df['job_satisfaction'].mean():.1f}")

st.divider()

# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Overview",
    "Career Transition",
    "Workload & Well-being",
    "Detailed Data"
])

# ---------------------------------------------------
# TAB 1 - EXECUTIVE OVERVIEW
# ---------------------------------------------------
with tab1:
    row1_col1, row1_col2 = st.columns(2)

    income_by_entry = (
        filtered_df.groupby("entry_type", as_index=False)["annual_income"]
        .mean()
        .sort_values("annual_income", ascending=False)
    )

    fig_income_entry = px.bar(
        income_by_entry,
        x="entry_type",
        y="annual_income",
        title="Average Income by Entry Path"
    )
    row1_col1.plotly_chart(fig_income_entry, use_container_width=True)

    income_by_english = (
        filtered_df.groupby("english_level", as_index=False)["annual_income"]
        .mean()
        .sort_values("annual_income", ascending=False)
    )

    fig_income_english = px.bar(
        income_by_english,
        x="english_level",
        y="annual_income",
        title="Average Income by English Level"
    )
    row1_col2.plotly_chart(fig_income_english, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)

    income_by_country = (
        filtered_df.groupby("country_of_origin", as_index=False)["annual_income"]
        .mean()
        .sort_values("annual_income", ascending=False)
    )

    fig_country = px.treemap(
        income_by_country,
        path=["country_of_origin"],
        values="annual_income",
        title="Income Distribution by Origin"
    )
    row2_col1.plotly_chart(fig_country, use_container_width=True)

    profession_income = (
        filtered_df.groupby("current_profession", as_index=False)["annual_income"]
        .mean()
        .sort_values("annual_income", ascending=False)
    )

    fig_prof_income = px.bar(
        profession_income,
        x="current_profession",
        y="annual_income",
        title="Average Income by Current Profession"
    )
    row2_col2.plotly_chart(fig_prof_income, use_container_width=True)

# ---------------------------------------------------
# TAB 2 - CAREER TRANSITION
# ---------------------------------------------------
with tab2:
    st.subheader("Professional trajectory: origin x U.S.")

    career_transition = (
        filtered_df.groupby(
            ["previous_profession", "current_profession"],
            as_index=False
        )
        .size()
        .sort_values("size", ascending=False)
    )

    fig_transition = px.sunburst(
        career_transition,
        path=["previous_profession", "current_profession"],
        values="size",
        title="Career Transition Flow"
    )
    st.plotly_chart(fig_transition, use_container_width=True)

    top_transitions = career_transition.head(15)

    fig_top_transitions = px.bar(
        top_transitions,
        x="size",
        y="previous_profession",
        color="current_profession",
        orientation="h",
        title="Top Career Transitions"
    )
    st.plotly_chart(fig_top_transitions, use_container_width=True)

# ---------------------------------------------------
# TAB 3 - WORKLOAD & WELL-BEING
# ---------------------------------------------------
with tab3:
    row3_col1, row3_col2 = st.columns(2)

    stress_by_profession = (
        filtered_df.groupby("current_profession", as_index=False)["stress_level"]
        .mean()
        .sort_values("stress_level", ascending=False)
    )

    fig_stress = px.bar(
        stress_by_profession,
        x="current_profession",
        y="stress_level",
        title="Average Stress by Current Profession"
    )
    row3_col1.plotly_chart(fig_stress, use_container_width=True)

    satisfaction_by_profession = (
        filtered_df.groupby("current_profession", as_index=False)["job_satisfaction"]
        .mean()
        .sort_values("job_satisfaction", ascending=False)
    )

    fig_satisfaction = px.bar(
        satisfaction_by_profession,
        x="current_profession",
        y="job_satisfaction",
        title="Average Satisfaction by Current Profession"
    )
    row3_col2.plotly_chart(fig_satisfaction, use_container_width=True)

    fig_hours_stress = px.scatter(
        filtered_df,
        x="hours_per_week",
        y="stress_level",
        color="current_profession",
        size="annual_income",
        hover_data=["country_of_origin", "entry_type", "previous_profession"],
        title="Workload vs Stress"
    )
    st.plotly_chart(fig_hours_stress, use_container_width=True)

# ---------------------------------------------------
# TAB 4 - DETAILED DATA
# ---------------------------------------------------
with tab4:
    st.subheader("Detailed filtered dataset")
    st.dataframe(filtered_df, use_container_width=True)