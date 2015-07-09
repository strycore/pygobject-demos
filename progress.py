# -*- coding: utf-8 -*-
from gi.repository import Gtk, GObject
from common import Window


class CheckBoxWindow(Window):
    width = 485
    height = 104

    def post_init(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_border_width(13)
        self.add(box)

        self.main_label = Gtk.Label(u"Checking for updates…")
        self.main_label.set_alignment(0, 0)
        box.pack_start(self.main_label, True, True, 0)

        progress_box = Gtk.Box()
        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_margin_bottom(10)
        self.progressbar.set_margin_right(10)

        progress_box.pack_start(self.progressbar, True, True, 0)

        self.cancel_button = Gtk.Button(stock=Gtk.STOCK_CANCEL)
        progress_box.add(self.cancel_button)

        box.pack_start(progress_box, False, False, 0)

        self.secondary_label = Gtk.Label()
        self.secondary_label.set_markup(
            u"<span size='10000'>Downloading http://ubuntu.com</span>"
        )
        self.secondary_label.set_alignment(0, 0)
        box.pack_start(self.secondary_label, True, True, 0)

        self.timeout_id = GObject.timeout_add(50, self.on_timeout, None)

    def on_timeout(self, user_data):
        self.progressbar.pulse()
        return True

if __name__ == "__main__":
    CheckBoxWindow()
    Gtk.main()
