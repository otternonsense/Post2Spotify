'''
Pulls the current playlist from output file,
then searches for these tracks in Spotify. They are added to the playlist
in config.ini if they are available, and not already in the playlist.
After adding the tracks, the original output file is cleared of data.
'''

import os
import re
import requests
import spotipy
import spotipy.util as util
import ConfigParser

tracksavailable = 0
tracksnotavailable = 0
tracksduplicate = 0
prev_playlist = [] #track uris of playlist already on spotify
track_ids = [] #track uris we will add to the playlist

sp = spotipy.Spotify()

#import settings from config.ini
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

playlist_id = ConfigSectionMap("Playlist")['playlist_id']

username = ConfigSectionMap("SpotifyAPI")['username']
client_id = ConfigSectionMap("SpotifyAPI")['client_id']
client_secret = ConfigSectionMap("SpotifyAPI")['client_secret']
redirect_uri = ConfigSectionMap("SpotifyAPI")['redirect_uri']


scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

songs = []
songtitle = True #used to combine song titles and artist names in each element
n = 0


#read in track names and add to array
with open("songoutput", "r") as myfile:
  songs = myfile.readlines()

#creates list of tracks currently in playlist
def show_tracks(results):
  global prev_playlist
  for i, item in enumerate(tracks['items']):
      track = item['track']['uri']
      track = track.replace('spotify:track:', '')
      prev_playlist.append(track)
  #print prev_playlist
  print 'Which currently contains', len(prev_playlist), 'tracks \n'
  
  
#search spotify for each track, determining if it is available and if so, whether it is a duplicate
def searchspot():
  global tracksavailable
  global tracksnotavailable
  global tracksduplicate
  global track_ids
  global results
  global songs
  for name in songs:
      print("searching for " + name)
      results = sp.search(q=name, type='track')
      try: #check if song exists on spotify
        trackURI = results['tracks']['items'][0]['uri']
        trackURI = trackURI.replace('spotify:track:', '')
        if trackURI not in track_ids and trackURI not in prev_playlist:
          track_ids.append(trackURI)
          tracksavailable+=1
        else:
          print("**Duplicate track**\n")
          tracksduplicate+=1
      except IndexError:
        print("**Track not available**\n")
        tracksnotavailable+=1
  return
        

#authenticate in spotify
if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    
    #run through each playlist until we find the one we want. There is probably a much simpler way
    #to do this but I have not figured it out yet.
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']: #playlist is equal to the element position 0,1,2,3,etc
        if playlist['owner']['id'] == username and playlist['id'] == playlist_id:
              print 'Will be using the playlist titled', playlist['name']
              results = sp.user_playlist(username, playlist_id,
                  fields="tracks,next")
              tracks = results['tracks']
              show_tracks(tracks)
              while tracks['next']: #needed so it doesn't stop after first 100 tracks
                tracks = sp.next(tracks)
                show_tracks(tracks)
    
    #grab the artist and song names from the page, then send to search spotify function
    searchspot()
    
    while len(track_ids) > 99:
      first99 = []
      first99 = track_ids[0:98]
      results = sp.user_playlist_add_tracks(username, playlist_id, first99)
      del track_ids[0:98]
    if len(track_ids) > 0: #otherwise there will be an error if no tracks were passed to track_ids
      results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
      
else:
    print("Can't get token for", username)

print "\nOut of", (tracksavailable + tracksnotavailable + tracksduplicate), "tracks,", tracksavailable, "were available,", tracksnotavailable, "were not available, and", tracksduplicate, " were duplicates or already on the playlist.\n"

#clear contents of file
with open("songoutput", "w") as myfile:
  pass
