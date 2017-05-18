import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Window(Gtk.Window):
    width = 400
    height = 400

    def __init__(self):
        super(Window, self).__init__()
        self.css_provider = Gtk.CssProvider.new()
        self.css_provider.load_from_path('styles.css')
        self.connect('destroy', Gtk.main_quit)
        self.set_default_size(self.width, self.height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.post_init()
        self.show_all()
        self.after_init()

        screen = self.props.screen
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def post_init(self):
        pass

    def after_init(self):
        pass
