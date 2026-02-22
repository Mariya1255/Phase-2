# Deployment Guide - Vercel + HuggingFace

## ✅ Code Changes Completed

The following issues have been fixed in the codebase:

### 1. Environment Variable Standardization
- **Changed:** `NEXT_PUBLIC_API_BASE_URL` → `NEXT_PUBLIC_API_URL`
- **Files Updated:**
  - `frontend/.env`
  - `frontend/src/services/api.ts`

### 2. CORS Configuration Fixed
- **Changed:** HTTP → HTTPS for Vercel deployment
- **File Updated:** `backend/src/main.py`
- **New CORS origins:**
  ```python
  "https://frontend-red-omega-45.vercel.app"  # Your production URL
  "https://*.vercel.app"  # All Vercel preview deployments
  ```

## 🚀 Deployment Steps

### Step 1: Deploy Backend to HuggingFace

1. **Push your backend code to HuggingFace Spaces**
2. **Note your HuggingFace Space URL** (format: `https://username-spacename.hf.space`)
3. **Verify backend is running:**
   ```bash
   curl https://your-space-name.hf.space/health
   ```
   Should return: `{"status": "healthy"}`

### Step 2: Configure Vercel Environment Variables

1. **Go to Vercel Dashboard** → Your Project → Settings → Environment Variables
2. **Add the following variable:**
   ```
   Name: NEXT_PUBLIC_API_URL
   Value: https://your-huggingface-space.hf.space
   ```
   ⚠️ **IMPORTANT:**
   - Use HTTPS (not HTTP)
   - No trailing slash
   - Replace with your actual HuggingFace URL

3. **Apply to all environments:**
   - ✅ Production
   - ✅ Preview
   - ✅ Development

### Step 3: Update Backend CORS (if needed)

If your Vercel URL is different from `frontend-red-omega-45.vercel.app`:

1. **Edit `backend/src/main.py` line 58:**
   ```python
   "https://your-actual-vercel-url.vercel.app",
   ```

2. **Redeploy backend to HuggingFace**

### Step 4: Trigger New Vercel Deployment

⚠️ **CRITICAL:** Environment variables are baked into the build at BUILD TIME.

**Option A: Redeploy via Git**
```bash
git add .
git commit -m "Fix deployment configuration"
git push origin main
```

**Option B: Manual Redeploy**
- Go to Vercel Dashboard → Deployments
- Click "Redeploy" on the latest deployment

### Step 5: Verify Deployment

1. **Open browser console** on your Vercel URL
2. **Check Network tab** when signing in/up
3. **Verify API calls go to:** `https://your-huggingface-space.hf.space/api/auth/...`

## 🔍 Troubleshooting

### Issue: "Failed to connect to authentication service"

**Cause:** Frontend can't reach backend
**Check:**
```javascript
// Add temporarily to sign-in page
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);
```
- If `undefined` → Environment variable not set in Vercel
- If `localhost` → Old build, need to redeploy

### Issue: "CORS policy blocked"

**Cause:** Backend CORS doesn't allow your Vercel URL
**Fix:**
1. Check browser console for exact origin being blocked
2. Add that origin to `backend/src/main.py` CORS list
3. Redeploy backend

### Issue: "Network request failed"

**Cause:** HuggingFace backend is down or URL is wrong
**Check:**
```bash
curl https://your-space-name.hf.space/health
```
- If fails → Backend not running on HuggingFace
- If succeeds → Check URL in Vercel env vars

## 📋 Deployment Checklist

- [ ] Backend deployed to HuggingFace
- [ ] Backend health endpoint returns 200
- [ ] Vercel env var `NEXT_PUBLIC_API_URL` set to HuggingFace URL (HTTPS)
- [ ] Backend CORS includes your Vercel URL (HTTPS)
- [ ] New Vercel deployment triggered after env var change
- [ ] Browser console shows correct API URL (not localhost)
- [ ] Sign up/sign in works on production
- [ ] Tasks can be created/updated/deleted

## 🔐 Security Notes

1. **Never commit `.env` files** with production secrets
2. **Use Vercel environment variables** for production config
3. **Rotate JWT secrets** before production deployment
4. **Enable HTTPS only** in production (already configured)

## 📝 Environment Variable Reference

### Frontend (Vercel)
```bash
NEXT_PUBLIC_API_URL=https://your-huggingface-space.hf.space
```

### Backend (HuggingFace)
```bash
DATABASE_URL=postgresql://...  # Your Neon database URL
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BETTER_AUTH_SECRET=your-production-auth-secret
```

## 🎯 Next Steps After Deployment

1. Test all authentication flows
2. Test task CRUD operations
3. Monitor HuggingFace logs for errors
4. Check Vercel function logs for issues
5. Set up error monitoring (Sentry, LogRocket, etc.)

---

**Need Help?** Check the browser console and network tab for specific error messages.
