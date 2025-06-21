# Add this to your app.py file

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
