# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from DrawSingleTool import DrawSingleTool
from base import settings
from items import SmdPad

class SmdPadTool (DrawSingleTool):
    
    def __init__ (self, surface):
        super (SmdPadTool, self).__init__ (surface)
        self._horizontal = False
    
    def rect (self):
        return QRectF (
            self._position.x () - self._width / 2,
            self._position.y () - self._height / 2,
            self._width,
            self._height
        ) if not self._horizontal else QRectF (
            self._position.x () - self._height / 2,
            self._position.y () - self._width / 2,
            self._height,
            self._width
        )
    
    def reloadSettings (self):
        super (SmdPadTool, self).reloadSettings ()
        self._width = settings.getFloat ('SmdPad/Width', 1.1)
        self._height = settings.getFloat ('SmdPad/Height', 2.54)
        self._brush = settings.glob.selectionBrush ()
    
    def createItem (self):
        result = SmdPad (
            self._position,
            self._width,
            self._height,
            self._surface.currentLayer ()
        )
        if self._horizontal:
            result.rotate (90)
        return result

    def switchType (self):
        self._surface.invalidate (self.rect ())
        self._horizontal = not self._horizontal
        self._surface.invalidate (self.rect ())
    
    def draw (self, painter, rect):
        painter.setPen (Qt.NoPen)
        painter.setCompositionMode (settings.const.toolCompositionMode)
        painter.fillRect (QRectF (self.rect ()), self._brush)
