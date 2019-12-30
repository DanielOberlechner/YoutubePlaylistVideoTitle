# -*- coding: utf-8 -*-
# NOTICE: the playlist shall not contain deleted videos if so the program won't work correct - throw's a out of index error

import requests
import json
import datetime

currentDate = datetime.datetime.now().strftime("%d %B %Y.txt")
apiKey = ""
playlistId = "PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj" # random 200 pop songs on youtube

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

    allVideoCounter = requestJSON["pageInfo"]["totalResults"]

    for i in range(50):
        actualVideo = requestJSON["items"][i]["snippet"]["position"]
        actualTitle = requestJSON["items"][i]["snippet"]["title"]

        videoData = str(actualVideo) + " - " + actualTitle + "\n"

        print(videoData)
        file.write(videoData)

        if actualVideo == allVideoCounter - 1:
            print("All Videos are displayed... Exit program")
            exit(0)

    if "nextPageToken" in requestJSON:
        doRequest(requestJSON["nextPageToken"])


doRequest("")
