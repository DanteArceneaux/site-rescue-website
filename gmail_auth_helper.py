"""
Gmail API Authentication Helper
Handles OAuth2 flow and token management.
"""

import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config_email import EmailConfig, LogConfig

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]


class GmailAuthenticator:
    """Handles Gmail API authentication and service creation."""
    
    def __init__(self):
        self.creds = None
        self.service = None
    
    def authenticate(self):
        """
        Authenticate with Gmail API using OAuth2.
        Opens browser on first run for authorization.
        """
        # Check if we have saved credentials
        if os.path.exists(EmailConfig.TOKEN_FILE):
            if LogConfig.LOG_TO_CONSOLE:
                print("📁 Loading saved credentials...")
            
            with open(EmailConfig.TOKEN_FILE, 'rb') as token:
                self.creds = pickle.load(token)
        
        # If credentials are invalid or don't exist, get new ones
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                if LogConfig.LOG_TO_CONSOLE:
                    print("🔄 Refreshing expired credentials...")
                
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"❌ Failed to refresh token: {e}")
                    print("🔑 Starting new authentication flow...")
                    self.creds = self._get_new_credentials()
            else:
                if LogConfig.LOG_TO_CONSOLE:
                    print("🔑 Starting OAuth2 authentication flow...")
                
                self.creds = self._get_new_credentials()
            
            # Save credentials for future use
            with open(EmailConfig.TOKEN_FILE, 'wb') as token:
                pickle.dump(self.creds, token)
            
            if LogConfig.LOG_TO_CONSOLE:
                print("✅ Credentials saved!")
        
        return self.creds
    
    def _get_new_credentials(self):
        """Get new credentials via OAuth2 flow."""
        if not os.path.exists(EmailConfig.CREDENTIALS_FILE):
            print(f"\n❌ ERROR: {EmailConfig.CREDENTIALS_FILE} not found!")
            print("\n📋 To fix this:")
            print("1. Go to: https://console.cloud.google.com/")
            print("2. Create a new project (or select existing)")
            print("3. Enable Gmail API")
            print("4. Create OAuth 2.0 credentials (Desktop app)")
            print(f"5. Download as '{EmailConfig.CREDENTIALS_FILE}'")
            print("6. Place it in this directory\n")
            print("See setup_gmail_api.md for detailed instructions.")
            raise FileNotFoundError(f"{EmailConfig.CREDENTIALS_FILE} not found")
        
        flow = InstalledAppFlow.from_client_secrets_file(
            EmailConfig.CREDENTIALS_FILE, 
            SCOPES
        )
        
        creds = flow.run_local_server(port=0)
        
        return creds
    
    def get_service(self):
        """Get Gmail API service object."""
        if not self.creds:
            self.authenticate()
        
        try:
            self.service = build('gmail', 'v1', credentials=self.creds)
            return self.service
        except HttpError as error:
            print(f'❌ An error occurred: {error}')
            return None
    
    def test_connection(self):
        """Test Gmail API connection."""
        try:
            service = self.get_service()
            
            # Try to get user profile (lightweight test)
            profile = service.users().getProfile(userId='me').execute()
            
            print(f"✅ Successfully connected to Gmail API!")
            print(f"📧 Email: {profile.get('emailAddress')}")
            print(f"📊 Total messages: {profile.get('messagesTotal')}")
            
            return True
        
        except HttpError as error:
            print(f'❌ Connection test failed: {error}')
            return False
        
        except Exception as e:
            print(f'❌ Unexpected error: {e}')
            return False


def setup_gmail_api():
    """
    Interactive setup wizard for Gmail API.
    Run this first before using the email automation.
    """
    print("=" * 70)
    print("🔧 Gmail API Setup Wizard")
    print("=" * 70)
    print()
    
    # Check for credentials file
    if not os.path.exists(EmailConfig.CREDENTIALS_FILE):
        print(f"❌ {EmailConfig.CREDENTIALS_FILE} not found!")
        print()
        print("📋 Setup Steps:")
        print()
        print("1. Go to Google Cloud Console:")
        print("   https://console.cloud.google.com/")
        print()
        print("2. Create a new project (or select existing)")
        print()
        print("3. Enable Gmail API:")
        print("   - Go to 'APIs & Services' > 'Library'")
        print("   - Search for 'Gmail API'")
        print("   - Click 'Enable'")
        print()
        print("4. Create credentials:")
        print("   - Go to 'APIs & Services' > 'Credentials'")
        print("   - Click '+ CREATE CREDENTIALS'")
        print("   - Choose 'OAuth client ID'")
        print("   - Application type: 'Desktop app'")
        print("   - Name it 'Lead Gen Bot'")
        print("   - Click 'Create'")
        print()
        print("5. Download credentials:")
        print("   - Click the download icon next to your OAuth client")
        print(f"   - Save as '{EmailConfig.CREDENTIALS_FILE}'")
        print(f"   - Place it in: {os.getcwd()}")
        print()
        print("6. Run this setup again")
        print()
        return False
    
    print(f"✅ Found {EmailConfig.CREDENTIALS_FILE}")
    print()
    print("🔑 Starting OAuth2 flow...")
    print("   (Your browser will open for authorization)")
    print()
    
    try:
        authenticator = GmailAuthenticator()
        authenticator.authenticate()
        
        print()
        print("🧪 Testing connection...")
        
        if authenticator.test_connection():
            print()
            print("=" * 70)
            print("✅ SETUP COMPLETE!")
            print("=" * 70)
            print()
            print(f"🎉 Gmail API is ready to use!")
            print(f"📁 Token saved to: {EmailConfig.TOKEN_FILE}")
            print()
            print("Next steps:")
            print("1. Edit config_email.py with your information")
            print("2. Set TEST_MODE = True in config_email.py")
            print("3. Run: python email_sender.py")
            print()
            return True
        else:
            print()
            print("❌ Connection test failed. Please try again.")
            return False
    
    except Exception as e:
        print()
        print(f"❌ Setup failed: {e}")
        print()
        print("Please check:")
        print("1. credentials.json is in the correct directory")
        print("2. Gmail API is enabled in Google Cloud Console")
        print("3. You authorized the app in your browser")
        return False


if __name__ == "__main__":
    # Run setup wizard if executed directly
    setup_gmail_api()

