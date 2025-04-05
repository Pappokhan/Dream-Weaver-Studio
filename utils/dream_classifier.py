from transformers import pipeline

classifier = pipeline("zero-shot-classification")

LABELS = [
    "adventure", "fantasy", "romance", "anxiety",
    "fear", "mystery", "joy", "exploration"
]

def classify_dream_theme(dream_text: str, threshold: float = 0.3) -> str:
    try:
        result = classifier(dream_text, candidate_labels=LABELS)
        top_label = result["labels"][0]
        top_score = result["scores"][0]

        return top_label if top_score >= threshold else "mystery"

    except Exception as e:
        print(f"[Dream Theme Classification Error] {e}")
        return "mystery"