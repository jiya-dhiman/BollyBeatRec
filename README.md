# BollyBeat Lounge - Music Discovery Reimagined

An AI-powered web application that helps users discover the perfect Bollywood song based on their current mood, activity, or specific "vibe."

## Project Structure
```text
BollyBeat_Lounge/
├── app.py            
├── templates/
│   ├── base.html       
│   ├── index.html      
│   ├── about.html      
│   └── features.html   
└── README.md

## Features
1. **AI Vibe Matching:** Describe any situation (e.g, "A late night drive in the rain"), and the AI finds the perfect Bollywood match with detailed reasong.
2. **Smart Player Integration:** Uses the YouTube IFrame API to play song previews directly within the browser
3. **Intelligent Fallback:** Automateically detects when a music label restricts embedded playback and trainsforms the "Play Audio" button into a direct "Play on Youtube" link.
4. **Modern UI*:* Built with a clean, responsive card-based layout featuring a dedicated dashboard for results

## How it Works
1. **Generation:** The user enters a prompt, which the backend processes to retrieve a song title, movie, and YouTube ID
2. **State Management:** The frontend initalizes an invsible YouTube YT.Player
3. **Error Handling:** If the song is blocked by copyright, the player enters an error state, automatically converting the interface to a direct redirect.

## Tech Stack 
- Python/Flask
- HTML/CSS
- YouTube IFrame API and Google API
