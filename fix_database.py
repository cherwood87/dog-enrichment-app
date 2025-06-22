#!/usr/bin/env python3
"""
Script to fix the database issues and ensure activities are properly categorized
"""

import os
import sys
from enrichment_database import EnrichmentDatabase

def initialize_database():
    """Initialize the database with proper activities"""
    print("🔧 Initializing enrichment activities database...")
    
    # Create database instance - this will create the file and populate it
    db = EnrichmentDatabase()
    
    # Verify database was created
    if os.path.exists(db.db_path):
        print(f"✅ Database created at: {db.db_path}")
        
        # Check contents
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM activities")
        count = cursor.fetchone()[0]
        print(f"✅ Database contains {count} activities")
        
        # Show breakdown by category
        cursor.execute("SELECT category, COUNT(*) FROM activities GROUP BY category")
        categories = cursor.fetchall()
        print("\n📊 Activities by category:")
        for category, count in categories:
            print(f"  {category}: {count} activities")
        
        conn.close()
        
    else:
        print("❌ Failed to create database")
        return False
    
    return True

def test_matching():
    """Test the activity matching logic"""
    print("\n🧪 Testing activity matching...")
    
    db = EnrichmentDatabase()
    
    # Test different profiles
    test_profiles = [
        {
            'breed': 'Medium breed (25-60 lbs)',
            'age': 'Adult (3-7 years)', 
            'energy_level': 'High energy',
            'weather': 'Nice weather',
            'enrichment_type': 'Mental Enrichment'
        },
        {
            'breed': 'Large breed (60-90 lbs)',
            'age': 'Young adult (1-3 years)',
            'energy_level': 'Medium energy', 
            'weather': 'Indoor weather',
            'enrichment_type': 'Physical Enrichment'
        },
        {
            'breed': 'Small breed (under 25 lbs)',
            'age': 'Senior (8+ years)',
            'energy_level': 'Low energy',
            'weather': 'Any weather',
            'enrichment_type': 'Passive Enrichment'
        }
    ]
    
    for i, profile in enumerate(test_profiles):
        print(f"\n--- Test {i+1}: {profile['enrichment_type']} ---")
        activities = db.find_matching_activities(profile, limit=4)
        print(f"Found {len(activities)} activities:")
        for activity in activities:
            print(f"  ✓ {activity['name']} ({activity['category']})")

if __name__ == "__main__":
    print("🚀 Dog Enrichment Database Fixer")
    print("=" * 50)
    
    if initialize_database():
        test_matching()
        print("\n✅ Database initialization complete!")
        print("\n💡 Next steps:")
        print("1. Restart your Flask app")
        print("2. Test activity generation from the web interface")
        print("3. Activities should now match the selected enrichment type")
    else:
        print("\n❌ Database initialization failed!")
        sys.exit(1)
