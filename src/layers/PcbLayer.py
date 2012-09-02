# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from base import settings

class PcbLayer (object):
    
    def __init__ (self, collection, name):
        self._collection = collection
        self._name = name
        self._items = []
        self._zValue = 0.0
        self._visible = True
        self._inverted = False
        self._brush = None
        self.reloadSettings ()
        
    def reloadSettings (self):
        self._brush = settings.get (QBrush, 'Layers/{}/Brush'.format (self._name), Qt.green)
        for item in self._items:
            item.reloadSettings ()
    
    def setInverted (self, inverted):
        if self._inverted == inverted:
            return
        
        self._inverted = inverted
        for item in self._items:
            item.update ()
    
    def inverted (self):
        return self._inverted
    
    def invert (self):
        self.setInverted (not self._inverted)
    
    def setBrush (self, brush):
        if self._brush == brush:
            return
        
        self._brush = brush
        for item in self._items:
            item.update ()
    
    def brush (self):
        return self._brush
    
    def setZValue (self, value):
        if self._zValue == value:
            return
        
        self._zValue = value
        for item in self._items:
            item.setZValue (self._zValue)
        
    def zValue (self):
        return self._zValue
    
    def setVisible (self, visible):
        if self._visible == visible:
            return
        
        self._visible = visible
        for item in self._items:
            item.setVisible (self._visible)
    
    def isVisible (self):
        return self._visible

    def hide (self):
        if self._visible:
            self.setVisible (False)

    def show (self):
        if not self._visible:
            self.setVisible (True)
            
        
    def indexOf (self, item):
        try:
            return self._items.index (item)
        except ValueError:
            return -1
        
    def add (self, item):
        if self.indexOf (item) >= 0:
            return
        
        self._items.append (item)
        item.setZValue (self._zValue)
        item.setVisible (self._visible)
        item.update ()
        
    def remove (self, item):
        index = self.indexOf (item)
        if index >= 0:
            del self._items [index]

    def bringToFront (self):
        self.setZValue (max ([self._collection [name].zValue () for name in self._collection]) + 1.0)

