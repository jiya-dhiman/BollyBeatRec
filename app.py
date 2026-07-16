import os
import urllib.request
import urllib.parse
import re
import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)

# Updated API Key Check
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_youtube_id(song_title, movie_name):
    """
    Programmatically searches YouTube for the song and extracts 
    the very first video ID from the search results page.
    """
    search_query = f"{song_title} {movie_name} official audio"
    try:
        search_query = f"{song_title} {movie_name} official audio"
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
    
    Think of ANY real Bollywood song from history that best fits their vibe, mood, tempo, or dance needs.
    You must respond ONLY with a raw JSON object containing the song details. Do not add any conversational text or markdown code blocks.
    
    Use this exact JSON structure for your response:
    {{
        "id": 1,
        "title": "Song Title",
        "movie": "Movie Name",
        "vibe": "e.g., Romantic, Energetic, Melancholic",
        "tempo": "e.g., Fast, Medium, Slow",
        "energy": "e.g., High, Medium, Low",
        "dance_difficulty": "e.g., Easy, Medium, Hard",
        "why": "A short 1-sentence personalized explanation why this specific song matches their request."
    }}
    """

    try:
        print("Generating recommendation with high-speed gemini-3.1-flash-lite...")
        response = model.generate_content(ai_instructions)

        # Cleanup response string and parse JSON...
        # (The rest of your logic remains exactly the same)

        # Cleanup response string
        clean_text = response.text.strip()
        if clean_text.startswith("```"):
            lines = clean_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            clean_text = "\n".join(lines).strip()

        song_data = json.loads(clean_text)

        # Retrieve YouTube ID
        video_id = get_youtube_id(song_data['title'], song_data['movie'])
        song_data['youtube_id'] = video_id

        return jsonify(song_data)

    except Exception as e:
        return jsonify({"error": "Failed generating recommendation", "details": str(e)}), 500

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()