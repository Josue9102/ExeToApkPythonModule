from flask import Flask, request, send_file, render_template
import moviepy.editor as mp
import cv2
import numpy as np
import ffmpeg
import os

app = Flask(__name__)

# Explicitly set the path to FFmpeg binary if it's not detected
from moviepy.config import change_settings
change_settings({"FFMPEG_BINARY": "/data/data/com.termux/files/usr/bin/ffmpeg"})  # Replace with your path

UPLOAD_FOLDER = "/uploads"
OUTPUT_FOLDER = "/outputs"
HORROR_INTRO = "intro.mp4"  # Replace with your horror intro video

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def apply_glitch_effect(input_video, output_video):
    cap = cv2.VideoCapture(input_video)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        glitch_frame = frame.copy()
        rows, cols, _ = frame.shape
        glitch_frame[:, :cols//2] = frame[:, cols//2:]  # Shift half the image

        out.write(glitch_frame)

    cap.release()
    out.release()

def merge_videos(intro, main_video, output_video):
    intro_clip = mp.VideoFileClip(intro)
    main_clip = mp.VideoFileClip(main_video)
    final_video = mp.concatenate_videoclips([intro_clip, main_clip])
    final_video.write_videofile(output_video, codec="libx264")

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["video"]
        if file:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            # Apply glitch effect
            glitched_video = os.path.join(OUTPUT_FOLDER, "glitched_" + file.filename)
            apply_glitch_effect(input_path, glitched_video)

            # Merge with intro
            final_video = os.path.join(OUTPUT_FOLDER, "final_" + file.filename)
            merge_videos(HORROR_INTRO, glitched_video, final_video)

            return send_file(final_video, as_attachment=True)

    return render_template("/templates/index.html")

if __name__ == "__main__":
    app.run(debug=True)
