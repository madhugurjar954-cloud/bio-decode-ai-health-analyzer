import streamlit as st
import json
import os
import base64
import requests
import logging
from datetime import datetime, date, timedelta
from io import BytesIO
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Bio Decode AI — Health Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
:root{--bg:#0a0f0d;--bg2:#0d1410;--card:#161f1c;--card2:#1a2520;--accent:#3dffa0;--accent2:#2dd099;--warn:#ffb84d;--danger:#ff5e5e;--blue:#4da6ff;--purple:#a78bfa;--text:#e8f0ec;--text2:#8fa898;--text3:#4a6058;--border:#1e2e28;--r:14px;--rs:10px}
*{box-sizing:border-box;margin:0;padding:0}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important;font-family:'Inter',sans-serif!important}
[data-testid="stSidebar"]{background:var(--bg2)!important;border-right:1px solid var(--border)!important}
[data-testid="stSidebar"] *{color:var(--text)!important}
.stTabs [data-baseweb="tab-list"]{background:var(--card)!important;border-radius:12px!important;padding:4px!important;border:1px solid var(--border)!important}
.stTabs [data-baseweb="tab-list"] button{color:var(--text2)!important;border-radius:9px!important;font-size:12px!important;font-weight:500!important;padding:7px 12px!important;transition:all .2s!important}
.stTabs [aria-selected="true"]{background:var(--accent)!important;color:#060e0a!important;font-weight:700!important}
.stButton>button{background:linear-gradient(135deg,var(--accent),var(--accent2))!important;color:#060e0a!important;border:none!important;border-radius:var(--rs)!important;padding:10px 22px!important;font-weight:700!important;font-size:13px!important;transition:all .25s!important;box-shadow:0 2px 12px rgba(61,255,160,.2)!important}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 6px 22px rgba(61,255,160,.35)!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input{background:var(--card)!important;color:var(--text)!important;border:1px solid var(--border)!important;border-radius:var(--rs)!important;font-size:13px!important}
.stTextInput input:focus,.stTextArea textarea:focus,.stNumberInput input:focus{border-color:var(--accent)!important;box-shadow:0 0 0 2px rgba(61,255,160,.1)!important}
.stSelectbox>div>div,.stMultiSelect>div>div{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:var(--rs)!important;color:var(--text)!important}
.stExpander{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:var(--r)!important}
.stExpander summary{color:var(--text)!important;font-weight:600!important}
.stMetric{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:16px;text-align:center}
.stMetric label{color:var(--text2)!important;font-size:12px!important}
.stMetric [data-testid="metric-container"]{background:transparent}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:18px 20px;margin:8px 0;transition:all .25s}
.card:hover{border-color:rgba(61,255,160,.3);box-shadow:0 4px 20px rgba(61,255,160,.06)}
.card.accent-left{border-left:3px solid var(--accent)}
.card.warn-left{border-left:3px solid var(--warn)}
.card.danger-left{border-left:3px solid var(--danger)}
.card.blue-left{border-left:3px solid var(--blue)}
.card.purple-left{border-left:3px solid var(--purple)}
.score-ring{width:110px;height:110px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:0 auto}
.score-num{font-size:2.2em;font-weight:800;line-height:1}
.score-of{font-size:11px;opacity:.7;letter-spacing:.05em}
.test-val{font-size:2em;font-weight:800;line-height:1}
.badge{display:inline-flex;align-items:center;gap:5px;padding:3px 11px;border-radius:99px;font-size:11px;font-weight:600;letter-spacing:.03em}
.badge-green{background:rgba(61,255,160,.12);border:1px solid rgba(61,255,160,.25);color:var(--accent)}
.badge-warn{background:rgba(255,184,77,.12);border:1px solid rgba(255,184,77,.25);color:var(--warn)}
.badge-danger{background:rgba(255,94,94,.12);border:1px solid rgba(255,94,94,.25);color:var(--danger)}
.badge-blue{background:rgba(77,166,255,.12);border:1px solid rgba(77,166,255,.25);color:var(--blue)}
.badge-purple{background:rgba(167,139,250,.12);border:1px solid rgba(167,139,250,.25);color:var(--purple)}
.meal-box{background:var(--card2);border:1px solid var(--border);border-radius:var(--rs);padding:13px 15px;margin:5px 0}
.meal-head{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:var(--accent);margin-bottom:6px}
.meal-body{font-size:13px;color:var(--text2);line-height:1.65}
.med-dot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:6px}
.dot-green{background:var(--accent)}
.dot-red{background:var(--danger)}
.dot-gray{background:var(--text3)}
.progress-bar{height:6px;background:var(--card2);border-radius:99px;overflow:hidden;margin:4px 0}
.progress-fill{height:100%;border-radius:99px;transition:width .6s ease}
.streak-badge{background:linear-gradient(135deg,#ff9500,#ff5e00);color:white;padding:6px 14px;border-radius:99px;font-size:13px;font-weight:700;display:inline-block}
.hero-title{font-size:2.6em;font-weight:800;background:linear-gradient(135deg,var(--accent),#00d4ff,var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.15;margin-bottom:10px}
.hero-sub{color:var(--text2);font-size:14px;font-weight:300;line-height:1.7;max-width:580px}
.section-head{font-size:16px;font-weight:700;color:var(--text);margin:22px 0 14px;display:flex;align-items:center;gap:8px}
.divider{height:1px;background:var(--border);margin:18px 0}
.empty{text-align:center;padding:48px 20px;color:var(--text3)}
.empty-icon{font-size:44px;margin-bottom:12px}
.privacy-note{background:rgba(61,255,160,.05);border:1px solid rgba(61,255,160,.12);border-radius:var(--rs);padding:11px 16px;font-size:12px;color:var(--text2);margin:10px 0}
.disclaimer{background:rgba(255,94,94,.04);border:1px solid rgba(255,94,94,.12);border-radius:var(--rs);padding:14px 18px;font-size:12px;color:var(--text3);line-height:1.7;margin:14px 0}
.macro-bar{margin:6px 0}
.macro-label{font-size:12px;color:var(--text2);margin-bottom:3px;display:flex;justify-content:space-between}
</style>
""", unsafe_allow_html=True)

# ===== SESSION STATE =====
DEFAULTS = {
    "groq_key": "",
    "analysis_result": None,
    "analysis_history": [],
    "medicines": [],
    "workouts": [],
    "user_profile": {"age": 25, "gender": "Not specified", "conditions": "", "weight": 60, "height": 165, "activity": "Moderate"},
    "med_logs": {},
    "workout_logs": {},
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        if k == "groq_key":
            try:
                st.session_state[k] = st.secrets["GROQ_API_KEY"]
            except:
                st.session_state[k] = os.getenv("GROQ_API_KEY", "")
        else:
            st.session_state[k] = v

# ===== LANGUAGE PROMPTS =====
LANG_PROMPTS = {
    "English": "Respond entirely in English. Use very simple, friendly language that anyone can understand — avoid complex medical jargon.",
    "हिन्दी (Hindi)": "Respond entirely in Hindi using Devanagari script. Use very simple Hindi that anyone can understand.",
    "English + हिन्दी": "Write English first, then Hindi translation below. Use simple language in both.",
    "ਪੰਜਾਬੀ (Punjabi)": "Respond entirely in Punjabi using Gurmukhi script. Use simple everyday Punjabi.",
    "ગુજરાતી (Gujarati)": "Respond entirely in Gujarati script. Use simple everyday Gujarati.",
    "Español": "Respond entirely in Spanish. Use simple, clear Spanish.",
    "العربية": "Respond entirely in Arabic. Use simple, clear Arabic.",
}

# ===== HELPERS =====
def safe_int(v, default=0):
    try:
        return int(str(v).strip())
    except:
        return default

def today_str():
    return date.today().isoformat()

def call_groq(messages, max_tokens=7000):
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json={"model": "llama-3.3-70b-versatile", "messages": messages, "max_tokens": max_tokens, "temperature": 0.3},
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {st.session_state.groq_key}"},
            timeout=60
        )
        if r.status_code == 200:
            return True, r.json()["choices"][0]["message"]["content"]
        return False, r.json().get("error", {}).get("message", "API error")
    except requests.Timeout:
        return False, "Request timed out. Please try again."
    except Exception as e:
        return False, str(e)

def analyze_labs(lab_input, language, profile, mode="text"):
    lang = LANG_PROMPTS.get(language, LANG_PROMPTS["English"])
    ctx = f"Age: {profile['age']}. Sex: {profile['gender']}. Weight: {profile['weight']}kg. Height: {profile['height']}cm. Activity: {profile['activity']}."
    if profile['conditions']:
        ctx += f" Known conditions: {profile['conditions']}."

    system = f"""You are Bio Decode AI — a world-class medical analyst, clinical nutritionist, and health educator.
{lang}

CRITICAL RULES:
1. Explain everything in the SIMPLEST possible language — like explaining to a 12-year-old
2. For EVERY test, explain WHY it is high/low in simple terms like "Your kidney is having trouble filtering waste"
3. Be warm, caring, and encouraging — not scary
4. Give VERY specific food recommendations based on the patient's profile
5. Calculate personalized daily nutrition needs based on weight, height, age, gender, activity level

Return ONLY valid compact JSON, absolutely no markdown:
{{"health_score":"0-100","score_summary":"warm 2-3 sentence summary in simple language","overall_status":"Good/Needs Attention/See a Doctor","tests":[{{"name":"test name","name_local":"local name","value":"number","unit":"unit","status":"Normal/High/Low/Critical/Borderline","normal_range":"range with unit","simple_explanation":"explain in 1-2 sentences as if talking to a child — what is this test, what does your result mean, WHY is it high/low","what_happening_in_body":"1 sentence explaining what is happening in the body right now because of this value","symptoms":["symptom in simple words"],"good_foods":["specific food 1","specific food 2","specific food 3"],"avoid_foods":["avoid item 1","avoid item 2"],"action":"what to do — e.g. See doctor, Monitor, No action needed","urgency":"Urgent/Soon/Routine/Normal"}}],"nutrition_plan":{{"daily_calories":number,"daily_protein_g":number,"daily_carbs_g":number,"daily_fat_g":number,"daily_fiber_g":number,"daily_water_L":number,"plan_summary":"2 sentence personalized nutrition summary","breakfast":{{"meal":"specific meal","calories":number,"why":"why this is good for you"}},"lunch":{{"meal":"specific meal","calories":number,"why":"why this is good for you"}},"dinner":{{"meal":"specific meal","calories":number,"why":"why this is good for you"}},"snacks":{{"meal":"healthy snack options","calories":number}},"foods_avoid":"specific foods to avoid based on ALL lab results combined","indian_foods":"if applicable, suggest specific Indian foods that are beneficial"}},"doctor_advice":[{{"test":"test name","urgency":"Urgent/Soon/Routine","what_to_tell_doctor":"exact sentence patient should say to doctor","timeframe":"when to see doctor e.g. within 48 hours, within 2 weeks"}}],"lifestyle_tips":["3-4 specific actionable tips based on results"],"positive_note":"one encouraging sentence to end on a positive note"}}
Patient: {ctx}"""

    user = f"Analyze these lab values in detail:\n\n{lab_input}" if mode == "text" else "Extract ALL lab values from this image and analyze them."
    ok, raw = call_groq([{"role": "system", "content": system}, {"role": "user", "content": user}])
    if not ok:
        return False, raw
    try:
        return True, json.loads(raw.replace("```json", "").replace("```", "").strip())
    except:
        return False, "Could not parse response. Please try again with clearer lab values."

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("## 🧬 Bio Decode AI")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("**🌐 Language**")
    language = st.selectbox("", list(LANG_PROMPTS.keys()), label_visibility="collapsed")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.groq_key:
        st.markdown("**🔑 API Key**")
        k = st.text_input("", type="password", placeholder="gsk_...", label_visibility="collapsed")
        if k:
            st.session_state.groq_key = k
            st.success("✅ Key saved!")
            st.rerun()
    else:
        st.success("✅ API Key ready")
        if st.button("Change Key", use_container_width=True):
            st.session_state.groq_key = ""
            st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("**👤 Your Profile**")
    p = st.session_state.user_profile
    p["age"] = st.number_input("Age", 1, 120, p["age"])
    p["gender"] = st.selectbox("Gender", ["Not specified", "Female", "Male", "Other"])
    p["weight"] = st.number_input("Weight (kg)", 20, 300, p["weight"])
    p["height"] = st.number_input("Height (cm)", 100, 250, p["height"])
    p["activity"] = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
    p["conditions"] = st.text_input("Known Conditions", placeholder="e.g. Diabetes, BP", value=p["conditions"])

    # BMI
    if p["weight"] and p["height"]:
        bmi = round(p["weight"] / ((p["height"] / 100) ** 2), 1)
        bmi_label = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
        st.markdown(f"**BMI:** {bmi} — {bmi_label}")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:var(--text3);line-height:1.9">🔒 Zero data stored<br>🔒 No tracking<br>🔒 HTTPS encrypted<br>🔒 Photos deleted instantly</div>', unsafe_allow_html=True)

# ===== HERO =====
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown('<div class="hero-title">🧬 Bio Decode AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Your personal AI health companion. Understand your lab reports in simple language, track medicines, log workouts, and get a nutrition plan tailored just for you — in your language.</div>', unsafe_allow_html=True)

with c2:
    scores = [safe_int(h.get("health_score", 0)) for h in st.session_state.analysis_history]
    avg_score = sum(scores) // len(scores) if scores else 0
    today = today_str()
    meds_taken = sum(1 for k, v in st.session_state.med_logs.get(today, {}).items() if v)
    total_meds = len(st.session_state.medicines)

    st.markdown(f"""
<div class="card" style="text-align:center;margin-top:10px">
<div style="font-size:2.5em;font-weight:800;color:var(--accent)">{avg_score}</div>
<div style="font-size:12px;color:var(--text2)">Avg Health Score</div>
<div style="margin-top:10px;font-size:13px;color:var(--text2)">💊 {meds_taken}/{total_meds} meds today</div>
<div style="font-size:13px;color:var(--text2)">📊 {len(st.session_state.analysis_history)} analyses done</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ===== TABS =====
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📝 Analyze", "📷 Photo", "💊 Medicines",
    "🏋️ Workout", "📊 History", "📈 Compare", "ℹ️ Guide"
])

# ==================== TAB 1: ANALYZE ====================
with tab1:
    st.markdown('<div class="section-head">📝 Enter Your Lab Values</div>', unsafe_allow_html=True)

    lab_input = st.text_area(
        "Paste or type your lab report values",
        placeholder="Example:\nHemoglobin: 10.2 g/dL\nTSH: 6.8 mIU/L\nFasting Blood Sugar: 148 mg/dL\nCreatinine: 1.8 mg/dL\nVitamin D: 14 ng/mL\nLDL: 155 mg/dL",
        height=160, key="lab_text"
    )

    st.markdown("**Quick Samples:**")
    sc = st.columns(6)
    samples = {
        "Thyroid": "TSH: 7.2 mIU/L\nT3: 0.8 ng/mL\nT4: 5.5 µg/dL",
        "Diabetes": "Fasting Blood Sugar: 148 mg/dL\nHbA1c: 7.2%\nPost Prandial Sugar: 210 mg/dL",
        "Anemia": "Hemoglobin: 8.5 g/dL\nHematocrit: 28%\nFerritin: 6 ng/mL\nMCV: 72 fL",
        "Kidney": "Creatinine: 2.1 mg/dL\nBUN: 35 mg/dL\neGFR: 38 mL/min\nUric Acid: 8.5 mg/dL",
        "Liver": "SGPT: 85 U/L\nSGOT: 72 U/L\nBilirubin: 2.4 mg/dL\nAlkaline Phosphatase: 165 U/L",
        "Full": "Hemoglobin: 9.8 g/dL\nFasting Sugar: 138 mg/dL\nTSH: 5.9 mIU/L\nCholesterol: 235 mg/dL\nLDL: 155 mg/dL\nHDL: 38 mg/dL\nCreatinine: 1.6 mg/dL\nVitamin D: 14 ng/mL"
    }
    for i, (label, val) in enumerate(samples.items()):
        if sc[i].button(label, use_container_width=True, key=f"samp_{i}"):
            st.session_state["lab_text"] = val
            st.rerun()

    st.markdown('<div class="privacy-note">🔒 Your lab values are analyzed instantly by AI and never stored or shared with anyone.</div>', unsafe_allow_html=True)

    if st.button("🔬 Analyze My Lab Report", use_container_width=True, key="btn_analyze"):
        val = st.session_state.get("lab_text", "")
        if not val or len(val.strip()) < 5:
            st.error("❌ Please enter your lab values first.")
        elif not any(c.isdigit() for c in val):
            st.error("❌ No numbers found. Please include values like: Hemoglobin: 10.2 g/dL")
        elif not st.session_state.groq_key:
            st.error("❌ Please add your Groq API Key in the sidebar.")
        else:
            with st.spinner("🧬 AI is analyzing your report — this takes about 10 seconds..."):
                ok, result = analyze_labs(val, language, st.session_state.user_profile, "text")
                if ok:
                    st.session_state.analysis_result = result
                    st.session_state.analysis_history.append({
                        "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                        "health_score": result.get("health_score", 0),
                        "analysis": result,
                        "input": val
                    })
                    st.success("✅ Analysis complete! Scroll down to see your results.")
                    st.rerun()
                else:
                    st.error(f"❌ {result}")

# ==================== TAB 2: PHOTO ====================
with tab2:
    st.markdown('<div class="section-head">📷 Upload Lab Report Photo</div>', unsafe_allow_html=True)
    st.markdown('<div class="privacy-note">🔒 Your photo is analyzed instantly and permanently deleted. Never stored or shared.</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload a clear photo of your lab report (JPG or PNG)", type=["jpg", "jpeg", "png"])
    if uploaded:
        if uploaded.size > 5 * 1024 * 1024:
            st.error("❌ Image too large. Please upload under 5MB.")
        else:
            st.image(uploaded, caption="Your lab report", use_container_width=True)
            img_b64 = base64.b64encode(uploaded.getvalue()).decode()
            if st.button("🔬 Analyze This Photo", use_container_width=True, key="btn_photo"):
                if not st.session_state.groq_key:
                    st.error("❌ Please add your Groq API Key in the sidebar.")
                else:
                    with st.spinner("📸 Reading your lab report..."):
                        ok, result = analyze_labs(img_b64, language, st.session_state.user_profile, "photo")
                        if ok:
                            st.session_state.analysis_result = result
                            st.session_state.analysis_history.append({
                                "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                                "health_score": result.get("health_score", 0),
                                "analysis": result,
                                "input": "Photo upload"
                            })
                            st.success("✅ Done! Scroll down for results.")
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")

# ==================== TAB 3: MEDICINES ====================
with tab3:
    st.markdown('<div class="section-head">💊 Medicine Tracker</div>', unsafe_allow_html=True)

    with st.expander("➕ Add New Medicine", expanded=len(st.session_state.medicines) == 0):
        c1, c2, c3 = st.columns(3)
        with c1:
            mn = st.text_input("Medicine Name", placeholder="e.g. Metformin", key="mn")
        with c2:
            md = st.text_input("Dosage", placeholder="e.g. 500mg", key="md")
        with c3:
            mf = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "Weekly", "As needed"], key="mf")

        mt = st.multiselect("When to take", ["Morning", "Afternoon", "Evening", "Night", "Before Food", "After Food", "Bedtime"], key="mt")
        c4, c5 = st.columns(2)
        with c4:
            mdur = st.text_input("Duration", placeholder="e.g. 30 days, Ongoing", key="mdur")
        with c5:
            mtype = st.selectbox("Type", ["Tablet", "Capsule", "Syrup", "Injection", "Drops", "Inhaler", "Other"], key="mtype")
        mnotes = st.text_area("Doctor's Instructions", placeholder="e.g. Take with food, avoid alcohol", height=70, key="mnotes")

        if st.button("➕ Add Medicine", use_container_width=True, key="add_med_btn"):
            if mn:
                st.session_state.medicines.append({
                    "id": datetime.now().isoformat(),
                    "name": mn, "dose": md, "frequency": mf,
                    "time": mt, "duration": mdur, "type": mtype,
                    "notes": mnotes, "added": today_str()
                })
                st.success(f"✅ {mn} added!")
                st.rerun()
            else:
                st.error("❌ Please enter medicine name.")

    if st.session_state.medicines:
        today = today_str()
        if today not in st.session_state.med_logs:
            st.session_state.med_logs[today] = {}

        st.markdown('<div class="section-head">✅ Today\'s Medicines</div>', unsafe_allow_html=True)

        total = len(st.session_state.medicines)
        taken = sum(1 for m in st.session_state.medicines if st.session_state.med_logs[today].get(m["id"], False))
        pct = int((taken / total) * 100) if total else 0

        st.markdown(f"""
<div class="card accent-left">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
<span style="font-size:14px;font-weight:600">Today's Progress</span>
<span style="font-size:20px;font-weight:800;color:var(--accent)">{taken}/{total}</span>
</div>
<div class="progress-bar"><div class="progress-fill" style="width:{pct}%;background:var(--accent)"></div></div>
<div style="font-size:12px;color:var(--text2);margin-top:4px">{pct}% medicines taken today</div>
</div>
""", unsafe_allow_html=True)

        time_slots = ["Morning", "Afternoon", "Evening", "Night", "Before Food", "After Food", "Bedtime"]
        slot_icons = {"Morning": "🌅", "Afternoon": "☀️", "Evening": "🌆", "Night": "🌙",
                      "Before Food": "🍽️", "After Food": "🍽️", "Bedtime": "😴"}

        for slot in time_slots:
            slot_meds = [m for m in st.session_state.medicines if slot in (m.get("time") or [])]
            if slot_meds:
                st.markdown(f"**{slot_icons.get(slot,'')} {slot}**")
                for m in slot_meds:
                    mid = m["id"]
                    is_taken = st.session_state.med_logs[today].get(mid, False)
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1:
                        dot = "dot-green" if is_taken else "dot-gray"
                        st.markdown(f'<div style="padding:8px 0"><span class="med-dot {dot}"></span><b>{m["name"]}</b> {m["dose"]} — <span style="color:var(--text2);font-size:12px">{m["type"]}</span></div>', unsafe_allow_html=True)
                    with c2:
                        if is_taken:
                            if st.button("✅ Taken", key=f"untake_{mid}_{slot}", use_container_width=True):
                                st.session_state.med_logs[today][mid] = False
                                st.rerun()
                        else:
                            if st.button("Mark Taken", key=f"take_{mid}_{slot}", use_container_width=True):
                                st.session_state.med_logs[today][mid] = True
                                st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-head">📊 Adherence Tracker (Last 7 Days)</div>', unsafe_allow_html=True)

        days = [(date.today() - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
        day_labels = [(date.today() - timedelta(days=i)).strftime("%d %b") for i in range(6, -1, -1)]

        adherence_data = []
        for d in days:
            logs = st.session_state.med_logs.get(d, {})
            if logs and total > 0:
                taken_d = sum(1 for m in st.session_state.medicines if logs.get(m["id"], False))
                adherence_data.append(int((taken_d / total) * 100))
            else:
                adherence_data.append(None)

        cols = st.columns(7)
        for i, (label, pct_d) in enumerate(zip(day_labels, adherence_data)):
            with cols[i]:
                if pct_d is None:
                    color = "var(--text3)"
                    emoji = "○"
                    val_str = "—"
                elif pct_d >= 80:
                    color = "var(--accent)"
                    emoji = "✅"
                    val_str = f"{pct_d}%"
                elif pct_d >= 50:
                    color = "var(--warn)"
                    emoji = "⚠️"
                    val_str = f"{pct_d}%"
                else:
                    color = "var(--danger)"
                    emoji = "❌"
                    val_str = f"{pct_d}%"
                st.markdown(f'<div style="text-align:center;font-size:11px;color:var(--text2)">{label}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align:center;font-size:18px">{emoji}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align:center;font-size:12px;font-weight:700;color:{color}">{val_str}</div>', unsafe_allow_html=True)

        streak = 0
        for d in reversed(days):
            logs = st.session_state.med_logs.get(d, {})
            if logs and total > 0:
                taken_d = sum(1 for m in st.session_state.medicines if logs.get(m["id"], False))
                if taken_d == total:
                    streak += 1
                else:
                    break
            else:
                break

        if streak > 0:
            st.markdown(f'<div style="margin-top:12px"><span class="streak-badge">🔥 {streak} day streak!</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-head">💊 All Medicines</div>', unsafe_allow_html=True)
        for i, m in enumerate(st.session_state.medicines):
            c1, c2 = st.columns([5, 1])
            with c1:
                times_str = ", ".join(m.get("time") or []) or "Not set"
                st.markdown(f"""
<div class="card warn-left">
<div style="font-size:14px;font-weight:700">{m['name']} <span style="font-size:12px;color:var(--warn);font-weight:400">{m['dose']}</span> <span class="badge badge-warn">{m['type']}</span></div>
<div style="font-size:12px;color:var(--text2);margin-top:5px">⏰ {times_str} &nbsp;|&nbsp; 🔁 {m['frequency']} &nbsp;|&nbsp; 📅 {m.get('duration','Ongoing')}</div>
{f"<div style='font-size:12px;color:var(--text3);margin-top:3px'>📋 {m['notes']}</div>" if m.get('notes') else ''}
</div>
""", unsafe_allow_html=True)
            with c2:
                if st.button("🗑️", key=f"delmed_{i}", use_container_width=True):
                    st.session_state.medicines.pop(i)
                    st.rerun()

        if st.button("🗑️ Clear All Medicines", use_container_width=True, key="clearmed"):
            st.session_state.medicines = []
            st.session_state.med_logs = {}
            st.rerun()
    else:
        st.markdown('<div class="empty"><div class="empty-icon">💊</div><p>No medicines added yet.<br>Add your medicines above to start tracking.</p></div>', unsafe_allow_html=True)

# ==================== TAB 4: WORKOUT ====================
with tab4:
    st.markdown('<div class="section-head">🏋️ Workout Tracker</div>', unsafe_allow_html=True)

    with st.expander("➕ Log Today's Workout", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            wtype = st.selectbox("Exercise Type", ["Walking", "Running", "Cycling", "Yoga", "Gym/Weights", "Swimming", "Dance", "HIIT", "Stretching", "Sports", "Other"], key="wtype")
        with c2:
            wdur = st.number_input("Duration (minutes)", 5, 300, 30, key="wdur")
        with c3:
            wint = st.selectbox("Intensity", ["Light", "Moderate", "Intense", "Very Intense"], key="wint")

        c4, c5 = st.columns(2)
        with c4:
            wcal = st.number_input("Calories Burned (approx)", 0, 2000, 0, key="wcal")
        with c5:
            wmood = st.selectbox("How did you feel?", ["😊 Great", "🙂 Good", "😐 Okay", "😔 Tired", "💪 Energized"], key="wmood")

        wnotes = st.text_input("Notes (optional)", placeholder="e.g. Morning walk in park", key="wnotes")

        if st.button("➕ Log Workout", use_container_width=True, key="add_workout"):
            today = today_str()
            if today not in st.session_state.workout_logs:
                st.session_state.workout_logs[today] = []
            st.session_state.workout_logs[today].append({
                "type": wtype, "duration": wdur, "intensity": wint,
                "calories": wcal, "mood": wmood, "notes": wnotes,
                "time": datetime.now().strftime("%I:%M %p")
            })
            st.success(f"✅ {wtype} — {wdur} mins logged!")
            st.rerun()

    st.markdown('<div class="section-head">📅 This Week\'s Activity</div>', unsafe_allow_html=True)

    days_week = [(date.today() - timedelta(days=i)) for i in range(6, -1, -1)]
    total_min_week = 0
    total_cal_week = 0

    cols = st.columns(7)
    for i, d in enumerate(days_week):
        dstr = d.isoformat()
        workouts = st.session_state.workout_logs.get(dstr, [])
        total_min = sum(w["duration"] for w in workouts)
        total_cal = sum(w["calories"] for w in workouts)
        total_min_week += total_min
        total_cal_week += total_cal

        with cols[i]:
            if total_min >= 60:
                color = "var(--accent)"
                emoji = "🔥"
            elif total_min >= 30:
                color = "var(--warn)"
                emoji = "✅"
            elif total_min > 0:
                color = "var(--blue)"
                emoji = "🏃"
            else:
                color = "var(--text3)"
                emoji = "○"

            st.markdown(f'<div style="text-align:center;font-size:11px;color:var(--text2)">{d.strftime("%a")}<br>{d.strftime("%d")}</div>', unsafe_allow_html=True)
            height = max(4, min(60, total_min))
            st.markdown(f'<div style="text-align:center;margin:4px 0"><div style="width:28px;height:{height}px;background:{color};border-radius:4px;margin:0 auto;opacity:0.85"></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center;font-size:11px;color:{color};font-weight:700">{total_min}m</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("This Week", f"{total_min_week} mins")
    with c2:
        st.metric("Calories Burned", f"{total_cal_week} kcal")
    with c3:
        active_days = sum(1 for d in days_week if st.session_state.workout_logs.get(d.isoformat()))
        st.metric("Active Days", f"{active_days}/7")

    # Workout streak
    wstreak = 0
    for d in reversed(days_week):
        if st.session_state.workout_logs.get(d.isoformat()):
            wstreak += 1
        else:
            break
    if wstreak > 0:
        st.markdown(f'<div style="margin:8px 0"><span class="streak-badge">🔥 {wstreak} day workout streak!</span></div>', unsafe_allow_html=True)

    today_workouts = st.session_state.workout_logs.get(today_str(), [])
    if today_workouts:
        st.markdown('<div class="section-head">Today\'s Workouts</div>', unsafe_allow_html=True)
        for i, w in enumerate(today_workouts):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"""
<div class="card blue-left">
<div style="font-size:14px;font-weight:700">{w['type']} <span class="badge badge-blue">{w['intensity']}</span></div>
<div style="font-size:12px;color:var(--text2);margin-top:4px">⏱️ {w['duration']} mins &nbsp;|&nbsp; 🔥 {w['calories']} kcal &nbsp;|&nbsp; {w['mood']} &nbsp;|&nbsp; 🕐 {w['time']}</div>
{f"<div style='font-size:12px;color:var(--text3);margin-top:3px'>{w['notes']}</div>" if w.get('notes') else ''}
</div>
""", unsafe_allow_html=True)
            with c2:
                if st.button("🗑️", key=f"delw_{i}", use_container_width=True):
                    st.session_state.workout_logs[today_str()].pop(i)
                    st.rerun()

# ==================== TAB 5: HISTORY ====================
with tab5:
    st.markdown('<div class="section-head">📊 Your Health History</div>', unsafe_allow_html=True)

    if st.session_state.analysis_history:
        scores = [safe_int(h.get("health_score", 0)) for h in st.session_state.analysis_history]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Analyses", len(scores))
        c2.metric("Average Score", f"{sum(scores)//len(scores)}/100")
        c3.metric("Best Score", f"{max(scores)}/100")
        c4.metric("Latest Score", f"{scores[-1]}/100")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        for h in reversed(st.session_state.analysis_history):
            sc = safe_int(h.get("health_score", 0))
            icon = "🟢" if sc >= 70 else "🟡" if sc >= 40 else "🔴"
            status = "Good" if sc >= 70 else "Needs Attention" if sc >= 40 else "Needs Care"
            with st.expander(f"{icon} {h['date']} — Score: {sc}/100 — {status}"):
                st.markdown(f"**Summary:** {h['analysis'].get('score_summary','')}")
                if h['analysis'].get('tests'):
                    for t in h['analysis']['tests']:
                        sl = t.get("status","").lower()
                        bg = "🟢" if "normal" in sl else "🔴" if "high" in sl or "critical" in sl else "🟡"
                        st.markdown(f"{bg} **{t.get('name','')}**: {t.get('value','')} {t.get('unit','')} — {t.get('status','')}")
                if h['analysis'].get('lifestyle_tips'):
                    st.markdown("**Tips:**")
                    for tip in h['analysis']['lifestyle_tips']:
                        st.markdown(f"• {tip}")
                if h['analysis'].get('positive_note'):
                    st.markdown(f"💚 *{h['analysis']['positive_note']}*")

        if st.button("🗑️ Clear History", use_container_width=True, key="clhist"):
            st.session_state.analysis_history = []
            st.session_state.analysis_result = None
            st.rerun()
    else:
        st.markdown('<div class="empty"><div class="empty-icon">📊</div><p>No analyses yet.<br>Complete your first lab analysis to start tracking.</p></div>', unsafe_allow_html=True)

# ==================== TAB 6: COMPARE ====================
with tab6:
    st.markdown('<div class="section-head">📈 Compare Two Reports</div>', unsafe_allow_html=True)
    if len(st.session_state.analysis_history) >= 2:
        c1, c2 = st.columns(2)
        with c1:
            idx1 = st.selectbox("First Report", range(len(st.session_state.analysis_history)),
                                format_func=lambda i: f"{st.session_state.analysis_history[i]['date']} ({st.session_state.analysis_history[i]['health_score']}/100)", key="cmp1")
        with c2:
            idx2 = st.selectbox("Second Report", range(len(st.session_state.analysis_history)),
                                format_func=lambda i: f"{st.session_state.analysis_history[i]['date']} ({st.session_state.analysis_history[i]['health_score']}/100)", key="cmp2")
        if idx1 != idx2:
            r1 = st.session_state.analysis_history[idx1]
            r2 = st.session_state.analysis_history[idx2]
            s1, s2 = safe_int(r1['health_score']), safe_int(r2['health_score'])
            diff = s2 - s1
            c1, c2, c3 = st.columns(3)
            c1.metric("Report 1", f"{s1}/100")
            c2.metric("Report 2", f"{s2}/100", delta=diff)
            c3.metric("Trend", "📈 Improving" if diff > 0 else "📉 Declining" if diff < 0 else "➡️ Same")

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("**Test Comparison:**")
            t1 = {t['name']: t for t in r1['analysis'].get('tests', [])}
            t2 = {t['name']: t for t in r2['analysis'].get('tests', [])}
            for name in set(t1.keys()) | set(t2.keys()):
                a, b = t1.get(name, {}), t2.get(name, {})
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**{name}**")
                c2.markdown(f"{a.get('value','N/A')} {a.get('unit','')} — {a.get('status','N/A')}")
                c3.markdown(f"{b.get('value','N/A')} {b.get('unit','')} — {b.get('status','N/A')}")
        else:
            st.warning("Please select two different reports.")
    elif len(st.session_state.analysis_history) == 1:
        st.info("Complete at least 2 analyses to compare.")
    else:
        st.markdown('<div class="empty"><div class="empty-icon">📈</div><p>No history yet.</p></div>', unsafe_allow_html=True)

# ==================== TAB 7: GUIDE ====================
with tab7:
    st.markdown('<div class="section-head">ℹ️ How to Use Bio Decode AI</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
**📝 Analyze Lab Report**
1. Enter age, weight, height in sidebar
2. Paste your lab values
3. Click Analyze
4. Get simple explanation of every test

**📷 Upload Photo**
1. Take clear photo of lab report
2. Upload it
3. AI reads values automatically

**💊 Medicine Tracker**
1. Add your medicines
2. Mark as taken each day
3. See your 7-day adherence graph
4. Track your streak 🔥
        """)
    with c2:
        st.markdown("""
**🏋️ Workout Tracker**
1. Log your daily exercise
2. See weekly activity bar chart
3. Track calories and streak

**📊 Health History**
- All analyses saved automatically
- Track health score over time

**📈 Compare Reports**
- Compare two lab reports side by side
- See what improved or worsened

**🌐 Languages**
English, Hindi, Punjabi, Gujarati, Spanish, Arabic
        """)

    st.markdown('<div class="disclaimer">⚕️ <b>Medical Disclaimer:</b> Bio Decode AI is for health literacy and educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider before making any health decisions. Do not use for self-diagnosis or self-treatment.</div>', unsafe_allow_html=True)

# ==================== RESULTS ====================
if st.session_state.analysis_result:
    analysis = st.session_state.analysis_result
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-head">📊 Your Health Analysis Report</div>', unsafe_allow_html=True)

    # Health Score
    if "health_score" in analysis:
        sc = safe_int(analysis["health_score"])
        if sc >= 70:
            col, border, emoji = "#3dffa0", "rgba(61,255,160,.3)", "🟢"
        elif sc >= 40:
            col, border, emoji = "#ffb84d", "rgba(255,184,77,.3)", "🟡"
        else:
            col, border, emoji = "#ff5e5e", "rgba(255,94,94,.3)", "🔴"

        c1, c2 = st.columns([1, 3])
        with c1:
            st.markdown(f"""
<div class="score-ring" style="background:{col}15;border:3px solid {col};margin-top:10px">
<div class="score-num" style="color:{col}">{sc}</div>
<div class="score-of" style="color:{col}">/100</div>
</div>
""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
<div class="card" style="border-color:{border};margin-top:10px">
<div style="font-size:18px;font-weight:700;color:{col};margin-bottom:8px">{emoji} {analysis.get('overall_status','')}</div>
<div style="font-size:14px;color:var(--text2);line-height:1.7">{analysis.get('score_summary','')}</div>
{f"<div style='margin-top:12px;font-size:13px;color:var(--accent);font-style:italic'>💚 {analysis.get('positive_note','')}</div>" if analysis.get('positive_note') else ''}
</div>
""", unsafe_allow_html=True)

    # Lifestyle tips
    if analysis.get("lifestyle_tips"):
        st.markdown('<div class="section-head">💡 Personalized Health Tips</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        for i, tip in enumerate(analysis["lifestyle_tips"]):
            with c1 if i % 2 == 0 else c2:
                st.markdown(f'<div class="card accent-left" style="padding:12px 16px;font-size:13px">✨ {tip}</div>', unsafe_allow_html=True)

    # Test Results
    if analysis.get("tests"):
        st.markdown('<div class="section-head">🔬 Your Test Results — In Simple Language</div>', unsafe_allow_html=True)

        for test in analysis["tests"]:
            sl = test.get("status", "").lower()
            urgency = test.get("urgency", "Normal")
            if "normal" in sl or "good" in sl:
                icon, card_cls, val_col, ubadge = "✅", "accent-left", "var(--accent)", "badge-green"
            elif "critical" in sl or urgency == "Urgent":
                icon, card_cls, val_col, ubadge = "🚨", "danger-left", "var(--danger)", "badge-danger"
            elif "high" in sl:
                icon, card_cls, val_col, ubadge = "⚠️", "danger-left", "var(--danger)", "badge-danger"
            elif "low" in sl or "borderline" in sl:
                icon, card_cls, val_col, ubadge = "📍", "warn-left", "var(--warn)", "badge-warn"
            else:
                icon, card_cls, val_col, ubadge = "❓", "accent-left", "var(--text2)", "badge-green"

            with st.expander(f"{icon} {test.get('name','')} — {test.get('value','')} {test.get('unit','')} — {test.get('status','')}", expanded=False):
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"""
<div class="card {card_cls}" style="text-align:center">
<div style="font-size:13px;color:var(--text2);margin-bottom:6px">{test.get('name','')}</div>
{f"<div style='font-size:12px;color:var(--text3);margin-bottom:4px'>{test.get('name_local','')}</div>" if test.get('name_local') else ''}
<div style="font-size:2.2em;font-weight:800;color:{val_col};line-height:1">{test.get('value','')}</div>
<div style="font-size:13px;color:var(--text2)">{test.get('unit','')}</div>
<div style="font-size:11px;color:var(--text3);margin-top:6px">Normal: {test.get('normal_range','')}</div>
<div style="margin-top:10px"><span class="badge {ubadge}">{test.get('status','')}</span></div>
{f"<div style='margin-top:6px'><span class='badge badge-danger'>{urgency}</span></div>" if urgency in ['Urgent','Soon'] else ''}
</div>
""", unsafe_allow_html=True)
                with c2:
                    if test.get("simple_explanation"):
                        st.markdown("**🗣️ What does this mean?**")
                        st.markdown(f'<div style="font-size:14px;color:var(--text);line-height:1.7;background:var(--card2);padding:12px;border-radius:10px">{test.get("simple_explanation","")}</div>', unsafe_allow_html=True)
                    if test.get("what_happening_in_body"):
                        st.markdown(f'<div style="margin-top:8px;font-size:13px;color:var(--text2);font-style:italic">🫀 {test.get("what_happening_in_body","")}</div>', unsafe_allow_html=True)

                if test.get("symptoms"):
                    st.markdown("**Possible Symptoms:**")
                    cols = st.columns(min(3, len(test["symptoms"])))
                    for j, sym in enumerate(test["symptoms"]):
                        cols[j % len(cols)].markdown(f"• {sym}")

                if test.get("good_foods") or test.get("avoid_foods"):
                    c1, c2 = st.columns(2)
                    with c1:
                        if test.get("good_foods"):
                            st.markdown("✅ **Eat these:**")
                            for f in test["good_foods"]:
                                st.markdown(f"• {f}")
                    with c2:
                        if test.get("avoid_foods"):
                            st.markdown("❌ **Avoid these:**")
                            for f in test["avoid_foods"]:
                                st.markdown(f"• {f}")

    # Nutrition Plan
    if analysis.get("nutrition_plan"):
        st.markdown('<div class="section-head">🥗 Your Personalized Nutrition Plan</div>', unsafe_allow_html=True)
        np = analysis["nutrition_plan"]

        if np.get("plan_summary"):
            st.markdown(f'<div class="card accent-left" style="font-size:14px;color:var(--text2);line-height:1.7">{np.get("plan_summary","")}</div>', unsafe_allow_html=True)

        # Macros
        cals = np.get("daily_calories", 0)
        protein = np.get("daily_protein_g", 0)
        carbs = np.get("daily_carbs_g", 0)
        fat = np.get("daily_fat_g", 0)
        fiber = np.get("daily_fiber_g", 0)
        water = np.get("daily_water_L", 0)

        if cals:
            st.markdown("**📊 Your Daily Nutrition Targets:**")
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            c1.metric("Calories", f"{cals} kcal")
            c2.metric("Protein", f"{protein}g")
            c3.metric("Carbs", f"{carbs}g")
            c4.metric("Fat", f"{fat}g")
            c5.metric("Fiber", f"{fiber}g")
            c6.metric("Water", f"{water}L")

            if cals > 0 and protein and carbs and fat:
                p_cal = protein * 4
                c_cal = carbs * 4
                f_cal = fat * 9

                st.markdown("**Macro Distribution:**")
                mc1, mc2, mc3 = st.columns(3)
                with mc1:
                    pct = int(p_cal / cals * 100) if cals else 0
                    st.markdown(f'<div class="macro-bar"><div class="macro-label"><span>🥩 Protein</span><span>{pct}%</span></div><div class="progress-bar"><div class="progress-fill" style="width:{pct}%;background:var(--accent)"></div></div></div>', unsafe_allow_html=True)
                with mc2:
                    pct = int(c_cal / cals * 100) if cals else 0
                    st.markdown(f'<div class="macro-bar"><div class="macro-label"><span>🌾 Carbs</span><span>{pct}%</span></div><div class="progress-bar"><div class="progress-fill" style="width:{pct}%;background:var(--blue)"></div></div></div>', unsafe_allow_html=True)
                with mc3:
                    pct = int(f_cal / cals * 100) if cals else 0
                    st.markdown(f'<div class="macro-bar"><div class="macro-label"><span>🫒 Fat</span><span>{pct}%</span></div><div class="progress-bar"><div class="progress-fill" style="width:{pct}%;background:var(--warn)"></div></div></div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("**🍽️ Meal Plan:**")
        c1, c2 = st.columns(2)
        meals = [
            ("🌅 Breakfast", np.get("breakfast", {})),
            ("☀️ Lunch", np.get("lunch", {})),
            ("🌙 Dinner", np.get("dinner", {})),
            ("🍎 Snacks", np.get("snacks", {})),
        ]
        for i, (label, meal) in enumerate(meals):
            if meal:
                with c1 if i % 2 == 0 else c2:
                    meal_text = meal.get("meal", meal) if isinstance(meal, dict) else meal
                    meal_cal = meal.get("calories", "") if isinstance(meal, dict) else ""
                    meal_why = meal.get("why", "") if isinstance(meal, dict) else ""
                    st.markdown(f"""
<div class="meal-box">
<div class="meal-head">{label} {f'— {meal_cal} kcal' if meal_cal else ''}</div>
<div class="meal-body">{meal_text}</div>
{f"<div style='font-size:11px;color:var(--text3);margin-top:4px'>💡 {meal_why}</div>" if meal_why else ''}
</div>
""", unsafe_allow_html=True)

        if np.get("foods_avoid"):
            st.markdown(f'<div class="card danger-left" style="margin-top:10px"><b style="color:var(--danger)">⚠️ Foods & Drinks to Avoid:</b><br><span style="font-size:13px;color:var(--text2)">{np.get("foods_avoid","")}</span></div>', unsafe_allow_html=True)

        if np.get("indian_foods"):
            st.markdown(f'<div class="card accent-left" style="margin-top:8px"><b style="color:var(--accent)">🇮🇳 Beneficial Indian Foods:</b><br><span style="font-size:13px;color:var(--text2)">{np.get("indian_foods","")}</span></div>', unsafe_allow_html=True)

    # Doctor Advice
    if analysis.get("doctor_advice"):
        st.markdown('<div class="section-head">⚕️ When to See a Doctor</div>', unsafe_allow_html=True)
        for adv in analysis["doctor_advice"]:
            urg = adv.get("urgency", "Routine")
            col = "var(--danger)" if urg == "Urgent" else "var(--warn)" if urg == "Soon" else "var(--accent)"
            badgecls = "badge-danger" if urg == "Urgent" else "badge-warn" if urg == "Soon" else "badge-green"
            st.markdown(f"""
<div class="card" style="border-left:3px solid {col}">
<div style="margin-bottom:6px"><b>{adv.get('test','')}</b> <span class="badge {badgecls}">{urg}</span> <span style="font-size:12px;color:var(--text3)">— {adv.get('timeframe','')}</span></div>
<div style="font-size:13px;color:var(--text2)">{adv.get('what_to_tell_doctor','')}</div>
</div>
""", unsafe_allow_html=True)

    # Actions
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        text = f"🧬 Bio Decode AI\nHealth Score: {analysis.get('health_score')}/100\n\n"
        text += "\n".join([f"• {t.get('name')}: {t.get('value')} {t.get('unit')} — {t.get('status')}" for t in analysis.get("tests", [])])
        st.link_button("💬 Share on WhatsApp", f"https://wa.me/?text={requests.utils.quote(text)}", use_container_width=True)
    with c2:
        st.link_button("📧 Share via Email", f"mailto:?subject=My Health Report&body={requests.utils.quote(text)}", use_container_width=True)
    with c3:
        if st.button("🔄 New Analysis", use_container_width=True, key="newanalysis"):
            st.session_state.analysis_result = None
            st.rerun()

    st.markdown('<div class="disclaimer">⚕️ <b>Medical Disclaimer:</b> This AI analysis is for health literacy and educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider before making any health decisions.</div>', unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;color:var(--text3);font-size:11px;padding:16px;line-height:1.9">🧬 <b>Bio Decode AI</b> — AI-Powered Health Intelligence Platform<br>🔒 Zero data storage &nbsp;|&nbsp; 🔒 No tracking &nbsp;|&nbsp; 🔒 HTTPS encrypted<br>© 2025 Bio Decode AI. For educational purposes only.</div>', unsafe_allow_html=True)   
