#!/usr/bin/env python3
"""
Drop Folder Activity Importer

Place .txt files with activities in the 'new_activities' folder and this script
will automatically convert them to your database format and add them.

Expected format:
**Activity Name**
**•Materials Needed**
* item 1
* item 2
**•Step-by-Step Instructions**
1. Step one
2. Step two
**•Safety Notes**
Safety information here
**•Estimated Time**
10-15 minutes
"""

import os
import re
import json
from pathlib import Path
from enrichment_database import EnrichmentDatabase

class DropFolderImporter:
    def __init__(self):
        self.db = EnrichmentDatabase()
        self.drop_folder = Path("new_activities")
        self.processed_folder = Path("processed_activities")
        
        # Create folders if they don't exist
        self.drop_folder.mkdir(exist_ok=True)
        self.processed_folder.mkdir(exist_ok=True)
    
    def process_all_files(self):
        """Process all .txt files in the drop folder"""
        txt_files = list(self.drop_folder.glob("*.txt"))
        
        if not txt_files:
            print("📂 No .txt files found in the new_activities folder")
            print("Add your activity files there and run this script again!")
            return
        
        print(f"📁 Found {len(txt_files)} files to process:")
        for file in txt_files:
            print(f"  - {file.name}")
        
        total_added = 0
        
        for file_path in txt_files:
            print(f"\n📄 Processing {file_path.name}...")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                activities = self.parse_activities_from_content(content)
                
                added_count = 0
                for activity in activities:
                    if activity and activity.get('name'):
                        # Auto-detect category from filename or content
                        category = self.detect_category(file_path.name, content)
                        activity['category'] = category
                        
                        if not self.activity_exists(activity['name']):
                            try:
                                self.db.add_activity(activity)
                                print(f"  ✅ Added: {activity['name']} ({category})")
                                added_count += 1
                            except Exception as e:
                                print(f"  ❌ Error adding {activity['name']}: {e}")
                        else:
                            print(f"  ⏭️  Skipped: {activity['name']} (already exists)")
                
                total_added += added_count
                
                # Move processed file
                processed_path = self.processed_folder / file_path.name
                file_path.rename(processed_path)
                print(f"  📦 Moved {file_path.name} to processed_activities/")
                
            except Exception as e:
                print(f"  ❌ Error processing {file_path.name}: {e}")
        
        print(f"\n🎉 Processing complete! Added {total_added} total activities")
        self.show_summary()
    
    def parse_activities_from_content(self, content: str) -> list:
        """Parse activities from the simple format"""
        activities = []
        
        # Split by activity headers (lines starting with **)
        # Each activity starts with **Activity Name**
        activity_sections = re.split(r'\n(?=\*\*[^*]+\*\*\s*$)', content)
        
        for section in activity_sections:
            section = section.strip()
            if len(section) < 50:  # Skip very short sections
                continue
            
            activity = self.parse_single_activity(section)
            if activity:
                activities.append(activity)
        
        return activities
    
    def parse_single_activity(self, text: str) -> dict:
        """Parse a single activity from the simple format"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return {}
        
        # Extract activity name (first line with **name**)
        name_match = re.match(r'\*\*(.+?)\*\*', lines[0])
        if not name_match:
            return {}
        
        name = name_match.group(1).strip()
        
        # Initialize activity with defaults
        activity = {
            'name': name,
            'category': 'Mental',  # Will be updated by detect_category
            'subcategory': '',
            'description': f"A {name.lower()} enrichment activity",
            'materials': [],
            'instructions': [],
            'safety_notes': '',
            'estimated_time': '',
            'difficulty_level': 'Medium',
            'energy_required': 'Medium',
            'weather_suitable': 'Any',
            'breed_sizes': ['All'],
            'age_groups': ['All'],
            'tags': []
        }
        
        # Parse sections
        current_section = None
        
        for line in lines[1:]:  # Skip the name line
            line = line.strip()
            
            # Identify sections
            if line.startswith('**•Materials Needed**'):
                current_section = 'materials'
                continue
            elif line.startswith('**•Step-by-Step Instructions**'):
                current_section = 'instructions'
                continue
            elif line.startswith('**•Safety Notes**'):
                current_section = 'safety'
                continue
            elif line.startswith('**•Estimated Time**'):
                current_section = 'time'
                continue
            elif line.startswith('**•Description**'):
                current_section = 'description'
                continue
            
            # Process content based on current section
            if current_section == 'materials':
                if line.startswith('*'):
                    material = line.replace('*', '').strip()
                    if material:
                        activity['materials'].append(material)
            
            elif current_section == 'instructions':
                # Look for numbered steps
                step_match = re.match(r'^(\d+)\.\s*(.+)$', line)
                if step_match:
                    step_text = step_match.group(2)
                    activity['instructions'].append(step_text)
            
            elif current_section == 'safety':
                if line and not line.startswith('**'):
                    if activity['safety_notes']:
                        activity['safety_notes'] += ' ' + line
                    else:
                        activity['safety_notes'] = line
            
            elif current_section == 'time':
                if line and not line.startswith('**'):
                    activity['estimated_time'] = line
            
            elif current_section == 'description':
                if line and not line.startswith('**'):
                    activity['description'] = line
        
        # Set intelligent defaults
        activity = self.set_intelligent_defaults(activity)
        
        return activity
    
    def detect_category(self, filename: str, content: str) -> str:
        """Auto-detect category from filename or content"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # Check filename first
        if 'mental' in filename_lower or 'brain' in filename_lower:
            return 'Mental'
        elif 'physical' in filename_lower or 'exercise' in filename_lower:
            return 'Physical'
        elif 'social' in filename_lower:
            return 'Social'
        elif 'environmental' in filename_lower:
            return 'Environmental'
        elif 'instinctual' in filename_lower:
            return 'Instinctual'
        elif 'passive' in filename_lower:
            return 'Passive'
        
        # Check content
        if any(word in content_lower for word in ['training', 'bonding', 'social', 'interaction']):
            return 'Social'
        elif any(word in content_lower for word in ['puzzle', 'brain', 'cognitive', 'thinking', 'mental']):
            return 'Mental'
        elif any(word in content_lower for word in ['exercise', 'running', 'jumping', 'physical']):
            return 'Physical'
        elif any(word in content_lower for word in ['environment', 'outdoor', 'exploration']):
            return 'Environmental'
        elif any(word in content_lower for word in ['instinct', 'natural', 'digging', 'hunting']):
            return 'Instinctual'
        elif any(word in content_lower for word in ['calm', 'passive', 'relaxing', 'lick']):
            return 'Passive'
        
        # Default to Social for training activities
        return 'Social'
    
    def set_intelligent_defaults(self, activity: dict) -> dict:
        """Set smart defaults based on activity name and content"""
        name_lower = activity['name'].lower()
        
        # Set energy and difficulty based on activity type
        if 'training' in name_lower or 'bonding' in name_lower:
            activity['energy_required'] = 'Low'
            activity['difficulty_level'] = 'Easy'
            activity['tags'] = ['training', 'bonding', 'communication']
        
        # Ensure required fields are not empty
        if not activity['materials']:
            activity['materials'] = ['Basic supplies']
        if not activity['instructions']:
            activity['instructions'] = ['Follow activity guidelines']
        
        return activity
    
    def activity_exists(self, name: str) -> bool:
        """Check if activity already exists"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM activities WHERE name = ?", (name,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists
    
    def show_summary(self):
        """Show database summary"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM activities")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT category, COUNT(*) FROM activities GROUP BY category")
        by_category = cursor.fetchall()
        
        conn.close()
        
        print(f"\n📊 Database Summary:")
        print(f"Total activities: {total}")
        print("By category:")
        for category, count in by_category:
            print(f"  {category}: {count}")

def main():
    print("🐕 Drop Folder Activity Importer")
    print("=" * 40)
    print("Place .txt files with activities in the 'new_activities' folder")
    print("This script will automatically convert and add them to your database")
    print()
    
    importer = DropFolderImporter()
    importer.process_all_files()

if __name__ == "__main__":
    main()
