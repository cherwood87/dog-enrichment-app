#!/usr/bin/env python3
"""
Text Activity Importer - Add well-formatted activities to database

This script takes properly formatted activity text and adds it to the database
while preserving the original formatting and structure.
"""

import re
import json
from enrichment_database import EnrichmentDatabase

class TextActivityImporter:
    def __init__(self):
        self.db = EnrichmentDatabase()
    
    def parse_activity_text(self, text_content: str) -> list:
        """Parse activities from formatted text"""
        activities = []
        
        # Split by double newlines or activity headers
        # Look for patterns like "Activity Name\n🏃 Physical"
        activity_sections = re.split(r'\n(?=[A-Z][^\n]*\n🏃)', text_content)
        
        # Also try splitting by just the emoji line patterns
        if len(activity_sections) <= 1:
            activity_sections = text_content.split('\n\n')
        
        for section in activity_sections:
            section = section.strip()
            if len(section) < 100:  # Skip very short sections
                continue
            
            # Check if this looks like an activity (has name + emoji line)
            lines = section.split('\n')
            if len(lines) >= 2 and '🏃' in lines[1]:
                activity = self.parse_single_activity(section)
                if activity and activity.get('name'):
                    activities.append(activity)
        
        return activities
    
    def parse_single_activity(self, text: str) -> dict:
        """Parse a single activity from text"""
        lines = text.split('\n')
        
        if not lines:
            return {}
        
        # Extract activity name (first line)
        name = lines[0].strip()
        if not name:
            return {}
        
        # Initialize activity
        activity = {
            'name': name,
            'category': 'Physical',  # Default, will be updated
            'subcategory': '',
            'description': '',
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
        
        # Parse the formatted info line (🏃 Physical | ⏱ 5–7 minutes | etc.)
        if len(lines) > 1:
            info_line = lines[1]
            activity.update(self.parse_info_line(info_line))
        
        # Parse description (usually the third line)
        if len(lines) > 2:
            activity['description'] = lines[2].strip()
        
        # Parse sections
        current_section = None
        section_content = []
        
        for line in lines[3:]:
            line = line.strip()
            if not line:
                continue
            
            # Identify sections
            if line.startswith('Emotional Goal:'):
                current_section = 'emotional_goal'
                section_content = []
                continue
            elif line.startswith('You\'ll Need:'):
                current_section = 'materials'
                section_content = []
                continue
            elif line.startswith('Steps:'):
                current_section = 'instructions'
                section_content = []
                continue
            
            # Add content to current section
            if current_section == 'emotional_goal':
                if activity['description']:
                    activity['description'] += ' ' + line
                else:
                    activity['description'] = line
            elif current_section == 'materials':
                if line.startswith('•'):
                    material = line.replace('•', '').strip()
                    if material:
                        activity['materials'].append(material)
            elif current_section == 'instructions':
                if re.match(r'^\d+\.', line):
                    # Numbered instruction
                    instruction = re.sub(r'^\d+\.\s*', '', line)
                    if instruction:
                        activity['instructions'].append(instruction)
                elif line and not line.startswith('•'):
                    # Continuation of previous instruction
                    if activity['instructions']:
                        activity['instructions'][-1] += ' ' + line
        
        return activity
    
    def parse_info_line(self, info_line: str) -> dict:
        """Parse the emoji info line: 🏃 Physical | ⏱ 5–7 minutes | 🌿 Outdoor | 🔋 Moderate Energy"""
        info = {}
        
        # Extract category
        if '🏃' in info_line and 'Physical' in info_line:
            info['category'] = 'Physical'
        elif '🧠' in info_line or 'Mental' in info_line:
            info['category'] = 'Mental'
        elif '👥' in info_line or 'Social' in info_line:
            info['category'] = 'Social'
        elif '🌿' in info_line and 'Environmental' in info_line:
            info['category'] = 'Environmental'
        elif 'Instinctual' in info_line:
            info['category'] = 'Instinctual'
        elif 'Passive' in info_line:
            info['category'] = 'Passive'
        
        # Extract time
        time_match = re.search(r'⏱\s*([^|]+)', info_line)
        if time_match:
            info['estimated_time'] = time_match.group(1).strip()
        
        # Extract location/weather
        if '🌿' in info_line and 'Outdoor' in info_line:
            info['weather_suitable'] = 'Nice weather'
        elif '🏠' in info_line and ('Indoor' in info_line or 'Indoor or Outdoor' in info_line):
            info['weather_suitable'] = 'Any'
        
        # Extract energy level
        energy_match = re.search(r'🔋\s*([^|]+)', info_line)
        if energy_match:
            energy_text = energy_match.group(1).strip()
            if 'Low' in energy_text:
                info['energy_required'] = 'Low'
            elif 'High' in energy_text:
                info['energy_required'] = 'High'
            elif 'Moderate' in energy_text:
                info['energy_required'] = 'Medium'
        
        return info
    
    def import_text_activities(self, text_content: str):
        """Import activities from text content"""
        print("🐕 Importing activities from text...")
        
        activities = self.parse_activity_text(text_content)
        
        print(f"📝 Found {len(activities)} activities to import")
        
        added_count = 0
        skipped_count = 0
        
        for activity in activities:
            # Check if already exists
            if self.activity_exists(activity['name']):
                print(f"  ⏭️  Skipped: {activity['name']} (already exists)")
                skipped_count += 1
                continue
            
            try:
                self.db.add_activity(activity)
                print(f"  ✅ Added: {activity['name']}")
                added_count += 1
            except Exception as e:
                print(f"  ❌ Error adding {activity['name']}: {e}")
        
        print(f"\n🎉 Import complete!")
        print(f"✅ Added: {added_count} activities")
        print(f"⏭️  Skipped: {skipped_count} activities (already existed)")
        
        self.show_database_summary()
    
    def activity_exists(self, name: str) -> bool:
        """Check if activity already exists"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM activities WHERE name = ?", (name,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists
    
    def show_database_summary(self):
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
    """Main function - can be used interactively or with file input"""
    print("🐕 Text Activity Importer")
    print("=" * 30)
    
    importer = TextActivityImporter()
    
    print("Options:")
    print("1. Import from paste.txt file")
    print("2. Paste text directly")
    print("3. Show current database")
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == '1':
        try:
            with open('paste.txt', 'r', encoding='utf-8') as f:
                text_content = f.read()
            importer.import_text_activities(text_content)
        except FileNotFoundError:
            print("❌ paste.txt file not found!")
    elif choice == '2':
        print("Paste your activity text (press Ctrl+D when done):")
        import sys
        text_content = sys.stdin.read()
        importer.import_text_activities(text_content)
    elif choice == '3':
        importer.show_database_summary()

if __name__ == "__main__":
    main()
