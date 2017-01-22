#!/usr/bin/python3

import pitch,player

p = pitch.Pitch()
pl = player.Player('josh')
pl1 = player.Player('zeezey')
pl2 = player.Player('JMapes')

p.players.append(pl)
p.players.append(pl1)
p.players.append(pl2)

p.shuffleDeck()
p.deal()
p.showTable()
p.bettingRound()
p.flop()
p.showTable()
p.bettingRound()
p.turnRiver()
p.showTable()
p.bettingRound()
p.turnRiver()
p.showTable()
p.bettingRound()
p.finishHand()

for pi in p.players:
  print(pi.name+'\n\n')
  for k,v in pi.__dict__.items():
    print(' '+k+' ==> '+str(v))
  print('\n')
