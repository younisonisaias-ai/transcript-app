import os
import sys
if 'whisper' in sys.modules:
    del sys.modules['whisper']
import whisper
from flask import Flask, request, jsonify, send_from_directory
from moviepy import VideoFileClip

app = Flask(__name__)

print("Loading Whisper model...")
model = whisper.load_model("tiny")
print("Model ready!")

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')  # ✅ Serves your new HTML file

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"})

    video_file = request.files["video"]
    video_path = "uploaded_video.mp4"
    audio_path = "extracted_audio.mp3"

    video_file.save(video_path)

    try:
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path, logger=None)
        clip.close()

        result = model.transcribe(audio_path)
        transcript = result["text"]

        return jsonify({"transcript": transcript})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        if os.path.exists(video_path): os.remove(video_path)
        if os.path.exists(audio_path): os.remove(audio_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)