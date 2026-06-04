const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:5000',
  credentials: true
}));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb' }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Bio Decode AI Backend is running' });
});

// Main API endpoint for lab analysis
app.post('/api/analyze', async (req, res) => {
  try {
    const { systemPrompt, userMessage } = req.body;

    if (!systemPrompt || !userMessage) {
      return res.status(400).json({ 
        error: 'Missing required fields: systemPrompt and userMessage' 
      });
    }

    // Verify API key exists
    if (!process.env.GROQ_API_KEY) {
      console.error('GROQ_API_KEY is not set in environment variables');
      return res.status(500).json({ 
        error: 'Server configuration error: API key not found' 
      });
    }

    // Call Groq API
    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.GROQ_API_KEY}`
      },
      body: JSON.stringify({
        model: 'llama-3.3-70b-versatile',
        max_tokens: 6000,
        temperature: 0.3,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userMessage }
        ]
      })
    });

    const data = await response.json();

    if (!response.ok) {
      console.error('Groq API Error:', data);
      return res.status(response.status).json({ 
        error: data.error?.message || 'Error calling Groq API' 
      });
    }

    // Extract the response content
    const content = data.choices?.[0]?.message?.content || '';
    
    res.json({
      success: true,
      content: content,
      raw: data
    });

  } catch (error) {
    console.error('Backend Error:', error.message);
    res.status(500).json({ 
      error: 'Internal server error: ' + error.message 
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled Error:', err);
  res.status(500).json({ 
    error: 'An unexpected error occurred' 
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ 
    error: 'Endpoint not found' 
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🧬 Bio Decode AI Backend running on port ${PORT}`);
  console.log(`Frontend URL: ${process.env.FRONTEND_URL || 'http://localhost:5000'}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});
