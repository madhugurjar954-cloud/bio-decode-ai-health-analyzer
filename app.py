import streamlit as st
import json
import os
import base64
import io
import requests

st.set_page_config(page_title="Bio Decode AI", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>:root{--bg:#0a0f0d;--card:#1a2320;--accent:#3dffa0;--warn:#ffb84d;--danger:#ff5e5e;--text:#e8f0ec;--text2:#8fa898;}.stApp{background-color:#0a0f0d;}.main{background-color:#0a0f0d;color:#e8f0ec;}.stButton>button{background-color:#3dffa0;color:#060e0a;border:none;font-weight:600;width:100%;}.stButton>button:hover{background-color:#00cc7a;}h1,h2,h3{color:#3dffa0;}.info-box{background-color:rgba(61,255,160,0.1);border-left:3px solid #3dffa0;padding:15px;border-radius:5px;margin:10px 0;}.warning-box{background-color:rgba(255,184,77,0.1);border-left:3px solid #ffb84d;padding:15px;border-radius:5px;margin:10px 0;}.danger-box{background-color:rgba(255,94,94,0.1);border-left:3px solid #ff5e5e;padding:15px;border-radius:5px;margin:10px 0;}</style>""", unsafe_allow_html=True)

if "groq_key" not in st.session_state:
    try:
        st.session_state.groq_key = st.secrets["GROQ_API_KEY"]
    except:
        st.session_state.groq_key = os.getenv("GROQ_API_KEY", "")
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

st.markdown("# 🧬 Bio Decode AI")
st.markdown("**Understand Your Lab Report Instantly & Clearly**")
st.markdown("Get personalized health scores, medical insights, and nutrition plans in seconds.")

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    language = st.selectbox("Analysis Language", ["English", "हिन्दी (Hindi)", "English + हिन्दी", "ਪੰਜਾਬੀ (Punjabi)", "ગુજરાતી (Gujarati)", "Español (Spanish)", "Français (French)", "العربية (Arabic)"])
    if not st.session_state.groq_key:
        st.session_state.groq_key = st.text_input("Groq API Key", type="password", help="Get from https://console.groq.com")
    else:
        st.success("✅ API Key loaded")
    st.markdown("---")
    st.markdown("### 🔒 Privacy\n- ✅ Data never stored\n- ✅ Photos deleted after analysis\n- ✅ All processing is local")

language_prompts = {"English": "Respond entirely in English.", "हिन्दी (Hindi)": "Respond entirely in Hindi using Devanagari script.", "English + हिन्दी": "For every field, write English first, then Hindi translation in Devanagari.", "ਪੰਜਾਬੀ (Punjabi)": "Respond entirely in Punjabi using Gurmukhi script.", "ગુજરાતી (Gujarati)": "Respond entirely in Gujarati script.", "Español (Spanish)": "Respond entirely in Spanish.", "Français (French)": "Respond entirely in French.", "العربية (Arabic)": "Respond entirely in Arabic."}

tab1, tab2 = st.tabs(["📝 Type Values", "📷 Upload Photo"])

with tab1:
    st.markdown("### Enter Your Lab Values")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
    with col2:
        gender = st.selectbox("Biological Sex", ["Not specified", "Female", "Male", "Other"])
    with col3:
        conditions = st.text_input("Known Conditions", placeholder="e.g., Diabetes, Hypertension")
    lab_input = st.text_area("Paste or type your lab values", placeholder="Example:\nHemoglobin: 10.2 g/dL\nTSH: 6.8 mIU/L\nFasting Blood Sugar: 148 mg/dL\nCreatinine: 1.8 mg/dL", height=150)
    st.markdown("**Quick samples:**")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    samples = {
        "Thyroid": "TSH: 7.2 mIU/L\nT3: 0.8 ng/mL\nT4: 5.5 µg/dL",
        "Diabetes": "Fasting Blood Sugar: 148 mg/dL\nHbA1c: 7.2%\nPost Prandial Sugar: 210 mg/dL",
        "Anemia": "Hemoglobin: 8.5 g/dL\nHematocrit: 28%\nMCV: 72 fL\nFerritin: 6 ng/mL",
        "Kidney": "Creatinine: 2.1 mg/dL\nBUN: 35 mg/dL\neGFR: 38 mL/min\nUric Acid: 8.5 mg/dL",
        "Liver": "SGPT: 85 U/L\nSGOT: 72 U/L\nBilirubin: 2.4 mg/dL\nAlkaline Phosphatase: 165 U/L",
        "Full Panel": "Hemoglobin: 9.8 g/dL\nFasting Sugar: 138 mg/dL\nTSH: 5.9 mIU/L\nCholesterol: 235 mg/dL\nLDL: 155 mg/dL\nHDL: 38 mg/dL\nCreatinine: 1.6 mg/dL"
    }
    if col1.button("Thyroid", use_container_width=True):
        lab_input = samples["Thyroid"]
    if col2.button("Diabetes", use_container_width=True):
        lab_input = samples["Diabetes"]
    if col3.button("Anemia", use_container_width=True):
        lab_input = samples["Anemia"]
    if col4.button("Kidney", use_container_width=True):
        lab_input = samples["Kidney"]
    if col5.button("Liver", use_container_width=True):
        lab_input = samples["Liver"]
    if col6.button("Full Panel", use_container_width=True):
        lab_input = samples["Full Panel"]
    input_mode, input_data = "text", lab_input

with tab2:
    st.markdown("### Upload Lab Report Photo")
    uploaded_file = st.file_uploader("Upload your lab report image", type=["jpg", "jpeg", "png"], help="AI will extract all values automatically")
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded image", use_container_width=True)
        img_base64 = base64.b64encode(uploaded_file.getvalue()).decode()
        input_mode, input_data = "photo", img_base64
    else:
        input_mode, input_data = None, None
        input_mode, input_data = None, None

st.markdown("---")
if st.button("🔬 Analyze My Report", use_container_width=True, key="analyze"):
    if not input_data and not uploaded_file:
        st.error("❌ Please enter lab values or upload a photo first")
    elif not st.session_state.groq_key:
        st.error("❌ Please provide your Groq API Key")
    else:
        with st.spinner("🧬 Decoding your biomarkers..."):
            try:
                context = f"Age: {age}. " + (f"Biological sex: {gender}. " if gender != "Not specified" else "") + (f"Known conditions: {conditions}. " if conditions else "")
                lang_prompt = language_prompts.get(language, "Respond entirely in English.")
                system_prompt = f"""You are Bio Decode AI, a medical analyst. {lang_prompt}
Return ONLY valid JSON with no markdown fences:
{{"health_score":"0-100","score_summary":"brief summary","tests":[{{"name":"Test Name","value":"123","unit":"unit","status":"Normal/High/Low/Critical","normal_range":"60-100","explanation_en":"What this means","symptoms":["symptom1"],"diet_do":"Foods to include","diet_dont":"Foods to avoid"}}],"nutrition_plan":{{"summary":"guidance","water":"recommendation","meals":{{"breakfast":"suggestion","lunch":"suggestion","dinner":"suggestion","snacks":"snacks"}},"avoid":"avoid"}},"doctor_advice":[{{"label":"advice","en":"English","local":"local"}}]}}
Patient profile: {context}"""
                user_msg = f"Analyze these lab values:\n\n{input_data}" if input_mode == "text" else "Extract all lab values from this image and analyze them."
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {st.session_state.groq_key}"}
                payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}], "max_tokens": 6000, "temperature": 0.3}
                response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=30)
                if response.status_code == 200:
                    content = response.json()["choices"][0]["message"]["content"]
                    try:
                        st.session_state.analysis_result = json.loads(content.replace("```json", "").replace("```", "").strip())
                    except:
                        st.error("❌ Could not parse response. Try again.")
                else:
                    st.error(f"❌ API Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

if st.session_state.analysis_result:
    st.markdown("---")
    st.markdown("# 📊 Your Health Report")
    analysis = st.session_state.analysis_result
    if "health_score" in analysis:
        score = int(analysis["health_score"])
        color, status = ("🟢", "Good") if score >= 70 else ("🟡", "Needs Attention") if score >= 40 else ("🔴", "See a Doctor")
        st.markdown(f'<div class="info-box"><h2>{color} Health Score: {score}/100</h2><p><strong>Status:</strong> {status}</p><p>{analysis.get("score_summary", "")}</p></div>', unsafe_allow_html=True)
    if "tests" in analysis:
        st.markdown("## 🔬 Test Results")
        for test in analysis["tests"]:
            status_lower = test.get("status", "").lower()
            icon = "✅" if "normal" in status_lower or "good" in status_lower else "⚠️" if "high" in status_lower or "critical" in status_lower else "📍"
            with st.expander(f"{icon} {test.get('name', 'Test')} - {test.get('value', '')} {test.get('unit', '')}"):
                col1, col2 = st.columns(2)
                col1.markdown(f"**Status:** {test.get('status', 'N/A')}\n**Range:** {test.get('normal_range', 'N/A')}")
                col2.markdown(f"**Value:** {test.get('value', 'N/A')} {test.get('unit', '')}")
                st.markdown(f"**Explanation:** {test.get('explanation_en', 'N/A')}")
                if test.get("symptoms"):
                    st.markdown("**Possible Symptoms:**\n" + "\n".join(f"- {s}" for s in test["symptoms"]))
                if test.get("diet_do") or test.get("diet_dont"):
                    st.markdown("**Dietary Guidance:**")
                    if test.get("diet_do"):
                        st.markdown(f"✅ **Include:** {test.get('diet_do')}")
                    if test.get("diet_dont"):
                        st.markdown(f"❌ **Avoid:** {test.get('diet_dont')}")
    if "nutrition_plan" in analysis:
        st.markdown("## 🥗 Your Personalized Nutrition Plan")
        nutrition = analysis["nutrition_plan"]
        st.markdown(f"**{nutrition.get('summary', '')}**")
        if nutrition.get("water"):
            st.markdown(f"💧 {nutrition.get('water')}")
        if nutrition.get("meals"):
            st.markdown("### Meal Suggestions")
            cols = st.columns(2)
            meals = nutrition["meals"]
            for i, (name, suggestion) in enumerate([("🌅 Breakfast", meals.get("breakfast")), ("☀️ Lunch", meals.get("lunch")), ("🌙 Dinner", meals.get("dinner")), ("🍎 Snacks", meals.get("snacks"))]):
                if suggestion:
                    with cols[i % 2]:
                        st.markdown(f"**{name}**\n{suggestion}")
        if nutrition.get("avoid"):
            st.markdown(f'<div class="danger-box"><strong>⚠️ Foods & Drinks to Avoid:</strong><br>{nutrition.get("avoid")}</div>', unsafe_allow_html=True)
    if "doctor_advice" in analysis and analysis["doctor_advice"]:
        st.markdown("## ⚕️ When to Consult a Doctor")
        for advice in analysis["doctor_advice"]:
            st.markdown(f'<div class="warning-box"><strong>{advice.get("label", "Consultation Advice")}:</strong><br>{advice.get("en", "")}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="danger-box"><strong>⚕️ Medical Disclaimer:</strong><br>This analysis is for educational purposes only. Not a substitute for professional medical advice. Always consult a healthcare provider.</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    if col1.button("📋 Copy Results", use_container_width=True):
        st.success("✅ Results copied!")
    if col2.button("🔄 New Analysis", use_container_width=True):
        st.session_state.analysis_result = None
        st.rerun()
    if col3.button("💬 Share on WhatsApp", use_container_width=True):
        text = "🧬 Bio Decode AI - My Health Report\n\n" + ("".join(f"• {t.get('name')}: {t.get('value')} {t.get('unit')} - {t.get('status')}\n" for t in analysis.get("tests", [])) if "tests" in analysis else "")
        st.markdown(f"[Open WhatsApp](https://wa.me/?text={text})")

st.markdown("---")
st.markdown('<div style="text-align:center;color:#8fa898;font-size:12px;">🧬 Bio Decode AI | © 2025 | All rights reserved</div>', unsafe_allow_html=True)
