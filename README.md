# Post2Spotify
Searches Spotify for song information from text file and adds those songs to a selected playlist.


Prerequsites:

-Spotipy (https://github.com/plamere/spotipy): Cannot say enough good things about this project. Clear code and great documentation. Made this project relatively easy.

-Python 2.7 (I need to update this project to 3 at some point)



Setup:

1. Update config.ini with your Spotify API information and Spotify playlist id

  1.1 Spotify API Information: https://developer.spotify.com/my-applications/

  1.2 Spotify playlist id: In the Spotify web player, click the play list you want. The URL will be something like https://play.spotify.com/user/username/playlist/PLAYLIST_ID.

2. Add songs to the songoutput file. Intended method is using a web scraper in the following format "artist song_name" with one enttry per line.
