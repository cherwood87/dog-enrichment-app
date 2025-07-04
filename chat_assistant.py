#!/usr/bin/env python3
"""
AI Chat Modal Routes - Enhanced with Supabase Integration

Adds intelligent chat support using Supabase enrichment-coach function
with fallback to local chat for reliability.
"""

from flask import request, jsonify, session
import openai
import json
import sqlite3
from enrichment_database import EnrichmentDatabase
from supabase_client import supabase_client

class EnrichmentChatAssistant:
    def __init__(self, openai_api_key):
        if openai_api_key:
            openai.api_key = openai_api_key
            self.client = openai
        else:
            self.client = None
        self.db = EnrichmentDatabase()
    
    def get_relevant_activities(self, user_query: str, limit: int = 3):
        """Get activities relevant to user's query"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        # Search for relevant activities based on keywords
        keywords = self.extract_keywords(user_query)
        
        search_conditions = []
        search_params = []
        
        for keyword in keywords:
            search_conditions.append(
                "(name LIKE ? OR description LIKE ? OR category LIKE ? OR tags LIKE ?)"
            )
            search_params.extend([f'%{keyword}%'] * 4)
        
        if search_conditions:
            query = f"""
                SELECT name, category, description, materials, instructions, safety_notes, estimated_time, age_groups, breed_sizes
                FROM activities 
                WHERE {' OR '.join(search_conditions)}
                LIMIT ?
            """
            search_params.append(limit)
            cursor.execute(query, search_params)
        else:
            # Fallback to random activities
            cursor.execute("SELECT name, category, description, materials, instructions, safety_notes, estimated_time, age_groups, breed_sizes FROM activities ORDER BY RANDOM() LIMIT ?", (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        activities = []
        for row in results:
            activities.append({
                'name': row[0],
                'category': row[1],
                'description': row[2],
                'materials': json.loads(row[3]),
                'instructions': json.loads(row[4]),
                'safety_notes': row[5],
                'estimated_time': row[6],
                'age_groups': json.loads(row[7]),
                'breed_sizes': json.loads(row[8])
            })
        
        return activities
    
    def extract_keywords(self, query: str) -> list:
        """Extract relevant keywords from user query"""
        query_lower = query.lower()
        
        # Age-related keywords
        age_keywords = []
        if any(word in query_lower for word in ['puppy', 'young', '4 month', 'months old']):
            age_keywords.append('puppy')
        if any(word in query_lower for word in ['senior', 'old', 'elderly']):
            age_keywords.append('senior')
        
        # Behavior keywords
        behavior_keywords = []
        if any(word in query_lower for word in ['swallow', 'eats everything', 'gulps']):
            behavior_keywords.append('safe')
        if any(word in query_lower for word in ['destructive', 'chews everything']):
            behavior_keywords.append('chew')
        if any(word in query_lower for word in ['anxious', 'stressed', 'calm']):
            behavior_keywords.append('calming')
        
        # Activity type keywords
        activity_keywords = []
        if any(word in query_lower for word in ['mental', 'brain', 'puzzle']):
            activity_keywords.append('mental')
        if any(word in query_lower for word in ['physical', 'exercise', 'active']):
            activity_keywords.append('physical')
        if any(word in query_lower for word in ['social', 'bonding']):
            activity_keywords.append('social')
        if any(word in query_lower for word in ['passive', 'quiet', 'calm']):
            activity_keywords.append('passive')
        
        # Safety keywords
        safety_keywords = []
        if any(word in query_lower for word in ['safe', 'no bones', 'cant have']):
            safety_keywords.append('safe')
        
        return age_keywords + behavior_keywords + activity_keywords + safety_keywords
    
    def generate_chat_response(self, user_message: str, conversation_history: list = None) -> dict:
        """Generate AI response using Supabase enrichment-coach with local fallback"""
        
        # Try Supabase enrichment-coach first
        if supabase_client.enabled:
            try:
                print("🤖 Using Supabase enrichment-coach for chat")
                
                # Get dog profile from session if available
                dog_profile = self.build_dog_profile_from_session()
                
                # Build messages for Supabase
                messages = []
                if conversation_history:
                    messages.extend(conversation_history[-4:])  # Keep last 4 messages
                messages.append({'role': 'user', 'content': user_message})
                
                # Call Supabase enrichment coach
                result = supabase_client.get_enrichment_coach_advice(
                    user_message, 
                    dog_profile,
                    activity_context=None
                )
                
                if result['success']:
                    print("✅ Supabase enrichment-coach responded successfully")
                    return {
                        'success': True,
                        'response': result['reply'],
                        'activities': result.get('activities', []),
                        'source': 'supabase',
                        'conversation_id': self.generate_conversation_id()
                    }
                else:
                    print(f"❌ Supabase enrichment-coach failed: {result.get('error')}")
                    raise Exception(result.get('error', 'Supabase chat failed'))
                    
            except Exception as e:
                print(f"🔄 Supabase chat failed, falling back to local: {str(e)}")
        
        # Fallback to local chat system
        print("🔄 Using local chat system")
        return self.generate_local_chat_response(user_message, conversation_history)
    
    def build_dog_profile_from_session(self) -> dict:
        """Build dog profile from session data or use defaults"""
        session_profile = session.get('dog_profile', {})
        
        # Convert session data to Supabase format if available
        if session_profile:
            return supabase_client.build_dog_profile(session_profile)
        
        # Default profile if no session data
        return {
            'name': 'Your Dog',
            'breed': 'Mixed',
            'size': 'Medium',
            'age': 3,
            'ageGroup': 'Adult',
            'energyLevel': 'Medium',
            'livingSituation': 'House',
            'mobilityIssues': []
        }
    
    def generate_local_chat_response(self, user_message: str, conversation_history: list = None) -> dict:
        """Original local chat response generation"""
        
        # Get relevant activities for context
        relevant_activities = self.get_relevant_activities(user_message, limit=3)
        
        # Build context for AI
        activities_context = ""
        if relevant_activities:
            activities_context = "Relevant activities from our database:\n"
            for activity in relevant_activities:
                activities_context += f"- {activity['name']} ({activity['category']}): {activity['description']}\n"
                activities_context += f"  Materials: {', '.join(activity['materials'][:3])}\n"
                activities_context += f"  Instructions: {len(activity['instructions'])} steps\n"
                if activity['safety_notes']:
                    activities_context += f"  Safety: {activity['safety_notes'][:100]}...\n"
                activities_context += "\n"
        
        # Create system prompt for enrichment expert
        system_prompt = f"""
        You are an expert dog enrichment specialist and certified trainer. Your job is to help dog owners with enrichment activities and training advice.

        CORE PRINCIPLES:
        1. SAFETY FIRST: Always prioritize dog safety and well-being
        2. BREAK DOWN COMPLEX BEHAVIORS: Explain things in simple, step-by-step terms
        3. PROVIDE CRITERIA: Give clear success criteria for each step before moving forward
        4. PERSONALIZE: Tailor advice to the specific dog's age, size, and situation
        5. BE PRACTICAL: Suggest realistic activities with common household items

        RESPONSE FORMAT:
        - Start with empathy and understanding
        - Break activities into micro-steps with clear criteria
        - Provide 2-3 specific activity recommendations
        - Include safety considerations
        - End with encouragement and next steps

        SPECIAL CONSIDERATIONS:
        - For puppies under 6 months: Focus on safe, size-appropriate activities
        - For dogs who swallow everything: Emphasize supervised activities and safe materials
        - For anxious dogs: Start with calming, low-pressure activities
        - Always mention when to move to the next step

        AVAILABLE ACTIVITIES CONTEXT:
        {activities_context}

        Remember: You're helping real dog owners with real challenges. Be encouraging, practical, and safety-focused.
        """
        
        # Build conversation for AI
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history[-6:])  # Keep last 6 messages for context
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            if not self.client:
                return {
                    'success': False,
                    'error': "OpenAI API not available",
                    'relevant_activities': relevant_activities[:2] if relevant_activities else []
                }
            
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=800,
                temperature=0.7
            )
            
            ai_response = response['choices'][0]['message']['content']
            
            return {
                'success': True,
                'response': ai_response,
                'relevant_activities': relevant_activities[:2],  # Include top 2 activities
                'source': 'local',
                'conversation_id': self.generate_conversation_id()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Sorry, I'm having trouble right now. Please try again. ({str(e)})",
                'relevant_activities': relevant_activities[:2] if relevant_activities else [],
                'source': 'local'
            }
    
    def generate_activity_breakdown(self, activity_name: str) -> dict:
        """Generate detailed breakdown using Supabase coach with local fallback"""
        
        # Try Supabase enrichment-coach for activity-specific help
        if supabase_client.enabled:
            try:
                print(f"🎨 Using Supabase for activity breakdown: {activity_name}")
                
                # Get dog profile from session
                dog_profile = self.build_dog_profile_from_session()
                
                # Get activity details for context
                activity_details = self.get_activity_from_database(activity_name)
                
                if activity_details:
                    # Build activity context for Supabase
                    activity_context = {
                        'activityName': activity_details['name'],
                        'activityPillar': activity_details['category'],
                        'activityDifficulty': activity_details.get('difficulty_level', 'Medium'),
                        'activityDuration': activity_details.get('estimated_time', '15 minutes')
                    }
                    
                    # Ask for detailed breakdown
                    message = f"Please provide a detailed step-by-step breakdown for the '{activity_name}' activity. Include preparation steps, success criteria, troubleshooting tips, and how to make it easier or harder based on my dog's profile."
                    
                    result = supabase_client.get_enrichment_coach_advice(
                        message,
                        dog_profile,
                        activity_context=activity_context
                    )
                    
                    if result['success']:
                        print("✅ Supabase activity breakdown successful")
                        return {
                            'success': True,
                            'activity': activity_details,
                            'breakdown': result['reply'],
                            'additional_activities': result.get('activities', []),
                            'source': 'supabase'
                        }
                    else:
                        print(f"❌ Supabase breakdown failed: {result.get('error')}")
                        raise Exception(result.get('error', 'Supabase breakdown failed'))
                else:
                    print(f"❌ Activity '{activity_name}' not found in database")
                    raise Exception(f"Activity '{activity_name}' not found")
                    
            except Exception as e:
                print(f"🔄 Supabase breakdown failed, falling back to local: {str(e)}")
        
        # Fallback to local breakdown
        print("🔄 Using local activity breakdown")
        return self.generate_local_activity_breakdown(activity_name)
    
    def get_activity_from_database(self, activity_name: str) -> dict:
        """Get activity details from local database"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activities WHERE name = ?", (activity_name,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
            
        return {
            'name': result[1],
            'category': result[2],
            'description': result[4],
            'materials': json.loads(result[5]),
            'instructions': json.loads(result[6]),
            'safety_notes': result[7],
            'estimated_time': result[8],
            'difficulty_level': result[9],
            'energy_required': result[10]
        }
    
    def generate_local_activity_breakdown(self, activity_name: str) -> dict:
        """Original local activity breakdown generation"""
        
        # Get activity from database
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activities WHERE name = ?", (activity_name,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return {
                'success': False,
                'error': f"Activity '{activity_name}' not found in our database.",
                'source': 'local'
            }
        
        activity = {
            'name': result[1],
            'category': result[2],
            'description': result[4],
            'materials': json.loads(result[5]),
            'instructions': json.loads(result[6]),
            'safety_notes': result[7],
            'estimated_time': result[8],
            'difficulty_level': result[9],
            'energy_required': result[10]
        }
        
        # Generate AI breakdown
        breakdown_prompt = f"""
        Break down this dog enrichment activity into micro-steps with clear success criteria:

        Activity: {activity['name']} ({activity['category']})
        Description: {activity['description']}
        Materials: {', '.join(activity['materials'])}
        Instructions: {'. '.join(activity['instructions'])}
        Safety: {activity['safety_notes']}

        Please provide:
        1. PREPARATION STEPS: What to set up before starting
        2. INTRODUCTION PHASE: How to introduce this to the dog
        3. STEP-BY-STEP BREAKDOWN: Each instruction broken into micro-steps
        4. SUCCESS CRITERIA: What to look for before moving to the next step
        5. TROUBLESHOOTING: Common issues and solutions
        6. PROGRESSION: How to make it easier or harder

        Format as clear, numbered steps that a beginner could follow.
        """
        
        try:
            if not self.client:
                return {
                    'success': False,
                    'error': f"OpenAI API not available for activity breakdown.",
                    'activity': activity,
                    'source': 'local'
                }
            
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a dog training expert. Break down activities into the simplest possible steps with clear success criteria."},
                    {"role": "user", "content": breakdown_prompt}
                ],
                max_tokens=1000,
                temperature=0.6
            )
            
            return {
                'success': True,
                'activity': activity,
                'breakdown': response['choices'][0]['message']['content'],
                'source': 'local'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error generating breakdown: {str(e)}",
                'activity': activity,
                'source': 'local'
            }
    
    def generate_conversation_id(self) -> str:
        """Generate unique conversation ID"""
        import time
        import random
        return f"conv_{int(time.time())}_{random.randint(1000, 9999)}"

# Flask routes for chat functionality
def add_chat_routes(app, openai_api_key):
    """Add chat routes to Flask app"""
    
    chat_assistant = EnrichmentChatAssistant(openai_api_key)
    
    @app.route('/api/chat', methods=['POST'])
    def chat_endpoint():
        """Handle chat messages"""
        try:
            data = request.json
            user_message = data.get('message', '').strip()
            conversation_history = data.get('history', [])
            
            if not user_message:
                return jsonify({
                    'success': False,
                    'error': 'Please enter a message'
                }), 400
            
            # Generate response
            response = chat_assistant.generate_chat_response(user_message, conversation_history)
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Chat error: {str(e)}'
            }), 500
    
    @app.route('/api/activity-breakdown', methods=['POST'])
    def activity_breakdown_endpoint():
        """Handle activity breakdown requests"""
        try:
            data = request.json
            activity_name = data.get('activity_name', '').strip()
            
            if not activity_name:
                return jsonify({
                    'success': False,
                    'error': 'Please specify an activity name'
                }), 400
            
            # Generate breakdown
            response = chat_assistant.generate_activity_breakdown(activity_name)
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Breakdown error: {str(e)}'
            }), 500

if __name__ == "__main__":
    # Test the chat assistant
    assistant = EnrichmentChatAssistant("your-api-key-here")
    
    test_query = "I have a 4 month old puppy who swallows everything and cant have bones, I need enrichment ideas for them"
    response = assistant.generate_chat_response(test_query)
    
    print("Test Response:")
    print(response)
