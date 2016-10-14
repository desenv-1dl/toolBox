# -*- coding: utf-8 -*-

from main import Main

def name():
    return "Caixa de Ferramentas"
def description():
    return "Conjunto de Ferramentas para Aquisição"
def version():
    return "Version 0.1"
def classFactory(iface):
    return Main(iface)
def qgisMinimumVersion():
    return "2.0"
def author():
    return ""
def email():
    return "me@hotmail.com"
def icon():
    return "icon.png"
