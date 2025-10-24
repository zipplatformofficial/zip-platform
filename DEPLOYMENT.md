# 🚀 Deployment Guide

## Pre-Deployment Checklist

### ✅ Code Cleanup
- [x] Remove Claude references
- [x] Delete `.claude` directory
- [x] Clean up unnecessary documentation
- [x] Update README.md
- [x] Create .gitignore

### ✅ Frontend Configuration

1. **Environment Variables**
   ```bash
   cd frontend-web
   cp .env.example .env.production
   ```

   Update the following in `.env.production`:
   - `VITE_API_URL` - Your backend API URL
   - `VITE_PAYSTACK_PUBLIC_KEY` - Paystack public key
   - `VITE_GOOGLE_MAPS_API_KEY` - Google Maps API key
   - Other service keys as needed

2. **Build Test**
   ```bash
   npm run build
   npm run preview
   ```

3. **Check Build Output**
   - Verify no errors in build
   - Test the preview build
   - Check bundle size

### ✅ Backend Configuration

1. **Environment Variables**
   Update `.env` in backend with production values:
   - Database connection string
   - Secret keys
   - CORS origins (add your Netlify URL)
   - Email settings
   - Payment gateway credentials

2. **Database Migration**
   ```bash
   # Run migrations on production database
   alembic upgrade head
   ```

3. **Test API**
   - All endpoints working
   - Authentication working
   - File uploads working

## Netlify Deployment Steps

### Method 1: Netlify Dashboard (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial deployment setup"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Netlify**
   - Go to https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub and select your repository
   - Configure build settings:
     - **Base directory:** `frontend-web`
     - **Build command:** `npm run build`
     - **Publish directory:** `dist`
     - **Node version:** 18

3. **Add Environment Variables**
   - Go to Site settings → Environment variables
   - Add all variables from `.env.example`
   - Save and redeploy

4. **Configure Domain**
   - Go to Domain settings
   - Add custom domain or use Netlify subdomain
   - Configure SSL (automatically handled by Netlify)

### Method 2: Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize site
cd frontend-web
netlify init

# Deploy
netlify deploy --prod
```

## Backend Deployment Options

### Option 1: Railway

1. Go to https://railway.app
2. Create new project from GitHub
3. Select backend folder
4. Add environment variables
5. Deploy

### Option 2: Render

1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables
7. Deploy

### Option 3: DigitalOcean App Platform

1. Go to DigitalOcean Apps
2. Create new app from GitHub
3. Configure Python environment
4. Add database
5. Deploy

## Post-Deployment

### 1. Update Frontend API URL
```bash
# In Netlify environment variables
VITE_API_URL=https://your-backend-url.com/api/v1
```

### 2. Configure Backend CORS
```python
# backend/app/core/config.py
CORS_ORIGINS = [
    "https://your-netlify-app.netlify.app",
    "https://your-custom-domain.com"
]
```

### 3. Test Everything
- [ ] User registration
- [ ] User login
- [ ] Browse vehicles
- [ ] Book rental
- [ ] Book maintenance
- [ ] Shop products
- [ ] Payment flow
- [ ] Admin dashboard

### 4. Performance Optimization
- [ ] Enable gzip compression (Netlify does this automatically)
- [ ] Optimize images
- [ ] Enable CDN
- [ ] Add caching headers

### 5. Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Set up analytics (Google Analytics)
- [ ] Monitor API performance
- [ ] Set up uptime monitoring

## Environment Variables Reference

### Frontend (.env)
```env
VITE_API_URL=https://api.zipplatform.com/api/v1
VITE_PAYSTACK_PUBLIC_KEY=pk_live_xxxxx
VITE_GOOGLE_MAPS_API_KEY=xxxxx
VITE_FIREBASE_API_KEY=xxxxx
VITE_APP_NAME=ZIP Platform
VITE_APP_VERSION=1.0.0
```

### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["https://your-app.netlify.app"]
PAYSTACK_SECRET_KEY=sk_live_xxxxx
SMTP_HOST=smtp.gmail.com
SMTP_USER=noreply@zipplatform.com
SMTP_PASSWORD=xxxxx
```

## Troubleshooting

### Build Fails on Netlify
- Check Node version (should be 18+)
- Verify all dependencies are in package.json
- Check for any import errors

### API Connection Issues
- Verify VITE_API_URL is correct
- Check CORS settings on backend
- Ensure backend is deployed and running

### Environment Variables Not Working
- Prefix with `VITE_` for frontend
- Redeploy after adding variables
- Check variable names match exactly

## Rollback Plan

If something goes wrong:

1. **Netlify:**
   - Go to Deploys tab
   - Click on a previous successful deploy
   - Click "Publish deploy"

2. **Backend:**
   - Revert to previous commit
   - Redeploy

## Security Checklist

- [ ] All API keys are in environment variables
- [ ] No hardcoded secrets in code
- [ ] HTTPS enabled (automatic on Netlify)
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation working
- [ ] SQL injection protection
- [ ] XSS protection

## Performance Targets

- Lighthouse Score: 90+
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- Total Bundle Size: < 1MB

---

**Ready to Deploy! 🎉**
