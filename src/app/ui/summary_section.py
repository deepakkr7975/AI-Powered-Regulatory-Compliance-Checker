import streamlit as st
import pandas as pd
from utils.pdf_generator import generate_rewritten_pdf

def render_summary_section():
    if not st.session_state.analysis_results:
        st.info("Upload and analyze a contract first in the Upload section.")
        return

    results = st.session_state.analysis_results

    st.header("📋 Summary & Insights")

    # Contract Summary
    st.subheader("Contract Summary")
    st.write("This contract covers data handling, security controls, encryption, and liability.")

    gdpr_issues = len([r for r in results if 'GDPR' in r.get('regulation', '')])
    hipaa_issues = len([r for r in results if 'HIPAA' in r.get('regulation', '')])
    high_risk = len([r for r in results if r['risk_level'] == 'High'])

    summary_points = []
    if gdpr_issues > 0:
        summary_points.append("Data retention terms conflict with GDPR.")
    if hipaa_issues > 0:
        summary_points.append("Access control and encryption measures are compliant.")
    if high_risk > 0:
        summary_points.append("Liability clause is missing, which may increase legal risks.")
    for point in summary_points:
        st.write(f"• {point}")

    # Key Points to Consider
    st.subheader("Key Points to Consider")
    recommendations = []
    if gdpr_issues > 0:
        recommendations.append("Update retention policy to match GDPR timelines.")
    if any('liability' in r.get('key_clauses', '').lower() for r in results):
        recommendations.append("Include liability clause to reduce legal exposure.")
    if recommendations:
        for rec in recommendations:
            st.warning(f"• {rec}")
    else:
        st.success("• All clauses appear to be in good standing.")

    # Recommendation
    st.subheader("Recommendation")
    high_risk_items = [r for r in results if r['risk_level'] == 'High']
    medium_risk_items = [r for r in results if r['risk_level'] == 'Medium']
    total_count = len(results)
    if high_risk_items:
        st.error("Do NOT accept this contract in current form. Review highlighted clauses before approval.")
    elif len(medium_risk_items) > total_count * 0.5:
        st.warning("Review recommended changes before proceeding with contract approval.")
    else:
        st.success("Contract appears acceptable with minor considerations.")

    # Results Table
    st.subheader("Analysis Results")
    display_data = [
        {
            'Clause ID': r['clause_id'],
            'Risk Level': r['risk_level'],
            'Compliant': '✓' if r['risk_level'] == 'Low' else '✗',
            'Comments': r['summary'][:50] + '...' if len(r['summary']) > 50 else r['summary']
        }
        for r in results
    ]
    display_df = pd.DataFrame(display_data)
    st.dataframe(display_df, use_container_width=True)

    st.markdown("---")

    # AI-Rewritten Clauses
    st.subheader(" AI-Modified Clauses")
    if "show_rewrites" not in st.session_state:
        st.session_state.show_rewrites = False

    if not st.session_state.show_rewrites:
        if st.button(" Show AI-Generated Modifications"):
            st.session_state.show_rewrites = True
            st.rerun()

    if st.session_state.show_rewrites:
        df = pd.DataFrame(results)
        high_risk_df = df[df["risk_level"].isin(["High", "Medium"])].copy()
        if high_risk_df.empty:
            st.info(" No high-risk clauses were found to rewrite.")
        else:
            display_columns = {
                "clause_id": "Clause ID",
                "clause": "Original Clause",
                "AI-Modified Clause": "AI-Modified Clause",
                "AI-Modified Risk Level": "New Risk Level"
            }
            sugg_df = high_risk_df[list(display_columns.keys())].rename(columns=display_columns)
            st.dataframe(sugg_df, use_container_width=True, height=400)

            pdf_data = generate_rewritten_pdf(high_risk_df)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_data,
                file_name="ai_rewritten_clauses_report.pdf",
                mime="application/pdf",
            )
