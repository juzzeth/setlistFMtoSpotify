import sys
import config
import spotipy
import spotipy.util as util
from html.parser import HTMLParser
import urllib.request as urllib2

def get_tracks(setURL, songArray):

    class songParser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.inLink = False
            self.dataArray = []
            self.countSongs = 0
            self.lasttag = None
            self.lastname = None
            self.lastvalue = None

        def handle_starttag(self, tag, attrs):
            self.inLink = False
            if tag == 'a':
                for name, value in attrs:
                    if name == 'class' and value == 'songLabel': # this is what the songs are classed as, if this changes, script breaks
                        self.countSongs += 1
                        self.inLink = True
                        self.lasttag = tag

        def handle_endtag(self, tag):
            if tag == "a":
                self.inlink = False

        def handle_data(self, data):
            if self.lasttag == 'a' and data != '\\n' and self.inLink and data.strip():
                songArray.append(data)

    parser = songParser()

    html_page = urllib2.urlopen(setURL)

    parser.feed(str(html_page.read()))

    return songArray

username = '1236988197' #spotify user ID
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

    # set artist detail
    

    # set track, this will be a loop eventually
    songArray = []
    songArray = get_tracks(setlistURL, songArray)
    for track in songArray:
        track = track.replace("'","")
        results = sp.search(q='artist:' + artist + ' track:' + track, type='track', limit='1')
        item = results['tracks']['items']
        if len(item) > 0:
            track = item[0]
            trackID = track['id']
            trackList.append(trackID)

    print (songArray)
    print
    print ("Your playlist has been created")
    sp.user_playlist_add_tracks(username, playlistID, trackList)

else:
    print ("Can't get token for", username)