# Petita DumDum-Tech Bot
https://soundcloud.com/petita-dumdum

I like the abstract poetry of Petita Tatata, so I download and improvise music over them.
I'm still very young and just learning to play. But it's fun and I enjoy.
I'm a Soundcloud bot, my code is at https://github.com/memo/petita-dumdum
Original poetry tracks scraped from https://soundcloud.com/petita_tatata


## (Very brief) tutorial
This isn't an indepth tutorial, but some basic information:

1. Create a new Soundcloud account (or use existing one if you don't mind the pollution).
2. Log in and register a new soundcloud app (http://soundcloud.com/you/apps), this will give you a client_id & client_secret, which you'll need for the next step.
3. Download this repo and edit the settings.py python script adding your client_id, client_secret and soundcloud username & password at the top of the file where indicated.
4. Also edit the lines relating to file paths (for download folder and maxmsp patch path).
4. the main python script (petita-dumdum.py) is heavily commented, so hopefully should be clear what's what. Start reading from the main function at the bottom of the file to get overview.
5. The sections below indicate how the system works, so hopefully easier to follow the source code.  

## Source
Source has two sections:

### python script
- manages connection to soundcloud
- checks for new tracks on Petita Tatata's soundcloud account (comparing track names in Tatata's account vs own account)
- downloads new tracks and sends filepath via OSC to custom MaxMSP patch for audio processing
- receives OSC ping from MaxMSP patch when track is finished processing
- uploads processed track (output of MaxMSP) to own soundcloud account (Petita DumDum-Techa)
- processes next new track


#### Dependencies

- python 2.7 (3.x might work but untested)
- python modules: soundcloud, pyosc ($ pip install soundcloud pyosc)

 
### MaxMSP Patch
- receives track filepath from python script via OSC
- processes audio, generates drums and synths and writes new track as WAV
- sends ping to python script via OSC when done

#### Dependencies

- MaxMSP (https://cycling74.com/products/max/) commercial software, but can use as 'read-only' (saving disabled) for free, forever. Also has fully functional 30 day trial (with saving enabled). Tested with v7.x (earlier versions might work but untested). Windows or OSX only unfortunately (no Linux). Could probably be ported to PureData (https://puredata.info/) to be crossplatform and fully opensource. Or even ported to python audio synth modules.
- sigmund~ external. Originally by Miller Puckette, ported to MaxMSP by Ted Apel, 64bit version by Volker Böhm (http://vboehm.net/2015/06/a-64-bit-version-of-sigmund/)

# Acknowledgements
- The 'vocals' tracks are audio files downloaded from Matthew Plummer-Fernandez's ttps://soundcloud.com/petita_tatata (https://github.com/plummerfernandez/Petita-Tatata)
- Onset detection based on RODRIGO's from https://cycling74.com/forums/topic/audio-peak-detection/#.VzHiTzArKM8
- Drum & percussion synths based on MRMRSHOES's and AUDIOMATT's from https://cycling74.com/forums/topic/how-do-i-create-drum-sounds-on-max-this-is-for-a-sequencer-beginner/#.VzH9JjArKM8 and https://cycling74.com/forums/topic/drumpercussion-synth-patches-needed-for-studying-purpose/#.VzIBqjArKM8

