# Model of the Xazam app
import requests
import gettext

_ = gettext.gettext

class Model:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.lista_notas = [_("do"),
                            _("do♯/re♭"),
                            _("re"),
                            _("re♯/mi♭"),
                            _("mi"),
                            _("fa"),
                            _("fa♯/sol♭"),
                            _("sol"),
                            _("sol♯/la♭"),
                            _("la"),
                            _("la♯/si♭"),
                            _("si")]
        self.intervals = ["2m",
                          "2M",
                          "3m",
                          "3M",
                          "4j",
                          "4aum",
                          "5j",
                          "6m",
                          "6M",
                          "7m",
                          "7M",
                          "8a"]
        self.distancias = dict(zip(self.intervals, list(range(1, 13))))

    def _get_interval_name(self, index):
        if index == -1:
            return None
        else:
            return self.intervals[index]

    @staticmethod
    def get_interval_size(index, is_asc):
        if is_asc:
            return index + 1
        else:

            return 0 - (index + 1)

    def get_example(self, interval_index, is_asc):
        return self._get_example(self.get_interval_size(interval_index, is_asc))

    def _get_example(self, interval_size):
        # interval_size es un entero positivo para intervalos ascendentes
        # y un entero negativo para intervalos descententes
        from random import randint
        i = randint(0, 11)
        nota_1 = self.lista_notas[i]
        nota_2 = self.lista_notas[(i + interval_size) % 12]
        return f"{nota_1} - {nota_2}"

    # Este método recibe el índice del intervalo, y un boolean indicando si es ascendente
    # indicando si es ascendente o descendente
    def get_songs(self, interval_index, is_asc):
        interval = self._get_interval_name(interval_index)
        sentido = "asc" if is_asc else "des"
        url = f"http://{self.server_address}:{self.server_port}/songs/{interval}/{sentido}"
        try:
            req = requests.get(url)
            if req.status_code != 200:
                raise IOError()
            responsedata = req.json().get('data')
            if responsedata is None:
                raise ValueError()
            songs_list = list()
            # Converts the list of lists to a list of tuples because that's what the view was designed for
            # Plus, tuples are inmutable and we shouldn't want to change a song's information
            for songdata in responsedata:
                songs_list.append((songdata[0], songdata[1], (True if songdata[2] == "YES" else False)))
            return songs_list
        except Exception:
            raise IOError("Server not responding or response invalid")
