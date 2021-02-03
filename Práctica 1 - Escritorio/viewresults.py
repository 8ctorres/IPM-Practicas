# Results window view

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gettext

_ = gettext.gettext


class ViewResults:
    def __init__(self, interval_index, is_asc, example):
        self.window = Gtk.Window(title=_("Xazam - Resultados"))

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.window.add(self.vbox)

        interval = self._interval_full_name(interval_index)
        if is_asc:
            direccion = _("ascendente")
        else:
            direccion = _("descendente")

        self.vbox.pack_start(Gtk.Box(), expand=False, fill=False, padding=6)  # Margen parte superior

        hboxlabel = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)  # Margins
        hboxlabel.pack_start(Gtk.Box(), expand=False, fill=False, padding=10)  # Margen izq
        self.label1 = Gtk.Label(_("Para el intervalo {} {}, un ejemplo sería:").format(interval, direccion))
        hboxlabel.pack_start(self.label1, expand=True, fill=False, padding=0)
        hboxlabel.pack_start(Gtk.Box(), expand=False, fill=False, padding=10)  # Margen derecho
        self.vbox.pack_start(hboxlabel, expand=True, fill=False, padding=10)

        self.label_ejemplo = Gtk.Label(example)
        self.vbox.pack_start(self.label_ejemplo, expand=True, fill=False, padding=5)

        self.label_canciones = Gtk.Label(_("Canciones representativas del intervalo:"))
        self.vbox.pack_start(self.label_canciones, expand=True, fill=False, padding=15)

        self.spinner = Gtk.Spinner()
        self.vbox.pack_start(self.spinner, expand=False, fill=False, padding=15)

        # Margen inferior
        self.vbox.pack_end(Gtk.Box(), expand=False, fill=False, padding=10)  # Margen inferior

        # Fila inferior
        self.hbox_abajo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox.pack_end(self.hbox_abajo, expand=False, fill=False, padding=15)

        # Boton de volver
        self.volver_align = Gtk.Alignment(xalign=0.90, xscale=0, yalign=0.50, yscale=0)
        self.volver_button = Gtk.Button(_("Volver"))
        self.volver_align.add(self.volver_button)
        self.hbox_abajo.pack_end(self.volver_align, expand=True, fill=False, padding=15)

        # Boton para ver más
        self.see_more_align = Gtk.Alignment(xalign=0.10, xscale=0, yalign=0.50, yscale=0)
        self.see_more_button = Gtk.Button(_("Ver más"))
        self.see_more_button.connect('clicked', self._see_more)
        self.see_more_align.add(self.see_more_button)
        self.hbox_abajo.pack_end(self.see_more_align, expand=True, fill=False, padding=5)

    def update_song_list(self, new_list):
        self.song_list = new_list
        # Las canciones se almacenan en una lista de tuplas (ternas) de la forma (nombre, link, is_fav)
        # Dicha lista viene por parámetro. La ventana de resultados se instancia cuando ya se saben los resultados

        # El conjunto de los tres elementos que muestran una canción (la label con su nombre, la label que indica si
        # es o no favorita, y el botón de escuchar), vienen en una tupla y se añaden a la ventana principal

        self.hboxsongs = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox.pack_start(self.hboxsongs, expand=True, fill=False, padding=5)
        self.vbox_titles = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox_listen = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.hboxsongs.pack_start(Gtk.Box(), expand=True, fill=False, padding=10)  # Margenes laterales
        self.hboxsongs.pack_start(self.vbox_titles, expand=True, fill=False, padding=5)
        self.hboxsongs.pack_start(self.vbox_listen, expand=False, fill=False, padding=5)
        self.hboxsongs.pack_start(Gtk.Box(), expand=True, fill=False, padding=10)  # Margenes laterales

        # Generador de tuplas de canciones
        self.songs_generator = self._get_song()
        song_widgets = self.songs_generator.__next__()

        self.vbox_titles.pack_start(song_widgets[0], expand=True, fill=False, padding=5)
        self.vbox_listen.pack_start(song_widgets[1], expand=True, fill=False, padding=5)

        self.hboxsongs.show_all()

    def _see_more(self, wigdet=None):
        # Hides away the "Ver más" button
        self.see_more_button.hide()
        for song_widgets in self.songs_generator:
            self.vbox_titles.pack_start(song_widgets[0], expand=True, fill=False, padding=5)
            self.vbox_listen.pack_start(song_widgets[1], expand=True, fill=False, padding=5)
        self.hboxsongs.show_all()

    # Yields a tuple with the widgets referring to a song from the list
    def _get_song(self):
        import webbrowser
        for song in self.song_list:
            is_fav = ("❤" if song[2] else "♡")  # Shows a red heart if the song is considered "favorite"
            song_title = song[0] + "   " + is_fav
            song_label = Gtk.Label(song_title)
            listen_button = Gtk.Button(label=_("Escuchar"))
            if song[1] == '':
                listen_button.set_sensitive(False)  # Si no hay enlace de Youtube
            else:
                listen_button.connect('clicked', (lambda _: webbrowser.open(song[1])))
            widgets = (song_label, listen_button)
            yield widgets

    @staticmethod
    def _interval_full_name(index):
        intervals_full = [_("Segunda menor (2m)"),
                          _("Segunda mayor (2M)"),
                          _("Tercera menor (3m)"),
                          _("Tercera mayor (3M)"),
                          _("Cuarta justa (4j)"),
                          _("Cuarta aumentada (4aum)"),
                          _("Quinta justa (5j)"),
                          _("Sexta menor (6m)"),
                          _("Sexta mayor (6M)"),
                          _("Séptima menor (7m)"),
                          _("Séptima mayor (7M)"),
                          _("Octava (8a)")]
        return intervals_full[index]

    def show_waiting(self):
        self.label_canciones.set_label(_("Esperando respuesta del servidor..."))
        self.volver_button.set_label(_("Cancelar"))
        self.window.show_all()
        self.see_more_align.hide()
        self.spinner.start()

    def show_songs(self):
        self.label_canciones.set_label(_("Canciones representativas del intervalo:"))
        self.volver_button.set_label(_("Volver"))
        self.spinner.stop()
        self.window.show_all()
        #If there are no more songs, hide the "See more" button
        if len(self.song_list)<2:
            self.see_more_button.hide()
        self.spinner.hide()

    def destroy(self):
        self.window.destroy()

    def connect_delete_event(self, handler):
        self.window.connect('delete-event', handler)

    def connect_volver_clicked(self, handler):
        self.volver_button.connect('clicked', handler)
