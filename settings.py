#%% CONFIGURATION PARAMETERS

# EDIT THESE WITH YOUR DETAILS
sc_username			= 'abc@xyz.com' # username to log into soundcloud
sc_password			= 'xxxxxxxxxxx' # password to log into soundcloud
sc_client_id		= 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # registered app client ID
sc_client_secret	= 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # registered app client secret

root_folder			= 'C:/path/to/PetitaDumdum/' # make sure ends with slash
download_folder		= root_folder + 'audio/' # where audio files will be downloaded to (make sure ends with slash)
maxmsp_patch_path	= root_folder + 'src/msaVocalHarmonizer.maxpat' # where the maxmsp patch is located


# DO NOT EDIT THESE UNLESS YOU HAVE GOOD REASON TO
src_user_url		= 'https://soundcloud.com/petita_tatata' # url of user to get source sounds from
my_user_url			= 'https://soundcloud.com/petita-dumdum' # url of my account

osc_target_ip		= '127.0.0.1' # where the maxmsp patch is running
osc_target_port		= 8000 # port that maxmsp is listening on (python is sending)
osc_listen_port		= 9000 # port that python is listening on (maxmsp is sending)

track_suffix 		= "_DUMDUM.wav" # the suffix added to processed files by maxmsp
