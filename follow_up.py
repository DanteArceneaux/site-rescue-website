"""
Follow-Up Sender - Automated Follow-Up Sequence
Sends follow-up emails to non-responders based on timing rules.
"""

import os
import sys
import time
import base64
import pandas as pd
from datetime import datetime, date, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from googleapiclient.errors import HttpError
from colorama import init, Fore

from gmail_auth_helper import GmailAuthenticator
from config_email import (
    EmailConfig, EmailTemplates, FollowUpConfig,
    CSVColumns, FilePaths, TestConfig, LogConfig
)

# Initialize colorama
init(autoreset=True)


class FollowUpSender:
    """Handles automated follow-up email sequence."""
    
    def __init__(self):
        self.authenticator = GmailAuthenticator()
        self.service = None
        self.emails_sent_today = 0
    
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
            return None
        
        df = pd.read_csv(FilePaths.LEADS_CSV)
        
        # Ensure follow-up columns exist
        for col in [CSVColumns.FOLLOWUP_1_SENT, CSVColumns.FOLLOWUP_2_SENT, CSVColumns.FOLLOWUP_3_SENT]:
            if col not in df.columns:
                df[col] = ''
        
        return df
    
    def is_weekend(self):
        """Check if today is weekend."""
        if FollowUpConfig.SKIP_WEEKENDS:
            return date.today().weekday() >= 5  # 5=Saturday, 6=Sunday
        return False
    
    def parse_date(self, date_str):
        """Parse date string to date object."""
        if pd.isna(date_str) or not date_str:
            return None
        
        try:
            return datetime.strptime(str(date_str), "%Y-%m-%d").date()
        except:
            return None
    
    def days_since(self, date_str):
        """Calculate days since a date."""
        date_obj = self.parse_date(date_str)
        if not date_obj:
            return None
        
        return (date.today() - date_obj).days
    
    def filter_leads_for_followup(self, df, followup_number):
        """Filter leads that need a specific follow-up."""
        # Must have initial email sent
        df_filtered = df[df[CSVColumns.EMAIL_SENT] == True]
        
        # Must have a date sent
        df_filtered = df_filtered[df_filtered[CSVColumns.DATE_SENT].notna()]
        df_filtered = df_filtered[df_filtered[CSVColumns.DATE_SENT] != '']
        
        # Must NOT have responded
        df_filtered = df_filtered[
            (df_filtered[CSVColumns.RESPONSE].isna()) | 
            (df_filtered[CSVColumns.RESPONSE] == '')
        ]
        
        # Must NOT be unsubscribed
        df_filtered = df_filtered[df_filtered[CSVColumns.STATUS] != 'Unsubscribed']
        
        # Check timing and previous follow-ups
        leads_ready = []
        
        for idx, lead in df_filtered.iterrows():
            date_sent = lead[CSVColumns.DATE_SENT]
            days_elapsed = self.days_since(date_sent)
            
            if days_elapsed is None:
                continue
            
            # Check which follow-up to send
            if followup_number == 1:
                # First follow-up
                if days_elapsed >= FollowUpConfig.FIRST_FOLLOWUP_DAYS:
                    # Check if not already sent
                    if pd.isna(lead[CSVColumns.FOLLOWUP_1_SENT]) or not lead[CSVColumns.FOLLOWUP_1_SENT]:
                        leads_ready.append(idx)
            
            elif followup_number == 2:
                # Second follow-up
                if days_elapsed >= FollowUpConfig.SECOND_FOLLOWUP_DAYS:
                    # Must have sent first follow-up
                    if pd.notna(lead[CSVColumns.FOLLOWUP_1_SENT]) and lead[CSVColumns.FOLLOWUP_1_SENT]:
                        # Check if not already sent second
                        if pd.isna(lead[CSVColumns.FOLLOWUP_2_SENT]) or not lead[CSVColumns.FOLLOWUP_2_SENT]:
                            leads_ready.append(idx)
            
            elif followup_number == 3:
                # Third follow-up
                if days_elapsed >= FollowUpConfig.THIRD_FOLLOWUP_DAYS:
                    # Must have sent second follow-up
                    if pd.notna(lead[CSVColumns.FOLLOWUP_2_SENT]) and lead[CSVColumns.FOLLOWUP_2_SENT]:
                        # Check if not already sent third
                        if pd.isna(lead[CSVColumns.FOLLOWUP_3_SENT]) or not lead[CSVColumns.FOLLOWUP_3_SENT]:
                            leads_ready.append(idx)
        
        return df.loc[leads_ready]
    
    def create_followup_message(self, lead, followup_number):
        """Create follow-up email message."""
        business_name = lead[CSVColumns.BUSINESS_NAME]
        to_email = TestConfig.TEST_EMAIL if TestConfig.TEST_MODE else lead[CSVColumns.EMAIL]
        
        # Select template based on follow-up number
        if followup_number == 1:
            subject = EmailTemplates.FOLLOWUP_1_SUBJECT.format(business_name=business_name)
            body = EmailTemplates.FOLLOWUP_1_BODY.format(
                business_name=business_name,
                your_name=EmailConfig.YOUR_NAME,
                your_phone=EmailConfig.YOUR_PHONE
            )
        
        elif followup_number == 2:
            subject = EmailTemplates.FOLLOWUP_2_SUBJECT.format(business_name=business_name)
            body = EmailTemplates.FOLLOWUP_2_BODY.format(
                business_name=business_name,
                your_name=EmailConfig.YOUR_NAME
            )
        
        elif followup_number == 3:
            subject = EmailTemplates.FOLLOWUP_3_SUBJECT.format(business_name=business_name)
            body = EmailTemplates.FOLLOWUP_3_BODY.format(
                business_name=business_name,
                your_name=EmailConfig.YOUR_NAME,
                your_phone=EmailConfig.YOUR_PHONE,
                your_website=EmailConfig.YOUR_WEBSITE
            )
        
        else:
            return None
        
        # Create message
        message = MIMEMultipart()
        message['to'] = to_email
        message['from'] = EmailConfig.YOUR_EMAIL
        message['subject'] = subject
        
        # Add body
        message.attach(MIMEText(body, 'plain'))
        
        # Encode
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        return {'raw': raw_message}
    
    def send_email(self, message_body):
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
                print(f"  {Fore.RED}❌ Rate limit hit! Stopping.")
                return False, "RATE_LIMIT"
            
            return False, error_msg
        
        except Exception as e:
            return False, str(e)
    
    def send_followups(self, df, followup_number):
        """Send a specific follow-up sequence."""
        # Check if weekend
        if self.is_weekend():
            print(f"{Fore.YELLOW}⏸️  Weekend detected - skipping sends")
            return df
        
        # Filter leads
        leads_to_send = self.filter_leads_for_followup(df, followup_number)
        
        if len(leads_to_send) == 0:
            print(f"{Fore.YELLOW}No leads ready for Follow-Up #{followup_number}")
            return df
        
        print(f"\n{Fore.GREEN}📧 {len(leads_to_send)} leads ready for Follow-Up #{followup_number}\n")
        
        # Column name for this follow-up
        followup_col = [
            CSVColumns.FOLLOWUP_1_SENT,
            CSVColumns.FOLLOWUP_2_SENT,
            CSVColumns.FOLLOWUP_3_SENT
        ][followup_number - 1]
        
        success_count = 0
        fail_count = 0
        
        for idx, lead in leads_to_send.iterrows():
            business_name = lead[CSVColumns.BUSINESS_NAME]
            email = TestConfig.TEST_EMAIL if TestConfig.TEST_MODE else lead[CSVColumns.EMAIL]
            
            print(f"{Fore.CYAN}{'─'*70}")
            print(f"{Fore.CYAN}📤 Follow-Up #{followup_number} to: {business_name}")
            print(f"{Fore.CYAN}📧 Email: {email}")
            
            try:
                # Create message
                message = self.create_followup_message(lead, followup_number)
                
                if not message:
                    print(f"{Fore.RED}  ❌ Failed to create message")
                    fail_count += 1
                    continue
                
                # Send
                success, result = self.send_email(message)
                
                if success:
                    print(f"{Fore.GREEN}  ✅ Sent successfully! (ID: {result})")
                    
                    # Update CSV
                    df.loc[idx, followup_col] = datetime.now().strftime("%Y-%m-%d")
                    
                    # Mark as dead after final follow-up
                    if followup_number >= FollowUpConfig.MAX_FOLLOWUPS:
                        df.loc[idx, CSVColumns.STATUS] = "Dead"
                        print(f"{Fore.YELLOW}  💀 Marked as Dead (no response after {followup_number} follow-ups)")
                    
                    success_count += 1
                    self.emails_sent_today += 1
                
                else:
                    if result == "RATE_LIMIT":
                        fail_count += 1
                        break
                    else:
                        print(f"{Fore.RED}  ❌ Failed: {result}")
                        fail_count += 1
                
                # Save progress
                df.to_csv(FilePaths.LEADS_CSV, index=False)
                
                # Delay between sends
                if success and idx < leads_to_send.index[-1]:
                    delay = EmailConfig.DELAY_BETWEEN_SENDS
                    print(f"{Fore.CYAN}  ⏳ Waiting {delay} seconds...")
                    time.sleep(delay)
            
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}⚠️  Interrupted by user. Progress saved.")
                df.to_csv(FilePaths.LEADS_CSV, index=False)
                break
            
            except Exception as e:
                print(f"{Fore.RED}  ❌ Unexpected error: {e}")
                fail_count += 1
                df.to_csv(FilePaths.LEADS_CSV, index=False)
        
        # Summary
        print(f"\n{Fore.CYAN}Follow-Up #{followup_number} Summary:")
        print(f"{Fore.GREEN}  ✅ Sent: {success_count}")
        print(f"{Fore.RED}  ❌ Failed: {fail_count}")
        
        return df


def main():
    """Main entry point."""
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}🔄 Follow-Up Sender - Automated Sequence")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    sender = FollowUpSender()
    
    # Connect to Gmail
    if not sender.connect():
        print(f"\n{Fore.RED}❌ Failed to connect to Gmail API")
        print(f"{Fore.YELLOW}Run: python gmail_auth_helper.py")
        return
    
    # Load leads
    df = sender.load_leads()
    if df is None:
        return
    
    # Send each follow-up sequence
    for followup_num in range(1, FollowUpConfig.MAX_FOLLOWUPS + 1):
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}Processing Follow-Up #{followup_num}")
        print(f"{Fore.CYAN}{'='*70}")
        
        df = sender.send_followups(df, followup_num)
    
    # Final save
    df.to_csv(FilePaths.LEADS_CSV, index=False)
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}📊 FOLLOW-UP SESSION SUMMARY")
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.GREEN}✅ Total follow-ups sent: {sender.emails_sent_today}")
    print(f"{Fore.GREEN}✅ Results saved to: {FilePaths.LEADS_CSV}\n")


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

