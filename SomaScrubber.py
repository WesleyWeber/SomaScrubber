import os
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
    if any(['MP3 PLS (SSL):' in contents for contents in playlist.contents]):
        mp3_url = playlist.find('a')
        mp3_playlist_url = BASE_URL+mp3_url.attrs['href']
        PLAYLISTS.append(mp3_playlist_url)

#Make playlist DIR and save to it
files=[]
os.makedirs(os.path.dirname(PLAYLIST_DIR), exist_ok=True)
for playlist in PLAYLISTS:
    r = requests.get(playlist, allow_redirects=True)
    filename = playlist[playlist.rfind('/')+1:]
    fullfilepath = PLAYLIST_DIR + filename
    open(fullfilepath, 'wb').write(r.content)

    with open(fullfilepath,'r') as f:
        playlist_doc = f.readlines()
    
    for line in playlist_doc:
        if 'File1' in line:
            files.append(line)

#build playlist body
document = "[playlist]\n"

#build FileN= lines
playlists_numbered = []
document += "numberofentries={}\n".format(len(files))
for index, line in enumerate(files):
    #playlists_numbered.append(line.replace('File1=h',"File{}=h".format(index+1)))
    document += line.replace('File1=h',"File{}=h".format(index+1))

print(document)

with open("{}{}".format(PLAYLIST_DIR, 'somafm_all.pls'),'w') as f:
    f.write(document)

