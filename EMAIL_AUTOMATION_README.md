# 📧 Email Automation System - Complete Guide

Automated lead generation and outreach system with AI-powered analysis, intelligent email sending, response tracking, and follow-up sequences.

---

## 🎯 What This System Does

### **Complete Pipeline:**
1. **🔍 Lead Research** (`agency_bot.py`) - Finds local businesses with outdated websites
2. **📧 Email Sender** (`email_sender.py`) - Sends personalized initial contact emails
3. **📬 Response Tracker** (`response_tracker.py`) - Monitors inbox for replies
4. **🔄 Follow-Up System** (`follow_up.py`) - Sends automated follow-up sequences

---

## 📋 Files Overview

| File | Purpose |
|------|---------|
| `config_email.py` | **All settings** - Templates, timing, limits |
| `gmail_auth_helper.py` | **Gmail OAuth** - Handles authentication |
| `email_sender.py` | **Initial emails** - Sends first contact |
| `response_tracker.py` | **Track replies** - Monitors inbox |
| `follow_up.py` | **Follow-ups** - Automated sequence |
| `run_all.py` | **Master script** - Runs everything |
| `setup_gmail_api.md` | **Setup guide** - Gmail API instructions |

---

## ⚡ Quick Start

### **Step 1: Install Additional Packages**

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### **Step 2: Set Up Gmail API**

Follow the detailed guide in `setup_gmail_api.md`:
1. Create Google Cloud project
2. Enable Gmail API
3. Download credentials.json
4. Run: `python gmail_auth_helper.py`

**(Takes ~15 minutes, one-time setup)**

### **Step 3: Configure Your Settings**

Edit `config_email.py`:

```python
# Your Information
YOUR_NAME = "John Smith"
YOUR_EMAIL = "john@gmail.com"
YOUR_PHONE = "(555) 123-4567"
YOUR_WEBSITE = "https://yoursite.com"

# Send limits (be conservative!)
MAX_DAILY_SENDS = 50

# Test mode (sends to yourself)
TEST_MODE = True  # Set False when ready
TEST_EMAIL = "your.test@gmail.com"
```

### **Step 4: Customize Email Templates**

In `config_email.py`, edit the templates:

```python
INITIAL_BODY = """Hi,

I was searching for {niche} in {city} and came across your website.

{ai_hook}

I'm a local web developer in {your_city}, and I'd be happy to send 
over a quick mockup showing how we could modernize your site—no 
charge, no obligation.

Would you be open to a brief call this week?

Best,
{your_name}
"""
```

### **Step 5: Test Everything**

```bash
# Test with yourself first
python email_sender.py
```

Check your email - you should receive a test email!

### **Step 6: Go Live**

```python
# In config_email.py, change:
TEST_MODE = False
```

```bash
# Run the full pipeline
python run_all.py
```

---

## 🚀 How To Use

### **Option A: Run Full Pipeline**

```bash
python run_all.py
```

This runs everything in sequence:
1. Find leads
2. Send initial emails
3. Check for responses
4. Send follow-ups

---

### **Option B: Run Components Separately**

```bash
# 1. Find leads (if you need new ones)
python agency_bot.py

# 2. Send initial emails
python email_sender.py

# 3. Check for responses (run hourly)
python response_tracker.py

# 4. Send follow-ups (run daily)
python follow_up.py
```

---

## 📊 Understanding the CSV

### **New Columns Added:**

| Column | What It Means |
|--------|---------------|
| `Email_Sent` | True if initial email sent |
| `Date_Sent` | When initial email was sent |
| `Send_Status` | Success/Failed/Skipped |
| `FollowUp_1_Sent` | Date of first follow-up |
| `FollowUp_2_Sent` | Date of second follow-up |
| `FollowUp_3_Sent` | Date of third follow-up |
| `Response` | YES/NO/MAYBE |
| `Response_Date` | When they replied |
| `Response_Text` | First 100 chars of reply |
| `Status` | Active/Responded/Dead/Unsubscribed |

---

## ⏰ Follow-Up Timing

Default schedule (configure in `config_email.py`):

| Follow-Up | Days After | Action |
|-----------|------------|--------|
| Initial Email | Day 0 | Personalized pitch with AI analysis |
| Follow-Up #1 | Day 3 | "Just following up..." |
| Follow-Up #2 | Day 7 | "Last follow-up..." (with unsubscribe) |
| Mark as Dead | Day 14 | Stop sending (if no response) |

---

## 🎛️ Configuration Options

### **Email Limits (IMPORTANT!)**

```python
# config_email.py
MAX_DAILY_SENDS = 50  # New Gmail: 100-500/day safe limit
DELAY_BETWEEN_SENDS = 10  # Seconds between emails
```

**Gmail Limits:**
- **New accounts**: 100-500 emails/day
- **Established accounts**: 2000 emails/day
- **Always start conservative!**

---

### **Lead Filtering**

```python
# Only send to these tiers
SEND_TO_TIERS = ["HOT", "WARM"]  # Skip COLD

# Skip manual review leads
SKIP_MANUAL_REVIEW = True
```

---

### **Follow-Up Timing**

```python
# config_email.py - FollowUpConfig
FIRST_FOLLOWUP_DAYS = 3   # Day 3
SECOND_FOLLOWUP_DAYS = 7  # Day 7
THIRD_FOLLOWUP_DAYS = 14  # Day 14

MAX_FOLLOWUPS = 2  # Stop after 2 follow-ups (3 total emails)
SKIP_WEEKENDS = True  # Don't send on weekends
```

---

### **Attachments**

```python
ATTACH_SCREENSHOTS = True  # Attach website screenshots
MAX_ATTACHMENT_SIZE_MB = 10  # Max size
```

---

## 📈 Typical Results

### **Sample Campaign:**
- **Leads found**: 50
- **Emails sent**: 45 (5 filtered)
- **Response rate**: 8-15% (4-7 replies)
- **Interested**: 2-4 leads
- **Meetings booked**: 1-2

---

## 🛡️ Safety Features

### **Rate Limiting:**
- ✅ Daily send caps
- ✅ Delays between emails
- ✅ Automatic stopping on rate limits

### **Testing Mode:**
- ✅ Send to yourself first
- ✅ Limit to 3 test leads
- ✅ Verify everything works

### **Error Handling:**
- ✅ Saves progress after each email
- ✅ Graceful failures
- ✅ Detailed logging

### **Unsubscribe Handling:**
- ✅ Detects "unsubscribe" in replies
- ✅ Automatically marks as unsubscribed
- ✅ Never emails them again

---

## 🔧 Automation (Run Daily)

### **Windows Task Scheduler:**

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Lead Gen Bot"
4. Trigger: Daily at 9:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `C:\path\to\run_all.py`
   - Start in: `C:\path\to\Automation`

---

### **Run Manually When Needed:**

```bash
# Daily routine:
python response_tracker.py   # Check responses
python follow_up.py          # Send follow-ups

# Weekly:
python agency_bot.py         # Find new leads
python email_sender.py       # Send to new leads
```

---

## 📊 Monitoring Your Campaigns

### **Check Response Rates:**

```python
import pandas as pd
df = pd.read_csv('leads.csv')

# Overall stats
sent = len(df[df['Email_Sent'] == True])
responses = len(df[df['Response'].notna() & (df['Response'] != '')])
interested = len(df[df['Response'] == 'YES'])

print(f"Sent: {sent}")
print(f"Responses: {responses} ({responses/sent*100:.1f}%)")
print(f"Interested: {interested} ({interested/sent*100:.1f}%)")
```

---

### **Find Hot Leads:**

```python
# Filter for interested prospects
hot = df[df['Response'] == 'YES']
print(hot[['Business_Name', 'Email', 'Response_Text']])
```

---

## ⚠️ Troubleshooting

### **"Gmail API not authenticated"**
**Solution:** Run `python gmail_auth_helper.py` again

---

### **"Daily send limit reached"**
**Solution:** 
- Wait 24 hours
- Reduce `MAX_DAILY_SENDS` in config
- Spread sends over multiple days

---

### **"Emails going to spam"**
**Solutions:**
- Reduce volume (50/day max for new accounts)
- Increase delays (15+ seconds)
- Personalize more (use {business_name})
- Ask recipients to whitelist you
- Build sender reputation over time

---

### **"No responses after 50 emails"**
**Check:**
- Are emails landing in inbox? (Test with friends)
- Is your pitch compelling? (A/B test templates)
- Are you targeting the right audience?
- Is your offer clear and valuable?

---

## 📈 Optimization Tips

### **Improve Response Rates:**

1. **Better Targeting:**
   - Focus on businesses that really need your service
   - Check `Design_Score` - target 1-4 scores

2. **Personalization:**
   - Reference the specific flaw from AI analysis
   - Mention something unique about their business

3. **Timing:**
   - Send Tuesday-Thursday, 9 AM - 3 PM
   - Avoid Mondays and Fridays
   - Skip weekends

4. **Follow-Up:**
   - Most responses come from follow-up #1
   - Always send at least one follow-up

5. **Template Testing:**
   - Try different subject lines
   - A/B test email body
   - Vary your call-to-action

---

## 🔐 Security & Privacy

### **Protect Your Credentials:**

```bash
# Add to .gitignore:
credentials.json
token.json
*.csv
sent_emails_today.txt
```

### **Never Share:**
- `credentials.json` - OAuth client ID
- `token.json` - Your access token
- `leads.csv` - Contains personal data

### **If Compromised:**
- Revoke access in Google Account settings
- Delete OAuth client in Cloud Console
- Create new credentials
- Re-run setup

---

## 📧 Legal Compliance (CAN-SPAM Act)

### **Required by Law:**

✅ **Real "From" address** - Your actual email
✅ **Honest subject line** - No deception
✅ **Physical address** - In your signature
✅ **Unsubscribe option** - In follow-ups
✅ **Honor unsubscribes** - Within 10 days (automated)

### **Best Practices:**

✅ **Relevant** - They operate in your target niche
✅ **Personalized** - Uses their business name and specific issues
✅ **Valuable** - Offering real help, not just selling
✅ **Professional** - Polite, helpful tone
✅ **Limited** - Max 2-3 emails per lead

---

## 🎓 Advanced Usage

### **Multiple Campaigns:**

Run separate campaigns for different niches:

```bash
# Campaign 1: Landscapers
python agency_bot.py  # Edit search_query first
mv leads.csv leads_landscapers.csv

# Campaign 2: Restaurants
python agency_bot.py  # Change search_query
mv leads.csv leads_restaurants.csv
```

---

### **Custom Scheduling:**

```python
# In run_all.py, customize timing:
time.sleep(1800)  # Wait 30 min between steps
```

---

### **Integration with CRM:**

Export CSV to your CRM:
- Airtable
- HubSpot
- Salesforce
- Google Sheets

---

## 📞 Support

### **Common Issues:**
1. Check `setup_gmail_api.md` for setup problems
2. Review error messages in console
3. Check `email_automation.log` if enabled
4. Test in `TEST_MODE` first

### **Need Help?**
- Review Gmail API docs
- Check Google Cloud Console logs
- Test individual components separately

---

## 🚀 Next Steps

1. ✅ Complete Gmail API setup
2. ✅ Configure templates
3. ✅ Test with yourself (`TEST_MODE = True`)
4. ✅ Send to 5-10 real leads
5. ✅ Monitor results
6. ✅ Refine and scale

---

**Good luck with your automated outreach! 💪**

*Remember: Quality > Quantity. Personalized emails to the right people always win.*

