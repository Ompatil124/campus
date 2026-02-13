# Emotion Intensity - Detailed Guide

## 📊 What is Emotion Intensity?

**Emotion Intensity** is a numerical score (0-100%) that measures **how strongly** an emotion is expressed in the text. It helps distinguish between mild discomfort and severe distress.

---

## 🎯 How It Works

### 1. **Keyword Detection**
The system scans the text for emotion-specific keywords:

```python
emotions = {
    'fear': ['scared', 'afraid', 'terrified', 'frightened', 'worried', 'anxious', 'panic'],
    'anger': ['angry', 'furious', 'mad', 'outraged', 'irritated', 'annoyed', 'frustrated'],
    'sadness': ['sad', 'depressed', 'upset', 'hurt', 'disappointed', 'miserable', 'unhappy'],
    'disgust': ['disgusted', 'revolted', 'sick', 'repulsed', 'appalled'],
    'distress': ['distressed', 'troubled', 'disturbed', 'uncomfortable', 'uneasy', 'helpless']
}
```

### 2. **Counting Matches**
The system counts how many emotion keywords appear in the text:
- **1 keyword** = Low intensity
- **2 keywords** = Medium intensity  
- **3+ keywords** = High intensity

### 3. **Normalization Formula**
```python
intensity = min(keyword_count / 3.0, 1.0)
```

This means:
- 1 keyword → 33% intensity
- 2 keywords → 67% intensity
- 3+ keywords → 100% intensity (capped)

---

## 📈 Intensity Levels Explained

### **0% - No Emotion Detected**
```
Text: "The library is closed today."
Emotion: Neutral
Intensity: 0%
```
**Meaning**: No emotional keywords found, text is factual/neutral.

---

### **33% - Low Intensity (1 keyword)**
```
Text: "I'm worried about the exam tomorrow."
Emotion: Fear
Intensity: 33%
Keywords Found: ['worried']
```
**Meaning**: Mild emotional expression, single emotion word detected.

**Examples:**
- "I feel uncomfortable in this situation" → Distress (33%)
- "This is annoying" → Anger (33%)
- "I'm a bit sad about this" → Sadness (33%)

---

### **67% - Medium Intensity (2 keywords)**
```
Text: "I'm scared and anxious about what might happen."
Emotion: Fear
Intensity: 67%
Keywords Found: ['scared', 'anxious']
```
**Meaning**: Moderate emotional expression, multiple emotion words detected.

**Examples:**
- "I feel uncomfortable and uneasy" → Distress (67%)
- "I'm angry and frustrated" → Anger (67%)
- "I'm sad and disappointed" → Sadness (67%)

---

### **100% - High Intensity (3+ keywords)**
```
Text: "I'm terrified, scared, and extremely worried about my safety."
Emotion: Fear
Intensity: 100%
Keywords Found: ['terrified', 'scared', 'worried']
```
**Meaning**: Strong emotional expression, multiple intense emotion words detected.

**Examples:**
- "I'm afraid, terrified, and panicking" → Fear (100%)
- "I'm furious, angry, and outraged" → Anger (100%)
- "I feel sad, depressed, and miserable" → Sadness (100%)

---

## 🔍 Real-World Examples from Tests

### Example 1: Fear Detection
```python
Text: "I'm so scared and terrified of what might happen next"
Result:
  Emotion: Fear
  Intensity: 67%
  Keywords: ['scared', 'terrified']
  
Interpretation: Strong fear response with 2 fear-related words
```

### Example 2: Anger Detection
```python
Text: "This makes me extremely angry and frustrated"
Result:
  Emotion: Anger
  Intensity: 67%
  Keywords: ['angry', 'frustrated']
  
Interpretation: Moderate to high anger with 2 anger-related words
```

### Example 3: Distress Detection
```python
Text: "I feel very uncomfortable and uneasy about this"
Result:
  Emotion: Distress
  Intensity: 67%
  Keywords: ['uncomfortable', 'uneasy']
  
Interpretation: Significant distress with 2 distress-related words
```

### Example 4: Neutral Case
```python
Text: "Someone stole my laptop from the library"
Result:
  Emotion: Neutral
  Intensity: 0%
  Keywords: []
  
Interpretation: Factual statement with no emotional keywords
```

---

## 🎨 Visual Representation in UI

The intensity is displayed in the CampusSafe interface:

```
┌─────────────────────────┐
│   😊 Emotion            │
│   😨 Fear               │
│   Intensity: 67%        │
└─────────────────────────┘
```

**Color Coding (Potential Enhancement):**
- 0-33%: 🟢 Green (Low)
- 34-66%: 🟡 Yellow (Medium)
- 67-100%: 🔴 Red (High)

---

## 💡 Why Intensity Matters

### 1. **Prioritization**
Higher intensity = More urgent attention needed
```
"I'm worried" (33%) vs "I'm terrified and panicking" (100%)
```

### 2. **Context Understanding**
Helps admins gauge the emotional state of the reporter:
- Low intensity: Mild concern, routine follow-up
- High intensity: Severe distress, immediate support needed

### 3. **Pattern Recognition**
Track emotional trends over time:
- Are reports becoming more intense?
- Which categories trigger highest emotional responses?

### 4. **Support Services**
Route high-intensity cases to counseling services:
```
if emotion_intensity >= 0.67 and emotion in ['Fear', 'Distress', 'Sadness']:
    suggest_counseling_support()
```

---

## 🔧 Technical Implementation

### Code Walkthrough

```python
def analyze_emotions(text):
    """
    Detects emotional tone in text.
    Returns primary emotion and intensity.
    """
    cleaned_text = preprocess_text(text)
    
    if not cleaned_text:
        return "Neutral", 0.0
    
    # Emotion keywords dictionary
    emotions = {
        'fear': ['scared', 'afraid', 'terrified', 'frightened', 'worried', 'anxious', 'panic'],
        'anger': ['angry', 'furious', 'mad', 'outraged', 'irritated', 'annoyed', 'frustrated'],
        'sadness': ['sad', 'depressed', 'upset', 'hurt', 'disappointed', 'miserable', 'unhappy'],
        'disgust': ['disgusted', 'revolted', 'sick', 'repulsed', 'appalled'],
        'distress': ['distressed', 'troubled', 'disturbed', 'uncomfortable', 'uneasy', 'helpless']
    }
    
    text_lower = cleaned_text.lower()
    emotion_scores = {}
    
    # Count keyword matches for each emotion
    for emotion, keywords in emotions.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            emotion_scores[emotion] = score
    
    # No emotions detected
    if not emotion_scores:
        return "Neutral", 0.0
    
    # Get primary emotion (highest score)
    primary_emotion = max(emotion_scores, key=emotion_scores.get)
    
    # Calculate intensity (normalize to 0-1, cap at 1.0)
    # Formula: min(count / 3, 1.0)
    intensity = min(emotion_scores[primary_emotion] / 3.0, 1.0)
    
    return primary_emotion.capitalize(), round(intensity, 2)
```

---

## 📊 Intensity Distribution in Test Data

From our test results:

| Emotion | Intensity | Frequency |
|---------|-----------|-----------|
| Fear | 67% | Common |
| Fear | 33% | Common |
| Anger | 67% | Common |
| Sadness | 67% | Common |
| Disgust | 33% | Common |
| Distress | 67% | Common |
| Distress | 33% | Common |
| Neutral | 0% | Very Common |

**Observation**: Most emotional texts fall in the 33-67% range, which is realistic for incident reports.

---

## 🚀 Advanced Use Cases

### 1. **Automatic Escalation**
```python
if emotion_intensity >= 0.67 and emotion in ['Fear', 'Distress']:
    urgency = 'High'
    notify_counselor = True
```

### 2. **Trend Analysis**
```python
# Track average intensity over time
monthly_avg_intensity = calculate_avg_intensity(reports_this_month)

if monthly_avg_intensity > 0.5:
    alert_admin("Emotional distress levels rising on campus")
```

### 3. **Support Recommendations**
```python
if emotion == 'Fear' and intensity >= 0.67:
    suggest_resources = [
        "Campus Security: ext. 1234",
        "Counseling Services: ext. 5678",
        "Anonymous Helpline: 1800-XXX-XXXX"
    ]
```

---

## 🎯 Improving Intensity Detection

### Current Limitations:
1. **Simple counting**: Doesn't consider word strength
   - "worried" vs "terrified" both count as 1
   
2. **No context**: Doesn't understand negation
   - "I'm not scared" still detects "scared"

### Potential Enhancements:

#### 1. **Weighted Keywords**
```python
fear_weights = {
    'worried': 0.3,      # Mild
    'scared': 0.6,       # Moderate
    'terrified': 1.0,    # Severe
    'panicking': 1.0     # Severe
}
```

#### 2. **Intensity Modifiers**
```python
modifiers = {
    'very': 1.5,
    'extremely': 2.0,
    'slightly': 0.5,
    'a bit': 0.5
}
```

#### 3. **Negation Handling**
```python
if 'not' in text before emotion_word:
    skip_this_keyword()
```

---

## 📚 Summary

### Key Points:
- ✅ Intensity ranges from **0% to 100%**
- ✅ Based on **keyword counting** (1 word = 33%, 2 = 67%, 3+ = 100%)
- ✅ Helps **prioritize** urgent cases
- ✅ Provides **context** for admin review
- ✅ Can trigger **automatic support** recommendations

### Formula:
```
Intensity = min(keyword_count / 3.0, 1.0) × 100%
```

### Interpretation:
- **0%**: No emotion detected (neutral/factual)
- **33%**: Low intensity (1 keyword, mild emotion)
- **67%**: Medium intensity (2 keywords, moderate emotion)
- **100%**: High intensity (3+ keywords, strong emotion)

---

**Last Updated**: February 13, 2026  
**Version**: 2.0  
**Status**: Production Ready ✅
