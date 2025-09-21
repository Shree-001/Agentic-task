import yt_dlp
import os

# The URL of the YouTube video
video_url = "https://www.youtube.com/watch?v=0FUFewGHLLg"

# Define the output filenames
video_filename = "downloaded_video.mp4"
vtt_filename = "downloaded_video.en.vtt"

# Set the options for yt-dlp
# We want the best quality mp4 video and the English VTT transcript
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': os.path.splitext(video_filename)[0],  # Use the base filename for output
    'writeautomaticsub': True,
    'subformat': 'vtt',
    'subtitleslangs': ['en'],
    'noplaylist': True, # Ensure we only download a single video
}

print("Starting download...")

# The download process
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    # Rename the VTT file to our desired simple name
    # yt-dlp might name it something like 'downloaded_video.en-US.vtt'
    generated_vtt_path = "downloaded_video.en.vtt" # Default name yt-dlp will likely use
    if os.path.exists(generated_vtt_path):
        os.rename(generated_vtt_path, vtt_filename)
        print(f"Successfully downloaded and saved video as '{video_filename}'")
        print(f"Successfully downloaded and saved transcript as '{vtt_filename}'")
    else:
        # Sometimes the language code is different, let's find it
        found = False
        for file in os.listdir('.'):
            if file.startswith('downloaded_video') and file.endswith('.vtt'):
                os.rename(file, vtt_filename)
                print(f"Successfully downloaded and saved video as '{video_filename}'")
                print(f"Successfully downloaded and saved transcript as '{vtt_filename}'")
                found = True
                break
        if not found:
            print("VTT file not found with expected name. Please check the downloaded files.")


except Exception as e:
    print(f"An error occurred: {e}")