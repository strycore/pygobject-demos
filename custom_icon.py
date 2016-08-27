import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from common import Window


class CustomIconWindow(Window):
    def post_init(self):
        self.button = Gtk.Button()
        self.set_image('./data/firefox.jpg')
        self.button.connect('clicked', self.on_button_clicked)
        box = Gtk.VBox()
        box.pack_start(self.button, True, False, 0)
        box2 = Gtk.HBox()
        box2.pack_start(box, True, False, 0)
        self.add(box2)

    def set_image(self, filename):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filename, 64, 64)

        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        self.button.set_image(image)

    def on_button_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.set_image(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        image_filter = Gtk.FileFilter()
        image_filter.set_name("Images")
        image_filter.add_pixbuf_formats()
        dialog.add_filter(image_filter)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

if __name__ == "__main__":
    CustomIconWindow()
    Gtk.main()
