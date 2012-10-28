# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from grids import classes
from base import settings
from Guides import Guides
from layers import *
from items import *
import tools


class Surface (QGraphicsScene):
    
    scaled = pyqtSignal (float)
    dragStarted = pyqtSignal ()
    dragEnded = pyqtSignal ()
    dragging = pyqtSignal (QPoint)

    def __init__ (self, rect, parent = None):
        super (Surface, self).__init__ (rect, parent)
        self._gridType = ''
        self.guides = Guides (self)
        #self.guides.show ()
        self._position = QPointF ()
        self._tool = None
        self._scale = 1.0
        self._dragging = False
        self._dragPosition = QPoint ()
        self._mouseLock = False
        self._currentLayer = None
        self.reloadSettings ()
        self._layers = dict ()
        self._layers ['TopMask'] = SilkscreenLayer (self._layers, 'TopMask')
        self._layers ['TopSlikscreen'] = SilkscreenLayer (self._layers, 'TopSlikscreen', self._layers ['TopMask'])
        self._layers ['TopConductive'] = ConductiveLayer (self._layers, 'TopConductive', self._layers ['TopSlikscreen'])
        self._layers ['BottomMask'] = SilkscreenLayer (self._layers, 'BottomMask')
        self._layers ['BottomSlikscreen'] = SilkscreenLayer (self._layers, 'BottomSlikscreen', self._layers ['BottomMask'])
        self._layers ['BottomConductive'] = ConductiveLayer (self._layers, 'BottomConductive', self._layers ['BottomSlikscreen'])
        self.setCurrentLayer ('BottomConductive')
        #self._tool = tools.SmdPadTool (self)
        self._tool = tools.DrawTrackTool (self)
        
        track = Track (QPointF (20, 20), [QPointF (0, 0), QPointF (10, 10), QPointF (10, 50), QPointF (20, 60)], 1.0, self._currentLayer)
        self.addItem (track)
    
    def reloadSettings (self):
        self._unusedSpaceBrush = settings.get (QBrush, 'Surface/UnusedSpaceBrush', Qt.gray)
        self.setBackgroundBrush (settings.get (QBrush, 'Surface/BackgroundBrush', Qt.black))
        gridType = settings.getString ('Grid/Type', u'lines')
        if self._gridType != gridType:
            self._gridType = gridType
            self.grid = classes.get (gridType, classes ['lines']) (self)
        else:
            self.grid.reloadSettings ()
        self.guides.reloadSettings ()
        if self._tool:
            self._tool.reloadSettings ()

    def position (self):
        return self._position
        
    def currentLayer (self):
        return self._currentLayer
    
    def setCurrentLayer (self, name):
        if self._currentLayer and self._currentLayer.name == name:
            return
        self._currentLayer = self._layers [name]
        self._currentLayer.bringToFront ()
    
    def drawBackground (self, painter, rect):
        painter.fillRect (rect, self._unusedSpaceBrush)
        realRect = rect.intersect (self.sceneRect ())
        painter.fillRect (realRect, self.backgroundBrush ())
        self.grid.draw (painter, realRect)

    def drawForeground (self, painter, rect):
        realRect = rect.intersect (self.sceneRect ())
        self.guides.draw (painter, realRect)
        # TODO : рисовать дырки в плате
        if self._tool:
            self._tool.draw (painter, rect)
    
    def _startDrag (self, position):
        self._dragPosition = position
        self._dragging = True
        self.dragStarted.emit ()

    def _moveDrag (self, event):
        self._mouseLock = True
        
        delta = self._dragPosition - event.screenPos ()
        
        self._dragPosition = event.screenPos ()
        event.accept ()
        
        self._mouseLock = False
        self.dragging.emit (delta)
        
    def _stopDrag (self):
        self._dragging = False
        self.dragEnded.emit ()
    
    def mousePressEvent (self, event):
        #print 'Surface.mousePressEvent'
        if event.button () == Qt.MidButton:
            # Начинаем перетаскивание
            self._startDrag (event.screenPos ())
            event.accept ()
            return
        
        if self._tool:
            # Если есть инструмент, передаем обработку ему
            self._tool.onMousePress (event)
            event.accept ()
            return
        
        #if event.button () != Qt.LeftButton:
        #    return
        super (Surface, self).mousePressEvent (event)
        
    def mouseMoveEvent (self, event):
        if self._mouseLock:
            return
        
        if self._dragging:
            self._moveDrag (event)
            return
        
        # Определяем положение курсора
        lastPosition = self._position
        self._position = self.grid.closestNode (event.scenePos ()) if self.grid.isEnabled () else event.scenePos ()
        if self._position == lastPosition:
            return
        if not self.sceneRect ().contains (self._position):
            self._position = lastPosition
            return
        
        # Перемещаем направляющие
        self.guides.moveTo (self._position)
        if self._tool:
            # Если есть инструмент, передаем обработку ему
            self._tool.onMouseMove (event)
        else:
            # иначе вызываем обработчик по умолчанию
            super (Surface, self).mouseMoveEvent (event)
    
    def mouseReleaseEvent (self, event):
        if self._dragging and event.button () == Qt.MidButton:
            self._stopDrag ()
            return
        
        if self._tool:
            self._tool.onMouseRelease (event)
            event.accept ()
            return
        
        super (Surface, self).mouseReleaseEvent (event)
    
    def mouseDoubleClickEvent (self, event):
        if self._tool:
            self._tool.onMouseDoubleClick (event)
    
    def wheelEvent (self, event):
        if self._tool:
            self._tool.onMouseWheel (event)
            if event.isAccepted ():
                return
            
        if event.delta () > 0:
            self.zoomIn ()
        else:
            self.zoomOut ()
        
        event.accept ()
    
    def keyPressEvent (self, event):
        if self._tool:
            self._tool.onKeyPress (event)
    
    def keyReleaseEvent (self, event):
        if self._tool:
            self._tool.onKeyRelease (event)

    def cancelTool (self):
        if not self._tool:
            return
        self._tool.cancel ()
        del self._tool
        self._tool = None
    
    def scale (self):
        return self._scale
    
    def setScale (self, value):
        self._scale = value
        self.grid.checkVisibilty (self._scale)
        self.scaled.emit (self._scale)
    
    def zoomIn (self):
        self.setScale (self.scale () * 1.25)

    def zoomOut (self):
        self.setScale (self.scale () / 1.25)
    
    def moveSelectedBy (self, delta):
        if delta.isNull ():
            return
        
        rect = QRectF ()
        for item in self.selectedItems ():
            if rect.isNull ():
                rect = item.mapRectToScene (item.boundingRect ())
            else:
                rect.unite (item.mapRectToScene (item.boundingRect ()))
        
        if not self.sceneRect ().contains (rect.translated (delta)):
            return
        
        for item in self.selectedItems ():
            item.moveBy (delta.x (), delta.y ())




