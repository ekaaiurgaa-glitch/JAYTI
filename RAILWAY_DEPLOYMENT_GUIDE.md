# 🚂 RAILWAY DEPLOYMENT GUIDE - JAYTI BIRTHDAY WEBSITE

## 📋 ACCOUNT INFORMATION

**Platform:** Railway.app  
**Account Email:** ekaaiurgaa@gmail.com  
**Account Username:** ekaaiurgaa-glitch  
**Repository:** https://github.com/ekaaiurgaa-glitch/JAYTI  
**Target Domain:** www.jaytibirthday.in  

---

## 🎯 DEPLOYMENT OVERVIEW

**Time Required:** 15-20 minutes  
**Cost:** FREE (using Railway's $5/month starter plan)  
**Database:** PostgreSQL (included)  
**SSL:** Auto-provided  
**Custom Domain:** Supported  

---

## 🚀 STEP-BY-STEP DEPLOYMENT

### STEP 1: Login to Railway

1. Go to **https://railway.app**
2. Click **"Login"**
3. Choose **"Login with GitHub"**
4. Authorize Railway to access your GitHub account
5. You should see your GitHub repositories

---

### STEP 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Search for: `JAYTI` or `ekaaiurgaa-glitch/JAYTI`
4. Select the repository
5. Click **"Add Variables"** (we'll configure these next)

---

### STEP 3: Add PostgreSQL Database

1. In your project dashboard, click **"New"**
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway will automatically:
   - Create PostgreSQL instance
   - Generate `DATABASE_URL` environment variable
   - Connect it to your project

**✅ Verification:** You should see a green PostgreSQL card in your project.

---

### STEP 4: Configure Environment Variables

Go to your project → **Variables** tab → Click **"New Variable"**

Add these variables ONE BY ONE:

#### 🔐 CRITICAL VARIABLES (Must Set)

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | `django-jayti-birthday-2026-secret-key-9876543210` | Django security key |
| `DEBUG` | `False` | Production mode |
| `GEMINI_API_KEY` | `AIzaSyBqPxR4P3xW9mYcZ8...` | Your Google Gemini API key |
| `GEMINI_MODEL` | `gemini-pro` | AI model |
| `ALLOWED_HOSTS` | `jaytibirthday.in,www.jaytibirthday.in,.up.railway.app,*.up.railway.app` | Domains |
| `TIME_ZONE` | `Asia/Kolkata` | IST timezone |
| `BIRTH_DATE_DAY` | `6` | Birthday day |
| `BIRTH_DATE_MONTH` | `2` | Birthday month (February) |

#### 📌 Notes:
- **SECRET_KEY:** Generate your own 50+ character random string at https://djecrety.ir/
- **GEMINI_API_KEY:** Get from https://makersuite.google.com/app/apikey
- **ALLOWED_HOSTS:** The `.up.railway.app` is auto-added, but include it anyway

---

### STEP 5: Configure Build & Deploy

1. Go to project **Settings** tab
2. Under **Build**, ensure:
   - Build command: *(leave empty - Railway auto-detects)*
   - Start command: *(leave empty - uses Procfile)*
3. Under **Deploy**, enable:
   - ✅ **Auto-deploy on push**
   - ✅ **Deploy on branch: main**

---

### STEP 6: Deploy

1. Click **"Deploy"** button (or it will auto-deploy)
2. Wait 2-3 minutes for build to complete
3. Check logs in the **Deployments** tab

**Expected Log Output:**
```
[build] Successfully built
[deploy] Starting container
Running migrations...
Creating initial user...
Collecting static files...
Starting Gunicorn...
```

---

### STEP 7: Post-Deploy Commands

Once deployed, open **Railway Console** (click "View logs" → "Console" tab):

Run these commands ONE BY ONE:

```bash
# 1. Run database migrations
python manage.py migrate --noinput

# 2. Create initial user (jayati/jayati2026)
python manage.py create_initial_user

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Verify deployment
python manage.py railway_debug
```

**✅ Success Indicators:**
- Migrations: "OK"
- User: "Successfully created user 'jayati'"
- Static: "132 static files copied"
- Debug: "ALL CHECKS PASSED"

---

### STEP 8: Test Deployment

1. Railway will provide a URL like:
   `https://jayti-production-abc123.up.railway.app`

2. Open the URL in browser

3. **Test Login:**
   - Username: `jayati`
   - Password: `jayati2026`

4. **Verify Features:**
   - [ ] Login page loads with flower slideshow
   - [ ] Dashboard shows 6 feature cards
   - [ ] Notes: Create, edit, delete works
   - [ ] Diary: Write entry (today only)
   - [ ] Goals: Create goal, AI generates tasks
   - [ ] Astro: Birth chart displays
   - [ ] AI Chat: Responds to messages

---

### STEP 9: Custom Domain (www.jaytibirthday.in)

1. In Railway project, go to **Settings** → **Domains**
2. Click **"Custom Domain"**
3. Enter: `www.jaytibirthday.in`
4. Copy the **DNS Target** (looks like: `abc123.up.railway.app`)

#### Configure DNS (in GoDaddy/Cloudflare):

**Option A: CNAME Record (Recommended)**
```
Type: CNAME
Name: www
Value: [RAILWAY_DNS_TARGET]
TTL: 600 seconds
```

**Option B: A Record (if CNAME not supported)**
```
Type: A
Name: www
Value: [RAILWAY_SERVER_IP]
TTL: 600 seconds
```

5. Return to Railway, click **"Verify"**
6. Railway will auto-provision SSL certificate
7. Wait 5-10 minutes for DNS propagation

**✅ Verification:** https://www.jaytibirthday.in loads your website

---

### STEP 10: Final Checks

**Test these URLs:**
- [ ] `https://www.jaytibirthday.in/` (Login page)
- [ ] `https://www.jaytibirthday.in/health/` (Health check)
- [ ] `https://www.jaytibirthday.in/admin/` (Django admin)

**Login Credentials:**
- Username: `jayati`
- Password: `jayati2026`

---

## 🔧 TROUBLESHOOTING

### Issue: "Build Failed"
**Solution:**
1. Check logs in Deployments tab
2. Common fix: `pip install --upgrade pip` in build command
3. Or add to railway.toml: `NIXPACKS_PYTHON_VERSION = "3.11"`

### Issue: "Database Connection Failed"
**Solution:**
1. Verify `DATABASE_URL` is set (Railway auto-sets this)
2. Check PostgreSQL is provisioned (green card in project)
3. Restart deployment

### Issue: "Static Files 404"
**Solution:**
1. Run in console: `python manage.py collectstatic --noinput`
2. Check `STATIC_ROOT` in settings.py
3. Verify WhiteNoise is in `MIDDLEWARE`

### Issue: "Allowed Hosts Error"
**Solution:**
1. Add Railway domain to `ALLOWED_HOSTS` env var
2. Include pattern: `.up.railway.app`
3. Redeploy

### Issue: "Domain Not Working"
**Solution:**
1. Check DNS propagation: https://dnschecker.org
2. Verify CNAME/A record is correct
3. Wait 10-15 minutes for SSL certificate
4. Try clearing browser cache (Ctrl+F5)

---

## 📱 BIRTHDAY FEATURE TEST

**To test birthday message (February 6th):**

1. In Railway Console, run:
```python
python manage.py shell
```

2. Then:
```python
from django.utils import timezone
import pytz
ist = pytz.timezone('Asia/Kolkata')
now = timezone.now().astimezone(ist)
print(f"Current IST date: {now.date()}")
```

3. If today is NOT Feb 6, the birthday overlay won't show
4. To force test, temporarily modify `core/views.py` line 123
5. Or set system date to Feb 6 (not recommended)

**On actual Feb 6, 2026:** Jayti will see birthday message automatically!

---

## 💰 COST BREAKDOWN

| Component | Cost |
|-----------|------|
| Railway Starter Plan | **FREE** ($5 credit/month) |
| PostgreSQL | Included FREE |
| Custom Domain | FREE (you own domain) |
| SSL Certificate | FREE (auto-provided) |
| **Total** | **$0/month** (within free tier) |

**Note:** If traffic exceeds free tier, upgrade to $5/month plan.

---

## 🎉 SUCCESS CRITERIA

Deployment is **COMPLETE** when:

- [ ] Website loads at `https://www.jaytibirthday.in`
- [ ] SSL certificate is valid (green lock)
- [ ] Login works with jayati/jayati2026
- [ ] All 6 features work (Notes, Diary, Astro, Goals, AI Chat, Profile)
- [ ] Data persists after server restart
- [ ] Birthday message appears on Feb 6
- [ ] Health check returns 200 OK

---

## 📞 SUPPORT

**Railway Docs:** https://docs.railway.app  
**Railway Discord:** https://discord.gg/railway  
**Project Repo:** https://github.com/ekaaiurgaa-glitch/JAYTI  

**Emergency:** If deployment fails, check Railway logs and run:
```bash
python manage.py railway_debug
```

---

## 🚀 QUICK REFERENCE COMMANDS

```bash
# Deploy latest code
git push origin main

# Railway auto-deploys on push

# Check deployment status
railway status

# View logs
railway logs

# Open console
railway console

# Run management commands
python manage.py [command]
```

---

**Ready to deploy! Start with Step 1: Login to Railway.app**

🎂🌸 Happy Birthday Jayti! 🌸🎂
