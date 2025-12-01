# 🚀 Quick Start Guide - 5 Minutes to Your First Leads

## Step 1: Install Everything (2 minutes)

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

## Step 2: Get Your Free Gemini API Key (1 minute)

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

## Step 3: Configure (1 minute)

**Set your API key:**

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY="your_key_here"
```

**Mac/Linux:**
```bash
export GEMINI_API_KEY="your_key_here"
```

**Or edit `agency_bot.py` line 44:**
```python
GEMINI_API_KEY = "your_actual_key_here"
```

**Set your search query (line 36):**
```python
SEARCH_QUERY = "Landscapers in Austin Texas"  # ← Change this
```

## Step 4: Run! (1 minute)

```bash
python agency_bot.py
```

## Step 5: Check Results

- **CSV**: `leads.csv` (open in Excel/Google Sheets)
- **Screenshots**: `scans/` folder

---

## 🎯 What You'll Get

### HOT Leads 🔥
- Outdated website
- Email found
- Ready to contact immediately

### WARM Leads 🌡️
- Outdated website  
- Contact page found
- Visit page to get email

### COLD Leads ❄️
- Modern website
- Different pitch needed

### Manual Review 🔍
- AI couldn't analyze
- Check the screenshot manually

---

## 💡 Pro Tips

### Your First Run
1. Start with `MAX_RESULTS = 5` to test
2. Set `HEADLESS = False` to watch the browser
3. Check `scans/` folder to see what it captures

### Refining Your Search
```python
# Good searches (specific + location)
"Plumbers in Brooklyn NY"
"Italian restaurants in Miami"
"Real estate agents in Denver"

# Bad searches (too broad)
"Plumbers"
"Restaurants"
"Agents"
```

### Rate Limits
- Free Gemini tier: 15 requests/minute
- Bot processes ~6-10 leads/min
- Safe for up to 50 leads per session

---

## 🆘 Common Issues

**"Playwright browser not installed"**
→ Run: `playwright install chromium`

**"GEMINI_API_KEY not set"**
→ Set the environment variable or edit line 44 in the script

**"No leads found"**
→ Try a more specific search query with a city name

**Too many timeouts**
→ Some sites are slow. Increase delays or try different query

---

## 📧 Sample Email Template

```
Subject: Quick question about [Business Name]

Hi [Name],

I was searching for [niche] in [city] and came across your website.

[PASTE THE DRAFT_HOOK FROM CSV HERE]

I'm a local web developer and I'd be happy to send over a quick 
mockup showing how we could modernize your site—no charge, no 
obligation.

Would you be interested in seeing what that could look like?

Best,
[Your Name]
[Your Contact Info]
```

---

**Ready? Run `python agency_bot.py` and watch the magic! ✨**

