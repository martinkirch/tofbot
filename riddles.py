#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Awesome riddles
"""

riddles = [
    ("Tu connais l'histoire de Toto au toilettes?", "Ben moi non plus"),
    ("Où est charlie?", "Sur ta mère"),
    ("Qu'est-ce qui est vert, qui vit sous terre, et qui mange des pierres ?", "Le mange cailloux"),
    ("Pourquoi les Américains ne voient-ils pas le bout du tunnel ?", "Parce que George Bush."),
    ("La petite fille tombe de la balançoire. Pourquoi ?", "Parce qu'elle n'a pas de bras."),
    ("Pourquoi les Spices Girls mouillent ?" , "Parce que les boys band!"),
    
]

if __name__ == "__main__":
    from bot import InnocentHand
    joker = InnocentHand(riddles)
    print joker()
    print joker(1)
