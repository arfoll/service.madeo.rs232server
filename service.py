# Copyright (C) 2011-2021 Brendan Le Foll <brendan@fridu.net>
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

import sys
import time
import xbmc
import xbmcgui
import xbmcaddon

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

class Caller:
  def __init__(self):
    #for notify mode 1
    self.NOTIFYDONE = False
    self.POWER = False
    self.control = DbusControl()
    self.control.startAzur()
    self.control.startLgtv()

  def send_azur_cmd(self, msg, repeat):
    self.control.getAmpIface().send_cmd(msg, repeat, False)

  def send_lgtv_cmd(self, msg, repeat):
    #self.control.getLgtvIface().send_cmd(msg, repeat, False)
    pass

  def poweron(self, audioonly=False):
    try:
      self.send_azur_cmd('poweron', 1)
      self.send_lgtv_cmd('poweron', 1)
      if audioonly:
        # need to set enerscreenoff when tv is on
        self.send_lgtv_cmd('enerscreenoff', 1)
        self.POWER = 2
      else:
        self.POWER = True
    except:
      self.connectionError()

  def poweroff(self):
    try:
      self.send_azur_cmd('poweroff', 1)
      self.POWER = False
    except:
      self.connectionError()

  def errorMessage(self, phrase):
    dialog = xbmcgui.Dialog()
    dialog.ok(__language__(30101), phrase)

  def connectionError(self):
    if (bool(Addon.getSetting('notify'))) and (self.NOTIFYDONE is False):
      self.NOTIFYDONE = True
      self.errorMessage(__language__(30100))

  def powerStatus(self):
    return self.POWER


caller = Caller()
#xbmc.executeJSONRPC("{\"jsonrpc\": \"2.0\", \"method\": \"Application.SetVolume\", \"params\": { \"volume\": 100 }, \"id\": 1}")
player = xbmc.Player()
monitor = xbmc.Monitor()

while not monitor.abortRequested():
  # if xbmc is playing 
  if (player.isPlaying() == 1):
    IDLE = 0
    DIDPLAY = True
    lastcheck = time.time()
  # check play type
  if (player.isPlayingAudio()):
    music = True
    if (caller.powerStatus() is False):
      caller.poweron(not bool(Addon.getSetting('musicon')))
    if (video is True):
      caller.send_azur_cmd('voldown', int(Addon.getSetting('voldiff')))
      video = False
  elif (player.isPlayingVideo()):
    video = True
    if (caller.powerStatus() is False) or (caller.powerStatus() == 2):
      caller.poweron()
    if (music is True):
      caller.send_azur_cmd('volup', int(Addon.getSetting('voldiff')))
      caller.send_lgtv_cmd('poweron', 1)
      if (Addon.getSetting('muteonvid')):
        caller.send_lgtv_cmd('mute', 1)
      music = False
  #poweroff if hasn't played/idle for defined timeout
  elif (xbmc.getGlobalIdleTime() > int(Addon.getSetting('timeout'))) and (caller.powerStatus() is True or FIRSTRUN is True):
    if (IDLE == 0) and (DIDPLAY is False):
      caller.poweroff()
      FIRSTRUN = False
      IDLE = 1
    elif(DIDPLAY == True) and ((time.time() - lastcheck) > int(Addon.getSetting('timeout'))):
      DIDPLAY = False;
  # small sleep
  xbmc.sleep(1000)
