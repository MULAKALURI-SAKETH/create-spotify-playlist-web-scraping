from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
year = date.split("-")[0]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
website = response.text
soup = BeautifulSoup(website, "html.parser")

song_reviews = soup.find_all(class_="lrv-a-unstyle-list lrv-u-flex lrv-u-height-100p lrv-u-flex-direction-column@mobile-max")
song_names = [review.find("h3").getText().strip() for review in song_reviews]
song_uris = []

# Configuration
scope = "playlist-modify-private"
CLIENT_ID = "33dc5c24b9cc4c5aa45ada1ea8da4a25"
CLIENT_SECRET = "2200be3fa1484c72a2da751f4b27797d"
REDIRECT_URI = "http://localhost:5000"
USERNAME = "31gvsxzaynhqdemvpbequyw56zbq"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope, cache_path="token.txt", show_dialog=True))
user_id = sp.current_user()["id"]

for song in song_names:
    song_details = sp.search(f"track:{song} year:{year}", type="track")
    try:
        song_uri = song_details["tracks"]['items'][0]['uri']
        song_uris.append(song_uri)
    except IndexError:
        # print(f"Song '{song}' not found in the track")
        pass
playlist_id = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)['id']
sp.playlist_add_items(playlist_id, song_uris)