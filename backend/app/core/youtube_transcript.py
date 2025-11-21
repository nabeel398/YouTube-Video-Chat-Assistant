from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import re
import time

def fetch_transcript(video_url: str, max_retries=3):
    try:
        # Extract video ID
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\/\?\#]+)',
            r'youtube\.com\/v\/([^&\/\?\#]+)'
        ]
        
        video_id = None
        for pattern in patterns:
            match = re.search(pattern, video_url)
            if match:
                video_id = match.group(1)
                break
        
        if not video_id:
            raise ValueError("Invalid YouTube URL - could not extract video ID")
        
        print(f"Fetching transcript for video ID: {video_id}")

        # Retry mechanism for long videos
        for attempt in range(max_retries):
            try:
                # Create API instance and fetch transcript
                yt_api = YouTubeTranscriptApi()
                
                # Try to get transcript in English first, fallback to any available
                try:
                    # Method 1: Try with English
                    fetched_transcript = yt_api.fetch(video_id, languages=['en'])
                except:
                    # Method 2: Try any available language
                    fetched_transcript = yt_api.fetch(video_id)
                
                # Extract text from transcript snippets
                text = " ".join([snippet.text for snippet in fetched_transcript])
                
                print(f"Successfully fetched transcript with {len(fetched_transcript)} segments")
                print(f"Transcript length: {len(text)} characters")
                
                return text
                
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5  # 5, 10, 15 seconds
                    print(f"Attempt {attempt + 1} failed. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise e
        
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video")
    except NoTranscriptFound:
        raise Exception("No transcript found for this video. This video might not have captions.")
    except VideoUnavailable:
        raise Exception("Video is unavailable or doesn't exist")
    except Exception as e:
        error_msg = str(e)
        if "too long" in error_msg.lower() or "timeout" in error_msg.lower():
            raise Exception("Video is too long (2+ hours). Please try a shorter video or check if captions are available.")
        elif "retry" in error_msg.lower():
            raise Exception("Service is busy. Please try again in a few moments.")
        else:
            raise Exception(f"Error fetching transcript: {error_msg}")