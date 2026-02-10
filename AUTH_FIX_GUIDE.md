# Fix: "Not Found" Error on Sign In and Sign Up Pages

**Date**: 2026-02-08
**Issue**: Both Sign In and Sign Up pages show "Not Found" error when submitting forms

## Root Cause Analysis

### Problem Identified
Multiple backend servers are running on port 8000, and the one responding to requests is **NOT** the current FastAPI Todo API backend.

**Evidence**:
1. Swagger UI shows "Kiro Gateway" instead of "Todo API"
2. Multiple processes listening on port 8000:
   - PID 5748
   - PID 12556
   - PID 3656
   - PID 10524
3. Direct curl test to `/api/auth/signup` returns 404 Not Found
4. The correct FastAPI app shows routes are registered when imported in Python

### Architecture Flow
```
Frontend (Next.js) → Next.js API Route Proxy → FastAPI Backend
   /signup              /api/auth/signup         /api/auth/signup
```

**Current State**:
- Frontend: ✅ Correctly calling `/api/auth/signup` and `/api/auth/signin`
- Next.js Proxy: ✅ Correctly forwarding to `http://localhost:8000/api/auth/*`
- FastAPI Backend: ❌ Wrong server responding on port 8000

## Solution Steps

### Step 1: Stop All Servers on Port 8000

**Option A - Using Task Manager (Recommended for Windows)**:
1. Press `Ctrl + Shift + Esc` to open Task Manager
2. Go to "Details" tab
3. Find processes with PIDs: 5748, 12556, 3656, 10524
4. Right-click each → "End Task"

**Option B - Using PowerShell**:
```powershell
# Run in PowerShell as Administrator
Stop-Process -Id 5748 -Force
Stop-Process -Id 12556 -Force
Stop-Process -Id 3656 -Force
Stop-Process -Id 10524 -Force
```

**Option C - Using Command Prompt**:
```cmd
taskkill /F /PID 5748
taskkill /F /PID 12556
taskkill /F /PID 3656
taskkill /F /PID 10524
```

### Step 2: Verify Port 8000 is Free

```bash
netstat -ano | findstr :8000
```

Should return empty or no LISTENING entries.

### Step 3: Start the Correct FastAPI Backend

**Navigate to backend directory**:
```bash
cd backend
```

**Activate virtual environment** (if using one):
```bash
# Windows
.\venv\Scripts\activate
# or
.\backend_env\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**Start the server**:
```bash
# Option 1: Using uvicorn directly
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python
python -m src.main
```

**Expected output**:
```
Database tables created successfully!
API routes successfully loaded
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using StatReload
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 4: Verify Backend is Running Correctly

**Test 1: Check health endpoint**
```bash
curl http://localhost:8000/health
```
Expected: `{"status":"healthy"}`

**Test 2: Check API documentation**
Open browser: `http://localhost:8000/docs`
- Should show "Todo API" (not "Kiro Gateway")
- Should list `/api/auth/signup` and `/api/auth/signin` endpoints

**Test 3: Test signup endpoint directly**
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```
Expected: JSON response with user and token (or error if user exists)

### Step 5: Start Frontend Server

**Navigate to frontend directory**:
```bash
cd frontend
```

**Install dependencies** (if not done):
```bash
npm install
```

**Start the development server**:
```bash
npm run dev
```

**Expected output**:
```
> frontend@0.1.0 dev
> next dev

   ▲ Next.js 14.x.x
   - Local:        http://localhost:3000
   - Ready in X.Xs
```

### Step 6: Test the Authentication Flow

1. **Open browser**: `http://localhost:3000/signup`
2. **Fill in the form**:
   - Email: `user@example.com`
   - Password: `password123`
   - Confirm Password: `password123`
3. **Click "Sign up"**
4. **Expected**: Redirect to dashboard (no "Not Found" error)

5. **Test Sign In**: `http://localhost:3000/signin`
6. **Use the same credentials**
7. **Expected**: Redirect to dashboard

## Verification Checklist

- [ ] All old processes on port 8000 stopped
- [ ] Port 8000 is free
- [ ] Backend server started successfully
- [ ] Backend shows "API routes successfully loaded"
- [ ] `/health` endpoint returns healthy status
- [ ] `/docs` shows "Todo API" (not "Kiro Gateway")
- [ ] Direct curl to `/api/auth/signup` works (returns JSON, not 404)
- [ ] Frontend server running on port 3000
- [ ] Sign Up page loads without errors
- [ ] Sign Up form submission works (no "Not Found")
- [ ] Sign In page loads without errors
- [ ] Sign In form submission works (no "Not Found")
- [ ] After sign in, dashboard displays correctly
- [ ] Tasks page shows tasks (or empty state)

## Common Issues and Solutions

### Issue: "Address already in use" when starting backend
**Solution**: Another process is still using port 8000. Repeat Step 1 to kill all processes.

### Issue: "Module not found" errors when starting backend
**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

### Issue: Database connection errors
**Solution**: Check `.env` file in backend directory has correct `DATABASE_URL`

### Issue: CORS errors in browser console
**Solution**: Verify backend CORS settings include `http://localhost:3000`

### Issue: Frontend still shows "Not Found"
**Solution**:
1. Clear browser cache (Ctrl + Shift + Delete)
2. Hard refresh (Ctrl + F5)
3. Check browser console for actual error messages
4. Verify Next.js proxy routes exist in `frontend/src/app/api/auth/`

## Files Involved

### Backend
- `backend/src/main.py` - Main FastAPI application
- `backend/src/api/auth.py` - Authentication endpoints
- `backend/src/services/auth.py` - Authentication service logic
- `backend/src/models/user.py` - User model
- `backend/.env` - Environment variables

### Frontend
- `frontend/src/app/signup/page.tsx` - Sign Up page
- `frontend/src/app/signin/page.tsx` - Sign In page
- `frontend/src/lib/auth.ts` - Authentication helper functions
- `frontend/src/app/api/auth/signup/route.ts` - Next.js proxy for signup
- `frontend/src/app/api/auth/signin/route.ts` - Next.js proxy for signin
- `frontend/.env` - Environment variables

## Expected API Endpoints

After fix, these endpoints should work:

### Backend (FastAPI)
- `POST http://localhost:8000/api/auth/signup` - Register new user
- `POST http://localhost:8000/api/auth/signin` - Authenticate user
- `POST http://localhost:8000/api/auth/signout` - Sign out user
- `GET http://localhost:8000/api/tasks` - Get user tasks (requires auth)
- `GET http://localhost:8000/health` - Health check

### Frontend (Next.js)
- `POST http://localhost:3000/api/auth/signup` - Proxies to backend
- `POST http://localhost:3000/api/auth/signin` - Proxies to backend
- `POST http://localhost:3000/api/auth/signout` - Proxies to backend

## Next Steps After Fix

1. Test user registration with multiple users
2. Test user isolation (User A cannot see User B's tasks)
3. Test JWT token expiration handling
4. Test logout functionality
5. Add error handling for network failures
6. Consider adding loading states and better error messages
