from gi.repository import Gtk
from common import Window


class CheckBoxWindow(Window):
    def post_init(self):
        box = Gtk.Box()
        self.add(box)
        checkbox = Gtk.CheckButton(label="It's a _checkbox!",
                                   use_underline=True)
        checkbox.connect('clicked', self.default_callback)
        box.add(checkbox)
        inconsistent = Gtk.CheckButton(label="it's _inconsistent",
                                       use_underline=True)
        inconsistent.set_active(True)
        inconsistent.set_inconsistent(True)
        inconsistent.connect('clicked', self.reset_state)
        inconsistent.connect('clicked', self.default_callback)
        box.add(inconsistent)

    def default_callback(self, widget):
        print "Checkbox is", widget.get_active()

    def reset_state(self, widget):
        if widget.get_inconsistent():
            print "Resetting state"
            widget.set_inconsistent(False)

if __name__ == "__main__":
    CheckBoxWindow()
    Gtk.main()
