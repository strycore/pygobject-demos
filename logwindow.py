from gi.repository import Gtk, Gdk, Pango
from common import Window


class LabelWindow(Window):
    def post_init(self):
        self.grid = Gtk.Grid()
        self.add(self.grid)
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 0, 1, 1)

        bg_color = Gdk.RGBA()
        bg_color.parse('rgb(47,47,47)')
        fg_color = Gdk.RGBA()
        fg_color.parse('rgb(255,199,116)')
        font_description = Pango.FontDescription('Monospace 11')

        self.textview = Gtk.TextView()
        self.textview.override_color(Gtk.StateFlags.NORMAL, fg_color)
        self.textview.override_color(Gtk.StateFlags.SELECTED, bg_color)
        self.textview.override_background_color(Gtk.StateFlags.NORMAL, bg_color)
        self.textview.override_background_color(Gtk.StateFlags.SELECTED, fg_color)
        self.textview.set_left_margin(10)
        self.textview.set_editable(False)
        self.textview.override_font(font_description)

        self.textbuffer = self.textview.get_buffer()
        with open('/var/log/Xorg.0.log', 'r') as log_file:
            log_content = log_file.read()
        self.textbuffer.set_text(log_content)
        scrolledwindow.add(self.textview)


if __name__ == "__main__":
    LabelWindow()
    Gtk.main()
