# 🚀 ONE-CLICK DEPLOY TO RAILWAY

## ⚡ Easiest Deployment Method (No Token Required!)

---

## 🎯 Option A: Railway Dashboard (Recommended - 5 minutes)

### Step 1: Open Railway
👉 **https://railway.app**

### Step 2: Create New Project
1. Click **"New"** → **"Project"**
2. Click **"Deploy from GitHub repo"**
3. Select: `ekaaiurgaa-glitch/JAYTI`
4. Click **"Deploy"**

### Step 3: Add Database
1. Click **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Wait 30 seconds (auto-configures)

### Step 4: Add Environment Variables
Go to your project → **Variables** tab → Add these:

```
SECRET_KEY=django-insecure-change-this-to-50-random-chars
DEBUG=False
GEMINI_API_KEY=AIzaSyBqPxR4P3xW9mYcZ8...
GEMINI_MODEL=gemini-pro
ALLOWED_HOSTS=jaytibirthday.in,www.jaytibirthday.in
TIME_ZONE=Asia/Kolkata
BIRTH_DATE_DAY=6
BIRTH_DATE_MONTH=2
```

### Step 5: Deploy
- Railway auto-deploys on save
- Wait 2-3 minutes

### Step 6: Run Setup Commands
Click **"View Logs"** → **"Console"** tab, run:

```bash
python manage.py migrate --noinput
python manage.py create_initial_user
python manage.py collectstatic --noinput
```

✅ **DONE!** Get your Railway URL from the dashboard.

---

## 🎯 Option B: Deploy Button (Coming Soon)

```markdown
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/ekaaiurgaa-glitch/JAYTI)
```

**Note:** This requires Railway template setup. Use Option A for now.

---

## 🎯 Option C: Railway CLI (For Advanced Users)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login (opens browser)
railway login

# Link to project
railway link

# Deploy
railway up
```

---

## 📋 POST-DEPLOYMENT CHECKLIST

- [ ] Website loads at Railway URL
- [ ] Login works: jayati / jayati2026
- [ ] Dashboard shows 6 features
- [ ] All features tested (Notes, Diary, Astro, Goals, AI Chat)
- [ ] Custom domain configured: www.jaytibirthday.in

---

## 🆘 NEED HELP?

**Railway Docs:** https://docs.railway.app  
**Full Guide:** See `RAILWAY_DEPLOYMENT_GUIDE.md`

**Quick Start:** https://railway.app
