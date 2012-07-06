# Copyright (C) 2011, 2012 Brendan Le Foll <brendan@fridu.net>
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
import xbmcgui
import xbmcaddon
import sys

Addon = xbmcaddon.Addon(id='service.madeo.rs232server')
__language__ = Addon.getLocalizedString

#Dbus paths
RS232SERVER_BUS_NAME = 'uk.co.madeo.rs232server'
AZURSERVICE_OBJ_PATH = '/uk/co/madeo/rs232server/azur'
AZURSERVICE_IFACE = 'uk.co.madeo.rs232server.azur'
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

class DbusControl:
  def __init__(self):
    pass

  def connect(self):
    self.bus = dbus.SystemBus()
    self.amp = self.bus.get_object(RS232SERVER_BUS_NAME, AZURSERVICE_OBJ_PATH)
    self.iface = dbus.Interface(self.amp, AZURSERVICE_IFACE)

  def checkIface(self):
    try:
      iface.check()
      return True
    except:
      return False

  def getIface(self):
    if self.checkIface():
      return self.iface
    else:
      self.connect()
      return self.iface

class Caller:
  def __init__(self):
    #for notify mode 1
    self.NOTIFYDONE = False
    self.POWER = False
    self.control = DbusControl()

  def send_cmd(self, msg, repeat):
    self.control.getIface().send_cmd(msg, repeat, False)

  def poweron(self):
    try:
      self.send_cmd('poweron', 1)
      self.POWER = True
    except:
      self.connectionError()

  def poweroff(self):
    try:
      self.send_cmd('poweroff', 1)
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

while (not xbmc.abortRequested):
  # if xbmc is playing 
  if (xbmc.Player().isPlaying() == 1):
    IDLE = 0
    DIDPLAY = True
    lastcheck = time.time()
    #Application.Property.Name(volume)
    #Application.Property.Name(muted)
  # check play type
  if (xbmc.Player().isPlayingAudio()):
    music = True
    if (caller.powerStatus() is False):
      caller.poweron()
    if (video is True):
      caller.send_cmd('voldown', int(Addon.getSetting('voldiff')))
      video = False
  elif (xbmc.Player().isPlayingVideo()):
    video = True
    if (caller.powerStatus() is False):
      caller.poweron()
    if (music is True):
      caller.send_cmd('volup', int(Addon.getSetting('voldiff')))
      music = False
  #poweroff if hasn't played/idle for 120secs
  elif (xbmc.getGlobalIdleTime() > int(Addon.getSetting('timeout'))) and (caller.powerStatus() is True or FIRSTRUN is True):
    if (IDLE == 0) and (DIDPLAY is False):
      caller.poweroff()
      FIRSTRUN = False
      IDLE = 1
    elif(DIDPLAY == True) and ((time.time() - lastcheck) > int(Addon.getSetting('timeout'))):
      DIDPLAY = False;
  # small sleep
  xbmc.sleep(1000)
