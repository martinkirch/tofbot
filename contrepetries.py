#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Awesome contrepetries
"""

contrepetries = [
      ("Salut Fred")
    , ("La programmeuse compile le C")
    , ("Personne n'est jamais assez fort pour ce calcul")
    , ("Elle aime le tenis en pension")
    , ("La Chine s'élève à l'approche des Nippons")
    , ("Il fait beau et chaud")
    , ("Elle revenait de la ferme pleine d'espoir jusqu'au pont du Juras")
]

if __name__ == "__main__":
    from bot import InnocentHand
    joker = InnocentHand(contrepetries)
    print joker()
    print joker(1)
