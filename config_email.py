"""
Email Automation Configuration
Customize all settings, templates, and timing here.
"""

import os

# ============================================================================
# EMAIL SETTINGS
# ============================================================================

class EmailConfig:
    """Email account and sending configuration."""
    
    # Your Information
    YOUR_NAME = "Dante Arceneaux"
    YOUR_EMAIL = "siterescue205@gmail.com"
    YOUR_PHONE = "253-545-1034"
    YOUR_WEBSITE = "https://siterescue.com"  # TODO: Update when you have a website
    YOUR_CITY = "Seattle, Washington"
    
    # Gmail API Credentials
    CREDENTIALS_FILE = "credentials.json"  # Download from Google Cloud Console
    TOKEN_FILE = "token.json"  # Auto-generated after first auth
    
    # Sending Limits (Be Conservative!)
    MAX_DAILY_SENDS = 50  # Don't exceed 100 for new Gmail accounts
    DELAY_BETWEEN_SENDS = 10  # Seconds between each email
    
    # Attachments
    ATTACH_SCREENSHOTS = True  # Attach website screenshots to emails
    MAX_ATTACHMENT_SIZE_MB = 10  # Gmail limit is 25MB, we use 10MB to be safe
    
    # Lead Filtering
    SEND_TO_TIERS = ["HOT", "WARM"]  # Only send to these tier levels
    SKIP_MANUAL_REVIEW = True  # Don't send to MANUAL_REVIEW tier


# ============================================================================
# FOLLOW-UP TIMING
# ============================================================================

class FollowUpConfig:
    """Follow-up sequence timing (in days)."""
    
    FIRST_FOLLOWUP_DAYS = 3   # Send first follow-up after 3 days
    SECOND_FOLLOWUP_DAYS = 7  # Send second follow-up after 7 days
    THIRD_FOLLOWUP_DAYS = 14  # Final follow-up after 14 days
    
    # Stop sending after this many follow-ups
    MAX_FOLLOWUPS = 2  # Set to 2 for gentle approach (3 total emails)
    
    # Skip weekends? (Professional practice)
    SKIP_WEEKENDS = True  # Don't send on Saturday/Sunday


# ============================================================================
# EMAIL TEMPLATES
# ============================================================================

class EmailTemplates:
    """All email templates with variable placeholders."""
    
    # ---------------------------------------------------------------------------
    # INITIAL CONTACT EMAIL
    # ---------------------------------------------------------------------------
    
    INITIAL_SUBJECT = "Quick question about {business_name}"
    
    INITIAL_BODY = """Hi,

I was searching for {niche} in {city} and came across your website.

{ai_hook}

I'm a local web developer in {your_city}, and I specialize in affordable website redesigns for small businesses—just $300 for a complete mobile-friendly redesign with 2 rounds of revisions.

Would you be open to a brief call this week? I'd be happy to send over a free mockup first.

Best,
{your_name}
{your_phone}
{your_website}

P.S. I've attached a screenshot of your current site for reference."""
    
    # ---------------------------------------------------------------------------
    # FOLLOW-UP #1 (Day 3)
    # ---------------------------------------------------------------------------
    
    FOLLOWUP_1_SUBJECT = "Re: Quick question about {business_name}"
    
    FOLLOWUP_1_BODY = """Hi again,

Just wanted to follow up on my email from a few days ago about your website.

I took another look at your site and have a few specific ideas for how we could improve the mobile experience and make it easier for customers to contact you.

Would you like me to send over a quick mockup? It only takes 2 minutes to review.

No pressure—just thought it might be helpful!

Best,
{your_name}
{your_phone}"""
    
    # ---------------------------------------------------------------------------
    # FOLLOW-UP #2 (Day 7)
    # ---------------------------------------------------------------------------
    
    FOLLOWUP_2_SUBJECT = "Last follow-up - {business_name}"
    
    FOLLOWUP_2_BODY = """Hi,

I know you're busy, so I'll keep this short.

If you're interested in seeing how we could update your website to be more mobile-friendly and convert more visitors into customers, just reply "YES" and I'll send over a free mockup.

Otherwise, no worries—I'll stop following up after this.

Best,
{your_name}

---
If you'd like me to stop contacting you, just reply "UNSUBSCRIBE" and I'll remove you from my list immediately."""
    
    # ---------------------------------------------------------------------------
    # FOLLOW-UP #3 (Day 14) - Final
    # ---------------------------------------------------------------------------
    
    FOLLOWUP_3_SUBJECT = "Final note - {business_name}"
    
    FOLLOWUP_3_BODY = """Hi,

This is my final follow-up. I completely understand if now isn't the right time for a website update.

If you ever want to revisit this in the future, feel free to reach out. My contact info is below.

Wishing you and {business_name} continued success!

Best,
{your_name}
{your_phone}
{your_website}

---
To unsubscribe from future emails, reply "UNSUBSCRIBE"."""


# ============================================================================
# RESPONSE DETECTION
# ============================================================================

class ResponseConfig:
    """Keywords for detecting positive/negative responses."""
    
    # Positive Response Keywords
    POSITIVE_KEYWORDS = [
        'yes', 'interested', 'sounds good', 'tell me more', 'send it',
        'sure', 'okay', 'ok', 'absolutely', 'love to', 'would like',
        'go ahead', 'please send', 'let\'s talk', 'schedule', 'call me'
    ]
    
    # Negative Response Keywords
    NEGATIVE_KEYWORDS = [
        'no thanks', 'not interested', 'no thank you', 'unsubscribe',
        'remove me', 'stop emailing', 'don\'t contact', 'not now',
        'maybe later', 'in the future'
    ]
    
    # Out-of-Office / Bounce Detection
    IGNORE_KEYWORDS = [
        'out of office', 'away from', 'automatic reply', 'auto-reply',
        'vacation', 'delivery failed', 'undeliverable', 'mailer-daemon'
    ]


# ============================================================================
# CSV COLUMN NAMES
# ============================================================================

class CSVColumns:
    """Column names for tracking in leads.csv."""
    
    # Original columns from agency_bot.py
    BUSINESS_NAME = "Business_Name"
    URL = "URL"
    TIER = "Tier"
    EMAIL = "Email"
    CONTACT_PAGE = "Contact_Page"
    DESIGN_SCORE = "Design_Score"
    IS_OUTDATED = "Is_Outdated"
    SPECIFIC_FLAWS = "Specific_Flaws"
    DRAFT_HOOK = "Draft_Hook"
    SCREENSHOT = "Screenshot"
    
    # New tracking columns
    EMAIL_SENT = "Email_Sent"
    DATE_SENT = "Date_Sent"
    SEND_STATUS = "Send_Status"
    
    FOLLOWUP_1_SENT = "FollowUp_1_Sent"
    FOLLOWUP_2_SENT = "FollowUp_2_Sent"
    FOLLOWUP_3_SENT = "FollowUp_3_Sent"
    
    RESPONSE = "Response"  # YES/NO/MAYBE
    RESPONSE_DATE = "Response_Date"
    RESPONSE_TEXT = "Response_Text"  # First 100 chars of reply
    
    STATUS = "Status"  # Active/Responded/Dead/Unsubscribed


# ============================================================================
# FILE PATHS
# ============================================================================

class FilePaths:
    """File and directory paths."""
    
    LEADS_CSV = "leads.csv"
    SCREENSHOT_DIR = "scans"
    LOG_FILE = "email_automation.log"
    SENT_TRACKER = "sent_emails_today.txt"  # Track daily send count


# ============================================================================
# LOGGING
# ============================================================================

class LogConfig:
    """Logging configuration."""
    
    ENABLE_LOGGING = True
    LOG_TO_FILE = True
    LOG_TO_CONSOLE = True
    
    # Log levels: DEBUG, INFO, WARNING, ERROR
    LOG_LEVEL = "DEBUG"  # Maximum verbosity!


# ============================================================================
# TESTING MODE
# ============================================================================

class TestConfig:
    """Test mode to avoid sending to real leads."""
    
    # IMPORTANT: Set to True when testing!
    TEST_MODE = True
    
    # In test mode, all emails go here instead:
    TEST_EMAIL = "siterescue205@gmail.com"  # Your email for testing
    
    # Only process this many leads in test mode
    TEST_LEAD_LIMIT = 2  # Small number so you can watch closely


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_signature():
    """Generate email signature."""
    return f"""
{EmailConfig.YOUR_NAME}
{EmailConfig.YOUR_PHONE}
{EmailConfig.YOUR_WEBSITE}
"""


def get_niche_from_query(search_query):
    """Extract niche from search query.
    
    Example: "Landscapers in Austin Texas" -> "Landscapers"
    """
    if " in " in search_query:
        return search_query.split(" in ")[0].strip()
    return "local businesses"


def get_city_from_query(search_query):
    """Extract city from search query.
    
    Example: "Landscapers in Austin Texas" -> "Austin"
    """
    if " in " in search_query:
        city_part = search_query.split(" in ")[1].strip()
        # Take first word as city
        return city_part.split()[0] if city_part else "your area"
    return "your area"

