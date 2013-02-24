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

#Dbus paths
RS232SERVER_BUS_NAME = 'uk.co.madeo.rs232server'
RS232SERVER_PATH = '/uk/co/madeo/rs232server/'
AZURSERVICE_OBJ_PATH = str(RS232SERVER_PATH) + 'azur'
AZURSERVICE_IFACE = str(RS232SERVER_BUS_NAME) + '.azur'
LGTVSERVICE_OBJ_PATH = str(RS232SERVER_PATH) + 'lgtv'
LGTVSERVICE_IFACE = str(RS232SERVER_BUS_NAME) + '.lgtv'

class DbusControl:
  def __init__(self):
    self.bus = dbus.SystemBus()
    self.azur_stat = False
    self.lgtv_stat = False

  def startAzur(self):
    try:
      # Amp connection
      self.amp_obj = self.bus.get_object(RS232SERVER_BUS_NAME, AZURSERVICE_OBJ_PATH)
      self.amp_iface = dbus.Interface(self.amp_obj, AZURSERVICE_IFACE)
      self.azur_stat = True
    except:
      pass
    return self.azur_stat

  def startLgtv(self):
    try:
      # Lgtv connection
      self.lgtv_obj = self.bus.get_object(RS232SERVER_BUS_NAME, LGTVSERVICE_OBJ_PATH)
      self.lgtv_iface = dbus.Interface(self.lgtv_obj, LGTVSERVICE_IFACE)
      self.lgtv_stat = True
    except:
      pass
    return self.lgtv_stat

  def getAmpIface(self):
    if not self.azur_stat:
      self.startAzur()
    return self.amp_iface

  def getLgtvIface(self):
    if not self.lgtv_stat:
      self.startLgtv()
    return self.lgtv_iface

