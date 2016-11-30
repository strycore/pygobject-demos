import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from common import Window


class EditableGridWindow(Window):
    def post_init(self):
        self.model = [
            ('FOO', 'BAR'),
            ('BAZ', 'BANG'),
        ]
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.liststore = Gtk.ListStore(str, str)
        for item in self.model:
            self.liststore.append(list(item))

        self.treeview = Gtk.TreeView.new_with_model(self.liststore)
        for i, column_title in enumerate(["Key", "Value"]):
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", True)
            renderer.connect("edited", self.on_text_edited)

            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_resizable(True)
            self.treeview.append_column(column)

        self.buttons = list()
        for action in ["Add", "Delete"]:
            button = Gtk.Button(action)
            self.buttons.append(button)
            button.connect("clicked", self.on_action)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)

        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)
        self.scrollable_treelist.add(self.treeview)

    def on_action(self, widget):
        print("oh hai")

    def on_text_edited(self, widget, path, text):
        self.liststore[path][1] = text

if __name__ == "__main__":
    EditableGridWindow()

    GObject.threads_init()
    Gtk.main()
