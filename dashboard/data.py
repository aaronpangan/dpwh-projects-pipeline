"""Placeholder data generators for the four DPWH marts.

Numbers are fabricated but shaped to feel realistic — region/province names
are real, contractor names are real-sounding, status distributions and
budget magnitudes roughly match the actual DPWH portfolio shape.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)

REGIONS = [
    ("National Capital Region", "Luzon"),
    ("Region I", "Luzon"),
    ("Region II", "Luzon"),
    ("Region III", "Luzon"),
    ("Region IV-A", "Luzon"),
    ("Region IV-B", "Luzon"),
    ("Region V", "Luzon"),
    ("Cordillera Administrative Region", "Luzon"),
    ("Region VI", "Visayas"),
    ("Region VII", "Visayas"),
    ("Region VIII", "Visayas"),
    ("Negros Island Region", "Visayas"),
    ("Region IX", "Mindanao"),
    ("Region X", "Mindanao"),
    ("Region XI", "Mindanao"),
    ("Region XII", "Mindanao"),
    ("Region XIII", "Mindanao"),
    ("Central Office", "National / Central Office"),
]

PROVINCES = {
    "National Capital Region": ["Metro Manila North", "Metro Manila South", "Metro Manila Central"],
    "Region I": ["Ilocos Norte", "Ilocos Sur", "La Union", "Pangasinan"],
    "Region II": ["Cagayan", "Isabela", "Nueva Vizcaya", "Quirino", "Batanes"],
    "Region III": ["Bulacan", "Pampanga", "Tarlac", "Nueva Ecija", "Bataan", "Zambales", "Aurora"],
    "Region IV-A": ["Cavite", "Laguna", "Batangas", "Rizal", "Quezon"],
    "Region IV-B": ["Mindoro Oriental", "Mindoro Occidental", "Palawan", "Romblon", "Marinduque"],
    "Region V": ["Albay", "Camarines Norte", "Camarines Sur", "Catanduanes", "Masbate", "Sorsogon"],
    "Cordillera Administrative Region": ["Abra", "Apayao", "Benguet", "Ifugao", "Kalinga", "Mountain Province"],
    "Region VI": ["Aklan", "Antique", "Capiz", "Iloilo", "Guimaras"],
    "Region VII": ["Bohol", "Cebu", "Siquijor"],
    "Region VIII": ["Leyte", "Southern Leyte", "Northern Samar", "Eastern Samar", "Samar", "Biliran"],
    "Negros Island Region": ["Negros Occidental", "Negros Oriental"],
    "Region IX": ["Zamboanga del Norte", "Zamboanga del Sur", "Zamboanga Sibugay"],
    "Region X": ["Bukidnon", "Camiguin", "Lanao del Norte", "Misamis Occidental", "Misamis Oriental"],
    "Region XI": ["Davao del Norte", "Davao del Sur", "Davao Oriental", "Davao Occidental", "Davao de Oro"],
    "Region XII": ["Cotabato", "Sarangani", "South Cotabato", "Sultan Kudarat"],
    "Region XIII": ["Agusan del Norte", "Agusan del Sur", "Surigao del Norte", "Surigao del Sur", "Dinagat Islands"],
    "Central Office": ["UPMO / Central Office", "Regional Office / Multi-Province"],
}

CATEGORIES = [
    ("Bridges", 1, "Bridge infrastructure projects."),
    ("Buildings and Facilities", 2, "Vertical infrastructure and public facility projects."),
    ("Flood Control and Drainage", 3, "Water management and disaster mitigation infrastructure projects."),
    ("Roads", 4, "Road network construction and rehabilitation projects."),
    ("Septage and Sewerage Plants", 5, "Sanitation and wastewater management projects."),
    ("Water Provision and Storage", 6, "Water supply and storage infrastructure projects."),
    ("Uncategorized", 7, "Contracts with missing or unclassified categories."),
]

CONTRACTOR_SEEDS = [
    "EQUI-PARCO CONSTRUCTION COMPANY",
    "ST. GERRARD CONSTRUCTION",
    "ALLENCON DEVELOPMENT CORPORATION",
    "ULTICON BUILDERS, INC.",
    "MEGAWIDE CONSTRUCTION CORPORATION",
    "FIRST BALFOUR INCORPORATED",
    "DM CONSUNJI INCORPORATED",
    "EEI CORPORATION",
    "PRIME INFRASTRUCTURE CAPITAL",
    "SUN VALLEY CONSTRUCTION",
    "PHESCO INCORPORATED",
    "CAGAYAN PEAK BUILDERS",
    "GOLDEN MILE DEVELOPMENT",
    "PIONEER CONCRETE AND AGGREGATE",
    "VICENTE T. LAO CONSTRUCTION",
    "JADE PROGRESSIVE BUILDERS",
    "ERA CONSTRUCTION INC.",
    "ROYAL ARROW CONTRACTORS",
    "MAKATI DEVELOPMENT CORPORATION",
    "PRIMEROCK CONSTRUCTION",
    "VEGA STEEL AND INFRASTRUCTURE",
    "MAGSAYSAY INFRASTRUCTURE",
    "SANTA CLARA INTERNATIONAL",
    "EMERALD HALO ENGINEERING",
    "TRIANGLE CONSTRUCTION SUPPLY",
    "BENGUET BUILDERS",
    "SOUTHPOINT ENGINEERING",
    "L.P.O. ENTERPRISES",
    "MELMAN BUILDERS OPC",
    "VGP CONSTRUCTION AND EQUIPMENTS RENTAL",
]

# Expand to ~180 contractor entries by combining real seeds with generated names
_PREFIXES = ["NORTH STAR", "EASTERN", "SOUTHERN", "PACIFIC", "ARCHIPELAGO", "MOUNTAIN VIEW", "HORIZON", "KEYSTONE", "IRONWORKS", "BLUE RIDGE", "SILVER CREEK", "RED EARTH", "DELTA", "VANGUARD", "OAKWOOD", "STERLING", "MARINER", "HIGHLAND", "RIDGEWAY", "CRESCENT"]
_CORES = ["BUILDERS", "CONSTRUCTION", "INFRASTRUCTURE", "DEVELOPMENT", "ENGINEERING", "CONTRACTORS", "GENERAL CONTRACTOR", "CIVIL WORKS", "ROADWORKS", "AGGREGATES"]
_SUFFIXES = ["INC.", "CORP.", "OPC", "& CO.", "INTERNATIONAL", "PHILIPPINES", "GROUP", "ENTERPRISES", "TRADING", ""]

def _generate_contractors() -> list[str]:
    names = list(CONTRACTOR_SEEDS)
    seen = set(names)
    rng = np.random.default_rng(7)
    while len(names) < 180:
        p = rng.choice(_PREFIXES)
        c = rng.choice(_CORES)
        s = rng.choice(_SUFFIXES)
        name = f"{p} {c} {s}".strip()
        if name not in seen:
            seen.add(name)
            names.append(name)
    return names

CONTRACTORS = _generate_contractors()


def mart_budget_by_location() -> pd.DataFrame:
    rows = []
    for region, island in REGIONS:
        for province in PROVINCES[region]:
            n = int(RNG.integers(120, 4500))
            total_budget = float(RNG.uniform(2e9, 80e9))
            completed = int(n * RNG.uniform(0.35, 0.75))
            delayed = int(n * RNG.uniform(0.05, 0.30))
            ghost = int(n * RNG.uniform(0.0, 0.04))
            rows.append({
                "island_group": island,
                "region": region,
                "province_name": province,
                "total_projects": n,
                "total_budget": total_budget,
                "avg_budget": total_budget / n,
                "completed_projects": completed,
                "delayed_projects": delayed,
                "ghost_projects": ghost,
                "completion_rate_pct": round(completed * 100 / n, 2),
                "delay_rate_pct": round(delayed * 100 / n, 2),
                "ghost_rate_pct": round(ghost * 100 / n, 2),
            })
    return pd.DataFrame(rows)


def mart_budget_by_category() -> pd.DataFrame:
    weights = [0.06, 0.16, 0.22, 0.46, 0.03, 0.04, 0.03]
    rows = []
    for (cat, order, desc), w in zip(CATEGORIES, weights):
        n = int(252000 * w)
        total_budget = float(w * 950e9 * RNG.uniform(0.85, 1.15))
        completed = int(n * RNG.uniform(0.40, 0.70))
        delayed = int(n * RNG.uniform(0.08, 0.25))
        ghost = int(n * RNG.uniform(0.005, 0.03))
        rows.append({
            "component_category": cat,
            "category_sort_order": order,
            "category_description": desc,
            "total_projects": n,
            "total_budget": total_budget,
            "avg_budget": total_budget / n,
            "completed_projects": completed,
            "delayed_projects": delayed,
            "ghost_projects": ghost,
            "completion_rate_pct": round(completed * 100 / n, 2),
            "delay_rate_pct": round(delayed * 100 / n, 2),
            "ghost_rate_pct": round(ghost * 100 / n, 2),
        })
    return pd.DataFrame(rows)


def mart_contractor_performance() -> pd.DataFrame:
    rows = []
    for name in CONTRACTORS:
        n = int(RNG.integers(15, 850))
        lead = int(n * RNG.uniform(0.55, 0.95))
        jv = n - lead
        avg_budget = float(RNG.uniform(8e6, 95e6))
        total_budget = avg_budget * n
        completed = int(n * RNG.uniform(0.40, 0.85))
        delayed = int(n * RNG.uniform(0.04, 0.35))
        ghost = int(n * RNG.uniform(0.0, 0.06))
        rows.append({
            "contractor_pk": f"c{abs(hash(name)) & 0xFFFF:04x}",
            "contractor_code": str(int(RNG.integers(10000, 99999))),
            "contractor_name": name,
            "total_projects": n,
            "lead_contractor_projects": lead,
            "joint_venture_projects": jv,
            "total_budget": total_budget,
            "avg_budget": avg_budget,
            "completed_projects": completed,
            "delayed_projects": delayed,
            "ghost_projects": ghost,
            "completion_rate_pct": round(completed * 100 / n, 2),
            "delay_rate_pct": round(delayed * 100 / n, 2),
            "ghost_rate_pct": round(ghost * 100 / n, 2),
        })
    return pd.DataFrame(rows).sort_values("total_budget", ascending=False).reset_index(drop=True)


PROJECT_TEMPLATES = [
    "Construction of {road} along {place} National Road",
    "Rehabilitation of {place} Bridge",
    "Improvement of Drainage System along {place} Avenue",
    "Asphalt Overlay of {road} Road, {place} Section",
    "Construction of Flood Control Structure along {place} River",
    "Widening of {road} Highway, K{km1}+{m1} to K{km2}+{m2}",
    "Construction of {n}-Story School Building, {place} Elementary School",
    "Construction of Multi-Purpose Building in {place}",
    "Slope Protection Works along {place} Mountain Pass",
    "Replacement of {place} Bridge",
    "Reblocking of Concrete Pavement, {place} Section",
    "Construction of Seawall along {place} Coast",
]

ROAD_NAMES = ["Maharlika", "Pan-Philippine", "Aurora", "Quirino", "Bonifacio", "Rizal", "Mabini", "Burgos", "Magsaysay"]
PLACES = ["San Isidro", "San Pedro", "Santa Rosa", "Tagum", "Vigan", "Iloilo", "Bacolod", "Naga", "Tarlac", "Tuguegarao", "Calbayog", "Butuan", "Cotabato", "Olongapo", "Cabanatuan", "Roxas"]
STATUSES = ["Completed", "On-Going", "For Procurement", "Terminated", "Not Yet Started"]
STATUS_WEIGHTS = [0.55, 0.30, 0.08, 0.02, 0.05]
BUDGET_TIERS = ["No Budget", "Small", "Medium", "Large", "Major"]


def _budget_tier(b: float) -> str:
    if b <= 0:
        return "No Budget"
    if b < 1e6:
        return "Small"
    if b < 1e7:
        return "Medium"
    if b < 1e8:
        return "Large"
    return "Major"


def mart_projects_overview(n: int = 240) -> pd.DataFrame:
    loc = mart_budget_by_location()
    rows = []
    for i in range(n):
        l = loc.sample(1, random_state=int(RNG.integers(0, 1_000_000))).iloc[0]
        status = str(RNG.choice(STATUSES, p=STATUS_WEIGHTS))
        budget = float(min(RNG.lognormal(mean=16.6, sigma=1.25), 2.5e9))
        if status in ("For Procurement", "Not Yet Started"):
            budget *= 0  # zero out
        progress = (
            100.0 if status == "Completed"
            else (0.0 if status in ("For Procurement", "Not Yet Started")
                  else float(RNG.uniform(8, 92)))
        )
        c_count = int(RNG.choice([1, 1, 1, 1, 1, 2, 2, 3]))
        contractor_names = list(RNG.choice(CONTRACTORS, size=c_count, replace=False))
        cat_count = int(RNG.choice([1, 1, 1, 1, 2, 2, 3]))
        cats = list(RNG.choice([c[0] for c in CATEGORIES[:-1]], size=cat_count, replace=False))

        tmpl = str(RNG.choice(PROJECT_TEMPLATES))
        desc = tmpl.format(
            road=str(RNG.choice(ROAD_NAMES)),
            place=str(RNG.choice(PLACES)),
            km1=int(RNG.integers(0, 200)),
            m1=int(RNG.integers(0, 999)),
            km2=int(RNG.integers(200, 400)),
            m2=int(RNG.integers(0, 999)),
            n=int(RNG.integers(2, 5)),
        )

        delayed = (status == "Completed" and progress < 100) or (
            status not in ("Completed", "For Procurement", "Not Yet Started", "Terminated")
            and bool(RNG.random() < 0.25)
        )
        ghost = (progress == 0 and budget > 0 and status not in ("For Procurement", "Not Yet Started", "Terminated") and bool(RNG.random() < 0.15))

        rows.append({
            "contract_id": f"{int(RNG.integers(15, 26)):02d}{chr(int(RNG.integers(65, 91)))}{int(RNG.integers(10000, 99999))}",
            "island_group": l["island_group"],
            "region": l["region"],
            "province_name": l["province_name"],
            "project_description": desc,
            "component_categories": ", ".join(sorted(cats)),
            "category_count": cat_count,
            "contractor_names": " / ".join(contractor_names),
            "contractor_count": c_count,
            "is_joint_venture": c_count > 1,
            "project_status": status,
            "budget_amount": budget,
            "budget_tier": _budget_tier(budget),
            "progress_pct": round(progress, 1),
            "is_delayed": delayed,
            "is_ghost_project": ghost,
            "is_completed": status == "Completed",
            "infra_year": int(RNG.integers(2018, 2026)),
        })
    return pd.DataFrame(rows)
