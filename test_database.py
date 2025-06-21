#!/usr/bin/env python3

# Test script to verify the database system works
from enrichment_database import EnrichmentDatabase

def test_database():
    print("🐕 Testing Enrichment Database System...\n")
    
    # Initialize database
    db = EnrichmentDatabase()
    
    # Test profiles for different scenarios
    test_profiles = [
        {
            'name': 'High Energy Large Dog',
            'profile': {
                'breed': 'Large breed (60-90 lbs)',
                'age': 'Adult (3-7 years)',
                'energy_level': 'High energy - needs lots of stimulation',
                'weather': 'Nice weather - outdoor activities preferred',
                'enrichment_type': 'Physical enrichment - exercise and movement activities'
            }
        },
        {
            'name': 'Senior Small Dog',
            'profile': {
                'breed': 'Small breed (under 25 lbs)',
                'age': 'Senior (7+ years)',
                'energy_level': 'Low energy - prefers calm activities',
                'weather': 'Indoor weather - need indoor activities',
                'enrichment_type': 'Mental enrichment - cognitive challenges and problem-solving'
            }
        },
        {
            'name': 'Puppy Socialization',
            'profile': {
                'breed': 'Medium breed (25-60 lbs)',
                'age': 'Puppy (under 1 year)',
                'energy_level': 'High energy - needs lots of stimulation',
                'weather': 'Nice weather - outdoor activities preferred',
                'enrichment_type': 'Social enrichment - interactive bonding activities'
            }
        },
        {
            'name': 'Passive Enrichment Request',
            'profile': {
                'breed': 'Any dog',
                'age': 'Any age',
                'enrichment_type': 'Passive'
            }
        }
    ]
    
    # Test each profile
    for test in test_profiles:
        print(f"🔍 Testing: {test['name']}")
        print(f"Profile: {test['profile']}")
        
        activities = db.find_matching_activities(test['profile'], limit=4)
        
        print(f"✅ Found {len(activities)} activities:")
        for i, activity in enumerate(activities, 1):
            print(f"  {i}. {activity['name']} ({activity['category']})")
            print(f"     Time: {activity['estimated_time']}")
            print(f"     Materials: {', '.join(activity['materials'][:3])}{'...' if len(activity['materials']) > 3 else ''}")
        
        print("-" * 60)
    
    print("🎉 Database system test completed!")
    print("\n💡 Benefits of the new system:")
    print("   ✅ No repetitive AI responses")
    print("   ✅ Instant activity generation")
    print("   ✅ Consistent high quality")
    print("   ✅ Smart profile matching")
    print("   ✅ Easy to expand with more activities")

if __name__ == "__main__":
    test_database()
