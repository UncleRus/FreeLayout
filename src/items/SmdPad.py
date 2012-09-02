# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PcbItem import PcbItem

class SmdPad (PcbItem):
    
    def __init__ (self, position, width, height, layer, parent = None):
        super (SmdPad, self).__init__ (layer, parent)
        self._width = width
        self._height = height
        self.setPos (position)
    
    def width (self):
        return self._width
    
    def setWidth (self, value):
        self._width = value
        self.update ()

    def height (self):
        return self._height
    
    def setHeight (self, value):
        self._height = value
        self.update ()
    
    def paint (self, painter, option, widget):
        painter.setPen (Qt.NoPen)
        painter.fillRect (self.boundingRect (), self._brush ())
    
    def boundingRect (self):
        return QRectF (-self._width / 2, -self._height / 2, self._width, self._height)
