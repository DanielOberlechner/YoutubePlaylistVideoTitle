# YoutubePlaylistVideoTitle - For Music Playlists
This Program copy's all video titles of a youtube playlist. 
This is important because sometimes youtube deletes music titles or a user sets a video as private and so you can not see which video exactly is missing in your playlist.

This short script saves all video names from a playlist into a file which has the current date as name into the directory in which the script is running.

If a video from your playlist gets deleted you can use the created file to lookup which one it was and then search for the same video from a different uploader and add it again to your music playlist.

## Requirements
First you'll need a Google Account and then go to https://console.developers.google.com/project and create a new project.
Then go to the API Keys section and create a new Youtube Data API v3 key. All of this is of course free.

Insert this key into the index.py and search for the 'apiKey' variable which is on the top of the script.
Then you need your playlist url which should be looking like the one below:
https://www.youtube.com/watch?v=SlPhMPnQ58k&list=PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG

What is important is the string after 'list=', so in this case the pure playlist ID would be the followning:
PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG

This string you have to insert into the index.py and there into playlistId variable.

### Restrictions:
This Software needs Python3 to run.

If the playlist contains deleted or private videos it will abort when it reaches such a video. 
It should throw an out of index error.

If a video from a playlist which isn't from your account you have to save the foreign playlist into your account.
When thats done you can now delete videos which aren't available anymore.

For questions or comments you can create a issue or reach me here:
https://twitter.com/danielthehok

Greets by 
Daniel Oberlechner


Feel free to copy, extend or write changes to this code.

Below you can see an example output:

<img src="Example.png">
