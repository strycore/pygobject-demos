from gi.repository import Gtk, GdkPixbuf
from common import Window

IMAGE = 'data/firefox.jpg'


class PixbufLoading(Window):
    def post_init(self):
        box = Gtk.Box()

        pixbuf_orig = GdkPixbuf.Pixbuf.new_from_file(IMAGE)
        image_orig = Gtk.Image.new_from_pixbuf(pixbuf_orig)
        box.add(image_orig)

        pixbuf_sized = GdkPixbuf.Pixbuf.new_from_file_at_size(IMAGE, 400, 50)
        image_sized = Gtk.Image.new_from_pixbuf(pixbuf_sized)
        box.add(image_sized)

        pixbuf_scaled = GdkPixbuf.Pixbuf.new_from_file_at_scale(IMAGE, 400, 50, False)
        image_scaled = Gtk.Image.new_from_pixbuf(pixbuf_scaled)
        box.add(image_scaled)

        self.add(box)


class SaturateDemo(Window):
    def post_init(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            "data/firefox.jpg", 120, 120
        )
        desaturated = pixbuf.copy()
        pixbuf.saturate_and_pixelate(desaturated, 0, True)
        image = Gtk.Image.new_from_pixbuf(desaturated)
        self.add(image)


class DrawEvent(Window):
    def post_init(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            "data/firefox.jpg", 120, 120
        )
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        image.connect('draw', self.on_draw)
        self.add(image)

    def on_draw(self, image, cairo_context):
        print "Drawing image"


if __name__ == "__main__":
    DrawEvent()
    Gtk.main()
