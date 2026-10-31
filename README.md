# Food Verse AI – Multimodal Food Intelligence Agent

A runnable college-project MVP with a React frontend and Flask backend.

## Features
- Responsive food-tech dashboard
- Food image upload with preview
- Food scan endpoint (clearly labeled demo mode unless an AI provider is configured)
- Nutrition estimates for common foods
- Ingredient-based recipe suggestions
- Food assistant chat (demo responses)
- Recent scan history stored in browser localStorage

## Requirements
- Python 3.8+
- Node.js 18+
- npm

## Run locally

### 1. Backend
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Backend: http://127.0.0.1:5000

### 2. Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```
Frontend: http://localhost:5173

## AI integration
The app runs in demo mode by default and does not pretend that a real vision model has analyzed an image. To connect a real multimodal AI provider, implement the provider call in `backend/services/ai_service.py` and keep credentials in `backend/.env` (never in frontend code). See `.env.example`.

## Notes
Nutrition values are rough estimates per typical serving, not medical or dietary advice. Actual values depend on recipe and portion size.
