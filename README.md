# YoutubePlaylistVideoTitle
This Program is able to copy all video titles of multiple Youtube playlists. 
This is important because sometimes Youtube deletes videos or a user sets a video as private and so you can not see which video exactly is missing in your playlist.

This short script saves all video titles and Youtube channel uploader name from multiple playlists into a directory and creates another with the current date.

If a video from your playlist gets deleted you can use the created files to lookup which one it was and then search for the same video from a different uploader and add it again to your playlist.

## Requirements
First you'll need a Google Account and then go to https://console.developers.google.com/project and create a new project.
Then go to the API Keys section and create a new Youtube Data API v3 key. All of this is of course free.

Insert this key into the index.py and search for the 'apiKey' variable which is on the top of the script.
Then you need your playlist url which should be looking like the one below: <br />
https://www.youtube.com/watch?v=SlPhMPnQ58k&list=PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG

What is important is the string after 'list=', so in this case the pure playlist ID would be the following:
PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG

Lets make a clear example: <br />
You have two playlists: <br />
1x Music Playlist <br />
1x Random Playlist <br />

Now go to "Playlists Examples" in the index.py file. <br />
Create the following variables like this: <br />
```python
Music = ["Playlist_ID", "Music"]
Random = ["Playlist_ID", "Random"]

allPlaylists = [Music, Random]
```

Now you have chosen the directory name to be "Music" and "Random". <br />
Now you're able to run the script! :)

### Restrictions:
This Software needs Python3 to run and the Python module "requests". <br />

### Good to know!
#### Error messages

If a video is deleted in your playlist, it will be shown as "Index Number - Deleted Video".

If you have a public playlist for example from Youtube directly or for example from a friend you first have to save the playlist into your own account or else you can't download it. <br />

It would quit the script saying: <br />
`404 Playlist was not found`

#### Autostart script once a week (recommended)
I would recommend to run this script once a week. Why not more often?
In my case I use about 5 playlists with at least ~ 1000 videos in all playlists together in it. 
This script also downloads the thumbnail of each video so that it helps you recognize the videos content. 
I download those thumbnails in high resolution which is about ~ 100kb per video.
If you run this every day you waste a lot of space on your hard disk. 
On my system 7 runs of the script are around ~ 150 MByte on the hard disk.

##### macOS
On macOS you can create a launchctl service which will run this script automatically.
Cron wouldn't work because when your computer sleeps or is shut down the cron job misses the job and does **NOT** run the next time you start the computer.

I use homebrew to install newest python3 and pipenv:<br>
[Homebrew Website](https://brew.sh/)

```shell
brew install python3 pipenv
```

Then change into the scripts folder and run the following commands:
```shell
pipenv install
pipenv run index.py
```

Then the script should be running without any errors. If this step is successfull you can go on further.

Next is an example code for launchctl service I created for myself:
Create a file with the following name in this directory with
```shell
nano ~/Library/LaunchAgents/com.youtubetitlegetter.plist
```

and insert the following but don't forget to edit {userName} into your current username and also {pathToScriptLocation} to the location where the script is stored.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.youtubetitlegetter</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/pipenv</string>
        <string>run</string>
        <string>python3</string>
        <string>/Users/{userName}/{pathToScriptLocation}/YoutubePlaylistVideoTitle/index.py</string>
    </array> 
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>0</integer>
        <key>Minute</key>
        <integer>0</integer>
        <key>Weekday</key>
        <integer>1</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/{userName}/{pathToScriptLocation}/YoutubePlaylistVideoTitle/</string>
    <key>StandardOutPath</key>
    <string>/tmp/youtube-out.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/youtube-error.log</string>
</dict>
</plist>
```

To start and register the service you'll have to run the following commands:
```shell
id -u
```

This command id -u gives you a specific number directly linked to the current user account.
Use this number for the next 2 commands to work properly. <br>Insert this number in my case 501 into the following {number} => 501

```shell
launchctl bootstrap gui/{number} com.youtubetitlegetter.plist
launchctl kickstart -k gui/{number}/com.youtubetitlegetter
```

With the last command you kickstart the service. This means you trigger it to run once to check if everything is fine.
Let it run and look into the script directory under the playlist folder if there is a folder with current date and video titles in it.
If there is the script runs successfully. If there isn't you can go to /tmp/youtube-error.log to check what specific error the script has thrown.

##### Linux
On Linux you can use anacron or a similar command.

### Problems?
For questions or comments you can create an issue or reach me here: <br />
https://github.com/DanielOberlechner/YoutubePlaylistVideoTitle/issues <br />
https://twitter.com/danielthehok

Greets by 
Daniel Oberlechner! :)

Below you can see an example output: <br />
<img src="Example.png" alt="program output">
