import streamlit as st
import uuid
import requests
import json
from datetime import datetime
from nlp_model import classify_incident, sentiment_score
from database import init_db, insert_incident, get_status, upload_proof
from admin import admin_panel

# Initialize Database
init_db()

# Page Configuration
st.set_page_config(
    page_title="CampusSafe",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""

<style>
/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-50px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes pulse {
    0% { transform: scale(1); box-shadow: 0 4px 8px rgba(0,0,0,0.3); }
    50% { transform: scale(1.02); box-shadow: 0 8px 16px rgba(255, 107, 107, 0.4); }
    100% { transform: scale(1); box-shadow: 0 4px 8px rgba(0,0,0,0.3); }
}
@keyframes shieldGlow {
    0% { transform: scale(0.8); opacity: 0; filter: drop-shadow(0 0 0 #4ecdc4); }
    50% { transform: scale(1.1); opacity: 1; filter: drop-shadow(0 0 20px #4ecdc4); }
    100% { transform: scale(1); opacity: 1; filter: drop-shadow(0 0 10px #4ecdc4); }
}

/* Global Styles */
body {
    background: linear-gradient(135deg, #1a1c20 0%, #0f2027 100%);
    color: #f0f2f6;
    font-family: 'Inter', sans-serif;
}

/* Headings */
h1, h2, h3 {
    font-weight: 700;
    color: white;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #ff6b6b 0%, #ee5253 100%);
    color: white;
    border-radius: 12px;
    height: 3.5em;
    width: 100%;
    border: none;
    font-weight: 600;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.stButton>button:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 8px 25px rgba(255, 107, 107, 0.5);
}

/* Cards */
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 25px;
    border-radius: 16px;
    margin: 15px 0;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    animation: fadeIn 0.8s ease-out;
}
.card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
    transition: all 0.3s ease;
}

/* Features */
.feature-box {
    text-align: center;
    padding: 20px;
    background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
    animation: slideInLeft 0.5s ease-out backwards;
}

/* Success Animation Container */
.success-container {
    text-align: center; 
    margin: 40px 0;
}
.shield-icon {
    font-size: 5rem;
    animation: shieldGlow 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
</style>
""", unsafe_allow_html=True)

# Navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"
if st.sidebar.button("📢 Report Incident"):
    st.session_state.page = "Report"
if st.sidebar.button("🔍 Track Report"):
    st.session_state.page = "Track"
if st.sidebar.button("🔐 Admin Panel"):
    st.session_state.page = "Admin"

page = st.session_state.page

def send_to_discord(report_id, proof_file, report_data):
    webhook_url = "https://discordapp.com/api/webhooks/1464631979491201211/gVERDrnBmxhLnIpJIZyHTabE7psdCxrG4WA7Y4frYQ3pOwaB6alyw80OLRMZ7Tvo_Lav"
    
    embed = {
        "title": f"🚨 New Incident Report: {report_id}",
        "description": report_data['description'],
        "color": 0xFF6B6B,
        "fields": [
            {"name": "📂 Category", "value": report_data['category'], "inline": True},
            {"name": "⚠️ Urgency", "value": report_data['urgency'], "inline": True},
            {"name": "📍 Location", "value": report_data['location'], "inline": True},
            {"name": "🧠 Sentiment Score", "value": str(report_data['sentiment']), "inline": True},
            {"name": "Status", "value": "Pending", "inline": True},
        ],
        "footer": {"text": "CampusSafe • Secure Reporting"}
    }
    
    payload = {"embeds": [embed]}
    
    try:
        if proof_file:
            proof_file.seek(0)
            files = {"file": (proof_file.name, proof_file.read(), proof_file.type)}
            response = requests.post(webhook_url, data={"payload_json": json.dumps(payload)}, files=files)
        else:
            response = requests.post(webhook_url, json=payload)
        return True
    except Exception as e:
        print(f"Discord Error: {e}")
        return False

# ---------------- HOME ----------------
if page == "Home":
    st.markdown("<h1 style='text-align: center;'>🛡️ CampusSafe</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card" style="text-align: center;">
        <h2>Safety, Simplified.</h2>
        <p>Report incidents anonymously, track their status, and help keep our campus safe.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.info("🔒 100% Anonymous")
    with col2: st.info("⚡ Instant Discord Alerts")
    with col3: st.info("📊 Admin Dashboard")

# ---------------- REPORT ----------------
elif page == "Report":
    st.markdown("<div class='card'><h2>📢 Report an Incident</h2></div>", unsafe_allow_html=True)
    
    with st.form("report_form"):
        description = st.text_area("Describe the incident")
        location = st.text_input("Location / Area")
        urgency = st.selectbox("Urgency", ["Low", "Medium", "High"])
        proof = st.file_uploader("Evidence (Optional)", type=['png', 'jpg', 'pdf', 'mp3', 'mp4'])
        
        if st.form_submit_button("Submit Report"):
            if description and location:
                report_id = str(uuid.uuid4())[:8]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                category = classify_incident(description)
                sentiment = sentiment_score(description)
                
                data = {
                    'report_id': report_id,
                    'description': description,
                    'location': location,
                    'urgency': urgency,
                    'category': category,
                    'sentiment': sentiment,
                    'timestamp': timestamp,
                    'status': 'Pending',
                    'proof_type': proof.type if proof else None
                }
                
                # 1. Upload Proof to Supabase Storage if exists
                proof_url = None
                if proof:
                    # Create a unique filename
                    file_ext = proof.name.split('.')[-1]
                    file_name = f"{report_id}.{file_ext}"
                    # Upload
                    from database import upload_proof
                    proof_url = upload_proof(proof, file_name)
                
                # Update data with proof URL
                data['proof'] = proof_url

                # 2. Save to Local DB (now Supabase)
                insert_incident(data)
                
                # 3. Send to Discord
                if send_to_discord(report_id, proof, data):
                    # SUCCESS STATE
                    st.markdown("""
                        <div class="success-container">
                            <div class="shield-icon">🛡️</div>
                            <h2 style="color: #4ecdc4; margin-top: 10px;">Report Securely Filed</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="card" style="border-left: 5px solid #4ecdc4;">
                        <p style="font-size: 1.1em;">
                            Your report has been <b>encrypted</b> and sent to the safety team. 
                            A copy is stored locally for tracking.
                        </p>
                        <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-top: 10px;">
                            <small>REFERENCE ID</small>
                            <h3 style="margin: 0; color: #ff6b6b; font-family: monospace;">{report_id}</h3>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Missing fields")

# ---------------- TRACK ----------------
elif page == "Track":
    st.markdown("<div class='card'><h2>🔍 Track Report Status</h2></div>", unsafe_allow_html=True)
    
    rid = st.text_input("Enter Report ID")
    if st.button("Check Status"):
        res = get_status(rid)
        if res:
            status, remark = res
            st.info(f"Status: **{status}**")
            if remark:
                st.success(f"Admin Remark: {remark}")
        else:
            st.error("Report not found.")

# ---------------- ADMIN ----------------
elif page == "Admin":
    admin_panel()
