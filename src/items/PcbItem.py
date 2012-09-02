# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from base import settings

class PcbItem (QGraphicsItem):
    
    def __init__ (self, layer, parent = None):
        super (PcbItem, self).__init__ (parent)
        self._layer = None
        self._dragging = False
        self._lastPosition = QPointF ()
        self.reloadSettings ()
        self.setToLayer (layer)
        self.setFlag (QGraphicsItem.ItemIsSelectable, True)
    
    def reloadSettings (self):
        self._selectedBrush = settings.glob.selectionBrush ()
    
    def setToLayer (self, layer):
        if not layer:
            raise ValueError ('layer cannot be None')
        if self._layer == layer:
            return
        if self._layer:
            self._layer.remove (self)
        self._layer = layer
        self._layer.add (self)

    def layer (self):
        return self._layer
    
    def _brush (self):
        return self._layer.brush () if not self.isSelected () else self._selectedBrush
    
    def mousePressEvent (self, event):
        super (PcbItem, self).mousePressEvent (event)
        self._dragging = True
        self._lastPosition = self.scene ().position ()
    
    def mouseReleaseEvent (self, event):
        super (PcbItem, self).mouseReleaseEvent (event)
        self._dragging = False
    
    def mouseMoveEvent (self, event):
        if not self._dragging or not self.scene ():
            return
        self.scene ().moveSelectedBy (self.scene ().position () - self._lastPosition)
        self._lastPosition = self.scene ().position ()
    
    def itemChange (self, change, value):
        if change == self.ItemSelectedHasChanged:
            self.setZValue (self.zValue () + 1000 if self.isSelected () else self.zValue () - 1000)
        return super (PcbItem, self).itemChange (change, value)

