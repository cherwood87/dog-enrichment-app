import sqlite3
import json
from typing import List, Dict, Any
from database_config import ensure_database_directory

class EnrichmentDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = ensure_database_directory()
        else:
            self.db_path = db_path
        self.init_database()
        self.populate_initial_data()
    
    def init_database(self):
        """Initialize the database with activity tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create activities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                description TEXT,
                materials TEXT, -- JSON array
                instructions TEXT, -- JSON array
                safety_notes TEXT,
                estimated_time TEXT,
                difficulty_level TEXT,
                energy_required TEXT,
                weather_suitable TEXT,
                breed_sizes TEXT, -- JSON array
                age_groups TEXT, -- JSON array
                tags TEXT, -- JSON array
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_activity(self, activity_data: Dict[str, Any]):
        """Add a new activity to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activities 
            (name, category, subcategory, description, materials, instructions, 
             safety_notes, estimated_time, difficulty_level, energy_required, 
             weather_suitable, breed_sizes, age_groups, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            activity_data['name'],
            activity_data['category'],
            activity_data.get('subcategory', ''),
            activity_data.get('description', ''),
            json.dumps(activity_data['materials']),
            json.dumps(activity_data['instructions']),
            activity_data['safety_notes'],
            activity_data['estimated_time'],
            activity_data.get('difficulty_level', 'Medium'),
            activity_data.get('energy_required', 'Medium'),
            activity_data.get('weather_suitable', 'Any'),
            json.dumps(activity_data.get('breed_sizes', ['All'])),
            json.dumps(activity_data.get('age_groups', ['All'])),
            json.dumps(activity_data.get('tags', []))
        ))
        
        conn.commit()
        conn.close()
    
    def find_matching_activities(self, dog_profile: Dict[str, str], limit: int = 4) -> List[Dict[str, Any]]:
        """Find activities that match the dog's profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Debug: Print what we're searching for
        print(f"DEBUG: Searching for activities with profile: {dog_profile}")
        
        # Extract profile info
        breed_size = self.extract_breed_size(dog_profile.get('breed', ''))
        age_group = dog_profile.get('age', '')
        energy_level = dog_profile.get('energy_level', '')
        weather = dog_profile.get('weather', '')
        enrichment_type = dog_profile.get('enrichment_type', '')
        
        print(f"DEBUG: Extracted - breed_size: {breed_size}, enrichment_type: {enrichment_type}")
        
        # Create search patterns - fix category matching
        if 'Mental' in enrichment_type:
            category_pattern = '%Mental%'
        elif 'Physical' in enrichment_type:
            category_pattern = '%Physical%'
        elif 'Social' in enrichment_type:
            category_pattern = '%Social%'
        elif 'Environmental' in enrichment_type:
            category_pattern = '%Environmental%'
        elif 'Instinctual' in enrichment_type:
            category_pattern = '%Instinctual%'
        elif 'Passive' in enrichment_type:
            category_pattern = '%Passive%'
        else:
            category_pattern = f"%{enrichment_type.split(' - ')[0] if ' - ' in enrichment_type else enrichment_type}%"
            
        breed_pattern = f"%{breed_size}%"
        age_pattern = f"%{age_group.split(' ')[0] if ' ' in age_group else age_group}%"
        weather_pattern = f"%{weather.split(' - ')[0] if ' - ' in weather else 'Any'}%"
        
        print(f"DEBUG: Search patterns - category: {category_pattern}, breed: {breed_pattern}")
        
        # First, let's see what's actually in the database
        cursor.execute("SELECT name, category FROM activities")
        all_activities = cursor.fetchall()
        print(f"DEBUG: Database contains {len(all_activities)} activities:")
        for activity in all_activities:
            print(f"  - {activity[0]} ({activity[1]})")
        
        # Build dynamic query based on preferences
        query = '''
            SELECT * FROM activities 
            WHERE category LIKE ? 
            AND (breed_sizes LIKE ? OR breed_sizes LIKE ?)
            AND (age_groups LIKE ? OR age_groups LIKE ?)
            AND (weather_suitable LIKE ? OR weather_suitable LIKE ?)
            ORDER BY RANDOM()
            LIMIT ?
        '''
        
        cursor.execute(query, (
            category_pattern, breed_pattern, '%All%',
            age_pattern, '%All%', 
            weather_pattern, '%Any%',
            limit
        ))
        
        results = cursor.fetchall()
        print(f"DEBUG: Found {len(results)} matching activities")
        
        conn.close()
        
        # Convert to dictionaries and parse JSON fields
        activities = []
        for row in results:
            activity = {
                'name': row[1],
                'category': row[2],
                'materials': json.loads(row[5]),
                'instructions': json.loads(row[6]),
                'safety_notes': row[7],
                'estimated_time': row[8]
            }
            activities.append(activity)
            print(f"DEBUG: Returning activity: {activity['name']}")
        
        return activities
    
    def extract_breed_size(self, breed_str: str) -> str:
        """Extract size from breed string"""
        if 'Small' in breed_str:
            return 'Small'
        elif 'Medium' in breed_str:
            return 'Medium'
        elif 'Large' in breed_str:
            return 'Large'
        elif 'Giant' in breed_str:
            return 'Giant'
        else:
            return 'All'
    
    def populate_initial_data(self):
        """Populate database with initial set of diverse activities"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM activities")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        conn.close()
        
        # Add initial activities
        initial_activities = self.get_initial_activities()
        for activity in initial_activities:
            self.add_activity(activity)
    
    def get_initial_activities(self) -> List[Dict[str, Any]]:
        """Return a comprehensive list of initial activities"""
        return [
            # MENTAL ENRICHMENT ACTIVITIES
            {
                'name': 'Frozen Kong Challenge',
                'category': 'Mental',
                'description': 'A mentally stimulating treat-dispensing activity',
                'materials': ['Kong toy', 'wet dog food or peanut butter', 'small treats', 'water'],
                'instructions': [
                    'Stuff the Kong with wet food or peanut butter',
                    'Add small treats throughout for variety',
                    'Fill any gaps with water',
                    'Freeze for 2-4 hours until solid',
                    'Give to your dog and supervise initially'
                ],
                'safety_notes': 'Use xylitol-free peanut butter only. Remove when Kong becomes small enough to swallow whole.',
                'estimated_time': '30-60 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['Adult', 'Young adult', 'Senior'],
                'tags': ['food_puzzle', 'long_lasting', 'solo_activity']
            },
            {
                'name': 'Muffin Tin Treat Hunt',
                'category': 'Mental',
                'description': 'A DIY puzzle using household items',
                'materials': ['12-cup muffin tin', 'tennis balls', 'small treats'],
                'instructions': [
                    'Place treats in each muffin cup',
                    'Cover each cup with a tennis ball',
                    'Show your dog the setup',
                    'Encourage them to remove balls to find treats',
                    'Praise when they solve each cup'
                ],
                'safety_notes': 'Supervise to ensure balls are not destroyed or swallowed. Use appropriately sized balls.',
                'estimated_time': '10-20 minutes',
                'difficulty_level': 'Medium',
                'energy_required': 'Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['Medium', 'Large', 'Giant'],
                'age_groups': ['All'],
                'tags': ['DIY', 'problem_solving', 'treats']
            },
            {
                'name': 'Snuffle Mat Foraging',
                'category': 'Mental',
                'description': 'Encourages natural foraging behavior',
                'materials': ['Snuffle mat or thick towel', 'small treats or kibble'],
                'instructions': [
                    'Scatter treats throughout the snuffle mat fibers',
                    'If using towel, scrunch it up with treats inside',
                    'Present to your dog',
                    'Let them use their nose to find all treats',
                    'Encourage sniffing behavior with praise'
                ],
                'safety_notes': 'Supervise to prevent eating the mat material. Clean mat regularly.',
                'estimated_time': '15-25 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['sniffing', 'foraging', 'instinctual']
            },
            
            # PHYSICAL ENRICHMENT ACTIVITIES
            {
                'name': 'Backyard Agility Course',
                'category': 'Physical',
                'description': 'Build confidence and coordination',
                'materials': ['Pool noodles', 'cones or markers', 'blanket', 'treats'],
                'instructions': [
                    'Set up pool noodles as jumps (low height)',
                    'Create a weaving course with cones',
                    'Lay blanket flat for crawling under',
                    'Guide dog through course slowly',
                    'Reward each successful obstacle'
                ],
                'safety_notes': 'Keep jumps low. Stop if dog shows stress. Ensure safe footing.',
                'estimated_time': '20-30 minutes',
                'difficulty_level': 'Medium',
                'energy_required': 'High',
                'weather_suitable': 'Nice weather',
                'breed_sizes': ['Medium', 'Large'],
                'age_groups': ['Young adult', 'Adult'],
                'tags': ['agility', 'confidence', 'coordination']
            },
            {
                'name': 'Stair Climbing Workout',
                'category': 'Physical',
                'description': 'Great cardio and leg strengthening',
                'materials': ['Stairs', 'leash', 'water bowl'],
                'instructions': [
                    'Start with 2-3 trips up and down',
                    'Walk slowly and let dog set pace',
                    'Take breaks at top and bottom',
                    'Gradually increase repetitions over weeks',
                    'Always provide water after exercise'
                ],
                'safety_notes': 'Not suitable for puppies or dogs with joint issues. Check with vet first.',
                'estimated_time': '10-15 minutes',
                'difficulty_level': 'Medium',
                'energy_required': 'High',
                'weather_suitable': 'Any',
                'breed_sizes': ['Medium', 'Large', 'Giant'],
                'age_groups': ['Young adult', 'Adult'],
                'tags': ['cardio', 'strength', 'indoor']
            },
            {
                'name': 'Swimming Session',
                'category': 'Physical',
                'description': 'Low-impact full body exercise',
                'materials': ['Safe swimming area', 'dog life jacket', 'towels'],
                'instructions': [
                    'Start in shallow water to build confidence',
                    'Use life jacket for safety',
                    'Enter water with your dog initially',
                    'Gradually encourage deeper water',
                    'Keep sessions short at first'
                ],
                'safety_notes': 'Never leave dog unattended. Check water safety. Rinse after swimming.',
                'estimated_time': '20-40 minutes',
                'difficulty_level': 'Medium',
                'energy_required': 'High',
                'weather_suitable': 'Nice weather',
                'breed_sizes': ['All'],
                'age_groups': ['Young adult', 'Adult'],
                'tags': ['swimming', 'low_impact', 'summer']
            },
            
            # SOCIAL ENRICHMENT ACTIVITIES
            {
                'name': 'Training & Bonding Session',
                'category': 'Social',
                'description': 'Strengthen your relationship through learning',
                'materials': ['High-value treats', 'clicker (optional)'],
                'instructions': [
                    'Choose 1-2 new tricks to work on',
                    'Keep sessions short and positive',
                    'Reward every small success',
                    'End on a successful note',
                    'Practice daily for consistency'
                ],
                'safety_notes': 'Use positive reinforcement only. Stop if dog becomes frustrated.',
                'estimated_time': '10-15 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['training', 'bonding', 'communication']
            },
            {
                'name': 'Puppy Playdate',
                'category': 'Social',
                'description': 'Supervised socialization with other dogs',
                'materials': ['Compatible dog friend', 'neutral meeting space'],
                'instructions': [
                    'Meet in neutral territory first',
                    'Keep both dogs on leash initially',
                    'Allow brief sniffing and greeting',
                    'Move to fenced area if all goes well',
                    'Supervise all interactions closely'
                ],
                'safety_notes': 'Ensure both dogs are vaccinated and friendly. Separate if any tension arises.',
                'estimated_time': '30-60 minutes',
                'difficulty_level': 'Medium',
                'energy_required': 'Medium',
                'weather_suitable': 'Nice weather',
                'breed_sizes': ['All'],
                'age_groups': ['Puppy', 'Young adult', 'Adult'],
                'tags': ['socialization', 'play', 'other_dogs']
            },
            
            # ENVIRONMENTAL ENRICHMENT ACTIVITIES
            {
                'name': 'Sensory Garden Exploration',
                'category': 'Environmental',
                'description': 'Explore different textures and scents safely',
                'materials': ['Various safe plants', 'different ground textures', 'leash'],
                'instructions': [
                    'Visit a dog-friendly garden or park',
                    'Allow dog to sniff different plants safely',
                    'Walk on various surfaces (grass, gravel, sand)',
                    'Let them investigate new scents',
                    'Encourage exploration with praise'
                ],
                'safety_notes': 'Research plant safety first. Avoid areas with pesticides or toxic plants.',
                'estimated_time': '20-30 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Low',
                'weather_suitable': 'Nice weather',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['exploration', 'nature', 'sensory']
            },
            {
                'name': 'Indoor Obstacle Course',
                'category': 'Environmental',
                'description': 'Transform your home into an adventure',
                'materials': ['Pillows', 'blankets', 'cardboard boxes', 'treats'],
                'instructions': [
                    'Create tunnels with blankets and chairs',
                    'Make stepping stones with pillows',
                    'Hide treats in cardboard boxes',
                    'Guide dog through the course',
                    'Rearrange weekly for variety'
                ],
                'safety_notes': 'Ensure all obstacles are stable. Remove anything that could be swallowed.',
                'estimated_time': '15-25 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Medium',
                'weather_suitable': 'Indoor weather',
                'breed_sizes': ['Small', 'Medium'],
                'age_groups': ['All'],
                'tags': ['indoor', 'DIY', 'exploration']
            },
            
            # INSTINCTUAL ENRICHMENT ACTIVITIES
            {
                'name': 'Digging Box Adventure',
                'category': 'Instinctual',
                'description': 'Safe outlet for natural digging behavior',
                'materials': ['Large plastic container', 'sand or dirt', 'buried toys', 'treats'],
                'instructions': [
                    'Fill container with clean sand or dirt',
                    'Bury toys and treats throughout',
                    'Show dog the box and encourage digging',
                    'Praise enthusiastic digging',
                    'Refresh with new treasures regularly'
                ],
                'safety_notes': 'Use clean materials only. Supervise to prevent eating sand/dirt.',
                'estimated_time': '20-30 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Medium',
                'weather_suitable': 'Nice weather',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['digging', 'natural_behavior', 'messy_fun']
            },
            {
                'name': 'Scent Trail Hunting',
                'category': 'Instinctual',
                'description': 'Engage their incredible sense of smell',
                'materials': ['Strong-scented treats', 'multiple locations'],
                'instructions': [
                    'Drag treat along ground to create scent trail',
                    'Start with short, simple trails',
                    'Hide jackpot of treats at trail end',
                    'Release dog to follow trail',
                    'Gradually increase trail complexity'
                ],
                'safety_notes': 'Use safe outdoor areas. Avoid areas with other animal waste.',
                'estimated_time': '15-25 minutes',
                'difficulty_level': 'Medium',
                'energy_required': 'Medium',
                'weather_suitable': 'Nice weather',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['scent_work', 'tracking', 'hunting']
            },
            
            # PASSIVE ENRICHMENT ACTIVITIES
            {
                'name': 'Lick Mat Meditation',
                'category': 'Passive',
                'description': 'Calming, self-directed activity',
                'materials': ['Lick mat or plate', 'wet food, yogurt, or peanut butter'],
                'instructions': [
                    'Spread thin layer of food on lick mat',
                    'Freeze for 30 minutes for longer lasting',
                    'Give to dog in quiet area',
                    'Let them work at their own pace',
                    'Clean mat when finished'
                ],
                'safety_notes': 'Use dog-safe ingredients only. Supervise initially to ensure they do not bite mat.',
                'estimated_time': '15-30 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['calming', 'solo', 'licking']
            },
            {
                'name': 'Puzzle Feeder Challenge',
                'category': 'Passive',
                'description': 'Makes mealtime last longer and more engaging',
                'materials': ['Puzzle feeder or slow feeder bowl', 'regular dog food'],
                'instructions': [
                    'Place regular meal portion in puzzle feeder',
                    'Show dog the feeder',
                    'Let them figure out how to access food',
                    'Start with easier puzzles for beginners',
                    'Gradually increase difficulty over time'
                ],
                'safety_notes': 'Ensure puzzle is appropriate size for your dog. Clean regularly.',
                'estimated_time': '20-45 minutes',
                'difficulty_level': 'Medium',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['feeding', 'problem_solving', 'solo']
            }
        ]

# Initialize database
def init_enrichment_db():
    """Initialize the enrichment database"""
    return EnrichmentDatabase()

if __name__ == "__main__":
    # Test the database
    db = EnrichmentDatabase()
    
    # Test matching
    test_profile = {
        'breed': 'Medium breed (25-60 lbs)',
        'age': 'Adult (3-7 years)',
        'energy_level': 'High energy',
        'weather': 'Nice weather',
        'enrichment_type': 'Physical enrichment'
    }
    
    activities = db.find_matching_activities(test_profile)
    print(f"Found {len(activities)} activities:")
    for activity in activities:
        print(f"- {activity['name']}")
