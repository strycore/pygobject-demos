import os
import stat
from gi.repository import Gtk, GdkPixbuf, Gdk
from common import Window


class SidebarTreeView(Gtk.TreeView):
    def __init__(self, path):
        self.model = Gtk.TreeStore(str, GdkPixbuf.Pixbuf, int, bool)
        self.dirwalk(path)

        super(SidebarTreeView, self).__init__(model=self.model)

        column = Gtk.TreeViewColumn("Files")
        column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        text_renderer = Gtk.CellRendererText()
        icon_renderer = Gtk.CellRendererPixbuf()
        icon_renderer.set_property('stock-size', 16)
        column.pack_start(icon_renderer, False)
        column.pack_start(text_renderer, True)
        column.add_attribute(text_renderer, "text", 0)
        column.add_attribute(icon_renderer, "pixbuf", 1)
        self.append_column(column)
        self.set_headers_visible(False)
        self.set_fixed_height_mode(True)

    def dirwalk(self, path, parent=None, depth=0):
        for f in sorted(os.listdir(path)):
            fullname = os.path.join(path, f)
            fdata = os.stat(fullname)
            is_folder = stat.S_ISDIR(fdata.st_mode)
            icon_theme = Gtk.IconTheme.get_default()
            img = icon_theme.load_icon("folder" if is_folder else "document",
                                       16, 0)
            li = self.model.append(parent, [f, img, fdata.st_size, is_folder])
            if is_folder:
                if depth < 1:
                    self.dirwalk(fullname, li, depth + 1)


class SidebarWindow(Window):
    def post_init(self):
        path = os.path.expanduser("~/Music")
        paned = Gtk.Paned()
        self.add(paned)
        b = Gtk.Button("bliblu")
        paned.add2(b)
        self.treeview = SidebarTreeView(path)

        self.sidebar_scrolled = Gtk.ScrolledWindow()
        self.sidebar_scrolled.add(self.treeview)

        paned.add1(self.sidebar_scrolled)
        paned.set_position(150)

        self.connect('key-press-event', self.on_keypress)

    def on_keypress(self, widget, event):
        if event.keyval == Gdk.KEY_F9:
            self.toggle_sidebar()

    def toggle_sidebar(self):
        if self.sidebar_scrolled.get_visible():
            self.sidebar_scrolled.hide()
        else:
            self.sidebar_scrolled.show()


if __name__ == "__main__":
    SidebarWindow()
    Gtk.main()
