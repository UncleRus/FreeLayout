# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from base import settings
from SurfaceTool import SurfaceTool
from math import copysign
from items import Track

class DrawTrackTool (SurfaceTool):
    
    dmDiagonal1 = 0
    dmDiagonal2 = 1
    dmSquare1 = 2
    dmSquare2 = 3
    dmLine = 4
    
    def __init__ (self, surface):
        super (DrawTrackTool, self).__init__ (surface)
        self._lastPoint = QPointF ()
        self._nodes = None
        self._started = False
        self._track = None
        self._drawMethod = self.dmDiagonal1
        self._surface.guides.show ()
    
    def reloadSettings (self):
        super (DrawTrackTool, self).reloadSettings ()
        self._width = settings.getFloat ('Track/Width', 0.8)
        self._brush = settings.glob.selectionBrush ()
    
    def _recalcPath (self):
        start = self._lastPoint
        finish = self._surface.position ()
        
        rect = QRectF (start, finish)
        width = abs (rect.width ())
        height = abs (rect.height ())
        
        self._nodes = []
        self._nodes.append (start)
        
        if (width == height or width == 0 or height == 0 or self._drawMethod == self.dmLine) \
            and self._drawMethod not in (self.dmSquare1, self.dmSquare2):
            self._nodes.append (finish)
            return
        
        if self._drawMethod == self.dmDiagonal1:
            if width > height:
                self._nodes.append (QPointF (finish.x () - copysign (height, rect.width ()), start.y ()))
            else:
                self._nodes.append (QPointF (start.x (), finish.y () - copysign (width, rect.height ())))

        elif self._drawMethod == self.dmDiagonal2:
            if width > height:
                self._nodes.append (QPointF (start.x () + copysign (height, rect.width ()), finish.y ()))
            else:
                self._nodes.append (QPointF (finish.x (), start.y () + copysign (width, rect.height ())))

        elif self._drawMethod == self.dmSquare1:
            self._nodes.append (QPointF (finish.x () + start.y ()))
        
        else:
            self._nodes.append (QPointF (start.x () + finish.y ()))
        
        self._nodes.append (finish)

    def _invalidate (self):
        rect = QPolygonF (self._nodes).boundingRect ()
        rect.adjust (-self._width, -self._width, self._width, self._width)
        self._surface.invalidate (rect, QGraphicsScene.AllLayers)
    
    def draw (self, painter, rect):
        painter.setCompositionMode (settings.const.toolCompositionMode)
        if not self._started or (len (self._nodes) == 2 and self._nodes [0] == self._nodes [1]):
            painter.setPen (Qt.NoPen)
            painter.setBrush (self._brush)
            painter.drawEllipse (self._surface.position (), self._width / 2, self._width / 2)
            return
        painter.setPen (QPen (self._brush, self._width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLines ([QLineF (self._nodes [i - 1], self._nodes [i]) for i in xrange (1, len (self._nodes))])
    
    def onMouseMove (self, event):
        self._recalcPath ()
        self._invalidate ()
    
    def onMouseClick (self, event):
        if event.button () == Qt.RightButton:
            if not self._started:
                self._surface.cancelTool ()
                return
            self._started = False
            #self._surface.invalidate (self._nodes.boundingRect (), QGraphicsScene.ForegroundLayer)
            self._track = None
            self._invalidate ()
            self._nodes = self._recalcPath ()
            self._invalidate ()
            return
        
        if self._surface.position () == self._lastPoint:
            return
        
        if event.button () == Qt.LeftButton:
            if not self._started:
                self._started = True
            else:
                if not self._track:
                    self._track = Track (
                        QPointF (0, 0),
                        self._nodes,
                        self._width,
                        self._surface.currentLayer ()
                    )
                    self._surface.addItem (self._track)
                    
                self._track.addNodes (self._nodes)
            self._lastPoint = self._surface.position ()
            self._recalcPath ()

    def cancel (self):
        self._surface.guides.hide ()
    