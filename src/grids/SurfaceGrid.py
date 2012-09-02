# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from base import settings

class SurfaceGrid (object):

    def __init__ (self, surface):
        self._surface = surface
        self._enabled = True
        self._visible = True
        self.reloadSettings ()
    
    def reloadSettings (self):
        self._size = settings.getFloat ('Grid/Size', 1.27)

    def disable (self):
        if self._enabled:
            self.setEnabled (False)

    def enable (self):
        if not self._enabled:
            self.setEnabled (False)

    def isEnabled (self):
        return self._enabled

    def surface (self):
        return self._surface

    def size (self):
        return self._size

    def setSize (self, value):
        self._size = value

    def setVisible (self, value):
        if self._visible == value:
            return
        self._visible = value
        self._surface.invalidate (self._surface.sceneRect (), QGraphicsScene.BackgroundLayer)
    
    def isVisible (self):
        return self._visible

    def hide (self):
        if self._visible:
            self.setVisible (False)

    def show (self):
        if not self._visible:
            self.setVisible (True)

    def checkVisibilty (self, scale):
        self.setVisible (scale * self._size >= 3.0)

    def closestNode (self, point):
        return QPointF (
            round (point.x () / self._size) * self._size,
            round (point.y () / self._size) * self._size
        )

    def draw (self, painter, rect):
        raise NotImplementedError ('draw() is not implemented')
