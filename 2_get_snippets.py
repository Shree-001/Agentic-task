import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def parse_vtt(vtt_content):
    """
    Parses the content of a VTT file and returns a clean transcript string.
    """
    lines = vtt_content.strip().split('\n')
    transcript = []
    # State machine to handle multi-line cues
    in_cue_text = False
    
    for line in lines:
        # Skip empty lines, WEBVTT header, and style blocks
        if not line.strip() or line.strip().startswith('WEBVTT') or '::cue' in line:
            in_cue_text = False
            continue
        # A line with '-->' indicates a time cue, the text follows
        if '-->' in line:
            in_cue_text = True
            continue
        # If we are in a cue text block, append the line
        if in_cue_text:
            transcript.append(line.strip())
            
    # Join all transcript parts into a single string
    return ' '.join(transcript)

# --- Main execution ---
VTT_FILE = "downloaded_video.en.vtt"
SNIPPETS_FILE = "snippets.json"
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")
if not os.path.exists(VTT_FILE):
    raise FileNotFoundError(f"{VTT_FILE} not found. Please run the download script first.")

# Configure the Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Using a fast and capable model

# Read and parse the VTT file
print(f"Reading and parsing transcript from '{VTT_FILE}'...")
with open(VTT_FILE, 'r', encoding='utf-8') as f:
    vtt_content = f.read()

full_transcript = parse_vtt(vtt_content)
print("Transcript parsed successfully.")

# This is the prompt that instructs the AI. It's the most important part.
prompt = f"""
You are an expert video editor tasked with creating a compelling 2-3 minute summary teaser from a video transcript.
The video is about "the best way to learn how to code."

Your task is to identify the most impactful and informative snippets from the full transcript provided below.

RULES:
1.  The total duration of all combined snippets MUST be between 120 and 180 seconds (2 to 3 minutes).
2.  Select snippets that are engaging, provide key advice, ask rhetorical questions, or present strong opinions. Avoid generic intros or outros.
3.  For each selected snippet, you MUST provide the exact start and end timestamps.
4.  Your final output MUST be a valid JSON array of objects. Each object must have three keys: "start_time", "end_time", and "reason".
5.  The timestamps MUST be in the format "HH:MM:SS.mmm".

Here is the full transcript:
---
{full_transcript}
---

Now, analyze the transcript and provide the JSON output with the selected snippets.
"""

print("Sending request to Gemini AI. This may take a moment...")
try:
    response = model.generate_content(prompt)
    
    # Clean up the response from the AI
    # LLMs sometimes wrap their JSON output in markdown backticks (```json ... ```)
    cleaned_response = re.sub(r'^```json\s*|```\s*$', '', response.text.strip(), flags=re.MULTILINE)
    
    # Parse the JSON string into a Python list
    snippets = json.loads(cleaned_response)
    
    # Save the snippets to a file
    with open(SNIPPETS_FILE, 'w') as f:
        json.dump(snippets, f, indent=4)
        
    print(f"Successfully generated and saved snippets to '{SNIPPIPETS_FILE}'")
    
    # Optional: Print the snippets to the console to verify
    # print("\n--- Generated Snippets ---")
    # print(json.dumps(snippets, indent=2))
    # print("------------------------\n")

except Exception as e:
    print(f"An error occurred while communicating with the AI or processing its response: {e}")
    print("Full response text received:", response.text if 'response' in locals() else "No response received.")