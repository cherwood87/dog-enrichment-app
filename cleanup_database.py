#!/usr/bin/env python3
"""
Cleanup Script - Remove Bulk Imported Activities

This script will remove the activities that were just bulk imported and restore
your database to its original state with only the well-curated activities.
"""

import sqlite3
from enrichment_database import EnrichmentDatabase

class DatabaseCleanup:
    def __init__(self):
        self.db_path = 'enrichment_activities.db'
    
    def show_current_stats(self):
        """Show current database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM activities")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT category, COUNT(*) FROM activities GROUP BY category ORDER BY category")
        by_category = cursor.fetchall()
        
        conn.close()
        
        print(f"Current database contains {total} activities:")
        for category, count in by_category:
            print(f"  {category}: {count}")
        
        return total
    
    def reset_to_original_activities(self):
        """Reset database to original curated activities only"""
        print("🔄 Resetting database to original activities...")
        
        # Drop the existing table
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS activities")
        conn.commit()
        conn.close()
        
        # Reinitialize with just the original activities
        db = EnrichmentDatabase()
        
        print("✅ Database reset complete!")
        
        # Show new stats
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM activities")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT category, COUNT(*) FROM activities GROUP BY category ORDER BY category")
        by_category = cursor.fetchall()
        
        conn.close()
        
        print(f"\n📊 Restored database contains {total} original activities:")
        for category, count in by_category:
            print(f"  {category}: {count}")
    
    def selective_cleanup(self):
        """Remove activities added after a certain point"""
        print("🧹 Performing selective cleanup...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get activities sorted by creation time
        cursor.execute("SELECT id, name, created_at FROM activities ORDER BY created_at")
        all_activities = cursor.fetchall()
        
        print(f"Found {len(all_activities)} total activities")
        
        if len(all_activities) > 50:  # If we have way more than the original ~14
            # Keep only the first 20 activities (original ones)
            cursor.execute("DELETE FROM activities WHERE id > 20")
            deleted = cursor.rowcount
            conn.commit()
            
            print(f"✅ Removed {deleted} bulk-imported activities")
            
            # Show remaining
            cursor.execute("SELECT COUNT(*) FROM activities")
            remaining = cursor.fetchone()[0]
            print(f"📊 {remaining} original activities remain")
        
        conn.close()

def main():
    print("🚨 Database Cleanup Tool")
    print("=" * 30)
    
    cleanup = DatabaseCleanup()
    
    print("Current database status:")
    total = cleanup.show_current_stats()
    
    if total > 50:  # Way more than original
        print(f"\n⚠️  You have {total} activities - this seems like too many!")
        print("The bulk import probably fragmented your content.")
        print("\nOptions:")
        print("1. Reset to original curated activities only (RECOMMENDED)")
        print("2. Try selective cleanup (keep first 20 activities)")
        print("3. Cancel and keep current database")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            confirm = input("Are you sure you want to reset to original activities? (yes/no): ")
            if confirm.lower() == 'yes':
                cleanup.reset_to_original_activities()
            else:
                print("Cancelled.")
        elif choice == '2':
            cleanup.selective_cleanup()
        else:
            print("No changes made.")
    else:
        print("✅ Database size looks normal - no cleanup needed.")

if __name__ == "__main__":
    main()
