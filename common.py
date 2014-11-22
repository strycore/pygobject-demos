from gi.repository import Gtk


class Window(Gtk.Window):
    def __init__(self):
        super(Window, self).__init__()
        self.connect('destroy', Gtk.main_quit)
        self.set_default_size(400, 400)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.post_init()
        self.show_all()

    def post_init(self):
        pass
