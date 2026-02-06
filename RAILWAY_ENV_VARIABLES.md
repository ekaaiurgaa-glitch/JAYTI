# 🔐 RAILWAY ENVIRONMENT VARIABLES - COMPLETE LIST

## 📋 REQUIRED VARIABLES (Must Set)

```bash
# Django Security (Generate at https://djecrety.ir/)
SECRET_KEY=django-insecure-change-this-to-50-random-characters-minimum

# Production Mode
DEBUG=False

# AI Chat (Get from https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=AIzaSyBqPxR4P3xW9mYcZ8aBcDeFgHiJkLmNoPqRsTuVwXyZ

# AI Model
GEMINI_MODEL=gemini-pro

# Domain Security
ALLOWED_HOSTS=jaytibirthday.in,www.jaytibirthday.in,.up.railway.app

# Timezone (IST for India)
TIME_ZONE=Asia/Kolkata

# Birthday Settings (February 6)
BIRTH_DATE_DAY=6
BIRTH_DATE_MONTH=2
```

---

## 📋 OPTIONAL VARIABLES (Have Defaults)

```bash
# Language/Locale
LANGUAGE_CODE=en-us

# Database (Auto-set by Railway PostgreSQL)
# DATABASE_URL=postgresql://... (auto-generated)

# Google Service Account (Optional - for Vertex AI fallback)
# GOOGLE_APPLICATION_CREDENTIALS_JSON={}

# Railway Specific
RAILWAY_ENVIRONMENT=production
PYTHONUNBUFFERED=1
```

---

## 🎯 QUICK SETUP

### Step 1: Generate SECRET_KEY
Go to: https://djecrety.ir/  
Copy the generated key (50+ characters)

### Step 2: Get GEMINI_API_KEY
Go to: https://makersuite.google.com/app/apikey  
Create new key → Copy

### Step 3: Add to Railway
1. Railway Dashboard → Your Project → Variables
2. Click "New Variable" for each
3. Paste values
4. Click "Deploy"

---

## ✅ VERIFICATION

After adding variables, run in Railway Console:
```bash
python manage.py railway_debug
```

Should show:
```
✓ SECRET_KEY set
✓ GEMINI_API_KEY set
✓ ALLOWED_HOSTS configured
✓ ALL CHECKS PASSED
```

---

## 🚨 IMPORTANT NOTES

- **SECRET_KEY:** Must be 50+ random characters, keep it secret!
- **DEBUG:** Must be `False` in production
- **GEMINI_API_KEY:** Required for AI Chat feature
- **ALLOWED_HOSTS:** Must include your domain + Railway domains

---

## 📋 COPY-PASTE TEMPLATE

```
SECRET_KEY=django-insecure-replace-with-50-random-chars-here
DEBUG=False
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro
ALLOWED_HOSTS=jaytibirthday.in,www.jaytibirthday.in,.up.railway.app
TIME_ZONE=Asia/Kolkata
BIRTH_DATE_DAY=6
BIRTH_DATE_MONTH=2
```

Replace the placeholder values with your actual keys!
