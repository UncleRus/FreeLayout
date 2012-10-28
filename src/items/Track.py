# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PcbItem import PcbItem
from base import settings

class Track (PcbItem):
    
    def __init__ (self, position, nodes, width, layer, parent = None):
        super (Track, self).__init__ (layer, parent)
        self._width = width
        self._nodes = nodes
        self.setPos (position)
        self._recalc ()
        self._dragNode = None
    
    def reloadSettings (self):
        super (Track, self).reloadSettings ()
        self._selectedNodesPen = settings.get (QPen, 'Track/SelectedNodesPen', Qt.white)
        self._selectedNodesBrush = settings.get (QBrush, 'Track/SelectedNodesBrush', Qt.blue)
    
    def width (self):
        return self._width
    
    def setWidth (self, value):
        self._width = value
        self._recalc ()
        self.update ()

    def paint (self, painter, option, widget):
        if len (self._nodes) == 0:
            return
        color = self._brush ().color ()
        painter.setPen (
            QPen (
                QBrush (color, Qt.SolidPattern),
                #self._width,
                0,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin
            )
        )
        #for i in xrange (1, len (self._nodes)):
        #    painter.drawLine (self._nodes [i - 1], self._nodes [i])
        painter.drawPath (self._shape)
        if self.isSelected ():
            painter.setPen (self._selectedNodesPen)
            painter.setBrush (self._selectedNodesBrush)
            radius = self._width / 2.0
            for node in self._nodes:
                painter.drawEllipse (node, radius, radius)
    
    def _recalc (self):
        p = QPainterPath ()
        p.moveTo (self._nodes [0])
        for node in self._nodes [1:]:
            p.lineTo (node)
        for node in reversed (self._nodes [:-1]):
            p.lineTo (node)
        ps = QPainterPathStroker ()
        ps.setCapStyle (Qt.RoundCap)
        ps.setJoinStyle (Qt.RoundJoin)
        ps.setWidth (self._width)
        self._shape = ps.createStroke (p)
        self._rect = self._shape.boundingRect ()
        radius = self._width / 2
        self._nodeMarkers = []
        for node in self._nodes:
            marker = QPainterPath ()
            marker.addEllipse (node, radius, radius)
            self._nodeMarkers.append ((marker, node))
    
    def _findNode (self, point):
        for marker in self._nodeMarkers:
            if marker [0].contains (point):
                return marker [1]
        return None
    
    def mousePressEvent (self, event):
        self._dragNode = self._findNode (event.pos ())
        if self._dragNode is None:
            super (Track, self).mousePressEvent (event)
        #else:
        #    QGraphicsItem.mousePressEvent (self, event)
    
    def mouseReleaseEvent (self, event):
        self._dragNode = None
        super (Track, self).mouseReleaseEvent (event)
    
    def mouseMoveEvent (self, event):
        if self._dragNode is None:
            super (Track, self).mouseMoveEvent (event)
            return
        self.scene ().update (self.mapRectToScene (self.boundingRect ()))
        self._dragNode += (self.scene ().position () - self.pos ()) - self._dragNode
        self._recalc ()
        self.scene ().update (self.mapRectToScene (self.boundingRect ()))
        
    def shape (self):
        return self._shape
    
    def boundingRect (self):
        return self._rect

    def addNodes (self, nodes):
        self._nodes += nodes
        self._recalc ()
        self.update ()
        
    def addNode (self, node):
        self._nodes.append (node)
        self._recalc ()
        self.update ()
