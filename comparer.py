import os
import re
import sys

from datetime import datetime
from decouple import config

DEBUG = config("DEBUG", default=False, cast=bool)

firstPlaylistWithoutUploader = []
lastPlaylistWithoutUploader = []
playlistWithoutUploader = []

allPlaylists = os.listdir()
os.chdir("playlists")


# def videoRemoveIndexNumber(video):
#     subString = re.findall(r"\d+ - ", video)
#     return video.replace(subString, "")


def getVideoIndexNumber(var):
    return re.findall(r"\d+", var)


def removeVideoIndex(playlist):
    playlist.pop()
    return playlist


def removeUploader(playlist):
    for video in playlist:
        # print("video: ", video)
        # ToDo:
        # This regex could make problems with strange video titles I should redo this one
        subString = re.findall(r" by.*", video)
        # print("subString: ", subString)
        if subString:
            # print("subString is True")
            playlistWithoutUploader.append(video.replace(subString[0], ""))
            # print("This is the video title", video.replace(subString[0], ""))
            # playlistWithoutUploader.append(video)
        # print("subString:", type(subString[0]))
    #     video.replace(subString, "")
    #     playlistWithoutUploader.append(video)
    # return playlistWithoutUploader
    # print("playlistWithoutUploader: ", playlistWithoutUploader)


def doWork():
    # This below is necessary because macOS creates hidden DS_Store file which bugs around
    # ToDo Check if Windows fucks around as well with hidden files
    if ".DS_Store" in lista:
        lista.remove(".DS_Store")

    lista.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))

    cleanedFirstList = []
    cleanedLastList = []

    # print(lista[0])
    # print(lista[-1])

    # selects the first and last folder
    firstPlaylist = os.listdir(lista[0])
    lastPlaylist = os.listdir(lista[-1])

    def sortVideosNumerically(string):
        return list(map(int, getVideoIndexNumber(string)))[0]

    # This only works if videos are sorted from the beginning from show the oldest video first
    firstPlaylist.sort(key=sortVideosNumerically, reverse=True)
    lastPlaylist.sort(key=sortVideosNumerically, reverse=True)

    print(firstPlaylist[-1])
    print(lastPlaylist[-1])

    firstPlaylistDeletedVideos = getVideoIndexNumber(firstPlaylist[-1])
    lastPlaylistDeletedVideos = getVideoIndexNumber(lastPlaylist[-1])

    if firstPlaylistDeletedVideos == lastPlaylistDeletedVideos:
        print("No videos went missing ...")
    else:
        print("Videos are missing. Trying now to recover them")
        firstPlaylist = removeVideoIndex(firstPlaylist)
        lastPlaylist = removeVideoIndex(lastPlaylist)
        # print(firstPlaylist)
        # print(lastPlaylist)
        firstPlaylist.sort(key=sortVideosNumerically)
        lastPlaylist.sort(key=sortVideosNumerically)
        # print(firstPlaylist)
        # print(lastPlaylist)
        # remove Uploader and compare lists
        firstPlaylist = removeUploader(firstPlaylist)

        for subString in playlistWithoutUploader:
            videoFound = False
            for video in lastPlaylist:
                if subString in video:
                    # print("Video found: ", subString)
                    videoFound = True
                    break
            if not videoFound:
                print("this video is missing: ", subString)

            # if video in lastPlaylist:
            #     print("Video found")
            # else:
            #     print("Problem: Video wasn't found ...")

    # index[-1] from both lists, if index number is not the same, can recover deleted videos
    #    both lists remove list.index[-1]
    #    firstPlaylist[0].removeVideoIndexNumber find subString in lastPlaylist
    #    if found:
    #        print("all clear")
    #    else:
    #        print("not found THIS video")

    # indexVideosMissing = []

    # for video in lastPlaylist:
    #     if "- Deleted video.jpg" in video or "- Private video.jpg" in video:
    #         if DEBUG:
    #             print("This video got removed: ", video)
    #         videoNumber = re.findall(r"\d+\b", video)
    #         indexVideosMissing += videoNumber
    # print(videoNumber)
    # print(indexVideosMissing)

    # videoNumbersInt = [int(x) for x in indexVideosMissing]

    # for i in videoNumbersInt:
    #     vid = firstPlaylist[i]
    #     if "- Deleted video.jpg" in vid or "- Private video.jpg" in vid:
    #         print("Video " + str(i) + " could not be found in previous list")
    #         continue
    #     print("Found deleted Video ", vid)
    # print(type(indexVideosMissing[0]))


os.chdir("Nirvana")
lista = os.listdir()
doWork()

# ToDo Final state
# for playlist in lista:
#     os.chdir(playlist)
#     doWork()
#     os.chdir("..")
