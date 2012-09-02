# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from base import settings

class Guides (object):
    
    def __init__ (self, surface):
        self._surface = surface
        self._position = QPointF ()
        self._visible = False
        self.reloadSettings ()
    
    def reloadSettings (self):
        self._pen = settings.get (QPen, 'Guides/Pen', QColor (Qt.yellow))
    
    def draw (self, painter, rect):
        if not self._visible:
            return
        painter.setCompositionMode (settings.const.toolCompositionMode)
        painter.setPen (self._pen)
        painter.drawLine (QLineF (rect.left (), self._position.y (), rect.right (), self._position.y ()))
        painter.drawLine (QLineF (self._position.x (), rect.top (), self._position.x (), rect.bottom ()))
    
    def getHRect (self):
        return QRectF (-1.0, self._position.y () - 1.0, self._surface.sceneRect ().width () + 2.0, self._position.y () + 1.0)

    def getVRect (self):
        return QRectF (self._position.x () - 1.0, -1, self._position.x () + 1.0, self._surface.sceneRect ().height () + 2.0)
    
    def update (self):
        self._surface.invalidate (self.getHRect (), QGraphicsScene.ForegroundLayer)
        self._surface.invalidate (self.getVRect (), QGraphicsScene.ForegroundLayer)
    
    def moveTo (self, position):
        if self._position == position or not self._visible:
            return

        self.update ()
        self._position = position
        self.update ()
    
    def position (self):
        return self._position
    
    def setPosition (self, position):
        self.moveTo (position)

    def setVisible (self, value):
        self._visible = value
        self.update ()
    
    def isVisible (self):
        return self._visible

    def hide (self):
        if self._visible:
            self.setVisible (False)

    def show (self):
        if not self._visible:
            self.setVisible (True)
