"""All custom CSS and Plotly theming — dark, minimalist, modern."""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --bg: #08090B;
  --bg-2: #0D0E11;
  --surface: #131418;
  --surface-2: #1B1D22;
  --surface-hi: #25272D;
  --border: rgba(255, 255, 255, 0.055);
  --border-md: rgba(255, 255, 255, 0.10);
  --border-hi: rgba(255, 255, 255, 0.20);
  --ink: #EDEDF0;
  --ink-2: #9C9CA5;
  --ink-3: #5C5C66;
  --ink-4: #393940;
  --accent: #D6F458;
  --accent-2: #B2D43A;
  --accent-deep: #748B22;
  --warn: #FF5447;
  --warn-soft: rgba(255, 84, 71, 0.14);
  --info: #7AB7FF;
  --ok: #4ADE80;
  --gold: #F0B847;

  --font-display: 'Geist', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: 'Geist', -apple-system, sans-serif;
  --font-italic: 'Instrument Serif', Georgia, serif;
  --font-mono: 'JetBrains Mono', 'SFMono-Regular', Menlo, monospace;
}

/* ---------- Strip Streamlit chrome ---------- */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
footer,
#MainMenu { display: none !important; }

[data-testid="stAppViewContainer"] > .main,
[data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
}

.stApp {
  background: var(--bg);
  background-image:
    radial-gradient(ellipse 1200px 600px at 8% 0%, rgba(214, 244, 88, 0.04) 0%, transparent 60%),
    radial-gradient(ellipse 900px 500px at 95% 100%, rgba(122, 183, 255, 0.03) 0%, transparent 55%);
  color: var(--ink);
  font-family: var(--font-body);
  font-feature-settings: 'ss01', 'ss03', 'cv11';
  -webkit-font-smoothing: antialiased;
}

.block-container {
  padding: 0 32px 6rem 32px !important;
  max-width: 1480px !important;
  position: relative;
  z-index: 1;
}
@media (max-width: 768px) {
  .block-container { padding: 0 20px 4rem 20px !important; }
}

/* ---------- Typography ---------- */
h1, h2, h3, h4, h5 {
  font-family: var(--font-display) !important;
  font-weight: 500 !important;
  color: var(--ink) !important;
  letter-spacing: -0.025em !important;
  margin: 0 !important;
}
h1 {
  font-size: clamp(2.6rem, 6vw, 4.5rem) !important;
  line-height: 0.98 !important;
  font-weight: 600 !important;
  letter-spacing: -0.04em !important;
}
h2 { font-size: clamp(1.7rem, 3vw, 2.4rem) !important; line-height: 1.05 !important; }
h3 { font-size: 1.4rem !important; line-height: 1.2 !important; }

p, label, span, li {
  font-family: var(--font-body);
  color: var(--ink-2);
  line-height: 1.55;
}

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; text-underline-offset: 3px; }

.italic-serif { font-family: var(--font-italic); font-style: italic; }

/* ---------- Masthead ---------- */
.masthead {
  border-top: 1px solid var(--border-md);
  border-bottom: 1px solid var(--border);
  padding: 14px 0;
  margin-bottom: 56px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  font-family: var(--font-mono);
  font-size: 10.5px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--ink-2);
}
.masthead-left { display: flex; gap: 22px; align-items: center; flex-wrap: wrap; }
.masthead-badge {
  position: relative;
  background: var(--accent);
  color: var(--bg);
  padding: 4px 10px 3px;
  letter-spacing: 0.20em;
  font-weight: 600;
  border-radius: 2px;
}
.live-dot {
  display: inline-block;
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--ok);
  margin-right: 6px;
  box-shadow: 0 0 8px rgba(74, 222, 128, 0.7);
  animation: pulse 2.4s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.45; transform: scale(0.85); }
}
.masthead-right { color: var(--ink-2); display: flex; gap: 18px; flex-wrap: wrap; }
.masthead-right .next { color: var(--accent); }

/* ---------- Hero ---------- */
.hero {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 64px;
  align-items: end;
  padding: 16px 0 56px;
  border-bottom: 1px solid var(--border);
}
@media (max-width: 960px) {
  .hero { grid-template-columns: 1fr; gap: 36px; }
}
.hero-eyebrow {
  font-family: var(--font-mono);
  font-size: 10.5px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 28px;
}
.hero h1 .stack { display: block; }
.hero h1 .accent { color: var(--accent); }
.hero-sub {
  font-family: var(--font-italic);
  font-style: italic;
  font-size: clamp(1.05rem, 1.6vw, 1.45rem);
  line-height: 1.4;
  color: var(--ink-2);
  margin-top: 28px;
  max-width: 44ch;
}
.hero-meta {
  border-left: 1px solid var(--border);
  padding-left: 36px;
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}
@media (max-width: 960px) {
  .hero-meta { border-left: none; border-top: 1px solid var(--border); padding: 24px 0 0; grid-template-columns: 1fr 1fr; gap: 18px 28px; }
}
@media (max-width: 480px) { .hero-meta { grid-template-columns: 1fr; } }
.hero-meta-block { display: flex; flex-direction: column; gap: 4px; }
.hero-meta-label {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--ink-3);
}
.hero-meta-value {
  font-family: var(--font-display);
  font-size: 15px;
  color: var(--ink);
  font-weight: 500;
}

/* ---------- Section header ---------- */
.section { margin-top: 96px; margin-bottom: 28px; }
@media (max-width: 768px) { .section { margin-top: 64px; } }
.section-rule {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 24px;
  align-items: baseline;
  border-top: 1px solid var(--border-md);
  padding-top: 18px;
  margin-bottom: 14px;
}
.section-num {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.22em;
  color: var(--accent);
}
.section-title {
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 2.6vw, 2.25rem);
  font-weight: 500;
  letter-spacing: -0.025em;
  line-height: 1.05;
  color: var(--ink);
}
.section-kicker {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ink-3);
  text-align: right;
}
@media (max-width: 600px) {
  .section-rule { grid-template-columns: 1fr; gap: 6px; }
  .section-kicker { text-align: left; }
}
.section-lede {
  font-family: var(--font-italic);
  font-style: italic;
  font-size: clamp(0.95rem, 1.3vw, 1.15rem);
  line-height: 1.45;
  color: var(--ink-2);
  max-width: 64ch;
  margin: 18px 0 40px;
}

/* ---------- Topline ---------- */
.topline {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  border-top: 1px solid var(--border-md);
  border-bottom: 1px solid var(--border-md);
}
@media (max-width: 900px) { .topline { grid-template-columns: 1fr 1fr; } }
@media (max-width: 480px) { .topline { grid-template-columns: 1fr; } }
.topline-cell {
  padding: 30px 28px;
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 6px;
  position: relative;
}
.topline-cell:last-child { border-right: none; }
@media (max-width: 900px) {
  .topline-cell:nth-child(2) { border-right: none; }
  .topline-cell:nth-child(1), .topline-cell:nth-child(2) { border-bottom: 1px solid var(--border); }
}
@media (max-width: 480px) {
  .topline-cell { border-right: none; border-bottom: 1px solid var(--border); }
  .topline-cell:last-child { border-bottom: none; }
}
.topline-label {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--ink-3);
}
.topline-value {
  font-family: var(--font-display);
  font-size: clamp(2.2rem, 3.5vw, 3.4rem);
  font-weight: 500;
  letter-spacing: -0.04em;
  line-height: 1;
  color: var(--ink);
  font-feature-settings: 'tnum';
  margin-top: 8px;
}
.topline-value .unit {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 400;
  letter-spacing: 0.18em;
  color: var(--ink-3);
  margin-left: 8px;
  vertical-align: 0.45em;
}
.topline-foot {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--ink-2);
  margin-top: 8px;
}
.topline-accent .topline-value { color: var(--accent); }
.topline-warn .topline-value { color: var(--warn); }

/* ---------- Panels / cards ---------- */
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 24px 28px;
  border-radius: 4px;
}
.kicker {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--ink-3);
}

/* ---------- Streamlit metric override ---------- */
[data-testid="stMetric"] {
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 22px 24px;
  border-radius: 4px;
}
[data-testid="stMetricLabel"] {
  font-family: var(--font-mono) !important;
  font-size: 10px !important;
  letter-spacing: 0.22em !important;
  text-transform: uppercase !important;
  color: var(--ink-3) !important;
}
[data-testid="stMetricValue"] {
  font-family: var(--font-display) !important;
  font-size: 2.4rem !important;
  font-weight: 500 !important;
  color: var(--ink) !important;
  font-feature-settings: 'tnum' !important;
  letter-spacing: -0.03em !important;
}

/* ---------- Inputs / filters ---------- */
.stSelectbox label, .stMultiSelect label, .stTextInput label, .stNumberInput label, .stSlider label {
  font-family: var(--font-mono) !important;
  font-size: 10px !important;
  letter-spacing: 0.20em !important;
  text-transform: uppercase !important;
  color: var(--ink-3) !important;
  font-weight: 500 !important;
}

[data-baseweb="select"] > div, [data-baseweb="input"] > div {
  background: var(--surface) !important;
  border: 1px solid var(--border-md) !important;
  border-radius: 4px !important;
  font-family: var(--font-body) !important;
  font-size: 13px !important;
  color: var(--ink) !important;
  min-height: 38px !important;
}
[data-baseweb="select"] > div:hover, [data-baseweb="input"] > div:hover {
  border-color: var(--border-hi) !important;
}
[data-baseweb="select"] [class*="placeholder"], [data-baseweb="select"] [class*="ValueContainer"] {
  color: var(--ink) !important;
  font-size: 13px !important;
}

/* dropdown popover */
[data-baseweb="popover"] [role="listbox"] {
  background: var(--surface-2) !important;
  border: 1px solid var(--border-md) !important;
  font-family: var(--font-body) !important;
  font-size: 13px !important;
}
[data-baseweb="popover"] [role="option"] { color: var(--ink) !important; }
[data-baseweb="popover"] [role="option"]:hover, [data-baseweb="popover"] [aria-selected="true"] {
  background: var(--surface-hi) !important;
  color: var(--accent) !important;
}

/* multiselect chips */
[data-baseweb="tag"] {
  background: var(--surface-hi) !important;
  color: var(--ink) !important;
  border: 1px solid var(--border-md) !important;
  border-radius: 2px !important;
  font-family: var(--font-mono) !important;
  font-size: 11px !important;
}

.stTextInput input, .stNumberInput input {
  background: var(--surface) !important;
  border: 1px solid var(--border-md) !important;
  border-radius: 4px !important;
  color: var(--ink) !important;
  font-family: var(--font-body) !important;
  font-size: 13px !important;
  padding: 9px 12px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
  border-color: var(--accent) !important;
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(214, 244, 88, 0.12) !important;
}
.stTextInput input::placeholder { color: var(--ink-3) !important; }

/* slider */
[data-baseweb="slider"] [role="slider"] { background: var(--accent) !important; border-color: var(--accent) !important; }
[data-baseweb="slider"] div[style*="background"] { background: var(--accent) !important; }

/* buttons */
.stButton > button, .stDownloadButton > button {
  background: var(--surface) !important;
  border: 1px solid var(--border-md) !important;
  color: var(--ink) !important;
  font-family: var(--font-mono) !important;
  font-size: 11px !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  font-weight: 500 !important;
  border-radius: 4px !important;
  padding: 9px 18px !important;
  transition: all 0.15s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  border-color: var(--accent) !important;
  color: var(--accent) !important;
  background: var(--surface-2) !important;
}
.stButton > button:active, .stDownloadButton > button:active { transform: translateY(1px); }

/* ---------- Dataframe ---------- */
[data-testid="stDataFrame"] {
  border: 1px solid var(--border) !important;
  border-radius: 4px !important;
  background: var(--surface) !important;
}
[data-testid="stDataFrame"] [role="columnheader"] {
  font-family: var(--font-mono) !important;
  font-size: 10px !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  color: var(--ink-2) !important;
  background: var(--surface-2) !important;
  border-bottom: 1px solid var(--border-md) !important;
}
[data-testid="stDataFrame"] [role="gridcell"] {
  font-family: var(--font-mono) !important;
  font-size: 12px !important;
  color: var(--ink) !important;
  background: var(--surface) !important;
  border-color: var(--border) !important;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
  gap: 4px;
  border-bottom: 1px solid var(--border-md);
  background: transparent;
}
.stTabs [data-baseweb="tab"] {
  font-family: var(--font-mono) !important;
  font-size: 11px !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  color: var(--ink-3) !important;
  padding: 12px 18px !important;
  background: transparent !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  transition: color 0.15s, border-color 0.15s;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--ink) !important; }
.stTabs [aria-selected="true"] {
  color: var(--accent) !important;
  border-bottom-color: var(--accent) !important;
}

/* ---------- Mono tags ---------- */
.tag {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 9.5px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  padding: 3px 7px;
  border: 1px solid var(--border-md);
  color: var(--ink-2);
  margin-right: 4px;
  margin-top: 2px;
  border-radius: 2px;
  background: var(--surface-2);
}
.tag-accent { background: var(--accent); color: var(--bg); border-color: var(--accent); font-weight: 600; }
.tag-warn { background: var(--warn-soft); color: var(--warn); border-color: rgba(255, 84, 71, 0.4); }
.tag-info { background: rgba(122, 183, 255, 0.12); color: var(--info); border-color: rgba(122, 183, 255, 0.36); }
.tag-gold { background: rgba(240, 184, 71, 0.12); color: var(--gold); border-color: rgba(240, 184, 71, 0.36); }
.tag-ok { background: rgba(74, 222, 128, 0.10); color: var(--ok); border-color: rgba(74, 222, 128, 0.34); }

/* ---------- Leader / contractor rows ---------- */
.leader-head, .leader-row {
  display: grid;
  grid-template-columns: 44px minmax(220px, 1fr) 130px 90px 90px 90px;
  gap: 18px;
  align-items: center;
  padding: 14px 14px;
  border-bottom: 1px solid var(--border);
  transition: background 0.12s;
}
.leader-head {
  border-top: 1px solid var(--border-md);
  border-bottom: 1px solid var(--border-md);
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.20em;
  text-transform: uppercase;
  color: var(--ink-3);
  padding: 11px 14px;
  background: transparent;
}
.leader-row:hover { background: var(--surface); }
.leader-rank {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--ink-3);
  font-feature-settings: 'tnum';
}
.leader-name {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 500;
  color: var(--ink);
  line-height: 1.25;
}
.leader-code {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--ink-3);
  letter-spacing: 0.10em;
  margin-top: 3px;
}
.leader-num {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--ink);
  text-align: right;
  font-feature-settings: 'tnum';
}
.leader-num.italic { font-family: var(--font-italic); font-style: italic; font-size: 17px; }
.leader-bar { height: 3px; background: var(--surface-2); position: relative; border-radius: 2px; overflow: hidden; margin-top: 8px; }
.leader-bar > span { position: absolute; inset: 0 auto 0 0; background: var(--accent); }

@media (max-width: 900px) {
  .leader-head, .leader-row { grid-template-columns: 40px 1fr 110px 80px; }
  .leader-col-hide-md { display: none !important; }
}
@media (max-width: 560px) {
  .leader-head, .leader-row { grid-template-columns: 36px 1fr 90px; gap: 12px; padding: 12px 8px; }
  .leader-col-hide-sm { display: none !important; }
}

/* ---------- Project ledger ---------- */
.ledger-item {
  display: grid;
  grid-template-columns: 110px 1fr 150px 130px;
  gap: 22px;
  padding: 22px 14px;
  border-bottom: 1px solid var(--border);
  align-items: baseline;
  transition: background 0.15s;
}
.ledger-item:hover { background: var(--surface); }
.ledger-id {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.10em;
  color: var(--ink-2);
}
.ledger-desc {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 500;
  color: var(--ink);
  line-height: 1.35;
}
.ledger-meta {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--ink-3);
  margin-top: 6px;
  letter-spacing: 0.08em;
}
.ledger-amount {
  font-family: var(--font-italic);
  font-style: italic;
  font-size: 1.45rem;
  color: var(--ink);
  text-align: right;
  font-feature-settings: 'tnum';
  line-height: 1;
}
.ledger-status {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.ledger-progress { height: 3px; background: var(--surface-2); position: relative; border-radius: 2px; overflow: hidden; }
.ledger-progress > span { position: absolute; inset: 0 auto 0 0; background: var(--accent); }

@media (max-width: 900px) {
  .ledger-item { grid-template-columns: 90px 1fr 130px; gap: 16px; }
  .ledger-col-hide-md { display: none !important; }
}
@media (max-width: 560px) {
  .ledger-item { grid-template-columns: 1fr; gap: 8px; padding: 18px 6px; }
  .ledger-amount { text-align: left; }
  .ledger-progress { margin-top: 4px; }
}

/* ---------- Category cards ---------- */
.cat-row {
  display: grid;
  grid-template-columns: 56px 1fr 200px 130px;
  gap: 28px;
  align-items: baseline;
  padding: 24px 14px;
  border-bottom: 1px solid var(--border);
  transition: background 0.15s;
}
.cat-row:hover { background: var(--surface); }
@media (max-width: 900px) {
  .cat-row { grid-template-columns: 44px 1fr 130px; gap: 16px; padding: 18px 8px; }
  .cat-col-hide-md { display: none !important; }
}
@media (max-width: 560px) {
  .cat-row { grid-template-columns: 1fr; gap: 6px; }
  .cat-col-hide-sm { display: none !important; }
}

/* ---------- Active filter chips ---------- */
.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0 24px;
  align-items: center;
}
.chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 10.5px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink);
  background: var(--surface-2);
  border: 1px solid var(--border-md);
  padding: 5px 10px;
  border-radius: 2px;
}
.chip .chip-key { color: var(--ink-3); }
.chip-count {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--ink-2);
  margin-left: auto;
  letter-spacing: 0.08em;
}

/* ---------- Pagination ---------- */
.pager {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0 0;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--ink-3);
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

/* ---------- Spacers + misc ---------- */
.spacer-lg { height: 64px; }
.spacer-md { height: 32px; }
.spacer-sm { height: 16px; }
hr { display: none; }

.callout {
  border-left: 2px solid var(--accent);
  padding: 4px 0 4px 16px;
  font-family: var(--font-italic);
  font-style: italic;
  font-size: 1.05rem;
  line-height: 1.4;
  color: var(--ink-2);
  margin: 16px 0;
}

/* ---------- Footer ---------- */
.foot {
  margin-top: 96px;
  padding: 32px 0 0;
  border-top: 1px solid var(--border-md);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 48px;
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--ink-2);
  line-height: 1.6;
}
@media (max-width: 768px) { .foot { grid-template-columns: 1fr; gap: 28px; } }
.foot strong {
  display: block;
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--ink);
  margin-bottom: 12px;
  font-weight: 500;
}
.foot em { color: var(--accent); font-style: normal; }
</style>
"""


PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Geist, sans-serif", size=12, color="#EDEDF0"),
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor="rgba(255,255,255,0.10)",
        linewidth=1,
        tickfont=dict(family="JetBrains Mono", size=10, color="#9C9CA5"),
        ticks="outside",
        tickcolor="rgba(255,255,255,0.10)",
        ticklen=4,
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.04)",
        zeroline=False,
        showline=False,
        tickfont=dict(family="JetBrains Mono", size=10, color="#9C9CA5"),
    ),
    legend=dict(
        font=dict(family="JetBrains Mono", size=10, color="#EDEDF0"),
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
    ),
    hoverlabel=dict(
        bgcolor="#1B1D22",
        bordercolor="rgba(214,244,88,0.5)",
        font=dict(family="JetBrains Mono", size=11, color="#EDEDF0"),
    ),
    colorway=["#D6F458", "#7AB7FF", "#F0B847", "#4ADE80", "#FF5447", "#9C9CA5", "#EDEDF0"],
)


COLORS = {
    "bg": "#08090B",
    "surface": "#131418",
    "surface2": "#1B1D22",
    "ink": "#EDEDF0",
    "ink2": "#9C9CA5",
    "ink3": "#5C5C66",
    "accent": "#D6F458",
    "accent_deep": "#748B22",
    "warn": "#FF5447",
    "info": "#7AB7FF",
    "ok": "#4ADE80",
    "gold": "#F0B847",
}
