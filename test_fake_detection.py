# -*- coding: utf-8 -*-
"""
Fake Report Detection Test
Demonstrates how the system detects and rejects fake/test reports
"""

from nlp_model import analyze_incident, detect_fake_report

print("=" * 80)
print("Fake Report Detection Test")
print("=" * 80)

# Test cases for fake reports
fake_reports = [
    {
        "category": "Test Patterns",
        "reports": [
            "test1 test2",
            "testing this system",
            "this is a test report",
            "sample1 sample2",
            "demo report here",
            "just testing the app",
        ]
    },
    {
        "category": "Gibberish/Keyboard Mashing",
        "reports": [
            "asdfghjkl qwerty",
            "xxxxxxxxx yyyyyy",
            "aaaaaa bbbbb ccccc",
            "qwerty asdf zxcv",
            "123456 111111 000000",
        ]
    },
    {
        "category": "Repeated Words",
        "reports": [
            "help help help help help",
            "test test test test",
            "incident incident incident",
            "report report report report",
        ]
    },
    {
        "category": "Placeholder Text",
        "reports": [
            "lorem ipsum dolor sit amet",
            "the quick brown fox jumps over the lazy dog",
            "hello world foo bar",
            "blah blah blah something",
        ]
    },
    {
        "category": "Low Quality Content",
        "reports": [
            "a b c d e f g",
            "this is a very very very very short",
            "12345 67890 numbers only here 999",
        ]
    }
]

# Test cases for legitimate reports
legitimate_reports = [
    "A senior student forced me to clean his room and threatened me when I refused",
    "My laptop was stolen from the library while I went to the restroom",
    "The electrical wiring in the lab is exposed and sparking, very dangerous",
    "Someone keeps following me around campus and making me uncomfortable",
]

print("\n🚫 Testing FAKE Reports (Should be REJECTED):")
print("=" * 80)

total_fake = 0
detected_fake = 0

for category_info in fake_reports:
    print(f"\n📋 {category_info['category']}")
    print("─" * 80)
    
    for i, text in enumerate(category_info['reports'], 1):
        total_fake += 1
        is_fake, reason = detect_fake_report(text)
        
        if is_fake:
            detected_fake += 1
            status = "✅ REJECTED"
            color = "🔴"
        else:
            status = "❌ ACCEPTED (ERROR!)"
            color = "🟢"
        
        print(f"\n{i}. \"{text}\"")
        print(f"   {color} {status}")
        if is_fake:
            print(f"   Reason: {reason}")

print("\n" + "=" * 80)
print(f"Fake Detection Rate: {detected_fake}/{total_fake} ({detected_fake/total_fake*100:.1f}%)")
print("=" * 80)

print("\n\n✅ Testing LEGITIMATE Reports (Should be ACCEPTED):")
print("=" * 80)

total_legit = 0
accepted_legit = 0

for i, text in enumerate(legitimate_reports, 1):
    total_legit += 1
    result = analyze_incident(text)
    
    if result['valid']:
        accepted_legit += 1
        status = "✅ ACCEPTED"
        color = "🟢"
        print(f"\n{i}. \"{text[:60]}...\"")
        print(f"   {color} {status}")
        print(f"   Category: {result['category']} ({result['confidence']:.1%} confidence)")
    else:
        status = "❌ REJECTED (ERROR!)"
        color = "🔴"
        print(f"\n{i}. \"{text[:60]}...\"")
        print(f"   {color} {status}")
        print(f"   Error: {result['error']}")

print("\n" + "=" * 80)
print(f"Legitimate Acceptance Rate: {accepted_legit}/{total_legit} ({accepted_legit/total_legit*100:.1f}%)")
print("=" * 80)

print("\n\n📊 COMPREHENSIVE TEST:")
print("=" * 80)
print(f"Fake Reports Detected: {detected_fake}/{total_fake} ({detected_fake/total_fake*100:.1f}%)")
print(f"Legitimate Reports Accepted: {accepted_legit}/{total_legit} ({accepted_legit/total_legit*100:.1f}%)")
print(f"Overall Accuracy: {(detected_fake + accepted_legit)/(total_fake + total_legit)*100:.1f}%")
print("=" * 80)

print("\n\n🛡️ Fake Detection Features:")
print("─" * 80)
print("✅ Test patterns (test1, test2, testing, demo, sample)")
print("✅ Keyboard mashing (asdf, qwerty, 123456)")
print("✅ Gibberish detection (random consonants)")
print("✅ Repeated words (same word 3+ times)")
print("✅ Placeholder text (lorem ipsum, hello world)")
print("✅ Low information content (too generic)")
print("✅ Number-heavy text (>50% numbers)")
print("✅ Character repetition (aaaa, xxxx)")
print("✅ Short meaningless words only")
print("✅ Common spam patterns")
print("=" * 80)
