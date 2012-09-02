# -*- coding: utf-8 -*-

import SurfaceGrid
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from base.support import xfrange
from base import settings

class LinesGrid (SurfaceGrid.SurfaceGrid):
    
    def reloadSettings (self):
        super (LinesGrid, self).reloadSettings ()
        self._step = settings.getInt ('Grid/Step', 5)
        self._normalPen = settings.get (QPen, 'Grid/Lines/NormalPen', QPen (QBrush (Qt.darkGray), 1.0))
        self._baselinePen = settings.get (QPen, 'Grid/Lines/BaselinePen', QPen (QBrush (Qt.darkGray), 3.0))
        self._normalPen.setCosmetic (True)
        self._baselinePen.setCosmetic (True)

    def draw (self, painter, rect):
        if not self._visible:
            return

        lines = []
        baseLines = []

        start = self.closestNode (rect.topLeft ())

        i = round (start.x () / self._size) % self._step
        for x in xfrange (start.x (), rect.right (), self._size):
            line = QLineF (x, rect.top (), x, rect.bottom ())
            if i % self._step == 0:
                baseLines.append (line)
            else:
                lines.append (line)
            i += 1

        i = round (start.y () / self._size) % self._step
        for y in xfrange (start.y (), rect.bottom (), self._size):
            line = QLineF (rect.left (), y, rect.right (), y)
            if i % self._step == 0:
                baseLines.append (line)
            else:
                lines.append (line)
            i += 1

        painter.setPen (self._normalPen)
        painter.drawLines (lines)
        painter.setPen (self._baselinePen)
        painter.drawLines (baseLines)
