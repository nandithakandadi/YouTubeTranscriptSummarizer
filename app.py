from flask import Flask, request, render_template
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from googletrans import Translator

app = Flask(__name__)

# Configure Gemini API (replace with your actual key)
genai.configure(api_key="mention your API key here")

# Truncate the transcript if it's too large
def truncate_text(text, max_words=5000):
    words = text.split()
    return " ".join(words[:max_words])

# Get YouTube transcript with fallback for language
def get_youtube_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try to get English transcript first
        try:
            transcript_obj = transcript_list.find_transcript(['en'])
            language_code = 'en'
        except:
            # Fallback to first available language
            transcript_obj = transcript_list.find_transcript([t.language_code for t in transcript_list])
            language_code = transcript_obj.language_code

        transcript_data = transcript_obj.fetch()
        transcript_text = " ".join([t['text'] for t in transcript_data])

        return transcript_text, language_code

    except TranscriptsDisabled:
        return None, None
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}", None

# Analyze transcript with Gemini AI (detailed + structured summary)
def analyze_with_gemini(text, language='en'):
    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    prompt = f"""
    Analyze the following YouTube video transcript and generate a comprehensive and structured summary.

    Include the following sections:
    1. Introduction: Briefly describe the topic and purpose of the video.
    2. Key Points: List the main points and arguments made by the speaker(s) in bullet points.
    3. Important Insights: Highlight any significant findings, examples, statistics, or noteworthy insights.
    4. Conclusion: Summarize the overall message, call-to-action, or final takeaway of the video.

    Additional guidelines:
    - Ensure the summary is detailed, informative, and at least 500 words.
    - Make it easy to read with bullet points and headers.
    - If the transcript is in another language, translate and summarize it in English.

    Transcript Language: {language}

    Transcript:
    {text}
    """

    response = model.generate_content(prompt)
    return response.text if response else "Error generating response."

# Extract YouTube video ID from URL
def extract_video_id(url):
    if "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

# Home route
@app.route('/')
def home_page():
    return render_template('home.html')

# Index route
@app.route('/index')
def index():
    return render_template('index.html')

# Analyze route with error handling and truncation
@app.route('/analyze', methods=['POST'])
def analyze():
    youtube_url = request.form.get("youtube_url")
    video_id = extract_video_id(youtube_url)

    if not video_id:
        return render_template('result.html', error="Invalid YouTube URL. Please enter a valid link.")

    transcript_text, language_code = get_youtube_transcript(video_id)

    if not transcript_text or not language_code:
        return render_template('result.html', error="No transcript available for this video. Ensure subtitles are enabled.", video_id=video_id)

    # Translate if not English
    if language_code != 'en':
        translator = Translator()
        translation = translator.translate(transcript_text, dest='en')
        translated_text = translation.text
        language_code = f"{language_code} (translated)"
    else:
        translated_text = transcript_text

    # Truncate transcript to prevent quota exhaustion
    truncated_text = truncate_text(translated_text)

    # Try analyzing with Gemini, handle quota errors
    try:
        summary = analyze_with_gemini(truncated_text, language=language_code)
    except Exception as e:
        error_msg = f"Analysis failed due to API limits: {str(e)}"
        return render_template('result.html', error=error_msg, video_id=video_id)

    return render_template('result.html',
                           transcript=truncated_text,
                           summary=summary,
                           video_id=video_id,
                           language=language_code)

if __name__ == '__main__':
    app.run(debug=True)
