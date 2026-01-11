import streamlit as st
import pandas as pd
from database import get_all_incidents, update_incident
from datetime import datetime
import plotly.graph_objects as go

def admin_panel():
    st.markdown(
        "<h2 style='color:#2E86C1;'>🔐 Admin Dashboard</h2>",
        unsafe_allow_html=True
    )

    # ---- Authentication ----
    password = st.text_input("Enter Admin Password", type="password")
    if password != "admin123":
        st.warning("❌ Unauthorized access")
        return

    # ---- Fetch Data ----
    incidents = get_all_incidents()
    df = pd.DataFrame(incidents)

    if df.empty:
        st.info("No reports available.")
        return

    # ---- Display All Reports ----
    st.subheader("📋 All Incident Reports")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # ---- Update Section ----
    st.subheader("✏️ Update Report Status")

    report_ids = df["report_id"].tolist()
    selected_id = st.selectbox("Select Report ID", report_ids)

    selected_row = df[df["report_id"] == selected_id].iloc[0]

    st.info(
        f"""
        **Current Status:** {selected_row['status']}
        **Current Remark:** {selected_row['admin_remark'] or 'None'}
        """
    )

    if selected_row.get('proof'):
        st.subheader("📎 Attached Proof")
        # proof is URL
        if selected_row.get('proof_type') and selected_row['proof_type'].startswith('image/'):
            st.image(selected_row['proof'])
        elif selected_row.get('proof_type') and selected_row['proof_type'].startswith('video/'):
            st.video(selected_row['proof'])
        else:
            st.markdown(f"[📎 View/Download Proof]({selected_row['proof']})")

    new_status = st.selectbox(
        "New Status",
        ["Pending", "Under Review", "Resolved"],
        index=["Pending", "Under Review", "Resolved"].index(selected_row["status"])
    )

    remark = st.text_area(
        "Admin Remark (Visible to complainer)",
        value=selected_row["admin_remark"] or ""
    )

    if st.button("✅ Update Report"):
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updates = {'status': new_status, 'admin_remark': remark, 'last_updated': last_updated}
        update_incident(selected_id, updates)

        st.success("Report updated successfully 🔄")
        st.rerun()

    # ---- Statistics ----
    st.divider()
    st.subheader("📊 Incident Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Incident Types")
        fig = go.Figure(data=[go.Bar(x=df["category"].value_counts().index, y=df["category"].value_counts().values)])
        st.plotly_chart(fig)

    with col2:
        st.subheader("Urgency Levels")
        fig = go.Figure(data=[go.Bar(x=df["urgency"].value_counts().index, y=df["urgency"].value_counts().values)])
        st.plotly_chart(fig)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Area-wise Incidents")
        fig = go.Figure(data=[go.Bar(x=df["location"].value_counts().index, y=df["location"].value_counts().values)])
        st.plotly_chart(fig)

    with col4:
        st.subheader("Status Distribution")
        status_counts = df["status"].value_counts()
        fig = go.Figure(data=[go.Pie(labels=status_counts.index, values=status_counts.values)])
        st.plotly_chart(fig)
