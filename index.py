# -*- coding: utf-8 -*-

import requests
import json
import datetime
import shutil
import os
import glob

currentDate = datetime.datetime.now().strftime("%d %B %Y.txt")
apiKey = "AIzaSyCd3VTnZ6hwGHKpUz52dsV8lrthFU3pUKU"
playlistId = "PLuP1wAti74xC6WBir_ZnRQ0lMMNH9U0Hc" # random 200 pop songs on youtube
part = "snippet"
textFile = open(currentDate, "w")
directory = "thumbnails"

def doRequest(pageToken):
    url = (
            "https://www.googleapis.com/youtube/v3/playlistItems?key="
            + apiKey
            + "&playlistId="
            + playlistId
            + "&part="
            + part
            + "&maxResults=50"
            + "&pageToken="
            + pageToken
    )

    result = requests.get(url)
    requestJSON = json.loads(result.content)
    token = ""
    allVideoCounter = requestJSON["pageInfo"]["totalResults"]

    if "nextPageToken" in requestJSON:
        token = requestJSON["nextPageToken"]

    for i in range(50):
        try:
            actualVideo = requestJSON["items"][i]["snippet"]["position"]
            actualTitle = requestJSON["items"][i]["snippet"]["title"]
            actualImage = requestJSON["items"][i]["snippet"]["thumbnails"]["default"]["url"]

            image = requests.get(actualImage)
            filer = open(str(actualVideo) + ".jpg", "wb")
            filer.write(image.content)
            filer.close()

            videoData = str(actualVideo) + " - " + actualTitle + "\n"
            print(videoData)
            textFile.write(videoData)

            if actualVideo == allVideoCounter - 1:
                print("All Videos successfully displayed... Exit program")
                break

        except:
            print("A error has occured! continue with next video ... " + videoData + " this video could have a problem")
            continue

    if token != "":
        doRequest(token)

doRequest("")

textFile.close()

try:
    os.mkdir(directory)
    source = "*.jpg"
    destination = directory
    for elfile in glob.glob(r'*.jpg'):
        shutil.move(elfile, destination)

except:
    print("could not create directory or move the images ...")