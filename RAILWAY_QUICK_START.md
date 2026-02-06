# ⚡ RAILWAY QUICK START - 5 MINUTE DEPLOYMENT

## 🎯 For: ekaaiurgaa@gmail.com

---

## 📱 STEP 1: One-Click Deploy (2 minutes)

**Click this button:**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/ekaaiurgaa-glitch/JAYTI)

If button doesn't work, follow manual steps below.

---

## 📝 STEP 2: Manual Deploy (If button fails)

### 2.1 Login
- Go to https://railway.app
- Click "Login with GitHub"
- Use: `ekaaiurgaa-glitch`

### 2.2 New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose: `ekaaiurgaa-glitch/JAYTI`

### 2.3 Add Database
- Click "New" → "Database" → "PostgreSQL"
- Wait 30 seconds (auto-provisions)

### 2.4 Add Environment Variables
Go to Variables tab, add:

```
SECRET_KEY=django-jayti-secret-9876543210-random-key
DEBUG=False
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro
ALLOWED_HOSTS=jaytibirthday.in,www.jaytibirthday.in,.up.railway.app
TIME_ZONE=Asia/Kolkata
BIRTH_DATE_DAY=6
BIRTH_DATE_MONTH=2
```

### 2.5 Deploy
- Click "Deploy"
- Wait 2-3 minutes

---

## ⚙️ STEP 3: Post-Deploy (3 minutes)

Open Railway Console (Logs → Console tab), run:

```bash
python manage.py migrate --noinput
python manage.py create_initial_user
python manage.py collectstatic --noinput
```

---

## 🌐 STEP 4: Domain (5 minutes)

1. Railway Settings → Domains → Custom Domain
2. Enter: `www.jaytibirthday.in`
3. Copy DNS target
4. In GoDaddy/Cloudflare:
   - Add CNAME: `www` → `[RAILWAY_DNS_TARGET]`
5. Back to Railway, click "Verify"
6. Wait 5 minutes for SSL

---

## ✅ DONE!

**Website:** https://www.jaytibirthday.in  
**Login:** jayati / jayati2026

---

## 🆘 If Something Breaks

```bash
# Debug command
python manage.py railway_debug

# Check logs
railway logs

# Restart
railway restart
```

**Full Guide:** See `RAILWAY_DEPLOYMENT_GUIDE.md`
