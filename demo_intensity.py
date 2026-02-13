# -*- coding: utf-8 -*-
"""
Emotion Intensity Demonstration
Shows how different texts produce different intensity scores
"""

from nlp_model import analyze_emotions

print("=" * 80)
print("Emotion Intensity Demonstration")
print("=" * 80)

# Test cases showing different intensity levels
test_cases = [
    {
        "category": "Fear - Low Intensity (33%)",
        "texts": [
            "I'm worried about this situation",
            "This makes me a bit anxious",
            "I feel scared about what happened"
        ]
    },
    {
        "category": "Fear - Medium Intensity (67%)",
        "texts": [
            "I'm scared and worried about my safety",
            "I feel terrified and anxious all the time",
            "This is frightening and makes me panic"
        ]
    },
    {
        "category": "Fear - High Intensity (100%)",
        "texts": [
            "I'm terrified, scared, and extremely worried about what will happen",
            "I feel afraid, anxious, and panicking about this situation",
            "I'm frightened, worried, and scared for my life"
        ]
    },
    {
        "category": "Anger - Different Intensities",
        "texts": [
            "I'm annoyed by this behavior",  # 33%
            "I'm angry and frustrated with this situation",  # 67%
            "I'm furious, outraged, and extremely mad about this"  # 100%
        ]
    },
    {
        "category": "Distress - Different Intensities",
        "texts": [
            "I feel uncomfortable about this",  # 33%
            "I'm troubled and uneasy about what's happening",  # 67%
            "I feel distressed, uncomfortable, and extremely uneasy"  # 100%
        ]
    },
    {
        "category": "Neutral - No Emotion",
        "texts": [
            "The laptop was stolen from the library",
            "There was an incident in the cafeteria",
            "Someone reported a problem with the stairs"
        ]
    }
]

for category_info in test_cases:
    print(f"\n{'─' * 80}")
    print(f"📊 {category_info['category']}")
    print('─' * 80)
    
    for i, text in enumerate(category_info['texts'], 1):
        emotion, intensity = analyze_emotions(text)
        
        # Create visual intensity bar
        bar_length = 20
        filled = int(intensity * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        # Determine intensity level
        if intensity == 0:
            level = "None"
            color = "⚪"
        elif intensity <= 0.33:
            level = "Low"
            color = "🟢"
        elif intensity <= 0.67:
            level = "Medium"
            color = "🟡"
        else:
            level = "High"
            color = "🔴"
        
        print(f"\n{i}. Text: \"{text}\"")
        print(f"   Emotion: {emotion}")
        print(f"   Intensity: {intensity:.0%} {color} [{bar}] {level}")

print("\n" + "=" * 80)
print("\n📈 Intensity Scale:")
print("   🟢 0-33%   = Low Intensity    (1 emotion keyword)")
print("   🟡 34-67%  = Medium Intensity (2 emotion keywords)")
print("   🔴 68-100% = High Intensity   (3+ emotion keywords)")
print("   ⚪ 0%      = Neutral          (No emotion keywords)")
print("\n" + "=" * 80)

# Show keyword breakdown
print("\n🔍 Emotion Keywords Reference:")
print("─" * 80)

emotions_keywords = {
    'Fear': ['scared', 'afraid', 'terrified', 'frightened', 'worried', 'anxious', 'panic'],
    'Anger': ['angry', 'furious', 'mad', 'outraged', 'irritated', 'annoyed', 'frustrated'],
    'Sadness': ['sad', 'depressed', 'upset', 'hurt', 'disappointed', 'miserable', 'unhappy'],
    'Disgust': ['disgusted', 'revolted', 'sick', 'repulsed', 'appalled'],
    'Distress': ['distressed', 'troubled', 'disturbed', 'uncomfortable', 'uneasy', 'helpless']
}

for emotion, keywords in emotions_keywords.items():
    print(f"\n{emotion}:")
    print(f"  Keywords: {', '.join(keywords)}")
    print(f"  Total: {len(keywords)} keywords")

print("\n" + "=" * 80)
print("\n💡 How It Works:")
print("   1. System scans text for emotion keywords")
print("   2. Counts how many keywords are found")
print("   3. Calculates intensity: min(count / 3, 1.0)")
print("   4. Returns primary emotion and intensity percentage")
print("\n" + "=" * 80)
