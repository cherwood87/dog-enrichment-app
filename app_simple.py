from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret-key')

@app.route('/')
def landing():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dog Enrichment App</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .hero { text-align: center; background: #f0f8ff; padding: 40px; border-radius: 10px; }
            .cta { background: #4CAF50; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 18px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="hero">
            <h1>🐕 Dog Enrichment Activity Generator</h1>
            <p>Get personalized enrichment activities for your furry friend!</p>
            <button class="cta" onclick="window.location.href='/app'">Get Started</button>
        </div>
        <div style="margin-top: 40px;">
            <h2>✨ Features</h2>
            <ul>
                <li>Personalized activities based on your dog's profile</li>
                <li>Safe, expert-approved enrichment ideas</li>
                <li>Step-by-step instructions</li>
                <li>Activities for all weather conditions</li>
            </ul>
        </div>
    </body>
    </html>
    '''

@app.route('/app')
def app_form():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dog Profile - Dog Enrichment App</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
            .form-group { margin: 20px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            select, input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            .submit-btn { background: #4CAF50; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>🐕 Tell Us About Your Dog</h1>
        <form action="/generate-activities" method="POST">
            <div class="form-group">
                <label for="breed">Dog Breed/Size:</label>
                <select name="breed" required>
                    <option value="">Select breed size...</option>
                    <option value="Small breed (under 25 lbs)">Small breed (under 25 lbs)</option>
                    <option value="Medium breed (25-60 lbs)">Medium breed (25-60 lbs)</option>
                    <option value="Large breed (60-90 lbs)">Large breed (60-90 lbs)</option>
                    <option value="Giant breed (over 90 lbs)">Giant breed (over 90 lbs)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="age">Age:</label>
                <select name="age" required>
                    <option value="">Select age...</option>
                    <option value="Puppy (under 1 year)">Puppy (under 1 year)</option>
                    <option value="Young adult (1-3 years)">Young adult (1-3 years)</option>
                    <option value="Adult (3-7 years)">Adult (3-7 years)</option>
                    <option value="Senior (7+ years)">Senior (7+ years)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="energy_level">Energy Level:</label>
                <select name="energy_level" required>
                    <option value="">Select energy level...</option>
                    <option value="Low energy">Low energy</option>
                    <option value="Medium energy">Medium energy</option>
                    <option value="High energy">High energy</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="weather">Weather/Environment:</label>
                <select name="weather" required>
                    <option value="">Select weather...</option>
                    <option value="Nice weather - outdoor activities">Nice weather - outdoor activities</option>
                    <option value="Indoor weather - inside activities">Indoor weather - inside activities</option>
                    <option value="Any weather - flexible activities">Any weather - flexible activities</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="enrichment_type">Preferred Enrichment Type:</label>
                <select name="enrichment_type" required>
                    <option value="">Select enrichment type...</option>
                    <option value="Mental enrichment - brain games">Mental enrichment - brain games</option>
                    <option value="Physical enrichment - exercise">Physical enrichment - exercise</option>
                    <option value="Social enrichment - bonding">Social enrichment - bonding</option>
                    <option value="Environmental enrichment - exploration">Environmental enrichment - exploration</option>
                    <option value="Instinctual enrichment - natural behaviors">Instinctual enrichment - natural behaviors</option>
                    <option value="Passive enrichment - independent activities">Passive enrichment - independent activities</option>
                </select>
            </div>
            
            <button type="submit" class="submit-btn">Generate Activities! 🎾</button>
        </form>
    </body>
    </html>
    '''

@app.route('/generate-activities', methods=['POST'])
def generate_activities():
    # Get form data
    breed = request.form.get('breed', 'Unknown')
    age = request.form.get('age', 'Unknown')
    energy_level = request.form.get('energy_level', 'Unknown')
    weather = request.form.get('weather', 'Unknown')
    enrichment_type = request.form.get('enrichment_type', 'Unknown')
    
    # Simple fallback activities (no AI for now)
    activities = [
        {
            "name": "Frozen Kong Treat",
            "materials": ["Kong toy", "wet dog food or peanut butter", "treats"],
            "instructions": [
                "Stuff Kong with wet food or peanut butter",
                "Add some treats for variety",
                "Freeze for 2+ hours"
            ],
            "safety_notes": "Use dog-safe peanut butter without xylitol",
            "estimated_time": "20-45 minutes"
        },
        {
            "name": "Sniff & Find Game",
            "materials": ["small treats", "towel or blanket"],
            "instructions": [
                "Hide small treats under a towel",
                "Encourage your dog to sniff and find them",
                "Start easy and make it harder"
            ],
            "safety_notes": "Use dog-safe treats only",
            "estimated_time": "10-15 minutes"
        },
        {
            "name": "Puzzle Feeding",
            "materials": ["muffin tin", "tennis balls", "dog food"],
            "instructions": [
                "Place food in muffin tin cups",
                "Cover each cup with a tennis ball",
                "Let your dog figure out how to get the food"
            ],
            "safety_notes": "Supervise to ensure balls aren't swallowed",
            "estimated_time": "15-25 minutes"
        }
    ]
    
    profile_summary = f"{breed}, {age}, {energy_level}, {weather}, {enrichment_type}"
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Your Activities - Dog Enrichment App</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
            .profile {{ background: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
            .activity {{ border: 1px solid #ddd; padding: 20px; margin: 20px 0; border-radius: 10px; }}
            .activity h3 {{ color: #4CAF50; margin-top: 0; }}
            ul {{ padding-left: 20px; }}
            .safety {{ background: #fff3cd; padding: 10px; border-radius: 5px; margin: 10px 0; }}
            .back-btn {{ background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>🎾 Your Personalized Activities</h1>
        
        <div class="profile">
            <h2>📋 Dog Profile</h2>
            <p>{profile_summary}</p>
        </div>
        
        {''.join([f'''
        <div class="activity">
            <h3>{activity["name"]}</h3>
            <p><strong>⏱️ Estimated Time:</strong> {activity["estimated_time"]}</p>
            
            <h4>🛠️ Materials Needed:</h4>
            <ul>
                {''.join([f"<li>{material}</li>" for material in activity["materials"]])}
            </ul>
            
            <h4>📝 Instructions:</h4>
            <ol>
                {''.join([f"<li>{instruction}</li>" for instruction in activity["instructions"]])}
            </ol>
            
            <div class="safety">
                <strong>⚠️ Safety Notes:</strong> {activity["safety_notes"]}
            </div>
        </div>
        ''' for activity in activities])}
        
        <p><a href="/app" class="back-btn">← Try Again</a></p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
