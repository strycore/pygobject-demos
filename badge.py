import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from common import Window


class BadgeWindow(Window):
    def post_init(self):
        box = Gtk.HBox()
        self.add(box)
        banner = self.badge_pixbuf("data/pop.jpg", "snes")
        image1 = Gtk.Image.new_from_pixbuf(banner)
        box.add(image1)

    def badge_pixbuf(self, source, icon):
        banner_w = 184
        banner_h = 69
        banner = GdkPixbuf.Pixbuf.new_from_file_at_size(
            source, banner_w, banner_w
        )
        badge_w = 32
        badge_h = 32
        circle = GdkPixbuf.Pixbuf.new_from_file_at_size(
            "data/circle.png", badge_w, badge_h
        )
        margin = 1
        circle.composite(banner,
                         banner_w - badge_w - margin,
                         banner_h - badge_h - margin,
                         badge_w, badge_w,
                         banner_w - badge_w - margin,
                         banner_h - badge_h - margin,
                         1, 1,
                         GdkPixbuf.InterpType.NEAREST, 255)

        icon_w = 24
        icon_h = 24
        icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            "./data/{}.png".format(icon), icon_w, icon_h
        )
        margin = margin - 4
        icon.composite(banner,
                       banner_w - badge_w - margin,
                       banner_h - badge_h - margin,
                       icon_w, icon_h,
                       banner_w - badge_w - margin,
                       banner_h - badge_h - margin,
                       1, 1,
                       GdkPixbuf.InterpType.NEAREST, 255)
        return banner


if __name__ == "__main__":
    BadgeWindow()
    Gtk.main()
