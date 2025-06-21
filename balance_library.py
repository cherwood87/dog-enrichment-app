#!/usr/bin/env python3
"""
Library Balancer - Add activities to smaller categories
"""

from enhanced_library import EnhancedActivityLibrary
import sqlite3

def balance_library():
    print("⚖️ Library Balancer")
    print("=" * 25)
    
    # Check current status
    library = EnhancedActivityLibrary()
    conn = sqlite3.connect(library.db.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT category, COUNT(*) FROM activities GROUP BY category ORDER BY COUNT(*)")
    categories = cursor.fetchall()
    conn.close()
    
    print("📊 Current categories (smallest to largest):")
    for category, count in categories:
        print(f"  {category}: {count}")
    
    # Target the smallest categories
    target_count = 10
    categories_to_boost = []
    
    for category, count in categories:
        if count < target_count:
            needed = target_count - count
            categories_to_boost.append((category, needed))
            print(f"\n🎯 {category} needs {needed} more activities")
    
    if not categories_to_boost:
        print("\n✅ All categories are well balanced!")
        return
    
    # Add activities to boost smaller categories
    for category, needed in categories_to_boost:
        print(f"\n📚 Generating {needed} more {category} activities...")
        
        # Generate activities for this specific category
        ai_activities = library.generate_ai_activities(category, needed)
        curated_activities = library.curate_quality_activities(ai_activities)
        
        added_count = 0
        for activity in curated_activities:
            try:
                activity['category'] = category
                if not activity_exists(activity['name'], library.db.db_path):
                    library.db.add_activity(activity)
                    print(f"  ✅ Added: {activity['name']}")
                    added_count += 1
                else:
                    print(f"  ⏭️  Skipped: {activity['name']} (exists)")
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        print(f"  📊 Added {added_count} {category} activities")
    
    # Show final status
    print(f"\n🎉 Library Balanced!")
    conn = sqlite3.connect(library.db.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM activities")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT category, COUNT(*) FROM activities GROUP BY category ORDER BY category")
    final_counts = cursor.fetchall()
    conn.close()
    
    print(f"📊 Final library: {total} total activities")
    for category, count in final_counts:
        print(f"  {category}: {count}")

def activity_exists(name: str, db_path: str) -> bool:
    """Check if activity exists"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM activities WHERE name = ?", (name,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

if __name__ == "__main__":
    balance_library()
