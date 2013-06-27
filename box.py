from gi.repository import Gtk

from common import Window


class BoxWindow(Window):
    def post_init(self):
        box = Gtk.VBox()
        box.set_border_width(15)

        button1 = Gtk.Button("Button packed with expand and fill, "
                             "click to toggle_homogeneous")
        button1.connect('clicked', self.toggle_homogeneous, box)
        box.pack_start(button1, True, True, 0)

        button2 = Gtk.Button("Button packed with expand and no fill")
        button2.connect('clicked', self.show_foreach, box)
        box.pack_start(button2, True, False, 0)

        button3 = Gtk.Button("Button packed with no expand and fill")
        box.pack_start(button3, False, True, 0)

        button4 = Gtk.Button("Button packed with no expand and no fill")
        box.pack_start(button4, False, False, 0)

        self.add(box)

    def toggle_homogeneous(self, widget, box):
        box.set_homogeneous(not box.get_homogeneous())

    def show_foreach(self, widget, box):
        box.foreach(self.foreach_cb, None)

    def foreach_cb(self, widget, _data):
        print widget

if __name__ == "__main__":
    BoxWindow()
    Gtk.main()
