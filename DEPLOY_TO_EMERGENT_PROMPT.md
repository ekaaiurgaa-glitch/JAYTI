# 🚀 EMERGENT DEPLOYMENT PROMPT - JAYTI BIRTHDAY WEBSITE

## 📋 PROJECT OVERVIEW

**Project Name:** Jayti Pargal - Personal Life Companion Website  
**Domain:** www.jaytibirthday.in  
**Repository:** https://github.com/ekaaiurgaa-glitch/JAYTI  
**Framework:** Django 4.2+  
**Database:** PostgreSQL (Production) / SQLite (Development)  
**Python Version:** 3.11+  

---

## 📁 REPOSITORY STRUCTURE

```
JAYTI/                          # Repository Root
├── .github/workflows/          # CI/CD (GitHub Actions)
│   ├── ci.yml                  # Continuous Integration
│   └── deploy.yml              # Deployment workflow
├── core/                       # User auth, dashboard, profile
│   ├── management/commands/    # Custom Django commands
│   │   ├── create_initial_user.py
│   │   └── railway_debug.py
│   └── templatetags/           # Custom template filters
├── ai_chat/                    # AI Chatbot (Gemini API)
├── astro/                      # Vedic Astrology (PySwissEph)
├── diary/                      # Multi-modal Diary
├── goals/                      # AI-powered Goal Management
├── notes/                      # Note Taking System
├── templates/                  # All HTML templates (30 files)
│   ├── ai_chat/
│   ├── astro/
│   ├── core/
│   ├── diary/
│   ├── goals/
│   └── notes/
├── static/                     # CSS, JS, Images
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── railway.toml               # Railway deployment config
├── railway_startup.sh         # Startup script
├── Procfile                   # Process definition
└── DEPLOYMENT.md              # Deployment guide
```

---

## 🔐 REQUIRED ENVIRONMENT VARIABLES

Set these in Emergent dashboard BEFORE deployment:

### CRITICAL (Must Set)
```bash
# Django Security
SECRET_KEY=your-random-50-character-secret-key-here-change-this
DEBUG=False

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# AI Chat (Gemini API)
GEMINI_API_KEY=your-google-gemini-api-key
GEMINI_MODEL=gemini-pro

# Domain Configuration
ALLOWED_HOSTS=jaytibirthday.in,www.jaytibirthday.in,localhost,127.0.0.1

# Timezone & Birthday Settings
TIME_ZONE=Asia/Kolkata
BIRTH_DATE_DAY=6
BIRTH_DATE_MONTH=2
```

### OPTIONAL (Have Defaults)
```bash
# Google Service Account (if using Vertex AI)
GOOGLE_APPLICATION_CREDENTIALS_JSON={}

# Railway Specific
RAILWAY_ENVIRONMENT=production
RAILWAY_DEBUG=false
PYTHONUNBUFFERED=1
```

---

## 📦 BUILD & DEPLOYMENT STEPS

### Step 1: Clone Repository
```bash
git clone https://github.com/ekaaiurgaa-glitch/JAYTI.git
cd JAYTI
```

### Step 2: Python Environment
```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Database Setup
```bash
# Run migrations
python manage.py migrate --noinput

# Create initial user (jayati/jayati2026)
python manage.py create_initial_user
```

### Step 4: Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### Step 5: Verify Deployment
```bash
# Run deployment debugger
python manage.py railway_debug

# Check Django
python manage.py check
```

### Step 6: Start Server
```bash
# Using Gunicorn (Production)
gunicorn jaytipargal.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 2 \
    --threads 4 \
    --worker-class gthread \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

# OR using the startup script
bash railway_startup.sh
```

---

## 🗄️ DATABASE CONFIGURATION

### PostgreSQL (Production - REQUIRED)
```bash
# Emergent should provide PostgreSQL
# Connection string format:
DATABASE_URL=postgres://username:password@hostname:5432/database_name
```

### SQLite (Development - NOT for production)
- Only for local testing
- Will be deleted on redeploy

---

## 🌐 DOMAIN SETUP

### Primary Domain
**www.jaytibirthday.in**

### DNS Configuration (User will set in GoDaddy/Cloudflare)
```
A Record:     @     → [EMERGENT_SERVER_IP]
CNAME Record: www   → [EMERGENT_APP_URL]
```

### SSL Certificate
- Must enable HTTPS
- Auto-redirect HTTP to HTTPS

---

## 🔍 HEALTH CHECK ENDPOINT

**URL:** `https://www.jaytibirthday.in/health/`  
**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-06T23:44:58",
  "checks": {
    "database": "ok",
    "staticfiles": "ok",
    "astrology": "available"
  }
}
```

---

## 🎂 BIRTHDAY FEATURE (FEB 6)

On February 6th every year, the website shows a special birthday message:
- Login page displays birthday overlay
- Personalized message from Vivek
- Special animations

**To Test:** Set system date to Feb 6 or modify `core/views.py` line 123

---

## 👤 DEFAULT LOGIN CREDENTIALS

After deployment, Jayti logs in with:
- **Username:** `jayati`
- **Password:** `jayati2026`

She can change password via: Profile → Change Password

---

## 📱 FEATURES TO VERIFY AFTER DEPLOYMENT

### 1. Login Page (`/`)
- [ ] Beautiful login with flower slideshow
- [ ] Daily changing quotes
- [ ] Clock showing IST time
- [ ] Birthday message (on Feb 6)

### 2. Dashboard (`/dashboard/`)
- [ ] 6 navigation cards (Profile, Notes, Diary, Astro, Goals, Ask Jayti)
- [ ] Statistics display
- [ ] Birthday greeting (on Feb 6)

### 3. Profile (`/profile/`)
- [ ] Display personal info
- [ ] Change password functionality
- [ ] Profile picture upload

### 4. Notes (`/notes/`)
- [ ] Create, edit, delete notes
- [ ] Search functionality
- [ ] Tags system

### 5. Diary (`/diary/`)
- [ ] Multi-input (Type, Voice, Handwriting)
- [ ] Date restriction (only write today)
- [ ] Calendar view
- [ ] Mood tracking
- [ ] Writing streak counter

### 6. Astro (`/astro/`)
- [ ] Birth chart display
- [ ] 12 houses analysis
- [ ] Vimshottari Dasha periods
- [ ] 90-day predictions

### 7. Goals (`/goals/`)
- [ ] Create marketing career goals
- [ ] AI-generated tasks by department
- [ ] Kanban board view
- [ ] Progress tracking

### 8. AI Chat (`/ai-chat/`)
- [ ] Gemini AI integration
- [ ] Mentors mode (remembers context)
- [ ] Clean formatting (no *, #, etc.)
- [ ] Conversation history

---

## 🚨 IMPORTANT NOTES FOR EMERGENT

### 1. File Structure
- Django project is at **REPOSITORY ROOT** (not in a subdirectory)
- `manage.py` is directly in the root
- Do NOT use `cd jaytipargal` - it will fail

### 2. Static Files
- WhiteNoise is configured for static files
- Static files are served from `/static/` URL
- Run `collectstatic` during build

### 3. Media Files
- User uploads go to `/media/` directory
- Configure persistent storage for `/media/`
- Profile pictures, handwriting images stored here

### 4. Database Persistence
- PostgreSQL is REQUIRED for production
- SQLite will be lost on redeploy
- DATABASE_URL must be set

### 5. PySwissEph (Astrology)
- This package requires C compiler
- If installation fails, astrology features auto-disable
- Site works fine without it (graceful degradation)

### 6. Gemini API
- Required for AI Chat and Goal AI features
- If not set, AI features show fallback responses
- Get API key from: https://makersuite.google.com/app/apikey

---

## 🔧 TROUBLESHOOTING

### Issue: "ModuleNotFoundError: No module named 'xyz'"
```bash
pip install -r requirements.txt
```

### Issue: "SECRET_KEY not set"
```bash
export SECRET_KEY="your-random-secret-key-min-50-chars"
```

### Issue: "Database connection failed"
- Verify DATABASE_URL is correct
- Check PostgreSQL is running
- Ensure database exists

### Issue: "Static files 404"
```bash
python manage.py collectstatic --noinput
```

### Issue: "Allowed hosts error"
- Add domain to ALLOWED_HOSTS env var
- Or temporarily set `ALLOWED_HOSTS=*` (not secure)

---

## 📞 EMERGENCY CONTACT

If deployment fails:
1. Check logs in Emergent dashboard
2. Run: `python manage.py railway_debug`
3. Verify all env vars are set
4. Check PostgreSQL connection
5. Test locally first: `python manage.py runserver`

---

## ✅ DEPLOYMENT VERIFICATION CHECKLIST

Before marking as complete:

- [ ] Repository cloned successfully
- [ ] Python 3.11+ installed
- [ ] All pip dependencies installed
- [ ] PostgreSQL database connected
- [ ] All environment variables set
- [ ] Migrations applied successfully
- [ ] Static files collected
- [ ] Initial user created (jayati/jayati2026)
- [ ] Health check endpoint responds 200 OK
- [ ] All 6 main features working (Notes, Diary, Astro, Goals, AI Chat, Profile)
- [ ] Domain www.jaytibirthday.in configured
- [ ] SSL certificate installed
- [ ] HTTPS redirect working

---

## 🎯 SUCCESS CRITERIA

Website is successfully deployed when:
1. ✅ https://www.jaytibirthday.in/ loads without errors
2. ✅ Login works with jayati/jayati2026
3. ✅ Dashboard shows 6 feature cards
4. ✅ All features (Notes, Diary, Astro, Goals, AI Chat) are functional
5. ✅ Data persists after server restart
6. ✅ Birthday message appears on Feb 6

---

**Repository:** https://github.com/ekaaiurgaa-glitch/JAYTI  
**Domain:** www.jaytibirthday.in  
**Ready for Deployment:** YES  

🚀 DEPLOY AND MAKE JAYTI'S BIRTHDAY SPECIAL!
