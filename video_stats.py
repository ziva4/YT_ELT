import requests,json

CHANNEL_HANDLE = "MrBeast"
max_results = 50
import os 
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path="./.env")

def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response = requests.get(url)
        data = response.json() 
        #json.dumps is used to convert a python object into a json string. The indent parameter is used to specify the number of spaces to use for indentation in the output json string. In this case, it is set to 4, which means that each level of the json structure will be indented by 4 spaces for better readability.
        #print(json.dumps(data, indent=4))
        channel_items = data['items'][0]
        channel_playlistId = channel_items['contentDetails']['relatedPlaylists']['uploads']
        print(channel_playlistId)
        return channel_playlistId
    except requests.exceptions.RequestException as e:
        raise e

def get_video_ids(playlist_id):
    video_ids = []
    pageToken = None
    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}'
    try:
        while True:
            url = base_url
            if pageToken:
                url += f'&pageToken={pageToken}'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            pageToken = data.get('nextPageToken')
            if not pageToken:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e

def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_id_list, batch_size):
        for i in range(0, len(video_id_list), batch_size):
            yield video_id_list[i:i + batch_size]

    try:
        for batch in batch_list(video_ids, max_results):
            video_ids_str = ','.join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_ids_str}&key={API_KEY}"

            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):

                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']

                video_data = {
                    "video_id": item['id'],
                    "title": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    "viewCount": statistics.get('viewCount'),
                    "likeCount": statistics.get('likeCount'),
                    "commentCount": statistics.get('commentCount')
                }

                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(extracted_data):
    today = datetime.today().strftime("%Y-%m-%d")
    os.makedirs("data", exist_ok=True)  # create folder if not exists

    file_path = f"./data/YT_data_{today}.json"

    with open(file_path, 'w', encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    playlist_id = get_playlist_id() 
    video_ids = get_video_ids(playlist_id)
    video_data = extract_video_data(video_ids)
    save_to_json(video_data)


