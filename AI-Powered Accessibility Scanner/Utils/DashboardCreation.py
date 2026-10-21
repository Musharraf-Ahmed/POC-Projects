import streamlit as st
import pandas as pd
from importlib import import_module

def CreateDashboard():
    Portkey = import_module("portkey_ai").Portkey
    # ==========================================
    # CONFIGURATION
    # ==========================================

    DB_USER = "postgres"
    DB_PASSWORD = "Mprsnl2026"
    DB_HOST = "localhost"
    DB_NAME = "Accessibility_Data"

    # ==========================================
    # PAGE SETTINGS
    # ==========================================

    st.set_page_config(
        page_title="AI Accessibility Scanner",
        page_icon="♿",
        layout="wide"
    )

    st.title("♿ AI-Powered Accessibility Scanner Dashboard")

    # ==========================================
    # DATABASE CONNECTION
    # ==========================================

    @st.cache_data
    def load_data():
        create_engine = import_module("sqlalchemy").create_engine

        engine = create_engine(
        "postgresql+psycopg2://postgres:Mprsnl2026@localhost/Accessibility_Data")

        query = """
        SELECT *
        FROM accessibility_violations
        """

        df = pd.read_sql(query, engine)

        return df


    try:
        df = load_data()

    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        st.stop()

    # ==========================================
    # SIDEBAR FILTERS
    # ==========================================

    st.sidebar.header("Filters")

    selected_impact = st.sidebar.selectbox(
        "Severity",
        ["All", "critical", "serious", "moderate", "minor"]
    )

    page_search = st.sidebar.text_input(
        "Search URL"
    )

    if selected_impact != "All":
        df = df[df["impact"] == selected_impact]

    if page_search:
        df = df[
            df["page_url"]
            .str.contains(page_search, case=False, na=False)
        ]

    # ==========================================
    # ACCESSIBILITY SCORE
    # ==========================================

    critical_count = len(df[df["impact"] == "critical"])
    serious_count = len(df[df["impact"] == "serious"])
    moderate_count = len(df[df["impact"] == "moderate"])
    minor_count = len(df[df["impact"] == "minor"])

    score = (
        100
        - (critical_count * 5)
        - (serious_count * 3)
        - (moderate_count * 2)
        - (minor_count * 1)
    )

    score = max(score, 0)

    # ==========================================
    # KPI CARDS
    # ==========================================

    st.subheader("Accessibility Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Accessibility Score",
        f"{score}/100"
    )

    col2.metric(
        "Critical",
        critical_count
    )

    col3.metric(
        "Serious",
        serious_count
    )

    col4.metric(
        "Moderate",
        moderate_count
    )

    col5.metric(
        "Minor",
        minor_count
    )

    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================

    st.subheader("Executive Summary")

    top_issue = (
        df["rule_id"].mode()[0]
        if not df.empty
        else "N/A"
    )

    st.info(
        f"""
        Total Violations: {len(df)}

        Most Common Issue: {top_issue}

        Critical Issues: {critical_count}

        Accessibility Health Score: {score}/100
        """
    )

    # ==========================================
    # CHARTS
    # ==========================================

    left, right = st.columns(2)

    # Severity Breakdown

    with left:

        st.subheader("Severity Distribution")

        severity_counts = (
            df["impact"]
            .value_counts()
            .reset_index()
        )

        severity_counts.columns = [
            "Severity",
            "Count"
        ]

        if not severity_counts.empty:

            st.bar_chart(
                severity_counts.set_index("Severity")["Count"]
            )

    # Top Violations

    with right:

        st.subheader("Top Accessibility Violations")

        top_violations = (
            df["rule_id"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_violations.columns = [
            "Rule",
            "Count"
        ]

        if not top_violations.empty:

            st.bar_chart(
                top_violations.set_index("Rule")["Count"]
            )

    # ==========================================
    # HISTORICAL TREND
    # ==========================================

    st.subheader("Violation Trend")

    if not df.empty and "scan_date" in df.columns:

        trend = (
            df.groupby("scan_date")
            .size()
            .reset_index(name="Violations")
        )

        st.line_chart(
            trend.set_index("scan_date")["Violations"]
        )

    # ==========================================
    # PAGE WISE ANALYSIS
    # ==========================================

    st.subheader("Page Wise Analysis")

    page_summary = (
        df.groupby("page_url")
        .size()
        .reset_index(name="Violations")
        .sort_values(
            by="Violations",
            ascending=False
        )
    )

    st.dataframe(
        page_summary,
        use_container_width=True
    )

    # ==========================================
    # DETAILED RESULTS
    # ==========================================

    st.subheader("Accessibility Findings")

    selected_page = st.selectbox(
        "Select Page",
        ["All Pages"] + list(
            df["page_url"]
            .dropna()
            .unique()
        )
    )

    filtered_df = df.copy()

    if selected_page != "All Pages":
        filtered_df = filtered_df[
            filtered_df["page_url"]
            == selected_page
        ]

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    # ==========================================
    # AI ANALYSIS SECTION
    # ==========================================

    st.subheader("AI Recommendations")

    if "ai_analysis" in filtered_df.columns:

        for row in filtered_df.head(20).itertuples():

            title = (
                f"{row.rule_id}"
                f" ({row.impact})"
            )

            with st.expander(title):

                st.write(
                    row.ai_analysis
                )

    # ==========================================
    # DOWNLOAD REPORT
    # ==========================================

    st.subheader("Download Report")

    csv = filtered_df.to_csv(
        index=False
    )

    st.download_button(
        label="Download CSV Report",
        data=csv,
        file_name="accessibility_report.csv",
        mime="text/csv"
    )

    st.header("🤖 Accessibility Assistant")

    question = st.chat_input(
            "Ask a question about accessibility results...")

    if question:

        summary = f"""
        Total Violations:
        {len(df)}

        Critical:
        {critical_count}

        Serious:
        {serious_count}

        Top Issues:
        {df['rule_id'].value_counts().head(5).to_dict()}
        """
        prompt = f"""
        You are an accessibility expert.

        Accessibility Data:

        {summary}

        Question:
        {question}
        """
        
        portkey = Portkey(
            base_url = "https://portkeygateway.perficient.com/v1",
            api_key = "myr2tBJ3n1F9WsXBeDDLa50bgZxQ")
            
        response = portkey.chat.completions.create(
            model = "@azure-openai/anthropic.claude-3-7-sonnet@20250219",
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            MAX_TOKENS = 512)
    
        answer = response.choices[0].message.content

        st.chat_message("assistant").write(answer)

    # ==========================================
    # FOOTER
    # ==========================================

    st.markdown("---")

    st.caption(
        "AI-Powered Accessibility Scanner | "
        "Playwright + Axe-Core + Python + PostgreSQL + Streamlit"
    )

CreateDashboard()