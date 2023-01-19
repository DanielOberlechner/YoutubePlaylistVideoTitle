import os
import re
import sys

from datetime import datetime
from decouple import config

DEBUG = config("DEBUG", default=False, cast=bool)


allPlaylists = os.listdir()

os.chdir("playlists")


def videoRemoveIndexNumber(video):
    subString = re.findall(r"\d+ - ", video)
    return video.replace(subString, "")


def getVideoIndexNumber(var):
    return re.findall(r"\d+", var)


def removeVideoIndex(playlist):
    if playlist[0].getVideoIndexNumber == 0:
        playlist[0].remove()
    # Test if the two lines below do work for playlists which start with the highest number. Maybe this won't be even needed
    elif playlist[-1].getVideoIndexNumber == 0:
        playlist[-1].remove()
    else:
        print("Rare case: Could not found how many videos got deleted ...")
        sys.exit()
    return playlist



def compare(firstPlaylist, lastPlaylist):
    print(firstPlaylist)
    print(lastPlaylist)


def doWork():
    # This below is necessary because macOS creates hidden DS_Store file which bugs around
    # ToDo Check if Windows fucks around as well with hidden files
    if ".DS_Store" in lista:
        lista.remove(".DS_Store")

    lista.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))

    cleanedFirstList = []
    cleanedLastList = []

    print(lista[0])
    print(lista[-1])

    # selects the first and last folder
    firstPlaylist = os.listdir(lista[0])
    lastPlaylist = os.listdir(lista[-1])

    def sortVideosNumerically(string):
        return list(map(int, getVideoIndexNumber(string)))[0]

    # This only works if videos are sorted from the beginning from show the oldest video first
    firstPlaylist.sort(key=sortVideosNumerically)
    lastPlaylist.sort(key=sortVideosNumerically)

    print(firstPlaylist[0])
    print(lastPlaylist[0])

    firstPlaylistDeletedVideos = getVideoIndexNumber(firstPlaylist[0])
    lastPlaylistDeletedVideos = getVideoIndexNumber(lastPlaylist[0])

    print(firstPlaylistDeletedVideos[1])
    print(lastPlaylistDeletedVideos[1])

    if lastPlaylistDeletedVideos > firstPlaylistDeletedVideos:
        # prints only the two playlists including the index number and the 0. number of missing videos
        compare(firstPlaylist, lastPlaylist)
        firstPlaylist = removeVideoIndex(firstPlaylist)
        lastPlaylist = removeVideoIndex(lastPlaylist)
        # if first video of old playlist was found in the new playlist start the comparing
        for video in firstPlaylist:
            if video.
            # for vid in lastPlaylist:
            #     if video == vid:
            #         # GOTCHA, lists are now sync
            #         continue
            #     else:
            #         print(vid, " is missing")


    indexVideosMissing = []

    for video in lastPlaylist:
        if "- Deleted video.jpg" in video or "- Private video.jpg" in video:
            if DEBUG:
                print("This video got removed: ", video)
            videoNumber = re.findall(r"\d+\b", video)
            indexVideosMissing += videoNumber
            # print(videoNumber)

    # print(indexVideosMissing)
    videoNumbersInt = [int(x) for x in indexVideosMissing]
    if DEBUG:
        print(videoNumbersInt)

    # for i in videoNumbersInt:
    #     vid = firstPlaylist[i]
    #     if "- Deleted video.jpg" in vid or "- Private video.jpg" in vid:
    #         print("Video " + str(i) + " could not be found in previous list")
    #         continue
    #     print("Found deleted Video ", vid)
    # print(type(indexVideosMissing[0]))


os.chdir("Music")
lista = os.listdir()
doWork()

# ToDo Final state
# for playlist in lista:
#     os.chdir(playlist)
#     doWork()
#     os.chdir("..")
