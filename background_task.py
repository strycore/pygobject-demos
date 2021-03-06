# From : https://raw.github.com/gist/1132418/7ceda5465a8a148b085c8fe337b855771e88af29/async.py
import threading
import subprocess
import time

from gi.repository import Gtk, Gdk, GObject

from common import Window


class AsyncJob(threading.Thread):

    def __init__(self, monitor, callback):
        self.progress = 0
        self.callback = callback
        self.monitor = monitor
        super(AsyncJob, self).__init__()

    def run(self):
        while(self.progress < 100):
            self.progress += 1
            time.sleep(0.05)
            GObject.idle_add(self.monitor, self.progress)
        self.callback(self.progress, None)


def async_call(func, on_done, *args, **kwargs):
    """
    Starts a new thread that calls func and schedules on_done to be run (on the
    main thread) when GTK is not busy.

    func: the function to call asynchronously. No arguments are passed to it.
          func should not use any resources used by the main thread, at least
          not without locking.

    on_done: the function that is called when func completes. It is passed
             func's result as the first argument and whatever was thrown (if
             anything) as the second.  on_done is called on the main thread,
             so it can access resources on the main thread.
    """

    if not on_done:
        on_done = lambda r, e: None

    def do_call(*args, **kwargs):
        result = None
        error = None

        try:
            result = func(*args, **kwargs)
        except Exception, err:
            error = err

        GObject.idle_add(lambda: on_done(result, error))

    thread = threading.Thread(target=do_call, args=args, kwargs=kwargs)
    thread.start()


def async_function(on_done=None):
    """ A decorator that can be used on free functions so they will always be
    called asynchronously. The decorated function should not use any resources
    shared by the main thread.

    Example:
    @async_function(on_done = do_whatever_done)
    def do_whatever(look, at, all, the, pretty, args):
        # ...

    on_done: the function that is called when the decorated function completes.
             If omitted or set to None this will default to a no-op. This
             function will be called on the main thread.

             on_done is called with the decorated function's result
             and any raised exception.
    """

    def wrapper(f):
        def run(*args, **kwargs):
            async_call(lambda: f(*args, **kwargs), on_done)
        return run
    return wrapper


def async_method(on_done=None):
    """ A decorator that can be used on class methods so they will always be
    called asynchronously. The decorated function should not use any resources
    shared by the main thread.

    Example:
    @async_method(on_done=lambda self, result, error: self.on_whatever_done(result, error))
    def do_whatever(self, look, at, all, the, pretty, args):
        # ...

    on_done: the function that is called when the decorated function completes.
             If omitted or set to None this will default to a no-op. This
             function will be called on the main thread.

             on_done is called with the class instance used, the decorated
             function's result and any raised exception.
    """

    if not on_done:
        on_done = lambda s, r, e: None

    def wrapper(f):
        def run(self, *args, **kwargs):
            async_call(lambda: f(self, *args, **kwargs),
                       lambda r, e: on_done(self, r, e))
        return run
    return wrapper


def grep_directory(search_terms, with_errors=False):
    if with_errors:
        raise ValueError("Crashing")
    print "search for", search_terms
    start_time = time.time()
    directory = "/tmp"
    stdout, stderr = subprocess.Popen(
        ["grep", "-ri", search_terms, directory],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    return (time.time() - start_time, stdout)


class TaskWindow(Window):
    def post_init(self):
        self.set_default_size(400, 50)
        box = Gtk.HBox()
        box.set_border_width(15)
        self.launch_button = Gtk.Button("Launch")
        self.launch_button.connect("clicked", self.on_launch)
        box.pack_start(self.launch_button, False, False, 20)

        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_show_text(True)
        box.pack_start(self.progress_bar, True, False, 20)

        self.spinner = Gtk.Spinner()
        box.pack_start(self.spinner, False, False, 20)

        self.add(box)

    def on_launch(self, widget):
        self.spinner.start()
        self.launch_button.set_sensitive(False)
        job = AsyncJob(self.on_progress, self.on_finish)
        job.start()

    def on_finish(self, result, error):
        self.spinner.stop()
        self.launch_button.set_sensitive(True)
        print "result:", result
        print "error:", error

    def on_progress(self, progress):
        self.progress_bar.set_fraction(progress / 100.0)
        self.progress_bar.set_text("%d %%" % progress)

if __name__ == "__main__":
    TaskWindow()
    Gdk.threads_init()
    GObject.threads_init()
    Gtk.main()
