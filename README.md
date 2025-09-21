# Agentic AI Video Teaser Generator

This project automates the creation of a summary teaser video from a given YouTube URL. It was completed as a qualifying assignment for the Gridplex Digital Agentic AI Internship.

## How it Works

The process is a three-step pipeline orchestrated by Python scripts:
1.  **Download:** The first script downloads the source YouTube video and its timed transcript using `yt-dlp`.
2.  **Analyze:** The second script sends the transcript to the Google Gemini AI with a prompt that asks it to select the most impactful snippets for a 2-3 minute teaser. The result is saved as a structured JSON file.
3.  **Edit:** The final script reads the JSON file and uses FFmpeg to automatically cut the selected snippets from the source video and merge them into a final teaser video.

## How to Run This Project
1.  Clone this repository.
2.  Install the required tools: Python 3.8+ and FFmpeg.
3.  Create and activate a Python virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate
    ```
4.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
5.  Create a `.env` file and add your Gemini API key:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```
6.  Run the scripts in order:
    ```bash
    python 1_download_video.py
    python 2_get_snippets.py
    python 3_create_teaser.py
    ```
