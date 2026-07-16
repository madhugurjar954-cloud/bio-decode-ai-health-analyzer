import streamlit as st
import json
import os
import base64
import requests
import logging
from datetime import datetime, date, timedelta
from io import BytesIO

logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="Bio Decode AI — Your Personal Health Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
:root{
    --bg:#080e0b;--bg2:#0c1310;--card:#131c18;--card2:#182118;
    --accent:#3dffa0;--accent2:#2dd099;--warn:#ffb84d;--danger:#ff5e5e;
    --blue:#60a5fa;--purple:#a78bfa;--pink:#f472b6;
    --text:#e8f0ec;--text2:#7a9488;--text3:#3d5248;
    --border:#1a2820;--r:16px;--rs:10px
}
*{box-sizing:border-box;margin:0;padding:0}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important;font-family:'Inter',sans-serif!important}
[data-testid="stSidebar"]{background:var(--bg2)!important;border-right:1px solid var(--border)!important}
[data-testid="stSidebar"] *{color:var(--text)!important}
.stTabs [data-baseweb="tab-list"]{background:var(--card)!important;border-radius:14px!important;padding:5px!important;border:1px solid var(--border)!important;gap:3px!important}
.stTabs [data-baseweb="tab-list"] button{color:var(--text2)!important;border-radius:10px!important;font-size:12px!important;font-weight:500!important;padding:8px 14px!important;transition:all .2s!important}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,var(--accent),var(--accent2))!important;color:#060e0a!important;font-weight:700!important}
.stButton>button{background:linear-gradient(135deg,var(--accent),var(--accent2))!important;color:#060e0a!important;border:none!important;border-radius:var(--rs)!important;padding:11px 24px!important;font-weight:700!important;font-size:13px!important;transition:all .25s!important;box-shadow:0 2px 16px rgba(61,255,160,.18)!important;letter-spacing:.01em!important}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 6px 24px rgba(61,255,160,.32)!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input{background:var(--card)!important;color:var(--text)!important;border:1px solid var(--border)!important;border-radius:var(--rs)!important;font-size:13px!important;transition:all .2s!important}
.stTextInput input:focus,.stTextArea textarea:focus,.stNumberInput input:focus{border-color:var(--accent)!important;box-shadow:0 0 0 2px rgba(61,255,160,.08)!important}
.stSelectbox>div>div,.stMultiSelect>div>div{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:var(--rs)!important;color:var(--text)!important}
.stExpander{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:var(--r)!important}
.stExpander summary{color:var(--text)!important;font-weight:600!important;font-size:14px!important}

/* Layout */
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin:8px 0;transition:all .25s}
.card:hover{border-color:rgba(61,255,160,.2);box-shadow:0 4px 24px rgba(0,0,0,.3)}
.card.green{border-left:3px solid var(--accent)}
.card.yellow{border-left:3px solid var(--warn)}
.card.red{border-left:3px solid var(--danger)}
.card.blue{border-left:3px solid var(--blue)}
.card.purple{border-left:3px solid var(--purple)}
.card.pink{border-left:3px solid var(--pink)}

/* Score */
.score-circle{width:120px;height:120px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:0 auto}
.score-big{font-size:2.6em;font-weight:800;line-height:1}

/* Typography */
.hero-title{font-size:2.8em;font-weight:800;background:linear-gradient(135deg,var(--accent) 0%,#00d4ff 50%,var(--purple) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.15;margin-bottom:10px}
.section-head{font-size:17px;font-weight:700;color:var(--text);margin:24px 0 14px;display:flex;align-items:center;gap:9px}
.divider{height:1px;background:var(--border);margin:20px 0}

/* Badges */
.badge{display:inline-flex;align-items:center;padding:3px 11px;border-radius:99px;font-size:11px;font-weight:600;letter-spacing:.03em;margin:2px}
.b-green{background:rgba(61,255,160,.1);border:1px solid rgba(61,255,160,.25);color:var(--accent)}
.b-yellow{background:rgba(255,184,77,.1);border:1px solid rgba(255,184,77,.25);color:var(--warn)}
.b-red{background:rgba(255,94,94,.1);border:1px solid rgba(255,94,94,.25);color:var(--danger)}
.b-blue{background:rgba(96,165,250,.1);border:1px solid rgba(96,165,250,.25);color:var(--blue)}
.b-purple{background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.25);color:var(--purple)}

/* Meal cards */
.meal{background:var(--card2);border:1px solid var(--border);border-radius:var(--rs);padding:14px 16px;margin:5px 0}
.meal-head{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);margin-bottom:7px}
.meal-body{font-size:13px;color:var(--text2);line-height:1.7}
.meal-cal{font-size:11px;color:var(--text3);margin-top:5px}

/* Progress */
.prog-wrap{margin:6px 0}
.prog-label{font-size:12px;color:var(--text2);margin-bottom:4px;display:flex;justify-content:space-between}
.prog-track{height:7px;background:var(--card2);border-radius:99px;overflow:hidden}
.prog-fill{height:100%;border-radius:99px;transition:width .7s ease}

/* Medicine */
.med-item{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--warn);border-radius:var(--rs);padding:14px 16px;margin:6px 0;transition:all .2s}
.med-item:hover{border-color:rgba(255,184,77,.4);box-shadow:0 3px 16px rgba(255,184,77,.08)}
.med-name{font-size:15px;font-weight:700;color:var(--text)}
.med-sub{font-size:12px;color:var(--text2);margin-top:4px;line-height:1.6}

/* Workout */
.wo-bar{display:flex;align-items:flex-end;gap:6px;height:60px;margin:8px 0}
.wo-col{flex:1;border-radius:4px 4px 0 0;min-height:4px;transition:height .5s ease;position:relative}
.wo-col-label{font-size:10px;color:var(--text3);text-align:center;margin-top:4px}

/* Streak */
.streak{background:linear-gradient(135deg,#ff9500,#ff5e00);color:white;padding:6px 16px;border-radius:99px;font-size:13px;font-weight:700;display:inline-block}

/* Empty */
.empty{text-align:center;padding:52px 20px;color:var(--text3)}
.empty-ico{font-size:48px;margin-bottom:14px}
.empty p{font-size:14px;line-height:1.7}

/* Privacy */
.privacy{background:rgba(61,255,160,.04);border:1px solid rgba(61,255,160,.1);border-radius:var(--rs);padding:10px 16px;font-size:12px;color:var(--text2);margin:10px 0}
.disclaimer{background:rgba(255,94,94,.04);border:1px solid rgba(255,94,94,.1);border-radius:var(--rs);padding:14px 18px;font-size:12px;color:var(--text3);line-height:1.8;margin:14px 0}

/* Metric overrides */
[data-testid="stMetricValue"]{color:var(--accent)!important;font-weight:700!important}
[data-testid="stMetricLabel"]{color:var(--text2)!important;font-size:12px!important}
</style>
""", unsafe_allow_html=True)

# ===== SESSION STATE =====
DEFAULTS = {
    "groq_key": "",
    "result": None,
    "history": [],
    "medicines": [],
    "med_logs": {},
    "workouts": {},
    "profile": {"age": 25, "gender": "Not specified", "weight": 65, "conditions": ""},
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

LANG = {
    "English": "Respond entirely in clear, simple English. Explain like talking to a friend, not a doctor.",
    "हिन्दी": "Respond entirely in simple, everyday Hindi using Devanagari script.",
    "English + हिन्दी": "Write in English first, then Hindi translation below. Keep both simple.",
    "ਪੰਜਾਬੀ": "Respond entirely in simple Punjabi using Gurmukhi script.",
    "ગુજરાતી": "Respond entirely in simple Gujarati script.",
    "Español": "Respond entirely in simple, clear Spanish.",
    "العربية": "Respond entirely in simple, clear Arabic.",
}

def si(v):
    try: return int(str(v).strip())
    except: return 0

def today():
    return date.today().isoformat()

def call_api(messages, tokens=7000):
    if not st.session_state.groq_key:
        return False, "API key not configured."
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json={"model": "llama-3.3-70b-versatile", "messages": messages, "max_tokens": tokens, "temperature": 0.3},
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {st.session_state.groq_key}"},
            timeout=60
        )
        if r.status_code == 200:
            return True, r.json()["choices"][0]["message"]["content"]
        return False, r.json().get("error", {}).get("message", "API error")
    except requests.Timeout:
        return False, "Timeout. Please try again."
    except Exception as e:
        return False, str(e)

def analyze(lab_input, lang, mode="text"):
    p = st.session_state.profile
    bmi = round(p["weight"] / ((165/100)**2), 1)
    ctx = f"Age: {p['age']}. Gender: {p['gender']}. Weight: {p['weight']}kg. BMI: {bmi}."
    if p["conditions"]: ctx += f" Conditions: {p['conditions']}."

    prompt = f"""You are Bio Decode AI — a brilliant, warm medical analyst and nutritionist.
{LANG.get(lang, LANG['English'])}

Your job: Make complex lab reports feel simple, clear, and non-scary. Explain like a caring friend who happens to be a doctor.

RULES:
- Use the SIMPLEST possible words. No jargon.
- For each test: explain what it measures, what the result means, WHY it is high/low in body terms
- Be warm and encouraging, never scary
- Give VERY specific food and lifestyle advice
- Calculate exact daily nutrition needs from patient profile

Return ONLY valid JSON, no markdown:
{{"health_score":"0-100","status":"Excellent/Good/Fair/Poor","score_summary":"2-3 warm sentences about overall health","tests":[{{"name":"test name","name_local":"local lang name","value":"number","unit":"unit","status":"Normal/High/Low/Critical/Borderline","normal_range":"range","what_is":"1 sentence — what does this test measure in simple words","your_result":"1-2 sentences — what YOUR result means, why it is this way, in simple friendly words","body_effect":"1 sentence — what is happening in your body because of this","symptoms":["simple symptom"],"eat":["specific food 1","specific food 2","specific food 3"],"avoid":["item 1","item 2"],"action":"See doctor urgently / Monitor closely / No action needed","urgency":"Urgent/Soon/Monitor/Normal"}}],"nutrition":{{"calories":number,"protein_g":number,"carbs_g":number,"fat_g":number,"fiber_g":number,"water_L":number,"summary":"2 sentence warm personalized plan summary","breakfast":{{"food":"specific meal","cal":number,"why":"why good for you"}},"lunch":{{"food":"specific meal","cal":number,"why":"why good for you"}},"dinner":{{"food":"specific meal","cal":number,"why":"why good for you"}},"snacks":{{"food":"healthy options","cal":number}},"avoid":"specific items to avoid","tip":"one special nutrition tip"}},"doctor":[{{"test":"test","urgency":"Urgent/Soon/Routine","say":"exactly what to tell the doctor","when":"timeframe"}}],"tips":["tip 1","tip 2","tip 3"],"good_news":"one warm encouraging sentence"}}
Patient: {ctx}"""

    user = f"Analyze:\n\n{lab_input}" if mode == "text" else "Extract all lab values from image and analyze."
    ok, raw = call_api([{"role": "system", "content": prompt}, {"role": "user", "content": user}])
    if not ok: return False, raw
    try: return True, json.loads(raw.replace("```json","").replace("```","").strip())
    except: return False, "Could not read response. Please try again."

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 🧬 Bio Decode AI")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    lang = st.selectbox("🌐 Language", list(LANG.keys()))

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("**👤 Your Profile**")
    p = st.session_state.profile
    p["age"] = st.number_input("Age", 1, 120, p["age"])
    p["gender"] = st.selectbox("Gender", ["Not specified", "Female", "Male", "Other"])
    p["weight"] = st.number_input("Weight (kg)", 20, 300, p["weight"])
    p["conditions"] = st.text_input("Known conditions", placeholder="e.g. Diabetes, BP", value=p["conditions"])

    bmi = round(p["weight"] / ((165/100)**2), 1)
    bmi_label = "Underweight" if bmi < 18.5 else "Healthy" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
    bmi_col = "var(--accent)" if bmi_label == "Healthy" else "var(--warn)" if bmi_label in ["Overweight","Underweight"] else "var(--danger)"
    st.markdown(f'<div style="font-size:13px;margin-top:6px">BMI: <b style="color:{bmi_col}">{bmi} — {bmi_label}</b></div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    scores = [si(h["score"]) for h in st.session_state.history]
    avg = sum(scores)//len(scores) if scores else 0
    td = today()
    meds_taken = sum(1 for m in st.session_state.medicines if st.session_state.med_logs.get(td, {}).get(m["id"], False))

    st.markdown(f"""
<div style="font-size:12px;color:var(--text2);line-height:2.2">
📊 Analyses: <b style="color:var(--accent)">{len(st.session_state.history)}</b><br>
🏆 Avg Score: <b style="color:var(--accent)">{avg}/100</b><br>
💊 Meds today: <b style="color:var(--warn)">{meds_taken}/{len(st.session_state.medicines)}</b><br>
🏋️ Workouts logged: <b style="color:var(--blue)">{sum(len(v) for v in st.session_state.workouts.values())}</b>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:var(--text3);line-height:2">🔒 Zero data stored<br>🔒 No tracking<br>🔒 HTTPS only<br>🔒 Photos deleted instantly</div>', unsafe_allow_html=True)

# ===== HERO =====
c1, c2 = st.columns([3,1])
with c1:
    st.markdown('<div class="hero-title">Bio Decode AI</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:var(--text2);font-size:15px;font-weight:300;line-height:1.7;max-width:560px">Your personal AI health companion. Understand lab reports in simple language, track medicines, log workouts, and get a nutrition plan built just for you — all in one place.</div>', unsafe_allow_html=True)
with c2:
    col = "var(--accent)" if avg >= 70 else "var(--warn)" if avg >= 40 else "var(--danger)" if avg > 0 else "var(--text3)"
    st.markdown(f"""
<div class="card" style="text-align:center;margin-top:8px">
<div style="font-size:2.2em;font-weight:800;color:{col}">{avg if avg > 0 else "—"}</div>
<div style="font-size:12px;color:var(--text2);margin-bottom:10px">Health Score</div>
<div style="font-size:12px;color:var(--text2)">💊 {meds_taken}/{len(st.session_state.medicines)} today</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ===== TABS =====
t1,t2,t3,t4,t5,t6,t7 = st.tabs(["🔬 Analyze","📷 Upload","💊 Medicines","🏋️ Workouts","📊 History","📈 Compare","ℹ️ Guide"])

# ===== TAB 1: ANALYZE =====
with t1:
    st.markdown('<div class="section-head">🔬 Analyze Your Lab Report</div>', unsafe_allow_html=True)

    lab = st.text_area(
        "Paste your lab values here",
        placeholder="Example:\nHemoglobin: 10.2 g/dL\nTSH: 6.8 mIU/L\nFasting Blood Sugar: 148 mg/dL\nCreatinine: 1.8 mg/dL\nVitamin D: 14 ng/mL",
        height=160, key="lab_val"
    )

    st.markdown("**Try a sample:**")
    sc1,sc2,sc3,sc4,sc5,sc6 = st.columns(6)
    samps = {
        "Thyroid":"TSH: 7.2 mIU/L\nT3: 0.8 ng/mL\nT4: 5.5 µg/dL",
        "Diabetes":"Fasting Blood Sugar: 148 mg/dL\nHbA1c: 7.2%\nPost Prandial: 210 mg/dL",
        "Anemia":"Hemoglobin: 8.5 g/dL\nHematocrit: 28%\nFerritin: 6 ng/mL",
        "Kidney":"Creatinine: 2.1 mg/dL\nBUN: 35 mg/dL\neGFR: 38 mL/min",
        "Liver":"SGPT: 85 U/L\nSGOT: 72 U/L\nBilirubin: 2.4 mg/dL",
        "Full":"Hemoglobin: 9.8\nFasting Sugar: 138\nTSH: 5.9\nCholesterol: 235\nLDL: 155\nHDL: 38\nCreatinine: 1.6\nVit D: 14"
    }
    btns = [sc1,sc2,sc3,sc4,sc5,sc6]
    for i,(label,val) in enumerate(samps.items()):
        if btns[i].button(label, use_container_width=True, key=f"s{i}"):
            st.session_state["lab_val"] = val; st.rerun()

    st.markdown('<div class="privacy">🔒 Your lab values are sent only to AI for analysis and never stored anywhere.</div>', unsafe_allow_html=True)

    if st.button("🔬 Analyze My Report", use_container_width=True, key="btn_ana"):
        v = st.session_state.get("lab_val","")
        if not v or len(v.strip()) < 5:
            st.error("❌ Please enter your lab values first.")
        elif not any(c.isdigit() for c in v):
            st.error("❌ No numbers found. Please add values like: Hemoglobin: 10.2 g/dL")
        else:
            with st.spinner("🧬 Analyzing your report..."):
                ok, res = analyze(v, lang, "text")
                if ok:
                    st.session_state.result = res
                    st.session_state.history.append({"date": datetime.now().strftime("%d %b %Y, %I:%M %p"), "score": res.get("health_score",0), "data": res, "input": v})
                    st.success("✅ Done! Scroll down for your results.")
                    st.rerun()
                else:
                    st.error(f"❌ {res}")

# ===== TAB 2: UPLOAD =====
with t2:
    st.markdown('<div class="section-head">📷 Upload Lab Report Photo</div>', unsafe_allow_html=True)
    st.markdown('<div class="privacy">🔒 Photo is analyzed instantly and permanently deleted. Never stored.</div>', unsafe_allow_html=True)
    up = st.file_uploader("Upload a clear photo of your lab report", type=["jpg","jpeg","png"])
    if up:
        if up.size > 5*1024*1024:
            st.error("❌ Too large. Max 5MB.")
        else:
            st.image(up, use_container_width=True)
            b64 = base64.b64encode(up.getvalue()).decode()
            if st.button("🔬 Analyze This Photo", use_container_width=True, key="btn_ph"):
                with st.spinner("📸 Reading your report..."):
                    ok, res = analyze(b64, lang, "photo")
                    if ok:
                        st.session_state.result = res
                        st.session_state.history.append({"date": datetime.now().strftime("%d %b %Y, %I:%M %p"), "score": res.get("health_score",0), "data": res, "input": "Photo"})
                        st.success("✅ Done!")
                        st.rerun()
                    else:
                        st.error(f"❌ {res}")

# ===== TAB 3: MEDICINES =====
with t3:
    st.markdown('<div class="section-head">💊 Medicine Reminder & Tracker</div>', unsafe_allow_html=True)

    with st.expander("➕ Add New Medicine", expanded=len(st.session_state.medicines)==0):
        c1,c2,c3 = st.columns(3)
        with c1: mn = st.text_input("Medicine Name", placeholder="e.g. Metformin", key="mn")
        with c2: md = st.text_input("Dose", placeholder="e.g. 500mg", key="md")
        with c3: mtype = st.selectbox("Type", ["Tablet","Capsule","Syrup","Drops","Injection","Other"], key="mtp")
        c4,c5 = st.columns(2)
        with c4: mfreq = st.selectbox("How often?", ["Once daily","Twice daily","Three times daily","Weekly","As needed"], key="mfr")
        with c5: mdur = st.text_input("For how long?", placeholder="e.g. 30 days / Ongoing", key="mdu")
        mt = st.multiselect("Remind me at", ["Morning 🌅","Afternoon ☀️","Evening 🌆","Night 🌙","Before Food","After Food","Bedtime 😴"], key="mti")
        mnotes = st.text_input("Doctor's instructions (optional)", placeholder="e.g. Take with food", key="mno")
        if st.button("➕ Add to My Medicines", use_container_width=True, key="addm"):
            if mn:
                st.session_state.medicines.append({"id": datetime.now().isoformat(), "name": mn, "dose": md, "type": mtype, "freq": mfreq, "duration": mdur, "times": mt, "notes": mnotes, "added": today()})
                st.success(f"✅ {mn} added!")
                st.rerun()
            else:
                st.error("❌ Please enter medicine name.")

    if st.session_state.medicines:
        td = today()
        if td not in st.session_state.med_logs:
            st.session_state.med_logs[td] = {}

        total_m = len(st.session_state.medicines)
        taken_m = sum(1 for m in st.session_state.medicines if st.session_state.med_logs[td].get(m["id"], False))
        pct_m = int(taken_m/total_m*100) if total_m else 0

        # Progress
        pct_col = "var(--accent)" if pct_m==100 else "var(--warn)" if pct_m>=50 else "var(--danger)"
        st.markdown(f"""
<div class="card green" style="margin:12px 0">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
<span style="font-weight:700;font-size:15px">Today's Progress</span>
<span style="font-size:22px;font-weight:800;color:{pct_col}">{taken_m}/{total_m}</span>
</div>
<div class="prog-track"><div class="prog-fill" style="width:{pct_m}%;background:{pct_col}"></div></div>
<div style="font-size:12px;color:var(--text2);margin-top:6px">{pct_m}% medicines taken</div>
</div>
""", unsafe_allow_html=True)

        # Time slots
        slot_map = {"Morning 🌅":"🌅","Afternoon ☀️":"☀️","Evening 🌆":"🌆","Night 🌙":"🌙","Before Food":"🍽️","After Food":"🍽️","Bedtime 😴":"😴"}
        for slot in ["Morning 🌅","Afternoon ☀️","Evening 🌆","Night 🌙","Before Food","After Food","Bedtime 😴"]:
            slot_meds = [m for m in st.session_state.medicines if slot in (m.get("times") or [])]
            if slot_meds:
                st.markdown(f"**{slot_map.get(slot,'')} {slot}**")
                for m in slot_meds:
                    mid = m["id"]
                    is_taken = st.session_state.med_logs[td].get(mid, False)
                    c1,c2 = st.columns([4,1])
                    with c1:
                        dot_col = "var(--accent)" if is_taken else "var(--text3)"
                        st.markdown(f'<div class="med-item"><div class="med-name"><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{dot_col};margin-right:8px"></span>{m["name"]} <span style="font-size:12px;color:var(--warn);font-weight:400">{m["dose"]}</span> <span class="badge b-blue">{m["type"]}</span></div><div class="med-sub">{m["freq"]} {f"· {m["notes"]}" if m.get("notes") else ""}</div></div>', unsafe_allow_html=True)
                    with c2:
                        if is_taken:
                            if st.button("✅ Done", key=f"ut_{mid}_{slot}", use_container_width=True):
                                st.session_state.med_logs[td][mid] = False; st.rerun()
                        else:
                            if st.button("Take", key=f"tk_{mid}_{slot}", use_container_width=True):
                                st.session_state.med_logs[td][mid] = True; st.rerun()

        # 7-day chart
        st.markdown('<div class="section-head">📊 Last 7 Days</div>', unsafe_allow_html=True)
        days7 = [(date.today()-timedelta(days=i)) for i in range(6,-1,-1)]
        cols7 = st.columns(7)
        streak = 0
        for d in reversed(days7):
            logs = st.session_state.med_logs.get(d.isoformat(), {})
            tak = sum(1 for m in st.session_state.medicines if logs.get(m["id"],False))
            if tak == total_m and total_m > 0: streak += 1
            else: break

        for i,d in enumerate(days7):
            dstr = d.isoformat()
            logs = st.session_state.med_logs.get(dstr,{})
            tak = sum(1 for m in st.session_state.medicines if logs.get(m["id"],False))
            if not logs or total_m == 0:
                emoji,col,pct_d = "○","var(--text3)","—"
            else:
                pct_d2 = int(tak/total_m*100)
                if pct_d2==100: emoji,col,pct_d="✅","var(--accent)",f"100%"
                elif pct_d2>=50: emoji,col,pct_d="⚠️","var(--warn)",f"{pct_d2}%"
                else: emoji,col,pct_d="❌","var(--danger)",f"{pct_d2}%"
            with cols7[i]:
                st.markdown(f'<div style="text-align:center"><div style="font-size:10px;color:var(--text3)">{d.strftime("%a")}</div><div style="font-size:18px;margin:3px 0">{emoji}</div><div style="font-size:11px;font-weight:700;color:{col}">{pct_d}</div></div>', unsafe_allow_html=True)

        if streak > 0:
            st.markdown(f'<div style="margin:12px 0"><span class="streak">🔥 {streak} day streak!</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-head">💊 All Medicines</div>', unsafe_allow_html=True)
        for i,m in enumerate(st.session_state.medicines):
            c1,c2 = st.columns([5,1])
            with c1:
                times_str = ", ".join(m.get("times") or []) or "Not set"
                st.markdown(f'<div class="med-item"><div class="med-name">{m["name"]} <span style="color:var(--warn);font-weight:400;font-size:13px">{m["dose"]}</span></div><div class="med-sub">⏰ {times_str} &nbsp;·&nbsp; 🔁 {m["freq"]} &nbsp;·&nbsp; 📅 {m.get("duration","Ongoing")}{f" &nbsp;·&nbsp; 📋 {m[\"notes\"]}" if m.get("notes") else ""}</div></div>', unsafe_allow_html=True)
            with c2:
                if st.button("🗑️", key=f"dm_{i}", use_container_width=True):
                    st.session_state.medicines.pop(i); st.rerun()
        if st.button("🗑️ Clear All", use_container_width=True, key="clrm"):
            st.session_state.medicines=[]; st.session_state.med_logs={}; st.rerun()
    else:
        st.markdown('<div class="empty"><div class="empty-ico">💊</div><p>No medicines added yet.<br>Add your first medicine above.</p></div>', unsafe_allow_html=True)

# ===== TAB 4: WORKOUT =====
with t4:
    st.markdown('<div class="section-head">🏋️ Workout Tracker</div>', unsafe_allow_html=True)

    with st.expander("➕ Log a Workout", expanded=True):
        c1,c2,c3 = st.columns(3)
        with c1: wtype = st.selectbox("Exercise", ["Walking 🚶","Running 🏃","Cycling 🚴","Yoga 🧘","Gym/Weights 💪","Swimming 🏊","Dance 💃","HIIT ⚡","Sports 🏸","Stretching","Other"], key="wt")
        with c2: wdur = st.number_input("Duration (mins)", 5, 300, 30, key="wd")
        with c3: wint = st.selectbox("Intensity", ["Light","Moderate","Intense","Very Intense"], key="wi")
        c4,c5 = st.columns(2)
        with c4: wcal = st.number_input("Calories burned (approx)", 0, 2000, 0, key="wc")
        with c5: wmood = st.selectbox("How do you feel?", ["😊 Great","🙂 Good","😐 Okay","😔 Tired","💪 Energized"], key="wm")
        wnotes = st.text_input("Notes", placeholder="e.g. Morning walk in park", key="wn")
        if st.button("➕ Log Workout", use_container_width=True, key="addw"):
            td = today()
            if td not in st.session_state.workouts:
                st.session_state.workouts[td] = []
            st.session_state.workouts[td].append({"type":wtype,"dur":wdur,"intensity":wint,"cal":wcal,"mood":wmood,"notes":wnotes,"time":datetime.now().strftime("%I:%M %p")})
            st.success(f"✅ {wtype} — {wdur} mins logged!")
            st.rerun()

    st.markdown('<div class="section-head">📅 This Week</div>', unsafe_allow_html=True)
    days7w = [(date.today()-timedelta(days=i)) for i in range(6,-1,-1)]
    total_min_w = sum(sum(w["dur"] for w in st.session_state.workouts.get(d.isoformat(),[])) for d in days7w)
    total_cal_w = sum(sum(w["cal"] for w in st.session_state.workouts.get(d.isoformat(),[])) for d in days7w)
    active_days = sum(1 for d in days7w if st.session_state.workouts.get(d.isoformat()))

    c1,c2,c3 = st.columns(3)
    c1.metric("Total Minutes",f"{total_min_w} mins")
    c2.metric("Calories Burned",f"{total_cal_w} kcal")
    c3.metric("Active Days",f"{active_days}/7")

    # Bar chart
    cols7w = st.columns(7)
    for i,d in enumerate(days7w):
        dstr = d.isoformat()
        mins = sum(w["dur"] for w in st.session_state.workouts.get(dstr,[]))
        bar_h = max(4, min(56, mins))
        col = "var(--accent)" if mins>=60 else "var(--blue)" if mins>=30 else "var(--text3)" if mins==0 else "var(--warn)"
        with cols7w[i]:
            st.markdown(f'<div style="text-align:center"><div style="font-size:10px;color:var(--text3);margin-bottom:4px">{d.strftime("%a")}</div><div style="display:flex;align-items:flex-end;justify-content:center;height:56px"><div style="width:20px;height:{bar_h}px;background:{col};border-radius:4px 4px 0 0;opacity:.9"></div></div><div style="font-size:11px;font-weight:700;color:{col};margin-top:3px">{mins}m</div></div>', unsafe_allow_html=True)

    # Streak
    wstreak = 0
    for d in reversed(days7w):
        if st.session_state.workouts.get(d.isoformat()): wstreak+=1
        else: break
    if wstreak > 0:
        st.markdown(f'<div style="margin:12px 0"><span class="streak">🔥 {wstreak} day workout streak!</span></div>', unsafe_allow_html=True)

    # Today's workouts
    td_workouts = st.session_state.workouts.get(today(),[])
    if td_workouts:
        st.markdown('<div class="section-head">Today\'s Workouts</div>', unsafe_allow_html=True)
        for i,w in enumerate(td_workouts):
            c1,c2 = st.columns([5,1])
            with c1:
                st.markdown(f'<div class="card blue"><div style="font-size:14px;font-weight:700">{w["type"]} <span class="badge b-blue">{w["intensity"]}</span></div><div style="font-size:12px;color:var(--text2);margin-top:5px">⏱️ {w["dur"]} mins &nbsp;·&nbsp; 🔥 {w["cal"]} kcal &nbsp;·&nbsp; {w["mood"]} &nbsp;·&nbsp; 🕐 {w["time"]}{f" &nbsp;·&nbsp; {w[\"notes\"]}" if w.get("notes") else ""}</div></div>', unsafe_allow_html=True)
            with c2:
                if st.button("🗑️", key=f"dw_{i}", use_container_width=True):
                    st.session_state.workouts[today()].pop(i); st.rerun()

# ===== TAB 5: HISTORY =====
with t5:
    st.markdown('<div class="section-head">📊 Health History</div>', unsafe_allow_html=True)
    if st.session_state.history:
        scores = [si(h["score"]) for h in st.session_state.history]
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Analyses",len(scores))
        c2.metric("Avg Score",f"{sum(scores)//len(scores)}/100")
        c3.metric("Best",f"{max(scores)}/100")
        c4.metric("Latest",f"{scores[-1]}/100")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        for h in reversed(st.session_state.history):
            sc = si(h["score"])
            icon = "🟢" if sc>=70 else "🟡" if sc>=40 else "🔴"
            label = "Good" if sc>=70 else "Needs Attention" if sc>=40 else "Needs Care"
            with st.expander(f"{icon} {h['date']} — {sc}/100 — {label}"):
                st.markdown(f"**Summary:** {h['data'].get('score_summary','')}")
                for t in h['data'].get('tests',[]):
                    sl = t.get('status','').lower()
                    ico = "🟢" if "normal" in sl else "🔴" if "high" in sl or "critical" in sl else "🟡"
                    st.markdown(f"{ico} **{t.get('name','')}**: {t.get('value','')} {t.get('unit','')} — {t.get('status','')}")
                if h['data'].get('good_news'):
                    st.markdown(f"💚 *{h['data']['good_news']}*")
        if st.button("🗑️ Clear History", use_container_width=True, key="clhist"):
            st.session_state.history=[]; st.session_state.result=None; st.rerun()
    else:
        st.markdown('<div class="empty"><div class="empty-ico">📊</div><p>No analyses yet.<br>Start with your first lab report analysis.</p></div>', unsafe_allow_html=True)

# ===== TAB 6: COMPARE =====
with t6:
    st.markdown('<div class="section-head">📈 Compare Two Reports</div>', unsafe_allow_html=True)
    if len(st.session_state.history)>=2:
        c1,c2 = st.columns(2)
        with c1: i1 = st.selectbox("First Report", range(len(st.session_state.history)), format_func=lambda i: f"{st.session_state.history[i]['date']} ({st.session_state.history[i]['score']}/100)", key="cp1")
        with c2: i2 = st.selectbox("Second Report", range(len(st.session_state.history)), format_func=lambda i: f"{st.session_state.history[i]['date']} ({st.session_state.history[i]['score']}/100)", key="cp2")
        if i1!=i2:
            r1,r2 = st.session_state.history[i1], st.session_state.history[i2]
            s1,s2 = si(r1["score"]), si(r2["score"])
            c1,c2,c3 = st.columns(3)
            c1.metric("Report 1",f"{s1}/100")
            c2.metric("Report 2",f"{s2}/100",delta=s2-s1)
            c3.metric("Trend","📈 Improving" if s2>s1 else "📉 Declining" if s2<s1 else "➡️ Same")
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            t1d = {t['name']:t for t in r1['data'].get('tests',[])}
            t2d = {t['name']:t for t in r2['data'].get('tests',[])}
            for name in set(t1d.keys())|set(t2d.keys()):
                a,b = t1d.get(name,{}), t2d.get(name,{})
                c1,c2,c3 = st.columns(3)
                c1.markdown(f"**{name}**")
                c2.markdown(f"{a.get('value','—')} {a.get('unit','')} — {a.get('status','N/A')}")
                c3.markdown(f"{b.get('value','—')} {b.get('unit','')} — {b.get('status','N/A')}")
        else:
            st.warning("Please select two different reports.")
    elif len(st.session_state.history)==1:
        st.info("Complete at least 2 analyses to compare.")
    else:
        st.markdown('<div class="empty"><div class="empty-ico">📈</div><p>No history yet.</p></div>', unsafe_allow_html=True)

# ===== TAB 7: GUIDE =====
with t7:
    st.markdown('<div class="section-head">ℹ️ How to Use Bio Decode AI</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""
**🔬 Lab Analysis**
1. Set your profile in sidebar (age, weight, gender)
2. Paste lab values or upload photo
3. Click Analyze
4. Get simple, friendly explanation of every test

**💊 Medicine Reminder**
1. Add your medicines with timing
2. Mark them as taken each day
3. Track your 7-day adherence
4. Build a streak 🔥
        """)
    with c2:
        st.markdown("""
**🏋️ Workout Tracker**
1. Log each workout — type, duration, intensity
2. See your weekly bar chart
3. Track calories and streaks

**📊 History & Compare**
- All analyses saved in your session
- Compare any two reports side by side
- Track your health score over time

**🌐 7 Languages**
English · Hindi · Punjabi · Gujarati · Spanish · Arabic
        """)
    st.markdown("""
**🔮 Coming Soon**
Doctor & lab integrations · Health coaching · Team plans · API access
        """)
    st.markdown('<div class="disclaimer">⚕️ <b>Medical Disclaimer:</b> Bio Decode AI is for health literacy and educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider before making health decisions.</div>', unsafe_allow_html=True)

# ===== RESULTS =====
if st.session_state.result:
    res = st.session_state.result
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-head">📊 Your Health Analysis</div>', unsafe_allow_html=True)

    # Score
    sc = si(res.get("health_score",0))
    col = "#3dffa0" if sc>=70 else "#ffb84d" if sc>=40 else "#ff5e5e"
    border = f"rgba({('61,255,160' if sc>=70 else '255,184,77' if sc>=40 else '255,94,94')},.25)"

    c1,c2 = st.columns([1,3])
    with c1:
        st.markdown(f'<div class="score-circle" style="background:{col}12;border:3px solid {col};margin-top:8px"><div class="score-big" style="color:{col}">{sc}</div><div style="font-size:11px;color:{col};opacity:.8">/100</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
<div class="card" style="border-color:{border};margin-top:8px">
<div style="font-size:18px;font-weight:700;color:{col};margin-bottom:8px">{'🟢' if sc>=70 else '🟡' if sc>=40 else '🔴'} {res.get('status','')}</div>
<div style="font-size:14px;color:var(--text2);line-height:1.75">{res.get('score_summary','')}</div>
{f"<div style='margin-top:12px;font-size:13px;color:var(--accent);font-style:italic'>💚 {res.get('good_news','')}</div>" if res.get('good_news') else ''}
</div>
""", unsafe_allow_html=True)

    # Tips
    if res.get("tips"):
        st.markdown('<div class="section-head">💡 Personalized Tips</div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        for i,tip in enumerate(res["tips"]):
            with c1 if i%2==0 else c2:
                st.markdown(f'<div class="card green" style="padding:12px 16px;font-size:13px;color:var(--text2)">✨ {tip}</div>', unsafe_allow_html=True)

    # Tests
    if res.get("tests"):
        st.markdown('<div class="section-head">🔬 Your Test Results — In Simple Words</div>', unsafe_allow_html=True)
        for test in res["tests"]:
            sl = test.get("status","").lower()
            urg = test.get("urgency","Normal")
            if "normal" in sl: icon,cls,vcol,bc = "✅","green","var(--accent)","b-green"
            elif "critical" in sl or urg=="Urgent": icon,cls,vcol,bc = "🚨","red","var(--danger)","b-red"
            elif "high" in sl: icon,cls,vcol,bc = "⚠️","red","var(--danger)","b-red"
            elif "low" in sl or "borderline" in sl: icon,cls,vcol,bc = "📍","yellow","var(--warn)","b-yellow"
            else: icon,cls,vcol,bc = "❓","green","var(--text2)","b-green"

            with st.expander(f"{icon} {test.get('name','')} — {test.get('value','')} {test.get('unit','')} — {test.get('status','')}", expanded=False):
                c1,c2 = st.columns([1,2])
                with c1:
                    st.markdown(f"""
<div class="card {cls}" style="text-align:center;padding:16px">
<div style="font-size:12px;color:var(--text2);margin-bottom:6px">{test.get('name','')}</div>
{f"<div style='font-size:11px;color:var(--text3);margin-bottom:4px'>{test.get('name_local','')}</div>" if test.get('name_local') else ''}
<div style="font-size:2.4em;font-weight:800;color:{vcol};line-height:1">{test.get('value','')}</div>
<div style="font-size:13px;color:var(--text2)">{test.get('unit','')}</div>
<div style="font-size:11px;color:var(--text3);margin-top:5px">Normal: {test.get('normal_range','')}</div>
<div style="margin-top:10px"><span class="badge {bc}">{test.get('status','')}</span></div>
{f"<div style='margin-top:5px'><span class='badge b-red'>{urg}</span></div>" if urg in ['Urgent','Soon'] else ''}
</div>
""", unsafe_allow_html=True)
                with c2:
                    if test.get("what_is"):
                        st.markdown(f'<div style="font-size:12px;color:var(--text3);margin-bottom:6px">📌 {test.get("what_is","")}</div>', unsafe_allow_html=True)
                    if test.get("your_result"):
                        st.markdown(f'<div style="font-size:14px;color:var(--text);line-height:1.75;background:var(--card2);padding:14px;border-radius:12px">{test.get("your_result","")}</div>', unsafe_allow_html=True)
                    if test.get("body_effect"):
                        st.markdown(f'<div style="margin-top:8px;font-size:13px;color:var(--text2);font-style:italic">🫀 {test.get("body_effect","")}</div>', unsafe_allow_html=True)
                    if test.get("action"):
                        st.markdown(f'<div style="margin-top:8px;font-size:13px"><b>Action:</b> {test.get("action","")}</div>', unsafe_allow_html=True)

                if test.get("symptoms"):
                    st.markdown("**Possible Symptoms:**")
                    cols = st.columns(min(3,len(test["symptoms"])))
                    for j,s in enumerate(test["symptoms"]):
                        cols[j%len(cols)].markdown(f"• {s}")

                if test.get("eat") or test.get("avoid"):
                    c1,c2 = st.columns(2)
                    with c1:
                        if test.get("eat"):
                            st.markdown("✅ **Good foods:**")
                            for f in test["eat"]: st.markdown(f"• {f}")
                    with c2:
                        if test.get("avoid"):
                            st.markdown("❌ **Avoid:**")
                            for f in test["avoid"]: st.markdown(f"• {f}")

    # Nutrition
    if res.get("nutrition"):
        st.markdown('<div class="section-head">🥗 Your Personalized Nutrition Plan</div>', unsafe_allow_html=True)
        np = res["nutrition"]

        if np.get("summary"):
            st.markdown(f'<div class="card green" style="font-size:14px;color:var(--text2);line-height:1.75">{np["summary"]}</div>', unsafe_allow_html=True)

        # Macro targets
        cals = np.get("calories",0)
        if cals:
            st.markdown("**📊 Your Daily Nutrition Targets:**")
            c1,c2,c3,c4,c5,c6 = st.columns(6)
            c1.metric("Calories",f"{cals}")
            c2.metric("Protein",f'{np.get("protein_g",0)}g')
            c3.metric("Carbs",f'{np.get("carbs_g",0)}g')
            c4.metric("Fat",f'{np.get("fat_g",0)}g')
            c5.metric("Fiber",f'{np.get("fiber_g",0)}g')
            c6.metric("Water",f'{np.get("water_L",0)}L')

            # Macro bars
            prot_g = np.get("protein_g",0)
            carb_g = np.get("carbs_g",0)
            fat_g = np.get("fat_g",0)
            if cals and prot_g and carb_g and fat_g:
                p_pct = int(prot_g*4/cals*100)
                c_pct = int(carb_g*4/cals*100)
                f_pct = int(fat_g*9/cals*100)
                c1,c2,c3 = st.columns(3)
                with c1:
                    st.markdown(f'<div class="prog-wrap"><div class="prog-label"><span>🥩 Protein</span><span>{p_pct}%</span></div><div class="prog-track"><div class="prog-fill" style="width:{p_pct}%;background:var(--accent)"></div></div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="prog-wrap"><div class="prog-label"><span>🌾 Carbs</span><span>{c_pct}%</span></div><div class="prog-track"><div class="prog-fill" style="width:{c_pct}%;background:var(--blue)"></div></div></div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="prog-wrap"><div class="prog-label"><span>🫒 Fat</span><span>{f_pct}%</span></div><div class="prog-track"><div class="prog-fill" style="width:{f_pct}%;background:var(--warn)"></div></div></div>', unsafe_allow_html=True)

        # Meals
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        meals = [("🌅 Breakfast","breakfast"),("☀️ Lunch","lunch"),("🌙 Dinner","dinner"),("🍎 Snacks","snacks")]
        for i,(label,key) in enumerate(meals):
            meal = np.get(key,{})
            if meal:
                food = meal.get("food",meal) if isinstance(meal,dict) else meal
                cal = meal.get("cal","") if isinstance(meal,dict) else ""
                why = meal.get("why","") if isinstance(meal,dict) else ""
                with c1 if i%2==0 else c2:
                    st.markdown(f'<div class="meal"><div class="meal-head">{label}{f" — {cal} kcal" if cal else ""}</div><div class="meal-body">{food}</div>{f"<div class=\"meal-cal\">💡 {why}</div>" if why else ""}</div>', unsafe_allow_html=True)

        if np.get("avoid"):
            st.markdown(f'<div class="card red" style="margin-top:10px"><b style="color:var(--danger)">⚠️ Avoid:</b> <span style="font-size:13px;color:var(--text2)">{np["avoid"]}</span></div>', unsafe_allow_html=True)
        if np.get("tip"):
            st.markdown(f'<div class="card green" style="margin-top:8px"><b style="color:var(--accent)">💡 Special Tip:</b> <span style="font-size:13px;color:var(--text2)">{np["tip"]}</span></div>', unsafe_allow_html=True)

    # Doctor
    if res.get("doctor"):
        st.markdown('<div class="section-head">⚕️ When to See a Doctor</div>', unsafe_allow_html=True)
        for adv in res["doctor"]:
            urg = adv.get("urgency","Routine")
            col = "var(--danger)" if urg=="Urgent" else "var(--warn)" if urg=="Soon" else "var(--accent)"
            bc = "b-red" if urg=="Urgent" else "b-yellow" if urg=="Soon" else "b-green"
            st.markdown(f'<div class="card" style="border-left:3px solid {col}"><div style="margin-bottom:6px"><b>{adv.get("test","")}</b> <span class="badge {bc}">{urg}</span> <span style="font-size:12px;color:var(--text3)">— {adv.get("when","")}</span></div><div style="font-size:13px;color:var(--text2)">{adv.get("say","")}</div></div>', unsafe_allow_html=True)

    # Share
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    text = f"🧬 Bio Decode AI\nHealth Score: {res.get('health_score')}/100\n\n"
    text += "\n".join([f"• {t.get('name')}: {t.get('value')} {t.get('unit')} — {t.get('status')}" for t in res.get("tests",[])])
    c1,c2,c3 = st.columns(3)
    with c1: st.link_button("💬 WhatsApp", f"https://wa.me/?text={requests.utils.quote(text)}", use_container_width=True)
    with c2: st.link_button("📧 Email", f"mailto:?subject=My Health Report&body={requests.utils.quote(text)}", use_container_width=True)
    with c3:
        if st.button("🔄 New Analysis", use_container_width=True, key="newana"):
            st.session_state.result=None; st.rerun()

    st.markdown('<div class="disclaimer">⚕️ <b>Medical Disclaimer:</b> This AI analysis is for educational purposes only. NOT a substitute for professional medical advice. Always consult a qualified healthcare provider.</div>', unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;color:var(--text3);font-size:11px;padding:16px;line-height:2">🧬 <b>Bio Decode AI</b> — Personal Health Intelligence<br>🔒 Zero data storage &nbsp;·&nbsp; 🔒 No tracking &nbsp;·&nbsp; 🔒 HTTPS encrypted<br>© 2025 Bio Decode AI. For educational purposes only.</div>', unsafe_allow_html=True)
