from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Scraping top 100 songs from Billboard
URL = "https://www.billboard.com/charts/hot-100/"
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(URL + date)

soup = BeautifulSoup(response.text, "html.parser")
all_songs = soup.select("li ul li h3")
# Removing spans and leaving only song names in the list
song_names = [song.getText().strip() for song in all_songs]

# Spotify Authentication
# please enter your own Spotify client secret, and client id (Spotify for Developers)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_secret="",
        redirect_uri="https://www.example.com",
        client_id="",
        cache_path="token.txt",
        show_dialog=True
    )
)

# Print current user id and info
user_id = sp.current_user()["id"]
print(user_id)

# Searching Spotify for songs by title and getting its URI
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(song)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# print(song_uris)

# Creating a new private playlist in Spotify for current user
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

# Adding found songs to the created playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
