from gi.repository import Gtk, GdkPixbuf

IMAGE = 'data/firefox.jpg'


class Window(Gtk.Window):
    def __init__(self):
        super(Window, self).__init__()
        self.connect('destroy', self.quit)
        self.set_default_size(400, 400)
        self.post_init()
        self.show_all()

    def post_init(self):
        pass

    def quit(self, window):
        Gtk.main_quit()


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

        print dir(pixbuf_scaled.props)

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

if __name__ == "__main__":
    PixbufLoading()
    Gtk.main()
