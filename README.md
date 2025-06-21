# Dog Enrichment Activity Generator

A simple web app that generates personalized enrichment activities for dogs based on their profile.

## Quick Setup

1. **Install Python dependencies:**
   ```bash
   cd /Users/cherilynwood-game/Desktop/dog-enrichment-app
   pip install -r requirements.txt
   ```

2. **Get an OpenAI API key:**
   - Go to https://platform.openai.com/api-keys
   - Create a new API key
   - Copy the `.env.example` file to `.env` and add your key:
   ```bash
   cp .env.example .env
   # Edit .env and add your actual API key
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   - Go to http://127.0.0.1:5000
   - Fill out the 5 questions about your dog
   - Get personalized activities!

## Features

- ✅ 5 simple questions about your dog
- ✅ AI-generated personalized activities
- ✅ Step-by-step instructions
- ✅ Safety notes included
- ✅ Beautiful responsive design
- ✅ Works on mobile and desktop

## Next Steps for MVP

1. **Add payment processing** (Stripe integration)
2. **Deploy to web** (Heroku, Railway, or Vercel)
3. **Add more activity types** 
4. **Improve AI prompts** for better variety
5. **Add user accounts** (optional)

## Cost Estimate

- OpenAI API: ~$0.002 per activity generation
- At $9.99 one-time fee, break even after ~5000 uses
- Hosting: $0-25/month depending on platform

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML/CSS/JavaScript
- **AI:** OpenAI GPT-3.5-turbo
- **Database:** None needed for MVP
- **Payments:** Stripe (to be added)
# Railway deployment
