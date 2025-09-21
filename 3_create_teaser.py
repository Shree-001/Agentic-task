import os
import json
import subprocess

# --- Configuration ---
SNIPPETS_FILE = "snippets.json"
INPUT_VIDEO = "downloaded_video.mp4"
OUTPUT_VIDEO = "teaser_video.mp4"
TEMP_DIR = "temp_clips"

# --- Verification ---
if not os.path.exists(SNIPPETS_FILE):
    raise FileNotFoundError(f"'{SNIPPETS_FILE}' not found. Please run the AI analysis script first.")
if not os.path.exists(INPUT_VIDEO):
    raise FileNotFoundError(f"'{INPUT_VIDEO}' not found. Please run the video download script first.")

# --- Main Execution ---

# 1. Create a temporary directory for clips
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# 2. Read the snippets JSON file
with open(SNIPPETS_FILE, 'r') as f:
    snippets = json.load(f)

clip_files = []
print(f"Found {len(snippets)} snippets to process.")

# 3. Cut each snippet from the original video
for i, snippet in enumerate(snippets):
    start_time = snippet['start_time']
    end_time = snippet['end_time']
    clip_filename = os.path.join(TEMP_DIR, f"clip_{i+1}.mp4")
    
    print(f"Processing clip {i+1}/{len(snippets)}: from {start_time} to {end_time}")
    
    # This is the FFmpeg command to cut a video segment without re-encoding
    # -i: input file
    # -ss: seek to start time
    # -to: go to end time
    # -c copy: copy video and audio streams without re-encoding (very fast)
    command = [
        'ffmpeg',
        '-i', INPUT_VIDEO,
        '-ss', start_time,
        '-to', end_time,
        '-c', 'copy',
        '-y', # Overwrite output file if it exists
        clip_filename
    ]
    
    try:
        # We use subprocess.run to execute the command-line tool
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        clip_files.append(clip_filename)
    except subprocess.CalledProcessError as e:
        print(f"Error cutting clip {i+1}:")
        print("Command:", ' '.join(e.cmd))
        print("Stderr:", e.stderr.decode())
        # Stop execution if a clip fails
        raise

print("\nAll clips have been successfully created.")

# 4. Create the file list for FFmpeg's concat function
concat_list_file = os.path.join(TEMP_DIR, "concat_list.txt")
with open(concat_list_file, 'w') as f:
    for clip_file in clip_files:
        # The required format for ffmpeg is: file '/path/to/clip.mp4'
        f.write(f"file '{os.path.abspath(clip_file)}'\n")

print(f"Concatenation list created at '{concat_list_file}'")

# 5. Merge all the clips into the final video
print("\nMerging clips into the final teaser video...")

# This is the FFmpeg command to concatenate (merge) video files
# -f concat: use the concat demuxer
# -safe 0: needed for security reasons when using absolute paths in the list
# -i: the list file
# -c copy: copy streams without re-encoding
merge_command = [
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', concat_list_file,
    '-c', 'copy',
    '-y',
    OUTPUT_VIDEO
]

try:
    subprocess.run(merge_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"\n🎉 Teaser video successfully created: '{OUTPUT_VIDEO}'")
except subprocess.CalledProcessError as e:
    print("Error merging videos:")
    print("Command:", ' '.join(e.cmd))
    print("Stderr:", e.stderr.decode())
    raise

# 6. Clean up the temporary files and directory
print("\nCleaning up temporary files...")
for clip_file in clip_files:
    os.remove(clip_file)
os.remove(concat_list_file)
os.rmdir(TEMP_DIR)
print("Cleanup complete.")