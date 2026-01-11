from textblob import TextBlob

def classify_incident(text):
    text = text.lower()

    if "ragging" in text:
        return "Ragging"
    elif "harassment" in text:
        return "Harassment"
    elif "violence" in text or "hit" in text:
        return "Violence"
    elif "abuse" in text:
        return "Verbal Abuse"
    else:
        return "Other"

def sentiment_score(text):
    return TextBlob(text).sentiment.polarity
