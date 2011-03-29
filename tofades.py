#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Awesome tofades
"""

tofades = [
    ("Ho ho ho"),
    ("Hô hô hô"),
    ("Hô ho hooo"),
    ("ho ho HO"),
    ("Et toi, tu suces ?"),
    ("Appelle-moi papa !")
]

if __name__ == "__main__":
    from bot import InnocentHand
    tof = InnocentHand(tofades)
    print tof()
    print tof(1)
