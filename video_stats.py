import requests,json
API_KEY = "AIzaSyAIG3_7AMrj4_uKaiISpgx14K4UWY6MkPk"
CHANNEL_HANDLE = "MrBeast"

import os 
from dotenv import load_dotenv

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

if __name__ == "__main__":
    get_playlist_id()
