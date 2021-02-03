#!/usr/bin/env python3

import sys
import textwrap
from collections import namedtuple
import time

import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi

import e2e

"""Histories:
    GIVEN he lanzado la aplicación
    THEN veo el texto "Seleccionar intervalo" & Combo Box vacío
    GIVEN he lanzado la aplicación
    WHEN selecciono '3M'
    THEN la vista del intervalo muestra el texto "Tercera mayor(3M)"
    GIVEN he lanzado la aplicacion
    WHEN selecciono 3M Asc
    THEN las notas de ejemplo son 3M asc
    GIVEN he lanzado la aplicación
    WHEN busco intervalo 3M Asc
    THEN compruebo que texto de resultados es igual a 3M asc
    GIVEN he lanzado la aplicación
    WHEN busco intervalo 3M asc
    WHEN Ver más
    THEN compruebo que Kumbaya no es favorita
"""

# Funciones de ayuda

def show(text):
    print(textwrap.dedent(text))

def show_passed():
    print('\033[92m', "    Passed", '\033[0m')

def show_not_passed(e):
    print('\033[91m', "    Not passsed", '\033[0m')
    print(textwrap.indent(str(e), "    "))


# Contexto de las pruebas

Ctx = namedtuple("Ctx", "path process app")


# Implementación de los pasos

def given_he_lanzado_la_aplicacion(ctx):
    process, app = e2e.run(ctx.path)
    assert app is not None
    return Ctx(path= ctx.path, process= process, app= app)

def then_veo_el_texto_Seleccionar_intervalo(ctx):
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'label' and node.get_text(0, -1).startswith("Seleccionar intervalo"))
    label = next(gen, None)
    assert label is not None
    assert label.get_name() == "Seleccionar intervalo:"
    return ctx
    
    
def then_veo_combo_box_vacio(ctx):
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'combo box')
    CB = next(gen, None)
    assert CB is not None
    assert CB.get_name() == ""
    return ctx

def when_selecciono_3M(ctx):
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'combo box')
    CB = next(gen, None)
    assert CB is not None
    CB.select_child(3)
    return ctx
    
def then_veo_el_texto_3M(ctx):
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'combo box')
    CB = next(gen, None)
    assert CB is not None
    assert CB.get_name() == "Tercera mayor (3M)"
    return ctx

def when_selecciono_asc(ctx):
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'radio button')
    RB = next(gen, None)
    assert RB is not None
    #e2e.do_action(boton, 'click') en este caso no es necesario porque ascendente está seleccionado por defecto
    return ctx
  
def then_notas_de_ejemplo_3M_asc(ctx):
    notas = ["do - mi",
             "do♯/re♭ - fa",
             "re - fa♯/sol♭", 
             "re♯/mi♭ - sol", 
             "mi - sol♯/la♭", 
             "fa - la", 
             "fa♯/sol♭ - la♯/si♭", 
             "sol - si", 
             "sol♯/la♭ - do",
             "la - do♯/re♭", 
             "la♯/si♭ - re", 
             "si - re♯/mi♭"
             ]
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'label' and 
    (node.get_text(0, -1).startswith("do") or
     node.get_text(0, -1).startswith("re") or
     node.get_text(0, -1).startswith("mi") or
     node.get_text(0, -1).startswith("fa") or
     node.get_text(0, -1).startswith("sol") or
     node.get_text(0, -1).startswith("la") or
     node.get_text(0, -1).startswith("si")
    )
    )
    lbNotes = next(gen, None)
    assert lbNotes is not None
    assert (lbNotes.get_name() in notas) is True
    return ctx

def when_busco_intervalo(ctx):
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'push button' and node.get_name() == 'Buscar')
    PB = next(gen, None)
    assert PB is not None
    e2e.do_action(PB, 'click')
    return ctx

def when_ver_mas(ctx):
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'push button' and node.get_name() == 'Ver más')
    PB = next(gen, None)
    assert PB is not None
    isVisible = False
    isShowing = False
    while not (isVisible and isShowing):
        PBstates = PB.get_state_set()
        isVisible = PBstates.contains(Atspi.StateType.VISIBLE)
        isShowing = PBstates.contains(Atspi.StateType.SHOWING)
        time.sleep(0.5)
    e2e.do_action(PB, 'click')
    return ctx
    
def then_veo_el_texto_de_busqueda(ctx):
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'label' and node.get_text(0, -1).startswith("Para el intervalo"))
    label = next(gen, None)
    assert label is not None
    assert label.get_name() == "Para el intervalo Tercera mayor (3M) ascendente, un ejemplo sería:"
    return ctx

def then_compruebo_favorita(ctx):
    genKumb = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'label' and node.get_text(0, -1).startswith("Kumbaya"))
    lbKumb = next(genKumb, None)
    assert lbKumb is not None #Comprueba que Kumbaya está en las canciones de 3M asc
    assert lbKumb.get_name().endswith("♡") #Comprueba que Kumbaya no es favorita
    return ctx


if __name__ == '__main__':
    sut_path = sys.argv[1]
    initial_ctx = Ctx(path= sut_path, process= None, app= None)

    show("""
    GIVEN he lanzado la aplicación
    THEN veo el texto "Seleccionar intervalo" & Combo Box vacío
    """)
    ctx = initial_ctx
    try:
        ctx = given_he_lanzado_la_aplicacion(ctx)
        ctx = then_veo_el_texto_Seleccionar_intervalo(ctx)
        ctx = then_veo_combo_box_vacio(ctx)
        show_passed()
    except Exception as e:
        show_not_passed(e)
    e2e.stop(ctx.process)

    
    show("""
    GIVEN he lanzado la aplicación
    WHEN selecciono '3M'
    THEN la vista del intervalo muestra el texto "Tercera mayor(3M)"
    """)
    ctx = initial_ctx
    try:
        ctx = given_he_lanzado_la_aplicacion(ctx)
        ctx = when_selecciono_3M(ctx)
        ctx = then_veo_el_texto_3M(ctx)
        show_passed()
    except Exception as e:
        show_not_passed(e)
    e2e.stop(ctx.process)
    
    show("""
    GIVEN he lanzado la aplicacion
    WHEN selecciono 3M Asc
    THEN las notas de ejemplo son 3M asc
    """)
    ctx = initial_ctx
    try:
        ctx = given_he_lanzado_la_aplicacion(ctx)
        ctx = when_selecciono_3M(ctx)
        ctx = when_selecciono_asc(ctx)
        ctx = when_busco_intervalo(ctx)
        ctx = then_notas_de_ejemplo_3M_asc(ctx)
        show_passed()
    except Exception as e:
        show_not_passed(e)
    e2e.stop(ctx.process)
    
    show("""
    GIVEN he lanzado la aplicación
    WHEN busco intervalo 3M Asc
    THEN compruebo que texto de resultados es igual a 3M asc
    """)
    ctx = initial_ctx
    try:
        ctx = given_he_lanzado_la_aplicacion(ctx)
        ctx = when_selecciono_3M(ctx)
        ctx = when_selecciono_asc(ctx)
        ctx = when_busco_intervalo(ctx)
        ctx = then_veo_el_texto_de_busqueda(ctx)
        show_passed()
    except Exception as e:
        show_not_passed(e)
    e2e.stop(ctx.process)
    
    show("""
    GIVEN he lanzado la aplicación
    WHEN busco intervalo 3M asc
    WHEN Ver más
    THEN compruebo que Kumbaya no es favorita
    """)
    ctx = initial_ctx
    try:
        ctx = given_he_lanzado_la_aplicacion(ctx)
        ctx = when_selecciono_3M(ctx)
        ctx = when_selecciono_asc(ctx)
        ctx = when_busco_intervalo(ctx)
        ctx = when_ver_mas(ctx)
        ctx = then_compruebo_favorita(ctx)
        show_passed()
    except Exception as e:
        show_not_passed(e)
    e2e.stop(ctx.process)
