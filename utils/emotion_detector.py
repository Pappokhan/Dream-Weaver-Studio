from transformers import pipeline

emotion_pipeline = pipeline("sentiment-analysis")

EMOTION_MAP = {
    "positive": "joy",
    "negative": "fear",
    "neutral": "calm",
    "joy": "joy",
    "anger": "anger",
    "sadness": "sadness"
}

def detect_emotion(dream_text: str) -> str:
    try:
        result = emotion_pipeline(dream_text)[0]
        label = result.get("label", "neutral").lower()
        return EMOTION_MAP.get(label, label)
    except Exception as e:
        print(f"[Emotion Detection Error] {e}")
        return "curious"  # fallback emotion