import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Pango
from common import Window


class Welcome(Gtk.EventBox):
    def __init__(self, title_text, subtitle_text):
        super().__init__()

        self.title_label = Gtk.Label(title_text)
        self.title_label.set_justify(Gtk.Justification.CENTER)
        self.title_label.set_hexpand(True)
        self.title_label.get_style_context().add_class("h1")

        self.subtitle_label = Gtk.Label(subtitle_text)
        self.subtitle_label.set_justify(Gtk.Justification.CENTER)
        self.subtitle_label.set_hexpand(True)
        self.subtitle_label.set_line_wrap(True)
        self.subtitle_label.set_line_wrap_mode(Pango.WrapMode.WORD)
        self.subtitle_label.get_style_context().add_class(Gtk.STYLE_CLASS_DIM_LABEL)
        self.subtitle_label.get_style_context().add_class("h2")

        content = Gtk.Grid()
        content.set_hexpand(True)
        content.set_vexpand(True)
        content.set_margin_top(12)
        content.set_valign(Gtk.Align.CENTER)
        content.set_orientation(Gtk.Orientation.VERTICAL)
        content.add(self.title_label)
        content.add(self.subtitle_label)

        self.add(content)


class WelcomeWindow(Window):

    def post_init(self):
        self.welcome = Welcome("Add Photos", "No photos were found in your library")
        self.add(self.welcome)


if __name__ == '__main__':
    WelcomeWindow()
    Gtk.main()
