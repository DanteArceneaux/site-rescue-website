# 🔧 Gmail API Setup Guide

Complete step-by-step instructions to set up Gmail API for the email automation system.

---

## ⏱️ Time Required: ~15 minutes

---

## 📋 Prerequisites

- ✅ Gmail account
- ✅ Python 3.x installed
- ✅ All Python packages installed (`pip install -r requirements.txt`)

---

## 🚀 Step-by-Step Setup

### **Step 1: Go to Google Cloud Console**

1. Open your browser and go to:
   ```
   https://console.cloud.google.com/
   ```

2. Sign in with your Gmail account

---

### **Step 2: Create a New Project**

1. Click the project dropdown at the top (next to "Google Cloud")

2. Click **"NEW PROJECT"**

3. Enter project details:
   - **Project name**: `Lead Gen Bot` (or any name)
   - **Organization**: Leave as is (or select if you have one)

4. Click **"CREATE"**

5. Wait for the project to be created (~30 seconds)

6. Select your new project from the dropdown

---

### **Step 3: Enable Gmail API**

1. In the left sidebar, click **"APIs & Services"** > **"Library"**

2. In the search bar, type: `Gmail API`

3. Click on **"Gmail API"** from the results

4. Click the blue **"ENABLE"** button

5. Wait for it to enable (~10 seconds)

---

### **Step 4: Create OAuth Credentials**

1. In the left sidebar, click **"APIs & Services"** > **"Credentials"**

2. Click **"+ CREATE CREDENTIALS"** at the top

3. Select **"OAuth client ID"**

4. **If prompted to configure consent screen:**
   - Click **"CONFIGURE CONSENT SCREEN"**
   - Select **"External"** (unless you have Google Workspace)
   - Click **"CREATE"**
   - Fill in required fields:
     - **App name**: `Lead Gen Bot`
     - **User support email**: Your email
     - **Developer contact**: Your email
   - Click **"SAVE AND CONTINUE"**
   - Skip "Scopes" (click **"SAVE AND CONTINUE"**)
   - Add yourself as a test user:
     - Click **"+ ADD USERS"**
     - Enter your Gmail address
     - Click **"ADD"**
   - Click **"SAVE AND CONTINUE"**
   - Review summary and click **"BACK TO DASHBOARD"**
   - Go back to: **"APIs & Services"** > **"Credentials"**
   - Click **"+ CREATE CREDENTIALS"** > **"OAuth client ID"** again

5. **Create OAuth Client ID:**
   - Application type: **"Desktop app"**
   - Name: `Lead Gen Bot Desktop`
   - Click **"CREATE"**

6. A popup will show your credentials:
   - Click **"DOWNLOAD JSON"**
   - Save the file

---

### **Step 5: Save Credentials File**

1. Rename the downloaded file to exactly:
   ```
   credentials.json
   ```

2. Move it to your automation folder:
   ```
   C:\Users\dante\OneDrive\Desktop\Automation\credentials.json
   ```

3. Verify it's in the same folder as `agency_bot.py`

---

### **Step 6: Run Setup Script**

1. Open terminal in your automation folder

2. Run the setup helper:
   ```bash
   python gmail_auth_helper.py
   ```

3. **Your browser will open automatically**

4. You'll see a Google security warning:
   - Click **"Advanced"**
   - Click **"Go to Lead Gen Bot (unsafe)"**
   - (It's safe—it's your own app!)

5. Click **"Continue"**

6. Select your Gmail account

7. Review permissions:
   - ✅ Read, compose, send emails
   - Click **"Continue"**

8. **Authorization complete!**

9. Go back to the terminal—you should see:
   ```
   ✅ SETUP COMPLETE!
   🎉 Gmail API is ready to use!
   ```

10. A file called `token.json` will be created (this stores your authorization)

---

## ✅ Verify Setup

Run the test:
```bash
python gmail_auth_helper.py
```

You should see:
```
✅ Successfully connected to Gmail API!
📧 Email: your.email@gmail.com
📊 Total messages: 1234
```

---

## 🔒 Security Notes

### **What We Created:**
- `credentials.json` - OAuth client ID (not secret if leaked, but keep private)
- `token.json` - Your personal access token (KEEP THIS SECRET!)

### **Important:**
- ✅ **DO** add both files to `.gitignore` if using Git
- ❌ **DON'T** share these files with anyone
- ❌ **DON'T** commit them to GitHub
- ✅ **DO** keep backups in a secure location

### **If Compromised:**
- Go to Google Cloud Console > Credentials
- Delete the OAuth client
- Create a new one
- Re-run setup

---

## 🛠️ Troubleshooting

### **Error: "credentials.json not found"**
**Solution:** Make sure `credentials.json` is in the same folder as the scripts.

---

### **Error: "Access blocked: This app's request is invalid"**
**Solution:** 
1. Go to Cloud Console > OAuth consent screen
2. Make sure your email is added as a test user
3. Make sure app is in "Testing" mode (not "Production")

---

### **Error: "Gmail API has not been enabled"**
**Solution:** 
1. Go to APIs & Services > Library
2. Search "Gmail API"
3. Click "Enable"

---

### **Browser doesn't open during auth**
**Solution:** 
- The URL will print in terminal
- Copy and paste it into your browser manually

---

### **Error: "Token has been expired or revoked"**
**Solution:** 
1. Delete `token.json`
2. Run `python gmail_auth_helper.py` again
3. Re-authorize in browser

---

### **Error: "Daily sending limit exceeded"**
**Solution:** 
- New Gmail accounts: 100-500 emails/day
- Wait 24 hours
- Reduce `MAX_DAILY_SENDS` in `config_email.py`

---

### **Emails going to spam**
**Solution:** 
- Reduce sending volume
- Add delays between emails (10+ seconds)
- Personalize more (use business name)
- Ask recipients to whitelist your email
- Consider using a domain email (not @gmail.com)

---

## 📚 Additional Resources

- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
- [Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)

---

## 🎉 Next Steps

Once setup is complete:

1. **Edit `config_email.py`:**
   - Add your name, phone, website
   - Customize email templates
   - Set `TEST_MODE = True`

2. **Test with yourself:**
   ```bash
   python email_sender.py
   ```

3. **Check that emails arrive correctly**

4. **Once satisfied, set `TEST_MODE = False`**

5. **Start automating! 🚀**

---

**Questions?** Check the troubleshooting section or review the Google Cloud Console setup.

