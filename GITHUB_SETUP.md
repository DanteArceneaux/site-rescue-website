# GitHub + Netlify Continuous Deployment Setup

## Step 1: Create GitHub Repository

I've opened GitHub for you. In the browser:

1. **Repository name**: `site-rescue-website`
2. **Description**: "Site Rescue - Web design agency landing page"
3. **Visibility**: Choose **Public** (or Private if you prefer)
4. **DO NOT** initialize with README, .gitignore, or license (we already have them)
5. Click **"Create repository"**

---

## Step 2: Push Your Code to GitHub

After creating the repo, GitHub will show you commands. Run these in your terminal:

```bash
git remote add origin https://github.com/YOUR-USERNAME/site-rescue-website.git
git branch -M main
git push -u origin main
```

**Or copy this command (replace YOUR-USERNAME):**

```bash
git remote add origin https://github.com/YOUR-USERNAME/site-rescue-website.git && git branch -M main && git push -u origin main
```

---

## Step 3: Connect Netlify to GitHub

1. Go to your Netlify site: https://app.netlify.com/sites/zesty-dodol-376e53/configuration/deploys
2. Scroll to **"Continuous deployment"** section
3. Click **"Link repository"** button
4. Choose **GitHub**
5. Authorize Netlify (if prompted)
6. Select your repository: **site-rescue-website**
7. Configure build settings:
   - **Base directory**: `website`
   - **Build command**: (leave empty)
   - **Publish directory**: `.` or leave empty
8. Click **"Deploy site"**

---

## Step 4: Verify Continuous Deployment

After setup, every time you push code to GitHub:

```bash
git add .
git commit -m "Your changes"
git push
```

Netlify will automatically:
- Detect the push
- Deploy your changes
- Update your live site

---

## Current Status

✅ Git initialized
✅ Files committed
✅ Sensitive files excluded (.gitignore updated)
⏳ Waiting for GitHub repo creation
⏳ Waiting for Netlify connection

---

## Your Files Are Ready

Your project includes:
- ✅ Website files (index.html, style.css, script.js)
- ✅ Updated pricing ($1,500, $125/mo, $350/mo)
- ✅ Email automation scripts
- ✅ Lead generation bot
- ✅ .gitignore (protecting credentials)

**Next**: Complete Steps 1-3 above to enable continuous deployment!
