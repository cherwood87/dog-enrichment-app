#!/usr/bin/env python3
"""
Reset and repopulate the enrichment database with improved activities
"""

import os
import sqlite3
from enrichment_database import EnrichmentDatabase

def reset_database():
    """Remove existing database and create a fresh one"""
    db_path = "enrichment_activities.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed existing database")
    
    # Create new database with improved activities
    db = EnrichmentDatabase()
    print("Created new database with improved activities")
    
    # Verify activities were added
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT category, COUNT(*) FROM activities GROUP BY category")
    results = cursor.fetchall()
    
    print("\nActivities by category:")
    total = 0
    for category, count in results:
        print(f"  {category}: {count} activities")
        total += count
    
    print(f"\nTotal activities: {total}")
    
    # Test the matching function
    print("\n" + "="*50)
    print("TESTING ACTIVITY MATCHING")
    print("="*50)
    
    test_profiles = [
        {
            'breed': 'Medium breed (25-60 lbs)',
            'age': 'Adult (3-7 years)',
            'energy_level': 'High energy - needs lots of stimulation',
            'weather': 'Nice weather - outdoor activities preferred',
            'enrichment_type': 'Physical Enrichment - Exercise and movement activities'
        },
        {
            'breed': 'Small breed (under 25 lbs)',
            'age': 'Senior (7+ years)',
            'energy_level': 'Low energy - calm activities',
            'weather': 'Indoor weather - need indoor activities',
            'enrichment_type': 'Mental Enrichment - Cognitive challenges and problem-solving'
        },
        {
            'breed': 'Large breed (60-90 lbs)',
            'age': 'Young adult (1-3 years)',
            'energy_level': 'Moderate energy - regular exercise',
            'weather': 'Mixed - indoor and outdoor options',
            'enrichment_type': 'Instinctual Enrichment - Natural behaviors like sniffing, foraging, hunting'
        }
    ]
    
    for i, profile in enumerate(test_profiles, 1):
        print(f"\nTest {i}: {profile['breed']}, {profile['age']}, {profile['enrichment_type']}")
        activities = db.find_matching_activities(profile, limit=4)
        print(f"Found {len(activities)} activities:")
        for activity in activities:
            print(f"  - {activity['name']} ({activity['category']})")
    
    conn.close()

if __name__ == "__main__":
    reset_database()
