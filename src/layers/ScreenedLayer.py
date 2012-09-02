# -*- coding: utf-8 -*-

import PcbLayer

class ScreenedLayer (PcbLayer.PcbLayer):
    
    def __init__ (self, collection, name, screen = None):
        super (ScreenedLayer, self).__init__ (collection, name)
        self._screen = screen
        self.backing = None
        if self._screen:
            self._screen.backing = self

    def bringToFront (self, byBacking = False):
        if self.backing and not byBacking:
            self.backing.bringToFront ()
        super (ScreenedLayer, self).bringToFront ()
        if self._screen:
            self._screen.bringToFront (True)
    
