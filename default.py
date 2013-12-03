# Copyright (C) 2011, 2012, 2013 Brendan Le Foll <brendan@fridu.net>
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

import time
import xbmc
import xbmcgui
import xbmcaddon
import sys

from dbus_control import DbusControl

Addon = xbmcaddon.Addon(id='service.madeo.rs232server')
__language__ = Addon.getLocalizedString

#volume control variables
music = False
video = False
#to avoid xbmc start with ampon but never switching off 
#because power is wrong
FIRSTRUN = False
#in order to not stop playing as soon as video/playlist ends
IDLE = 0
DIDPLAY = False
NOTIFYDONE = False

services = {"amp": Service("azur"), "tv": Service("lgtv")}

def poweron(audioonly=False):
  services["amp"].sendCmd('poweron')
  if not audioonly:
    services["tv"].sendCmd('poweron')
  if audioonly and bool(Addon.getSetting('musicon')):
    services["tv"].sendCmd('poweron')
    # unknown callback is necesary to know tv on time
    #services["tv"].sendCmd('enerscreenoff')

def poweroff():
  self.services["amp"].sendCmd('poweroff')
  self.services["tv"].sendCmd('poweroff')

def powerStatus():
  return self.services["amp"].getPower() & self.services["tv"].getPower()

if bool(Addon.getSetting('maxvolume'):
  xbmc.executeJSONRPC("{\"jsonrpc\": \"2.0\", \"method\": \"Application.SetVolume\", \"params\": { \"volume\": 100 }, \"id\": 1}")

while (not xbmc.abortRequested):
  # if xbmc is playing 
  if (xbmc.Player().isPlaying() == 1):
    IDLE = 0
    DIDPLAY = True
    lastcheck = time.time()
  # check play type
  if (xbmc.Player().isPlayingAudio()):
    music = True
    if (powerStatus() is False):
      poweron(not bool(Addon.getSetting('musicon')))
    if (video is True):
      caller.send_azur_cmd('voldown', int(Addon.getSetting('voldiff')))
      video = False
  elif (xbmc.Player().isPlayingVideo()):
    video = True
    if powerStatus() is False:
      poweron()
    if (music is True):
      self.services["amp"].sendCmd('volup', int(Addon.getSetting('voldiff')))
      self.services["tv"].sendCmd('poweron')
      if (Addon.getSetting('muteonvid')):
        self.services["tv"].sendCmd('mute')
      music = False
  #poweroff if hasn't played/idle for defined timeout
  elif (xbmc.getGlobalIdleTime() > int(Addon.getSetting('timeout'))) and (caller.powerStatus() is True or FIRSTRUN is True):
    if (IDLE == 0) and (DIDPLAY is False):
      poweroff()
      FIRSTRUN = False
      IDLE = 1
    elif(DIDPLAY == True) and ((time.time() - lastcheck) > int(Addon.getSetting('timeout'))):
      DIDPLAY = False;
  xbmc.sleep(1000)
