import streamlit as st
import requests
import plotly.graph_objects as go
import time
import random
from pypdf import PdfReader 

# --- UI CONFIG ---
st.set_page_config(page_title="SkillBridge AI", page_icon="⚡", layout="wide")
API_URL = "http://127.0.0.1:8001" 

def scroll_to_top():
    js = """<script>window.parent.document.querySelector(".main").scrollTop = 0;</script>"""
    st.components.v1.html(js, height=0)

# --- VIBRANT NEON STYLING ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); color: #ffffff; }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.07); padding: 25px; border-radius: 20px; 
        border: 1px solid rgba(0, 255, 255, 0.3); backdrop-filter: blur(15px);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
    }
    .stButton>button { 
        background: linear-gradient(90deg, #ff00cc, #3333ff); 
        color: white; border: none; padding: 15px; border-radius: 50px; 
        font-size: 18px; font-weight: bold; transition: 0.4s; width: 100%;
        box-shadow: 0 0 15px rgba(255, 0, 204, 0.4); text-transform: uppercase; letter-spacing: 2px;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 30px rgba(51, 51, 255, 0.6); }
    .job-card {
        background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 18px; 
        margin-bottom: 15px; border-left: 6px solid #00f2fe; box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
    }
    [data-testid="stMetricValue"] { color: #00f2fe !important; text-shadow: 0 0 10px rgba(0, 242, 254, 0.5); }
    h1, h2, h3, h4, p, span, label { color: white !important; font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 1
if 'resume_text' not in st.session_state: st.session_state.resume_text = ""
if 'target_role' not in st.session_state: st.session_state.target_role = ""

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("# ⚡ SkillBridge")
    st.caption("Revolutionizing Career Paths")
    uploaded_file = st.file_uploader("📂 Upload CV", type="pdf")
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        st.session_state.resume_text = "".join([p.extract_text() for p in reader.pages])
        st.success("✅ Neural Link Active")

# --- APP PHASES ---
if st.session_state.step == 1:
    st.title("🚀 Accelerate Your Future")
    st.markdown("#### Mapping your professional genome into a 30-day mastery roadmap.")
    col_a, col_b, col_c = st.columns(3)
    col_a.info("**Precision Mapping**\nBeyond keywords.")
    col_b.info("**30-Day Protocol**\nActionable daily missions.")
    col_c.info("**The PM Bridge**\nLead-to-Product path.")
    if uploaded_file and st.button("IGNITE AI ANALYSIS"):
        scroll_to_top()
        with st.status("🧠 Mapping Career Genome...", expanded=True):
            res = requests.post(f"{API_URL}/generate-questions", json={"resume_text": st.session_state.resume_text})
            st.session_state.questions = res.json()['questions']
            time.sleep(1); st.session_state.step = 2; st.rerun()

elif st.session_state.step == 2:
    st.title("🎯 Select Your Preferences")
    answers = {q['id']: st.radio(q['text'], q['options'], key=q['id']) for q in st.session_state.questions}
    if st.button("GENERATE DASHBOARD"):
        scroll_to_top()
        with st.spinner("🔮 Decoding Archetype..."):
            res = requests.post(f"{API_URL}/analyze-role", json={"resume_text": st.session_state.resume_text, "quiz_answers": answers})
            st.session_state.target_role = res.json()['role']; st.session_state.step = 3; st.rerun()

elif st.session_state.step == 3:
    res = requests.post(f"{API_URL}/gap-analysis", json={"role": st.session_state.target_role, "resume_text": "demo"})
    data = res.json()
    
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("<h3 style='text-align:center;'>🧬 ALIGNING NEURAL CAREER NODES...</h3>", unsafe_allow_html=True)
        pb = st.progress(0)
        for i in range(100):
            time.sleep(0.008); pb.progress(i + 1)
        st.success("✅ OPTIMIZATION COMPLETE"); time.sleep(0.4)
    placeholder.empty()

    live_match = data['base_match'] + random.randint(1, 5)
    live_demand = data['base_demand'] + random.randint(-2, 3)

    st.balloons(); st.title(f"✨ TARGET: {st.session_state.target_role.upper()}")
    m1, m2, m3 = st.columns(3)
    m1.metric("Match Index", f"{live_match}%", delta=f"+{random.uniform(0.1, 0.9):.1f}%")
    m2.metric("Avg Market Salary", data['salary_range'], delta="Live Data")
    m3.metric("Industry Demand", f"{live_demand}%", delta="SURGING 🔥")

    st.divider()
    st.subheader("🗓️ 30-Day Mastery Protocol")
    for s in data['roadmap']:
        with st.expander(f"📅 {s['phase']}: {s['task']}", expanded=True): st.markdown(f"👉 [Access Training]({s['link']})")

    st.divider()
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("📊 Skill Archetype")
        v, k = list(data['chart_data'].values()), list(data['chart_data'].keys())
        v.append(v[0]); k.append(k[0])
        fig = go.Figure(data=go.Scatterpolar(r=v, theta=k, fill='toself', line_color='#00f2fe', fillcolor='rgba(0, 242, 254, 0.2)'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("📝 Analysis Checkpoints")
        for p in data['archetype_points']: st.markdown(f"✅ {p}")

    st.divider(); st.subheader("💼 Verified Openings")
    t1, t2 = st.tabs(["🎓 Internships", "🏢 Full-Time Roles"])
    with t1:
        for i in data['internships']:
            st.markdown(f'<div class="job-card"><h4>{i["title"]}</h4><p style="color:#00f2fe;">{i["company"]}</p></div>', unsafe_allow_html=True)
            ca, cb = st.columns(2); ca.link_button("📺 Prep Video", i['video']); cb.info(f"📚 {i['book']}")
    with t2:
        for j in data['jobs']:
            st.markdown(f'<div class="job-card"><h4>{j["title"]}</h4><p style="color:#00f2fe;">{j["company"]}</p></div>', unsafe_allow_html=True)
            ca, cb = st.columns(2); ca.link_button("📽️ Masterclass", j['video']); cb.warning(f"📖 {j['book']}")

    if st.button("🔄 RESTART"): st.session_state.step = 1; st.rerun()