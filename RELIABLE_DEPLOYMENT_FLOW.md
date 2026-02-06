# 🔄 RELIABLE DEPLOYMENT FLOW

## 🎯 Overview

This document describes the reliable CI/CD pipeline for deploying JAYTI to Railway.app

**GitHub Account:** ekaaiurgaa-glitch  
**Repository:** https://github.com/ekaaiurgaa-glitch/JAYTI  
**Platform:** Railway.app  
**Domain:** www.jaytibirthday.in  

---

## 🏗️ Deployment Architecture

```
GitHub Push → CI Build & Test → Deploy to Railway → Post-Deploy Verification
     ↓              ↓                    ↓                    ↓
  Code Commit   Validate Build      Auto-Deploy          Health Check
```

---

## 📋 Workflow Files

| Workflow | File | Purpose |
|----------|------|---------|
| **CI** | `.github/workflows/ci.yml` | Build, test, validate on every push |
| **Reliable Deploy** | `.github/workflows/reliable-deploy.yml` | Deploy to Railway with verification |

---

## 🚀 Deployment Process

### 1. CI Pipeline (Automatic on every push)

**Triggers:**
- Push to `main` branch
- Push to `develop` branch
- Pull request to `main`

**Steps:**
1. ✅ Checkout code
2. ✅ Set up Python 3.11
3. ✅ Install dependencies
4. ✅ Django system check
5. ✅ Check migrations
6. ✅ Run migrations
7. ✅ Collect static files

**Outcome:** Build validated before deployment

---

### 2. Deployment Pipeline (Automatic on main branch)

**Prerequisites:**
- CI pipeline must pass
- Push to `main` branch
- `RAILWAY_TOKEN` secret configured

**Steps:**
1. ✅ Verify Railway token
2. ✅ Install Railway CLI
3. ✅ Deploy to Railway
4. ✅ Wait for stabilization
5. ✅ Verify deployment status

---

### 3. Post-Deploy Verification

**Checks:**
1. ✅ Wait 60 seconds for startup
2. ✅ Health check endpoint
3. ✅ Deployment report

---

## 🔐 Required GitHub Secrets

Configure these in GitHub Repository Settings → Secrets → Actions:

| Secret | Value | How to Get |
|--------|-------|------------|
| `RAILWAY_TOKEN` | Railway API token | Railway Dashboard → Account → Tokens |

**To generate Railway token:**
1. Go to https://railway.app/account/tokens
2. Click "New Token"
3. Name: `GitHub Actions Deploy`
4. Copy token
5. Add to GitHub Secrets as `RAILWAY_TOKEN`

---

## 📊 Deployment Scenarios

### Scenario 1: Normal Push to Main

```
Developer pushes code → CI runs → Deploys to Railway → Verification
```

**Time:** ~5 minutes

### Scenario 2: Pull Request

```
PR created → CI runs (build & test) → Report status → Merge
```

**Time:** ~3 minutes

### Scenario 3: Manual Deployment

```
Go to Actions → Reliable Railway Deployment → Run workflow
```

**Use when:** Emergency deployment needed

---

## 🛡️ Safety Features

| Feature | Description |
|---------|-------------|
| **CI Gates** | Deployment only if CI passes |
| **Branch Protection** | Only `main` branch deploys |
| **Token Verification** | Validates Railway token before deploy |
| **Status Checks** | Verifies deployment success |
| **Timeout Protection** | Prevents hanging deployments |

---

## 🚨 Troubleshooting

### Issue: "RAILWAY_TOKEN not set"

**Solution:**
```bash
# 1. Get token from Railway
https://railway.app/account/tokens

# 2. Add to GitHub
GitHub Repo → Settings → Secrets → Actions → New repository secret
Name: RAILWAY_TOKEN
Value: [your-token-here]
```

### Issue: "Deployment failed"

**Check:**
1. Railway logs in dashboard
2. GitHub Actions logs
3. Environment variables set
4. Database connected

### Issue: "Health check failed"

**Manual verification:**
```bash
# Check deployment URL
curl https://your-app.up.railway.app/health/

# Expected response:
{"status": "healthy", ...}
```

---

## 📝 Manual Deployment (No CI/CD)

If CI/CD is not working, deploy manually:

### Option A: Railway Dashboard
1. Go to https://railway.app
2. Select project
3. Click "Deploy" button

### Option B: Railway CLI
```bash
# Install CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

---

## 🎉 Success Indicators

Deployment is **SUCCESSFUL** when:

- [ ] ✅ CI pipeline passes (green checkmark)
- [ ] ✅ Deployment workflow completes
- [ ] ✅ Railway shows green "Healthy" status
- [ ] ✅ Website loads at Railway URL
- [ ] ✅ Login works (jayati/jayati2026)
- [ ] ✅ Custom domain configured
- [ ] ✅ SSL certificate active

---

## 📈 Deployment History

View all deployments:
- GitHub: Actions tab → Workflow runs
- Railway: Dashboard → Deployments

---

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| GitHub Repo | https://github.com/ekaaiurgaa-glitch/JAYTI |
| Railway Dashboard | https://railway.app/dashboard |
| Railway Token | https://railway.app/account/tokens |
| Website (Live) | https://www.jaytibirthday.in |

---

## 🎯 Next Steps

1. **Configure Railway Token** in GitHub Secrets
2. **Push code** to trigger deployment
3. **Verify** deployment successful
4. **Configure domain** www.jaytibirthday.in
5. **Test** all features

---

**Reliable deployment flow is ready! 🚀**
