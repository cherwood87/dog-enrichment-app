#!/usr/bin/env python3

import sys
import os
sys.path.append('/Users/cherilynwood-game/Desktop/dog-enrichment-app')

from enrichment_database import EnrichmentDatabase

def test_activity_matching():
    """Test the improved activity matching"""
    print("Testing improved activity matching...")
    
    # Initialize database
    db = EnrichmentDatabase()
    
    # Test different scenarios
    test_scenarios = [
        {
            'name': 'High Energy Physical Activities',
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
            'name': 'Senior Mental Activities',
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
            'name': 'Instinctual Activities',
            'profile': {
                'breed': 'Large breed (60-90 lbs)',
                'age': 'Young adult (1-3 years)',
                'energy_level': 'Moderate energy - regular exercise',
                'weather': 'Mixed - indoor and outdoor options',
                'enrichment_type': 'Instinctual Enrichment - Natural behaviors like sniffing, foraging, hunting'
            },
            'expected_category': 'Instinctual'
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{'='*60}")
        print(f"Testing: {scenario['name']}")
        print(f"Expected category: {scenario['expected_category']}")
        print(f"Profile: {scenario['profile']['breed']}, {scenario['profile']['age']}")
        print(f"Weather: {scenario['profile']['weather']}")
        print(f"Type: {scenario['profile']['enrichment_type']}")
        
        # Test the matching
        activities = db.find_matching_activities(scenario['profile'], limit=4)
        
        print(f"\nFound {len(activities)} activities:")
        correct_category = 0
        for activity in activities:
            category_match = "✅" if activity['category'] == scenario['expected_category'] else "❌"
            print(f"  {category_match} {activity['name']} ({activity['category']})")
            if activity['category'] == scenario['expected_category']:
                correct_category += 1
        
        success_rate = (correct_category / len(activities) * 100) if activities else 0
        print(f"\nSuccess rate: {success_rate:.0f}% ({correct_category}/{len(activities)} correct category)")
        
        if success_rate >= 75:
            print("✅ PASS - Good category matching")
        else:
            print("❌ FAIL - Poor category matching")

if __name__ == "__main__":
    test_activity_matching()
