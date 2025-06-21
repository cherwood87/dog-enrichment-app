#!/usr/bin/env python3
"""
Complete Database Reset

This script will completely reset the database to a clean state with just a few sample activities.
"""

import sqlite3
import os
from pathlib import Path

def reset_database():
    """Reset database to clean state"""
    db_path = 'enrichment_activities.db'
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Removed existing database")
    
    # Remove processed files
    processed_folder = Path("processed_activities")
    if processed_folder.exists():
        for file in processed_folder.glob("*"):
            file.unlink()
        processed_folder.rmdir()
        print("✅ Cleaned processed_activities folder")
    
    # Remove new activities
    new_folder = Path("new_activities")
    if new_folder.exists():
        for file in new_folder.glob("*"):
            file.unlink()
        new_folder.rmdir()
        print("✅ Cleaned new_activities folder")
    
    print("🧹 Database completely reset!")
    print("Run your app now for a fresh start")

if __name__ == "__main__":
    print("🚨 Complete Database Reset")
    print("=" * 30)
    confirm = input("Are you sure you want to delete ALL activities? (yes/no): ")
    if confirm.lower() == 'yes':
        reset_database()
    else:
        print("Reset cancelled.")
