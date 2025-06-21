#!/usr/bin/env python3
"""
Chewing & Bone Activity Generator

Adds comprehensive chewing and bone activities to the passive enrichment category.
Covers recreational vs ingestible bones, safety guidelines, and variety.
"""

from enrichment_database import EnrichmentDatabase
from typing import List, Dict

class ChewingBoneLibrary:
    def __init__(self):
        self.db = EnrichmentDatabase()
    
    def get_chewing_bone_activities(self) -> List[Dict]:
        """Generate comprehensive chewing and bone activities"""
        
        activities = [
            # Recreational Bones
            {
                'name': 'Raw Recreational Bone Session',
                'category': 'Passive',
                'subcategory': 'Recreational Chewing',
                'description': 'Supervised chewing session with appropriate raw recreational bones for dental health and mental stimulation.',
                'materials': [
                    'Raw beef knuckle bone or marrow bone (size-appropriate)',
                    'Towel or washable mat',
                    'Timer for session limits'
                ],
                'instructions': [
                    'Choose bone appropriate for your dog\'s size (larger than their mouth)',
                    'Place dog on towel or mat in designated chewing area',
                    'Give bone and allow 15-30 minutes of supervised chewing',
                    'Remove bone when it becomes small enough to swallow whole',
                    'Store leftover bone in refrigerator for up to 3 days'
                ],
                'safety_notes': 'Never leave dog unattended with bones. Remove when bone becomes small enough to swallow. Refrigerate between sessions. Avoid cooked bones which can splinter.',
                'estimated_time': '15-30 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['Medium', 'Large', 'Giant'],
                'age_groups': ['Young adult', 'Adult'],
                'tags': ['chewing', 'dental_health', 'recreational_bone', 'supervised']
            },
            
            {
                'name': 'Antler Chew Time',
                'category': 'Passive',
                'subcategory': 'Recreational Chewing',
                'description': 'Long-lasting antler chewing for aggressive chewers who need durable recreational options.',
                'materials': [
                    'Naturally shed deer or elk antler (size-appropriate)',
                    'Comfortable chewing spot'
                ],
                'instructions': [
                    'Select antler slightly larger than your dog\'s mouth width',
                    'Introduce antler gradually - start with 10-15 minute sessions',
                    'Monitor for small pieces that might break off',
                    'Allow self-directed chewing while you supervise',
                    'Remove if antler becomes too small or develops sharp edges'
                ],
                'safety_notes': 'Choose antlers appropriate for your dog\'s chewing strength. Remove if cracks develop or pieces break off. Not suitable for senior dogs with dental issues.',
                'estimated_time': '20-60 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['Medium', 'Large', 'Giant'],
                'age_groups': ['Young adult', 'Adult'],
                'tags': ['chewing', 'durable', 'long_lasting', 'recreational']
            },
            
            # Ingestible Chews
            {
                'name': 'Bully Stick Meditation',
                'category': 'Passive',
                'subcategory': 'Ingestible Chewing',
                'description': 'Calming chew session with fully digestible bully sticks for stress relief and quiet time.',
                'materials': [
                    'High-quality bully stick (appropriate thickness)',
                    'Quiet, comfortable area',
                    'Optional: bully stick holder for safety'
                ],
                'instructions': [
                    'Choose bully stick thickness appropriate for dog size',
                    'Set up quiet chewing area away from distractions',
                    'Give bully stick and allow dog to settle into rhythm',
                    'Use bully stick holder when stick becomes short',
                    'Allow dog to fully consume or remove when very small'
                ],
                'safety_notes': 'Monitor for appropriate piece size. Use bully stick holder when stick becomes short to prevent swallowing large pieces. Ensure high-quality, single-ingredient product.',
                'estimated_time': '30-90 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['chewing', 'digestible', 'calming', 'single_ingredient']
            },
            
            {
                'name': 'Frozen Kong Chew Challenge',
                'category': 'Passive',
                'subcategory': 'Enrichment Chewing',
                'description': 'Extended chewing and licking session with frozen Kong filled with dog-safe ingredients.',
                'materials': [
                    'Kong toy (size-appropriate)',
                    'Wet dog food, plain yogurt, or peanut butter',
                    'Small treats or kibble',
                    'Freezer space'
                ],
                'instructions': [
                    'Fill Kong with wet food or safe paste, leaving small air pockets',
                    'Add some kibble or small treats for texture variety',
                    'Seal opening with small amount of paste',
                    'Freeze for 2-4 hours until solid',
                    'Give to dog in appropriate area and allow extended work session'
                ],
                'safety_notes': 'Use only xylitol-free peanut butter. Ensure all ingredients are dog-safe. Monitor for wear on Kong toy and replace when damaged.',
                'estimated_time': '45-120 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['frozen', 'long_lasting', 'food_puzzle', 'licking']
            },
            
            {
                'name': 'Himalayan Yak Chew Session',
                'category': 'Passive',
                'subcategory': 'Ingestible Chewing',
                'description': 'Hard cheese chew that softens as dog works on it, providing extended chewing satisfaction.',
                'materials': [
                    'Himalayan yak chew (size-appropriate)',
                    'Comfortable chewing area',
                    'Microwave for end piece'
                ],
                'instructions': [
                    'Select yak chew appropriate for dog\'s size and chewing strength',
                    'Allow dog to work on chew at their own pace',
                    'Monitor as chew becomes smaller and softer',
                    'When chew becomes small, microwave for 30-60 seconds to puff',
                    'Cool completely before giving puffed piece as final treat'
                ],
                'safety_notes': 'Choose appropriate hardness for your dog. Remove when piece becomes small enough to swallow whole. Always cool microwaved pieces completely.',
                'estimated_time': '60-180 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['Medium', 'Large', 'Giant'],
                'age_groups': ['Young adult', 'Adult'],
                'tags': ['cheese', 'long_lasting', 'digestible', 'hard_chew']
            },
            
            # Dental Health Chews
            {
                'name': 'Dental Chew Routine',
                'category': 'Passive',
                'subcategory': 'Dental Health',
                'description': 'Regular dental chew routine using veterinary-approved products for oral health maintenance.',
                'materials': [
                    'VOHC-approved dental chews',
                    'Fresh water available',
                    'Quiet chewing area'
                ],
                'instructions': [
                    'Choose dental chews with Veterinary Oral Health Council approval',
                    'Follow package directions for frequency (typically daily)',
                    'Allow dog to chew thoroughly rather than gulping',
                    'Ensure fresh water is always available',
                    'Monitor effectiveness and check with vet at regular visits'
                ],
                'safety_notes': 'Choose size-appropriate dental chews. Monitor chewing style to ensure proper breakdown. Consult veterinarian for dogs with dental issues.',
                'estimated_time': '10-20 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['dental_health', 'veterinary_approved', 'daily_routine', 'oral_care']
            },
            
            {
                'name': 'Rope Toy Chew & Fray',
                'category': 'Passive',
                'subcategory': 'Recreational Chewing',
                'description': 'Natural cotton rope toy that provides chewing satisfaction and helps clean teeth through fraying action.',
                'materials': [
                    'Natural cotton rope toy (no synthetic materials)',
                    'Supervision during use'
                ],
                'instructions': [
                    'Provide thick cotton rope toy appropriate for dog size',
                    'Allow dog to chew and fray rope naturally',
                    'Monitor for loose threads that might be swallowed',
                    'Trim any long loose threads to prevent ingestion',
                    'Replace rope when it becomes too frayed or small'
                ],
                'safety_notes': 'Use only natural cotton ropes. Monitor for thread ingestion. Replace when excessively frayed. Not suitable for dogs who gulp non-food items.',
                'estimated_time': '15-45 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['natural', 'dental_cleaning', 'cotton', 'supervised']
            },
            
            # Specialized Chews
            {
                'name': 'Fish Skin Chew Treat',
                'category': 'Passive',
                'subcategory': 'Natural Chewing',
                'description': 'Dehydrated fish skin provides omega-3 rich, easily digestible chewing experience with natural scaling action.',
                'materials': [
                    'Dehydrated fish skin strips (salmon, cod, or similar)',
                    'Clean area for chewing'
                ],
                'instructions': [
                    'Select fish skin appropriate for dog size',
                    'Offer in clean area to minimize mess',
                    'Allow dog to work through skin naturally',
                    'Monitor for appropriate piece sizes',
                    'Can be given 2-3 times per week as healthy treat'
                ],
                'safety_notes': 'Source from reputable suppliers. Ensure no added preservatives or chemicals. Monitor for allergic reactions on first use.',
                'estimated_time': '10-30 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['natural', 'omega_3', 'fish', 'healthy', 'digestible']
            },
            
            {
                'name': 'Frozen Lick Mat Meditation',
                'category': 'Passive',
                'subcategory': 'Soothing Chewing',
                'description': 'Frozen textured mat with spreadable treats provides calming licking and light chewing action.',
                'materials': [
                    'Textured lick mat',
                    'Plain yogurt, wet food, or peanut butter',
                    'Freezer space'
                ],
                'instructions': [
                    'Spread thin layer of dog-safe paste on textured lick mat',
                    'Freeze for 1-2 hours until firm',
                    'Place on easy-to-clean surface',
                    'Allow dog extended licking and gentle chewing session',
                    'Clean mat thoroughly after each use'
                ],
                'safety_notes': 'Use only dog-safe ingredients. Ensure mat material is food-grade silicone. Monitor for wear and replace damaged mats.',
                'estimated_time': '20-45 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['frozen', 'licking', 'calming', 'textured', 'soothing']
            },
            
            {
                'name': 'Rotating Chew Toy Schedule',
                'category': 'Passive',
                'subcategory': 'Enrichment Program',
                'description': 'Systematic rotation of different chew types to maintain interest and provide variety in chewing experiences.',
                'materials': [
                    'Variety of chew toys (3-5 different types)',
                    'Storage container for rotation',
                    'Schedule or calendar for tracking'
                ],
                'instructions': [
                    'Collect 3-5 different safe chew options',
                    'Introduce only 1-2 chews at a time',
                    'Rotate chews every 2-3 days to maintain novelty',
                    'Observe which types your dog prefers',
                    'Adjust rotation based on dog\'s preferences and needs'
                ],
                'safety_notes': 'Inspect all chews before each use. Remove damaged items immediately. Ensure all chews are appropriate for your dog\'s size and chewing style.',
                'estimated_time': 'Ongoing program',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['rotation', 'variety', 'program', 'systematic', 'enrichment']
            }
        ]
        
        return activities
    
    def add_chewing_activities_to_database(self):
        """Add all chewing and bone activities to the database"""
        activities = self.get_chewing_bone_activities()
        
        print("🦴 Adding Chewing & Bone Activities to Passive Enrichment")
        print("=" * 55)
        
        added_count = 0
        for activity in activities:
            try:
                if not self.activity_exists(activity['name']):
                    self.db.add_activity(activity)
                    print(f"  ✅ Added: {activity['name']}")
                    added_count += 1
                else:
                    print(f"  ⏭️  Skipped: {activity['name']} (already exists)")
            except Exception as e:
                print(f"  ❌ Error adding {activity['name']}: {e}")
        
        print(f"\n📊 Added {added_count} chewing and bone activities!")
        self.show_passive_summary()
    
    def activity_exists(self, name: str) -> bool:
        """Check if activity already exists"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM activities WHERE name = ?", (name,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists
    
    def show_passive_summary(self):
        """Show summary of passive activities"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM activities WHERE category = 'Passive'")
        passive_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT subcategory, COUNT(*) FROM activities WHERE category = 'Passive' GROUP BY subcategory")
        by_subcategory = cursor.fetchall()
        
        conn.close()
        
        print(f"\n🦴 Passive Enrichment Summary:")
        print(f"Total Passive activities: {passive_count}")
        if by_subcategory:
            print("By subcategory:")
            for subcategory, count in by_subcategory:
                subcategory_name = subcategory if subcategory else "General"
                print(f"  {subcategory_name}: {count}")

def main():
    print("🦴 Chewing & Bone Activity Library")
    print("=" * 40)
    print("Adding comprehensive chewing activities to your passive enrichment library")
    print()
    
    library = ChewingBoneLibrary()
    library.add_chewing_activities_to_database()
    
    print("\n🎯 Complete! Your passive enrichment now includes:")
    print("  • Recreational vs ingestible bone guidance")
    print("  • Safety protocols for different chew types")
    print("  • Dental health chewing routines")
    print("  • Natural and specialized chew options")
    print("  • Systematic chew rotation programs")

if __name__ == "__main__":
    main()
