from gi.repository import Gtk
from common import Window


class SpinnerWindow(Window):
    def post_init(self):
        spinner = Gtk.Spinner()
        spinner.start()
        self.add(spinner)

if __name__ == "__main__":
    SpinnerWindow()
    Gtk.main()
