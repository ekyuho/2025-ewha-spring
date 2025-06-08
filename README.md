# 2025-ewha-spring
## YouTube Travel Analyzer

유튜브 API를 사용해 여행 관련 영상을 수집하고, 텍스트 분석으로 여행 키워드를 추출하는 프로젝트입니다.

### 주요 파일 구조
---
- `main.py` : 실행 스크립트  
- `youtube_api.py` : 유튜브 API 호출  
- `text_processing.py` : 텍스트 전처리 및 키워드 분석  
- `config.py` : 환경변수 및 설정값 로딩  
- `stopwords-ko.txt` : 한국어 불용어 리스트  
- `.env` : API 키 등 환경변수 (깃허브에 포함하지 말 것)  
- `requirements.txt` : 필요한 패키지 목록  

### 설치 및 실행

1. 가상환경 생성 및 활성화  
2. `pip install -r requirements.txt`  
3. `.env` 파일 생성 후 아래 변수 설정

        YOUTUBE_API_KEY="여기에_API키"
        STOPWORDS_PATH="stopwords-ko.txt"
        REGION_CODE="KR"
        MAX_RESULTS=50
        TOP_KEYWORDS=3
        TRAVEL_SCORE_THRESHOLD=3

4. `python main.py` 실행

### 주의사항

- `.env` 파일에 API 키 등 민감 정보 포함, 깃허브 업로드 금지  
- API 키는 Google Cloud Console에서 발급받을 것  

