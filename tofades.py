#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Awesome tofades
"""

tofades = [
    ("alcoolique !"),
    ("soulak !"),
    ("bois un canon !"),
    ("tu viens boire un canon ?"),
    (";)"),
    ("t'es saoul ;)'")
]

if __name__ == "__main__":
    from bot import InnocentHand
    tof = InnocentHand(tofades)
    print tof()
    print tof(1)
