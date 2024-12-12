import requests
from datetime import datetime

def get_channel_info(api_key, channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            channel_data = data["items"][0]["snippet"]
            channel_image_url = channel_data["thumbnails"]["high"]["url"]
            return channel_image_url
        else:
            return None
    else:
        return None

def get_video_info(api_key, video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            video_data = data["items"][0]["snippet"]
            video_title = video_data["title"] 
            thumbnail_url = video_data["thumbnails"]["high"]["url"]
            release_date = datetime.fromisoformat(video_data["publishedAt"].replace("Z", "+00:00"))
            convert_date = release_date.strftime("%B %d, %Y")
            channel_name = video_data["channelTitle"]
            channel_id = video_data["channelId"] 

            # Get channel image URL
            channel_image_url = get_channel_info(api_key, channel_id)

            return {
                "thumbnail_url": thumbnail_url,
                "video_title":video_title,
                "release_date": convert_date,
                "channel_name": channel_name,
                "channel_image_url": channel_image_url 
            }
        else:
            return {"error": "Video not found or invalid video ID"}
    else:
        return {"error": f"Failed to retrieve data. Status code: {response.status_code}"}
