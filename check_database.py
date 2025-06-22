#!/usr/bin/env python3

import sqlite3
import os

def check_database_status():
    """Check what's currently in the database"""
    db_path = "/Users/cherilynwood-game/Desktop/dog-enrichment-app/enrichment_activities.db"
    
    if not os.path.exists(db_path):
        print("❌ Database does not exist!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if activities table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activities'")
    if not cursor.fetchone():
        print("❌ Activities table does not exist!")
        conn.close()
        return
    
    print("✅ Database and table exist")
    
    # Check total activities
    cursor.execute("SELECT COUNT(*) FROM activities")
    total = cursor.fetchone()[0]
    print(f"📊 Total activities: {total}")
    
    if total == 0:
        print("❌ No activities in database!")
        conn.close()
        return
    
    # Check by category
    cursor.execute("SELECT category, COUNT(*) FROM activities GROUP BY category ORDER BY category")
    categories = cursor.fetchall()
    
    print("\n📋 Activities by category:")
    for category, count in categories:
        print(f"  {category}: {count}")
    
    # Show sample activities
    print("\n🎯 Sample activities:")
    cursor.execute("SELECT name, category, estimated_time FROM activities LIMIT 8")
    samples = cursor.fetchall()
    for name, category, time in samples:
        print(f"  • {name} ({category}) - {time}")
    
    conn.close()

if __name__ == "__main__":
    check_database_status()
