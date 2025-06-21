#!/usr/bin/env python3
"""
Simple Text Activity Importer

A more robust parser for your specific activity format.
"""

import re
import json
from enrichment_database import EnrichmentDatabase

class SimpleTextImporter:
    def __init__(self):
        self.db = EnrichmentDatabase()
    
    def import_activities_from_file(self, filename: str):
        """Import activities from text file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into individual activities
            # Each activity starts with a title and ends before the next title
            activities = self.split_into_activities(content)
            
            print(f"📝 Found {len(activities)} activities to import")
            
            added_count = 0
            for activity_text in activities:
                activity = self.parse_single_activity(activity_text)
                if activity and activity.get('name'):
                    if not self.activity_exists(activity['name']):
                        try:
                            self.db.add_activity(activity)
                            print(f"  ✅ Added: {activity['name']}")
                            added_count += 1
                        except Exception as e:
                            print(f"  ❌ Error adding {activity['name']}: {e}")
                    else:
                        print(f"  ⏭️  Skipped: {activity['name']} (already exists)")
            
            print(f"\n🎉 Import complete! Added {added_count} activities")
            self.show_summary()
            
        except FileNotFoundError:
            print(f"❌ File {filename} not found!")
    
    def split_into_activities(self, content: str) -> list:
        """Split content into individual activities"""
        # Look for activity titles followed by emoji line
        # Pattern: Title\n🏃 Physical | ⏱ time | etc.
        
        activities = []
        lines = content.split('\n')
        current_activity = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if this is the start of a new activity
            # (title line followed by emoji line)
            if (i < len(lines) - 1 and 
                line and 
                not line.startswith('•') and 
                not line.startswith('Steps:') and
                not line.startswith('You\'ll Need:') and
                not line.startswith('Emotional Goal:') and
                '🏃' in lines[i + 1]):
                
                # Save previous activity if we have one
                if current_activity:
                    activities.append('\n'.join(current_activity))
                
                # Start new activity
                current_activity = [line]
            else:
                # Add to current activity
                current_activity.append(line)
            
            i += 1
        
        # Don't forget the last activity
        if current_activity:
            activities.append('\n'.join(current_activity))
        
        # Filter out very short sections
        return [activity for activity in activities if len(activity) > 100]
    
    def parse_single_activity(self, text: str) -> dict:
        """Parse a single activity"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if len(lines) < 2:
            return {}
        
        # Get activity name (first line)
        name = lines[0]
        
        # Initialize with defaults
        activity = {
            'name': name,
            'category': 'Physical',
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
        
        # Parse the emoji info line (second line)
        if len(lines) > 1 and '🏃' in lines[1]:
            self.parse_info_line(lines[1], activity)
        
        # Find description (usually after emoji line)
        desc_start = 2
        while desc_start < len(lines) and (not lines[desc_start] or lines[desc_start].startswith('🏃')):
            desc_start += 1
        
        # Collect description lines until we hit a section header
        description_lines = []
        i = desc_start
        while i < len(lines):
            line = lines[i]
            if line.startswith('Emotional Goal:') or line.startswith('You\'ll Need:') or line.startswith('Steps:'):
                break
            if line:
                description_lines.append(line)
            i += 1
        
        activity['description'] = ' '.join(description_lines)
        
        # Parse sections
        current_section = None
        for line in lines:
            if line.startswith('Emotional Goal:'):
                current_section = 'emotional_goal'
                continue
            elif line.startswith('You\'ll Need:'):
                current_section = 'materials'
                continue
            elif line.startswith('Steps:'):
                current_section = 'instructions'
                continue
            
            # Process content based on section
            if current_section == 'materials' and line.startswith('•'):
                material = line.replace('•', '').strip()
                if material:
                    activity['materials'].append(material)
            
            elif current_section == 'instructions':
                # Look for numbered steps
                step_match = re.match(r'^(\d+)\.\s*(.+)$', line)
                if step_match:
                    step_text = step_match.group(2)
                    activity['instructions'].append(step_text)
        
        return activity
    
    def parse_info_line(self, info_line: str, activity: dict):
        """Parse the emoji info line and update activity"""
        # Extract time
        time_match = re.search(r'⏱\s*([^|]+)', info_line)
        if time_match:
            activity['estimated_time'] = time_match.group(1).strip()
        
        # Extract location/weather
        if 'Outdoor' in info_line:
            activity['weather_suitable'] = 'Nice weather'
        elif 'Indoor' in info_line:
            activity['weather_suitable'] = 'Any'
        
        # Extract energy level
        if 'High Energy' in info_line:
            activity['energy_required'] = 'High'
        elif 'Low' in info_line and 'Energy' in info_line:
            activity['energy_required'] = 'Low'
        elif 'Moderate' in info_line:
            activity['energy_required'] = 'Medium'
    
    def activity_exists(self, name: str) -> bool:
        """Check if activity exists"""
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
    print("🐕 Simple Text Activity Importer")
    print("=" * 35)
    
    importer = SimpleTextImporter()
    importer.import_activities_from_file('paste.txt')

if __name__ == "__main__":
    main()
