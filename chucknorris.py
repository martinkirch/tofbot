#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Awesome chuck norris facts
"""


chuckNorrisFacts = [
    ("Chuck norris est tellement fort qu'il peut applaudir d'une seule main"),
    ("Il n'y a que sur Google qu'on peut taper Chuck Norris"),
    ("Chuck Norris a déjà compté jusqu'à l'infini. Deux fois."),
    ("Certaines personnes portent un pyjama Superman. Superman porte un pyjama Chuck Norris."),
    ("Chuck Norris donne fréquemment du sang à la Croix-Rouge. Mais jamais le sien."),
    ("Chuck Norris ne se mouille pas, c'est l'eau qui se Chuck Norris."),
    ("Chuck Norris et Superman ont fait un bras de fer, le perdant devait mettre son slip par dessus son pantalon."),
    ("Chuck Norris peut gagner une partie de puissance 4 en trois coups."),
    ("Le dernier homme a avoir serré la main à Chuck est Jamel Debbouze."),
    ("Jesus Christ est né en 1940 avant Chuck Norris."),
    ("Chuck Norris ne porte pas de montre. Il décide de l'heure qu'il est."),
    ("La seule chose qui arrive à la cheville de Chuck Norris... c'est sa chaussette."),
    ("Un jour, Chuck Norris a perdu son alliance. Depuis c'est le bordel dans les terres du milieu..."),
    ("Chuck Norris fait pleurer les oignons."),
    ("Dieu a dit: que la lumiere soit! et Chuck Norris répondit : On dit s'il vous plait."),
    ("Chuck Norris peut diviser par zéro."),
    ("Chuck Norris comprend Jean-Claude Van Damme."),
    ("Quand Google ne trouve pas quelque chose, il demande à Chuck Norris."),
    ("Chuck Norris sait parler le braille."),
    ("Chuck Norris joue à la roulette russe avec un chargeur plein."),
    ("Chuck Norris a un jour avalé un paquet entier de somnifères. Il a cligné des yeux."),
    ("Les suisses ne sont pas neutres, ils attendent de savoir de quel coté Chuck Norris se situe."),
    ("Il n'y a pas de théorie de l'évolution. Juste une liste d'espèces que Chuck Norris autorise à survivre."),
    ("Chuck Norris a déjà été sur Mars, c'est pour cela qu'il n'y a pas de signes de vie là bas."),
    ("Chuck Norris est la raison pour laquelle Charlie se cache."),
    ("Chuck Norris mesure son pouls sur l'échelle de Richter."),
    ("Un jour, au restaurant, Chuck Norris a commandé un steak. Et le steak a obéi."),
    ("Dans une pièce normale, il y a en moyenne 1242 objets avec lesquels Chuck Norris peut vous tuer, en incluant la pièce elle même."),
    ("Chuck Norris connait la dernière décimale de Pi."),
    ("Si Chuck Norris avait été pris dans le film \"300\" il l'aurait renommé en \"1\"."),
    ("Pour certains hommes le testicule gauche est plus large que le testicule droit, chez Chuck Norris, chaque testicule est plus large que l'autre."),
]

# tester
if __name__ == "__main__":
    from bot import InnocentHand
    facts = InnocentHand(chuckNorrisFacts)
    print facts()
    print facts(1)
