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
        age_group = self.extract_age_group(dog_profile.get('age', ''))
        energy_level = dog_profile.get('energy_level', '')
        weather = self.extract_weather_preference(dog_profile.get('weather', ''))
        enrichment_type = dog_profile.get('enrichment_type', '')
        
        print(f"DEBUG: Extracted - breed_size: {breed_size}, enrichment_type: {enrichment_type}")
        
        # Create search patterns - fix category matching
        enrichment_type_lower = enrichment_type.lower()
        if 'mental' in enrichment_type_lower:
            category_pattern = 'Mental'
        elif 'physical' in enrichment_type_lower:
            category_pattern = 'Physical'
        elif 'social' in enrichment_type_lower:
            category_pattern = 'Social'
        elif 'environmental' in enrichment_type_lower:
            category_pattern = 'Environmental'
        elif 'instinctual' in enrichment_type_lower:
            category_pattern = 'Instinctual'
        elif 'passive' in enrichment_type_lower:
            category_pattern = 'Passive'
        elif 'mixed' in enrichment_type_lower:
            category_pattern = '%'  # Match any category for mixed
        else:
            category_pattern = 'Mental'  # Default fallback
            
        breed_pattern = f"%{breed_size}%"
        age_pattern = f"%{age_group}%"
        weather_pattern = f"%{weather}%"
        
        print(f"DEBUG: Search patterns - category: {category_pattern}, breed: {breed_pattern}")
        
        # First, let's see what's actually in the database
        cursor.execute("SELECT name, category FROM activities")
        all_activities = cursor.fetchall()
        print(f"DEBUG: Database contains {len(all_activities)} activities:")
        for activity in all_activities:
            print(f"  - {activity[0]} ({activity[1]})")
        
        # Build dynamic query based on preferences
        if category_pattern == '%':  # Mixed enrichment - get variety
            query = '''
                SELECT * FROM activities 
                WHERE (breed_sizes LIKE ? OR breed_sizes LIKE ?)
                AND (age_groups LIKE ? OR age_groups LIKE ?)
                AND (weather_suitable LIKE ? OR weather_suitable LIKE ?)
                ORDER BY RANDOM()
                LIMIT ?
            '''
            cursor.execute(query, (
                breed_pattern, '%All%',
                age_pattern, '%All%', 
                weather_pattern, '%Any%',
                limit
            ))
        else:  # Specific category
            query = '''
                SELECT * FROM activities 
                WHERE category = ? 
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
        breed_lower = breed_str.lower()
        if 'small' in breed_lower:
            return 'Small'
        elif 'medium' in breed_lower:
            return 'Medium'
        elif 'large' in breed_lower:
            return 'Large'
        elif 'giant' in breed_lower:
            return 'Giant'
        else:
            return 'All'
    
    def extract_age_group(self, age_str: str) -> str:
        """Extract age group from age string"""
        age_lower = age_str.lower()
        if 'puppy' in age_lower:
            return 'Puppy'
        elif 'young adult' in age_lower:
            return 'Young adult'
        elif 'senior' in age_lower:
            return 'Senior'
        elif 'adult' in age_lower:
            return 'Adult'
        else:
            return 'All'
    
    def extract_weather_preference(self, weather_str: str) -> str:
        """Extract weather preference from weather string"""
        weather_lower = weather_str.lower()
        if 'nice' in weather_lower or 'outdoor' in weather_lower:
            return 'Nice weather'
        elif 'indoor' in weather_lower:
            return 'Indoor weather'
        elif 'mixed' in weather_lower:
            return 'Any'
        else:
            return 'Any'
    
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
            },
            
            # ADDITIONAL MENTAL ENRICHMENT ACTIVITIES
            {
                'name': 'Hide and Seek Treats',
                'category': 'Mental',
                'description': 'Mental stimulation through searching',
                'materials': ['treats', 'various hiding spots'],
                'instructions': [
                    'Start with easy hiding spots your dog can see',
                    'Hide treats around the room while dog watches',
                    'Release dog to find treats',
                    'Gradually make hiding spots more challenging',
                    'Always praise when treats are found'
                ],
                'safety_notes': 'Only hide treats in safe, accessible areas. Avoid small spaces dog could get stuck.',
                'estimated_time': '10-20 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['searching', 'treats', 'indoor']
            },
            {
                'name': 'Cardboard Box Puzzle',
                'category': 'Mental',
                'description': 'DIY puzzle using cardboard boxes',
                'materials': ['cardboard boxes', 'treats', 'tape'],
                'instructions': [
                    'Place treats inside small boxes',
                    'Tape boxes closed lightly',
                    'Let dog figure out how to open boxes',
                    'Start with easy-to-open boxes',
                    'Increase difficulty as dog improves'
                ],
                'safety_notes': 'Remove tape pieces dog might swallow. Supervise to prevent eating cardboard.',
                'estimated_time': '15-25 minutes',
                'difficulty_level': 'Medium',
                'energy_required': 'Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['DIY', 'puzzle', 'recycling']
            },
            
            # ADDITIONAL PHYSICAL ENRICHMENT ACTIVITIES
            {
                'name': 'Indoor Fetch Variations',
                'category': 'Physical',
                'description': 'Fetch games adapted for indoor spaces',
                'materials': ['soft toys', 'hallway or large room'],
                'instructions': [
                    'Use soft toys to prevent damage',
                    'Play in longest available space',
                    'Try "sit and stay" before throwing',
                    'Practice gentle retrieval',
                    'End before dog gets overstimulated'
                ],
                'safety_notes': 'Clear breakable items. Use only soft toys indoors.',
                'estimated_time': '10-15 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Medium',
                'weather_suitable': 'Indoor weather',
                'breed_sizes': ['Small', 'Medium'],
                'age_groups': ['All'],
                'tags': ['fetch', 'indoor', 'exercise']
            },
            {
                'name': 'Treadmill Walking',
                'category': 'Physical',
                'description': 'Controlled exercise using a treadmill',
                'materials': ['dog treadmill or human treadmill', 'treats', 'leash'],
                'instructions': [
                    'Start with treadmill off, let dog explore',
                    'Use treats to encourage stepping on',
                    'Start very slowly once comfortable',
                    'Stay beside dog at all times',
                    'Keep sessions short initially'
                ],
                'safety_notes': 'Never leave dog unattended. Start extremely slowly. Stop if dog shows stress.',
                'estimated_time': '5-15 minutes',
                'difficulty_level': 'Hard',
                'energy_required': 'Medium',
                'weather_suitable': 'Indoor weather',
                'breed_sizes': ['Medium', 'Large'],
                'age_groups': ['Adult', 'Young adult'],
                'tags': ['controlled_exercise', 'indoor', 'training']
            },
            
            # ADDITIONAL SOCIAL ENRICHMENT ACTIVITIES
            {
                'name': 'Basic Obedience Practice',
                'category': 'Social',
                'description': 'Strengthen communication and bonding',
                'materials': ['treats', 'quiet space'],
                'instructions': [
                    'Practice basic commands: sit, stay, come',
                    'Keep sessions short and positive',
                    'Reward immediately for correct responses',
                    'End on a successful command',
                    'Practice daily for best results'
                ],
                'safety_notes': 'Use positive reinforcement only. Stop if dog becomes frustrated.',
                'estimated_time': '5-10 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['training', 'bonding', 'communication']
            },
            {
                'name': 'Gentle Grooming Session',
                'category': 'Social',
                'description': 'Bonding through grooming and touch',
                'materials': ['brush', 'treats', 'calm environment'],
                'instructions': [
                    'Start with short, gentle brushing',
                    'Reward calm behavior with treats',
                    'Gradually increase session length',
                    'Include gentle massage',
                    'Stop if dog becomes uncomfortable'
                ],
                'safety_notes': 'Watch for signs of discomfort. Use appropriate brush for coat type.',
                'estimated_time': '10-20 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['grooming', 'bonding', 'calm']
            },
            
            # ADDITIONAL ENVIRONMENTAL ENRICHMENT ACTIVITIES
            {
                'name': 'Texture Exploration Mat',
                'category': 'Environmental',
                'description': 'Sensory exploration with different textures',
                'materials': ['various textured materials', 'treats', 'large mat or towel'],
                'instructions': [
                    'Arrange different textures on mat (carpet, bubble wrap, towels)',
                    'Hide treats among textures',
                    'Encourage dog to walk on different areas',
                    'Let them explore at their own pace',
                    'Reward brave exploration'
                ],
                'safety_notes': 'Ensure all materials are safe and non-toxic. Supervise to prevent eating materials.',
                'estimated_time': '15-25 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['sensory', 'textures', 'exploration']
            },
            {
                'name': 'Window Bird Watching',
                'category': 'Environmental',
                'description': 'Mental stimulation through observation',
                'materials': ['comfortable spot by window', 'bird feeder outside (optional)'],
                'instructions': [
                    'Set up comfortable viewing spot by window',
                    'Encourage dog to look outside',
                    'Point out birds and movement',
                    'Let them watch at their own pace',
                    'Consider adding bird feeder for more activity'
                ],
                'safety_notes': 'Ensure window is secure. Monitor for over-excitement.',
                'estimated_time': '10-30 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['observation', 'calm', 'visual_stimulation']
            },
            
            # ADDITIONAL INSTINCTUAL ENRICHMENT ACTIVITIES
            {
                'name': 'Sock Ball Hunt',
                'category': 'Instinctual',
                'description': 'Hunting simulation with safe objects',
                'materials': ['clean socks', 'treats', 'hiding spots'],
                'instructions': [
                    'Put treats inside clean socks and tie off',
                    'Hide sock balls around house',
                    'Encourage dog to find and "catch" them',
                    'Let them shake and carry socks',
                    'Retrieve socks to prevent destruction'
                ],
                'safety_notes': 'Use only clean socks. Remove if dog tries to destroy or swallow.',
                'estimated_time': '15-20 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Medium',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['hunting', 'carrying', 'seeking']
            },
            {
                'name': 'Backyard Sniff Safari',
                'category': 'Instinctual',
                'description': 'Structured sniffing exploration',
                'materials': ['leash', 'various scented items', 'treats'],
                'instructions': [
                    'Let dog lead with nose during walk',
                    'Allow extra time for sniffing',
                    'Hide treats in grass for them to find',
                    'Encourage investigation of new scents',
                    'Follow their nose, not a set path'
                ],
                'safety_notes': 'Avoid areas with unknown substances. Watch for harmful plants or objects.',
                'estimated_time': '20-30 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Low',
                'weather_suitable': 'Nice weather',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['sniffing', 'exploration', 'outdoor']
            },
            
            # ADDITIONAL PASSIVE ENRICHMENT ACTIVITIES
            {
                'name': 'Frozen Treat Popsicle',
                'category': 'Passive',
                'description': 'Long-lasting frozen enrichment',
                'materials': ['ice cube trays', 'dog-safe broth', 'small treats'],
                'instructions': [
                    'Fill ice cube trays with low-sodium broth',
                    'Add small treats to each cube',
                    'Freeze for several hours',
                    'Give to dog outside or on towel',
                    'Let them lick and chew at own pace'
                ],
                'safety_notes': 'Use only dog-safe ingredients. Give on easy-to-clean surface.',
                'estimated_time': '30-60 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['frozen', 'long_lasting', 'cooling']
            },
            {
                'name': 'Benebone or Chew Toy Session',
                'category': 'Passive',
                'description': 'Independent chewing satisfaction',
                'materials': ['appropriate chew toy', 'quiet space'],
                'instructions': [
                    'Choose size-appropriate chew toy',
                    'Give to dog in comfortable spot',
                    'Let them chew independently',
                    'Check toy condition periodically',
                    'Replace when worn down'
                ],
                'safety_notes': 'Choose appropriate size. Remove when too small or damaged.',
                'estimated_time': '20-60 minutes',
                'difficulty_level': 'Easy',
                'energy_required': 'Very Low',
                'weather_suitable': 'Any',
                'breed_sizes': ['All'],
                'age_groups': ['All'],
                'tags': ['chewing', 'independent', 'calming']
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
