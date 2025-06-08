import re
from sklearn.feature_extraction.text import TfidfVectorizer
from config import korean_stopwords, travel_keyword_weights, okt, TOP_KEYWORDS, TRAVEL_SCORE_THRESHOLD, exclude_keywords

def tokenize(text):
    return [t for t in okt.nouns(text) if t not in korean_stopwords and len(t) > 1]

def extract_mixed_keywords(text, top_n=TOP_KEYWORDS):
    korean_text = ' '.join(re.findall(r'[가-힣]+', text))
    english_text = ' '.join(re.findall(r'[a-zA-Z]+', text))

    ko_keywords = [t for t in okt.nouns(korean_text) if t not in korean_stopwords and len(t) > 1]

    en_keywords = []
    if english_text.strip():
        try:
            tfidf = TfidfVectorizer(stop_words='english')
            matrix = tfidf.fit_transform([english_text])
            scores = matrix.toarray().flatten()
            terms = tfidf.get_feature_names_out()
            top_indices = scores.argsort()[-top_n:][::-1]
            en_keywords = [terms[i] for i in top_indices if scores[i] > 0]
        except ValueError:
            pass
    return list(dict.fromkeys(ko_keywords + en_keywords))[:top_n] or ["키워드없음"]

def extract_hashtags(desc):
    return re.findall(r"#(\w+)", desc.lower())

def is_excluded_video(title, description):
    text = (title + " " + description).lower()
    return any(word in text for word in exclude_keywords)

def calculate_travel_score(keywords, hashtags):
    score = 0
    for kw in keywords + hashtags:
        score += travel_keyword_weights.get(kw.lower(), 0)
    return score

def is_travel_related(keywords, hashtags, threshold=TRAVEL_SCORE_THRESHOLD):
    return calculate_travel_score(keywords, hashtags) >= threshold
