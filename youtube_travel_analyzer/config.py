import os
from dotenv import load_dotenv
from konlpy.tag import Okt

load_dotenv()  # .env 파일 로드

STOPWORDS_PATH = "stopwords-ko.txt"
REGION_CODE = os.getenv("REGION_CODE")
MAX_RESULTS = int(os.getenv("MAX_RESULTS"))
TOP_KEYWORDS = int(os.getenv("TOP_KEYWORDS"))
TRAVEL_SCORE_THRESHOLD = int(os.getenv("TRAVEL_SCORE_THRESHOLD"))

# 형태소 분석기 초기화
okt = Okt()

# 불용어 로딩
def load_stopwords(path):
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

korean_stopwords = load_stopwords(STOPWORDS_PATH)

# 여행 키워드 정의 및 가중치
CATEGORY_WEIGHTS = {"일반": 3, "지역": 2, "활동": 2, "교통": 2, "테마": 1, "영어": 1}
travel_keywords_by_category = {
    "일반": ['여행', '브이로그', '트립', '휴가', '투어', '출발', '여정', '경로', '코스', '루트'],
    "지역": ['제주', '제주도', '부산', '서울', '강릉', '여수', '전주', '속초', '포항', '춘천', '경주', '울릉도',
             '한강', '남산', '경복궁', '해운대', '명동', '도쿄', '오사카', '후쿠오카', '삿포로', '방콕',
             '다낭', '푸켓', '세부', '발리', '파리', '런던', '로마', '바르셀로나', '베네치아', '뉴욕', 'LA',
             '샌프란시스코', '토론토', '멕시코시티'],
    "활동": ['캠핑', '등산', '트레킹', '낚시', '서핑', '스노클링', '자전거', '스쿠버', '패러글라이딩'],
    "교통": ['기차여행', '렌트카', '자유여행', '패키지', '비행기', '비자', '항공권'],
    "테마": ['맛집', '숙소', '호텔', '게스트하우스', '시장', '야시장', '풍경', '문화', '자연', '전통',
             '온천', '휴양지', '리조트', '관광지', '유적지', '명소'],
    "영어": ['trip', 'travel', 'vlog', 'resort', 'island', 'adventure',
             'tour', 'hiking', 'camping', 'beach', 'flight', 'visa', 'ticket', 'hotel', 'local']
}
travel_keyword_weights = {
    kw.lower(): CATEGORY_WEIGHTS[cat]
    for cat, kws in travel_keywords_by_category.items()
    for kw in kws
}

exclude_keywords = ['mv', 'music', '광고', 'promo', 'review', '뮤직비디오', 'official', '뉴스', 'news','ebs', '교육', '방송', 'kbs', 'mbc', 'sbs']
