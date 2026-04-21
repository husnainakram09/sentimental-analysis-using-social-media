from ..utils.preprocessing import clean_tweet

LABEL_MAP = {0: "negative", 1: "neutral", 2: "positive"}


def build_prediction(model, text: str) -> dict:
    cleaned = clean_tweet(text)
    probabilities = model.predict_proba([cleaned])[0]
    pred_idx = int(model.predict([cleaned])[0])
    probs_dict = {
        "negative": round(float(probabilities[0]), 4),
        "neutral": round(float(probabilities[1]), 4),
        "positive": round(float(probabilities[2]), 4),
    }
    return {
        "text": text,
        "cleaned_text": cleaned,
        "label": LABEL_MAP[pred_idx],
        "confidence": round(float(max(probabilities)), 4),
        "probabilities": probs_dict,
    }
