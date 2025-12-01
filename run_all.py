"""
Master Orchestrator - Run Complete Lead Gen Pipeline
Runs all components in sequence: Research → Send → Track → Follow-up
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)


def print_header(title):
    """Print formatted section header."""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{title}")
    print(f"{Fore.CYAN}{'='*70}\n")


def run_script(script_name, description):
    """Run a Python script and handle errors."""
    print_header(f"🚀 {description}")
    
    print(f"{Fore.CYAN}Running: {script_name}")
    print(f"{Fore.CYAN}Started at: {datetime.now().strftime('%H:%M:%S')}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n{Fore.GREEN}✅ {description} completed successfully!")
            return True
        else:
            print(f"\n{Fore.RED}❌ {description} failed with exit code {result.returncode}")
            return False
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Interrupted by user")
        return False
    
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error running {script_name}: {e}")
        return False


def check_prerequisites():
    """Check if required files exist."""
    required_files = [
        'agency_bot.py',
        'email_sender.py',
        'response_tracker.py',
        'follow_up.py',
        'config_email.py'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"{Fore.RED}❌ Missing required files:")
        for file in missing:
            print(f"  - {file}")
        return False
    
    return True


def main():
    """Main orchestration flow."""
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}🤖 FULL AUTOMATION PIPELINE")
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    # Check prerequisites
    if not check_prerequisites():
        print(f"\n{Fore.RED}Setup incomplete. Please ensure all files are present.")
        return
    
    # Track results
    results = {}
    
    # Step 1: Generate Leads (Optional - comment out if you already have leads)
    run_research = input(f"{Fore.YELLOW}Run lead research bot? (yes/no): ").strip().lower()
    
    if run_research == 'yes':
        success = run_script('agency_bot.py', 'STEP 1: Lead Research')
        results['Research'] = success
        
        if not success:
            print(f"\n{Fore.YELLOW}⚠️  Lead research failed. Check leads.csv manually.")
            proceed = input(f"{Fore.YELLOW}Continue with existing leads? (yes/no): ").strip().lower()
            if proceed != 'yes':
                return
    else:
        print(f"{Fore.CYAN}Skipping lead research (using existing leads.csv)")
        results['Research'] = 'Skipped'
    
    # Delay before sending
    print(f"\n{Fore.CYAN}⏳ Waiting 10 seconds before sending emails...")
    time.sleep(10)
    
    # Step 2: Send Initial Emails
    success = run_script('email_sender.py', 'STEP 2: Send Initial Emails')
    results['Email Sending'] = success
    
    if not success:
        print(f"\n{Fore.YELLOW}⚠️  Email sending encountered issues.")
        proceed = input(f"{Fore.YELLOW}Continue to tracking? (yes/no): ").strip().lower()
        if proceed != 'yes':
            return
    
    # Delay before checking responses
    print(f"\n{Fore.CYAN}⏳ Waiting 5 seconds before checking responses...")
    time.sleep(5)
    
    # Step 3: Track Responses
    success = run_script('response_tracker.py', 'STEP 3: Track Responses')
    results['Response Tracking'] = success
    
    # Delay before follow-ups
    print(f"\n{Fore.CYAN}⏳ Waiting 5 seconds before sending follow-ups...")
    time.sleep(5)
    
    # Step 4: Send Follow-Ups
    success = run_script('follow_up.py', 'STEP 4: Send Follow-Up Emails')
    results['Follow-Ups'] = success
    
    # Summary
    print_header("📊 PIPELINE SUMMARY")
    
    for step, result in results.items():
        if result == True:
            status = f"{Fore.GREEN}✅ Success"
        elif result == False:
            status = f"{Fore.RED}❌ Failed"
        else:
            status = f"{Fore.YELLOW}⊘ Skipped"
        
        print(f"{step:20} {status}")
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    print(f"{Fore.GREEN}✅ Pipeline complete!")
    print(f"{Fore.CYAN}📊 Check leads.csv for results")
    print(f"{Fore.CYAN}📸 Screenshots in scans/ folder\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Pipeline interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}💥 Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

