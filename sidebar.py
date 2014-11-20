from gi.repository import Gtk
from common import Window


class SidebarWindow(Window):
    def post_init(self):
        paned = Gtk.Paned()
        self.add(paned)

if __name__ == "__main__":
    SidebarWindow()
    Gtk.main()
