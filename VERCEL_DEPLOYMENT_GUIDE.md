# Vercel Deployment Guide for Prompt Lab

## Overview

This project has two parts:
- **Frontend**: Next.js (deploys directly on Vercel) ✅
- **Backend**: FastAPI (requires separate deployment)

## Quick Start Deployment

### Option 1: Deploy on Vercel (Recommended for Frontend)

#### Step 1: Prepare Frontend
```bash
cd frontend
npm install
```

#### Step 2: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/prompt-lab
git push -u origin main
```

#### Step 3: Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Framework: Select "Next.js"
5. Root Directory: Set to `frontend/`
6. Build command: `npm run build`
7. Output directory: `.next`

#### Step 4: Set Environment Variables in Vercel
In Vercel dashboard, go to **Settings** → **Environment Variables**:
```
NEXT_PUBLIC_API_URL = https://your-backend-url.com
```

---

### Option 2: Backend Deployment (Choose One)

#### A) Deploy on Render.com (FREE tier available)
1. Create account at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in:
   - **Name**: `prompt-lab-backend`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Add Environment Variables:
   - `OPENAI_API_KEY`: Your OpenRouter API key
   - `FRONTEND_ORIGIN`: Your Vercel frontend URL

#### B) Deploy on Railway.app
1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repo and `backend` folder
4. Add variables: `OPENAI_API_KEY`, `FRONTEND_ORIGIN`
5. Deploy

#### C) Deploy FastAPI on Vercel (Serverless)
The `vercel.json` in backend folder is configured for this.
```bash
cd backend
npm i -g vercel
vercel deploy
```

---

## Environment Variables Setup

### Frontend (.env.local in `frontend/` folder)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Backend (.env file in `backend/` folder)
```
OPENAI_API_KEY=your_openrouter_api_key
OPENAI_MODEL=openai/gpt-4o-mini
OPENAI_BASE_URL=https://api.openrouter.ai/v1
FRONTEND_ORIGIN=https://your-frontend-vercel-url.vercel.app
```

---

## Update Frontend API Client

Make sure your frontend's API client uses the environment variable:

**File**: `frontend/lib/api.ts`

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function evaluatePrompt(prompt: string) {
  const response = await fetch(`${API_URL}/evaluate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error("Failed to evaluate prompt");
  }

  return response.json();
}
```

---

## CORS Configuration

The backend needs CORS enabled for your Vercel frontend. In `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Deployment Checklist

- [ ] Frontend code pushed to GitHub
- [ ] Backend code pushed to GitHub (if separate repo or in same repo)
- [ ] Vercel project created and connected
- [ ] Backend deployed (Render/Railway/Vercel)
- [ ] Environment variables set in Vercel dashboard
- [ ] Environment variables set in backend service
- [ ] CORS configured correctly
- [ ] `NEXT_PUBLIC_API_URL` points to deployed backend
- [ ] Test the API endpoint from frontend
- [ ] Enable auto-deployments from GitHub

---

## Troubleshooting

### "Cannot reach backend"
- Check `NEXT_PUBLIC_API_URL` is correct
- Verify backend service is running
- Check CORS headers are correct
- Test backend URL directly in browser

### "API key not found"
- Verify environment variables in backend service dashboard
- Restart deployment after adding env vars

### Build fails on Vercel
- Check Node.js version compatibility
- Verify all dependencies in `package.json`
- Check build logs in Vercel dashboard

---

## Local Testing Before Deployment

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` and test the application.

---

## Additional Resources
- [Vercel Docs](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/app/building-your-application/deploying)
- [Render Deployment](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
