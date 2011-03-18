#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Awesome jokes
"""

jokes = [
    ("Voici l'histoire de Toto aux toilettes..."),
    ("Une autre histoire")
]

if __name__ == "__main__":
    from bot import InnocentHand
    joker = InnocentHand(jokes)
    print joker()
    print joker(1)
