import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from common import Window


class EditableGridWindow(Window):
    def post_init(self):
        self.model = dict(os.environ).items()[:4]
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        self.grid.set_margin_bottom(10)
        self.grid.set_margin_top(10)
        self.grid.set_margin_left(10)
        self.grid.set_margin_right(10)
        self.add(self.grid)

        self.liststore = Gtk.ListStore(str, str)
        for item in self.model:
            self.liststore.append(list(item))

        self.treeview = Gtk.TreeView.new_with_model(self.liststore)
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        for i, column_title in enumerate(["Key", "Value"]):
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", True)
            renderer.connect("edited", self.on_text_edited, i)

            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_resizable(True)
            column.set_min_width(200)
            column.set_sort_column_id(0)
            self.treeview.append_column(column)

        self.buttons = []
        self.add_button = Gtk.Button("Add")
        self.buttons.append(self.add_button)
        self.add_button.connect("clicked", self.on_add)

        self.delete_button = Gtk.Button("Delete")
        self.buttons.append(self.delete_button)
        self.delete_button.connect("clicked", self.on_delete)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.add(self.treeview)

        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 5)
        self.grid.attach(self.add_button, 8 - len(self.buttons), 6, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)

    def on_add(self, widget):
        self.liststore.append(["", ""])

    def on_delete(self, widget):
        selection = self.treeview.get_selection()
        liststore, iter = selection.get_selected()
        self.liststore.remove(iter)

    def on_text_edited(self, widget, path, text, field):
        self.liststore[path][field] = text


if __name__ == "__main__":
    EditableGridWindow()

    GObject.threads_init()
    Gtk.main()
