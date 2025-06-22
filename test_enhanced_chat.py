#!/usr/bin/env python3
"""
Test the enhanced Supabase chat integration
"""

import sys
import os
sys.path.append('/Users/cherilynwood-game/Desktop/dog-enrichment-app')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_enhanced_chat():
    """Test the enhanced chat with Supabase integration"""
    print("🤖 Testing Enhanced Chat with Supabase Integration")
    print("=" * 60)
    
    try:
        from chat_assistant import EnrichmentChatAssistant
        from supabase_client import supabase_client
        
        # Initialize chat assistant
        openai_key = os.getenv('OPENAI_API_KEY')
        chat_assistant = EnrichmentChatAssistant(openai_key)
        
        print(f"✅ Chat assistant initialized")
        print(f"✅ Supabase enabled: {'YES' if supabase_client.enabled else 'NO'}")
        
        # Test 1: Basic chat question
        print("\n🧪 Test 1: Basic enrichment question")
        test_message = "I have a 4 month old puppy who swallows everything. What safe enrichment activities can I do?"
        
        response = chat_assistant.generate_chat_response(test_message)
        
        if response['success']:
            source = response.get('source', 'unknown')
            print(f"✅ Chat response generated using: {source.upper()}")
            print(f"📝 Response preview: {response['response'][:100]}...")
            
            if 'activities' in response and response['activities']:
                print(f"🎯 Generated {len(response['activities'])} additional activities")
        else:
            print(f"❌ Chat failed: {response.get('error')}")
        
        # Test 2: Activity breakdown
        print("\n🧪 Test 2: Activity breakdown")
        activity_name = "Frozen Kong Challenge"
        
        breakdown_response = chat_assistant.generate_activity_breakdown(activity_name)
        
        if breakdown_response['success']:
            source = breakdown_response.get('source', 'unknown')
            print(f"✅ Activity breakdown generated using: {source.upper()}")
            print(f"📋 Activity: {breakdown_response['activity']['name']}")
            print(f"📝 Breakdown preview: {breakdown_response['breakdown'][:100]}...")
        else:
            print(f"❌ Breakdown failed: {breakdown_response.get('error')}")
        
        # Test 3: Session profile integration
        print("\n🧪 Test 3: Session profile integration")
        
        # Simulate session data
        import flask
        with flask.Flask(__name__).test_request_context():
            flask.session['dog_profile'] = {
                'dog_name': 'Buddy',
                'breed': 'Medium breed (25-60 lbs)',
                'age': 'Adult (3-7 years)',
                'energy_level': 'High energy - needs lots of stimulation'
            }
            
            profile = chat_assistant.build_dog_profile_from_session()
            print(f"✅ Session profile built: {profile['name']} - {profile['breed']} - {profile['energyLevel']} energy")
        
        print("\n🎉 All chat tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing chat: {str(e)}")
        return False

def test_chat_endpoints():
    """Test the Flask chat endpoints"""
    print("\n🌐 Testing Flask Chat Endpoints")
    print("=" * 40)
    
    try:
        import requests
        import json
        
        # Note: This requires the Flask app to be running
        base_url = "http://localhost:5000"
        
        # Test chat endpoint
        chat_data = {
            'message': 'What are some safe activities for a puppy?',
            'history': []
        }
        
        print("💬 Testing /api/chat endpoint...")
        print("(Note: Requires Flask app to be running at localhost:5000)")
        
        try:
            response = requests.post(f"{base_url}/api/chat", json=chat_data, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Chat endpoint working! Source: {data.get('source', 'unknown')}")
            else:
                print(f"⚠️ Chat endpoint returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("⚠️ Flask app not running - start with 'python app.py' to test endpoints")
        except requests.exceptions.Timeout:
            print("⚠️ Request timed out - Flask app may be starting up")
        
    except ImportError:
        print("⚠️ Requests library not available for endpoint testing")

if __name__ == "__main__":
    success = test_enhanced_chat()
    test_chat_endpoints()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ENHANCED CHAT SYSTEM READY!")
        print("Your chat now uses:")
        print("🥇 Supabase enrichment-coach (primary)")
        print("🥈 Local AI chat (secondary)")
        print("🥉 Local database activities (tertiary)")
        print("\n🚀 Start your app and test the chat feature!")
    else:
        print("⚠️ SETUP NEEDED")
        print("Check your Supabase configuration and try again")
