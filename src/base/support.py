# -*- coding: utf-8 -*-

def enum (*seq, **named):
    enums = dict (zip (seq, xrange (len (seq))), **named)
    return type ('Enum', (), enums)

def xfrange (start, stop, step = 1.0):
    while start < stop:
        yield start
        start += step
