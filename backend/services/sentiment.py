"""
GuardianAI - Sentiment Analysis Service

Fast keyword-based sentiment analysis for one-word responses.
Categorizes as: positive, neutral, negative, concerning
"""

import logging

logger = logging.getLogger(__name__)


def analyze_sentiment(one_word: str) -> dict:
    """
    Analyze sentiment of a one-word response using keyword matching.
    
    Fast and deterministic - no API calls, no ML models.
    Sufficient for MVP and runs in < 1ms.
    
    Args:
        one_word: Single word describing student's day
    
    Returns:
        Dict with keys:
        - sentiment: "positive" | "neutral" | "negative" | "concerning"
        - score: float (-1.0 to 1.0)
    
    Examples:
        >>> analyze_sentiment("hopeless")
        {'sentiment': 'concerning', 'score': -0.9}
        >>> analyze_sentiment("tired")
        {'sentiment': 'negative', 'score': -0.6}
        >>> analyze_sentiment("happy")
        {'sentiment': 'positive', 'score': 0.7}
    """
    if not one_word or len(one_word.strip()) == 0:
        return {"sentiment": "neutral", "score": 0.0}
    
    # Keyword lists for sentiment classification
    positive_words = [
        "happy", "good", "great", "excellent", "motivated", "energized", 
        "calm", "focused", "hopeful", "peaceful", "content", "excited",
        "confident", "strong", "better", "fine", "okay", "alright"
    ]
    
    negative_words = [
        "tired", "stressed", "overwhelmed", "anxious", "sad", "exhausted",
        "lost", "struggling", "worried", "confused", "frustrated", "angry",
        "annoyed", "upset", "down", "low", "drained", "burnt"
    ]
    
    concerning_words = [
        "empty", "numb", "hopeless", "worthless", "done", "pointless",
        "broken", "trapped", "alone", "desperate", "nothing", "end",
        "finished", "give up", "quit"
    ]
    
    word_lower = one_word.lower().strip()
    
    # Check for concerning words first (highest priority)
    if word_lower in concerning_words or any(c in word_lower for c in concerning_words):
        logger.warning(f"Concerning sentiment detected: {one_word}")
        return {"sentiment": "concerning", "score": -0.9}
    
    # Check for negative words
    elif word_lower in negative_words or any(n in word_lower for n in negative_words):
        logger.debug(f"Negative sentiment: {one_word}")
        return {"sentiment": "negative", "score": -0.6}
    
    # Check for positive words
    elif word_lower in positive_words or any(p in word_lower for p in positive_words):
        logger.debug(f"Positive sentiment: {one_word}")
        return {"sentiment": "positive", "score": 0.7}
    
    # Unknown word - default to neutral
    else:
        logger.debug(f"Neutral sentiment (unknown word): {one_word}")
        return {"sentiment": "neutral", "score": 0.0}
