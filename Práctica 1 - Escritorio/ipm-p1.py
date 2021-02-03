#!/usr/bin/env python3

from pathlib import Path
import controller
import sys
import locale
import gettext

if __name__ == '__main__':
    # Internationalizacion
    locale.setlocale(locale.LC_ALL, '')

    # Establecer BBDD de traducciones
    LOCALE_DIR = Path(__file__).parent / "locale"
    locale.bindtextdomain('Xazam', LOCALE_DIR)
    gettext.bindtextdomain('Xazam', LOCALE_DIR)
    gettext.textdomain('Xazam')

    if len(sys.argv) <= 1:
        controlador = controller.Controller()
    else:
        controlador = controller.Controller(sys.argv[1], sys.argv[2])
    controlador.start()
