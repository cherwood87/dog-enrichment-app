#!/bin/bash

# Navigate to the project directory
cd "/Users/cherilynwood-game/Desktop/dog-enrichment-app"

echo "🚀 Preparing to push Dog Enrichment App changes to GitHub..."

# Check current status
echo "📋 Current Git status:"
git status

echo ""
echo "📁 Adding all changes to staging..."
# Add all changes
git add .

echo ""
echo "💬 Committing changes..."
# Commit with a descriptive message
git commit -m "🚀 Major upgrade: Integrate Supabase AI functions with Flask UI

✨ New Features:
- Supabase integration with smart fallback to local database
- Enhanced dog profile building with name field
- AI-powered activity generation using discover-activities function
- Activity format conversion between Supabase and Flask
- Generation method indicator in results
- Enhanced activity display with benefits and metadata

🔧 Technical Improvements:
- New supabase_client.py with full API integration
- Profile conversion from form data to Supabase format
- Smart error handling and fallback system
- Enhanced results template with rich activity data
- Environment configuration for Supabase credentials

🎯 User Experience:
- Same beautiful glassmorphism UI
- Smarter, more personalized activity recommendations
- Dog name personalization
- Better activity descriptions and benefits
- Seamless experience with improved backend

📊 System Architecture:
- Cloud-based AI generation with local fallback
- Scalable Supabase backend integration
- Maintained Flask frontend for familiar interface
- Enhanced data models for richer activity content"

echo ""
echo "🌐 Pushing to GitHub..."
# Push to the main branch (or master, depending on your setup)
git push origin main 2>/dev/null || git push origin master 2>/dev/null || {
    echo "❓ Couldn't determine the main branch. Trying to push to current branch..."
    git push
}

echo ""
echo "✅ Done! Your changes have been pushed to GitHub."
echo "🔗 Check your repository to see the updates."
