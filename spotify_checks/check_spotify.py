import json

bookmarks = "/home/martin/.config/BraveSoftware/Brave-Browser/Default/Bookmarks"
playlist_ids = []

with open(bookmarks,'r') as f:
	bookmarks = json.load(f)

top_level_items =bookmarks['roots']['bookmark_bar']['children']
for item in top_level_items:
	if "Spotify" in item['name']:
		for linkitem in item['children']:
			name = linkitem['name']
			url = linkitem['url']
			playlist_ids.append((name,url.split('/')[-1]))


#%%
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "061482cfc1c1473098dbe0e71a6848b1"
client_secret = "c7b8be2addaa41d6a47e191042389ebf"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#%%
# results = sp.search(q="year:2022", type="track")
# print(results)
# for track in results['tracks']['items']:
#     print(track['name'], ' - ', track['artists'][0]['name'])
# results = sp.recommendations(seed_genres=['pop', 'rock'], limit=10)
# for track in results['tracks']:
#     print(track['name'], ' - ', track['artists'][0]['name'])

music_dir = "/mnt/HardDrive/Media/Music" 
for name,playlist_id in playlist_ids[::-1]: # newest first
	playlist = sp.playlist(playlist_id)
	out_dir= f"{music_dir}/{name}"
	os.makedirs(out_dir,exist_ok=True)
	for track in playlist['tracks']['items']:
		search_querry = track['track']['name'] + ' - '+ track['track']['artists'][0]['name']+ " lyrics"
		# search_querry = 
		# print(search_querry)
		cmd = f"yt-dlp \"ytsearch1:{search_querry} \" -f 140 -o \"{out_dir}/%(title)s.%(ext)s\""
		# print(cmd)

		os.system(cmd)
		# break




