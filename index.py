import requests
import datetime
import os

from functions import slugify, getJSON
from decouple import config

currentDate = datetime.datetime.now().strftime("%Y-%m-%d")

apiKey = config("apiKey", default="")

Music = [config("Music", default=""), "Music"]
Computer = [config("Computer", default=""), "Computer"]
LilPeep = [config("LilPeep", default=""), "LilP33P"]
Nirvana = [config("Nirvana", default=""), "Nirvana"]
Programming = [config("Programming", default=""), "Programming"]

DEBUG = config("DEBUG", default=False, cast=bool)

# print(Computer)
errorOccurred = False

# Add all Playlists variables to the allPlaylist Variable to download them properly
allPlaylists = [Music, Computer, LilPeep, Nirvana, Programming]

part = "snippet"
directory = "playlists"
deletedVideos = 0


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
        print(f"The following problem has occurred with this playlist:")
        print(f"{json['error']['code']}")
        print(f"{json['error']['errors'][0]['message']}")
        print(f"{json['error']['errors'][0]['reason']}")
        errorOccurred = True
    else:
        print("This is playlist: " + playlistid[1])
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

    if DEBUG:
        print(url)

    requestJSON = getJSON(url)

    for i in range(50):
        videoData = ""

        try:
            # Preparing youtube info data
            actualTitle = requestJSON["items"][i]["snippet"]["title"]
            global actualVideoPosition
            actualVideoPosition = (
                requestJSON["items"][i]["snippet"]["position"] + 1
            )  # so that counting starts not from 0
            generalInformation = requestJSON["pageInfo"]["totalResults"]

            if actualTitle == "Deleted video" or actualTitle == "Private video":
                actualVideoPosition = actualVideoPosition - 1
                videoData = "(" + str(actualVideoPosition) + ")" + " - " + actualTitle
                # ToDo here must be the global keyword be set
                print(videoData)
                file = open(videoData + ".jpg", "wb")
                file.close()
                global deletedVideos
                deletedVideos += 1
                continue

            actualChannelName = requestJSON["items"][i]["snippet"][
                "videoOwnerChannelTitle"
            ]

            # try:
            #     actualThumbnail = requestJSON["items"][i]["snippet"]["thumbnails"][
            #         "maxres"
            #     ]["url"]
            # except:
            actualThumbnail = requestJSON["items"][i]["snippet"]["thumbnails"][
                "medium"
            ]["url"]

            # print("actualVideoPosition: ", actualVideoPosition)
            # print("generalInformation: ", generalInformation)

            videoData = (
                str(actualVideoPosition)
                + " - "
                + actualTitle
                + " by "
                + actualChannelName
            )

            try:
                file = open(videoData + ".jpg", "wb")
            except OSError:
                file = open(
                    str(actualVideoPosition)
                    + " - "
                    + slugify(actualTitle)
                    + " by "
                    + slugify(actualChannelName)
                    + ".jpg",
                    "wb",
                )

            # Create Image
            thumbnail = requests.get(actualThumbnail)
            file.write(thumbnail.content)
            file.close()

            print(videoData)

            if actualVideoPosition == generalInformation:
                break

        except Exception as Error:
            print(
                "A error has occurred! continue with next video ... "
                + videoData
                + " this video could have a problem"
            )
            print(Error)
            continue

    try:
        pageToken = requestJSON["nextPageToken"]
        if pageToken != "":
            doRequest(elListo, pageToken)
    except:
        # print("Everything is done now!")
        if deletedVideos > 0:
            print(
                "Could not get "
                + str(deletedVideos)
                + " videos from playlist (private or deleted) \n"
            )
        else:
            print("All Videos got captured by this script successfully! :) \n")


def Work():
    if not os.path.exists("playlists"):
        os.mkdir("playlists")
    os.chdir("playlists")

    for playlist in allPlaylists:
        global deletedVideos
        deletedVideos = 0
        if playlist[1] not in os.listdir(os.getcwd()):
            os.mkdir(playlist[1])
            os.chdir(playlist[1])
            if currentDate not in os.listdir(os.getcwd()):
                os.mkdir(currentDate)
                os.chdir(currentDate)
            else:
                os.chdir(currentDate)
            checkForPrivacy(playlist[0])
        else:
            os.chdir(playlist[1])
            if currentDate not in os.listdir(os.getcwd()):
                os.mkdir(currentDate)
                os.chdir(currentDate)
            else:
                os.chdir(currentDate)
            checkForPrivacy(playlist)
        string = f"0 - There are {deletedVideos} deleted-private Videos"
        file = open(string, "w")
        file.close()
        os.chdir("../../")

    finale()


def finale():
    if not errorOccurred:
        print(
            "Everything went down just fine! :) Congratulations, no critical errors reported!"
        )
    else:
        print("It looks like there was some sort of problem while running this script!")
        print(
            "Please investigate further on your own or create your own issue on Github:"
        )
        print("https://github.com/DanielOberlechner/YoutubePlaylistVideoTitle/issues")


Work()

# ToDo find a better solution for the deletedVideos variable and if possible don't use global
