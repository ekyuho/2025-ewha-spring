from youtube_api import get_travel_videos
from utils import analyze_and_display

if __name__ == "__main__":
    df = get_travel_videos()
    analyze_and_display(df)