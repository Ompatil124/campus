# -*- coding: utf-8 -*-
"""
Quick test for the specific case: "test1 test2"
"""

from nlp_model import analyze_incident

print("=" * 80)
print("Testing Your Specific Case: 'test1 test2'")
print("=" * 80)

test_input = "test1 test2"

print(f"\nInput: \"{test_input}\"")
print("\nAnalyzing...")

result = analyze_incident(test_input)

print("\n" + "─" * 80)
if result['valid']:
    print("❌ ERROR: Report was ACCEPTED (should be rejected!)")
    print(f"Category: {result['category']}")
    print(f"Confidence: {result['confidence']:.1%}")
else:
    print("✅ SUCCESS: Report was REJECTED")
    print(f"Error Message: {result['error']}")
    if result.get('is_fake'):
        print("Flagged as: FAKE REPORT")

print("─" * 80)

# Test a few more variations
print("\n\nTesting Similar Variations:")
print("=" * 80)

variations = [
    "test1 test2 test3",
    "testing testing",
    "this is test1",
    "sample report test2",
]

for text in variations:
    result = analyze_incident(text)
    status = "✅ REJECTED" if not result['valid'] else "❌ ACCEPTED"
    print(f"\n'{text}' → {status}")
    if not result['valid']:
        print(f"  Reason: {result['error']}")

print("\n" + "=" * 80)
