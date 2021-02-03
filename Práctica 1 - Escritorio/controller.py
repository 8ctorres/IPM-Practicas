# Controller of the Xazam App

import model
import view
import viewresults
from gi.repository import GLib
import threading
import gettext

_ = gettext.gettext

class Controller:
    def __init__(self, server_address="localhost", server_port="5000"):
        self.view = view.View()
        self.model = model.Model(server_address, server_port)
        self.results = None
        self.selected_interval_index = -1
        self.selected_is_asc = True

        self.view.connect_delete_event(self.view.quit)
        self.view.connect_buscar_clicked(self.on_buscar_clicked)
        self.view.connect_interval_changed(self.on_interval_changed)
        self.view.connect_ascdes_changed(self.on_ascdes_changed)

    def start(self):
        self.view.show_all()
        self.view.start()

    def on_interval_changed(self, widget=None):
        self.selected_interval_index = self.view.dropdown_menu.get_active()
        self.view.update_view(buscar_active=(self.selected_interval_index > -1))

    def on_ascdes_changed(self, widget=None):
        self.selected_is_asc = self.view.asc_radiobutton.get_active()
        self.view.update_view(buscar_active=(self.selected_interval_index > -1))

    def on_buscar_clicked(self, widget=None):
        example = self.model.get_example(self.selected_interval_index, self.selected_is_asc)
        threading.Thread(target=self._async_get_songs, name="Server petition Thread",
                        args=(self.selected_interval_index, self.selected_is_asc), daemon=True).start()
        self.results = viewresults.ViewResults(self.selected_interval_index, self.selected_is_asc, example)
        self.results.connect_volver_clicked(self.on_volver_clicked)
        self.results.connect_delete_event(self.on_volver_clicked)
        self.view.hide()
        self.results.show_waiting()

    def _async_get_songs(self, interval_index, is_asc):
        try:
            import time
            time.sleep(1)  # Waits so the user can see that the app shows a loading screen
            song_list = self.model.get_songs(interval_index, is_asc)
            GLib.idle_add(self._async_set_songs, song_list)
        except IOError:
            GLib.idle_add(self._async_handle_server_error)

    def _async_set_songs(self, song_list):
        # TODO: Preguntar acerca del posible riesgo de concurrencia al acceder a self.results para comprobar si es None
        if self.results is not None:  # If it is None, it means the user cancelled the operation
            self.results.update_song_list(song_list)
            self.results.show_songs()

    def _async_handle_server_error(self):
        self.on_volver_clicked()
        self.view.show_error(_("Ha ocurrido un error en el servidor"))

    def on_view_delete_event(self, widget=None, event=None):
        self.view.quit(widget, event)

    def on_volver_clicked(self, widget=None, event=None):
        self.results.destroy()
        self.results = None
        self.view.reset_view()
        self.view.show_all()
