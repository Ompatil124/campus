import re
import numpy as np
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

# ==================== TEXT PREPROCESSING ====================

def preprocess_text(text):
    """
    Cleans and preprocesses input text.
    - Removes extra whitespace
    - Converts to lowercase
    - Removes special characters (keeps basic punctuation)
    - Returns cleaned text
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove excessive punctuation but keep basic ones
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text.strip()


def validate_input(text, min_length=10, max_length=2000):
    """
    Validates user input text.
    Returns (is_valid, error_message)
    """
    if not text or not isinstance(text, str):
        return False, "Please provide a description of the incident."
    
    text = text.strip()
    
    if len(text) < min_length:
        return False, f"Description too short. Please provide at least {min_length} characters."
    
    if len(text) > max_length:
        return False, f"Description too long. Please limit to {max_length} characters."
    
    # Check if text is meaningful (not just repeated characters)
    unique_chars = len(set(text.replace(' ', '')))
    if unique_chars < 5:
        return False, "Please provide a meaningful description."
    
    return True, ""


def detect_fake_report(text):
    """
    Detects fake, test, or spam reports.
    Returns (is_fake, reason) tuple.
    
    
    Checks for:
    - Test patterns (test1, test2, testing, etc.)
    - Gibberish/random text
    - Repeated words/characters
    - Common spam patterns
    - Low information content
    """
    if not text or not isinstance(text, str):
        return True, "Empty or invalid text"
    
    text_lower = text.lower().strip()
    words = text_lower.split()
    
    # 1. Check for test patterns (expanded)
    test_patterns = [
        # Test variations
        r'\btest\s*\d+\b',           # test1, test2, test 1
        r'\btesting\b',              # testing
        r'\btest\s+test\b',          # test test
        r'\btest\s*report\b',        # test report
        r'\btest\s*incident\b',      # test incident
        r'\btest\s*case\b',          # test case
        r'\btester\b',               # tester
        r'\btests\b',                # tests
        
        # Sample/Demo variations
        r'\bsample\s*\d*\b',         # sample, sample1
        r'\bdemo\s*\d*\b',           # demo, demo1
        r'\bexample\s*\d*\b',        # example, example1
        r'\bdummy\s*\d*\b',          # dummy, dummy1
        r'\bmock\s*\d*\b',           # mock, mock1
        
        # Fake indicators
        r'\bfake\s+report\b',        # fake report
        r'\bfake\s+incident\b',      # fake incident
        r'\bfake\s+submission\b',    # fake submission
        r'\bnot\s+real\b',           # not real
        r'\bjust\s+kidding\b',       # just kidding
        
        # Testing phrases
        r'\bthis\s+is\s+a\s+test\b', # this is a test
        r'\bjust\s+testing\b',       # just testing
        r'\btrying\s+to\s+test\b',   # trying to test
        r'\btest\s+run\b',           # test run
        r'\btest\s+submission\b',    # test submission
        
        # Check/Try variations
        r'\bcheck\s*\d*\b',          # check, check1
        r'\bchecking\b',             # checking
        r'\btry\s*\d*\b',            # try, try1
        r'\btrying\b',               # trying
        r'\btrial\b',                # trial
        
        # Keyboard patterns
        r'\bqwerty\b',               # keyboard pattern
        r'\basdf\b',                 # keyboard pattern
        r'\bzxcv\b',                 # keyboard pattern
        r'\bhjkl\b',                 # keyboard pattern
        r'\byuiop\b',                # keyboard pattern
        
        # ABC/XYZ patterns
        r'\b(abc|xyz)\s*\d*\b',      # abc, xyz patterns
        r'\babcd\b',                 # abcd
        r'\b123\s*abc\b',            # 123 abc
        
        # Spam indicators
        r'\bspam\b',                 # spam
        r'\bjunk\b',                 # junk
        r'\bgarbage\b',              # garbage
        r'\btrash\b',                # trash
        r'\bnonsense\b',             # nonsense
        r'\brandom\b',               # random
        
        # Placeholder indicators
        r'\bplaceholder\b',          # placeholder
        r'\btemp\s*\d*\b',           # temp, temp1
        r'\btemporary\b',            # temporary
        r'\btbd\b',                  # to be determined
        r'\btba\b',                  # to be announced
        
        # Debug/Dev patterns
        r'\bdebug\b',                # debug
        r'\bdebugging\b',            # debugging
        r'\bdev\s*\d*\b',            # dev, dev1
        r'\bprod\b',                 # prod
        r'\bstaging\b',              # staging
    ]
    
    for pattern in test_patterns:
        if re.search(pattern, text_lower):
            return True, "Test/demo report detected. Please submit a real incident."
    
    # 2. Check for gibberish (too many consonants or vowels in a row)
    if re.search(r'[bcdfghjklmnpqrstvwxyz]{6,}', text_lower):
        return True, "Gibberish detected. Please provide a meaningful description."
    
    # 3. Check for repeated words
    if len(words) >= 3:
        # Check if more than 50% of words are duplicates
        unique_words = set(words)
        if len(unique_words) / len(words) < 0.5:
            return True, "Too many repeated words. Please provide a detailed description."
    
    # 4. Check for single word repeated multiple times
    word_counts = {}
    for word in words:
        if len(word) > 2:  # Ignore short words like "a", "is"
            word_counts[word] = word_counts.get(word, 0) + 1
    
    for word, count in word_counts.items():
        if count >= 3 and len(words) <= 10:  # Same word 3+ times in short text
            return True, f"Repeated word '{word}' detected. Please provide a genuine description."
    
    # 5. Check for very short words only (no substance)
    long_words = [w for w in words if len(w) > 3]
    if len(words) >= 3 and len(long_words) == 0:
        return True, "No substantial words found. Please provide details."
    
    # 6. Check for common spam/placeholder patterns
    spam_phrases = [
        'lorem ipsum',
        'dolor sit amet',
        'quick brown fox',
        'the lazy dog',
        'hello world',
        'foo bar',
        'blah blah',
        'yada yada',
        'etc etc',
        'something something',
    ]
    
    for phrase in spam_phrases:
        if phrase in text_lower:
            return True, "Placeholder text detected. Please describe a real incident."
    
    # 7. Check for number-only or mostly numbers
    numbers_count = sum(1 for char in text if char.isdigit())
    if numbers_count / len(text) > 0.5:
        return True, "Too many numbers. Please provide a descriptive text."
    
    # 8. Check for very low information content (too generic)
    # Count meaningful words (not common stop words)
    stop_words = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 
                  'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                  'would', 'should', 'could', 'may', 'might', 'must', 'can',
                  'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
                  'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
                  'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
                  'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
                  'own', 'same', 'so', 'than', 'too', 'very', 'just', 'but',
                  'and', 'or', 'if', 'because', 'as', 'until', 'while', 'of',
                  'at', 'by', 'for', 'with', 'about', 'against', 'between',
                  'into', 'through', 'during', 'before', 'after', 'above',
                  'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off'}
    
    meaningful_words = [w for w in words if w not in stop_words and len(w) > 2]
    
    if len(words) >= 5 and len(meaningful_words) < 2:
        return True, "Not enough meaningful content. Please describe the incident in detail."
    
    # 9. Check for single character repeated
    for char in set(text_lower):
        if char.isalpha() and text_lower.count(char) / len(text_lower) > 0.4:
            return True, "Excessive character repetition detected. Please provide a real description."
    
    # 10. Check for keyboard mashing patterns
    keyboard_patterns = [
        'asdfgh', 'qwerty', 'zxcvbn', 'hjkl', 'yuiop',
        '123456', '111111', '000000', 'aaaaaa', 'xxxxxx'
    ]
    
    for pattern in keyboard_patterns:
        if pattern in text_lower.replace(' ', ''):
            return True, "Keyboard pattern detected. Please submit a genuine report."
    
    # All checks passed - appears to be legitimate
    return False, ""


# ==================== CATEGORY CLASSIFICATION ====================

# Training data for incident classification
TRAINING_DATA = {
    'Ragging': [
        'seniors forcing juniors to do embarrassing tasks in front of everyone',
        'being forced to sing and dance by seniors in the hostel common room',
        'verbal abuse and name calling by senior students',
        'physical harassment by seniors in hostel late at night',
        'ragging incident in mess area where seniors made me stand on table',
        'seniors asking inappropriate personal questions about my family',
        'forced to do push ups and run errands by seniors',
        'public humiliation by senior batch during fresher party',
        'bullying by older students who took my belongings',
        'intimidation by seniors during orientation week',
        'seniors made me clean their room and do their laundry',
        'forced to address seniors with special titles and bow down',
        'senior students slapped me for not following their orders',
        'ragging in college corridor where seniors blocked my way',
        'made to stand outside in the rain by senior students',
        'seniors forcing me to drink alcohol against my will',
        'harassment by final year students in the library',
        'seniors making fun of my accent and hometown',
        'forced participation in degrading activities by seniors',
        'threatened by seniors not to report ragging incidents'
    ],
    'Harassment': [
        'inappropriate comments about my body and appearance',
        'unwanted touching and physical contact in crowded areas',
        'sexual harassment by classmate who sends explicit messages',
        'stalking behavior on campus, someone follows me everywhere',
        'receiving inappropriate messages and photos on social media',
        'uncomfortable staring and following me to hostel',
        'verbal sexual harassment with lewd comments',
        'gender-based harassment and discriminatory remarks',
        'inappropriate advances by teaching assistant',
        'repeated unwanted attention despite saying no',
        'professor making uncomfortable personal remarks',
        'classmate touching me inappropriately during lab sessions',
        'someone taking photos of me without consent',
        'receiving late night calls from unknown campus number',
        'harassment in form of catcalling near campus gate',
        'peer pressuring me into uncomfortable situations',
        'someone spread rumors about my personal life',
        'inappropriate jokes with sexual undertones in class',
        'staff member asking for personal favors inappropriately',
        'constant unwanted compliments making me uncomfortable'
    ],
    'Violence': [
        'physical fight between students in the cafeteria',
        'assault in parking lot after evening class',
        'someone hit me during heated argument over project',
        'violent confrontation in cafeteria over seating',
        'physical attack by group of students near hostel',
        'beaten up after class due to personal conflict',
        'threatening with knife during dispute',
        'physical abuse in hostel room by roommate',
        'violent behavior during sports event, player attacked referee',
        'got punched in the face during college fest',
        'group fight broke out in campus ground',
        'student attacked with stick near library',
        'violent clash between two groups in auditorium',
        'someone threw chair at me during argument',
        'physical assault during exam over cheating accusation',
        'attacked with stones by outsiders who entered campus',
        'violent incident where student was pushed down stairs',
        'fight involving weapons in hostel mess',
        'brutal beating by seniors in isolated area',
        'witnessed violent attack on security guard'
    ],
    'Verbal Abuse': [
        'constant verbal insults and name calling by classmates',
        'abusive language by professor during lecture',
        'threatening words and intimidation by senior',
        'shouting and screaming at students in public',
        'offensive remarks about my family background',
        'racist comments in classroom about my ethnicity',
        'derogatory language used by lab instructor',
        'verbal threats of physical harm',
        'cursing and swearing at me in front of others',
        'humiliating comments in public during presentation',
        'professor using abusive words when I asked question',
        'classmate verbally attacking me over minor issue',
        'casteist slurs used by fellow students',
        'verbal bullying about my appearance and weight',
        'threatening language used by group of students',
        'professor shouting and using harsh words regularly',
        'abusive comments about my academic performance',
        'verbal harassment with religious slurs',
        'constant mocking and ridiculing in class',
        'threatening to fail me using abusive language'
    ],
    'Theft': [
        'laptop stolen from library while I went to restroom',
        'wallet missing from my bag in classroom',
        'bike theft from parking area during class hours',
        'phone stolen from desk in classroom',
        'books and notes missing from my locker',
        'money stolen from hostel room when I was sleeping',
        'bicycle disappeared from cycle stand overnight',
        'personal belongings taken from sports complex locker',
        'theft in computer lab, my hard drive is missing',
        'valuables missing from bag during lecture',
        'someone stole my calculator during exam',
        'headphones stolen from library table',
        'watch missing after gym session',
        'bag containing laptop stolen from cafeteria',
        'charger and accessories stolen from hostel room',
        'project materials and equipment stolen from lab',
        'clothes stolen from hostel laundry area',
        'sports equipment missing from my locker',
        'expensive textbooks stolen from library desk',
        'identity card and documents stolen from bag'
    ],
    'Safety Concern': [
        'broken stairs in academic building, someone might fall',
        'poor lighting in parking area creates safety risk',
        'unsafe electrical wiring exposed in classroom',
        'slippery floor without warning sign near entrance',
        'fire extinguisher not working, checked yesterday',
        'damaged railing on third floor balcony',
        'lack of security cameras in isolated campus areas',
        'dangerous construction zone without proper barriers',
        'unsafe lab equipment with exposed wires',
        'health hazard in cafeteria, found insects in food',
        'broken window panes in hostel room',
        'malfunctioning elevator getting stuck frequently',
        'no emergency exit signs in building',
        'loose tiles on corridor floor causing trips',
        'water leakage creating slippery surface',
        'broken door locks in washroom stalls',
        'sharp metal edges protruding from benches',
        'inadequate ventilation in chemistry lab',
        'overloaded electrical sockets sparking',
        'blocked fire exits with stored furniture'
    ],
    'Discrimination': [
        'treated differently due to my caste background',
        'religious discrimination by peers who exclude me',
        'bias based on my gender identity in sports selection',
        'excluded from group projects due to my background',
        'unfair treatment because of my religion',
        'discrimination in club selection, rejected without reason',
        'prejudice based on my physical appearance',
        'biased grading by professor, others get better marks',
        'excluded from group activities because I am different',
        'differential treatment in hostel room allocation',
        'denied opportunities due to language barrier',
        'professor favoring students from certain regions',
        'discrimination based on economic background',
        'excluded from events due to my disability',
        'unfair treatment in scholarship selection',
        'bias in internship recommendations',
        'discriminated against for my political views',
        'excluded from study groups due to my accent',
        'unequal access to facilities based on gender',
        'discrimination in leadership positions selection'
    ],
    'Other': [
        'general complaint about poor wifi connectivity',
        'noise disturbance in library from construction work',
        'parking space shortage during peak hours',
        'food quality concern, found hair in meal',
        'internet connectivity problem in hostel',
        'administrative issue with fee payment system',
        'lost my ID card near main gate',
        'suggestion to extend library hours',
        'general feedback about canteen timings',
        'complaint about irregular bus schedule',
        'request for more water coolers on campus',
        'air conditioning not working in lecture hall',
        'suggestion to improve waste management',
        'complaint about long queues in admin office',
        'request for better sports facilities',
        'feedback about outdated course curriculum',
        'complaint about limited printing facilities',
        'suggestion for more green spaces on campus',
        'issue with hostel room maintenance delay',
        'request for extended cafeteria menu options'
    ],
    'Fake/Spam': [
        'test1 test2 test3',
        'testing testing 123',
        'sample report here',
        'demo incident submission',
        'asdfgh qwerty keyboard',
        'xxxxxx yyyyyy zzzzz',
        'aaaaaa bbbbbb cccccc',
        'help help help help',
        'test test test test',
        'lorem ipsum dolor sit',
        'hello world foo bar',
        'blah blah blah blah',
        '123456 789 numbers only',
        'qwerty asdf zxcv hjkl',
        'random gibberish nonsense text',
        'spam junk garbage trash',
        'placeholder temporary dummy',
        'checking trying testing debug',
        'abc xyz 123 test pattern',
        'not real fake report submission'
    ]
}

# Create and train the classification model
def create_classifier():
    """
    Creates and trains a text classification pipeline.
    Uses TF-IDF vectorization and Multinomial Naive Bayes.
    """
    # Prepare training data
    texts = []
    labels = []
    
    for category, examples in TRAINING_DATA.items():
        texts.extend(examples)
        labels.extend([category] * len(examples))
    
    # Create pipeline
    classifier = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),  # Use unigrams and bigrams
            stop_words='english'
        )),
        ('clf', MultinomialNB(alpha=0.1))
    ])
    
    # Train the model
    classifier.fit(texts, labels)
    
    return classifier

# Initialize the classifier
_classifier = create_classifier()


def classify_incident(text, return_confidence=False):
    """
    Classifies incident text into categories using ML.
    
    Args:
        text: Input text to classify
        return_confidence: If True, returns (category, confidence)
    
    Returns:
        category name or (category, confidence) tuple
    """
    # Preprocess text
    cleaned_text = preprocess_text(text)
    
    if not cleaned_text:
        return ("Other", 0.0) if return_confidence else "Other"
    
    try:
        # Get prediction
        category = _classifier.predict([cleaned_text])[0]
        
        if return_confidence:
            # Get probability scores
            probabilities = _classifier.predict_proba([cleaned_text])[0]
            confidence = float(np.max(probabilities))
            return category, confidence
        
        return category
    
    except Exception as e:
        print(f"Classification error: {e}")
        return ("Other", 0.0) if return_confidence else "Other"


# ==================== SENTIMENT ANALYSIS ====================

def sentiment_score(text):
    """
    Analyzes sentiment of text using TextBlob.
    Returns polarity score between -1 (negative) and 1 (positive).
    """
    cleaned_text = preprocess_text(text)
    
    if not cleaned_text:
        return 0.0
    
    try:
        blob = TextBlob(cleaned_text)
        return round(blob.sentiment.polarity, 3)
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return 0.0


def get_sentiment_label(polarity):
    """
    Converts polarity score to human-readable label.
    """
    if polarity >= 0.3:
        return "Positive"
    elif polarity <= -0.3:
        return "Negative"
    else:
        return "Neutral"


def analyze_emotions(text):
    """
    Detects emotional tone in text.
    Returns primary emotion and intensity.
    """
    cleaned_text = preprocess_text(text)
    
    if not cleaned_text:
        return "Neutral", 0.0
    
    # Emotion keywords
    emotions = {
        'fear': ['scared', 'afraid', 'terrified', 'frightened', 'worried', 'anxious', 'panic'],
        'anger': ['angry', 'furious', 'mad', 'outraged', 'irritated', 'annoyed', 'frustrated'],
        'sadness': ['sad', 'depressed', 'upset', 'hurt', 'disappointed', 'miserable', 'unhappy'],
        'disgust': ['disgusted', 'revolted', 'sick', 'repulsed', 'appalled'],
        'distress': ['distressed', 'troubled', 'disturbed', 'uncomfortable', 'uneasy', 'helpless']
    }
    
    text_lower = cleaned_text.lower()
    emotion_scores = {}
    
    for emotion, keywords in emotions.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            emotion_scores[emotion] = score
    
    if not emotion_scores:
        return "Neutral", 0.0
    
    # Get primary emotion
    primary_emotion = max(emotion_scores, key=emotion_scores.get)
    intensity = min(emotion_scores[primary_emotion] / 3.0, 1.0)  # Normalize to 0-1
    
    return primary_emotion.capitalize(), round(intensity, 2)


def get_urgency_suggestion(text, category, sentiment):
    """
    Suggests urgency level based on text analysis.
    Returns: 'Low', 'Medium', or 'High'
    """
    text_lower = text.lower()
    
    # High urgency keywords
    high_urgency_words = ['emergency', 'urgent', 'immediate', 'danger', 'threat', 'weapon', 
                          'assault', 'attack', 'bleeding', 'injured', 'help', 'now']
    
    # Check for high urgency
    if any(word in text_lower for word in high_urgency_words):
        return 'High'
    
    # Category-based urgency
    high_urgency_categories = ['Violence', 'Harassment', 'Safety Concern']
    if category in high_urgency_categories:
        return 'High'
    
    # Sentiment-based urgency
    if sentiment < -0.5:  # Very negative sentiment
        return 'High'
    elif sentiment < -0.2:
        return 'Medium'
    
    return 'Medium'


# ==================== COMPREHENSIVE ANALYSIS ====================

def analyze_incident(text):
    """
    Performs comprehensive analysis on incident text.
    Returns dictionary with all analysis results.
    """
    # Validate input
    is_valid, error_msg = validate_input(text)
    if not is_valid:
        return {
            'valid': False,
            'error': error_msg
        }
    
    # Check for fake/test reports
    is_fake, fake_reason = detect_fake_report(text)
    if is_fake:
        return {
            'valid': False,
            'error': fake_reason,
            'is_fake': True
        }
    
    # Preprocess
    cleaned_text = preprocess_text(text)
    
    # Classification
    category, confidence = classify_incident(cleaned_text, return_confidence=True)
    
    # Secondary fake detection: Check if classified as Fake/Spam
    is_likely_fake = False
    fake_warning = ""
    
    if category == "Fake/Spam":
        if confidence > 0.5:  # High confidence it's fake
            # Reject it completely
            return {
                'valid': False,
                'error': "This appears to be a test or spam submission. Please provide a genuine incident report.",
                'is_fake': True,
                'category': category,
                'confidence': confidence
            }
        else:
            # Low confidence, flag but allow with warning
            is_likely_fake = True
            fake_warning = "⚠️ Warning: This report appears suspicious. Please ensure it's a genuine incident."
    
    # Sentiment analysis
    sentiment = sentiment_score(cleaned_text)
    sentiment_label = get_sentiment_label(sentiment)
    
    # Emotion detection
    emotion, emotion_intensity = analyze_emotions(cleaned_text)
    
    # Urgency suggestion
    urgency = get_urgency_suggestion(cleaned_text, category, sentiment)
    
    result = {
        'valid': True,
        'category': category,
        'confidence': confidence,
        'sentiment_score': sentiment,
        'sentiment_label': sentiment_label,
        'emotion': emotion,
        'emotion_intensity': emotion_intensity,
        'suggested_urgency': urgency,
        'cleaned_text': cleaned_text
    }
    
    # Add warning if suspicious
    if is_likely_fake:
        result['warning'] = fake_warning
        result['is_suspicious'] = True
    
    return result
