# -*- coding: utf-8 -*-
# NOTICE: the playlist shall not contain deleted videos if so the program won't work correct

import requests
import json

apiKey = ""
playlistId = "PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj" # random 200 pop songs on youtube

part= "snippet"
maxResults = "50"
maxResultsNumber = int(maxResults)

def doRequest(pageToken):
    url = "https://www.googleapis.com/youtube/v3/playlistItems?key=" + apiKey + "&playlistId=" + playlistId + "&part=" + part + "&maxResults=" + maxResults + "&pageToken=" + pageToken
    result = requests.get(url)
    requestJSON = json.loads(result.content)

    allVideoCounter = requestJSON["pageInfo"]["totalResults"]

    for i in range(maxResultsNumber):
        actualVideo = requestJSON["items"][i]["snippet"]["position"]
        actualTitle = requestJSON["items"][i]["snippet"]["title"]

        print(str(actualVideo) + " - " + actualTitle)

        if actualVideo > allVideoCounter - 2:
            print('All Videos are displayed... exit program')
            return

    if 'nextPageToken' in requestJSON:
        doRequest(requestJSON["nextPageToken"])

doRequest("")
