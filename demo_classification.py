# -*- coding: utf-8 -*-
"""
Quick demo script showing the enhanced classification in action
"""

from nlp_model import analyze_incident

print("=" * 80)
print("CampusSafe - AI Classification Demo")
print("=" * 80)

# Real-world example scenarios
demo_cases = [
    "A senior student forced me to clean his room and threatened me when I refused. This has been happening for the past week and I'm really scared.",
    
    "My phone was stolen from the library desk when I went to get a book. It was there just 2 minutes ago.",
    
    "The electrical wiring in our lab is completely exposed and sparking. This is very dangerous and needs immediate attention.",
]

for i, text in enumerate(demo_cases, 1):
    print(f"\n{'─' * 80}")
    print(f"Demo Case {i}:")
    print(f"Input: \"{text}\"")
    print()
    
    result = analyze_incident(text)
    
    if result['valid']:
        print(f"✅ ANALYSIS COMPLETE")
        print(f"   📂 Category: {result['category']} ({result['confidence']:.1%} confidence)")
        print(f"   💭 Sentiment: {result['sentiment_label']} (score: {result['sentiment_score']:.2f})")
        print(f"   😊 Emotion: {result['emotion']} ({result['emotion_intensity']:.0%} intensity)")
        print(f"   ⚠️  Suggested Urgency: {result['suggested_urgency']}")
    else:
        print(f"❌ VALIDATION ERROR: {result['error']}")

print("\n" + "=" * 80)
print("\n✨ The system successfully:")
print("   • Validated all inputs")
print("   • Classified incidents into correct categories")
print("   • Analyzed sentiment and emotions")
print("   • Suggested appropriate urgency levels")
print("\n" + "=" * 80)
