'''
this python file for sharing

the PairingGroup:group;
pulblic key:g;
'''

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, GT, pair

group = PairingGroup('SS512')
g = group.random(G1)
