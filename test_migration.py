#!/usr/bin/env python3
"""
Test the Supabase migration integration
"""

import sys
import os
sys.path.append('/Users/cherilynwood-game/Desktop/dog-enrichment-app')

from supabase_client import supabase_client

def test_supabase_integration():
    """Test the Supabase client integration"""
    print("🧪 Testing Supabase Integration")
    print("=" * 50)
    
    # Test 1: Check if Supabase is configured
    print(f"1. Supabase configured: {'✅ YES' if supabase_client.enabled else '❌ NO'}")
    
    if not supabase_client.enabled:
        print("   Configure Supabase credentials in .env file to enable")
        return False
    
    # Test 2: Test profile building
    print("\n2. Testing profile building...")
    test_form_data = {
        'dog_name': 'Buddy',
        'breed': 'Medium breed (25-60 lbs)',
        'age': 'Adult (3-7 years)',
        'energy_level': 'High energy - needs lots of stimulation',
        'weather': 'Nice weather - outdoor activities preferred',
        'enrichment_type': 'Physical Enrichment - Exercise and movement activities'
    }
    
    profile = supabase_client.build_dog_profile(test_form_data)
    print(f"   ✅ Profile built: {profile['name']}, {profile['breed']}, {profile['energyLevel']} energy")
    
    # Test 3: Test activity discovery (if credentials are valid)
    print("\n3. Testing activity discovery...")
    try:
        result = supabase_client.discover_activities(profile, max_activities=2)
        
        if result['success']:
            activities = result['activities']
            print(f"   ✅ Generated {len(activities)} activities")
            
            if activities:
                print(f"   Sample activity: '{activities[0].get('title', 'Unnamed')}' ({activities[0].get('pillar', 'Unknown')} pillar)")
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False
    
    print("\n🎉 All tests passed! Supabase integration is working.")
    return True

def test_fallback_system():
    """Test the fallback to local system"""
    print("\n🔄 Testing fallback system...")
    
    # Temporarily disable Supabase
    original_enabled = supabase_client.enabled
    supabase_client.enabled = False
    
    try:
        from enrichment_database import EnrichmentDatabase
        db = EnrichmentDatabase()
        
        test_profile = {
            'breed': 'Medium breed (25-60 lbs)',
            'age': 'Adult (3-7 years)',
            'energy_level': 'High energy - needs lots of stimulation',
            'weather': 'Nice weather - outdoor activities preferred',
            'enrichment_type': 'Physical Enrichment - Exercise and movement activities'
        }
        
        activities = db.find_matching_activities(test_profile, limit=2)
        print(f"   ✅ Local database returned {len(activities)} activities")
        
        if activities:
            print(f"   Sample activity: '{activities[0]['name']}' ({activities[0]['category']})")
        
    except Exception as e:
        print(f"   ❌ Local fallback failed: {str(e)}")
    finally:
        # Restore original state
        supabase_client.enabled = original_enabled
    
    print("   ✅ Fallback system tested")

if __name__ == "__main__":
    print("🚀 Dog Enrichment App - Supabase Migration Test")
    print("=" * 60)
    
    success = test_supabase_integration()
    test_fallback_system()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 MIGRATION SUCCESSFUL!")
        print("Your app is ready to use Supabase AI functions.")
        print("\nNext steps:")
        print("1. Set up your Supabase credentials in .env")
        print("2. Run your Flask app: python app.py")
        print("3. Test with real dog profiles")
    else:
        print("⚠️  MIGRATION NEEDS SETUP")
        print("Configure Supabase credentials to enable AI features.")
        print("The app will still work with local database fallback.")
