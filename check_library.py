#!/usr/bin/env python3
"""
Complete Library Status Checker

Checks your current activity library and shows exactly what you have.
"""

import sqlite3
import json
from enrichment_database import EnrichmentDatabase

class LibraryChecker:
    def __init__(self):
        self.db = EnrichmentDatabase()
    
    def check_complete_library(self):
        """Comprehensive check of your activity library"""
        print("📚 Complete Activity Library Status Check")
        print("=" * 50)
        
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        # Overall stats
        cursor.execute("SELECT COUNT(*) FROM activities")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT category, COUNT(*) FROM activities GROUP BY category ORDER BY category")
        by_category = cursor.fetchall()
        
        print(f"🎯 Total Activities: {total}")
        print("\n📊 Activities by Category:")
        for category, count in by_category:
            print(f"  {category}: {count} activities")
        
        # Check for chewing activities specifically
        cursor.execute("SELECT COUNT(*) FROM activities WHERE name LIKE '%chew%' OR name LIKE '%bone%' OR name LIKE '%Kong%'")
        chewing_count = cursor.fetchone()[0]
        print(f"\n🦴 Chewing/Bone Activities: {chewing_count}")
        
        # Recent additions
        cursor.execute("SELECT name, category FROM activities ORDER BY rowid DESC LIMIT 10")
        recent = cursor.fetchall()
        
        print(f"\n🆕 Last 10 Activities Added:")
        for i, (name, category) in enumerate(recent, 1):
            print(f"{i:2d}. {name} ({category})")
        
        # Check subcategories in Passive
        cursor.execute("SELECT subcategory, COUNT(*) FROM activities WHERE category = 'Passive' GROUP BY subcategory")
        passive_subcats = cursor.fetchall()
        
        if passive_subcats:
            print(f"\n🧘 Passive Enrichment Breakdown:")
            for subcat, count in passive_subcats:
                subcat_name = subcat if subcat else "General"
                print(f"  {subcat_name}: {count}")
        
        # Check for missing categories
        expected_categories = ['Mental', 'Physical', 'Social', 'Environmental', 'Instinctual', 'Passive']
        existing_categories = [cat for cat, _ in by_category]
        missing = [cat for cat in expected_categories if cat not in existing_categories]
        
        if missing:
            print(f"\n⚠️  Missing Categories: {', '.join(missing)}")
        else:
            print(f"\n✅ All 6 categories present!")
        
        # Quality check - look for activities with good content
        cursor.execute("""
            SELECT name, category, materials, instructions, safety_notes 
            FROM activities 
            WHERE json_array_length(materials) > 0 
            AND json_array_length(instructions) > 0
            LIMIT 5
        """)
        quality_check = cursor.fetchall()
        
        print(f"\n🔍 Quality Check - Sample Activities:")
        for name, category, materials, instructions, safety in quality_check:
            materials_list = json.loads(materials)
            instructions_list = json.loads(instructions)
            print(f"  📝 {name} ({category})")
            print(f"     Materials: {len(materials_list)} items")
            print(f"     Instructions: {len(instructions_list)} steps")
            print(f"     Safety notes: {'Yes' if safety else 'No'}")
        
        conn.close()
        
        # Recommendations
        self.provide_recommendations(total, by_category, chewing_count)
    
    def provide_recommendations(self, total, by_category, chewing_count):
        """Provide recommendations based on library status"""
        print(f"\n💡 Recommendations:")
        
        if total < 50:
            print("  📈 Consider running enhanced_library.py to build more activities")
        
        if chewing_count == 0:
            print("  🦴 Run add_chewing_activities.py to add bone/chewing activities")
        
        # Check category balance
        if by_category:
            counts = [count for _, count in by_category]
            min_count = min(counts)
            max_count = max(counts)
            
            if max_count - min_count > 10:
                print("  ⚖️  Some categories have significantly more activities than others")
                print("     Consider balancing by generating more for smaller categories")
        
        if total >= 80:
            print("  🎉 Excellent! You have a comprehensive activity library")
            print("  🚀 Your app is ready for launch!")
    
    def show_sample_activities(self, category=None):
        """Show sample activities from a specific category"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute("SELECT name, description, materials, instructions FROM activities WHERE category = ? LIMIT 3", (category,))
            print(f"\n📖 Sample {category} Activities:")
        else:
            cursor.execute("SELECT name, category, description FROM activities LIMIT 5")
            print(f"\n📖 Sample Activities (All Categories):")
        
        results = cursor.fetchall()
        
        for i, result in enumerate(results, 1):
            if category:
                name, desc, materials, instructions = result
                materials_list = json.loads(materials)
                instructions_list = json.loads(instructions)
                print(f"\n{i}. {name}")
                print(f"   Description: {desc}")
                print(f"   Materials: {materials_list[:3]}{'...' if len(materials_list) > 3 else ''}")
                print(f"   Steps: {len(instructions_list)} instructions")
            else:
                name, cat, desc = result
                print(f"{i}. {name} ({cat})")
                print(f"   {desc[:100]}{'...' if len(desc) > 100 else ''}")
        
        conn.close()
    
    def check_specific_activity(self, activity_name):
        """Check details of a specific activity"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM activities WHERE name LIKE ?", (f'%{activity_name}%',))
        results = cursor.fetchall()
        
        if not results:
            print(f"❌ No activities found matching '{activity_name}'")
            return
        
        print(f"\n🔍 Found {len(results)} matching activities:")
        
        for result in results:
            name = result[1]
            category = result[2]
            description = result[4]
            materials = json.loads(result[5])
            instructions = json.loads(result[6])
            safety = result[7]
            time_est = result[8]
            
            print(f"\n📝 {name} ({category})")
            print(f"   Description: {description}")
            print(f"   Materials ({len(materials)}): {', '.join(materials[:3])}{'...' if len(materials) > 3 else ''}")
            print(f"   Instructions: {len(instructions)} steps")
            print(f"   Safety notes: {'Yes' if safety else 'No'}")
            print(f"   Time: {time_est}")
        
        conn.close()

def main():
    checker = LibraryChecker()
    
    print("🐕 Activity Library Checker")
    print("=" * 30)
    print("1. Complete library status")
    print("2. Sample activities by category")
    print("3. Check specific activity")
    print("4. Exit")
    
    while True:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            checker.check_complete_library()
        elif choice == '2':
            category = input("Enter category (Mental/Physical/Social/Environmental/Instinctual/Passive): ").strip()
            if category:
                checker.show_sample_activities(category)
        elif choice == '3':
            activity_name = input("Enter activity name or keyword: ").strip()
            if activity_name:
                checker.check_specific_activity(activity_name)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
