# IMMEDIATE FIX: Authentication "Not Found" Error

## Problem Identified
**Wrong server (Kiro Gateway) is running on port 8000 instead of your Todo API**

## STEP-BY-STEP FIX (Do this NOW)

### Step 1: Stop All Servers on Port 8000

**Option A - Using Task Manager (EASIEST)**:
1. Press `Ctrl + Shift + Esc` to open Task Manager
2. Click "Details" tab
3. Find and END these processes:
   - PID 3656
   - PID 12556
   - PID 5748
   - PID 10524
4. Right-click each → "End Task"

**Option B - Using PowerShell (Run as Administrator)**:
```powershell
Stop-Process -Id 3656 -Force
Stop-Process -Id 12556 -Force
Stop-Process -Id 5748 -Force
Stop-Process -Id 10524 -Force
```

**Option C - Double-click the batch file**:
- File created: `kill-port-8000.bat`
- Location: `D:\Q4 AI\Hackathon 2\phase-II\`
- Just double-click it

### Step 2: Verify Port is Free

Open Command Prompt and run:
```cmd
netstat -ano | findstr :8000
```

Should return NOTHING or only TIME_WAIT entries (those are OK).

### Step 3: Start the Correct Backend

**Option A - Double-click the batch file**:
- File created: `start-backend.bat`
- Location: `D:\Q4 AI\Hackathon 2\phase-II\`
- Just double-click it

**Option B - Manual command**:
```cmd
cd "D:\Q4 AI\Hackathon 2\phase-II\backend"
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Verify Correct Server is Running

**Test 1 - Check root endpoint**:
```cmd
curl http://localhost:8000/
```
Expected: `{"message":"Todo API is running!"}`
NOT: `{"status":"ok","message":"Kiro Gateway is running"...}`

**Test 2 - Check Swagger UI**:
Open browser: http://localhost:8000/docs
- Title should be: **"Todo API"**
- NOT: "Kiro Gateway"
- Should show routes: `/api/auth/signup`, `/api/auth/signin`, `/api/tasks/`

**Test 3 - Test auth endpoint**:
```cmd
curl -X POST http://localhost:8000/api/auth/signup -H "Content-Type: application/json" -d "{\"email\":\"test@test.com\",\"password\":\"test12345\"}"
```
Expected: JSON with user and token (or error if user exists)
NOT: `{"detail":"Not Found"}`

### Step 5: Test Frontend

1. Make sure frontend is running:
   ```cmd
   cd "D:\Q4 AI\Hackathon 2\phase-II\frontend"
   npm run dev
   ```

2. Open browser: http://localhost:3000/signup

3. Fill in the form:
   - Email: `newuser@test.com`
   - Password: `password123`
   - Confirm Password: `password123`

4. Click "Sign up"

5. **Expected**: Redirect to dashboard (NO "Not Found" error)

6. Test Sign In: http://localhost:3000/signin
   - Use same credentials
   - **Expected**: Redirect to dashboard

## What Was Wrong

### Your Code: ✅ CORRECT
- Backend routes properly registered
- Frontend correctly calling `/api/auth/signup` and `/api/auth/signin`
- Next.js proxy routes correctly configured
- JWT authentication logic correct

### The Problem: ❌ WRONG SERVER RUNNING
- "Kiro Gateway" (AI proxy) was running on port 8000
- Your "Todo API" was NOT running
- Multiple old server processes were blocking the port

## Verification Checklist

After following the steps above, verify:

- [ ] All old processes on port 8000 are stopped
- [ ] Port 8000 is free (netstat shows nothing or only TIME_WAIT)
- [ ] Backend server started successfully
- [ ] Console shows: "API routes successfully loaded"
- [ ] Console shows: "Database tables created successfully!"
- [ ] `curl http://localhost:8000/` returns "Todo API is running!"
- [ ] http://localhost:8000/docs shows "Todo API" (not "Kiro Gateway")
- [ ] Auth routes visible in Swagger: `/api/auth/signup`, `/api/auth/signin`
- [ ] Direct curl to `/api/auth/signup` works (returns JSON, not 404)
- [ ] Frontend running on port 3000
- [ ] Sign Up page loads without errors
- [ ] Sign Up form submission works (NO "Not Found")
- [ ] Sign In page loads without errors
- [ ] Sign In form submission works (NO "Not Found")
- [ ] After sign in, dashboard displays
- [ ] Tasks page accessible

## If Still Not Working

### Issue: "Address already in use"
**Solution**: Repeat Step 1 - some processes may have restarted

### Issue: "Module not found" errors
**Solution**:
```cmd
cd backend
pip install -r requirements.txt
```

### Issue: Frontend still shows "Not Found"
**Solution**:
1. Clear browser cache (Ctrl + Shift + Delete)
2. Hard refresh (Ctrl + F5)
3. Check browser console for actual error
4. Verify backend is responding: `curl http://localhost:8000/health`

### Issue: CORS errors in browser
**Solution**: Backend CORS is already configured for localhost:3000. If you see CORS errors, the backend is not running correctly.

## Summary

**Root Cause**: Wrong server (Kiro Gateway) running on port 8000
**Solution**: Kill old servers, start correct backend
**Your Code**: 100% correct, no changes needed
**Time to Fix**: 2-3 minutes

## Next Steps After Fix

Once authentication is working:
1. Test creating tasks
2. Test viewing tasks
3. Test updating tasks
4. Test deleting tasks
5. Test user isolation (create second user, verify they can't see first user's tasks)
