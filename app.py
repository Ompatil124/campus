import streamlit as st
import uuid
from database import create_tables, insert_incident, get_status, check_connection, get_admin_remark
from nlp_model import classify_incident, sentiment_score
from admin import admin_panel

if "page" not in st.session_state:
    st.session_state.page = "Home"

st.set_page_config(
    page_title="CampusSafe",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
@keyframes slideInLeft {
    from { transform: translateX(-100px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
@keyframes slideInRight {
    from { transform: translateX(100px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
@keyframes bounceIn {
    0% { transform: scale(0.3); opacity: 0; }
    50% { transform: scale(1.05); }
    70% { transform: scale(0.9); }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes slideUp {
    from { transform: translateY(50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
@keyframes shieldGlow {
    0% { transform: scale(0.8); opacity: 0; filter: drop-shadow(0 0 0 #00ff88); }
    50% { transform: scale(1.1); opacity: 1; filter: drop-shadow(0 0 10px #00ff88); }
    100% { transform: scale(1); opacity: 1; filter: drop-shadow(0 0 5px #00ff88); }
}
@keyframes lockSecure {
    0% { transform: rotateY(0deg) scale(0.5); opacity: 0; }
    50% { transform: rotateY(180deg) scale(1.2); opacity: 1; }
    100% { transform: rotateY(360deg) scale(1); opacity: 1; }
}
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    animation: fadeIn 1s ease-in-out;
}
.stButton>button {
    background-color: #ff6b6b;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    transition: all 0.3s ease;
    border: none;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}
.stButton>button:hover {
    background-color: #ff5252;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    animation: pulse 0.6s ease-in-out;
}
.card {
    background-color: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 12px;
    margin: 10px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    animation: fadeIn 1s ease-in-out;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.4);
}
.title {
    text-align: center;
    animation: slideInLeft 1s ease-in-out;
}
.image-container {
    text-align: center;
    animation: slideInRight 1s ease-in-out;
}
.feature-cards {
    display: flex;
    justify-content: space-around;
    animation: fadeIn 1.5s ease-in-out;
}
.stSuccess {
    animation: bounceIn 0.8s ease-out;
}
.stAlert {
    animation: slideUp 0.6s ease-out;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🛡️ CampusSafe</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "Home"

with col2:
    if st.button("📢 Report Incident"):
        st.session_state.page = "Report"

with col3:
    if st.button("🔍 Track Report"):
        st.session_state.page = "Track"

with col4:
    if st.button("🔐 Admin"):
        st.session_state.page = "Admin"

page = st.session_state.page


create_tables()

# ---------------- HOME ----------------
if page == "Home":
    st.markdown('<div class="image-container"><img src="https://cdn-icons-png.flaticon.com/512/3064/3064197.png" width="200"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h2>Because Silence is Not Safety</h2>
        <p>
        CampusSafe empowers students and employees to report incidents
        <b>anonymously, securely, and confidently</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(check_connection())

    st.markdown('<div class="feature-cards">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='card' style='animation-delay: 0.5s;'>🔒 100% Anonymous Reporting</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card' style='animation-delay: 1s;'>🧠 AI-based Incident Analysis</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card' style='animation-delay: 1.5s;'>📊 Data-driven Safety Insights</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- REPORT ----------------
elif page == "Report":
    st.markdown("<div class='card'><h2>📢 Report an Incident</h2></div>", unsafe_allow_html=True)

    description = st.text_area("Describe the incident")
    location = st.text_input("Location / Area")
    urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High"])
    proof = st.file_uploader("Upload Proof (Optional)", type=["png","jpg","pdf","mp4","avi","mov","wmv","flv","webm","mkv"])

    if st.button("Submit Report"):
        report_id = str(uuid.uuid4())[:8]
        category = classify_incident(description)
        sentiment = sentiment_score(description)

        from datetime import datetime

        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        proof_bytes = proof.read() if proof else None
        proof_type = proof.type if proof else None

        data = {
            'report_id': report_id,
            'category': category,
            'description': description,
            'sentiment': sentiment,
            'urgency': urgency,
            'location': location,
            'status': 'Pending',
            'admin_remark': '',
            'last_updated': last_updated,
            'proof': proof_bytes,
            'proof_type': proof_type
        }

        insert_incident(data)


        st.success("Report submitted successfully!")
        st.markdown('<div style="text-align: center; margin: 20px 0;"><span style="font-size: 4em; animation: shieldGlow 1.5s ease-out;">🛡️</span></div>', unsafe_allow_html=True)
        st.info(f"Your Report ID: {report_id}")

# ---------------- TRACK ----------------
elif page == "Track":
    st.markdown("<div class='card'><h2>🔍 Track Your Report</h2></div>", unsafe_allow_html=True)

    rid = st.text_input("Enter your Report ID")

    if st.button("Check Status"):
        with st.spinner("Securely fetching report status..."):
            import time
            time.sleep(2)

            status = get_status(rid)

        if status:
            st.success(f"🟢 Current Status: {status}")
            # Also show admin remark if available
            remark = get_admin_remark(rid)
            if remark:
                st.info(f"💬 Admin Remark: {remark}")
        else:
            st.error("❌ Invalid Report ID")


# ---------------- ADMIN ----------------
elif page == "Admin":
    admin_panel()
