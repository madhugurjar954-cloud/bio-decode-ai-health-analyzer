# 🚀 QUICK START GUIDE - BIO DECODE AI v2.0

**Get your app running in 5 minutes!**

---

## ⚡ 5-Minute Setup

### Step 1: Clone the Repository (1 min)
```bash
git clone https://github.com/madhugurjar954-cloud/bio-decode-ai-health-analyzer.git
cd bio-decode-ai-health-analyzer
```

### Step 2: Install Dependencies (2 min)
```bash
pip install -r requirements.txt
```

### Step 3: Get Free Groq API Key (1 min)
1. Go to https://console.groq.com
2. Click "Sign Up" 
3. Sign up with email/Google
4. Go to "API Keys" section
5. Click "Create New API Key"
6. Copy the key (starts with `gsk_`)

### Step 4: Run the App (1 min)
```bash
streamlit run app.py
```

Your browser will open automatically. If not, go to: **http://localhost:8501**

### Step 5: Paste API Key & Analyze!
- In the sidebar, paste your Groq API Key
- Enter lab values or upload photo
- Click "🔬 ANALYZE REPORT"
- Done! 🎉

---

## 📝 Test It Immediately

### Quick Test (No Real Data Needed)
1. Open the app
2. Paste API key in sidebar
3. Go to "📝 Enter Values" tab
4. Click "🦴 Thyroid" button (auto-fills sample data)
5. Click "🔬 ANALYZE REPORT"
6. See results in 5 seconds!

### Try Other Samples
- 🩺 **Diabetes** - Blood sugar values
- 🧬 **Anemia** - Hemoglobin levels
- 🫘 **Kidney** - Creatinine, BUN
- 🍌 **Liver** - SGPT, SGOT values
- 📋 **Full Panel** - Complete health check

---

## 🌐 Deploy to Cloud (FREE)

### Deploy to Streamlit Cloud (5 minutes)

**Already deployed at:** https://bio-decode-ai-health-analyzer.streamlit.app

To deploy your own copy:

1. **Push to GitHub**
```bash
git add .
git commit -m "Bio Decode AI v2.0"
git push origin main
```

2. **Go to Streamlit Cloud**
- Visit https://share.streamlit.io
- Click "New app"
- Select your repo
- Branch: `main`
- File: `app.py`
- Click "Deploy"

3. **Add API Key**
- In Streamlit dashboard → Settings → Secrets
- Add: `GROQ_API_KEY = gsk_your_key_here`
- Save

Your app is now live! Share the link with anyone! 🌍

---

## 📊 Features Quick Reference

| Feature | How to Use |
|---------|-----------|
| **Enter Lab Values** | Paste text in "📝 Enter Values" tab |
| **Upload Photo** | Click "📷 Upload Photo" tab |
| **Change Language** | Select in sidebar "🌐 Analysis Language" |
| **Download PDF** | Click "📥 Download PDF" after analysis |
| **View History** | Go to "📋 History" tab |
| **Compare Reports** | Go to "📈 Compare" tab (need 2+ analyses) |
| **Share Results** | Click "💬 WhatsApp" or "📧 Email" |

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### "API Key Not Working"
- ✅ Check key starts with `gsk_`
- ✅ Visit https://console.groq.com and verify key is active
- ✅ Copy-paste carefully (no spaces)
- ✅ Try creating a new key

### "Port 8501 already in use"
```bash
streamlit run app.py --logger.level=debug --server.port 8502
```

### "Image Upload Not Working"
- ✅ File must be < 5MB
- ✅ Format: JPG or PNG only
- ✅ Make image clear and readable
- ✅ Try cropping just the lab report section

### "No Internet Connection"
- ✅ Check your internet
- ✅ Groq API needs internet connection
- ✅ Check if console.groq.com is accessible

---

## 🎯 Next Steps

### Option 1: Use the App
1. Try all features (text, photo, templates)
2. Download PDFs
3. Share with friends
4. Collect feedback

### Option 2: Customize
1. Edit `config.py` to change medical ranges
2. Modify `app.py` to add new features
3. Change colors in CSS section
4. Add new languages

### Option 3: Deploy & Share
1. Deploy to Streamlit Cloud (free)
2. Share link with friends
3. Collect usage data
4. Plan monetization

### Option 4: Contribute
1. Add new lab test templates
2. Improve UI/UX
3. Add new languages
4. Fix bugs
5. Submit pull requests

---

## 📚 What's Included

```
bio-decode-ai-health-analyzer/
├── app.py                 # Main Streamlit app
├── config.py             # Medical ranges & settings
├── requirements.txt      # Python dependencies
├── README.md            # Full documentation
├── QUICKSTART.md        # This file!
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
└── server.js            # Optional backend (Node.js)
```

---

## 💡 Pro Tips

### Tip 1: Use Sample Data First
Click template buttons (Thyroid, Diabetes, etc.) to test without real data.

### Tip 2: Copy-Paste Format
Copy directly from your lab report. Format like:
```
TSH: 7.2 mIU/L
Hemoglobin: 10.2 g/dL
```

### Tip 3: Save PDFs
Always download PDF reports to keep records. Share with doctors.

### Tip 4: Track Progress
Use "📈 Compare" to see if your health is improving over time.

### Tip 5: Share Results
Use WhatsApp/Email buttons to get feedback from friends & family.

---

## 🔒 Privacy Reminder

✅ Your data is **NOT stored** anywhere  
✅ Photos are **deleted** after analysis  
✅ No tracking or analytics  
✅ No account required  
✅ Completely anonymous  

---

## 📞 Need Help?

- **GitHub Issues:** https://github.com/madhugurjar954-cloud/bio-decode-ai-health-analyzer/issues
- **Email:** madhugurjar954@gmail.com
- **GitHub:** @madhugurjar954-cloud

---

## 🎓 Learn More

- **Streamlit Docs:** https://docs.streamlit.io
- **Groq API Docs:** https://console.groq.com/docs
- **Python Guide:** https://www.python.org/doc

---

## ⚠️ Important

**This app is educational only. Not a substitute for professional medical advice. Always consult doctors for health decisions.**

---

**Happy analyzing! 🧬**

Made with ❤️ | Version 2.0 | July 2026
