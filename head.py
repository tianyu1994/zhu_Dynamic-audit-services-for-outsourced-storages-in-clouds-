'''
this python file for sharing

the PairingGroup:group,
pulblic key:g,
CSP's secret key:sk
'''

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, GT, pair

group = PairingGroup('SS512')
g = group.random(G1)
sk = group.random(ZR)#CSP secret key

# some params in tian's scheme
tian_r = group.random(ZR)

# read blocksize for one time
blockSize = 128*1000#bytes



segmentNum = 200
blockNumber= 50000          #62500
trialsNumber = 20

