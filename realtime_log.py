#!/usr/bin/env python3
import os
from gi.repository import GLib
from gi.repository import Gtk


if __name__ == "__main__":

    class RealTimeLogWindow(Gtk.Window):
        def __init__(self):
            Gtk.Window.__init__(self, title="Example")

            box = Gtk.VBox()
            self.add(box)

            self.buffer = Gtk.TextBuffer()
            self.buffer.create_tag("warning", foreground="red")

            self.text_view = Gtk.TextView.new_with_buffer(self.buffer)
            self.text_view.connect("size-allocate", self.autoscroll)

            scrolledwindow = Gtk.ScrolledWindow(hexpand=True, vexpand=True,
                                                child=self.text_view)
            box.pack_start(scrolledwindow, False, True, 6)

            self.command = ['/bin/grep', '-r', 'nameserver', '/etc']

            self.button = Gtk.Button("Run '%s'" % ' '.join(self.command))
            self.button.connect("clicked", self.on_button_clicked)
            box.pack_start(self.button, False, True, 6)

            self.spinner = Gtk.Spinner()
            box.pack_start(self.spinner, False, True, 6)

        def run(self, cmd):
            #r = GLib.spawn_async(cmd, flags=GLib.SPAWN_DO_NOT_REAP_CHILD,
            #                     standard_output=True, standard_error=True)
            #self.pid, idin, idout, iderr = r
            fout = os.fdopen(idout, "r")
            ferr = os.fdopen(iderr, "r")

            #GLib.child_watch_add(self.pid, self.on_process_done)
            GLib.io_add_watch(fout, GLib.IO_IN, self.on_stdout_data)
            GLib.io_add_watch(ferr, GLib.IO_IN, self.on_stderr_data)
            #return self.pid

        def on_button_clicked(self, sender):
            self.spinner.start()
            self.button.set_sensitive(False)

            pid = self.run(self.command)
            #print("Started as process #", pid)

        def on_process_done(self, pid, exit_code):
            self.spinner.stop()
            self.button.set_sensitive(True)
            self.buffer.insert(self.buffer.get_end_iter(), "Done. exit code: %s\n" % exit_code, -1)

        def on_stdout_data(self, fobj, cond):
            if cond == GLib.IO_IN:
                line = fobj.readline()
                self.buffer.insert(self.buffer.get_end_iter(), line, -1)
            return True

        def on_stderr_data(self, fobj, cond):
            if cond == GLib.IO_IN:
                line = fobj.readline()
                self.buffer.insert_with_tags_by_name(self.buffer.get_end_iter(), line, "warning")
            return True

        def autoscroll(self, *args):
            adj = self.text_view.get_vadjustment()
            adj.set_value(adj.get_upper() - adj.get_page_size())

    win = RealTimeLogWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
