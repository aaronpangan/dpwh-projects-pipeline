# DPWH Public Works Dossier — Dashboard

Streamlit dashboard that reads the four dbt marts from the
`dpwh_projects_transform` project and presents them as an editorial-style
data dossier.

**Current state:** all figures are placeholder values shaped to feel realistic
(real region/province names, real-sounding contractor names, but fabricated
counts and budgets). Wire the data layer to Snowflake to make it live.

## Run

From the repo root:

```bash
streamlit run dashboard/app.py
```

## Files

| File | Purpose |
|---|---|
| `app.py` | Entry point — loads the marts and renders sections |
| `data.py` | Placeholder data generators for all four marts |
| `views.py` | Section renderers (hero, topline, location, category, contractor, projects) |
| `styles.py` | All custom CSS + Plotly theme |
| `.streamlit/config.toml` | Streamlit theme + chrome stripping |

## Wiring to live data

Replace each generator in `data.py` with a Snowflake read. The simplest
approach:

```python
import snowflake.connector
import pandas as pd

@st.cache_data(ttl=3600)
def mart_budget_by_location() -> pd.DataFrame:
    conn = snowflake.connector.connect(...)
    return pd.read_sql("select * from DPWH_PROJECTS_DB.DEV.mart_budget_by_location", conn)
```

Section renderers in `views.py` consume `pd.DataFrame` with the same column
names as the dbt mart definitions, so no further changes are needed.

## Design notes

- **Aesthetic:** editorial dossier — cream paper background, italic serif
  display (Instrument Serif), Geist for body, JetBrains Mono for data
- **Accent:** vermillion (#C8341A) for emphasis, deep blue and gold for
  secondary metric coloring
- **No generic chart titles** — kickers and section numbering carry the
  navigation
- **Plotly is themed** to match the paper aesthetic via `styles.PLOTLY_LAYOUT`
