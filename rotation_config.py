"""
Niche & City Rotation Configuration
Automatically rotates through niches and cities across America.
"""

import json
import os
from datetime import date

# ============================================================================
# ROTATION DATA
# ============================================================================

# Major US Cities (In order of priority)
US_CITIES = [
    # Pacific Northwest
    "Seattle WA", "Portland OR", "Spokane WA", "Tacoma WA", "Vancouver WA",
    "Bellevue WA", "Everett WA", "Olympia WA", "Boise ID",
    
    # California
    "Los Angeles CA", "San Diego CA", "San Francisco CA", "San Jose CA",
    "Sacramento CA", "Fresno CA", "Oakland CA", "Long Beach CA",
    
    # Southwest
    "Phoenix AZ", "Tucson AZ", "Las Vegas NV", "Albuquerque NM",
    "Denver CO", "Colorado Springs CO", "Aurora CO",
    
    # Texas
    "Austin TX", "Dallas TX", "Houston TX", "San Antonio TX",
    "Fort Worth TX", "El Paso TX", "Arlington TX", "Plano TX",
    
    # Midwest
    "Chicago IL", "Detroit MI", "Indianapolis IN", "Columbus OH",
    "Milwaukee WI", "Kansas City MO", "Omaha NE", "Minneapolis MN",
    
    # South
    "Atlanta GA", "Charlotte NC", "Miami FL", "Tampa FL",
    "Orlando FL", "Jacksonville FL", "Nashville TN", "Memphis TN",
    
    # East Coast
    "New York NY", "Philadelphia PA", "Boston MA", "Baltimore MD",
    "Washington DC", "Pittsburgh PA", "Buffalo NY", "Newark NJ"
]

# Service Niches (Rotating daily)
SERVICE_NICHES = [
    "Landscapers",
    "Roofing Companies",
    "HVAC Companies",
    "Plumbers",
    "Electricians",
    "Painters",
    "Carpet Cleaning",
    "Pool Services",
    "Pest Control",
    "Tree Services",
    "Garage Door Repair",
    "Handyman Services",
    "Window Cleaning",
    "Pressure Washing",
    "Fence Companies",
    "Concrete Contractors",
    "Flooring Companies",
    "Kitchen Remodeling",
    "Bathroom Remodeling",
    "Moving Companies",
    "Junk Removal",
    "Locksmiths",
    "Auto Repair Shops",
    "Restaurants",
    "Hair Salons",
    "Dental Clinics",
    "Chiropractors",
    "Physical Therapy",
    "Veterinarians",
    "Real Estate Agents"
]

# ============================================================================
# STATE FILE
# ============================================================================

STATE_FILE = "rotation_state.json"


def load_state():
    """Load current rotation state."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Default state: Start in Seattle
    return {
        "current_city_index": 0,
        "current_niche_index": 0,
        "last_run_date": None,
        "leads_found_in_city": 0,
        "total_leads_found": 0
    }


def save_state(state):
    """Save rotation state."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def get_current_query():
    """Get current search query based on rotation state."""
    state = load_state()
    
    city = US_CITIES[state["current_city_index"]]
    niche = SERVICE_NICHES[state["current_niche_index"]]
    
    return f"{niche} in {city}", city, niche


def rotate_niche():
    """Rotate to next niche (called daily)."""
    state = load_state()
    
    # Move to next niche
    state["current_niche_index"] = (state["current_niche_index"] + 1) % len(SERVICE_NICHES)
    
    # Reset if we've cycled through all niches
    if state["current_niche_index"] == 0:
        print("🔄 Completed full niche rotation!")
    
    save_state(state)
    return get_current_query()


def rotate_city(leads_found=0):
    """Rotate to next city (called when no leads or low leads found)."""
    state = load_state()
    
    # Track leads in current city
    state["leads_found_in_city"] += leads_found
    
    # If we found fewer than 5 leads, move to next city
    if state["leads_found_in_city"] < 5:
        print(f"⚠️  Only {state['leads_found_in_city']} leads in city. Moving to next city...")
        
        # Move to next city
        state["current_city_index"] = (state["current_city_index"] + 1) % len(US_CITIES)
        state["leads_found_in_city"] = 0
        
        # Reset niche rotation for new city
        state["current_niche_index"] = 0
        
        save_state(state)
    
    return get_current_query()


def mark_run_complete(leads_found):
    """Mark today's run as complete."""
    state = load_state()
    
    state["last_run_date"] = str(date.today())
    state["total_leads_found"] += leads_found
    state["leads_found_in_city"] += leads_found
    
    save_state(state)


def should_rotate_today():
    """Check if we should rotate niche today."""
    state = load_state()
    last_run = state.get("last_run_date")
    
    if last_run is None:
        return False  # First run
    
    # Rotate if it's a new day
    return str(date.today()) != last_run


def get_rotation_summary():
    """Get current rotation status."""
    state = load_state()
    query, city, niche = get_current_query()
    
    return f"""
Current Rotation Status:
  📍 City: {city} (#{state['current_city_index'] + 1}/{len(US_CITIES)})
  🎯 Niche: {niche} (#{state['current_niche_index'] + 1}/{len(SERVICE_NICHES)})
  📊 Leads in this city: {state['leads_found_in_city']}
  📊 Total leads found: {state['total_leads_found']}
  🔍 Current query: "{query}"
    """


# ============================================================================
# MAIN LOGIC
# ============================================================================

def get_todays_search_query():
    """
    Get today's search query with automatic rotation.
    Call this at the start of agency_bot.py
    """
    # Check if we need to rotate
    if should_rotate_today():
        print("📅 New day detected - rotating to next niche!")
        rotate_niche()
    
    query, city, niche = get_current_query()
    
    print(get_rotation_summary())
    
    return query


if __name__ == "__main__":
    # Test the rotation
    print("Testing rotation system...")
    print(get_rotation_summary())
    
    query = get_todays_search_query()
    print(f"\nToday's search: {query}")

