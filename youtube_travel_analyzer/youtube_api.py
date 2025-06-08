import os
from datetime import datetime, timedelta
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
from text_processing import extract_mixed_keywords, extract_hashtags, is_excluded_video, is_travel_related
from config import MAX_RESULTS, REGION_CODE

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_youtube_video_ids(keyword='여행'):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    try:
        published_after = (datetime.utcnow() - timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%SZ')
        search_response = youtube.search().list(
            q=keyword,
            part='id',
            regionCode=REGION_CODE,
            maxResults=MAX_RESULTS,
            type='video',
            order='viewCount',
            publishedAfter=published_after
        ).execute()
        return [item['id']['videoId'] for item in search_response.get('items', [])]
    except Exception as e:
        print(f"유튜브 검색 실패: {e}")
        return []

def fetch_video_details(video_ids):
    if not video_ids:
        return pd.DataFrame()

    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    try:
        response = youtube.videos().list(
            part="snippet,statistics",
            id=','.join(video_ids)
        ).execute()

        results = []
        for item in response.get('items', []):
            title = item['snippet']['title']
            description = item['snippet'].get('description', '')
            keywords = extract_mixed_keywords(f"{title} {description}")
            hashtags = extract_hashtags(description)

            if is_excluded_video(title, description) or not is_travel_related(keywords, hashtags):
                continue

            results.append({
                "제목": title,
                "업로더": item['snippet']['channelTitle'],
                "조회수": int(item['statistics'].get('viewCount', 0)),
                "업로드일": item['snippet']['publishedAt'],
                "해시태그": ", ".join(hashtags) if hashtags else "없음",
                "핵심키워드": ", ".join(keywords)
            })
        return pd.DataFrame(results)
    except Exception as e:
        print(f"상세 정보 수집 실패: {e}")
        return pd.DataFrame()

def get_travel_videos(keyword='여행'):
    ids = fetch_youtube_video_ids(keyword)
    return fetch_video_details(ids)
