import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# 1. Load the secrets from your .env file
load_dotenv()

# 2. Retrieve the Key and Build the Service
try:
    # Get the key from the environment variables
    api_key = os.getenv('YOUTUBE_KEY')
    
    # Check if the key was actually found
    if not api_key:
        raise ValueError("Key not found! Check your .env file.")

    # Create the youtube service object
    youtube = build('youtube', 'v3', developerKey=api_key)

    print("✅ Successfully connected to YouTube API!")

except Exception as e:
    print(f"❌ Error: {e}")
    print("Double check that your .env file exists and contains 'YOUTUBE_KEY=...'")