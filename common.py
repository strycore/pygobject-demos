import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Window(Gtk.Window):
    width = 400
    height = 400

    def __init__(self):
        super(Window, self).__init__()
        self.connect('destroy', Gtk.main_quit)
        self.set_default_size(self.width, self.height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.post_init()
        self.show_all()

    def post_init(self):
        pass
