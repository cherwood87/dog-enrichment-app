from flask import Flask, render_template, request, jsonify, session
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from enrichment_database import EnrichmentDatabase
from chat_assistant import add_chat_routes
from verified_dog_images import get_unique_dog_image, get_multiple_unique_dog_images

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here-change-in-production')  # Change this in production

# Initialize the enrichment database
db = EnrichmentDatabase()

# You'll need to add your API keys here (kept for fallback)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if OPENAI_API_KEY:
    import openai
    openai.api_key = OPENAI_API_KEY
    client = openai
else:
    client = None

# Add chat routes to the app
add_chat_routes(app, OPENAI_API_KEY)

@app.route('/')
def landing():
    # Get UNIQUE images for each section - NO REPEATS
    page_images = {
        'hero': get_unique_dog_image('hero'),
        'mental': get_unique_dog_image('mental_landing'),
        'physical': get_unique_dog_image('physical_landing'),
        'social': get_unique_dog_image('social_landing'),
        'environmental': get_unique_dog_image('environmental_landing'),
        'instinctual': get_unique_dog_image('instinctual_landing'),
        'passive': get_unique_dog_image('passive_landing')
    }
    return render_template('landing.html', images=page_images)

@app.route('/library')
def activity_library():
    # Get all activities from database organized by category
    conn = db.db_path
    import sqlite3
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    # Get all activities with their details
    cursor.execute('''
        SELECT name, category, description, materials, instructions, 
               safety_notes, estimated_time, difficulty_level, energy_required
        FROM activities 
        ORDER BY category, name
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    # Process results and organize by category
    activities_by_category = {
        'Mental': [],
        'Physical': [],
        'Social': [], 
        'Environmental': [],
        'Instinctual': [],
        'Passive': []
    }
    
    import json
    for row in results:
        activity = {
            'name': row[0],
            'category': row[1],
            'description': row[2] or f"A {row[1].lower()} enrichment activity for your dog",
            'materials': json.loads(row[3]),
            'instructions': json.loads(row[4]),
            'safety_notes': row[5],
            'estimated_time': row[6],
            'difficulty_level': row[7] or 'Medium',
            'energy_required': row[8] or 'Medium'
        }
        
        if activity['category'] in activities_by_category:
            activities_by_category[activity['category']].append(activity)
    
    # Get featured activities (first 4 from different categories)
    featured = []
    for category in activities_by_category:
        if activities_by_category[category] and len(featured) < 4:
            featured.append(activities_by_category[category][0])
    
    # Get UNIQUE, DIVERSE images for library page - NO REPEATS
    library_images = {
        'mental': get_multiple_unique_dog_images(6, 'library_mental'),
        'physical': get_multiple_unique_dog_images(6, 'library_physical'), 
        'social': get_multiple_unique_dog_images(6, 'library_social'),
        'environmental': get_multiple_unique_dog_images(6, 'library_environmental'),
        'instinctual': get_multiple_unique_dog_images(6, 'library_instinctual'),
        'passive': get_multiple_unique_dog_images(6, 'library_passive')
    }
    
    return render_template('library.html', 
                         activities_by_category=activities_by_category,
                         featured_activities=featured,
                         images=library_images)

@app.route('/app')
def app_form():
    # Get saved profile from session if available
    saved_profile = session.get('dog_profile', {})
    return render_template('index.html', saved_profile=saved_profile)

@app.route('/checkout')
def checkout():
    # This will be the payment page - for now just redirect to app
    saved_profile = session.get('dog_profile', {})
    return render_template('index.html', saved_profile=saved_profile)

@app.route('/generate-passive', methods=['POST'])
def generate_passive_activities():
    # Get basic dog info if provided
    breed = request.form.get('breed', 'Any dog')
    age = request.form.get('age', 'Any age')
    
    # Create a profile for passive enrichment
    dog_profile = {
        'breed': breed,
        'age': age,
        'enrichment_type': 'Passive'
    }
    
    try:
        # Get passive activities from database
        activities = db.find_matching_activities(dog_profile, limit=4)
        
        # If no passive activities found, get AI-generated ones
        if len(activities) < 4:
            ai_activities = generate_passive_enrichment_activities_ai(f"Dog breed: {breed}, Age: {age}")
            activities.extend(ai_activities[:4-len(activities)])
        
        return render_template('results.html', 
                             activities=activities, 
                             dog_profile=f"Passive Enrichment Ideas for: Dog breed: {breed}, Age: {age}")
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_passive_enrichment_activities_ai(dog_profile):
    """Generate passive enrichment activities using OpenAI API"""
    
    prompt = f"""
    Create 4 specific passive enrichment activities for a dog with this profile: {dog_profile}
    
    Passive enrichment means activities that dogs can do independently without direct human interaction or training. These should be things the dog can enjoy on their own while you're busy or want them to self-entertain.
    
    For each activity, provide:
    1. Activity name
    2. Materials needed (common household items)
    3. Simple setup instructions (2-3 steps)
    4. Safety notes
    5. How long it typically keeps dogs occupied
    
    Focus on:
    - Puzzle toys and food dispensers
    - Sniffing and foraging activities
    - Chew toys and long-lasting treats
    - Environmental enrichment they can explore alone
    - Activities that are safe for unsupervised dogs
    
    Make instructions simple for busy dog owners. Only suggest safe activities.
    
    Format as JSON with this structure:
    {{
        "activities": [
            {{
                "name": "Activity Name",
                "materials": ["item1", "item2"],
                "instructions": ["step1", "step2"],
                "safety_notes": "Safety information",
                "estimated_time": "15-30 minutes"
            }}
        ]
    }}
    """
    
    try:
        if not client:
            raise Exception("OpenAI client not available")
        
        response = client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional dog trainer specializing in passive enrichment and independent dog activities. Focus on safe, unsupervised activities."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        import json
        activities_json = response['choices'][0]['message']['content']
        activities_data = json.loads(activities_json)
        
        return activities_data['activities']
    
    except Exception as e:
        # Fallback passive activities if API fails
        return [
            {
                "name": "Frozen Kong Treat",
                "materials": ["Kong toy", "wet dog food or peanut butter", "treats"],
                "instructions": [
                    "Stuff Kong with wet food or peanut butter",
                    "Add some treats for variety",
                    "Freeze for 2+ hours"
                ],
                "safety_notes": "Use dog-safe peanut butter without xylitol. Supervise initially.",
                "estimated_time": "20-45 minutes"
            },
            {
                "name": "Sniff Mat Foraging",
                "materials": ["towel or blanket", "small treats"],
                "instructions": [
                    "Lay out towel and scatter small treats on it",
                    "Scrunch up the towel to hide treats",
                    "Let your dog find them by sniffing"
                ],
                "safety_notes": "Use appropriate-sized treats to prevent choking. Wash towel regularly.",
                "estimated_time": "10-20 minutes"
            }
        ]

@app.route('/generate-activities', methods=['POST'])
def generate_activities():
    # Get form data
    breed = request.form['breed']
    age = request.form['age']
    energy_level = request.form['energy_level']
    weather = request.form['weather']
    enrichment_type = request.form['enrichment_type']
    
    # Create dog profile for database matching
    dog_profile = {
        'breed': breed,
        'age': age,
        'energy_level': energy_level,
        'weather': weather,
        'enrichment_type': enrichment_type
    }
    
    # Save profile to session for future use
    session['dog_profile'] = dog_profile
    
    try:
        # Get activities from database
        print(f"DEBUG: Calling database with profile: {dog_profile}")
        activities = db.find_matching_activities(dog_profile, limit=4)
        print(f"DEBUG: Database returned {len(activities)} activities")
        
        # If we don't have enough activities, fall back to AI
        if len(activities) < 4:
            print(f"DEBUG: Only got {len(activities)} from database, falling back to AI")
            ai_activities = generate_enrichment_activities_ai(dog_profile)
            activities.extend(ai_activities[:4-len(activities)])
        else:
            print("DEBUG: Using database activities only")
        
        # Create profile summary for display
        profile_summary = f"Dog breed: {breed}, Age: {age}, Energy level: {energy_level}, Weather: {weather}, Preferred enrichment: {enrichment_type}"
        
        # Get breed-appropriate UNIQUE image
        breed_image = get_unique_dog_image(f'results_{breed}')
        
        return render_template('results.html', 
                             activities=activities, 
                             dog_profile=profile_summary,
                             breed_image=breed_image)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_enrichment_activities_ai(dog_profile):
    """Fallback AI generation when database doesn't have enough activities"""
    profile_str = f"Dog breed: {dog_profile['breed']}, Age: {dog_profile['age']}, Energy level: {dog_profile['energy_level']}, Weather: {dog_profile['weather']}, Preferred enrichment: {dog_profile['enrichment_type']}"
    
    prompt = f"""
    Create 4 specific, safe enrichment activities for a dog with this profile: {profile_str}
    
    For each activity, provide:
    1. Activity name
    2. Materials needed
    3. Step-by-step instructions (3-5 steps)
    4. Safety notes
    5. Estimated time
    
    Focus on activities appropriate for the weather and enrichment type requested.
    Make instructions clear and beginner-friendly.
    Only suggest safe activities with common household items or easily obtainable materials.
    
    Format as JSON with this structure:
    {{
        "activities": [
            {{
                "name": "Activity Name",
                "materials": ["item1", "item2"],
                "instructions": ["step1", "step2", "step3"],
                "safety_notes": "Safety information",
                "estimated_time": "15-20 minutes"
            }}
        ]
    }}
    """
    
    try:
        if not client:
            raise Exception("OpenAI client not available")
        
        response = client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional dog trainer and enrichment specialist. Provide safe, creative activities."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        import json
        activities_json = response['choices'][0]['message']['content']
        activities_data = json.loads(activities_json)
        
        return activities_data['activities']
    
    except Exception as e:
        # Final fallback
        return [
            {
                "name": "Sniff & Find Treats",
                "materials": ["small treats", "towel or blanket"],
                "instructions": [
                    "Hide small treats under a towel or blanket",
                    "Encourage your dog to sniff and find them",
                    "Start easy and make it harder as they get better",
                    "Praise them when they find treats"
                ],
                "safety_notes": "Use dog-safe treats only. Supervise to prevent eating towel.",
                "estimated_time": "10-15 minutes"
            }
        ]

def generate_enrichment_activities(dog_profile):
    """Generate enrichment activities using OpenAI API"""
    
    prompt = f"""
    Create 4 specific, safe enrichment activities for a dog with this profile: {dog_profile}
    
    For each activity, provide:
    1. Activity name
    2. Materials needed
    3. Step-by-step instructions (3-5 steps)
    4. Safety notes
    5. Estimated time
    
    Focus on activities appropriate for the weather and enrichment type requested.
    Make instructions clear and beginner-friendly.
    Only suggest safe activities with common household items or easily obtainable materials.
    
    Format as JSON with this structure:
    {{
        "activities": [
            {{
                "name": "Activity Name",
                "materials": ["item1", "item2"],
                "instructions": ["step1", "step2", "step3"],
                "safety_notes": "Safety information",
                "estimated_time": "15-20 minutes"
            }}
        ]
    }}
    """
    
    try:
        if not client:
            raise Exception("OpenAI client not available")
        
        response = client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional dog trainer and enrichment specialist. Provide safe, creative activities."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        import json
        activities_data = json.loads(response['choices'][0]['message']['content'])
        
        return activities_data['activities']
    
    except Exception as e:
        # Fallback activities if API fails
        return [
            {
                "name": "Sniff & Find Treats",
                "materials": ["small treats", "towel or blanket"],
                "instructions": [
                    "Hide small treats under a towel or blanket",
                    "Encourage your dog to sniff and find them",
                    "Start easy and make it harder as they get better",
                    "Praise them when they find treats"
                ],
                "safety_notes": "Use dog-safe treats only. Supervise to prevent eating towel.",
                "estimated_time": "10-15 minutes"
            }
        ]

@app.route('/import')
def import_activities():
    """Admin page for importing activities"""
    return render_template('import.html')

@app.route('/import-activity', methods=['POST'])
def import_activity():
    """Add new activity from import form"""
    try:
        data = request.json
        
        # Create activity data structure
        activity_data = {
            'name': data['name'],
            'category': data['category'],
            'subcategory': data.get('subcategory', ''),
            'description': data.get('description', ''),
            'materials': data.get('materials', []),
            'instructions': data.get('instructions', []),
            'safety_notes': data.get('safety_notes', ''),
            'estimated_time': data.get('estimated_time', ''),
            'difficulty_level': data.get('difficulty_level', 'Medium'),
            'energy_required': data.get('energy_required', 'Medium'),
            'weather_suitable': data.get('weather_suitable', 'Any'),
            'breed_sizes': data.get('breed_sizes', ['All']),
            'age_groups': data.get('age_groups', ['All']),
            'tags': data.get('tags', [])
        }
        
        # Add to database
        db.add_activity(activity_data)
        
        return jsonify({'success': True, 'message': f"Activity '{data['name']}' added successfully!"})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/activities', methods=['GET'])
def get_activities():
    """API endpoint to get all activities"""
    import sqlite3
    
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, category, description, materials, instructions,
               safety_notes, estimated_time, difficulty_level, energy_required,
               weather_suitable, breed_sizes, age_groups, tags
        FROM activities 
        ORDER BY category, name
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    activities = []
    import json
    for row in results:
        activities.append({
            'name': row[0],
            'category': row[1],
            'description': row[2],
            'materials': json.loads(row[3]),
            'instructions': json.loads(row[4]),
            'safety_notes': row[5],
            'estimated_time': row[6],
            'difficulty_level': row[7],
            'energy_required': row[8],
            'weather_suitable': row[9],
            'breed_sizes': json.loads(row[10]),
            'age_groups': json.loads(row[11]),
            'tags': json.loads(row[12])
        })
    
    return jsonify(activities)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
