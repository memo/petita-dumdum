# Petita DumDum-Techa Bot

I'm a Soundcloud bot.
I like the abstract poetry of Petita Tatata, so I download and improvise music over them.
I upload my improvisations to https://soundcloud.com/petita-dumdum

I'm still very young and just learning to play. But it's fun and I enjoy.
Original poetry tracks scraped from https://soundcloud.com/petita_tatata


## (Very brief) tutorial
This isn't an indepth tutorial, but some basic information:

1. Create a new Soundcloud account (or use existing one if you don't mind the pollution).
2. Log in and register a new soundcloud app (http://soundcloud.com/you/apps), this will give you a *client_id* & *client_secret*, which you'll need for the next step.
3. Download this repo and edit the settings.py python script adding your *client_id*, *client_secret* and soundcloud *username* & *password* at the top of the file where indicated. Also edit the lines relating to file paths (for *download folder* and *maxmsp patch path*). [1]
4. the main python script (petita-dumdum.py) is heavily commented, so hopefully should be clear what's what. Start reading from the main function at the bottom of the file to get overview.
5. The sections below indicate how the system works, so hopefully makes it easier to follow the source code. [2]

[1] Alternatively, create a copy of *settings.py* and call it *mysettings.py* or *settings_myname.py* etc. Edit *that* file instead of the original settings.py. Then in petita-dumdum.py change the line *'from settings import \*'* to *'from mysettings import \*'* or *'from settings_myname.py import \*'* etc. This makes it easier to distribute the project without accidentally giving away your passwords (just don't distribute your own settings file but the template one).

[2] In the python code there are #%% comments. These create 'cells' which you can run individually. My current favourite python IDE is spyder (https://pythonhosted.org/spyder/ -  also comes with the Anaconda distro https://www.continuum.io/downloads), which provides a matlab like interactive IDE / playground. You can run individual 'cells' and then play in the interactive shell. A bit like ipython notebooks, but with an object inspector, watch, debugger, interactive shell and more. 

## Source
Source has two components:

### python script
- manages connection to soundcloud.
- checks for new tracks on Petita Tatata's soundcloud account (comparing track names in Tatata's account vs own account).
- downloads new tracks and sends to MaxMSP Patch for audio processing (sends filepath of downloaded tracks via OSC).
- receives OSC ping from MaxMSP patch when MaxMSP has finished processing the new track.
- uploads processed track (output of MaxMSP) to own soundcloud account (Petita DumDum-Techa).
- moves onto next new track


#### Dependencies

- python 2.7 (3.x might work but untested)
- python modules: soundcloud, pyosc ($ pip install soundcloud pyosc)

 
### MaxMSP Patch
- receives track filepath from python script via OSC.
- processes audio, generates drums and synths and writes new track as WAV.
- sends ping to python script via OSC when done.

#### Dependencies

- MaxMSP (https://cycling74.com/products/max/) commercial software, but can use as 'read-only' (saving disabled) for free, forever. Also has fully functional 30 day trial (with saving enabled). Tested with v7.x (earlier versions might work but untested). Windows or OSX only unfortunately (no Linux). Could probably be ported to PureData (https://puredata.info/) to be crossplatform and fully opensource. Or even ported to python audio synth modules.
- sigmund~ external. Originally by Miller Puckette, ported to MaxMSP by Ted Apel, 64bit version by Volker Böhm (http://vboehm.net/2015/06/a-64-bit-version-of-sigmund/)

# Acknowledgements
- The 'vocals' tracks are audio files downloaded from Matthew Plummer-Fernandez's https://soundcloud.com/petita_tatata (src at https://github.com/plummerfernandez/Petita-Tatata)
- MaxMSP onset detection based on RODRIGO's from https://cycling74.com/forums/topic/audio-peak-detection/#.VzHiTzArKM8
- MaxMSP drum & percussion synths based on MRMRSHOES's and AUDIOMATT's from https://cycling74.com/forums/topic/how-do-i-create-drum-sounds-on-max-this-is-for-a-sequencer-beginner/#.VzH9JjArKM8 and https://cycling74.com/forums/topic/drumpercussion-synth-patches-needed-for-studying-purpose/#.VzIBqjArKM8

