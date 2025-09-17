import streamlit as st
import plotly.express as px
import pandas as pd
from app.utils.sheets_utils import get_worksheet


def render_risk_section(results_df: pd.DataFrame = None):
    st.header("3. Detected Clauses & Risk Levels")

    # --- Always try to pull fresh data from Google Sheets ---
    try:
        worksheet = get_worksheet()
        rows = worksheet.get_all_values()
        if rows and len(rows) > 1:  # first row is header
            sheet_df = pd.DataFrame(rows[1:], columns=rows[0])
        else:
            sheet_df = pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Failed to fetch from Google Sheets: {e}")
        sheet_df = None

    # Prefer Google Sheets data if available
    if sheet_df is not None and not sheet_df.empty:
        df = sheet_df
    elif results_df is not None and not results_df.empty:
        df = results_df
    else:
        st.warning("⚠️ No analysis results found. Please upload and analyze a contract first.")
        return

    # --- Convert Risk Level to categorical ---
    if "Risk Level" in df.columns:
        df["Risk Level"] = df["Risk Level"].astype(str)

    # --- KPI Cards ---
    st.markdown("### 📊 Risk Overview")
    col1, col2, col3 = st.columns(3)
    high_count = (df["Risk Level"] == "High").sum()
    medium_count = (df["Risk Level"] == "Medium").sum()
    low_count = (df["Risk Level"] == "Low").sum()

    col1.metric("High Risk ⚠️", high_count)
    col2.metric("Medium Risk 🔶", medium_count)
    col3.metric("Low Risk ✅", low_count)

    # --- Risk Distribution Chart ---
    risk_counts = df["Risk Level"].value_counts()
    fig_risk = px.bar(
        x=risk_counts.index,
        y=risk_counts.values,
        color=risk_counts.index,
        color_discrete_map={"High": "#ff4136", "Medium": "#ffdc00", "Low": "#2ecc40"},
        text=risk_counts.values,
        title="Risk Level Distribution"
    )
    fig_risk.update_traces(textposition="outside")
    st.plotly_chart(fig_risk, use_container_width=True)

    # --- Filter Controls ---
    st.markdown("### 🔍 Filter Clauses")
    col_a, col_b = st.columns(2)

    with col_a:
        risk_filter = st.multiselect(
            "Filter by Risk Level:",
            options=df["Risk Level"].unique(),
            default=df["Risk Level"].unique()
        )

    with col_b:
        regulation_filter = st.multiselect(
            "Filter by Regulation:",
            options=df["Regulation"].unique(),
            default=df["Regulation"].unique()
        )

    filtered_df = df[
        (df["Risk Level"].isin(risk_filter)) &
        (df["Regulation"].isin(regulation_filter))
    ]

    # --- Show Filtered Clauses ---
    st.subheader("📜 Filtered Clauses")
    st.dataframe(
        filtered_df[["Clause ID", "Regulation", "Risk Level", "Contract Clause", "AI Analysis"]],
        use_container_width=True
    )

    # --- Export Section ---
    st.subheader("📥 Export Filtered Data")
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    excel_path = "risk_clauses.xlsx"
    filtered_df.to_excel(excel_path, index=False, engine="openpyxl")

    colx, coly = st.columns(2)
    with colx:
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="risk_clauses.csv",
            mime="text/csv"
        )
    with coly:
        with open(excel_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Excel",
                data=f,
                file_name="risk_clauses.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
