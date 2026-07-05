# Bio Decode AI - Configuration File
# Medical Reference Ranges & Settings

# ===== NORMAL LAB VALUE RANGES =====
# These are general ranges. Individual ranges may vary by lab.

LAB_REFERENCE_RANGES = {
    # Thyroid Tests
    "TSH": {
        "normal_range": "0.4 - 4.0 mIU/L",
        "unit": "mIU/L",
        "critical_low": 0.1,
        "critical_high": 10,
        "low_threshold": 0.4,
        "high_threshold": 4.0
    },
    "T3": {
        "normal_range": "0.8 - 2.0 ng/mL",
        "unit": "ng/mL",
        "critical_low": 0.3,
        "critical_high": 3.0,
        "low_threshold": 0.8,
        "high_threshold": 2.0
    },
    "T4": {
        "normal_range": "4.5 - 12.0 µg/dL",
        "unit": "µg/dL",
        "critical_low": 2.0,
        "critical_high": 15.0,
        "low_threshold": 4.5,
        "high_threshold": 12.0
    },
    
    # Diabetes Tests
    "Fasting Blood Sugar": {
        "normal_range": "70 - 100 mg/dL",
        "unit": "mg/dL",
        "critical_low": 50,
        "critical_high": 300,
        "low_threshold": 70,
        "high_threshold": 100
    },
    "HbA1c": {
        "normal_range": "< 5.7%",
        "unit": "%",
        "critical_low": 3.0,
        "critical_high": 15.0,
        "low_threshold": 5.7,
        "high_threshold": 6.5
    },
    "Random Blood Sugar": {
        "normal_range": "< 140 mg/dL",
        "unit": "mg/dL",
        "critical_low": 50,
        "critical_high": 400,
        "low_threshold": 140,
        "high_threshold": 200
    },
    "Post Prandial Sugar": {
        "normal_range": "< 140 mg/dL",
        "unit": "mg/dL",
        "critical_low": 50,
        "critical_high": 400,
        "low_threshold": 140,
        "high_threshold": 200
    },
    
    # Anemia Tests
    "Hemoglobin": {
        "normal_range": "12.0 - 17.5 g/dL (Female: 12-15.5)",
        "unit": "g/dL",
        "critical_low": 7.0,
        "critical_high": 20.0,
        "low_threshold": 12.0,
        "high_threshold": 17.5
    },
    "Hematocrit": {
        "normal_range": "36 - 46%",
        "unit": "%",
        "critical_low": 20,
        "critical_high": 60,
        "low_threshold": 36,
        "high_threshold": 46
    },
    "MCV": {
        "normal_range": "80 - 100 fL",
        "unit": "fL",
        "critical_low": 50,
        "critical_high": 130,
        "low_threshold": 80,
        "high_threshold": 100
    },
    "Ferritin": {
        "normal_range": "30 - 400 ng/mL",
        "unit": "ng/mL",
        "critical_low": 5,
        "critical_high": 1000,
        "low_threshold": 30,
        "high_threshold": 400
    },
    "Serum Iron": {
        "normal_range": "60 - 170 µg/dL",
        "unit": "µg/dL",
        "critical_low": 30,
        "critical_high": 300,
        "low_threshold": 60,
        "high_threshold": 170
    },
    
    # Kidney Tests
    "Creatinine": {
        "normal_range": "0.7 - 1.3 mg/dL",
        "unit": "mg/dL",
        "critical_low": 0.1,
        "critical_high": 10.0,
        "low_threshold": 0.7,
        "high_threshold": 1.3
    },
    "BUN": {
        "normal_range": "7 - 20 mg/dL",
        "unit": "mg/dL",
        "critical_low": 2,
        "critical_high": 100,
        "low_threshold": 7,
        "high_threshold": 20
    },
    "eGFR": {
        "normal_range": "> 60 mL/min/1.73m²",
        "unit": "mL/min/1.73m²",
        "critical_low": 5,
        "critical_high": 120,
        "low_threshold": 60,
        "high_threshold": 120
    },
    "Uric Acid": {
        "normal_range": "3.5 - 7.2 mg/dL",
        "unit": "mg/dL",
        "critical_low": 1,
        "critical_high": 15,
        "low_threshold": 3.5,
        "high_threshold": 7.2
    },
    "Phosphorus": {
        "normal_range": "2.5 - 4.5 mg/dL",
        "unit": "mg/dL",
        "critical_low": 1,
        "critical_high": 10,
        "low_threshold": 2.5,
        "high_threshold": 4.5
    },
    
    # Liver Tests
    "SGPT": {
        "normal_range": "7 - 56 U/L",
        "unit": "U/L",
        "critical_low": 0,
        "critical_high": 500,
        "low_threshold": 56,
        "high_threshold": 200
    },
    "SGOT": {
        "normal_range": "10 - 40 U/L",
        "unit": "U/L",
        "critical_low": 0,
        "critical_high": 500,
        "low_threshold": 40,
        "high_threshold": 200
    },
    "Bilirubin": {
        "normal_range": "0.3 - 1.2 mg/dL",
        "unit": "mg/dL",
        "critical_low": 0,
        "critical_high": 10,
        "low_threshold": 1.2,
        "high_threshold": 3.0
    },
    "Alkaline Phosphatase": {
        "normal_range": "44 - 147 U/L",
        "unit": "U/L",
        "critical_low": 0,
        "critical_high": 500,
        "low_threshold": 147,
        "high_threshold": 300
    },
    "Albumin": {
        "normal_range": "3.5 - 5.5 g/dL",
        "unit": "g/dL",
        "critical_low": 1,
        "critical_high": 8,
        "low_threshold": 3.5,
        "high_threshold": 5.5
    },
    
    # Cholesterol Tests
    "Total Cholesterol": {
        "normal_range": "< 200 mg/dL",
        "unit": "mg/dL",
        "critical_low": 50,
        "critical_high": 500,
        "low_threshold": 200,
        "high_threshold": 239
    },
    "LDL": {
        "normal_range": "< 100 mg/dL",
        "unit": "mg/dL",
        "critical_low": 20,
        "critical_high": 500,
        "low_threshold": 100,
        "high_threshold": 159
    },
    "HDL": {
        "normal_range": "> 40 mg/dL",
        "unit": "mg/dL",
        "critical_low": 10,
        "critical_high": 200,
        "low_threshold": 40,
        "high_threshold": 200
    },
    "Triglycerides": {
        "normal_range": "< 150 mg/dL",
        "unit": "mg/dL",
        "critical_low": 20,
        "critical_high": 800,
        "low_threshold": 150,
        "high_threshold": 200
    },
}

# ===== CRITICAL VALUE ALERTS =====
# When results exceed these, prioritize doctor consultation

CRITICAL_ALERTS = {
    "Hemoglobin": {"low": 7, "high": 20},
    "Fasting Blood Sugar": {"low": 50, "high": 300},
    "Creatinine": {"low": 0.1, "high": 10},
    "TSH": {"low": 0.1, "high": 10},
}

# ===== LANGUAGE PROMPTS =====
LANGUAGE_PROMPTS = {
    "English": "Respond entirely in English.",
    "हिन्दी (Hindi)": "Respond entirely in Hindi using Devanagari script. Make sure all medical terms are explained in simple Hindi.",
    "English + हिन्दी": "For every field, provide response in English first (bold), then in Hindi. Use format: **English:** ... \n**हिन्दी:** ...",
    "ਪੰਜਾਬੀ (Punjabi)": "Respond entirely in Punjabi (Gurmukhi script). Use simple language understandable to common people.",
    "ગુજરાતી (Gujarati)": "Respond entirely in Gujarati. Provide medical information in simple Gujarati that common people can understand.",
    "Español (Spanish)": "Respond entirely in Spanish. Make explanations clear and accessible.",
    "العربية (Arabic)": "Respond entirely in Arabic. Use simple, clear language for medical explanations.",
}

# ===== TEST CATEGORIES =====
TEST_CATEGORIES = {
    "Thyroid": ["TSH", "T3", "T4", "Free T4"],
    "Diabetes": ["Fasting Blood Sugar", "HbA1c", "Random Blood Sugar", "Post Prandial Sugar"],
    "Anemia": ["Hemoglobin", "Hematocrit", "MCV", "Ferritin", "Serum Iron"],
    "Kidney": ["Creatinine", "BUN", "eGFR", "Uric Acid", "Phosphorus"],
    "Liver": ["SGPT", "SGOT", "Bilirubin", "Alkaline Phosphatase", "Albumin"],
    "Heart": ["Troponin", "BNP", "Total Cholesterol", "LDL", "HDL"],
    "Cholesterol": ["Total Cholesterol", "LDL", "HDL", "Triglycerides"],
}

# ===== DIETARY RECOMMENDATIONS BY TEST =====
DIETARY_RECOMMENDATIONS = {
    "High Cholesterol": {
        "include": "Oats, fish, nuts, olive oil, whole grains, fruits, vegetables",
        "avoid": "Butter, cheese, red meat, fried foods, processed items"
    },
    "High Blood Sugar": {
        "include": "Leafy greens, legumes, whole grains, lean protein, low-GI fruits",
        "avoid": "Sugar, refined carbs, white bread, sweets, sugary drinks"
    },
    "Low Hemoglobin": {
        "include": "Red meat, spinach, lentils, fortified cereals, beans, dark leafy greens",
        "avoid": "Tea with meals (inhibits iron absorption)"
    },
    "High Creatinine": {
        "include": "Low-protein vegetables, whole grains, fruits",
        "avoid": "Red meat, dairy, processed foods, salt"
    },
    "High SGPT": {
        "include": "Turmeric, leafy greens, whole grains, nuts, fish",
        "avoid": "Alcohol, fatty foods, processed items, refined sugars"
    },
}

# ===== APP SETTINGS =====
APP_CONFIG = {
    "version": "2.0",
    "app_name": "Bio Decode AI",
    "tagline": "Professional Lab Report Analyzer",
    "max_file_size_mb": 5,
    "api_timeout_seconds": 60,
    "max_tokens": 8000,
    "temperature": 0.3,
    "default_age": 30,
    "default_gender": "Not specified",
    "demo_mode": False,
}

# ===== GROQ MODEL CONFIG =====
MODEL_CONFIG = {
    "model_name": "llama-3.3-70b-versatile",
    "provider": "groq",
    "api_endpoint": "https://api.groq.com/openai/v1/chat/completions",
}

# ===== COLORS & STYLING =====
COLORS = {
    "bg": "#0a0f0d",
    "card": "#1a2320",
    "accent": "#3dffa0",
    "accent_dark": "#2dd099",
    "warn": "#ffb84d",
    "danger": "#ff5e5e",
    "text": "#e8f0ec",
    "text_secondary": "#8fa898",
}

# ===== HELP TEXT =====
HELP_TEXT = {
    "lab_values": """
    Paste your lab values in this format:
    
    Test Name: value unit
    Example:
    TSH: 7.2 mIU/L
    Hemoglobin: 10.2 g/dL
    Fasting Blood Sugar: 148 mg/dL
    """,
    "photo_upload": "Upload a clear photo of your lab report. The AI will extract values automatically.",
    "api_key": "Get a free API key from https://console.groq.com. Sign up and create an API key in your account.",
}
