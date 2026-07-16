import os
import urllib.request
import urllib.parse
import re
import json
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# API Key Check
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)

def get_youtube_id(song_title, movie_name):
    """
    Programmatically searches YouTube for the song and extracts 
    the very first video ID from the search results page.
    """
    if not song_title or not movie_name:
        return None
        
    search_query = f"{song_title} {movie_name} official audio"
    try:
        encoded_query = urllib.parse.urlencode({"search_query": search_query})
        search_url = f"https://www.youtube.com/results?{encoded_query}"
        
        req = urllib.request.Request(
            search_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req) as response:
            html = response.read().decode()
            video_ids = re.findall(r"watch\?v=(\S{11})", html)
            if video_ids:
                return video_ids[0]
    except Exception as e:
        print(f"Scraping error: {e}")
    
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend')
def recommend():
    user_prompt = request.args.get('prompt', '')
    if not user_prompt:
        return jsonify({"error": "Missing prompt"}), 400
    
    ai_instructions = f"""
    You are a Bollywood Music Expert AI. 
    A user is looking for a song recommendation based on this request: "{user_prompt}"
    Respond ONLY with a raw JSON object. No conversational text or markdown code blocks.
    Use this exact JSON structure:
    {{
        "title": "Song Title",
        "movie": "Movie Name",
        "vibe": "e.g., Romantic, Energetic",
        "why": "A short 1-sentence explanation."
    }}
    """
    
    try:
        # Utilizing your working model!
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite", 
            contents=ai_instructions
        )
        
        text = response.text.strip()
        start = text.find('{')
        end = text.rfind('}') + 1
        clean_text = text[start:end]

        song_data = json.loads(clean_text)
        
        # Retrieve YouTube ID
        video_id = get_youtube_id(song_data.get('title', ''), song_data.get('movie', ''))
        song_data['youtube_id'] = video_id

        return jsonify(song_data)

    except Exception as e:
        print(f"--- DEBUG: ERROR OCCURRED: {str(e)} ---")
        return jsonify({"error": "Failed", "details": str(e)}), 500
    
@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)