"""Section renderers — dark, minimal, responsive, interactive."""
from __future__ import annotations

from datetime import datetime, timedelta
from io import BytesIO

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from styles import COLORS, PLOTLY_LAYOUT


# ─────────────────────────────────────────────────────── formatting ──

def fmt_php(amount: float) -> str:
    if amount is None or pd.isna(amount):
        return "—"
    if amount >= 1e12: return f"₱{amount / 1e12:.2f}T"
    if amount >= 1e9:  return f"₱{amount / 1e9:.2f}B"
    if amount >= 1e6:  return f"₱{amount / 1e6:.1f}M"
    if amount >= 1e3:  return f"₱{amount / 1e3:.0f}K"
    return f"₱{amount:,.0f}"


def fmt_int(n: int) -> str:
    return f"{int(n):,}"


def next_refresh(now: datetime | None = None) -> datetime:
    """ELT runs at 00:01 Asia/Manila on the 1st of every month."""
    now = now or datetime.now()
    year, month = now.year, now.month
    if now.day == 1 and now.hour == 0 and now.minute < 5:
        return now.replace(minute=1, second=0, microsecond=0)
    if month == 12:
        return datetime(year + 1, 1, 1, 0, 1)
    return datetime(year, month + 1, 1, 0, 1)


def last_refresh(now: datetime | None = None) -> datetime:
    now = now or datetime.now()
    return datetime(now.year, now.month, 1, 0, 1)


# ──────────────────────────────────────────────── shared components ──

def section_header(num: str, title: str, kicker: str, lede: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="section">
          <div class="section-rule">
            <div class="section-num">§ {num}</div>
            <div class="section-title">{title}</div>
            <div class="section-kicker">{kicker}</div>
          </div>
          {f'<div class="section-lede">{lede}</div>' if lede else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def filter_chips(chips: list[tuple[str, str]], count_label: str | None = None) -> None:
    if not chips and not count_label:
        return
    html = '<div class="filter-chips">'
    for key, val in chips:
        html += f'<span class="chip"><span class="chip-key">{key}</span>{val}</span>'
    if count_label:
        html += f'<span class="chip-count">{count_label}</span>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    buf = BytesIO()
    df.to_csv(buf, index=False)
    return buf.getvalue()


# ───────────────────────────────────────────────────────── masthead ──

def render_masthead() -> None:
    lr = last_refresh()
    nr = next_refresh()
    days_to_next = (nr.date() - datetime.now().date()).days
    st.markdown(
        f"""
        <div class="masthead">
          <div class="masthead-left">
            <span class="masthead-badge">DPWH · DOSSIER</span>
            <span><span class="live-dot"></span>PIPELINE LIVE</span>
            <span>MONTHLY CADENCE · 1ST · 00:01 ASIA/MANILA</span>
          </div>
          <div class="masthead-right">
            <span>LAST REFRESH · {lr.strftime("%d %b %Y").upper()}</span>
            <span class="next">NEXT REFRESH · {nr.strftime("%d %b %Y").upper()} · IN {days_to_next}D</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ───────────────────────────────────────────────────────────── hero ──

def render_hero(total_projects: int, total_budget: float, regions: int, contractors: int) -> None:
    st.markdown(
        f"""
        <div class="hero">
          <div>
            <div class="hero-eyebrow">PHILIPPINE PUBLIC WORKS · 2018 — 2026</div>
            <h1>
              <span class="stack">Where the public</span>
              <span class="stack">money <span class="italic-serif accent">goes.</span></span>
            </h1>
            <div class="hero-sub">
              A monthly-refreshed ledger of {fmt_int(total_projects)} infrastructure contracts —
              the road repaved, the bridge rebuilt, the building unfinished.
            </div>
          </div>
          <div class="hero-meta">
            <div class="hero-meta-block">
              <span class="hero-meta-label">Total Portfolio</span>
              <span class="hero-meta-value">{fmt_php(total_budget)}</span>
            </div>
            <div class="hero-meta-block">
              <span class="hero-meta-label">Coverage</span>
              <span class="hero-meta-value">{regions} regions · 17 island groupings</span>
            </div>
            <div class="hero-meta-block">
              <span class="hero-meta-label">Contractors Tracked</span>
              <span class="hero-meta-value">{fmt_int(contractors)} registered entities</span>
            </div>
            <div class="hero-meta-block">
              <span class="hero-meta-label">Pipeline</span>
              <span class="hero-meta-value">DPWH API → S3 → Snowflake → dbt</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ────────────────────────────────────────────────────────── topline ──

def render_topline(location_df: pd.DataFrame) -> None:
    total_projects = int(location_df["total_projects"].sum())
    total_budget = float(location_df["total_budget"].sum())
    completed = int(location_df["completed_projects"].sum())
    delayed = int(location_df["delayed_projects"].sum())
    ghost = int(location_df["ghost_projects"].sum())
    completion_rate = completed * 100 / total_projects
    flagged_rate = (delayed + ghost) * 100 / total_projects

    st.markdown(
        f"""
        <div class="topline">
          <div class="topline-cell">
            <div class="topline-label">Contracts Awarded</div>
            <div class="topline-value">{total_projects / 1000:.1f}<span class="unit">THOUSAND</span></div>
            <div class="topline-foot">Cumulative since 2018 across all DEOs</div>
          </div>
          <div class="topline-cell topline-accent">
            <div class="topline-label">Total Budget</div>
            <div class="topline-value">₱{total_budget / 1e9:.0f}<span class="unit">B PHP</span></div>
            <div class="topline-foot">Awarded contract value, all categories</div>
          </div>
          <div class="topline-cell">
            <div class="topline-label">Completion Rate</div>
            <div class="topline-value">{completion_rate:.1f}<span class="unit">%</span></div>
            <div class="topline-foot">{fmt_int(completed)} contracts marked complete</div>
          </div>
          <div class="topline-cell topline-warn">
            <div class="topline-label">Flagged — Delayed or Ghost</div>
            <div class="topline-value">{flagged_rate:.1f}<span class="unit">%</span></div>
            <div class="topline-foot">{fmt_int(delayed)} delayed · {fmt_int(ghost)} ghost</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ────────────────────────────────────────────────── I. location ──

def render_location(df: pd.DataFrame) -> None:
    section_header(
        "I", "The Geography of Spend",
        "mart_budget_by_location",
        "Where the contracts land. Province-grain rollup of every awarded peso — "
        "select an island group below to focus the view.",
    )

    islands = ["All"] + sorted(df["island_group"].unique().tolist())
    c1, c2, _ = st.columns([1.5, 1.5, 4])
    with c1:
        sel_island = st.selectbox("ISLAND GROUP", islands, key="loc_island")
    with c2:
        sort_metric = st.selectbox("RANK BY", ["Total Budget", "Total Projects", "Delay Rate"], key="loc_sort")

    filtered = df if sel_island == "All" else df[df["island_group"] == sel_island]

    chips = []
    if sel_island != "All":
        chips.append(("ISLAND", sel_island))
    chips.append(("RANK", sort_metric.upper()))
    filter_chips(chips, count_label=f"{len(filtered)} PROVINCES · {fmt_int(filtered['total_projects'].sum())} CONTRACTS")

    sort_col = {"Total Budget": "total_budget", "Total Projects": "total_projects", "Delay Rate": "delay_rate_pct"}[sort_metric]

    region_summary = (
        filtered.groupby("region")
        .agg(total_budget=("total_budget", "sum"),
             total_projects=("total_projects", "sum"),
             delayed=("delayed_projects", "sum"))
        .reset_index()
    )
    region_summary["delay_rate_pct"] = region_summary["delayed"] * 100 / region_summary["total_projects"]
    region_summary = region_summary.sort_values(sort_col, ascending=False)

    col1, col2 = st.columns([1.2, 1], gap="large")
    with col1:
        st.markdown('<div class="kicker">REGIONAL RANKING</div><div class="spacer-md"></div>', unsafe_allow_html=True)
        top = region_summary.head(12).iloc[::-1]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top[sort_col] / (1e9 if sort_col == "total_budget" else 1),
            y=top["region"],
            orientation="h",
            marker=dict(color=COLORS["accent"], line=dict(width=0)),
            text=[fmt_php(b) if sort_col == "total_budget" else (f"{b:.1f}%" if sort_col == "delay_rate_pct" else fmt_int(b)) for b in top[sort_col]],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=10, color=COLORS["ink"]),
            hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>",
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=440, showlegend=False)
        if sort_col == "total_budget":
            fig.update_xaxes(title=None, ticksuffix="B", tickprefix="₱")
        elif sort_col == "delay_rate_pct":
            fig.update_xaxes(title=None, ticksuffix="%")
        else:
            fig.update_xaxes(title=None)
        fig.update_yaxes(title=None, tickfont=dict(size=11, color=COLORS["ink"]))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown('<div class="kicker">ISLAND GROUP · SHARE OF PORTFOLIO</div><div class="spacer-md"></div>', unsafe_allow_html=True)
        island_summary = (
            df.groupby("island_group")
            .agg(total_budget=("total_budget", "sum"),
                 total_projects=("total_projects", "sum"),
                 delayed=("delayed_projects", "sum"))
            .reset_index()
            .sort_values("total_budget", ascending=False)
        )
        island_summary["delay_rate"] = island_summary["delayed"] * 100 / island_summary["total_projects"]
        total = island_summary["total_budget"].sum()
        for _, row in island_summary.iterrows():
            pct = row["total_budget"] * 100 / total
            is_selected = sel_island == row["island_group"]
            color = COLORS["accent"] if is_selected else COLORS["ink"]
            st.markdown(
                f"""
                <div style="padding:18px 0;border-bottom:1px solid var(--border);">
                  <div style="display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap;">
                    <span style="font-family:var(--font-display);font-size:1.15rem;font-weight:500;color:{color};">{row['island_group']}</span>
                    <span style="font-family:var(--font-mono);font-size:10px;color:var(--ink-3);letter-spacing:0.16em;">{fmt_int(row['total_projects'])} CONTRACTS</span>
                  </div>
                  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:8px;gap:8px;flex-wrap:wrap;">
                    <span class="italic-serif" style="font-size:1.5rem;color:var(--accent);">{fmt_php(row['total_budget'])}</span>
                    <span style="font-family:var(--font-mono);font-size:10px;color:var(--ink-3);letter-spacing:0.16em;">{pct:.1f}% · DELAY {row['delay_rate']:.1f}%</span>
                  </div>
                  <div class="leader-bar" style="margin-top:12px;"><span style="width:{pct}%;background:{color};"></span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="kicker">PROVINCIAL SCATTER · BUDGET vs DELAY RATE · SIZED BY PROJECTS</div><div class="spacer-md"></div>', unsafe_allow_html=True)

    fig = go.Figure()
    palette = {"Luzon": COLORS["accent"], "Visayas": COLORS["info"], "Mindanao": COLORS["gold"], "National / Central Office": COLORS["warn"]}
    for island, color in palette.items():
        sub = filtered[filtered["island_group"] == island]
        if len(sub) == 0:
            continue
        fig.add_trace(go.Scatter(
            x=sub["total_budget"] / 1e9,
            y=sub["delay_rate_pct"],
            mode="markers",
            name=island,
            marker=dict(
                size=sub["total_projects"] / 60,
                color=color,
                opacity=0.78,
                line=dict(width=1, color=COLORS["bg"]),
            ),
            text=sub["province_name"],
            hovertemplate="<b>%{text}</b><br>Budget: ₱%{x:.2f}B<br>Delay: %{y:.1f}%<extra></extra>",
        ))
    fig.update_layout(**PLOTLY_LAYOUT, height=440)
    fig.update_xaxes(title=dict(text="TOTAL BUDGET (₱B)", font=dict(family="JetBrains Mono", size=10, color=COLORS["ink3"])))
    fig.update_yaxes(title=dict(text="DELAY RATE %", font=dict(family="JetBrains Mono", size=10, color=COLORS["ink3"])), ticksuffix="%")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.download_button(
        "↓ DOWNLOAD mart_budget_by_location.csv",
        data=to_csv_bytes(filtered),
        file_name="mart_budget_by_location.csv",
        mime="text/csv",
        key="dl_location",
    )


# ──────────────────────────────────────────────── II. category ──

def render_category(df: pd.DataFrame) -> None:
    section_header(
        "II", "By Infrastructure Type",
        "mart_budget_by_category · 7 rows",
        "Multi-category projects credit budget to every category they touch — "
        "totals across categories will exceed portfolio total.",
    )

    df_sorted = df.sort_values("total_budget", ascending=False).reset_index(drop=True)
    total = df_sorted["total_budget"].sum()
    max_budget = df_sorted["total_budget"].max()

    for idx, row in df_sorted.iterrows():
        pct = row["total_budget"] * 100 / total
        width_pct = row["total_budget"] * 100 / max_budget
        rank_num = f"{idx + 1:02d}"
        st.markdown(
            f"""
            <div class="cat-row">
              <div style="font-family:var(--font-mono);font-size:11px;color:var(--ink-3);letter-spacing:0.18em;">{rank_num}</div>
              <div>
                <div style="font-family:var(--font-display);font-size:clamp(1.3rem, 2.2vw, 1.7rem);font-weight:500;line-height:1.1;color:var(--ink);letter-spacing:-0.02em;">{row['component_category']}</div>
                <div style="font-family:var(--font-body);font-size:13px;color:var(--ink-2);margin-top:8px;max-width:60ch;">{row['category_description']}</div>
                <div class="leader-bar" style="margin-top:14px;"><span style="width:{width_pct}%;"></span></div>
                <div style="display:flex;gap:20px;margin-top:14px;font-family:var(--font-mono);font-size:10.5px;letter-spacing:0.14em;color:var(--ink-3);flex-wrap:wrap;">
                  <span>COMPLETION&nbsp;<span style="color:var(--ok);font-weight:500;">{row['completion_rate_pct']:.1f}%</span></span>
                  <span>DELAY&nbsp;<span style="color:var(--warn);font-weight:500;">{row['delay_rate_pct']:.1f}%</span></span>
                  <span>GHOST&nbsp;<span style="color:var(--gold);font-weight:500;">{row['ghost_rate_pct']:.1f}%</span></span>
                  <span>AVG&nbsp;<span style="color:var(--ink);font-weight:500;">{fmt_php(row['avg_budget'])}</span></span>
                </div>
              </div>
              <div style="text-align:right;" class="cat-col-hide-sm">
                <div class="italic-serif" style="font-size:clamp(1.6rem, 2.6vw, 2.2rem);color:var(--ink);line-height:1;">{fmt_php(row['total_budget'])}</div>
                <div style="font-family:var(--font-mono);font-size:10px;color:var(--accent);letter-spacing:0.18em;margin-top:6px;">{pct:.1f}% OF TOTAL</div>
              </div>
              <div style="text-align:right;" class="cat-col-hide-md">
                <div style="font-family:var(--font-mono);font-size:14px;color:var(--ink);font-feature-settings:'tnum';">{fmt_int(row['total_projects'])}</div>
                <div style="font-family:var(--font-mono);font-size:10px;color:var(--ink-3);letter-spacing:0.18em;margin-top:4px;">CONTRACTS</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ────────────────────────────────────────────── III. contractor ──

def render_contractor(df: pd.DataFrame) -> None:
    section_header(
        "III", "The Contractors",
        f"mart_contractor_performance · {len(df):,} entities",
        "Who is delivering the work. Search the registry, filter by "
        "performance band, sort by any metric.",
    )

    c1, c2, c3, c4 = st.columns([2, 1.3, 1.3, 1])
    with c1:
        q = st.text_input("SEARCH", placeholder="contractor name or code…", key="con_q", label_visibility="visible")
    with c2:
        sort_by = st.selectbox("SORT BY", [
            "Total Budget ↓", "Total Budget ↑",
            "Total Projects ↓", "Completion Rate ↓",
            "Delay Rate ↓", "Delay Rate ↑",
        ], key="con_sort")
    with c3:
        band = st.selectbox("PERFORMANCE BAND", [
            "All",
            "Top tier — ≥60% completion",
            "Mid tier — 45–60%",
            "At risk — <45%",
            "High delay — ≥20% delay rate",
            "Ghost-flagged — any",
        ], key="con_band")
    with c4:
        page_size = st.selectbox("PAGE", [20, 50, 100, "All"], index=0, key="con_page")

    filtered = df.copy()
    if q:
        ql = q.strip().lower()
        filtered = filtered[
            filtered["contractor_name"].str.lower().str.contains(ql, na=False)
            | filtered["contractor_code"].astype(str).str.contains(ql, na=False)
        ]
    if band == "Top tier — ≥60% completion":
        filtered = filtered[filtered["completion_rate_pct"] >= 60]
    elif band == "Mid tier — 45–60%":
        filtered = filtered[(filtered["completion_rate_pct"] >= 45) & (filtered["completion_rate_pct"] < 60)]
    elif band == "At risk — <45%":
        filtered = filtered[filtered["completion_rate_pct"] < 45]
    elif band == "High delay — ≥20% delay rate":
        filtered = filtered[filtered["delay_rate_pct"] >= 20]
    elif band == "Ghost-flagged — any":
        filtered = filtered[filtered["ghost_projects"] > 0]

    sort_map = {
        "Total Budget ↓":     ("total_budget", False),
        "Total Budget ↑":     ("total_budget", True),
        "Total Projects ↓":   ("total_projects", False),
        "Completion Rate ↓":  ("completion_rate_pct", False),
        "Delay Rate ↓":       ("delay_rate_pct", False),
        "Delay Rate ↑":       ("delay_rate_pct", True),
    }
    col, asc = sort_map[sort_by]
    filtered = filtered.sort_values(col, ascending=asc).reset_index(drop=True)

    chips = []
    if q: chips.append(("SEARCH", f'"{q}"'))
    if band != "All": chips.append(("BAND", band.split(" — ")[0].upper()))
    chips.append(("SORT", sort_by.upper()))
    filter_chips(chips, count_label=f"{len(filtered)} OF {len(df):,} CONTRACTORS")

    if len(filtered) == 0:
        st.markdown('<div class="callout">No contractors match your filters.</div>', unsafe_allow_html=True)
        return

    if page_size == "All":
        view = filtered
    else:
        view = filtered.head(int(page_size))

    max_budget = view["total_budget"].max() if len(view) else 1

    st.markdown(
        """
        <div class="leader-head">
          <div>#</div>
          <div>CONTRACTOR</div>
          <div style="text-align:right;">TOTAL BUDGET</div>
          <div style="text-align:right;" class="leader-col-hide-sm">CONTRACTS</div>
          <div style="text-align:right;" class="leader-col-hide-md">COMPLETION</div>
          <div style="text-align:right;" class="leader-col-hide-md">DELAY</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for idx, row in view.iterrows():
        rank_num = f"{idx + 1:02d}"
        pct = row["total_budget"] * 100 / max_budget if max_budget else 0
        comp_color = COLORS["ok"] if row["completion_rate_pct"] >= 60 else COLORS["gold"] if row["completion_rate_pct"] >= 45 else COLORS["warn"]
        delay_color = COLORS["warn"] if row["delay_rate_pct"] >= 20 else COLORS["gold"] if row["delay_rate_pct"] >= 10 else COLORS["ink2"]
        ghost_tag = '<span class="tag tag-warn" style="margin-left:8px;">GHOST</span>' if row["ghost_projects"] > 0 else ""
        st.markdown(
            f"""
            <div class="leader-row">
              <div class="leader-rank">{rank_num}</div>
              <div>
                <div class="leader-name">{row['contractor_name']}{ghost_tag}</div>
                <div class="leader-code">CODE&nbsp;{row['contractor_code']}&nbsp;·&nbsp;{row['lead_contractor_projects']} LEAD&nbsp;·&nbsp;{row['joint_venture_projects']} JV</div>
                <div class="leader-bar"><span style="width:{pct}%;"></span></div>
              </div>
              <div class="leader-num italic">{fmt_php(row['total_budget'])}</div>
              <div class="leader-num leader-col-hide-sm">{fmt_int(row['total_projects'])}</div>
              <div class="leader-num leader-col-hide-md" style="color:{comp_color};">{row['completion_rate_pct']:.1f}%</div>
              <div class="leader-num leader-col-hide-md" style="color:{delay_color};">{row['delay_rate_pct']:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="pager"><span>SHOWING {len(view)} OF {len(filtered)} MATCHED · {len(df)} TOTAL</span><span>SORT · {sort_by.upper()}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
    st.download_button(
        "↓ DOWNLOAD FILTERED CONTRACTORS.csv",
        data=to_csv_bytes(filtered),
        file_name="mart_contractor_performance_filtered.csv",
        mime="text/csv",
        key="dl_contractor",
    )


# ─────────────────────────────────────────────── IV. project ledger ──

def render_projects(df: pd.DataFrame) -> None:
    section_header(
        "IV", "Project Ledger",
        f"mart_projects_overview · {len(df):,} sample rows",
        "A reading view of the underlying contracts. Search, filter, and "
        "page through any subset.",
    )

    if "proj_page" not in st.session_state:
        st.session_state.proj_page = 1

    c1, c2 = st.columns([2.5, 1])
    with c1:
        q = st.text_input("SEARCH DESCRIPTION OR CONTRACT ID",
                          placeholder="e.g. road · bridge · 22A45123…",
                          key="proj_q")
    with c2:
        view_mode = st.selectbox("VIEW", ["Reader", "Table"], key="proj_view")

    c3, c4, c5, c6 = st.columns(4)
    with c3:
        islands = sorted(df["island_group"].unique().tolist())
        sel_islands = st.multiselect("ISLAND GROUP", islands, key="proj_islands")
    with c4:
        statuses = sorted(df["project_status"].unique().tolist())
        sel_statuses = st.multiselect("STATUS", statuses, key="proj_statuses")
    with c5:
        tiers = ["No Budget", "Small", "Medium", "Large", "Major"]
        sel_tiers = st.multiselect("BUDGET TIER", tiers, key="proj_tiers")
    with c6:
        flags = st.multiselect("FLAGS", ["Delayed", "Ghost", "Joint Venture", "Completed"], key="proj_flags")

    filtered = df.copy()
    if q:
        ql = q.strip().lower()
        filtered = filtered[
            filtered["project_description"].str.lower().str.contains(ql, na=False)
            | filtered["contract_id"].str.lower().str.contains(ql, na=False)
            | filtered["contractor_names"].str.lower().str.contains(ql, na=False)
        ]
    if sel_islands:  filtered = filtered[filtered["island_group"].isin(sel_islands)]
    if sel_statuses: filtered = filtered[filtered["project_status"].isin(sel_statuses)]
    if sel_tiers:    filtered = filtered[filtered["budget_tier"].isin(sel_tiers)]
    if "Delayed" in flags:        filtered = filtered[filtered["is_delayed"]]
    if "Ghost" in flags:          filtered = filtered[filtered["is_ghost_project"]]
    if "Joint Venture" in flags:  filtered = filtered[filtered["is_joint_venture"]]
    if "Completed" in flags:      filtered = filtered[filtered["is_completed"]]

    chips: list[tuple[str, str]] = []
    if q: chips.append(("SEARCH", f'"{q}"'))
    if sel_islands: chips.append(("ISLAND", " · ".join(sel_islands)))
    if sel_statuses: chips.append(("STATUS", " · ".join(sel_statuses)))
    if sel_tiers: chips.append(("TIER", " · ".join(sel_tiers)))
    if flags: chips.append(("FLAGS", " · ".join(flags).upper()))
    filter_chips(chips, count_label=f"{len(filtered):,} OF {len(df):,} CONTRACTS · {fmt_php(filtered['budget_amount'].sum())}")

    if len(filtered) == 0:
        st.markdown('<div class="callout">No contracts match these filters.</div>', unsafe_allow_html=True)
        return

    if view_mode == "Table":
        st.dataframe(
            filtered[[
                "contract_id", "project_description", "region", "province_name",
                "component_categories", "contractor_names", "project_status",
                "budget_amount", "progress_pct", "infra_year",
            ]].rename(columns=str.upper),
            use_container_width=True,
            height=520,
        )
        st.download_button(
            "↓ DOWNLOAD FILTERED PROJECTS.csv",
            data=to_csv_bytes(filtered),
            file_name="mart_projects_overview_filtered.csv",
            mime="text/csv",
            key="dl_proj_table",
        )
        return

    page_size = 12
    n_pages = max(1, (len(filtered) + page_size - 1) // page_size)
    page = min(st.session_state.proj_page, n_pages)
    start, end = (page - 1) * page_size, (page - 1) * page_size + page_size
    view = filtered.iloc[start:end]

    for _, row in view.iterrows():
        flag_tags = ""
        if row["is_delayed"]:        flag_tags += '<span class="tag tag-warn">DELAYED</span>'
        if row["is_ghost_project"]:  flag_tags += '<span class="tag tag-gold">GHOST</span>'
        if row["is_joint_venture"]:  flag_tags += '<span class="tag tag-info">JV</span>'
        if row["is_completed"]:      flag_tags += '<span class="tag tag-ok">COMPLETED</span>'

        status_color = {
            "Completed": COLORS["ok"],
            "On-Going": COLORS["accent"],
            "For Procurement": COLORS["ink2"],
            "Terminated": COLORS["warn"],
            "Not Yet Started": COLORS["ink3"],
        }.get(row["project_status"], COLORS["ink2"])

        st.markdown(
            f"""
            <div class="ledger-item">
              <div>
                <div class="ledger-id">{row['contract_id']}</div>
                <div style="font-family:var(--font-mono);font-size:9.5px;color:var(--ink-3);letter-spacing:0.16em;margin-top:6px;">FY {row['infra_year']}</div>
              </div>
              <div>
                <div class="ledger-desc">{row['project_description']}</div>
                <div class="ledger-meta">{row['region'].upper()} · {row['province_name'].upper()}</div>
                <div class="ledger-meta" style="color:var(--ink-2);margin-top:4px;">CAT&nbsp;·&nbsp;{row['component_categories']}</div>
                <div class="ledger-meta" style="color:var(--ink-2);margin-top:4px;">{row['contractor_count']}× CONTRACTOR&nbsp;·&nbsp;{row['contractor_names'][:80]}{'…' if len(row['contractor_names']) > 80 else ''}</div>
                <div style="margin-top:10px;">{flag_tags}</div>
              </div>
              <div>
                <div class="ledger-amount">{fmt_php(row['budget_amount'])}</div>
                <div style="font-family:var(--font-mono);font-size:10px;color:var(--accent);letter-spacing:0.16em;text-align:right;margin-top:6px;">{row['budget_tier'].upper()}</div>
              </div>
              <div class="ledger-col-hide-md">
                <div class="ledger-status" style="color:{status_color};">{row['project_status']}</div>
                <div class="ledger-progress" style="margin-top:10px;"><span style="width:{row['progress_pct']}%;"></span></div>
                <div style="font-family:var(--font-mono);font-size:10px;color:var(--ink-3);letter-spacing:0.14em;margin-top:6px;">{row['progress_pct']:.0f}% PROGRESS</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    pc1, pc2, pc3 = st.columns([1, 2, 1])
    with pc1:
        if st.button("← PREV", disabled=page <= 1, key="proj_prev", use_container_width=True):
            st.session_state.proj_page = max(1, page - 1)
            st.rerun()
    with pc2:
        st.markdown(
            f'<div style="text-align:center;padding-top:10px;font-family:var(--font-mono);font-size:11px;color:var(--ink-3);letter-spacing:0.20em;">PAGE {page} / {n_pages} · ROWS {start + 1}–{min(end, len(filtered))} OF {len(filtered):,}</div>',
            unsafe_allow_html=True,
        )
    with pc3:
        if st.button("NEXT →", disabled=page >= n_pages, key="proj_next", use_container_width=True):
            st.session_state.proj_page = min(n_pages, page + 1)
            st.rerun()

    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
    st.download_button(
        "↓ DOWNLOAD FILTERED PROJECTS.csv",
        data=to_csv_bytes(filtered),
        file_name="mart_projects_overview_filtered.csv",
        mime="text/csv",
        key="dl_projects",
    )


# ────────────────────────────────────────────────────────── footer ──

def render_footer() -> None:
    lr = last_refresh()
    nr = next_refresh()
    st.markdown(
        f"""
        <div class="foot">
          <div>
            <strong>The Pipeline</strong>
            Monthly ELT — runs <em>1st of every month at 00:01 Asia/Manila</em>.
            Extracts the full DPWH projects API, lands the snapshot as parquet
            in S3, merges into Snowflake on changed fields only, then runs the
            dbt models. Last refresh {lr.strftime("%d %b %Y")} · next {nr.strftime("%d %b %Y")}.
          </div>
          <div>
            <strong>Methodology</strong>
            Numbers shown in this preview are <em>placeholder</em> values
            generated to demonstrate the layout — region and contractor names
            are real, counts and budgets are fabricated. Wire the data layer
            to Snowflake to make it live; column shapes match the dbt marts
            one-to-one.
          </div>
          <div>
            <strong>Stack</strong>
            DPWH Transparency Portal API · Prefect 3 · AWS S3 · Snowflake ·
            dbt-snowflake · Streamlit · Plotly.<br><br>
            Designed and built by <em>Aaron Pangan</em> — 2026.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
