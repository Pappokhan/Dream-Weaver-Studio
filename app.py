from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from utils.story_generator import generate_story_from_dream
from utils.analyzer import analyze_dream_fun
from utils.dream_classifier import classify_dream_theme
from utils.emotion_detector import detect_emotion
import random
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

VISUAL_STYLES = {
    "fantasy": "watercolor",
    "anxiety": "sketch",
    "adventure": "cartoon",
    "mystery": "cyberpunk",
    "fear": "sketch",
    "romance": "watercolor",
    "joy": "cartoon",
    "exploration": "cyberpunk"
}

@app.route('/')
def landing_page():
    return render_template('home.html')

@app.route('/start')
def home():
    return render_template('index.html')

@app.route('/submit_dream', methods=['POST'])
def submit_dream():
    dream_text = request.form.get("dream")
    if not dream_text:
        return redirect(url_for('home'))

    try:
        theme = classify_dream_theme(dream_text)
        emotion = detect_emotion(dream_text)
        style = VISUAL_STYLES.get(theme, random.choice(list(VISUAL_STYLES.values())))
        story = generate_story_from_dream(dream_text, theme, emotion)
        analysis = analyze_dream_fun(dream_text)
    except Exception as e:
        return jsonify({"error": f"AI service error: {str(e)}"})

    session['result'] = {
        'theme': theme,
        'emotion': emotion,
        'story': story,
        'style': style,
        'image_url': f"/static/images/mock_{style}.jpg",
        'analysis': analysis
    }
    return redirect(url_for('show_result'))

@app.route('/result')
def show_result():
    result = session.get('result')
    if not result:
        return redirect(url_for('home'))
    return render_template('result.html', **result)

if __name__ == '__main__':
    app.run(debug=True)