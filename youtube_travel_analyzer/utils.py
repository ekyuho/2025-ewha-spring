import pandas as pd

def analyze_and_display(df):
    if df.empty:
        print("여행 관련 영상이 없습니다.")
        return

    df['업로드일'] = pd.to_datetime(df['업로드일'])

    print("\n📺 수집된 여행 영상 목록:")
    print(df[['제목', '업로더', '조회수', '업로드일', '해시태그', '핵심키워드']].to_string(index=False))

    print("\n📅 월별 업로드 수:")
    print(df.groupby(df['업로드일'].dt.to_period("M")).size())

    df.to_csv("youtube_travel_videos.csv", index=False, encoding="utf-8-sig")
