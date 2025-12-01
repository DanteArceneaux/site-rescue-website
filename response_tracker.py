"""
Response Tracker - Monitor Inbox for Replies
Checks Gmail inbox and updates leads.csv when prospects respond.
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta
from colorama import init, Fore

from gmail_auth_helper import GmailAuthenticator
from config_email import (
    CSVColumns, FilePaths, ResponseConfig, LogConfig
)

# Initialize colorama
init(autoreset=True)


class ResponseTracker:
    """Tracks responses from leads in Gmail inbox."""
    
    def __init__(self):
        self.authenticator = GmailAuthenticator()
        self.service = None
        self.lead_emails = {}  # email -> index mapping
    
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
        
        # Ensure response columns exist
        if CSVColumns.RESPONSE not in df.columns:
            df[CSVColumns.RESPONSE] = ''
        if CSVColumns.RESPONSE_DATE not in df.columns:
            df[CSVColumns.RESPONSE_DATE] = ''
        if CSVColumns.RESPONSE_TEXT not in df.columns:
            df[CSVColumns.RESPONSE_TEXT] = ''
        
        # Build email index for fast lookup
        for idx, row in df.iterrows():
            if pd.notna(row[CSVColumns.EMAIL]) and row[CSVColumns.EMAIL]:
                email = row[CSVColumns.EMAIL].lower().strip()
                self.lead_emails[email] = idx
        
        print(f"{Fore.CYAN}📊 Loaded {len(df)} leads ({len(self.lead_emails)} with emails)")
        
        return df
    
    def get_recent_messages(self, days_back=7):
        """Get messages from inbox from last N days."""
        try:
            # Calculate date for query
            after_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')
            
            # Query inbox
            query = f'in:inbox after:{after_date}'
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=500  # Adjust if needed
            ).execute()
            
            messages = results.get('messages', [])
            
            print(f"{Fore.CYAN}📬 Found {len(messages)} messages in last {days_back} days")
            
            return messages
        
        except Exception as e:
            print(f"{Fore.RED}❌ Error fetching messages: {e}")
            return []
    
    def get_message_details(self, message_id):
        """Get full message details."""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            return message
        
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Error fetching message {message_id}: {e}")
            return None
    
    def extract_email_from_header(self, headers, header_name):
        """Extract email address from message headers."""
        for header in headers:
            if header['name'].lower() == header_name.lower():
                value = header['value']
                # Extract email from "Name <email@domain.com>" format
                if '<' in value and '>' in value:
                    return value.split('<')[1].split('>')[0].lower().strip()
                return value.lower().strip()
        return None
    
    def get_message_body(self, payload):
        """Extract message body text."""
        try:
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            import base64
                            return base64.urlsafe_b64decode(
                                part['body']['data']
                            ).decode('utf-8', errors='ignore')
            
            elif 'body' in payload and 'data' in payload['body']:
                import base64
                return base64.urlsafe_b64decode(
                    payload['body']['data']
                ).decode('utf-8', errors='ignore')
            
            return ""
        
        except Exception as e:
            return ""
    
    def classify_response(self, body_text):
        """Classify response as positive/negative/neutral."""
        if not body_text:
            return "MAYBE"
        
        body_lower = body_text.lower()
        
        # Check for auto-replies/bounces (ignore these)
        for keyword in ResponseConfig.IGNORE_KEYWORDS:
            if keyword in body_lower:
                return "IGNORE"
        
        # Check for positive response
        positive_score = sum(1 for keyword in ResponseConfig.POSITIVE_KEYWORDS 
                            if keyword in body_lower)
        
        # Check for negative response
        negative_score = sum(1 for keyword in ResponseConfig.NEGATIVE_KEYWORDS 
                            if keyword in body_lower)
        
        if positive_score > negative_score:
            return "YES"
        elif negative_score > positive_score:
            return "NO"
        else:
            return "MAYBE"
    
    def process_responses(self, df):
        """Check inbox and update responses."""
        # Get recent messages
        messages = self.get_recent_messages(days_back=14)  # Check last 2 weeks
        
        if not messages:
            print(f"{Fore.YELLOW}No messages to process.")
            return df
        
        responses_found = 0
        new_responses = 0
        
        print(f"\n{Fore.CYAN}🔍 Checking messages for responses...\n")
        
        for msg in messages:
            try:
                # Get message details
                message = self.get_message_details(msg['id'])
                
                if not message:
                    continue
                
                headers = message['payload']['headers']
                
                # Get sender email
                from_email = self.extract_email_from_header(headers, 'From')
                
                if not from_email:
                    continue
                
                # Check if this is from a lead
                if from_email not in self.lead_emails:
                    continue
                
                lead_idx = self.lead_emails[from_email]
                
                # Skip if we already recorded a response
                if pd.notna(df.loc[lead_idx, CSVColumns.RESPONSE]) and \
                   df.loc[lead_idx, CSVColumns.RESPONSE]:
                    responses_found += 1
                    continue
                
                # Get message body
                body_text = self.get_message_body(message['payload'])
                
                # Classify response
                response_type = self.classify_response(body_text)
                
                # Skip auto-replies
                if response_type == "IGNORE":
                    continue
                
                # Record response
                business_name = df.loc[lead_idx, CSVColumns.BUSINESS_NAME]
                
                print(f"{Fore.GREEN}✉️  Response from: {business_name}")
                print(f"   Email: {from_email}")
                print(f"   Type: {response_type}")
                print(f"   Preview: {body_text[:80]}...")
                print()
                
                # Update CSV
                df.loc[lead_idx, CSVColumns.RESPONSE] = response_type
                df.loc[lead_idx, CSVColumns.RESPONSE_DATE] = datetime.now().strftime("%Y-%m-%d")
                df.loc[lead_idx, CSVColumns.RESPONSE_TEXT] = body_text[:100]  # First 100 chars
                
                # Update status
                if response_type == "YES":
                    df.loc[lead_idx, CSVColumns.STATUS] = "Responded-Interested"
                elif response_type == "NO":
                    df.loc[lead_idx, CSVColumns.STATUS] = "Responded-NotInterested"
                    # Check for unsubscribe
                    if 'unsubscribe' in body_text.lower():
                        df.loc[lead_idx, CSVColumns.STATUS] = "Unsubscribed"
                else:
                    df.loc[lead_idx, CSVColumns.STATUS] = "Responded-Neutral"
                
                new_responses += 1
            
            except Exception as e:
                if LogConfig.LOG_TO_CONSOLE:
                    print(f"{Fore.YELLOW}⚠️  Error processing message: {e}")
                continue
        
        # Summary
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}📊 RESPONSE TRACKING SUMMARY")
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.GREEN}✉️  New responses: {new_responses}")
        print(f"{Fore.CYAN}📧 Total responses tracked: {responses_found + new_responses}")
        
        # Breakdown by type
        if new_responses > 0:
            yes_count = len(df[df[CSVColumns.RESPONSE] == "YES"])
            no_count = len(df[df[CSVColumns.RESPONSE] == "NO"])
            maybe_count = len(df[df[CSVColumns.RESPONSE] == "MAYBE"])
            
            print(f"\n{Fore.CYAN}Response Breakdown:")
            print(f"{Fore.GREEN}  ✅ Interested (YES): {yes_count}")
            print(f"{Fore.RED}  ❌ Not Interested (NO): {no_count}")
            print(f"{Fore.YELLOW}  🤔 Neutral (MAYBE): {maybe_count}")
        
        print(f"\n{Fore.GREEN}✅ Results saved to: {FilePaths.LEADS_CSV}\n")
        
        return df


def main():
    """Main entry point."""
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}📬 Response Tracker - Monitor Inbox")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    tracker = ResponseTracker()
    
    # Connect to Gmail
    if not tracker.connect():
        print(f"\n{Fore.RED}❌ Failed to connect to Gmail API")
        print(f"{Fore.YELLOW}Run: python gmail_auth_helper.py")
        return
    
    # Load leads
    df = tracker.load_leads()
    if df is None:
        return
    
    # Process responses
    df_updated = tracker.process_responses(df)
    
    # Save
    df_updated.to_csv(FilePaths.LEADS_CSV, index=False)


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

