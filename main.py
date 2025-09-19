import os
import whisper
import ollama
from moviepy.editor import VideoFileClip

# Function to transcribe audio with Whisper
def transcribe_audio(audio_path):
    print(" Transcribing audio using Whisper...")
    model = whisper.load_model("base")  # You can change to "small", "medium", "large"
    result = model.transcribe(audio_path)
    return result["text"]

# Function to translate text into multiple languages using Ollama Phi
def translate_text_phi(text, target_languages):
    translations = {}
    for lang in target_languages:
        prompt = f"Translate the following text to {lang}:\n\n{text}"
        response = ollama.chat(
            model="phi",
            messages=[{"role": "user", "content": prompt}]
        )
        #  Correct way to extract translated content
        translations[lang] = response["message"]["content"]
    return translations

# Function to save text to file
def save_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

# ---------------- MAIN SCRIPT ----------------
if __name__ == "__main__":
    video_path = input("Enter video file path (e.g., sample_video.mp4): ").strip()

    if not os.path.exists(video_path):
        print(" File not found:", video_path)
        exit(1)

    # Extract audio from video
    print("Extracting audio...")
    video = VideoFileClip(video_path)
    audio_path = "audio.wav"
    video.audio.write_audiofile(audio_path)

    # Transcribe with Whisper
    transcription = transcribe_audio(audio_path)
    save_to_file("transcription_original.txt", transcription)
    print("Original transcription saved to transcription_original.txt")

    # Translate into multiple languages
    target_languages = ["Hindi", "Spanish", "French"]
    print(" Translating transcription into multiple languages using Phi...")
    translations = translate_text_phi(transcription, target_languages)

    # Save translations
    for lang, translated_text in translations.items():
        filename = f"transcription_{lang}.txt"
        save_to_file(filename, translated_text)
        print(f"Translation in {lang} saved to {filename}")

    print("All done!")

