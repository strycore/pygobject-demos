import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GnomeDesktop', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GnomeDesktop
from common import Window


class DisplaysWindow(Window):
    def post_init(self):
        self._box = Gtk.VBox()

        self.screen = Gdk.Screen.get_default()
        self.screen.connect('size-changed', self.on_size_changed)
        self.screen.connect('monitors-changed', self.on_monitor_changed)
        self.rr_screen = GnomeDesktop.RRScreen.new(self.screen)

        self.populate_display_info()
        self.add(self._box)

    def populate_display_info(self):
        for child in self._box.get_children():
            child.destroy()
        n_monitors = self.screen.get_n_monitors()

        for i in range(n_monitors):
            plug_name = self.screen.get_monitor_plug_name(i)
            plug_name_label = Gtk.Label()
            plug_name_label.set_markup("<b>{}</b>".format(plug_name))
            self._box.add(plug_name_label)

            # FIXME this is incorrect, the id of the Gdk.Screen and the id of
            # RRScreen don't match (id 0 for RRScreen is the left most display
            # when id 0 of Gdk.Screen is the primary display)
            output = self.rr_screen.get_output_by_id(i)
            mode = output.get_current_mode()

            self._box.add(Gtk.Label("Is primary: {}".format(output.get_is_primary())))
            try:
                self._box.add(Gtk.Label("Current mode: {}x{}@{} (id:{}, tiled:{})".format(
                    mode.get_width(),
                    mode.get_height(),
                    mode.get_freq_f(),
                    mode.get_id(),
                    mode.get_is_tiled())
                ))
            except:
                pass
            self._box.add(Gtk.Label("{}mm x {}mm".format(self.screen.width_mm(), self.screen.height_mm())))
        self._box.show_all()

    def on_size_changed(self, screen):
        print("Size changed")
        self.populate_display_info()

    def on_monitor_changed(self, screen):
        print("Monitor changed")
        self.populate_display_info()

if __name__ == "__main__":
    DisplaysWindow()
    Gtk.main()
