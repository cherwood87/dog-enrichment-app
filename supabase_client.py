"""
Supabase integration for the Flask dog enrichment app
"""

import os
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class SupabaseClient:
    def __init__(self):
        self.supabase_url = os.environ.get('SUPABASE_URL')
        self.supabase_anon_key = os.environ.get('SUPABASE_ANON_KEY')
        self.discover_activities_url = os.environ.get('SUPABASE_DISCOVER_ACTIVITIES_URL')
        self.enrichment_coach_url = os.environ.get('SUPABASE_ENRICHMENT_COACH_URL')
        self.generate_content_url = os.environ.get('SUPABASE_GENERATE_CONTENT_URL')
        
        if not all([self.supabase_url, self.supabase_anon_key]):
            print("⚠️  Supabase credentials not found - falling back to local mode")
            self.enabled = False
        else:
            self.enabled = True
            
        self.headers = {
            'Authorization': f'Bearer {self.supabase_anon_key}',
            'Content-Type': 'application/json'
        }
    
    def build_dog_profile(self, form_data: Dict[str, str]) -> Dict[str, Any]:
        """Convert Flask form data to Supabase dog profile format"""
        
        # Extract breed info
        breed_text = form_data.get('breed', '')
        if 'Small' in breed_text:
            size = 'Small'
            breed = breed_text.replace(' (under 25 lbs)', '')
        elif 'Medium' in breed_text:
            size = 'Medium' 
            breed = breed_text.replace(' (25-60 lbs)', '')
        elif 'Large' in breed_text:
            size = 'Large'
            breed = breed_text.replace(' (60-90 lbs)', '')
        elif 'Giant' in breed_text:
            size = 'Giant'
            breed = breed_text.replace(' (over 90 lbs)', '')
        else:
            size = 'Medium'
            breed = breed_text
            
        # Extract age
        age_text = form_data.get('age', '')
        if 'Puppy' in age_text:
            age = 0.5
            age_group = 'Puppy'
        elif 'Young adult' in age_text:
            age = 2
            age_group = 'Adult'
        elif 'Senior' in age_text:
            age = 8
            age_group = 'Senior'
        else:  # Adult
            age = 5
            age_group = 'Adult'
            
        # Extract energy level
        energy_text = form_data.get('energy_level', '')
        if 'Low energy' in energy_text:
            energy_level = 'Low'
        elif 'High energy' in energy_text:
            energy_level = 'High'
        else:
            energy_level = 'Medium'
            
        # Extract living situation from weather (rough approximation)
        weather_text = form_data.get('weather', '')
        if 'Indoor' in weather_text:
            living_situation = 'Apartment'
        else:
            living_situation = 'House'
            
        return {
            'name': form_data.get('dog_name', 'My Dog'),
            'breed': breed,
            'size': size,
            'age': age,
            'ageGroup': age_group,
            'energyLevel': energy_level,
            'livingSituation': living_situation,
            'mobilityIssues': [],  # Could be enhanced with form field
            'weatherPreference': form_data.get('weather', ''),
            'enrichmentPreference': form_data.get('enrichment_type', '')
        }
    
    def discover_activities(self, dog_profile: Dict[str, Any], existing_activities: List[Dict] = None, max_activities: int = 4) -> Dict[str, Any]:
        """Call Supabase discover-activities function"""
        if not self.enabled:
            raise Exception("Supabase not configured")
            
        payload = {
            'dogProfile': dog_profile,
            'existingActivities': existing_activities or [],
            'maxActivities': max_activities,
            'qualityThreshold': 0.6
        }
        
        try:
            response = requests.post(
                self.discover_activities_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'activities': data.get('activities', []),
                    'message': data.get('message', 'Activities generated successfully')
                }
            else:
                return {
                    'success': False,
                    'error': f"API error: {response.status_code}",
                    'activities': []
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Request failed: {str(e)}",
                'activities': []
            }
    
    def get_enrichment_coach_advice(self, message: str, dog_profile: Dict[str, Any], activity_context: Dict = None) -> Dict[str, Any]:
        """Get advice from the enrichment coach"""
        if not self.enabled:
            raise Exception("Supabase not configured")
            
        payload = {
            'messages': [{'role': 'user', 'content': message}],
            'dogProfile': dog_profile,
            'activityHistory': [],
            'pillarBalance': {},
            'activityContext': activity_context
        }
        
        try:
            response = requests.post(
                self.enrichment_coach_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'reply': data.get('reply', ''),
                    'activities': data.get('activities', [])
                }
            else:
                return {
                    'success': False,
                    'error': f"API error: {response.status_code}",
                    'reply': 'Sorry, I had trouble connecting to the enrichment coach.'
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Request failed: {str(e)}",
                'reply': 'Sorry, I had trouble connecting to the enrichment coach.'
            }
    
    def convert_activities_to_flask_format(self, supabase_activities: List[Dict]) -> List[Dict]:
        """Convert Supabase activity format to Flask template format"""
        flask_activities = []
        
        for activity in supabase_activities:
            flask_activity = {
                'name': activity.get('title', 'Unnamed Activity'),
                'category': activity.get('pillar', 'Mental').title(),
                'materials': activity.get('materials', []),
                'instructions': activity.get('instructions', []),
                'safety_notes': 'Always supervise your dog during activities.',
                'estimated_time': f"{activity.get('duration', 15)} minutes",
                'difficulty_level': activity.get('difficulty', 'Medium'),
                'energy_required': activity.get('energyLevel', 'Medium'),
                'benefits': activity.get('benefits', ''),
                'emotional_goals': activity.get('emotionalGoals', []),
                'tags': activity.get('tags', []),
                'age_group': activity.get('ageGroup', 'All Ages'),
                'confidence': activity.get('confidence', 0.8)
            }
            flask_activities.append(flask_activity)
            
        return flask_activities

# Global instance
supabase_client = SupabaseClient()
