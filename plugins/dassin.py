# -*- coding: utf-8 -*-
from toflib import Plugin

class PluginDassin(Plugin):

    def handle_msg(self, msg_text, chan, nick):
        ete =  [ "tu sais"
               , "je n'ai jamais été aussi heureux que ce matin-là"
               , "nous marchions sur une plage"
               , "un peu comme celle-ci"
               , "c'était l'automne"
               , "un automne où il faisait beau"
               , "une saison qui n'existe que dans le nord de l'amérique"
               , "là-bas on l'appelle l'été indien"
               , "mais c'était tout simplement le nôtre"
               , "avec ta robe longue"
               , "tu ressemblais à une aquarelle de marie laurencin"
               , "et je me souviens"
               , "je me souviens très bien de ce que je t'ai dit ce matin-là"
               , "il y a un an"
               , "il y a un siècle"
               , "il y a une éternité"
               , "on ira"
               , "où tu voudras, quand tu voudras"
               , "et l'on s'aimera encore"
               , "lorsque l'amour sera mort"
               , "toute la vie"
               , "sera pareille à ce matin"
               , "aux couleurs de l'été indien"
               ]
        colline = [ "je l'ai vue près d'un laurier"
                  , "elle gardait ses blanches brebis"
                  , "quand j'ai demandé d'où venait sa peau fraîche elle m'a dit"
                  , "c'est de rouler dans la rosée qui rend les bergères jolies"
                  , "mais quand j'ai dit qu'avec elle"
                  , "je voudrais y rouler aussi"
                  , "elle m'a dit"
                  , "elle m'a dit d'aller siffler là-haut sur la colline"
                  , "de l'attendre avec un petit bouquet d'églantines"
                  , "j'ai cueilli des fleurs"
                  , "et j'ai sifflé tant que j'ai pu"
                  , "j'ai attendu, attendu"
                  , "elle n'est jamais venue"
                  , "zay zay zay zay"
                  ]

        songs = [ete, colline]

        for song in songs:
            try:
                i = song.index(msg_text)
                self.say(song[i+1])
                break
            except:
                pass
