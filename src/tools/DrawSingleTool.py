# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from SurfaceTool import SurfaceTool

class DrawSingleTool (SurfaceTool):
    
    def onInit (self):
        self._position = QPointF ()
        self._surface.guides.show ()
    
    def onMouseMove (self, event):
        self._surface.invalidate (self.rect (), QGraphicsScene.ForegroundLayer)
        self._position = self._surface.position ()
        self._surface.invalidate (self.rect (), QGraphicsScene.ForegroundLayer)

    def onMouseClick (self, event):
        if not self._surface.sceneRect ().contains (self._position):
            return
        if event.button () == Qt.RightButton:
            self._surface.cancelTool ()
        elif event.button () == Qt.LeftButton:
            self._surface.addItem (self.createItem ())
    
    def onKeyPress (self, event):
        if event.key () == Qt.Key_Escape:
            self._surface.cancelTool ()
        elif event.key () == Qt.Key_Space:
            self.switchType ()

    def cancel (self):
        self._surface.guides.hide ()
    
    def createItem (self):
        raise NotImplementedError ('createItem() is not implemented')

    def rect (self):
        return QRectF ()

    def switchType (self):
        pass
