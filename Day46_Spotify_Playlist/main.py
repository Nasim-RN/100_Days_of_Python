from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Scraping Billboard 100

print("Welcome to the Music Time Machine!")
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

artist_names_spans = soup.find_all(name="span", class_="u-max-width-330")
artist_names = [artist.getText().strip("\n\t") for artist in artist_names_spans]

song_and_artist = dict(zip(song_names, artist_names))
print(song_and_artist)
print("\nSearching for songs on Spotify and creating new playlist...")


# Spotify Authentication

OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIPY_CLIENT_ID = "YOUR CLIENT ID"
SPOTIPY_CLIENT_SECRET = "YOUR CLIENT SECRET"
SPOTIPY_REDIRECT_URI = "http://example.com"
SPOTIPY_SCOPE = "playlist-modify-private"


sp = spotipy.Spotify(
auth_manager=SpotifyOAuth(
client_id=SPOTIPY_CLIENT_ID,
client_secret=SPOTIPY_CLIENT_SECRET,
redirect_uri=SPOTIPY_REDIRECT_URI,
scope=SPOTIPY_SCOPE,
show_dialog=True,
cache_path="token.txt"
)
)
user_id = sp.current_user()["id"]
print(user_id)

# Search Spotify for songs by title and artist
song_uris = []
for(song_names, artist_names) in song_and_artist.items():
    try:
        result = sp.search(q=f"track:{song_names} artist:{artist_names}", type="track")
        print(result)
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song_names} doesn't exist in Spotify. Skipped.")
print(f"Number of songs found: {len(song_uris)}")

# Create a new private playlist in Spotify

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, )
print(playlist)


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
