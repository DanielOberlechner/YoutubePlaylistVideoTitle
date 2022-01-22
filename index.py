# -*- coding: utf-8 -*-

import requests
import json
import datetime
import shutil
import os
import glob

from functions import slugify, getJSON

currentDate = datetime.datetime.now().strftime("%d %B %Y.txt")
apiKey = ""
errorOccurred = False

# Playlists Examples
Music = ["PLAYLIST_ID", "Music"]
Random = ["PLAYLIST_ID", "Random"]


# Add all Playlists variables to the allPlaylist Variable to download them properly
allPlaylists = [Music, Random]

part = "snippet"
directory = "playlists"

def checkForPrivacy(playlistid):
    url = (
            "https://www.googleapis.com/youtube/v3/playlistItems?key="
            + apiKey
            + "&playlistId="
            + playlistid[0]
            + "&part="
            + part
    )

    json = getJSON(url)
    global errorOccurred

    if "error" and 404 in json:
        print(f"The playlist {playlistid[1]} is set to private!")
        print("Please change the setting to at least unlisted!")
        errorOccurred = True
    elif "error" in json:
        print(f"The following problem has occured with this playlist:")
        print(f"{json['error']['code']}")
        print(f"{json['error']['errors'][0]['message']}")
        print(f"{json['error']['errors'][0]['reason']}")
        errorOccurred = True
    else:
        doRequest(playlistid[0])

def doRequest(elListo, pageToken=""):
    url = (
            "https://www.googleapis.com/youtube/v3/playlistItems?key="
            + apiKey
            + "&playlistId="
            + elListo
            + "&part="
            + part
            + "&maxResults=50"
            + "&pageToken="
            + pageToken
    )

    print(url)
    requestJSON = getJSON(url)

    for i in range(50):
        videoData = ""

        try:
            actualTitle = requestJSON["items"][i]["snippet"]["title"]
            actualVideoPostion = requestJSON["items"][i]["snippet"]["position"]
            generalInformation = requestJSON["pageInfo"]["totalResults"]

            if actualTitle == "Deleted video" or actualTitle == "Private video":
                videoData = str(actualVideoPostion) + " - " + actualTitle
                print(videoData)
                file = open(videoData + ".jpg", "wb")
                # file.write(thumbnail.content)
                file.close()
                continue

            actualChannelName = requestJSON["items"][i]["snippet"]["videoOwnerChannelTitle"]

            try:
                actualThumbnail = requestJSON["items"][i]["snippet"]["thumbnails"]["maxres"]["url"]
            except:
                actualThumbnail = requestJSON["items"][i]["snippet"]["thumbnails"]["high"]["url"]

            if actualVideoPostion == generalInformation - 1:
                print("All Videos got captured by this script successfully! :)")
                break

            videoData = str(actualVideoPostion) + " - " + actualTitle + " by " + actualChannelName

            try:
                file = open(videoData + ".jpg", "wb")
            except OSError:
                file = open(str(actualVideoPostion) + " - " + slugify(actualTitle) + " by " + actualChannelName + ".jpg", "wb")

            # Create Image
            thumbnail = requests.get(actualThumbnail)
            file.write(thumbnail.content)
            file.close()

            print(videoData)

        except Exception as Error:
            print("A error has occurred! continue with next video ... " + videoData + " this video could have a problem")
            print(Error.with_traceback())
            continue

    try:
        pageToken = requestJSON["nextPageToken"]
        if pageToken != "":
            doRequest(elListo, pageToken)
    except:
        print("Everything is done now!")


def Work():
    os.chdir("playlists")

    for playlist in allPlaylists:
        if playlist[1] not in os.listdir(os.getcwd()):
            os.mkdir(playlist[1])
            os.chdir(playlist[1])
            if currentDate not in os.listdir(os.getcwd()):
                os.mkdir(currentDate)
                os.chdir(currentDate)
            else:
                os.chdir(currentDate)
            checkForPrivacy(playlist)
            os.chdir("../../")
        else:
            os.chdir(playlist[1])
            if currentDate not in os.listdir(os.getcwd()):
                os.mkdir(currentDate)
                os.chdir(currentDate)
            else:
                os.chdir(currentDate)
            checkForPrivacy(playlist)
            os.chdir("../../")

    finale()

def finale():
    if errorOccurred == False:
        print("Everything went down just fine! :) Congratulations")
    else:
        print("It looks like there was some sort of problem while running this script!")
        print("Please investigate furhter on your own or create your own issue on Github:")
        print("https://github.com/DanielOberlechner/YoutubePlaylistVideoTitle/issues")

Work()
