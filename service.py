# Copyright (C) 2012,2013 Brendan Le Foll <brendan@fridu.net>
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

RS232SERVER_BUS_NAME = 'uk.co.madeo.rs232server'
RS232SERVER_PATH = '/uk/co/madeo/rs232server/'
MAX_RETRIES = 2

# The Service tries to wrap an rs232server service In order to make the
# programming simpler there are only ever 2 expected objects, a tv and amp
# service.  Either of these services can be started with the name "disabled"
# which will create a service that always replies on and behaves perfectly
# happily but does nothing.

class Service:
  connected = False
  power = False
  retries = 0

  def __init__(self, name):
    self.name = name
    if name is "disabled":
      power = True

  def getStatus(self):
    return connected

  def getPower(self):
    return self.power

  def sendCmd(self, msg, repeat=1):
    if name is "disabled":
      return
    if not self.connected:
      self.connect()
    try:
      self.iface.send_cmd(msg, repeat, False)
      self.retries = 0
      if msg is "poweron" or "enermin":
        self.power = True
      elif msg is "poweroff" or "enerscreenoff":
        self.power = False
    except DBusException:
      self.connect()
      if self.retries < MAX_RETRIES:
        self.retries = self.retries + 1
        self.sendCmd(msg, repeat)
      else:
        xbmc.log("dbus object seems to have gone stale", level=xbmc.LOGSEVERE)

  def connect(self):
    try:
      self.bus = dbus.SystemBus()
      self.obj = self.bus.get_object(RS232SERVER_BUS_NAME, str(RS232SERVER_PATH) + self.name)
      self.iface = dbus.Interface(self.amp_obj, str(RS232SERVER_BUS_NAME) + '.' + self.name)
      xbmc.log("Service " + name + " is connecting", level=xbmc.NOTICE)
      connected = True
    except:
      xbmc.log("Service " + name + " has failed to connect", level=xbmc.LOGSEVERE)
      connected = False
