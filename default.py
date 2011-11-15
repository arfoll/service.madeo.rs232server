# Copyright (C) 2011 Brendan Le Foll <brendan@fridu.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gobject
gobject.threads_init()
from dbus import glib
glib.init_threads()
import dbus
import time
import xbmc

AMPSERVER_BUS_NAME = 'uk.co.madeo.ampserver'
AMPSERVER_BUS_PATH = '/uk/co/madeo/ampserver'

bus = dbus.SystemBus()
amp = bus.get_object(AMPSERVER_BUS_NAME, AMPSERVER_BUS_PATH)
iface = dbus.Interface(amp, AMPSERVER_BUS_NAME)

music = False
video = False
power = False

#two minutes
IDLETIME = 120
#to avoid xbmc start with ampon but never switching off 
#because power is wrong
FIRSTRUN = False
#in order to not stop playing as soon as video/playlist ends
IDLE = 0
DIDPLAY = False

while (not xbmc.abortRequested):
  # if xbmc is playing 
  if (xbmc.Player().isPlaying() == 1):
    IDLE = 0
    DIDPLAY = True
    lastcheck = time.time()
  # check play type
  if (xbmc.Player().isPlayingAudio()):
    music = True
    if (power is False):
      iface.poweron()
      power = True
    if (video is True):
      iface.volumedown()
      video = False
  elif (xbmc.Player().isPlayingVideo()):
    video = True
    if (power is False):
      iface.poweron()
      power = True
    if (music is True):
      iface.volumeup()
      music = False
  #poweroff if hasn't played/idle for 120secs
  elif (xbmc.getGlobalIdleTime() > IDLETIME) and (power is True or FIRSTRUN is True):
    if (IDLE == 0) and (DIDPLAY is False):
      iface.poweroff()
      power = False
      FIRSTRUN = False
      IDLE = 1
    elif(DIDPLAY == True) and ((time.time() - lastcheck) > IDLETIME):
      DIDPLAY = False;
  # small sleep
  xbmc.sleep(1000)
