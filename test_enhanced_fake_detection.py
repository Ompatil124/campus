# -*- coding: utf-8 -*-
"""
Enhanced Fake Detection Test
Tests both primary detection and secondary classification-based detection
"""

from nlp_model import analyze_incident

print("=" * 80)
print("Enhanced Fake Detection Test - Two-Layer Protection")
print("=" * 80)

# Test cases that should be caught by PRIMARY detection (before classification)
print("\n🛡️ LAYER 1: Primary Detection (Pattern Matching)")
print("=" * 80)

primary_catches = [
    "test1 test2",
    "testing this system",
    "sample report here",
    "demo submission",
    "just checking the app",
    "trying to test",
    "spam junk garbage",
    "placeholder text here",
    "debugging the system",
    "temporary report temp1",
]

caught_primary = 0
for i, text in enumerate(primary_catches, 1):
    result = analyze_incident(text)
    
    if not result['valid'] and result.get('is_fake'):
        caught_primary += 1
        print(f"\n{i}. ✅ CAUGHT: \"{text}\"")
        print(f"   Reason: {result['error']}")
    else:
        print(f"\n{i}. ❌ MISSED: \"{text}\"")
        if result['valid']:
            print(f"   Classified as: {result['category']}")

print(f"\n{'─' * 80}")
print(f"Primary Detection Rate: {caught_primary}/{len(primary_catches)} ({caught_primary/len(primary_catches)*100:.1f}%)")
print("=" * 80)

# Test cases that might slip through primary but caught by SECONDARY (ML classification)
print("\n\n🧠 LAYER 2: Secondary Detection (ML Classification)")
print("=" * 80)

secondary_test = [
    "qwerty asdf keyboard mashing here",
    "random nonsense gibberish text",
    "blah blah blah nothing real",
    "xxxxxx yyyyyy zzzzz random",
    "123 abc xyz pattern test",
]

caught_secondary = 0
for i, text in enumerate(secondary_test, 1):
    result = analyze_incident(text)
    
    if not result['valid']:
        caught_secondary += 1
        print(f"\n{i}. ✅ CAUGHT: \"{text}\"")
        print(f"   Reason: {result['error']}")
        if 'category' in result:
            print(f"   Classified as: {result['category']} ({result.get('confidence', 0):.1%})")
    elif result.get('is_suspicious'):
        print(f"\n{i}. ⚠️  FLAGGED: \"{text}\"")
        print(f"   Category: {result['category']} ({result['confidence']:.1%})")
        print(f"   Warning: {result.get('warning', 'Suspicious content')}")
    else:
        print(f"\n{i}. ❌ MISSED: \"{text}\"")
        print(f"   Classified as: {result['category']} ({result['confidence']:.1%})")

print(f"\n{'─' * 80}")
print(f"Secondary Detection Rate: {caught_secondary}/{len(secondary_test)} ({caught_secondary/len(secondary_test)*100:.1f}%)")
print("=" * 80)

# Test legitimate reports (should NOT be caught)
print("\n\n✅ LEGITIMATE Reports (Should Pass Both Layers)")
print("=" * 80)

legitimate = [
    "A senior student forced me to clean his room and threatened me when I refused",
    "My laptop was stolen from the library while I went to the restroom",
    "The electrical wiring in the lab is exposed and sparking, very dangerous",
    "Someone keeps following me around campus making me uncomfortable",
]

passed_legit = 0
for i, text in enumerate(legitimate, 1):
    result = analyze_incident(text)
    
    if result['valid'] and result['category'] != 'Fake/Spam':
        passed_legit += 1
        print(f"\n{i}. ✅ ACCEPTED: \"{text[:60]}...\"")
        print(f"   Category: {result['category']} ({result['confidence']:.1%})")
    else:
        print(f"\n{i}. ❌ REJECTED (ERROR!): \"{text[:60]}...\"")
        if not result['valid']:
            print(f"   Error: {result['error']}")
        else:
            print(f"   Wrongly classified as: {result['category']}")

print(f"\n{'─' * 80}")
print(f"Legitimate Acceptance Rate: {passed_legit}/{len(legitimate)} ({passed_legit/len(legitimate)*100:.1f}%)")
print("=" * 80)

# Overall summary
print("\n\n📊 OVERALL SUMMARY")
print("=" * 80)

total_fake = len(primary_catches) + len(secondary_test)
total_caught = caught_primary + caught_secondary
total_legit = len(legitimate)

print(f"Layer 1 (Primary Detection):   {caught_primary}/{len(primary_catches)} caught ({caught_primary/len(primary_catches)*100:.1f}%)")
print(f"Layer 2 (ML Classification):   {caught_secondary}/{len(secondary_test)} caught ({caught_secondary/len(secondary_test)*100:.1f}%)")
print(f"Legitimate Reports Accepted:   {passed_legit}/{total_legit} passed ({passed_legit/total_legit*100:.1f}%)")
print(f"\nTotal Fake Detection:          {total_caught}/{total_fake} ({total_caught/total_fake*100:.1f}%)")
print(f"Overall System Accuracy:       {(total_caught + passed_legit)}/{(total_fake + total_legit)} ({(total_caught + passed_legit)/(total_fake + total_legit)*100:.1f}%)")

print("\n" + "=" * 80)
print("\n🎯 Detection Strategy:")
print("─" * 80)
print("1️⃣  Primary Layer: Pattern matching (fast, catches obvious fakes)")
print("2️⃣  Secondary Layer: ML classification (catches subtle fakes)")
print("3️⃣  Fallback: If classified as 'Fake/Spam', reject or warn")
print("\n✅ Result: Multi-layered protection against spam and test submissions!")
print("=" * 80)
