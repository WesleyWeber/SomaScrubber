import subprocess
import requests
from bs4 import BeautifulSoup

PLAYLIST_DIR = "./playlists/"
PLAYLISTS = []
BASE_URL = "https://www.somafm.com"
TARGET_PAGE = "/listen" 
URL = "{}{}".format(BASE_URL,TARGET_PAGE)

PAGE = requests.get(URL)
SOUP = BeautifulSoup(PAGE.content, 'html.parser')

PLAYLIST_LIST = SOUP.find_all("nobr")



for playlist in PLAYLIST_LIST:
    if any(['MP3:' in contents for contents in playlist.contents]):
        mp3_url = playlist.find('a')
        mp3_playlist_url = BASE_URL+mp3_url.attrs['href']
        PLAYLISTS.append(mp3_playlist_url)

for playlist in PLAYLISTS:
    print(playlist)
    r = requests.get(playlist, allow_redirects=True)
    filename = playlist[playlist.rfind('/')+1:]
    fullfilepath = PLAYLIST_DIR + filename
    open(fullfilepath, 'wb').write(r.content)


