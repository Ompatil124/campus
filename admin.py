import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from database import get_all_incidents, update_incident, delete_incident

def admin_panel():
    # Reuse the same CSS for consistency
    st.markdown("""
    <style>
    /* Global Styles */
    body {
        background: linear-gradient(135deg, #1a1c20 0%, #0f2027 100%);
        color: #f0f2f6;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 { color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #ff6b6b 0%, #ee5253 100%);
        color: white;
        border-radius: 12px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='color:#ff6b6b;'>🔐 Admin Dashboard</h2>", unsafe_allow_html=True)

    # ---- Authentication ----
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Login"):
            if password == "admin123":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Unauthorized access")
        return

    if st.button("Logout"):
        st.session_state.admin_logged_in = False
        st.rerun()

    # ---- Fetch Data ----
    incidents = get_all_incidents()
    
    if not incidents:
        st.info("No reports available in the database yet.")
        return

    df = pd.DataFrame(incidents)

    # ---- Statistics ----
    st.subheader("📊 Incident Statistics")
    col1, col2 = st.columns(2)

    with col1:
        st.caption("Incident Categories")
        fig_cat = go.Figure(data=[go.Bar(x=df["category"].value_counts().index, y=df["category"].value_counts().values, marker_color='#ff6b6b')])
        st.plotly_chart(fig_cat, use_container_width=True)

    with col2:
        st.caption("Urgency Levels")
        fig_urg = go.Figure(data=[go.Pie(labels=df["urgency"].value_counts().index, values=df["urgency"].value_counts().values, hole=.3)])
        st.plotly_chart(fig_urg, use_container_width=True)

    # ---- Update Section ----
    st.divider()
    st.subheader("📋 Manage Reports")

    report_ids = df["report_id"].tolist()
    selected_id = st.selectbox("Select Report ID to Update", report_ids)

    selected_row = df[df["report_id"] == selected_id].iloc[0]

    col_details, col_action = st.columns([2, 1])

    with col_details:
        st.markdown(f"""
        **Report ID:** `{selected_id}`  
        **Location:** {selected_row['location']}  
        **Time:** {selected_row['timestamp']}  
        **Description:**  
        > {selected_row['description']}
        """)
    
    with col_action:
        st.info(f"Current Status: **{selected_row['status']}**")
        new_status = st.selectbox("Update Status", ["Pending", "Under Review", "Resolved"], 
                                key="status_select")
        remark = st.text_area("Admin Remark", value=selected_row['admin_remark'] or "")
        
        if st.button("Update Report"):
            update_incident(selected_id, new_status, remark)
            st.success("Updated Successfully!")
            st.rerun()

        st.markdown("---")
        if st.button("🗑️ Delete Report", type="primary"):
            delete_incident(selected_id)
            st.warning(f"Report {selected_id} deleted.")
            st.rerun()

    st.subheader("All Data")
    st.dataframe(df)
