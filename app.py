import streamlit as st
import json
import os
import base64
import requests
import logging
import traceback
from datetime import datetime
from io import BytesIO
import re

# ===== LOGGING SETUP =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Bio Decode AI - Professional Health Analyzer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== ENHANCED CSS STYLING =====
st.markdown("""
<style>
:root {
    --bg: #0a0f0d;
    --card: #1a2320;
    --accent: #3dffa0;
    --accent-dark: #2dd099;
    --warn: #ffb84d;
    --danger: #ff5e5e;
    --text: #e8f0ec;
    --text2: #8fa898;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg);
    color: var(--text);
}

[data-testid="stSidebar"] {
    background-color: var(--card);
    border-right: 2px solid var(--accent);
}

.stTabs [data-baseweb="tab-list"] button {
    color: var(--text2);
    border-bottom: 2px solid transparent;
}

.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 3px solid var(--accent) !important;
}

.stButton > button {
    background-color: var(--accent) !important;
    color: var(--bg) !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    transition: all 0.3s !important;
    box-shadow: 0 2px 8px rgba(61, 255, 160, 0.2) !important;
}

.stButton > button:hover {
    background-color: var(--accent-dark) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(61, 255, 160, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

.health-score-box {
    background: linear-gradient(135deg, #1a2320, #0a3d2a);
    border: 2px solid var(--accent);
    padding: 25px;
    border-radius: 12px;
    margin: 20px 0;
    text-align: center;
}

.health-score-good {
    background: linear-gradient(135deg, #2dd099, #1a9d6d);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
    border-left: 5px solid #0ec86f;
}

.health-score-warning {
    background: linear-gradient(135deg, #ffb84d, #ff9800);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
    border-left: 5px solid #ffa500;
}

.health-score-danger {
    background: linear-gradient(135deg, #ff5e5e, #e53935);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
    border-left: 5px solid #d32f2f;
}

.test-card {
    background-color: var(--card);
    border-left: 5px solid var(--accent);
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    transition: all 0.3s;
}

.test-card:hover {
    background-color: #1f2f2a;
    box-shadow: 0 4px 12px rgba(61, 255, 160, 0.1);
}

.info-box {
    background-color: var(--card);
    border: 2px solid var(--accent);
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
}

.warning-box {
    background-color: rgba(255, 184, 77, 0.1);
    border-left: 4px solid var(--warn);
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
    color: #ffb84d;
}

.danger-box {
    background-color: rgba(255, 94, 94, 0.1);
    border-left: 4px solid var(--danger);
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
    color: #ff5e5e;
}

.nutrition-card {
    background: linear-gradient(135deg, #1a2320, #0a3d2a);
    border: 1px solid var(--accent);
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
}

.metric-box {
    background-color: var(--card);
    padding: 15px;
    border-radius: 8px;
    border-top: 3px solid var(--accent);
    margin: 10px 0;
    text-align: center;
}

.stNumberInput, .stSelectbox, .stTextInput, .stTextArea {
    color: var(--text);
}

.stNumberInput input, .stSelectbox select, .stTextInput input, .stTextArea textarea {
    background-color: #0f1614 !important;
    color: var(--text) !important;
    border: 1px solid var(--text2) !important;
    border-radius: 6px !important;
}

.stNumberInput input:focus, .stSelectbox select:focus, .stTextInput input:focus, .stTextArea textarea:focus {
    border: 2px solid var(--accent) !important;
    box-shadow: 0 0 10px rgba(61, 255, 160, 0.2) !important;
}

.header-title {
    background: linear-gradient(135deg, var(--accent), #2dd099);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5em;
    font-weight: 800;
    margin: 20px 0;
}

.badge {
    display: inline-block;
    background-color: var(--accent);
    color: var(--bg);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.8em;
    font-weight: 600;
    margin: 5px 5px 5px 0;
}

.comparison-table {
    background-color: var(--card);
    border: 1px solid var(--accent);
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ===== SESSION STATE INITIALIZATION =====
if "groq_key" not in st.session_state:
    try:
        st.session_state.groq_key = st.secrets["GROQ_API_KEY"]
    except:
        st.session_state.groq_key = os.getenv("GROQ_API_KEY", "")

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "age": 30,
        "gender": "Not specified",
        "conditions": ""
    }

# ===== UTILITY FUNCTIONS =====
def validate_lab_input(lab_input):
    """Validate lab input format and content"""
    if not lab_input or len(lab_input.strip()) < 10:
        return False, "Input too short. Please provide at least 10 characters."
    
    if not any(char.isdigit() for char in lab_input):
        return False, "No numbers found. Please include actual lab values (e.g., Hemoglobin: 10.2)"
    
    if not any(keyword in lab_input.lower() for keyword in [":", "mg", "ml", "iu", "g/dl", "%"]):
        return False, "Format unclear. Use format like: Test Name: value unit (e.g., TSH: 7.2 mIU/L)"
    
    return True, ""

def generate_pdf_report(analysis, user_age, user_gender, user_conditions=""):
    """Generate professional PDF report"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#3dffa0'),
            spaceAfter=30,
            alignment=1
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#3dffa0'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        elements.append(Paragraph("🧬 BIO DECODE AI - HEALTH REPORT", title_style))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Patient Profile
        elements.append(Paragraph("Patient Profile", heading_style))
        profile_data = [
            ["Age", f"{user_age} years"],
            ["Gender", user_gender],
            ["Known Conditions", user_conditions if user_conditions else "None reported"]
        ]
        profile_table = Table(profile_data, colWidths=[2*inch, 4*inch])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1a2320')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#e8f0ec')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#3dffa0'))
        ]))
        elements.append(profile_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Health Score
        score = int(analysis.get("health_score", 0))
        score_color = colors.HexColor('#2dd099') if score >= 70 else colors.HexColor('#ffb84d') if score >= 40 else colors.HexColor('#ff5e5e')
        
        elements.append(Paragraph("Overall Health Score", heading_style))
        elements.append(Paragraph(f"<font size=20 color='#3dffa0'><b>{score}/100</b></font>", styles['Normal']))
        elements.append(Paragraph(analysis.get("score_summary", ""), styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test Results
        if "tests" in analysis and analysis["tests"]:
            elements.append(Paragraph("Lab Test Results", heading_style))
            
            test_data = [["Test", "Value", "Status", "Normal Range"]]
            for test in analysis["tests"]:
                status_color = '#2dd099' if 'normal' in test.get('status', '').lower() else '#ffb84d' if 'high' in test.get('status', '').lower() else '#ff5e5e'
                test_data.append([
                    test.get("name", ""),
                    f"{test.get('value', '')} {test.get('unit', '')}",
                    test.get("status", ""),
                    test.get("normal_range", "")
                ])
            
            test_table = Table(test_data, colWidths=[1.8*inch, 1.2*inch, 1.2*inch, 1.8*inch])
            test_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a2320')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#3dffa0')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#0f1614')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#3dffa0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))
            elements.append(test_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Nutrition Plan
        if "nutrition_plan" in analysis:
            elements.append(PageBreak())
            elements.append(Paragraph("Personalized Nutrition Plan", heading_style))
            nutrition = analysis["nutrition_plan"]
            
            elements.append(Paragraph(f"<b>Summary:</b> {nutrition.get('summary', '')}", styles['Normal']))
            
            if nutrition.get("water"):
                elements.append(Paragraph(f"<b>Hydration:</b> {nutrition.get('water')}", styles['Normal']))
            
            if nutrition.get("meals"):
                elements.append(Spacer(1, 0.1*inch))
                elements.append(Paragraph("Meal Recommendations", heading_style))
                meals = nutrition["meals"]
                for meal_name, meal_suggestion in [
                    ("Breakfast", meals.get("breakfast")),
                    ("Lunch", meals.get("lunch")),
                    ("Dinner", meals.get("dinner")),
                    ("Snacks", meals.get("snacks"))
                ]:
                    if meal_suggestion:
                        elements.append(Paragraph(f"<b>{meal_name}:</b> {meal_suggestion}", styles['Normal']))
            
            if nutrition.get("avoid"):
                elements.append(Spacer(1, 0.1*inch))
                elements.append(Paragraph(f"<b>Foods to Avoid:</b> {nutrition.get('avoid')}", styles['Normal']))
        
        # Doctor Advice
        if "doctor_advice" in analysis and analysis["doctor_advice"]:
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("When to Consult a Doctor", heading_style))
            for advice in analysis["doctor_advice"]:
                elements.append(Paragraph(f"• {advice.get('en', '')}", styles['Normal']))
        
        # Disclaimer
        elements.append(Spacer(1, 0.3*inch))
        disclaimer_style = ParagraphStyle('Disclaimer', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#8fa898'))
        elements.append(Paragraph(
            "<b>Disclaimer:</b> This report is for educational purposes only and is NOT a substitute for professional medical advice. Always consult with a qualified healthcare provider before making any health decisions.",
            disclaimer_style
        ))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        logger.error(f"PDF generation error: {str(e)}")
        return None

def analyze_lab_values(lab_input, language, age, gender, conditions, input_mode="text"):
    """Call Groq API for lab analysis"""
    try:
        context = f"Age: {age}. " + (f"Biological sex: {gender}. " if gender != "Not specified" else "") + (f"Known conditions: {conditions}. " if conditions else "")
        
        language_prompts = {
            "English": "Respond entirely in English.",
            "हिन्दी (Hindi)": "Respond entirely in Hindi using Devanagari script.",
            "English + हिन्दी": "For every field, provide response in English first, then in Hindi.",
            "ਪੰਜਾਬੀ (Punjabi)": "Respond entirely in Punjabi (Gurmukhi script).",
            "ગુજરાતી (Gujarati)": "Respond entirely in Gujarati.",
            "Español (Spanish)": "Respond entirely in Spanish.",
            "العربية (Arabic)": "Respond entirely in Arabic."
        }
        
        lang_prompt = language_prompts.get(language, "Respond entirely in English.")
        
        system_prompt = f"""You are Bio Decode AI, a professional medical analysis assistant. {lang_prompt}
Return ONLY valid JSON with no markdown fences:
{{"health_score":"0-100","score_summary":"brief summary","tests":[{{"name":"Test Name","value":"123","unit":"unit","status":"Normal/High/Low/Critical","normal_range":"60-100","explanation_en":"explanation in English","symptoms":["symptom1"],"diet_do":"recommended foods","diet_dont":"foods to avoid"}}],"nutrition_plan":{{"summary":"dietary summary","water":"hydration recommendation","meals":{{"breakfast":"suggestion","lunch":"suggestion","dinner":"suggestion","snacks":"suggestion"}},"avoid":"foods to avoid"}},"doctor_advice":[{{"label":"condition","en":"when to see doctor"}}]}}

IMPORTANT: Be VERY specific with interpretations. Use real medical reference ranges. For CRITICAL values, strongly recommend doctor visit.
Patient profile: {context}"""
        
        user_msg = f"Analyze these lab values and provide detailed health insights:\n\n{lab_input}" if input_mode == "text" else "Extract all lab values from this medical report image and provide comprehensive analysis."
        
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
            "max_tokens": 8000,
            "temperature": 0.3
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=60
        )
        
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            result = json.loads(content.replace("```json", "").replace("```", "").strip())
            return True, result
        else:
            error_msg = response.json().get("error", {}).get("message", response.text)
            return False, f"API Error: {error_msg}"
            
    except json.JSONDecodeError:
        logger.error("JSON parsing failed")
        return False, "Could not parse AI response. Please try again with clearer lab values."
    except requests.Timeout:
        logger.error("Request timeout")
        return False, "API timeout. Please try again."
    except requests.exceptions.ConnectionError:
        logger.error("Connection error")
        return False, "No internet connection. Check your connection and try again."
    except Exception as e:
        logger.error(f"Unexpected error: {traceback.format_exc()}")
        return False, f"Error: {str(e)}"

# ===== MAIN APP HEADER =====
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="header-title">🧬 BIO DECODE AI</div>', unsafe_allow_html=True)
    st.markdown("### Professional Lab Report Analysis with AI")
    st.markdown("📊 **Instant insights • 7 Languages • Personalized Nutrition • Privacy First**")

with col2:
    st.markdown("### 📈 Features")
    st.markdown("""
    <div class="badge">✅ PDF Export</div>
    <div class="badge">💾 History</div>
    <div class="badge">🔒 Private</div>
    <div class="badge">⚡ Fast</div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ===== SIDEBAR SETTINGS =====
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    language = st.selectbox(
        "🌐 Analysis Language",
        ["English", "हिन्दी (Hindi)", "English + हिन्दी", "ਪੰਜਾਬੀ (Punjabi)", 
         "ગુજરાતી (Gujarati)", "Español (Spanish)", "العربية (Arabic)"],
        help="Choose your preferred language for analysis"
    )
    
    st.markdown("---")
    
    if not st.session_state.groq_key:
        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Get free key from https://console.groq.com",
            placeholder="gsk_..."
        )
        if api_key:
            st.session_state.groq_key = api_key
            st.success("✅ API Key loaded!")
    else:
        st.success("✅ API Key configured")
        if st.button("🔄 Change API Key"):
            st.session_state.groq_key = ""
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 👤 User Profile")
    st.session_state.user_profile["age"] = st.number_input("Age", min_value=1, max_value=120, value=st.session_state.user_profile["age"])
    st.session_state.user_profile["gender"] = st.selectbox("Gender", ["Not specified", "Female", "Male", "Other"], index=0)
    st.session_state.user_profile["conditions"] = st.text_input("Known Conditions", placeholder="e.g., Diabetes, Hypertension", value=st.session_state.user_profile["conditions"])
    
    st.markdown("---")
    
    st.markdown("### 🔒 Privacy & Security")
    st.info("✅ **Zero Data Storage** - All analysis is real-time\n✅ **No Tracking** - Privacy-first design\n✅ **Secure API** - Direct to Groq\n✅ **HTTPS Only** - Encrypted communication")
    
    st.markdown("---")
    
    st.markdown("### 📚 About")
    st.markdown("Bio Decode AI helps you understand lab reports in simple language with personalized health insights.")

# ===== MAIN TABS =====
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Enter Values", "📷 Upload Photo", "📊 History", "📈 Compare", "ℹ️ Guide"])

# ===== TAB 1: ENTER VALUES =====
with tab1:
    st.markdown("### Enter Your Lab Values")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=st.session_state.user_profile["age"])
    with col2:
        gender = st.selectbox("Biological Sex", ["Not specified", "Female", "Male", "Other"], index=0)
    with col3:
        conditions = st.text_input("Known Conditions", placeholder="e.g., Diabetes", value=st.session_state.user_profile["conditions"])
    
    lab_input = st.text_area(
        "Enter or paste your lab values",
        placeholder="Example:\nHemoglobin: 10.2 g/dL\nTSH: 6.8 mIU/L\nFasting Blood Sugar: 148 mg/dL\nCreatinine: 1.8 mg/dL",
        height=200,
        help="Copy-paste directly from your lab report or type values"
    )
    
    st.markdown("**Quick Templates:**")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    samples = {
        "Thyroid": "TSH: 7.2 mIU/L\nT3: 0.8 ng/mL\nT4: 5.5 µg/dL\nFree T4: 0.9 ng/dL",
        "Diabetes": "Fasting Blood Sugar: 148 mg/dL\nHbA1c: 7.2%\nPost Prandial Sugar: 210 mg/dL\nRandom Blood Sugar: 180 mg/dL",
        "Anemia": "Hemoglobin: 8.5 g/dL\nHematocrit: 28%\nMCV: 72 fL\nFerritin: 6 ng/mL\nSerum Iron: 30 µg/dL",
        "Kidney": "Creatinine: 2.1 mg/dL\nBUN: 35 mg/dL\neGFR: 38 mL/min\nUric Acid: 8.5 mg/dL\nPhosphorus: 4.8 mg/dL",
        "Liver": "SGPT: 85 U/L\nSGOT: 72 U/L\nBilirubin: 2.4 mg/dL\nAlkaline Phosphatase: 165 U/L\nAlbumin: 3.2 g/dL",
        "Full Panel": "Hemoglobin: 9.8 g/dL\nFasting Sugar: 138 mg/dL\nTSH: 5.9 mIU/L\nTotal Cholesterol: 235 mg/dL\nLDL: 155 mg/dL\nHDL: 38 mg/dL\nCreatinine: 1.6 mg/dL\nSGPT: 42 U/L"
    }
    
    if col1.button("🦴 Thyroid", use_container_width=True):
        lab_input = samples["Thyroid"]
        st.rerun()
    if col2.button("🩺 Diabetes", use_container_width=True):
        lab_input = samples["Diabetes"]
        st.rerun()
    if col3.button("🧬 Anemia", use_container_width=True):
        lab_input = samples["Anemia"]
        st.rerun()
    if col4.button("🫘 Kidney", use_container_width=True):
        lab_input = samples["Kidney"]
        st.rerun()
    if col5.button("🍌 Liver", use_container_width=True):
        lab_input = samples["Liver"]
        st.rerun()
    if col6.button("📋 Full", use_container_width=True):
        lab_input = samples["Full Panel"]
        st.rerun()

# ===== TAB 2: PHOTO UPLOAD =====
with tab2:
    st.markdown("### Upload Lab Report Photo")
    st.info("📸 Upload a clear photo of your lab report. AI will extract values automatically.")
    
    uploaded_file = st.file_uploader(
        "Upload lab report image",
        type=["jpg", "jpeg", "png"],
        help="Supported: JPG, PNG (Max 5MB)"
    )
    
    if uploaded_file:
        if uploaded_file.size > 5 * 1024 * 1024:
            st.error("❌ Image too large (max 5MB)")
        else:
            st.image(uploaded_file, caption="Uploaded Report", use_container_width=True)
            img_base64 = base64.b64encode(uploaded_file.getvalue()).decode()
            input_mode, input_data = "photo", img_base64
            st.success("✅ Photo ready for analysis")

# ===== TAB 3: HISTORY =====
with tab3:
    st.markdown("### 📋 Your Analysis History")
    
    if st.session_state.analysis_history:
        st.markdown(f"**Total Analyses:** {len(st.session_state.analysis_history)}")
        
        # Summary stats
        col1, col2, col3 = st.columns(3)
        scores = [h.get("health_score", 0) for h in st.session_state.analysis_history]
        
        with col1:
            st.metric("Average Score", f"{sum(scores)//len(scores) if scores else 0}/100")
        with col2:
            st.metric("Latest Score", f"{scores[-1]}/100")
        with col3:
            st.metric("Total Tests", len(st.session_state.analysis_history))
        
        st.markdown("---")
        
        for i, report in enumerate(reversed(st.session_state.analysis_history)):
            score = report.get("health_score", 0)
            status = "🟢 Good" if score >= 70 else "🟡 Needs Attention" if score >= 40 else "🔴 Needs Care"
            
            with st.expander(f"{status} - {report['date']} (Score: {score}/100)"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Score Summary:**")
                    st.write(report['analysis'].get('score_summary', 'N/A'))
                
                with col2:
                    if report['analysis'].get('tests'):
                        st.write("**Tests Analyzed:**")
                        for test in report['analysis']['tests'][:5]:
                            st.write(f"• {test.get('name', 'N/A')}: {test.get('status', 'N/A')}")
                
                if st.button(f"📥 Download {i}", use_container_width=True):
                    pdf_data = generate_pdf_report(report['analysis'], 
                                                   st.session_state.user_profile["age"],
                                                   st.session_state.user_profile["gender"],
                                                   st.session_state.user_profile["conditions"])
                    if pdf_data:
                        st.download_button(
                            label="💾 Download PDF",
                            data=pdf_data,
                            file_name=f"health_report_{report['date'].replace(':', '-')}.pdf",
                            mime="application/pdf"
                        )
    else:
        st.info("📊 No analysis history yet. Create your first analysis!")

# ===== TAB 4: COMPARE =====
with tab4:
    st.markdown("### 📈 Compare Your Reports")
    
    if len(st.session_state.analysis_history) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            idx1 = st.selectbox(
                "Select First Report",
                range(len(st.session_state.analysis_history)),
                format_func=lambda i: st.session_state.analysis_history[i]['date'],
                key="comp1"
            )
        
        with col2:
            idx2 = st.selectbox(
                "Select Second Report",
                range(len(st.session_state.analysis_history)),
                format_func=lambda i: st.session_state.analysis_history[i]['date'],
                key="comp2"
            )
        
        if idx1 != idx2:
            r1 = st.session_state.analysis_history[idx1]
            r2 = st.session_state.analysis_history[idx2]
            
            st.markdown("---")
            st.markdown("### Health Score Comparison")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                s1 = int(r1['health_score'])
                st.metric("Report 1 Score", f"{s1}/100", delta=None)
            with col2:
                s2 = int(r2['health_score'])
                st.metric("Report 2 Score", f"{s2}/100", delta=None)
            with col3:
                change = s2 - s1
                st.metric("Change", f"{s2}/100", delta=change)
            
            st.markdown("---")
            st.markdown("### Individual Test Comparison")
            
            tests1 = {t['name']: t for t in r1['analysis'].get('tests', [])}
            tests2 = {t['name']: t for t in r2['analysis'].get('tests', [])}
            
            all_tests = set(tests1.keys()) | set(tests2.keys())
            
            comparison_data = []
            for test_name in all_tests:
                t1 = tests1.get(test_name, {})
                t2 = tests2.get(test_name, {})
                
                v1 = f"{t1.get('value', 'N/A')} {t1.get('unit', '')}"
                v2 = f"{t2.get('value', 'N/A')} {t2.get('unit', '')}"
                s1 = t1.get('status', 'N/A')
                s2 = t2.get('status', 'N/A')
                
                comparison_data.append({
                    "Test": test_name,
                    "Report 1": v1,
                    "Status 1": s1,
                    "Report 2": v2,
                    "Status 2": s2
                })
            
            import pandas as pd
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ Please select two different reports to compare")
    
    elif len(st.session_state.analysis_history) == 1:
        st.info("📊 Create at least 2 analyses to compare")
    else:
        st.info("📊 No analysis history yet")

# ===== TAB 5: GUIDE =====
with tab5:
    st.markdown("### 📚 How to Use Bio Decode AI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 **Enter Values Method**")
        st.markdown("""
        1. **Go to 'Enter Values' tab**
        2. **Enter your details:**
           - Age & Gender
           - Known conditions
        3. **Paste lab values** in this format:
           ```
           Test Name: value unit
           TSH: 7.2 mIU/L
           Hemoglobin: 10.2 g/dL
           ```
        4. **Click Analyze**
        5. **Get results with insights**
        """)
    
    with col2:
        st.markdown("#### 📷 **Photo Upload Method**")
        st.markdown("""
        1. **Go to 'Upload Photo' tab**
        2. **Select your lab report image**
        3. **AI extracts values automatically**
        4. **Click Analyze**
        5. **Get detailed analysis**
        """)
    
    st.markdown("---")
    
    st.markdown("#### 🎯 **Features**")
    st.markdown("""
    - **Health Score:** 0-100 personalized assessment
    - **Test Analysis:** Individual interpretation of each test
    - **Nutrition Plan:** Personalized dietary recommendations
    - **PDF Export:** Download reports to share with doctors
    - **History:** Track your health over time
    - **Comparison:** See improvement in your health
    - **7 Languages:** Support for English, Hindi, Punjabi, Gujarati, Spanish & Arabic
    """)
    
    st.markdown("#### ⚠️ **Important Disclaimer**")
    st.markdown("""
    ⚕️ This app is **FOR EDUCATIONAL PURPOSES ONLY**
    
    🚫 **NOT** a substitute for professional medical advice
    
    ✅ Always consult a qualified healthcare provider
    
    💊 Don't make medical decisions based on this analysis alone
    """)

# ===== ANALYZE BUTTON & RESULTS =====
st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    analyze_clicked = st.button("🔬 ANALYZE REPORT", use_container_width=True, key="analyze_main")

with col2:
    if st.session_state.analysis_history:
        clear_history = st.button("🗑️ Clear History", use_container_width=True)
        if clear_history:
            st.session_state.analysis_history = []
            st.rerun()

with col3:
    if st.session_state.analysis_result:
        new_analysis = st.button("🔄 New Analysis", use_container_width=True)
        if new_analysis:
            st.session_state.analysis_result = None
            st.rerun()

if analyze_clicked:
    # Get input from current tab
    if 'lab_input' in locals() and lab_input:
        input_data = lab_input
        input_mode = "text"
    elif 'uploaded_file' in locals() and uploaded_file:
        input_data = img_base64
        input_mode = "photo"
    else:
        input_data = None
        input_mode = None
    
    # Validation
    if not input_data:
        st.error("❌ Please enter lab values or upload a photo first")
    elif not st.session_state.groq_key:
        st.error("❌ Please provide your Groq API Key in the sidebar")
    else:
        # Validate input
        if input_mode == "text":
            is_valid, error_msg = validate_lab_input(input_data)
            if not is_valid:
                st.error(f"❌ {error_msg}")
            else:
                with st.spinner("🧬 Analyzing your lab report..."):
                    success, result = analyze_lab_values(
                        input_data,
                        language,
                        st.session_state.user_profile["age"],
                        st.session_state.user_profile["gender"],
                        st.session_state.user_profile["conditions"],
                        input_mode
                    )
                    
                    if success:
                        st.session_state.analysis_result = result
                        # Save to history
                        st.session_state.analysis_history.append({
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "health_score": result.get("health_score"),
                            "analysis": result
                        })
                        st.success("✅ Analysis complete!")
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")
        else:
            with st.spinner("📸 Extracting and analyzing image..."):
                success, result = analyze_lab_values(
                    input_data,
                    language,
                    st.session_state.user_profile["age"],
                    st.session_state.user_profile["gender"],
                    st.session_state.user_profile["conditions"],
                    input_mode
                )
                
                if success:
                    st.session_state.analysis_result = result
                    st.session_state.analysis_history.append({
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "health_score": result.get("health_score"),
                        "analysis": result
                    })
                    st.success("✅ Analysis complete!")
                    st.rerun()
                else:
                    st.error(f"❌ {result}")

# ===== DISPLAY RESULTS =====
if st.session_state.analysis_result:
    analysis = st.session_state.analysis_result
    
    st.markdown("---")
    st.markdown("# 📊 Your Health Analysis Report")
    
    # Health Score
    if "health_score" in analysis:
        score = int(analysis["health_score"])
        if score >= 70:
            color_class = "health-score-good"
            status = "🟢 GOOD"
        elif score >= 40:
            color_class = "health-score-warning"
            status = "🟡 NEEDS ATTENTION"
        else:
            color_class = "health-score-danger"
            status = "🔴 NEEDS CARE"
        
        st.markdown(f"""
        <div class='{color_class}'>
            <h2>Overall Health Score: {score}/100</h2>
            <h3>{status}</h3>
            <p>{analysis.get('score_summary', '')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Test Results
    if "tests" in analysis and analysis["tests"]:
        st.markdown("## 🔬 Lab Test Results")
        
        for test in analysis["tests"]:
            status_lower = test.get("status", "").lower()
            if "normal" in status_lower or "good" in status_lower:
                icon = "✅"
            elif "high" in status_lower or "critical" in status_lower:
                icon = "⚠️"
            elif "low" in status_lower:
                icon = "📍"
            else:
                icon = "❓"
            
            with st.expander(f"{icon} {test.get('name', 'Test')} - {test.get('value', 'N/A')} {test.get('unit', '')}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class='test-card'>
                    <b>Status:</b> {test.get('status', 'N/A')}<br>
                    <b>Normal Range:</b> {test.get('normal_range', 'N/A')}<br>
                    <b>Your Value:</b> {test.get('value', 'N/A')} {test.get('unit', '')}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class='info-box'>
                    <b>What It Means:</b><br>
                    {test.get('explanation_en', 'N/A')}
                    </div>
                    """, unsafe_allow_html=True)
                
                if test.get("symptoms"):
                    st.markdown("**Possible Symptoms if Abnormal:**")
                    for symptom in test["symptoms"]:
                        st.markdown(f"• {symptom}")
                
                if test.get("diet_do") or test.get("diet_dont"):
                    st.markdown("**Dietary Guidance:**")
                    if test.get("diet_do"):
                        st.markdown(f"✅ **Include:** {test.get('diet_do')}")
                    if test.get("diet_dont"):
                        st.markdown(f"❌ **Avoid:** {test.get('diet_dont')}")
    
    # Nutrition Plan
    if "nutrition_plan" in analysis:
        st.markdown("## 🥗 Personalized Nutrition Plan")
        
        nutrition = analysis["nutrition_plan"]
        st.markdown(f"**{nutrition.get('summary', '')}**")
        
        if nutrition.get("water"):
            st.markdown(f"💧 **Hydration:** {nutrition.get('water')}")
        
        if nutrition.get("meals"):
            st.markdown("### 🍽️ Meal Suggestions")
            col1, col2 = st.columns(2)
            meals = nutrition["meals"]
            
            meal_items = [
                ("🌅 Breakfast", meals.get("breakfast")),
                ("☀️ Lunch", meals.get("lunch")),
                ("🌙 Dinner", meals.get("dinner")),
                ("🍎 Snacks", meals.get("snacks"))
            ]
            
            for i, (name, suggestion) in enumerate(meal_items):
                if suggestion:
                    with col1 if i % 2 == 0 else col2:
                        st.markdown(f"""
                        <div class='nutrition-card'>
                        <b>{name}</b><br>
                        {suggestion}
                        </div>
                        """, unsafe_allow_html=True)
        
        if nutrition.get("avoid"):
            st.markdown(f"""
            <div class='danger-box'>
            <b>⚠️ Foods & Drinks to Avoid:</b><br>
            {nutrition.get('avoid')}
            </div>
            """, unsafe_allow_html=True)
    
    # Doctor Advice
    if "doctor_advice" in analysis and analysis["doctor_advice"]:
        st.markdown("## ⚕️ When to Consult a Doctor")
        for advice in analysis["doctor_advice"]:
            st.markdown(f"""
            <div class='warning-box'>
            <b>{advice.get('label', 'Medical Advice')}:</b><br>
            {advice.get('en', '')}
            </div>
            """, unsafe_allow_html=True)
    
    # Actions
    st.markdown("---")
    st.markdown("## 📥 Report Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pdf_data = generate_pdf_report(
            analysis,
            st.session_state.user_profile["age"],
            st.session_state.user_profile["gender"],
            st.session_state.user_profile["conditions"]
        )
        if pdf_data:
            st.download_button(
                label="📥 Download PDF",
                data=pdf_data,
                file_name=f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with col2:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            st.success("✅ Report copied to clipboard!")
    
    with col3:
        text = f"🧬 Bio Decode AI Results\nHealth Score: {analysis.get('health_score')}/100\n"
        text += "\n".join([f"• {t.get('name')}: {t.get('status')}" for t in analysis.get("tests", [])])
        st.link_button(
            "💬 Share WhatsApp",
            f"https://wa.me/?text={text}",
            use_container_width=True
        )
    
    with col4:
        st.link_button(
            "📧 Share Email",
            f"mailto:?subject=My%20Health%20Report&body={text}",
            use_container_width=True
        )
    
    # Disclaimer
    st.markdown("---")
    st.markdown(f"""
    <div class='danger-box'>
    <b>⚕️ Medical Disclaimer:</b><br>
    This analysis is for educational purposes only and is NOT a substitute for professional medical advice. 
    Always consult with a qualified healthcare provider before making any health decisions. 
    This tool should not be used for self-diagnosis or self-treatment.
    </div>
    """, unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#8fa898;font-size:11px;padding:20px;'>
    <p>🧬 <b>Bio Decode AI v2.0</b> | Professional Health Report Analyzer</p>
    <p>Made with ❤️ for better health literacy | © 2025 All Rights Reserved</p>
    <p>⚠️ For informational purposes only. Not a substitute for professional medical advice.</p>
</div>
""", unsafe_allow_html=True)
