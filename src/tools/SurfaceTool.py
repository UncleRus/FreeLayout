# -*- coding: utf-8 -*-

from PyQt4.QtCore import *

class SurfaceTool (object):
    
    def __init__ (self, surface):
        self._surface = surface
        self.reloadSettings ()
        self.onInit ()
    
    def _checkClick (self, event, button):
        if event.button () != button:
            return
        p = event.screenPos () - event.buttonDownScreenPos (button)
        if 1 >= p.x () >= -1 and 1 >= p.y () >= -1:
            self.onMouseClick (event)
    
    def onInit (self):
        pass
    
    def reloadSettings (self):
        pass
    
    def onMouseWheel (self, event):
        pass

    def onMouseMove (self, event):
        pass

    def onMouseClick (self, event):
        pass

    def onMousePress (self, event):
        pass

    def onMouseRelease (self, event):
        self._checkClick (event, Qt.LeftButton)
        self._checkClick (event, Qt.MidButton)
        self._checkClick (event, Qt.RightButton)
        self._checkClick (event, Qt.XButton1)
        self._checkClick (event, Qt.XButton2)
    
    def onMouseDoubleClick (self, event):
        pass
    
    def onKeyPress (self, event):
        pass
    
    def onKeyRelease (self, event):
        pass
    
    def cancel (self):
        pass

    def draw (self, painter, rect):
        pass
