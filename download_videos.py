import os
import requests
import subprocess
import isodate

API_KEY = 'AIzaSyA_oQf9cK-cTljPgFprRuR46B-Re5MlOXw'  # Replace with your actual API key
SEARCH_QUERY = 'truck accident shorts'
MAX_RESULTS = 10
API_URL = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults={MAX_RESULTS}&q={SEARCH_QUERY}&key={API_KEY}'

response = requests.get(API_URL)

# Print the response to check if the API call was successful
print("API Response Status Code:", response.status_code)
print("API Response JSON:", response.json())

videos = response.json().get('items', [])

def get_video_details(video_id):
    video_details_url = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={API_KEY}'
    video_response = requests.get(video_details_url)
    return video_response.json().get('items', [])[0]

if not os.path.exists('videos'):
    os.makedirs('videos')

for video in videos:
    video_id = video['id']['videoId']
    video_title = video['snippet']['title']
    video_details = get_video_details(video_id)
    duration = isodate.parse_duration(video_details['contentDetails']['duration']).total_seconds()

    print(f'Video: {video_title}, Duration: {duration}s')

    if 10 <= duration <= 60:
        print(f'Downloading: {video_title} (Duration: {duration}s)')
        
        # Use yt-dlp to download the video
        download_command = f'yt-dlp https://www.youtube.com/watch?v={video_id} -o "videos/{video_title}.%(ext)s"'
        print("Executing Command:", download_command)
        result = subprocess.run(download_command, shell=True)
        print("Download Result:", result)
        
        # Change the resolution after downloading the video
        input_file = f'videos/{video_title}.mp4'  # Assuming the default format is mp4
        output_file = f'videos/{video_title}_resized.mp4'
        resize_command = f'ffmpeg -i "{input_file}" -vf scale=540:960 "{output_file}"'
        print("Executing Command:", resize_command)
        resize_result = subprocess.run(resize_command, shell=True)
        print("Resize Result:", resize_result)
    else:
        print(f'Skipping: {video_title} (Duration: {duration}s)')

print("Download and resize completed!")
