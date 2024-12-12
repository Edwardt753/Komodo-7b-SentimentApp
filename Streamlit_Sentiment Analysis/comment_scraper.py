from googleapiclient.discovery import build

def fetch_comments(api_key, video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    all_comments = []

    def get_replies(youtube, parent_id):
        replies = []
        next_page_token = None

        while True:
            reply_request = youtube.comments().list(
                part="snippet",
                parentId=parent_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=next_page_token
            )
            reply_response = reply_request.execute()

            for item in reply_response['items']:
                replies.append(item['snippet']['textDisplay'])

            next_page_token = reply_response.get('nextPageToken')
            if not next_page_token:
                break

        return replies

    next_page_token = None
    while True:
        comment_request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100,
            pageToken=next_page_token
        )
        comment_response = comment_request.execute()

        for item in comment_response['items']:
            all_comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])

            if item['snippet']['totalReplyCount'] > 0:
                all_comments.extend(get_replies(youtube, item['snippet']['topLevelComment']['id']))

        next_page_token = comment_response.get('nextPageToken')
        if not next_page_token:
            break

    # Function clean sebelum return
    return all_comments
