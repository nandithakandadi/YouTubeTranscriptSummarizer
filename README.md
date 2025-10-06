# YouTube Transcript Summarizer

## Overview
The **YouTube Transcript Summarizer** is a Python-based web application that automatically retrieves YouTube video transcripts, translates them if necessary, and generates a detailed, structured summary using Gemini AI. This tool makes it easy to quickly understand the content of YouTube videos by providing a clear summary including an introduction, key points, important insights, and a conclusion.

---

## Features
- Extract transcripts from YouTube videos, with fallback to available languages.
- Translate non-English transcripts to English using Google Translate.
- Generate detailed and structured summaries using Gemini AI.
- Web interface built with Flask for easy user interaction.
- Handles errors gracefully, including invalid URLs, unavailable transcripts, and API limits.

---

## Technologies Used
- Python
- Flask – Web framework  
- Google Generative AI (Gemini) – For summarization  
- youtube-transcript-api – Extract video transcripts  
- googletrans – Translate transcripts  
- HTML/CSS – Frontend templates

---

## Installation

1. Clone the repository

git clone https://github.com/yourusername/YouTube-Transcript-Summarizer.git
cd YouTube-Transcript-Summarizer

2. Create a virtual environment

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Install dependencies

pip install -r requirements.txt

4. Configure Gemini API

Open app.py
Replace genai.configure(api_key="mention your API key here") with your actual Gemini API key.

## Usage

1. Run the Flask app:

   python app.py

2. Enter a YouTube video URL and click Analyze

3. View the transcript, translation (if applicable), and AI-generated summary.

## Folder Structure Recommended

YouTube-Transcript-Summarizer/
│
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── home.html
│   ├── index.html
│   └── result.html
└── static/ (optional: for CSS, images, or JS files)

## Sample Output

Transcript: Full or truncated transcript of the video.
Summary: Structured summary with:
         Introduction
         Key Points (bullet points)
         Important Insights
         Conclusion
## Future Enhancements

Add support for more AI models for summarization.
Enable multi-language summary output.
Include sentiment analysis of the transcript.
Allow exporting summaries to PDF or Word.
