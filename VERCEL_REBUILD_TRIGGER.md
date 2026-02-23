# Force Vercel Rebuild - Mixed Content Fix

## Issue
Vercel environment variable is set to HTTPS, but the deployed app still uses HTTP because the old build has HTTP baked into the JavaScript bundle.

## Solution: Trigger New Build

### Method 1: Redeploy from Vercel Dashboard (Fastest)

1. Go to: https://vercel.com/dashboard
2. Select project: `todos-app-seven-alpha`
3. Click **Deployments** tab
4. Find the latest deployment
5. Click the **three dots (•••)** menu
6. Click **Redeploy**
7. Confirm the redeploy
8. Wait 2-3 minutes for build to complete

### Method 2: Push Empty Commit (Alternative)

```bash
cd "D:\Q4 AI\Hackathon 2\phase-II"
git commit --allow-empty -m "Trigger Vercel rebuild for HTTPS env var"
git push origin main
```

### Method 3: Make a Small Change (Alternative)

Add a comment to trigger rebuild:
```bash
cd "D:\Q4 AI\Hackathon 2\phase-II"
echo "# Rebuild trigger" >> README.md
git add README.md
git commit -m "Trigger rebuild for HTTPS backend URL"
git push origin main
```

## Verification After Rebuild

1. Wait for Vercel deployment to complete
2. Open: https://todos-app-seven-alpha.vercel.app/dashboard/tasks
3. Open browser DevTools (F12) → Console tab
4. Try adding a task
5. Check Network tab - should see requests to `https://maniyakhan-todo-stack.hf.space` (HTTPS)
6. No more "Mixed Content" errors
7. HuggingFace logs should show 200 OK instead of 307 Redirect

## Why This Happens

Next.js `NEXT_PUBLIC_*` environment variables are:
- ✅ Baked into JavaScript at BUILD TIME
- ❌ NOT loaded at runtime

So updating the env var in Vercel doesn't affect existing builds - you need a NEW build.

## Expected Timeline

- Vercel build: ~2-3 minutes
- DNS propagation: Instant (same domain)
- Total time: ~3 minutes

---

**Status:** Ready to redeploy
**Action Required:** Choose one of the methods above to trigger a new build
