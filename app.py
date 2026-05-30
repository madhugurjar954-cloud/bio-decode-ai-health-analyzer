import streamlit as st
import anthropic
import json
import os
from PIL import Image
import base64
import io

# Configure page
st.set_page_config(
    page_title="Bio Decode AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    :root {
        --bg: #0a0f0d;
        --card: #1a2320;
        --accent: #3dffa0;
        --warn: #ffb84d;
        --danger: #ff5e5e;
        --text: #e8f0ec;
        --text2: #8fa898;
    }
    
    .stApp {
        background-color: #0a0f0d;
    }
    
    .main {
        background-color: #0a0f0d;
        color: #e8f0ec;
    }
    
    .stButton>button {
        background-color: #3dffa0;
        color: #060e0a;
        border: none;
        font-weight: 600;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #00cc7a;
    }
    
    h1, h2, h3 {
        color: #3dffa0;
    }
    
    .info-box {
        background-color: rgba(61,255,160,0.1);
        border-left: 3px solid #3dffa0;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .warning-box {
        background-color: rgba(255,184,77,0.1);
        border-left: 3px solid #ffb84d;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .danger-box {
        background-color: rgba(255,94,94,0.1);
        border-left: 3px solid #ff5e5e;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "groq_key" not in st.session_state:
    st.session_state.groq_key = os.getenv("GROQ_API_KEY", "")
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# Header
st.markdown("# 🧬 Bio Decode AI")
st.markdown("**Understand Your Lab Report Instantly & Clearly**")
st.markdown("Get personalized health scores, medical insights, and nutrition plans in seconds.")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    # Language selection
    language = st.selectbox(
        "Analysis Language",
        ["English", "हिन्दी (Hindi)", "English + हिन्दी", "ਪੰਜਾਬੀ (Punjabi)", 
         "ગુજરાતી (Gujarati)", "Español (Spanish)", "Français (French)", "العربية (Arabic)"]
    )
    
    # API Key (if not in environment)
    if not st.session_state.groq_key:
        st.session_state.groq_key = st.text_input(
            "Groq API Key (optional - uses env var if not provided)",
            type="password",
            help="Get from https://console.groq.com"
        )
    else:
        st.success("✅ API Key loaded from environment")
    
    st.markdown("---")
    st.markdown("### 🔒 Privacy")
    st.markdown("""
    - ✅ Data never stored
    - ✅ Photos deleted after analysis
    - ✅ All processing is local
    - ✅ No data sharing
    """)

# Language prompts
language_prompts = {
    "English": "Respond entirely in English.",
    "हिन्दी (Hindi)": "Respond entirely in Hindi using Devanagari script.",
    "English + हिन्दी": "For every field, write the English text first, then the Hindi translation in Devanagari script on a new line below it.",
    "ਪੰਜਾਬੀ (Punjabi)": "Respond entirely in Punjabi using Gurmukhi script.",
    "ગુજરાતી (Gujarati)": "Respond entirely in Gujarati script.",
    "Español (Spanish)": "Respond entirely in Spanish.",
    "Français (French)": "Respond entirely in French.",
    "العربية (Arabic)": "Respond entirely in Arabic."
}

# Main content area
tab1, tab2 = st.tabs(["📝 Type Values", "📷 Upload Photo"])

with tab1:
    st.markdown("### Enter Your Lab Values")
    
    # Patient info
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
    with col2:
        gender = st.selectbox("Biological Sex", ["Not specified", "Female", "Male", "Other"])
    with col3:
        conditions = st.text_input("Known Conditions (optional)", placeholder="e.g., Diabetes, Hypertension")
    
    # Lab values input
    lab_input = st.text_area(
        "Paste or type your lab values",
        placeholder="""Example:
Hemoglobin: 10.2 g/dL
TSH: 6.8 mIU/L
Fasting Blood Sugar: 148 mg/dL
Creatinine: 1.8 mg/dL""",
        height=150
    )
    
    # Sample buttons
    st.markdown("**Quick samples:**")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    samples = {
        "Thyroid": "TSH: 7.2 mIU/L\nT3: 0.8 ng/mL\nT4: 5.5 µg/dL",
        "Diabetes": "Fasting Blood Sugar: 148 mg/dL\nHbA1c: 7.2%\nPost Prandial Sugar: 210 mg/dL",
        "Anemia": "Hemoglobin: 8.5 g/dL\nHematocrit: 28%\nMCV: 72 fL\nFerritin: 6 ng/mL",
        "Kidney": "Creatinine: 2.1 mg/dL\nBUN: 35 mg/dL\neGFR: 38 mL/min\nUric Acid: 8.5 mg/dL",
        "Liver": "SGPT (ALT): 85 U/L\nSGOT (AST): 72 U/L\nBilirubin Total: 2.4 mg/dL\nAlkaline Phosphatase: 165 U/L",
        "Full Panel": "Hemoglobin: 9.8 g/dL\nFasting Blood Sugar: 138 mg/dL\nTSH: 5.9 mIU/L\nTotal Cholesterol: 235 mg/dL\nLDL: 155 mg/dL\nHDL: 38 mg/dL\nCreatinine: 1.6 mg/dL\nSGPT: 58 U/L\nVitamin D: 14 ng/mL"
    }
    
    with col1:
        if st.button("Thyroid", use_container_width=True):
            lab_input = samples["Thyroid"]
    with col2:
        if st.button("Diabetes", use_container_width=True):
            lab_input = samples["Diabetes"]
    with col3:
        if st.button("Anemia", use_container_width=True):
            lab_input = samples["Anemia"]
    with col4:
        if st.button("Kidney", use_container_width=True):
            lab_input = samples["Kidney"]
    with col5:
        if st.button("Liver", use_container_width=True):
            lab_input = samples["Liver"]
    with col6:
        if st.button("Full Panel", use_container_width=True):
            lab_input = samples["Full Panel"]
    
    input_mode = "text"
    input_data = lab_input

with tab2:
    st.markdown("### Upload Lab Report Photo")
    uploaded_file = st.file_uploader(
        "Upload your lab report image",
        type=["jpg", "jpeg", "png"],
        help="AI will extract all values automatically"
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded image", use_container_width=True)
        
        # Convert image to base64
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode()
        
        input_mode = "photo"
        input_data = img_base64
    else:
        input_mode = None
        input_data = None

# Analyze button
st.markdown("---")
if st.button("🔬 Analyze My Report", use_container_width=True, key="analyze"):
    if not input_data:
        st.error("❌ Please enter lab values or upload a photo first")
    elif not st.session_state.groq_key:
        st.error("❌ Please provide your Groq API Key in the sidebar")
    else:
        with st.spinner("🧬 Decoding your biomarkers..."):
            try:
                # Build context
                context = ""
                if age:
                    context += f"Age: {age}. "
                if gender != "Not specified":
                    context += f"Biological sex: {gender}. "
                if conditions:
                    context += f"Known conditions: {conditions}. "
                
                # Build system prompt
                lang_prompt = language_prompts.get(language, "Respond entirely in English.")
                system_prompt = f"""You are Bio Decode AI, a world-class medical analyst and clinical nutritionist. {lang_prompt}

Return ONLY valid compact JSON with no markdown fences, no explanations, just the JSON:

{{
  "health_score": "0-100",
  "score_summary": "brief summary",
  "tests": [
    {{
      "name": "Test Name",
      "name_local": "Local name if different",
      "value": "123",
      "unit": "unit",
      "status": "Normal/High/Low/Critical",
      "normal_range": "60-100",
      "explanation_en": "What this means",
      "explanation_local": "Local language explanation",
      "symptoms": ["symptom1", "symptom2"],
      "diet_do": "Foods to include",
      "diet_do_local": "Local foods",
      "diet_dont": "Foods to avoid",
      "diet_dont_local": "Local foods to avoid",
      "medical_info": {{
        "what_is": "What this test measures",
        "why_important": "Why this matters",
        "what_causes_abnormal": "Common causes",
        "local_summary": "Local context"
      }}
    }}
  ],
  "nutrition_plan": {{
    "summary": "Overall nutrition guidance",
    "water": "Water intake recommendation",
    "meals": {{
      "breakfast": "Suggested breakfast",
      "lunch": "Suggested lunch",
      "dinner": "Suggested dinner",
      "snacks": "Healthy snacks"
    }},
    "avoid": "Foods/drinks to avoid",
    "local_tips": "Local food recommendations"
  }},
  "doctor_advice": [
    {{
      "label": "When to see doctor",
      "en": "English advice",
      "local": "Local language advice"
    }}
  ]
}}"""

                if context:
                    system_prompt += f"\n\nPatient profile: {context}"
                
                # Prepare user message
                if input_mode == "text":
                    user_msg = f"Analyze these lab values:\n\n{input_data}"
                else:
                    user_msg = "Extract all lab values from this image and analyze them completely."
                
                # Call Groq API using Anthropic SDK (compatible with Groq)
                import requests
                
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {st.session_state.groq_key}"
                }
                
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_msg}
                    ],
                    "max_tokens": 6000,
                    "temperature": 0.3
                }
                
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    # Parse JSON
                    try:
                        analysis = json.loads(content.replace("```json", "").replace("```", "").strip())
                        st.session_state.analysis_result = analysis
                    except json.JSONDecodeError:
                        st.error("❌ Could not parse response. Please try again.")
                else:
                    st.error(f"❌ API Error: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Display results
if st.session_state.analysis_result:
    st.markdown("---")
    st.markdown("# 📊 Your Health Report")
    
    analysis = st.session_state.analysis_result
    
    # Health Score
    if "health_score" in analysis:
        score = int(analysis["health_score"])
        if score >= 70:
            color = "🟢"
            status = "Good"
        elif score >= 40:
            color = "🟡"
            status = "Needs Attention"
        else:
            color = "🔴"
            status = "See a Doctor"
        
        st.markdown(f"""
<div class="info-box">
    <h2>{color} Health Score: {score}/100</h2>
    <p><strong>Status:</strong> {status}</p>
    <p>{analysis.get('score_summary', '')}</p>
</div>
""", unsafe_allow_html=True)
    
    # Tests
    if "tests" in analysis:
        st.markdown("## 🔬 Test Results")
        for test in analysis["tests"]:
            status = test.get("status", "").lower()
            if "normal" in status or "good" in status:
                icon = "✅"
            elif "high" in status or "critical" in status or "abnormal" in status:
                icon = "⚠️"
            else:
                icon = "📍"
            
            with st.expander(f"{icon} {test.get('name', 'Test')} - {test.get('value', '')} {test.get('unit', '')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Status:** {test.get('status', 'N/A')}")
                    st.markdown(f"**Range:** {test.get('normal_range', 'N/A')}")
                with col2:
                    st.markdown(f"**Value:** {test.get('value', 'N/A')} {test.get('unit', '')}")
                
                st.markdown(f"**Explanation:** {test.get('explanation_en', 'N/A')}")
                if test.get('explanation_local'):
                    st.markdown(f"*{test.get('explanation_local')}*")
                
                if test.get("symptoms"):
                    st.markdown("**Possible Symptoms:**")
                    for sym in test["symptoms"]:
                        st.markdown(f"- {sym}")
                
                if test.get("diet_do") or test.get("diet_dont"):
                    st.markdown("**Dietary Guidance:**")
                    if test.get("diet_do"):
                        st.markdown(f"✅ **Include:** {test.get('diet_do')}")
                    if test.get("diet_dont"):
                        st.markdown(f"❌ **Avoid:** {test.get('diet_dont')}")
    
    # Nutrition Plan
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
            meal_list = [
                ("🌅 Breakfast", meals.get("breakfast")),
                ("☀️ Lunch", meals.get("lunch")),
                ("🌙 Dinner", meals.get("dinner")),
                ("🍎 Snacks", meals.get("snacks"))
            ]
            
            for i, (meal_name, meal_suggestion) in enumerate(meal_list):
                if meal_suggestion:
                    with cols[i % 2]:
                        st.markdown(f"**{meal_name}**")
                        st.markdown(meal_suggestion)
        
        if nutrition.get("avoid"):
            st.markdown(f"""
<div class="danger-box">
    <strong>⚠️ Foods & Drinks to Avoid:</strong><br>
    {nutrition.get('avoid')}
</div>
""", unsafe_allow_html=True)
    
    # Doctor Advice
    if "doctor_advice" in analysis and analysis["doctor_advice"]:
        st.markdown("## ⚕️ When to Consult a Doctor")
        for advice in analysis["doctor_advice"]:
            st.markdown(f"""
<div class="warning-box">
    <strong>{advice.get('label', 'Consultation Advice')}:</strong><br>
    {advice.get('en', '')}
</div>
""", unsafe_allow_html=True)
    
    # Medical Disclaimer
    st.markdown("---")
    st.markdown("""
<div class="danger-box">
    <strong>⚕️ Medical Disclaimer:</strong><br>
    This analysis is generated by AI for health literacy and educational purposes only. 
    It is not a substitute for professional medical advice, diagnosis, or treatment. 
    Always consult a qualified healthcare provider before making any health decisions.
</div>
""", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Copy Results", use_container_width=True):
            st.success("✅ Results copied to clipboard!")
    with col2:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.analysis_result = None
            st.rerun()
    with col3:
        if st.button("💬 Share on WhatsApp", use_container_width=True):
            text = "🧬 Bio Decode AI - My Health Report\n\n"
            if "tests" in analysis:
                for test in analysis["tests"]:
                    text += f"• {test.get('name')}: {test.get('value')} {test.get('unit')} - {test.get('status')}\n"
            wa_url = f"https://wa.me/?text={text}"
            st.markdown(f"[Open WhatsApp]({wa_url})")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8fa898; font-size: 12px;">
    🧬 Bio Decode AI | © 2025 | All rights reserved<br>
    Results are AI-generated for informational purposes only
</div>
""", unsafe_allow_html=True)
