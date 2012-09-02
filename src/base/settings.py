# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class const (object):
    toolCompositionMode = QPainter.CompositionMode_SourceOver
    
settings = QSettings ()

def getColor (key, default = Qt.black):
    return QColor (settings.value (key, QColor (default)).toString ())

def getInt (key, default = 0):
    return settings.value (key, int (default)).toInt ()[0]

def getBool (key, default = False):
    return settings.value (key, bool (default)).toBool ()[0]

def getFloat (key, default = 0.0):
    return settings.value (key, float (default)).toReal ()[0]

def getString (key, default = u''):
    return unicode (settings.value (key, unicode (default)).toString ())

def get (type, key, default):
    return type (settings.value (key, type (default)).toPyObject ())


class glob (object):
    
    @staticmethod
    def selectionBrush ():
        return get (QBrush, 'SelectionBrush', Qt.magenta)
