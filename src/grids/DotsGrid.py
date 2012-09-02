# -*- coding: utf-8 -*-

import SurfaceGrid
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from base.support import xfrange
from base import settings

class DotsGrid (SurfaceGrid.SurfaceGrid):
    
    def reloadSettings (self):
        super (DotsGrid, self).reloadSettings ()
        self._normalColor = settings.getColor ('Grid/NormalColor', Qt.darkGray)

    def draw (self, painter, rect):
        if not self._visible:
            return
        start = self.closestNode (rect.topLeft ())
        painter.setPen (self._normalColor)
        for x in xfrange (start.x (), rect.right (), self._size):
            dots = []
            for y in xfrange (start.y (), rect.bottom (), self._size):
                dots.append (QPointF (x, y))
            painter.drawPoints (QPolygonF (dots))
