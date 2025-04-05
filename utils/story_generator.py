from transformers import pipeline
import re

# Load the GPT-2 model once
story_pipeline = pipeline("text-generation", model="gpt2")

def generate_story_from_dream(dream_text: str, theme: str = None, emotion: str = None) -> str:
    """
    Generate a vivid short story from a dream description using a transformer-based text generator.

    Args:
        dream_text (str): The user's dream description.
        theme (str, optional): Theme to influence the story (e.g., 'fantasy', 'mystery').
        emotion (str, optional): Emotion/tone for the story (e.g., 'joy', 'fear').

    Returns:
        str: A generated story inspired by the dream.
    """
    theme = theme or "mystery"
    emotion = emotion or "curious"

    prompt = (
        f"You are a poetic AI storyteller. Based on the dream below, write a beautiful and short fantasy story. "
        f"The story should reflect the theme of '{theme}' and convey a tone of '{emotion}'.\n\n"
        f"Dream: \"{dream_text}\"\n\n"
        f"Story:"
    )

    try:
        result = story_pipeline(
            prompt,
            max_length=280,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.9,
            num_return_sequences=1,
            pad_token_id=50256
        )

        full_output = result[0]["generated_text"]

        # Extract story after "Story:"
        story = full_output.split("Story:", 1)[-1].strip()

        # Clean up the result: keep full sentences, remove model weirdness
        story = re.sub(r"\n+", " ", story)
        story = re.sub(r"\s{2,}", " ", story)
        sentences = re.split(r'(?<=[.!?]) +', story)
        trimmed_story = " ".join(sentences[:6])  # Keep first ~6 sentences

        return trimmed_story.strip()

    except Exception as e:
        print(f"[Story Generator Error] {e}")
        return "Sorry, the dream weaver had a hiccup while spinning your tale. Try again!"