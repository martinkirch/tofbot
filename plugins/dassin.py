# -*- coding: utf-8 -*-
#
# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011 Etienne Millon <etienne.millon@gmail.com>
#                    Martin Kirchgessner <martin.kirch@gmail.com>
from toflib import Plugin
from toflib import distance

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
        
        # Rone - Bora (vocal edit, un texte d'Alain Damasio), texte redécoupé pour que ça toffe
        bora = [ "il n'y pas de secret",
                 "pas de secrets",
                 "il y a une vérité",
                 "simple, sobre, crue, quoi",
                 "la horde du contrevent",
                 "tu la réussiras uniquement si tu t'isoles",
                 "si tu t'isoles quoi",
                 "tu comprends ce que ça veut dire isole ?",
                 "isola",
                 "l'ile quoi",
                 "tu crées ton ile et tu l'effaces au maximum",
                 "il faut que les gens soient extrêmement loin de toi",
                 "mais loin parce que ton univers sera vaste",
                 "sera immense",
                 "sera énorme",
                 "énorme univers",
                 "énorme puissance d'univers",
                 "caracole il existe en toi complètement",
                 "comme strochnis",
                 "qu'il soit toi",
                 "que pietro della rocca tu le deviennes",
                 "et la croute aussi",
                 "et tous l'univers"
                 "et tout le vent",
                 "tu vis complètement la dedans",
                 "c'est ca qu'il faut",
                 "y a que ca qu'il faut",
                 "tu restes collé au vent",
                 "collé au vent",
                 "collé au vent, toi",
                 "et que tu te battes",
                 "que tu ne fasses aucune concessison sur le reste",
                 "tu oublies tout",
                 "t'es pas consultant, t'es rien",
                 "le consulting c'est d'la merde",
                 "la seule chose qui a d'la valeur",
                 "c'est quand t'es capable de faire un chapitre comme celui-là",
                 "ça, ça restera, ça mérite que tu vives",
                 "tu peux vivre pour écrire ça",
                 "ça mérite que tu vives",
                 "là t'es pas né pour rien",
                 "t'es nécessaire",
                 "t'es pas surnuméraire",
                 "t'es pas superflu",
                 "là t'as une nécessité quand t'écris ça",
                 "la nécessité d'être",
                 "et c'est ça qu'il faut tenir mec",
                 "c'est ça qu'il faut putain de tenir",
                 "lâches pas le morceau",
                 "t'fais pas enculer",
                 "t'fais pas disperser",
                 "t'fais pas fragmenter",
                 "fais pas de concession",
                 "y'a pas de concession avec la vie",
                 "y'a pas de concession",
                 "tu vis et faut vivre à fond"
                 ]
	
	oizo = ["coucou","tu veux voir ma bite ?"]

        songs = [oizo, ete, colline, bora]
        
        searched = msg_text.lower()
        minDist = 9999999
        best = False
        
        for song in songs:
            try:
                i = 0
                for line in song:
                    dist = distance(line, searched)
                    if dist < minDist:
                        best = song[i+1]
                        minDist = dist
                    i += 1
            except:
                pass
        
        if len(best) > 1 and minDist < (len(searched)/5):
            self.say(best)
