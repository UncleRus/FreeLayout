#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import Surface

class Window (QWidget):

    def __init__ (self, parent = None):
        super (Window, self).__init__ (parent)
        self.setupUi ()

    def setupUi (self):
        self.view = QGraphicsView (self)
        self.view.setMouseTracking (True)
        self.vl = QVBoxLayout (self)
        self.vl.addWidget (self.view)

        self.surface = Surface.Surface (QRectF (0, 0, 800, 800), self)
        self.surface.dragStarted.connect (self.onDragStarted)
        self.surface.dragging.connect (self.onDragging)
        self.surface.dragEnded.connect (self.onDragEnded)
        self.surface.scaled.connect (self.onScaled)
        self.view.setScene (self.surface)
        self.surface.setScale (10)
    
    def onDragStarted (self):
        self.view.setCursor (QCursor (Qt.ClosedHandCursor))
    
    def onDragging (self, delta):
        if self.view.isRightToLeft ():
            delta.setX (-delta.x ())
        self.view.horizontalScrollBar ().setValue (self.view.horizontalScrollBar ().value () + delta.x ())
        self.view.verticalScrollBar ().setValue (self.view.verticalScrollBar ().value () + delta.y ())
    
    def onDragEnded (self):
        self.view.setCursor (Qt.ArrowCursor)
    
    def onScaled (self, scale):
        m = self.view.matrix ()
        self.view.resetMatrix ()
        self.view.translate (m.dx (), m.dy ())
        self.view.scale (scale, scale)


version = '0.1.0'

def main ():
    QCoreApplication.setOrganizationName ('UncleRus')
    QCoreApplication.setApplicationName ('FreeLayout')
    QCoreApplication.setApplicationVersion (version)

    app = QApplication (sys.argv)

    mainWindow = Window ()
    mainWindow.show ()

    sys.exit (app.exec_ ())


if __name__ == '__main__':
    main ()
