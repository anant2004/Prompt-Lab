# Prompt Lab

Prompt Lab is a beginner-friendly AI-powered web app that evaluates user-written prompts and provides actionable feedback for prompt engineering workshops and training sessions.

## Tech Stack

- Frontend: Next.js 15 (App Router), TypeScript, TailwindCSS
- Backend: FastAPI (Python)
- AI: OpenAI-compatible API (OpenRouter-ready by default)

## Features

- Prompt quality score out of 100
- Component-wise scoring:
  - Clarity
  - Context
  - Specificity
  - Structure
  - Professional Tone
- Strengths, weaknesses, and AI suggestions
- Rewritten improved prompt
- Dark mode dashboard UI
- Animated score bars
- Copy improved prompt button
- Toast notifications
- Loading states and mobile responsive design
- Mock fallback when OpenAI key is missing

## Project Structure

```bash
prompt-lab/
  frontend/   # Next.js app
  backend/    # FastAPI service
```

## Setup Instructions

### 1) Clone and enter project

```bash
git clone <your-repo-url>
cd prompt-lab
```

### 2) Start backend

```bash
cd backend
python -m venv .venv
```

Activate virtual environment:

- Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

- macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and run:

```bash
pip install -r requirements.txt
cp .env.example .env   # On Windows, copy .env.example .env

```

### 3) Start frontend

In a new terminal:

```bash
cd frontend
npm install
cp .env.example .env.local   # On Windows, copy .env.example .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Environment Variables

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (`backend/.env`)

```env
OPENAI_API_KEY=your_openrouter_api_key_here
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-4o-mini
OPENROUTER_SITE_URL=http://localhost:3000
OPENROUTER_APP_NAME=Prompt Lab
FRONTEND_ORIGIN=http://localhost:3000
```

## API Contract

### POST `/evaluate`

Request:

```json
{
  "prompt": "Write a marketing email for our new AI course in under 120 words."
}
```

Response:

```json
{
  "overall_score": 85,
  "scores": {
    "clarity": 90,
    "context": 80,
    "specificity": 84,
    "structure": 88,
    "tone": 82
  },
  "strengths": [
    "Clear objective and audience focus",
    "Professional and concise wording"
  ],
  "weaknesses": [
    "Missing explicit format constraints"
  ],
  "suggestions": [
    "Specify output format and include required CTA details"
  ],
  "improved_prompt": "You are an expert copywriter..."
}
```

## Notes

- If `OPENAI_API_KEY` is missing or the model call fails, backend returns a safe mock response.
- For OpenRouter, keep `OPENAI_BASE_URL=https://openrouter.ai/api/v1` and use an OpenRouter model ID in `OPENAI_MODEL`.
- No authentication or database is used to keep the project workshop-friendly.
