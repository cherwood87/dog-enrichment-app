#!/usr/bin/env python3
"""
Quick test of your specific Supabase setup
"""

import os
import sys
sys.path.append('/Users/cherilynwood-game/Desktop/dog-enrichment-app')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_your_setup():
    """Test your specific Supabase configuration"""
    print("🧪 Testing Your Supabase Setup")
    print("=" * 50)
    
    # Check environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    discover_url = os.getenv('SUPABASE_DISCOVER_ACTIVITIES_URL')
    
    print(f"✅ Supabase URL: {supabase_url}")
    print(f"✅ Anon Key: {supabase_key[:20]}...")
    print(f"✅ Discover URL: {discover_url}")
    
    # Test the client
    try:
        from supabase_client import supabase_client
        
        if supabase_client.enabled:
            print("\n🚀 Supabase client is enabled!")
            
            # Test profile building
            test_form = {
                'dog_name': 'Buddy',
                'breed': 'Medium breed (25-60 lbs)',
                'age': 'Adult (3-7 years)',
                'energy_level': 'High energy - needs lots of stimulation',
                'weather': 'Nice weather - outdoor activities preferred',
                'enrichment_type': 'Physical Enrichment - Exercise and movement activities'
            }
            
            profile = supabase_client.build_dog_profile(test_form)
            print(f"📋 Test profile: {profile['name']} - {profile['breed']} - {profile['energyLevel']} energy")
            
            # Test actual API call
            print("\n🌐 Testing API call to discover-activities...")
            result = supabase_client.discover_activities(profile, max_activities=2)
            
            if result['success']:
                activities = result['activities']
                print(f"🎉 SUCCESS! Generated {len(activities)} activities")
                
                if activities:
                    for i, activity in enumerate(activities, 1):
                        print(f"   {i}. {activity.get('title', 'Unnamed')} ({activity.get('pillar', 'Unknown')} pillar)")
                        print(f"      Duration: {activity.get('duration', 'Unknown')} min, Difficulty: {activity.get('difficulty', 'Unknown')}")
            else:
                print(f"❌ API call failed: {result.get('error', 'Unknown error')}")
                return False
                
        else:
            print("❌ Supabase client is not enabled - check your .env file")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Supabase: {str(e)}")
        return False
    
    print("\n🎉 ALL TESTS PASSED!")
    print("Your Supabase integration is working perfectly!")
    return True

if __name__ == "__main__":
    success = test_your_setup()
    
    if success:
        print("\n🚀 READY TO GO!")
        print("Start your app with: python app.py")
        print("Then test with real dog profiles!")
    else:
        print("\n⚠️ SETUP NEEDED")
        print("Check your Edge Functions are deployed in Supabase")
