from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def compress_gif(input_path, output_path):
    """ Compress and resize GIF to be under 1MB """
    gif = Image.open(input_path)
    frames = []

    # Reduce GIF size by resizing
    new_size = (gif.width // 2, gif.height // 2)  # Resize by 50%
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_resized = gif.copy().resize(new_size)
        frames.append(frame_resized)

    # Save optimized GIF
    frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=True, loop=0)

    # If still above 1MB, resize further
    while os.path.getsize(output_path) > 1_000_000:
        new_size = (new_size[0] // 2, new_size[1] // 2)  # Resize again
        frames = [frame.resize(new_size) for frame in frames]
        frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=True, loop=0)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["gif"]
        if file.filename == "":
            return "No file selected!"

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "compressed_" + file.filename)

        file.save(input_path)

        # Compress GIF
        compress_gif(input_path, output_path)

        return redirect(url_for("download", filename="compressed_" + file.filename))

    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    return render_template("download.html", filename=filename)

@app.route("/get_file/<filename>")
def get_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
