# -*- coding: utf-8 -*-
# NOTICE: the playlist shall not contain deleted videos if so the program won't work correct - throw's a out of index error

import requests
import json
import datetime
import shutil

currentDate = datetime.datetime.now().strftime("%d %B %Y.txt")
apiKey = "AIzaSyCd3VTnZ6hwGHKpUz52dsV8lrthFU3pUKU"
playlistId = "PLuP1wAti74xC6WBir_ZnRQ0lMMNH9U0Hc" # random 200 pop songs on youtube

file = open(currentDate, "w")
part = "snippet"

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
    print(requestJSON)
    for i in range(50):
        try:
            actualVideo = requestJSON["items"][i]["snippet"]["position"]
            actualTitle = requestJSON["items"][i]["snippet"]["title"]
            actualImage = requestJSON["items"][i]["snippet"]["thumbnails"]["default"]["url"]

            image = requests.get(actualImage, stream=True)
            with open(actualVideo + ".jpg", "wb") as out_file:
                shutil.copyfileobj(image.raw, out_file)
            del actualImage

            videoData = str(actualVideo) + " - " + actualTitle + "\n"

            print(videoData)
            file.write(videoData)

            if actualVideo == allVideoCounter - 1:
                print("All Videos successfully displayed... Exit program")
                break
                exit(0)
        except:
            print('A error has occured! continue with next video ...')
            continue
    if token != "":
        doRequest(token)


doRequest("")
