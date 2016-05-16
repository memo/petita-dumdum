# Manages connection to soundcloud, downloads tracks and uploads new ones.
# Communicates with MaxMSP patch via OSC
# More info at https://github.com/memo/petita-dumdum
#
# by Memo Akten, www.memo.tv
#
# TODO: Lots of error checking and robustness could be added
# e.g. to manage failures in comms, MaxMSP and/or OSC
#

import soundcloud
import urllib
import os
import OSC
import types
from time import sleep
from random import shuffle

# import our own config file
from settings import *

#%% GLOBALS
do_osc_loop = True


#%% connect to soundcloud
def connect_to_sc(sc_username, sc_password, sc_client_id, sc_client_secret):
    sc_client = soundcloud.Client(client_id = sc_client_id,
                               client_secret = sc_client_secret,
                               username = sc_username,
                               password = sc_password)
    print "Client credentials ok. Welcome " + sc_client.get('/me').username 
    return sc_client
    
    
    
#%% get any user's track list (by user URL, e.g. https://soundcloud.com/petita-dumdum )
def get_track_list(sc_client, user_url, limit=1000):
    user = sc_client.get('/resolve', url = user_url)
    print "Getting track list for user " + user.username + "...", 
    tracks = sc_client.get("/tracks", user_id = user.id, limit = limit)
    print str(len(tracks)) + " tracks"
    return tracks


        
#%% UTIL FUNCTIONS, not used in main process 
# make all given tracks downloadable or not        
def make_tracks_downloadable(sc_client, tracks, downloadable = 1):
    for track in tracks:
        print "Setting track '" + track.title + "' downloadable to " + str(downloadable)
        sc_client.put(track.uri, track={'downloadable':downloadable})
        
        
        
# update description for all my tracks from src_tracks
def update_track_descriptions(sc_client, my_tracks, src_tracks):
    # probably a more python way of doing this, but whatever
    for my_track in my_tracks: # iterate everything in my list
        print "Looking for track source: " + my_track.title, 
        found = False
        for src_track in src_tracks: # iterate everything in src list
            if(src_track.title == my_track.title): # compare names
                found = True
                descr = generate_track_description(src_track)
                print "...FOUND. Updating description"
                sc_client.put(my_track.uri, track={'description': descr})
                break
        if not found: # how come there's a track in my list that isn't in src?
            print "...NOT FOUND IN SOURCE: " + my_track.permalink_url
        
        
        
#%% find new tracks (by title) which are in src_tracks list but not in my_tracks list
# TODO: more 'python' way of doing it at:
# http://stackoverflow.com/questions/37191908/how-to-find-objects-which-are-in-a-list-but-not-in-another-list-comparing-by-p
def find_new_tracks(src_tracks, my_tracks):
    new_tracks = []
    for src_track in src_tracks: # iterate everything in src list
        found = False
        for my_track in my_tracks: # iterate everything in my list
            if(src_track.title == my_track.title): # compare names, break if true
                found = True
                break
        if not found: # add to new list if wasn't found
            new_tracks.append(src_track)
    print str(len(new_tracks)) + " new tracks found"
    return new_tracks


    
#%% download track from soundcloud
# provide unique track url 
def download_track_from_sc(sc_client, track_uri, download_folder):
    track = sc_client.get('/resolve', url=track_uri)
    print "Downloading track '" + track.title + " to " + download_folder
    download_path = ''
    if(track.downloadable):
        src_url = track.download_url + '?client_id=' + sc_client_id
        download_path = download_folder + track.title + ".mp3"
        urllib.urlretrieve(src_url, download_path)
    else:
        print "ERROR: Track is not downloadable"
    return track, download_path



#%% send path of track to maxmsp patch for processing
def send_track_to_maxmsp(osc_client, track_path):
    osc_msg = OSC.OSCMessage()
    osc_msg.setAddress("/openfile")
    osc_msg.append(track_path)
    osc_client.send(osc_msg)    
    print "Sending track " + track_path + " to MaxMSP " + str(osc_client.client_address)
    
    
    
#%% send ping to maxmsp patch to see if it's ready
def send_ping_to_maxmsp(osc_client):
    osc_msg = OSC.OSCMessage()
    osc_msg.setAddress("/ping")
    osc_msg.append(1)
    osc_client.send(osc_msg)    
    print "Sending ping to MaxMSP " + str(osc_client.client_address)



#%% osc callback for maxmsp ping
def osc_callback_maxmsp_finished(path, tags, args, source):
    global do_osc_loop
    do_osc_loop = False
    print "osc_callback_maxmsp_finished"
    


#%% post track to soundcloud
def post_track_to_sc(sc_client, filename, title, description = '', downloadable = 1):
    track = sc_client.post('/tracks', track={
        'title': title,
        'sharing': 'public', 
        'asset_data': open(filename, 'rb'),
        'downloadable':downloadable,
        'description':description
    })
    print "Track uploaded to " + track.permalink_url



#%% loop until osc message received from maxmsp
# TODO: add timeout
def wait_for_osc_ping(osc_server):
    global do_osc_loop
    do_osc_loop = True
    while do_osc_loop:
        osc_server.timed_out = False
        while not osc_server.timed_out:
            osc_server.handle_request()
        sleep(1)


        
#%% generate track description by getting relevant data from src       
def generate_track_description(src_track):
    d = u'Jam on ' + src_track.permalink_url
    d += u'\n-------\n'
    if src_track.description:
        d += src_track.description
    return d

    

#%% process track
# provide unique track url 
def process_track(osc_client, osc_server, sc_client, track_uri, download_folder, track_suffix):
    # clear waiting osc messages
    osc_server.timed_out = False
    while not osc_server.timed_out:
        osc_server.handle_request()
     
    # download track
    src_track, track_path = download_track_from_sc(sc_client, track_uri, download_folder)
    
    if src_track.downloadable:
        send_track_to_maxmsp(osc_client, track_path)
        
        # Wait till OSC ping comes indicating track is finished
        wait_for_osc_ping(osc_server)
    
        sleep(3) # well done, have a little break for a few seconds
            
            
        # post to sound cloud with same name and description as original
        title = src_track.title
        description = generate_track_description(src_track)
        new_track_path = track_path + track_suffix    
        print "Starting upload for track " + new_track_path
        post_track_to_sc(sc_client, new_track_path, title, description)
        
    
    
#%% for osc server timeout    
def handle_timeout(self):
    self.timed_out = True



#%% main
def main():
    # initialize OSC sender   
    print "Initializing OSC Sender"
    osc_client = OSC.OSCClient()
    osc_client.connect((osc_target_ip, osc_target_port))
    
    # initialize OSC Server (receiver)
    print "Initializing OSC Server (receiver)"
    osc_server = OSC.OSCServer((osc_target_ip, osc_listen_port))
    osc_server.addMsgHandler( "/finished", osc_callback_maxmsp_finished )
    osc_server.timeout = 0
    osc_server.handle_timeout = types.MethodType(handle_timeout, osc_server)
    
    # launch maxmsp patch
    print "Starting MaxMSP with " + maxmsp_patch_path
    os.startfile(maxmsp_patch_path) 
    
    # send ping to see when maxmsp patch is ready
    send_ping_to_maxmsp(osc_client)
    
    # wait till OSC ping comes back from maxmsp patch indicating it's ready
    wait_for_osc_ping(osc_server)

    # connect to soundcloud
    sc_client = connect_to_sc(sc_username, sc_password, sc_client_id, sc_client_secret)

    # get list of source tracks
    src_tracks = get_track_list(sc_client, src_user_url)
    
    # get list of my tracks
    my_tracks = get_track_list(sc_client, my_user_url)
    
    # find new tracks
    new_tracks = find_new_tracks(src_tracks, my_tracks)
    shuffle(new_tracks) # randomize order of new tracks (otherwise alphabetical)
    
    # process all new tracks
    for track in new_tracks:
        process_track(osc_client, osc_server, sc_client, track.uri, download_folder, track_suffix)
        sleep(3) # well done, have a little break for a few seconds
        
    # close OSC server
    print "Closing OSC Server"
    osc_server.close()


if __name__ == "__main__":
    main()
