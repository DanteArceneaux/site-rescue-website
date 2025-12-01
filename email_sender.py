"""
Email Sender - Automated Initial Contact Emails
Reads leads.csv and sends personalized emails to qualified leads.
"""

import os
import sys
import time
import base64
import pandas as pd
from datetime import datetime, date
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from googleapiclient.errors import HttpError
from colorama import init, Fore, Style

from gmail_auth_helper import GmailAuthenticator
from config_email import (
    EmailConfig, EmailTemplates, CSVColumns, FilePaths,
    TestConfig, LogConfig, get_niche_from_query, get_city_from_query
)

# Initialize colorama
init(autoreset=True)


class EmailSender:
    """Handles sending initial contact emails to leads."""
    
    def __init__(self):
        self.authenticator = GmailAuthenticator()
        self.service = None
        self.emails_sent_today = 0
        self.load_daily_count()
    
    def load_daily_count(self):
        """Load today's send count from file."""
        if os.path.exists(FilePaths.SENT_TRACKER):
            try:
                with open(FilePaths.SENT_TRACKER, 'r') as f:
                    data = f.read().strip().split('|')
                    if len(data) == 2:
                        saved_date, count = data
                        if saved_date == str(date.today()):
                            self.emails_sent_today = int(count)
                        else:
                            # New day, reset counter
                            self.emails_sent_today = 0
            except:
                self.emails_sent_today = 0
    
    def save_daily_count(self):
        """Save today's send count to file."""
        with open(FilePaths.SENT_TRACKER, 'w') as f:
            f.write(f"{date.today()}|{self.emails_sent_today}")
    
    def connect(self):
        """Connect to Gmail API."""
        print(f"{Fore.CYAN}🔐 Connecting to Gmail API...")
        self.service = self.authenticator.get_service()
        
        if self.service:
            print(f"{Fore.GREEN}✅ Connected successfully!")
            return True
        else:
            print(f"{Fore.RED}❌ Failed to connect to Gmail API")
            return False
    
    def load_leads(self):
        """Load leads from CSV."""
        if not os.path.exists(FilePaths.LEADS_CSV):
            print(f"{Fore.RED}❌ {FilePaths.LEADS_CSV} not found!")
            print(f"{Fore.YELLOW}Run agency_bot.py first to generate leads.")
            return None
        
        df = pd.read_csv(FilePaths.LEADS_CSV)
        
        # Add new columns if they don't exist
        new_columns = {
            CSVColumns.EMAIL_SENT: False,
            CSVColumns.DATE_SENT: '',
            CSVColumns.SEND_STATUS: '',
            CSVColumns.FOLLOWUP_1_SENT: '',
            CSVColumns.FOLLOWUP_2_SENT: '',
            CSVColumns.FOLLOWUP_3_SENT: '',
            CSVColumns.RESPONSE: '',
            CSVColumns.RESPONSE_DATE: '',
            CSVColumns.RESPONSE_TEXT: '',
            CSVColumns.STATUS: 'Active'
        }
        
        for col, default_val in new_columns.items():
            if col not in df.columns:
                df[col] = default_val
        
        return df
    
    def filter_leads_to_send(self, df):
        """Filter leads that should receive emails."""
        # Filter by tier
        df_filtered = df[df[CSVColumns.TIER].isin(EmailConfig.SEND_TO_TIERS)]
        
        # Skip if already sent
        df_filtered = df_filtered[df_filtered[CSVColumns.EMAIL_SENT] != True]
        
        # Must have email
        df_filtered = df_filtered[df_filtered[CSVColumns.EMAIL].notna()]
        df_filtered = df_filtered[df_filtered[CSVColumns.EMAIL] != '']
        
        # Skip if unsubscribed
        df_filtered = df_filtered[df_filtered[CSVColumns.STATUS] != 'Unsubscribed']
        
        print(f"\n{Fore.CYAN}📊 Lead Statistics:")
        print(f"  Total leads in CSV: {len(df)}")
        print(f"  Qualified to send: {len(df_filtered)}")
        print(f"  Already sent: {len(df[df[CSVColumns.EMAIL_SENT] == True])}")
        print(f"  Emails sent today: {self.emails_sent_today}/{EmailConfig.MAX_DAILY_SENDS}")
        
        # Apply daily limit
        remaining_today = EmailConfig.MAX_DAILY_SENDS - self.emails_sent_today
        if remaining_today <= 0:
            print(f"{Fore.YELLOW}⚠️  Daily send limit reached!")
            return df_filtered.iloc[0:0]  # Return empty dataframe
        
        df_filtered = df_filtered.head(remaining_today)
        
        if TestConfig.TEST_MODE:
            print(f"\n{Fore.YELLOW}⚠️  TEST MODE ENABLED")
            print(f"  Limiting to {TestConfig.TEST_LEAD_LIMIT} leads")
            print(f"  All emails will go to: {TestConfig.TEST_EMAIL}")
            df_filtered = df_filtered.head(TestConfig.TEST_LEAD_LIMIT)
        
        return df_filtered
    
    def create_email_message(self, lead):
        """Create email message for a lead."""
        # Get lead data
        business_name = lead[CSVColumns.BUSINESS_NAME]
        to_email = TestConfig.TEST_EMAIL if TestConfig.TEST_MODE else lead[CSVColumns.EMAIL]
        ai_hook = lead[CSVColumns.DRAFT_HOOK]
        
        # Extract niche and city (you can customize this)
        niche = "local businesses"  # Default
        city = EmailConfig.YOUR_CITY
        
        # Format subject
        subject = EmailTemplates.INITIAL_SUBJECT.format(
            business_name=business_name
        )
        
        # Format body
        body = EmailTemplates.INITIAL_BODY.format(
            business_name=business_name,
            niche=niche,
            city=city,
            ai_hook=ai_hook,
            your_name=EmailConfig.YOUR_NAME,
            your_phone=EmailConfig.YOUR_PHONE,
            your_website=EmailConfig.YOUR_WEBSITE,
            your_city=EmailConfig.YOUR_CITY
        )
        
        # Create message
        message = MIMEMultipart()
        message['to'] = to_email
        message['from'] = EmailConfig.YOUR_EMAIL
        message['subject'] = subject
        
        # Add body
        message.attach(MIMEText(body, 'plain'))
        
        # Attach screenshot if enabled
        if EmailConfig.ATTACH_SCREENSHOTS and pd.notna(lead[CSVColumns.SCREENSHOT]):
            screenshot_path = lead[CSVColumns.SCREENSHOT]
            if os.path.exists(screenshot_path):
                try:
                    # Check file size
                    file_size_mb = os.path.getsize(screenshot_path) / (1024 * 1024)
                    
                    if file_size_mb <= EmailConfig.MAX_ATTACHMENT_SIZE_MB:
                        with open(screenshot_path, 'rb') as f:
                            img_data = f.read()
                        
                        image = MIMEImage(img_data, name=os.path.basename(screenshot_path))
                        message.attach(image)
                    else:
                        print(f"  {Fore.YELLOW}⚠️  Screenshot too large ({file_size_mb:.1f}MB), skipping attachment")
                
                except Exception as e:
                    print(f"  {Fore.YELLOW}⚠️  Failed to attach screenshot: {e}")
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        return {'raw': raw_message}
    
    def send_email(self, message_body, lead_info):
        """Send email via Gmail API."""
        try:
            message = self.service.users().messages().send(
                userId='me',
                body=message_body
            ).execute()
            
            return True, message['id']
        
        except HttpError as error:
            error_msg = str(error)
            
            if 'quota' in error_msg.lower() or 'rate' in error_msg.lower():
                print(f"  {Fore.RED}❌ Rate limit hit! Stopping for today.")
                return False, "RATE_LIMIT"
            
            return False, error_msg
        
        except Exception as e:
            return False, str(e)
    
    def process_leads(self):
        """Main processing loop."""
        # Load leads
        df = self.load_leads()
        if df is None:
            return
        
        # Filter leads to send
        leads_to_send = self.filter_leads_to_send(df)
        
        if len(leads_to_send) == 0:
            print(f"\n{Fore.YELLOW}No leads to send emails to.")
            return
        
        print(f"\n{Fore.GREEN}📧 Ready to send {len(leads_to_send)} emails\n")
        
        if not TestConfig.TEST_MODE:
            confirm = input(f"{Fore.YELLOW}Continue? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print(f"{Fore.YELLOW}Cancelled by user.")
                return
        
        # Process each lead
        success_count = 0
        fail_count = 0
        
        for idx, lead in leads_to_send.iterrows():
            business_name = lead[CSVColumns.BUSINESS_NAME]
            email = TestConfig.TEST_EMAIL if TestConfig.TEST_MODE else lead[CSVColumns.EMAIL]
            
            print(f"{Fore.CYAN}{'─'*70}")
            print(f"{Fore.CYAN}📤 Sending to: {business_name}")
            print(f"{Fore.CYAN}📧 Email: {email}")
            
            try:
                # Create message
                message = self.create_email_message(lead)
                
                # Send
                success, result = self.send_email(message, lead)
                
                if success:
                    print(f"{Fore.GREEN}  ✅ Sent successfully! (ID: {result})")
                    
                    # Update CSV
                    df.loc[idx, CSVColumns.EMAIL_SENT] = True
                    df.loc[idx, CSVColumns.DATE_SENT] = datetime.now().strftime("%Y-%m-%d")
                    df.loc[idx, CSVColumns.SEND_STATUS] = "Success"
                    
                    success_count += 1
                    self.emails_sent_today += 1
                    self.save_daily_count()
                
                else:
                    if result == "RATE_LIMIT":
                        # Stop immediately
                        df.loc[idx, CSVColumns.SEND_STATUS] = "Rate Limited"
                        fail_count += 1
                        break
                    else:
                        print(f"{Fore.RED}  ❌ Failed: {result}")
                        df.loc[idx, CSVColumns.SEND_STATUS] = f"Failed: {result[:50]}"
                        fail_count += 1
                
                # Save progress after each email
                df.to_csv(FilePaths.LEADS_CSV, index=False)
                
                # Rate limiting delay
                if success and idx < len(leads_to_send) - 1:
                    delay = EmailConfig.DELAY_BETWEEN_SENDS
                    print(f"{Fore.CYAN}  ⏳ Waiting {delay} seconds...")
                    time.sleep(delay)
            
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}⚠️  Interrupted by user. Progress saved.")
                df.to_csv(FilePaths.LEADS_CSV, index=False)
                break
            
            except Exception as e:
                print(f"{Fore.RED}  ❌ Unexpected error: {e}")
                df.loc[idx, CSVColumns.SEND_STATUS] = f"Error: {str(e)[:50]}"
                fail_count += 1
                # Save and continue
                df.to_csv(FilePaths.LEADS_CSV, index=False)
        
        # Final save
        df.to_csv(FilePaths.LEADS_CSV, index=False)
        
        # Summary
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}📊 SENDING SUMMARY")
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.GREEN}✅ Successfully sent: {success_count}")
        print(f"{Fore.RED}❌ Failed: {fail_count}")
        print(f"{Fore.CYAN}📧 Total sent today: {self.emails_sent_today}/{EmailConfig.MAX_DAILY_SENDS}")
        print(f"{Fore.GREEN}✅ Progress saved to: {FilePaths.LEADS_CSV}\n")


def main():
    """Main entry point."""
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}📧 Email Sender - Initial Contact")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    sender = EmailSender()
    
    # Connect to Gmail
    if not sender.connect():
        print(f"\n{Fore.RED}❌ Failed to connect to Gmail API")
        print(f"{Fore.YELLOW}Run: python gmail_auth_helper.py")
        return
    
    # Process leads
    sender.process_leads()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

