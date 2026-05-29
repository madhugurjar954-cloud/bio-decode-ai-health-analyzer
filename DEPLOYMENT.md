# 🚀 Deployment Guide — Bio Decode AI

This guide walks you through deploying Bio Decode AI to live URLs.

## Option 1: GitHub Pages (Recommended - Free)

### Step 1: Enable GitHub Pages

1. Go to your repository: `https://github.com/madhugurjar954-cloud/bio-decode-ai-health-analyzer`
2. Click **Settings** (top navigation)
3. Scroll to **Pages** section (left sidebar)
4. Under **Source**:
   - Select Branch: `main`
   - Select Folder: `/ (root)`
5. Click **Save**

### Step 2: Wait for Deployment

- GitHub will build and deploy your site
- Check the **Deployments** section in your repository
- Look for a checkmark ✓ next to "github-pages"

### Step 3: Access Your Live Site

**Your live URL will be:**
```
https://madhugurjar954-cloud.github.io/bio-decode-ai-health-analyzer/
```

### Step 4: Update API Key Securely (IMPORTANT)

⚠️ **NEVER commit your API key to GitHub!**

#### Option A: Use a Backend Server
1. Create a backend API endpoint (Node.js, Python, etc.)
2. Backend handles Groq API calls securely
3. Update the JavaScript to call your backend instead

**Example backend endpoint:**
```javascript
// In index.html, replace the fetch call with:
fetch('https://your-backend.com/api/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    values: userMsg,
    language: lang,
    // other parameters
  })
})
```

#### Option B: Use GitHub Secrets + GitHub Actions
1. Add your Groq API key to GitHub Secrets:
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `GROQ_API_KEY`
   - Value: Your Groq API key
2. Create a `.github/workflows/deploy.yml` file to inject it

---

## Option 2: Netlify (Alternative - Free)

### Step 1: Connect Netlify
1. Go to [netlify.com](https://netlify.com)
2. Sign up with GitHub
3. Click "New site from Git"
4. Select your repository
5. Configure build settings:
   - Build command: (leave empty)
   - Publish directory: `.` (root)
6. Click "Deploy site"

### Step 2: Get Your URL
- Netlify will provide a URL like: `https://your-site-name.netlify.app`

### Step 3: Add Environment Variables
1. Go to Site Settings → Build & deploy → Environment
2. Add:
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key
3. Redeploy

---

## Option 3: Vercel (Alternative - Free)

### Step 1: Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "Import Project"
3. Select your GitHub repository
4. Click "Import"

### Step 2: Configure Environment
1. Add environment variable:
   - Name: `GROQ_API_KEY`
   - Value: Your Groq API key
2. Click "Deploy"

### Step 3: Access Your Site
- Vercel provides a URL: `https://your-project.vercel.app`

---

## Securing Your API Key

### ✅ Best Practices

1. **Never** commit API keys to GitHub
2. **Always** use environment variables
3. **Use** a backend server for production
4. **Rotate** API keys if compromised
5. **Monitor** API usage for unusual activity

### Backend Example (Node.js + Express)

```javascript
// backend/server.js
const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');

const app = express();
app.use(cors());
app.use(express.json());

const GROQ_API_KEY = process.env.GROQ_API_KEY;

app.post('/api/analyze', async (req, res) => {
  try {
    const { userMsg, language } = req.body;
    
    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GROQ_API_KEY}`
      },
      body: JSON.stringify({
        model: 'llama-3.3-70b-versatile',
        max_tokens: 6000,
        temperature: 0.3,
        messages: [/* your messages */]
      })
    });

    const data = await response.json();
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

---

## Custom Domain Setup

### For GitHub Pages:
1. Go to Settings → Pages
2. Under "Custom domain", enter your domain (e.g., `bioai.example.com`)
3. Add DNS records to point to GitHub:
   - Type: `A` records pointing to GitHub IPs
   - Or `CNAME` record pointing to your GitHub Pages URL

### For Netlify:
1. Go to Site Settings → Domain Management
2. Click "Add custom domain"
3. Follow Netlify's DNS setup instructions

---

## Testing Before Going Live

1. **Test locally**: Open `index.html` in your browser
2. **Test with data**: Use the sample buttons or enter test values
3. **Check all features**:
   - Text input ✓
   - Photo upload ✓
   - Language switching ✓
   - PDF export ✓
   - WhatsApp sharing ✓
4. **Test responsiveness**: Check on mobile, tablet, desktop
5. **Verify API calls**: Open browser DevTools → Network tab

---

## Troubleshooting

### Site not loading?
- Check if GitHub Pages is enabled
- Verify branch is set to `main` and folder is `/`
- Wait a few minutes after enabling (GitHub takes time to build)

### API calls failing?
- Check if API key is correct
- Verify Groq API key is active
- Check browser console for errors (F12)
- Ensure you're using the correct Groq endpoint

### Images not loading?
- Verify image paths are relative
- Check if images are in the repository

### CORS errors?
- Use a backend server (recommended)
- Or enable CORS in your backend

---

## Monitoring & Analytics

### Optional: Add Analytics
Add Google Analytics to track usage:

```html
<!-- Add before </head> in index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

---

## Next Steps

1. ✅ Enable GitHub Pages (instructions above)
2. ✅ Get your live URL
3. ✅ Secure your API key
4. ✅ Test all features
5. ✅ Share with users

---

**Need help?** Check the main README.md or open a GitHub Issue.
