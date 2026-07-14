# ToneShift: Audience-Aware Rewriter

Streamlit app that rewrites text using Groq (Llama 3.3) while adapting to audience and tone, with analysis, history, exports, and TTS.

## Features
- Paste text
- Upload PDF / DOCX
- Select audience, tone, and adjustments
- Rewrite via Groq API
- Text analysis (word/character count, readability)
- Plotly charts
- Save rewrite history
- Export rewritten text (TXT / DOCX / PDF)
- Play voice (gTTS)

## Setup
1. Create a virtual environment (recommended)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure env:
   ```bash
   cp .env.example .env
   # set GROQ_API_KEY
   ```
4. Run:
   ```bash
   python -m streamlit run app.py
   ```

## Deployment
Compatible with Streamlit Community Cloud and GitHub.
- Configure `GROQ_API_KEY` in Streamlit secrets/environment variables.

