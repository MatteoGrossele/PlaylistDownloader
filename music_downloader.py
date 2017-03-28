#!/bin/python2.7

from __future__ import unicode_literals
import json

import youtube_dl
import eyed3
import shutil
import os

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloaded.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
SEPARATOR = "-"
DIRECTORY = "playlist"
IMAGE = "wall.jpg"
PLAYLIST = "playlist.json"

playlist = None
json_data = open(PLAYLIST)
playlist = json.load(json_data)

# Check if playlist directory is present , if not create it
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

for song in playlist['playlist']['song']:

    #Create filename
    if song['subdir']:
        filename = song['subdir'] + "/" + song['artist'] + SEPARATOR + \
            song['title'] + ".mp3"
    else:
        filename = song['artist'] + SEPARATOR + song['title'] + ".mp3"

    #Skip song if already downloaded
    if os.path.isfile(DIRECTORY + "/" + filename):
        continue

    #Download song from youtube
    print("Downloading ->" + filename + "\n")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song['ytlink']])

    #Set ID3 tags for the downloaded file
    audiofile = eyed3.load("downloaded.mp3")

    audiofile.tag.artist = song['artist']
    audiofile.tag.title = song['title']
    imagedata = open(IMAGE, "rb").read()
    audiofile.tag.images.set(3, imagedata, "image/jpeg", "Album title")
    #audiofile.tag.images = ""
    #audiofile.tag.Date = song['year']

    audiofile.tag.save()

    #Move the file inside the folder

    shutil.move("downloaded.mp3", DIRECTORY + "/" + filename)
