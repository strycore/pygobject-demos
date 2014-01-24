from gi.repository import Gtk
from common import Window


class LabelWindow(Window):
    def post_init(self):
        label = Gtk.Label()
        label.set_markup("Test <a href='http://strycore.com'>link</a>")
        self.add(label)


if __name__ == "__main__":
    LabelWindow()
    Gtk.main()
