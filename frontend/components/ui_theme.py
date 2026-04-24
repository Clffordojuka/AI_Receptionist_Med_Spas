import streamlit as st


def inject_dashboard_css():
    st.markdown(
        """
        <style>
        /* ===== Base App Layout ===== */
        .stApp {
            background: linear-gradient(180deg, #f5f7fb 0%, #eef3f8 100%);
            color: #1f2937;
        }

        [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #f5f7fb 0%, #eef3f8 100%);
        }

        [data-testid="stHeader"] {
            background: rgba(245, 247, 251, 0.85);
            backdrop-filter: blur(8px);
        }

        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        /* ===== Typography ===== */
        .app-subtitle {
            color: #667085;
            font-size: 0.98rem;
            margin-top: -0.35rem;
            margin-bottom: 1.2rem;
        }

        .section-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 0.15rem;
        }

        .section-caption {
            color: #667085;
            font-size: 0.9rem;
            margin-bottom: 0.9rem;
        }

        .tiny-muted {
            color: #667085;
            font-size: 0.82rem;
        }

        h1, h2, h3 {
            color: #111827;
            letter-spacing: -0.01em;
        }

        /* ===== Cards / Surfaces ===== */
        .soft-card {
            background: #ffffff;
            border: 1px solid #e6ebf2;
            border-radius: 18px;
            padding: 1rem 1rem 0.85rem 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        }

        /* ===== Tabs ===== */
        [data-testid="stTabs"] button {
            border-radius: 10px;
        }

        [data-testid="stTabs"] button[aria-selected="true"] {
            background-color: #e8f0fe;
            color: #1d4ed8;
        }

        /* ===== Inputs ===== */
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-baseweb="textarea"] > div {
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #dbe3ee;
        }

        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="select"] > div:focus-within,
        div[data-baseweb="textarea"] > div:focus-within {
            border-color: #93c5fd;
            box-shadow: 0 0 0 2px rgba(147, 197, 253, 0.18);
        }

        /* ===== Buttons ===== */
        .stButton > button {
            border-radius: 12px;
            border: 1px solid #d5deea;
            background: #ffffff;
            color: #1f2937;
            font-weight: 600;
            padding: 0.45rem 0.9rem;
        }

        .stButton > button:hover {
            border-color: #bfd2ea;
            background: #f8fbff;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
        }

        /* ===== Metrics ===== */
        [data-testid="metric-container"] {
            background: #ffffff;
            border: 1px solid #e6ebf2;
            border-radius: 16px;
            padding: 0.85rem 1rem;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
        }

        /* ===== Expanders ===== */
        [data-testid="stExpander"] {
            border: 1px solid #e6ebf2;
            border-radius: 14px;
            background: #ffffff;
        }

        /* ===== Dataframe / Tables ===== */
        [data-testid="stDataFrame"] {
            border: 1px solid #e6ebf2;
            border-radius: 14px;
            overflow: hidden;
            background: #ffffff;
        }

        /* ===== Info / Success / Warning ===== */
        [data-testid="stAlert"] {
            border-radius: 14px;
        }

        /* ===== Badges ===== */
        .badge {
            display: inline-block;
            padding: 0.24rem 0.62rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
        }

        .badge-neutral {
            background: #eef2f7;
            color: #475467;
            border: 1px solid #d8e0ea;
        }

        .badge-success {
            background: #e8f7ee;
            color: #157347;
            border: 1px solid #bfe8cc;
        }

        .badge-warning {
            background: #fff4df;
            color: #b45309;
            border: 1px solid #f4d7a1;
        }

        .badge-danger {
            background: #fdecec;
            color: #b42318;
            border: 1px solid #f3c7c7;
        }

        .badge-info {
            background: #eaf2ff;
            color: #1d4ed8;
            border: 1px solid #cdddfd;
        }

        /* ===== Chat ===== */
        .chat-wrap {
            margin-top: 0.35rem;
        }

        .chat-meta {
            font-size: 0.78rem;
            color: #667085;
            margin-bottom: 0.3rem;
        }

        .chat-bubble {
            border-radius: 16px;
            padding: 0.85rem 0.95rem;
            margin-bottom: 0.85rem;
            line-height: 1.5;
            border: 1px solid #e4eaf2;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        }

        .chat-user {
            background: #edf4ff;
            border-color: #d6e6ff;
        }

        .chat-assistant {
            background: #eefbf3;
            border-color: #d4f1df;
        }

        .chat-system {
            background: #f3f5f8;
            border-color: #e4e7ec;
        }

        /* ===== Horizontal lines ===== */
        hr {
            border: none;
            border-top: 1px solid #e6ebf2;
            margin-top: 1.1rem;
            margin-bottom: 1.1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, caption: str | None = None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="section-caption">{caption}</div>', unsafe_allow_html=True)


def badge(label: str, tone: str = "neutral"):
    st.markdown(
        f'<span class="badge badge-{tone}">{label}</span>',
        unsafe_allow_html=True,
    )