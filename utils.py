from gi.repository import Gtk, GdkPixbuf, GLib


def get_pixbuf(filename, size):
    try:

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filename, size[0], size[1])
        return pixbuf
    except GLib.Error:
        print('Error getting image', filename)


def get_image_from_file(filename, size):
    pixbuf = get_pixbuf(filename, size)
    if pixbuf:
        return get_image_from_pixbuf(pixbuf)


def get_image_from_pixbuf(pixbuf):
    image = Gtk.Image()
    image.set_from_pixbuf(pixbuf)
    image.show()
    return image
