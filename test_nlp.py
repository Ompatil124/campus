# -*- coding: utf-8 -*-
"""
Test script for the enhanced NLP model
Demonstrates text classification, sentiment analysis, and emotion detection
"""

from nlp_model import (
    analyze_incident,
    classify_incident,
    sentiment_score,
    get_sentiment_label,
    analyze_emotions,
    validate_input
)

print("=" * 80)
print("CampusSafe - Enhanced NLP Model Test")
print("=" * 80)

# Test cases
test_cases = [
    {
        "description": "I was forced by seniors to sing and dance in the hostel mess. They were laughing at me and made me feel very uncomfortable and scared.",
        "expected_category": "Ragging"
    },
    {
        "description": "Someone stole my laptop from the library while I was in the restroom. It was there just 5 minutes ago.",
        "expected_category": "Theft"
    },
    {
        "description": "A classmate keeps making inappropriate comments about my appearance. This has been happening for weeks and I feel very uncomfortable.",
        "expected_category": "Harassment"
    },
    {
        "description": "There was a physical fight in the cafeteria. Two students were punching each other and one got injured.",
        "expected_category": "Violence"
    },
    {
        "description": "The professor constantly uses abusive language and shouts at students in class. It's very humiliating.",
        "expected_category": "Verbal Abuse"
    },
    {
        "description": "The stairs in Block C are broken and there's no warning sign. Someone could get seriously injured.",
        "expected_category": "Safety Concern"
    },
    {
        "description": "I'm being excluded from group activities because of my background. It feels like discrimination.",
        "expected_category": "Discrimination"
    }
]

print("\n📊 Running Classification Tests...\n")

for i, test in enumerate(test_cases, 1):
    print(f"\n{'─' * 80}")
    print(f"Test Case {i}:")
    print(f"Description: {test['description'][:70]}...")
    print(f"Expected Category: {test['expected_category']}")
    
    # Perform comprehensive analysis
    result = analyze_incident(test['description'])
    
    if result['valid']:
        print(f"\n✅ Analysis Results:")
        print(f"   • Category: {result['category']} (Confidence: {result['confidence']:.1%})")
        print(f"   • Sentiment: {result['sentiment_label']} (Score: {result['sentiment_score']:.2f})")
        print(f"   • Emotion: {result['emotion']} (Intensity: {result['emotion_intensity']:.0%})")
        print(f"   • Suggested Urgency: {result['suggested_urgency']}")
        
        # Check if classification matches expected
        if result['category'] == test['expected_category']:
            print(f"   ✓ Classification CORRECT")
        else:
            print(f"   ✗ Classification mismatch (got {result['category']}, expected {test['expected_category']})")
    else:
        print(f"❌ Validation Error: {result['error']}")

print("\n" + "=" * 80)
print("\n🧪 Testing Input Validation...\n")

# Test validation
validation_tests = [
    ("Short", False),  # Too short
    ("a" * 2500, False),  # Too long
    ("aaaaaaaaaa", False),  # Not meaningful
    ("This is a proper incident description with enough detail.", True)  # Valid
]

for text, should_pass in validation_tests:
    is_valid, error = validate_input(text)
    status = "✓" if is_valid == should_pass else "✗"
    display_text = text[:50] + "..." if len(text) > 50 else text
    print(f"{status} '{display_text}' - Valid: {is_valid}")
    if not is_valid:
        print(f"   Error: {error}")

print("\n" + "=" * 80)
print("\n🎭 Testing Emotion Detection...\n")

emotion_tests = [
    "I'm so scared and terrified of what might happen next",
    "This makes me extremely angry and frustrated",
    "I feel so sad and disappointed about this situation",
    "I'm disgusted by this behavior",
    "I feel very uncomfortable and uneasy about this"
]

for text in emotion_tests:
    emotion, intensity = analyze_emotions(text)
    print(f"Text: '{text[:60]}...'")
    print(f"   → Emotion: {emotion} (Intensity: {intensity:.0%})\n")

print("=" * 80)
print("\n✅ All tests completed!\n")
print("The enhanced NLP model includes:")
print("  • 8 category classification (Ragging, Harassment, Violence, etc.)")
print("  • Sentiment analysis with polarity scoring")
print("  • Emotion detection (Fear, Anger, Sadness, Disgust, Distress)")
print("  • Confidence scoring for classifications")
print("  • Input validation and preprocessing")
print("  • Automatic urgency suggestion")
print("\n" + "=" * 80)
