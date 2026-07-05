"""DPWH Public Works Dossier — Streamlit dashboard.

A reading of the four dbt marts produced by `dpwh_projects_transform`.
All data here is placeholder. Run with:

    streamlit run dashboard/app.py
"""
from __future__ import annotations

import streamlit as st

import data
from styles import CSS
from views import (
    render_category,
    render_contractor,
    render_footer,
    render_hero,
    render_location,
    render_masthead,
    render_projects,
    render_topline,
)

st.set_page_config(
    page_title="DPWH · Dossier",
    page_icon="◑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_marts():
    return {
        "location": data.mart_budget_by_location(),
        "category": data.mart_budget_by_category(),
        "contractor": data.mart_contractor_performance(),
        "projects": data.mart_projects_overview(n=420),
    }


marts = load_marts()
loc_df = marts["location"]
cat_df = marts["category"]
con_df = marts["contractor"]
proj_df = marts["projects"]

render_masthead()

render_hero(
    total_projects=int(loc_df["total_projects"].sum()),
    total_budget=float(loc_df["total_budget"].sum()),
    regions=loc_df["region"].nunique(),
    contractors=len(con_df),
)

st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
render_topline(loc_df)

render_location(loc_df)
render_category(cat_df)
render_contractor(con_df)
render_projects(proj_df)

render_footer()
