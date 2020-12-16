import config
import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util

def get_tracks(setURL, tracks):
    page = requests.get(setURL)
    if page.status_code == 404:
        print("Page not found! Please check the setlist URL.")
        raise SystemExit(0)

    soup = BeautifulSoup(page.text, "html.parser")

    for track in soup.findAll("a", class_="songLabel"):
        tracks.append(track.text.strip())

    return tracks

username = config.username #spotify user ID
token = util.prompt_for_user_token(username,'playlist-modify-private',client_id=config.id,client_secret=config.secret,redirect_uri='http://localhost')

if token:
    sp = spotipy.Spotify(auth=token)

    # set playlist name and create it
    playlistName = input("Please enter the playlist name: ") #replace with setlist title
    setlistURL = input("Please paste in the setlist.fm URL: ")
    artist = setlistURL.split('/')[-3].split('/')[0]
    artist = artist.replace("-"," ")

    trackList = []
    playlistResult = sp.user_playlist_create(username, playlistName, public=False)

    # return playlist ID after it is created so we can add to it
    playlistID = playlistResult['id']

    tracks = []
    tracks = get_tracks(setlistURL, tracks)
    for track in tracks:
        track = track.replace("'","")
        results = sp.search(q='artist:' + artist + ' track:' + track, type='track', limit='1')
        item = results['tracks']['items']
        if len(item) > 0:
            track = item[0]
            trackID = track['id']
            trackList.append(trackID)

    print (tracks)
    print
    sp.user_playlist_add_tracks(username, playlistID, trackList)
    print ("Your playlist has been created")
    

else:
    print ("Can't get token for", username)