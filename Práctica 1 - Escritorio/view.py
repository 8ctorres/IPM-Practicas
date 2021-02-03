# Main window view

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gettext

_ = gettext.gettext

class View:
    @classmethod
    def start(cls):
        Gtk.main()

    @classmethod
    def quit(cls, widget=None, event=None):
        Gtk.main_quit()

    def __init__(self):
        self.window = Gtk.Window(title=_("Xazam"))

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.window.add(vbox)

        vbox.pack_start(Gtk.Box(), expand=False, fill=False, padding=4)
        self.label1 = Gtk.Label(_("Seleccionar intervalo:"))
        vbox.pack_start(self.label1, expand=True, fill=False, padding=5)  # Child of VBOX

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # Dropdown list

        drop_list = Gtk.ListStore(str)
        drop_list.append([_("Segunda menor (2m)")])
        drop_list.append([_("Segunda mayor (2M)")])
        drop_list.append([_("Tercera menor (3m)")])
        drop_list.append([_("Tercera mayor (3M)")])
        drop_list.append([_("Cuarta justa (4j)")])
        drop_list.append([_("Cuarta aumentada (4aum)")])
        drop_list.append([_("Quinta justa (5j)")])
        drop_list.append([_("Sexta menor (6m)")])
        drop_list.append([_("Sexta mayor (6M)")])
        drop_list.append([_("Séptima menor (7m)")])
        drop_list.append([_("Séptima mayor (7M)")])
        drop_list.append([_("Octava (8a)")])

        self.dropdown_menu = Gtk.ComboBox.new_with_model(drop_list)
        text_renderer = Gtk.CellRendererText()
        self.dropdown_menu.pack_start(text_renderer, expand=True)
        self.dropdown_menu.add_attribute(text_renderer, "text", 0)

        # Radio Buttons

        self.asc_radiobutton = Gtk.RadioButton.new_with_label(None, "Asc")
        self.des_radiobutton = Gtk.RadioButton.new_with_label_from_widget(self.asc_radiobutton, "Des")

        radiobuttons_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        radiobuttons_box.pack_start(self.asc_radiobutton, expand=False, fill=False, padding=3)
        radiobuttons_box.pack_start(self.des_radiobutton, expand=False, fill=False, padding=3)

        hbox.pack_start(Gtk.Box(), expand=False, fill=False, padding=2)

        hbox.pack_start(self.dropdown_menu, expand=True, fill=True, padding=10)

        hbox.pack_start(radiobuttons_box, expand=False, fill=False, padding=5)

        self.button_buscar = Gtk.Button(label=_("Buscar"))
        hbox.pack_start(self.button_buscar, expand=False, fill=False, padding=10)

        hbox.pack_start(Gtk.Box(), expand=False, fill=False, padding=2)

        vbox.pack_start(hbox, expand=True, fill=False, padding=5)

        vbox.pack_start(Gtk.Box(), expand=False, fill=False, padding=10)

        self.reset_view()  # The view is built with the default values

    def show_all(self):
        self.window.show_all()

    def show_error(self, error_message):
        dialog = Gtk.MessageDialog(parent=self.window,
                                   message_type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.CLOSE,
                                   text=error_message)
        dialog.run()
        dialog.destroy()
        self.reset_view()

    def hide(self):
        self.window.hide()

    def destroy(self):
        self.window.destroy()

    def update_view(self, **kwargs):
        for key, value in kwargs.items():
            if key == "interval":
                self.dropdown_menu.set_active(value)
            elif key == "ascdes":
                if value:
                    self.asc_radiobutton.set_active(True)
                    self.des_radiobutton.set_active(False)
                else:
                    self.asc_radiobutton.set_active(False)
                    self.des_radiobutton.set_active(True)
            elif key == "buscar_active":
                self.button_buscar.set_sensitive(value)
            else:
                raise ValueError(f"Unexpected argument in view.updateview {key},{value}")

    def reset_view(self):
        self.button_buscar.set_sensitive(False)
        self.dropdown_menu.set_active(-1)
        self.asc_radiobutton.set_active(True)
        self.des_radiobutton.set_active(False)

    def connect_buscar_clicked(self, handler):
        self.button_buscar.connect('clicked', handler)

    def connect_interval_changed(self, handler):
        self.dropdown_menu.connect('changed', handler)

    def connect_ascdes_changed(self, handler):
        self.asc_radiobutton.connect('toggled', handler)
        self.des_radiobutton.connect('toggled', handler)

    def connect_delete_event(self, handler):
        self.window.connect('delete-event', handler)
