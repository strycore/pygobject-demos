import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Pango
import utils
from common import Window

(
    COL_ID,
    COL_FILENAME,
    COL_IMAGE,
) = list(range(3))

SIZE = (256, 256)
ASSET_PATH = os.path.expanduser('~/.cache/media-art/')
LIMIT = 900


class FlowBoxWindow(Window):
    def post_init(self):
        scrolled_window = Gtk.ScrolledWindow()
        self.add(scrolled_window)

        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_homogeneous(False)
        scrolled_window.add(self.flowbox)
        self.data = []

    def after_init(self):
        self.get_items()
        loader = self._fill_store_generator(self.data)
        GLib.idle_add(loader.__next__)

    def _fill_store_generator(self, data, step=100):
        n = 0
        for item in data:
            self.add_item(item)
            n += 1
            if (n % step) == 0:
                yield True
        yield False

    def get_items(self):
        for index, filename in enumerate(os.listdir(ASSET_PATH)):
            if LIMIT and index > LIMIT:
                break
            item = (index, filename)
            self.data.append(item)

    def add_item(self, item):
        filename = item[1]
        image = utils.get_image_from_file(ASSET_PATH + filename, SIZE)
        if not image:
            return

        vbox = Gtk.VBox()
        vbox.add(image)
        text = filename[:40] + '\n' + filename[40:]
        label = Gtk.Label(text)
        label.set_property('wrap', True)
        label.set_max_width_chars(50)
        label.set_property('ellipsize', Pango.EllipsizeMode.END)
        label.set_selectable(True)
        vbox.add(label)
        vbox.show_all()
        self.flowbox.add(vbox)

if __name__ == "__main__":
    FlowBoxWindow()

    GObject.threads_init()
    Gtk.main()
