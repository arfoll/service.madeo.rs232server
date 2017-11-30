# KODI/XBMC service addon that allows rs232server to control from within XBMC/KODI in a semi automated matter

rs232server is a service addon and requires XBMC 11.x 'Eden'. Note this is only
tested on x86-64 KODI 15.x on Linux.  rs232server must be running before XBMC
starts with addon.

INSTALL
-------

Run the rs232_server.py in the background (needs to be started before xbmc
runs). Place in ~/.kodi/addons

KEYMAP
------

In order to have keyboard/remote control of rs232service from XBMC the
xbmcclient.py script can be used in conjunction with the keyboard.xml file.
Place the keyboard.xml in ~/.xbmc/userdata/keymaps/. Unless you run xbmc as
user brendan you will want to replace the path of xbmcclient.py in the
keymap.xml and make sure the keymap matches what you want to do.  Essentially
you can use xbmcclient.py to call any function as you would miniclient but from
the RunScript() call within xbmc.  All commands and rs232server plugins shold
work using this.

FUNCTIONALITY
-------------

On video/audio start amp will be poweredon.  On media type change (video ->
audio) or (audio -> video) volume will be modified. I like the play videos
louder than music.  On XBMC screensaver start (or blackout) and no media is
playing, amplifier will be turned off Audio only mode is a mode for TVs that
are controlling the audio (via spdif to the amp via HDMI). Usually when the TV
is off spdif is down (this can also affect HDMI only connections via an amp
when they are set up as pure repeaters - blame HDCP). This will turn the TV on
even if not needed (not watching video) and set it to energysaving maximum (at
least on My LG TV this seems to equal a panel off).
