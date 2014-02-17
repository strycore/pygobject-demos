# Original code by Luca Bruno
# http://lethalman.blogspot.fr/2008/11/single-app-instances-python-and-dbus.html
import dbus
import dbus.bus
import dbus.service
import dbus.mainloop.glib
from gi.repository import Gtk, Gdk
import time

DBUS_NAME = "com.strycore.dbusdemo"


class DBusDaemon(dbus.service.Object):
    def __init__(self, bus, path, name):
        dbus.service.Object.__init__(self, bus, path, name)
        self.running = False
        self.main_window = Gtk.Window()
        self.main_window.connect('destroy', Gtk.main_quit)
        self.main_window.show_all()

    @dbus.service.method(DBUS_NAME, in_signature='', out_signature='b')
    def is_running(self):
        return self.running

    @dbus.service.method(DBUS_NAME, in_signature='a{sv}i', out_signature='')
    def start(self, options, timestamp):
        if self.is_running():
            self.main_window.present_with_time(timestamp)
        else:
            self.running = True
            Gtk.main()
            self.running = False

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
request = bus.request_name(DBUS_NAME, dbus.bus.NAME_FLAG_DO_NOT_QUEUE)
if request != dbus.bus.REQUEST_NAME_REPLY_EXISTS:
    app = DBusDaemon(bus, '/', DBUS_NAME)
else:
    obj = bus.get_object(DBUS_NAME, "/")
    app = dbus.Interface(obj, DBUS_NAME)

# Get your options from the command line, e.g. with OptionParser
options = {'option1': 'value1'}
app.start(options, int(time.time()))
if app.is_running():
    Gdk.notify_startup_complete()
