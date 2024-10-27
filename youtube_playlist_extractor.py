import os
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables from .env file
load_dotenv('/Users/netraranga/Desktop/Projects/.env')

# Get YouTube API key from environment variables
api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)

def get_playlist_videos(playlist_id):
    """
    Retrieve all videos from a YouTube playlist.
    
    Args:
    playlist_id (str): The ID of the YouTube playlist.
    
    Returns:
    list: A list of dictionaries containing video IDs and titles.
    """
    videos = []
    next_page_token = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()

        for item in playlist_response["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            title = item["snippet"]["title"]
            videos.append({"id": video_id, "title": title})

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

    return videos

def get_video_transcript(video_id):
    """
    Retrieve the transcript of a YouTube video.
    
    Args:
    video_id (str): The ID of the YouTube video.
    
    Returns:
    str: The full transcript of the video, or None if unavailable.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript])
    except Exception as e:
        print(f"Error fetching transcript for video {video_id}: {str(e)}")
        return None

def extract_playlist_contents(playlist_url):
    """
    Extract contents (titles and transcripts) from all videos in a playlist.
    
    Args:
    playlist_url (str): The URL of the YouTube playlist.
    
    Returns:
    list: A list of dictionaries containing video titles and contents.
    """
    playlist_id = playlist_url.split("list=")[1]
    videos = get_playlist_videos(playlist_id)
    extracted_contents = []

    for video in videos:
        title = video["title"]
        transcript = get_video_transcript(video["id"])
        if transcript:
            extracted_contents.append({
                "Video Title": title,
                "Video Contents": f"{title}\n\n{transcript}"
            })
        else:
            extracted_contents.append({
                "Video Title": title,
                "Video Contents": f"{title}\n\nNo transcript available."
            })

    return extracted_contents

if __name__ == "__main__":
    # URL of the CS229 course playlist
    playlist_url = "https://www.youtube.com/playlist?list=PLoROMvodv4rNyWOpJg_Yh4NSqI4Z4vOYy"
    contents = extract_playlist_contents(playlist_url)

    # Create a DataFrame from the extracted contents
    df = pd.DataFrame(contents)

    # Save the contents to a CSV file
    csv_filename = "youtube_playlist_contents.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Contents saved to {csv_filename}")

# Note: This script is part of a larger project to create an AI-powered
# course assistant for Stanford's CS229 Machine Learning course.
# It extracts video titles and transcripts from the course's YouTube playlist,
# which are then used to train an AI model to answer questions about the course content.
