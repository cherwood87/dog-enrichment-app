#!/usr/bin/env python3
"""
Complete fix for the dog enrichment activity matching system
"""

import os
import sys
import sqlite3

# Add the project directory to Python path
project_dir = '/Users/cherilynwood-game/Desktop/dog-enrichment-app'
sys.path.insert(0, project_dir)

def force_database_reset():
    """Force a complete database reset"""
    db_path = os.path.join(project_dir, 'enrichment_activities.db')
    
    print("🔄 Forcing database reset...")
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Removed existing database")
    
    # Import and create new database
    from enrichment_database import EnrichmentDatabase
    
    print("🔧 Creating new database...")
    db = EnrichmentDatabase()
    
    # Verify population
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM activities")
    total = cursor.fetchone()[0]
    print(f"📊 Database populated with {total} activities")
    
    if total == 0:
        print("❌ Failed to populate database!")
        return False
    
    # Check categories
    cursor.execute("SELECT category, COUNT(*) FROM activities GROUP BY category")
    categories = cursor.fetchall()
    
    print("\n📋 Activities by category:")
    for category, count in categories:
        print(f"  {category}: {count}")
    
    conn.close()
    return True

def test_matching_logic():
    """Test the matching logic with various scenarios"""
    print("\n" + "="*60)
    print("🧪 TESTING ACTIVITY MATCHING LOGIC")
    print("="*60)
    
    from enrichment_database import EnrichmentDatabase
    db = EnrichmentDatabase()
    
    test_cases = [
        {
            'name': 'Physical Activities for Active Dog',
            'profile': {
                'breed': 'Medium breed (25-60 lbs)',
                'age': 'Adult (3-7 years)',
                'energy_level': 'High energy - needs lots of stimulation',
                'weather': 'Nice weather - outdoor activities preferred',
                'enrichment_type': 'Physical Enrichment - Exercise and movement activities'
            },
            'expected_category': 'Physical'
        },
        {
            'name': 'Mental Activities for Senior Dog',
            'profile': {
                'breed': 'Small breed (under 25 lbs)',
                'age': 'Senior (7+ years)',
                'energy_level': 'Low energy - calm activities',
                'weather': 'Indoor weather - need indoor activities',
                'enrichment_type': 'Mental Enrichment - Cognitive challenges and problem-solving'
            },
            'expected_category': 'Mental'
        },
        {
            'name': 'Social Activities',
            'profile': {
                'breed': 'Large breed (60-90 lbs)',
                'age': 'Young adult (1-3 years)',
                'energy_level': 'Moderate energy - regular exercise',
                'weather': 'Mixed - indoor and outdoor options',
                'enrichment_type': 'Social Enrichment - Interactive bonding activities'
            },
            'expected_category': 'Social'
        },
        {
            'name': 'Instinctual Activities',
            'profile': {
                'breed': 'Mixed breed',
                'age': 'Adult (3-7 years)',
                'energy_level': 'Moderate energy - regular exercise',
                'weather': 'Nice weather - outdoor activities preferred',
                'enrichment_type': 'Instinctual Enrichment - Natural behaviors like sniffing, foraging, hunting'
            },
            'expected_category': 'Instinctual'
        },
        {
            'name': 'Passive Activities',
            'profile': {
                'breed': 'Giant breed (over 90 lbs)',
                'age': 'Senior (7+ years)',
                'energy_level': 'Low energy - calm activities',
                'weather': 'Indoor weather - need indoor activities',
                'enrichment_type': 'Mixed Enrichment - Variety of different activities'
            },
            'expected_category': 'Any'  # Mixed should return various categories
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case['name']}")
        print(f"   Profile: {test_case['profile']['enrichment_type']}")
        
        activities = db.find_matching_activities(test_case['profile'], limit=4)
        
        print(f"   Found {len(activities)} activities:")
        
        if len(activities) == 0:
            print("   ❌ FAIL: No activities found!")
            all_passed = False
            continue
        
        correct_matches = 0
        for activity in activities:
            if test_case['expected_category'] == 'Any' or activity['category'] == test_case['expected_category']:
                correct_matches += 1
                print(f"   ✅ {activity['name']} ({activity['category']})")
            else:
                print(f"   ❌ {activity['name']} ({activity['category']}) - Expected {test_case['expected_category']}")
        
        success_rate = (correct_matches / len(activities)) * 100
        print(f"   Success Rate: {success_rate:.0f}%")
        
        if success_rate >= 75 or test_case['expected_category'] == 'Any':
            print("   ✅ PASS")
        else:
            print("   ❌ FAIL")
            all_passed = False
    
    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 ALL TESTS PASSED! Activity matching is working correctly.")
    else:
        print("❌ SOME TESTS FAILED! There are still issues with activity matching.")
    
    return all_passed

def main():
    """Main function to fix and test the system"""
    print("🚀 Dog Enrichment Activity Matching - Complete Fix")
    print("="*60)
    
    # Step 1: Reset database
    if not force_database_reset():
        print("❌ Failed to reset database!")
        return
    
    # Step 2: Test matching logic
    if test_matching_logic():
        print("\n✅ SUCCESS: Activity matching system is now working correctly!")
        print("Users should now receive personalized activities based on their dog's profile.")
    else:
        print("\n❌ FAILURE: There are still issues with the matching system.")

if __name__ == "__main__":
    main()
