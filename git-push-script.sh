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
git commit -m "✨ Major design system update + Landing page text fixes

🎨 Design System Updates:
- Applied purple gradient background across all pages
- Added floating geometric shapes animation
- Implemented glassmorphism cards with backdrop blur
- Unified color scheme (#2D1B69 for text)
- Consistent button styles and hover effects

🐛 Landing Page Fixes:
- Fixed text cutoff and overlap issues in enrichment cards
- Improved card layout structure and spacing
- Optimized text sizes and positioning
- Better mobile-responsive card design

📱 Mobile Improvements:
- Mobile-first approach with 430px container width
- Responsive breakpoints at 480px
- Touch-friendly button sizes and spacing

🔧 Pages Updated:
- Landing page: Enhanced hero + fixed card text layout
- Library page: Consistent styling with improved search/filter UI
- Form page (index.html): Complete redesign to match design system
- Results page: Unified styling
- Import page: Consistent design patterns

🌟 User Experience:
- Smooth animations and transitions
- Professional glassmorphism aesthetic
- Consistent visual hierarchy
- Fixed text readability issues
- Improved accessibility and usability"

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
