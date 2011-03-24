#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Awesome jokes
"""

jokes = [
    ("C'est toto qui monte dans le bus, il ne fait que chanter et le chauffeur en a mare... Toto chante : \" si ma mere était une poule et mon pere un coq moi je serais un poussin\", \"si ma mere était une vache et mon pere un taureau moi je serai un veau\". Le chauffeur de bus est vraiment enervé et lui dit : \"et si ta mere était une putain et ton pere un pédé tu serai quoi ?\", toto lui repond : \"bin je serais chauffeur de bus\" ! "),
    ("""Un singe rentre dans un bar et demande au barmann
- Vous avez des bananes ?
- Non on n'a pas de bananes.
- Vous avez des bananes ?
- Non on n'en n'a pas.
- Vous avez des bananes ?
- Non, t'es sourd ou quoi !! Si tu me demandes encore si j'ai des bananes je te cloue la langue au comptoir !!!!
- Vous avez des clous ?
- Non.
- Vous avez des bananes ?"""),
	("""C'est toto à l'ecole. La maitresse entend un miaulement et dit "qui a amené un chat ici?!" toto lui repond d'une voix douce
- c'est moi madame
- et pourqoi ça toto ?
- ben mon papa il a dit a maman "quand le petit part je te boufe la chatte" """),
    ("""Un enfant de huit ans entend des bruits venant de la chambre de sa maman... Celui-ci s'approche pour voir et voit sa mère se touchant en s'écriant "je veux un homme ,je veux un homme!".
L'enfant retourne dans sa chambre. Le lendemain il entend le même bruit et là il s'aperçoit qu il y a un homme sur sa mère! Il court vite dans sa chambre, baisse son pantalon, se touche le kiki en s'écriant "je veux un vélo bleu, je veux un vélo bleu." """),
    ("""C'est 2 amis qui parlent ensemble :
- dis donc Roger ta femme ne porte pas de culotte !
- Mais Marcel comment le sais tu?
- C'est mon petit doigt qui me la dit. """),
    ("Un prête catholique s'est perdu en visitant la jungle et se retrouve nez à nez avec un lion. Effrayé, il dit : « bon Dieu ! Faites que ce lion devienne chrétien ». Et le miracle s'accomplit... Le lion s'agenouille et dit : «Seigneur bénissez ce repas!»."),
    ("""Deux ivrognes sont pris dans une avalanche. Un St-Bernard vient vers eux pour les sauver.
L'un des deux ivrognes dit : "Le meilleur ami de l'homme vient à notre secours!"
L'autre répond : " Oui et il vient avec un chien." """),
]

if __name__ == "__main__":
    from bot import InnocentHand
    joker = InnocentHand(jokes)
    print joker()
    print joker(1)
