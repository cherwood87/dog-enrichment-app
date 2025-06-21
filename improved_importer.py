#!/usr/bin/env python3
"""
Improved Drop Folder Importer

Better parsing for activities that may be concatenated or poorly formatted.
"""

import os
import re
import json
from pathlib import Path
from enrichment_database import EnrichmentDatabase

class ImprovedDropFolderImporter:
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
                
                # Check if it's the simple format or the problematic concatenated format
                if self.is_simple_format(content):
                    activities = self.parse_simple_format(content)
                else:
                    activities = self.parse_concatenated_format(content)
                
                print(f"  📝 Found {len(activities)} activities")
                
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
    
    def is_simple_format(self, content: str) -> bool:
        """Check if content is in the simple **Activity Name** format"""
        return '**' in content and 'Materials Needed' in content
    
    def parse_simple_format(self, content: str) -> list:
        """Parse the simple **Activity Name** format"""
        activities = []
        
        # Split by activity headers (lines starting with **)
        activity_sections = re.split(r'\n(?=\*\*[^*]+\*\*\s*$)', content)
        
        for section in activity_sections:
            section = section.strip()
            if len(section) < 50:  # Skip very short sections
                continue
            
            activity = self.parse_single_simple_activity(section)
            if activity:
                activities.append(activity)
        
        return activities
    
    def parse_concatenated_format(self, content: str) -> list:
        """Parse concatenated format where activities are mashed together"""
        activities = []
        
        # Try to identify activity names by looking for patterns
        # Look for lines that might be activity titles (before emoji lines or time indicators)
        lines = content.split('\n')
        
        # Common activity name patterns to look for
        potential_names = []
        
        # Look for lines that could be activity names
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty lines and obvious non-names
            if not line or len(line) < 5 or len(line) > 100:
                continue
            
            # Skip lines that are clearly not names
            if any(skip in line.lower() for skip in [
                'materials needed', 'step-by-step', 'instructions', 'safety notes',
                'estimated time', 'minutes', 'energy', 'indoor', 'outdoor',
                'physical', 'mental', 'social', '🏃', '⏱', '🌿', '🔋', '🧰', '📋'
            ]):
                continue
            
            # Look for potential activity names
            if (
                # Contains common activity words
                any(word in line.lower() for word in [
                    'chase', 'game', 'walk', 'tug', 'play', 'explore', 'find', 
                    'search', 'circuit', 'flow', 'pause', 'catch', 'hide'
                ]) or
                # Capitalized words (likely titles)
                len([w for w in line.split() if w[0].isupper()]) >= 2
            ):
                potential_names.append((i, line))
        
        print(f"  🔍 Found {len(potential_names)} potential activity names:")
        for _, name in potential_names[:5]:  # Show first 5
            print(f"    - {name}")
        
        # For now, create one combined activity from the content
        # This is a fallback when we can't properly separate activities
        if potential_names:
            # Use the first potential name found
            activity_name = potential_names[0][1]
            
            # Extract materials and instructions from the jumbled content
            materials = self.extract_materials_from_text(content)
            instructions = self.extract_instructions_from_text(content)
            
            activity = {
                'name': activity_name,
                'category': 'Physical',  # Will be updated by detect_category
                'subcategory': '',
                'description': f'A {activity_name.lower()} enrichment activity',
                'materials': materials[:10] if materials else ['Basic supplies'],  # Limit to 10 items
                'instructions': instructions[:10] if instructions else ['Follow activity guidelines'],  # Limit to 10 steps
                'safety_notes': 'Supervise your dog during this activity. Stop if dog shows stress.',
                'estimated_time': '5-15 minutes',
                'difficulty_level': 'Medium',
                'energy_required': 'Medium',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': []
            }
            
            activities.append(activity)
        
        return activities
    
    def extract_materials_from_text(self, text: str) -> list:
        """Extract materials from concatenated text"""
        materials = []
        
        # Look for common material words
        material_words = [
            'long line', 'rope toy', 'treats', 'toys', 'cones', 'markers', 
            'space', 'area', 'mat', 'box', 'tug toy', 'kibble', 'props',
            'stool', 'leash', 'field', 'park', 'trail'
        ]
        
        text_lower = text.lower()
        for material in material_words:
            if material in text_lower and material not in materials:
                materials.append(material.title())
        
        return materials
    
    def extract_instructions_from_text(self, text: str) -> list:
        """Extract instruction-like sentences from text"""
        instructions = []
        
        # Look for instruction-like sentences
        sentences = re.split(r'[.!?]\s+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            
            # Look for sentences that sound like instructions
            if (
                len(sentence) > 20 and len(sentence) < 200 and
                any(word in sentence.lower() for word in [
                    'let', 'wait', 'pause', 'move', 'start', 'end', 'repeat',
                    'offer', 'watch', 'cue', 'toss', 'drag', 'sit', 'walk'
                ]) and
                not any(skip in sentence.lower() for skip in [
                    'materials', 'energy', 'minutes', 'outdoor', 'indoor'
                ])
            ):
                instructions.append(sentence)
                if len(instructions) >= 10:  # Limit to 10 instructions
                    break
        
        return instructions
    
    def parse_single_simple_activity(self, text: str) -> dict:
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
            'category': 'Physical',  # Will be updated by detect_category
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
        elif any(word in content_lower for word in ['chase', 'running', 'jumping', 'physical', 'walk', 'tug', 'play']):
            return 'Physical'
        elif any(word in content_lower for word in ['environment', 'outdoor', 'exploration']):
            return 'Environmental'
        elif any(word in content_lower for word in ['instinct', 'natural', 'digging', 'hunting']):
            return 'Instinctual'
        elif any(word in content_lower for word in ['calm', 'passive', 'relaxing', 'lick']):
            return 'Passive'
        
        # Default to Physical for movement activities
        return 'Physical'
    
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
    print("🐕 Improved Drop Folder Activity Importer")
    print("=" * 45)
    print("Place .txt files with activities in the 'new_activities' folder")
    print("This script will automatically parse and add them to your database")
    print()
    
    importer = ImprovedDropFolderImporter()
    importer.process_all_files()

if __name__ == "__main__":
    main()
