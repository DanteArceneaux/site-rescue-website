# Secure GitHub Setup

## Create Personal Access Token (Instead of Password)

I've opened the token creation page. Follow these steps:

1. **Note**: "Site Rescue Deployment"
2. **Expiration**: 90 days (or your preference)
3. **Scopes**: Check these boxes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
4. Click **"Generate token"**
5. **COPY THE TOKEN** - you'll only see it once!

---

## Push Code to GitHub

After creating your repo and getting your token:

```bash
# Add remote (replace USERNAME with: dantearcene)
git remote add origin https://github.com/dantearcene/site-rescue-website.git

# Push code
git branch -M main
git push -u origin main
```

When prompted for password, **paste your token** (not your actual password).

---

## Even Better: Use GitHub CLI

```bash
gh auth login
```

Choose:
- GitHub.com
- HTTPS
- Yes (authenticate Git with GitHub credentials)
- Login with web browser

Then:
```bash
gh repo create site-rescue-website --public --source=. --push
```

Done! No password needed.

---

## Security Tips

✅ Never share passwords with anyone (including AI assistants)
✅ Use Personal Access Tokens for Git operations
✅ Use SSH keys for long-term access
✅ Enable 2-factor authentication on GitHub
⚠️ Change your password since it was shared

