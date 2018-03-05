import random, math, time, binascii, hashlib
import numpy as np
from charm.toolbox.pairinggroup import ZR, G1, GT, pair
import myToolBox
from head import group, g

class ZhuScheme:
    def __init__(self, blockNum, segNum):
        self._blockNum = blockNum
        self._segmentNum = segNum
        self._blockSize = segNum * 20 #(a segment size is 20 bytes)

        self.clientOmigas = []
        self._tags = []
        self.CSPOmigas = []
        self.thetas = []

        self.group = group
        self.g = g
        self._alpha = self.group.random(ZR)
        self._beta = self.group.random(ZR)
        self.h = self.group.random(G1)
        self.H1 = self.h ** self._alpha
        self.H2 = self.h ** self._beta


        self.fileName = myToolBox.GenRandomSerial(8).encode()
        self.hfname = hashlib.sha256(self.fileName).hexdigest()
        self.Us = []
        self._verInfo = []

    def TagGen(self):
        us = []
        tau = []
        self._verInfo = np.asarray([myToolBox.GenRandomSerial(8) for i in range(self._blockNum)])

        for j in range(self._segmentNum):
            tau.append(self.group.random(ZR))
            us.append(self.g ** tau[j])
        self.Us = us

        signatures = list()
        for i in range(self._blockNum):
            f = open('/home/ty/workspace_for_py/AllSchemeTestData/test0', 'rb')# test0 is the name of test file
            f.seek(i * blockSize, 0)
            blockBytes = f.read(self._blockSize)
            f.close()

            mi = self.group.init(ZR, 0)
            for j in range(self._segmentNum):
                mij = blockBytes[20*j:20*(j+1)]
                mij = int(binascii.hexlify(mij), 16)
                mij = self.group.init(ZR, mij)
                mij = tau[j] * mij * self._beta
                mi += mij

            hwi = self.hfname + self._verInfo[i]
            sig = (self.group.hash(hwi, G1) ** self._alpha) * (self.g ** mi )
            signatures.append(sig)

        self._tags = signatures

    def Challenge(self, CNum):
        assert CNum > 0
        assert CNum < self._blockNum

        chal = dict()

        selectBlockSet = myToolBox.getUniqueRandomNum(self._blockNum, CNum)

        chal = {i : self.group.random(ZR) for i in selectBlockSet}

        return chal

    def Commitment(self):
        commit = dict()
        self.gamma = self.group.random(ZR)
        self.Lambda = [self.group.random(ZR) for j in range(self._segmentNum)]

        left = self.group.init(G1, 1)
        for j in range(self._segmentNum):
            temp = self.Us[j] ** self.Lambda[j]
            left *= temp

        Pi = self.group.pair_prod(left, self.H2)

        commit['H'] = self.H1 ** self.gamma
        commit['pi'] = Pi

        return commit

    def Proof(self, chal):
        assert isinstance(chal, dict)

        proof = dict()
        sigma = self.group.init(G1, 1)
        mus = []

        for i in chal.keys():
            sigma *= self._tags[i] ** (self.gamma * chal[i])

        for j in range(self._segmentNum):
            mj = self.group.init(ZR, 0)
            for i in chal.keys():
                f = open('/home/ty/workspace_for_py/AllSchemeTestData/test0', 'rb')
                f.seek(i * blockSize, 0)
                blockBytes = f.read(self._blockSize)
                f.close()

                mij = blockBytes[20*j:20*(j+1)]
                mij = int(binascii.hexlify(mij), 16)
                mij = self.group.init(ZR, mij)

                mj += mij * chal[i]

            mus.append(self.Lambda[j] + (self.gamma * mj))


        proof['sigma'] = sigma
        proof['mu'] = mus

        return proof

    def Verify(self, chal, commit, proof):
        assert isinstance(proof, dict)
        assert isinstance(commit, dict)
        assert isinstance(chal, dict)

        lhs = commit['pi'] * self.group.pair_prod(proof['sigma'], self.h)

        right1 = self.group.init(G1, 1)
        for i in chal.keys():
            hwi = self.hfname + self._verInfo[i]
            right1 *= self.group.hash(hwi, G1) ** chal[i]

        right2 = self.group.init(G1, 1)
        for j in range(self._segmentNum):
            right2 *= self.Us[j] ** proof['mu'][j]

        rhs = self.group.pair_prod(right1, commit['H']) * \
              self.group.pair_prod(right2, self.H2)

        return lhs == rhs


if __name__ == '__main__':

    t0 = time.perf_counter()
    testCase = ZhuScheme(10, 50)
    t1 = time.perf_counter()
    print('Initialize time :', (t1 - t0) * 1000, 'ms')

    t0 = time.perf_counter()
    testCase.TagGen()
    t1 = time.perf_counter()
    print('TagGen time :', (t1 - t0) * 1000, 'ms')

    t0 = time.perf_counter()
    commit = testCase.Commitment()
    t1 = time.perf_counter()
    print('Commitment time :', (t1 - t0) * 1000, 'ms')

    t0 = time.perf_counter()
    chal = testCase.Challenge(6)
    t1 = time.perf_counter()
    print('Challenge time :', (t1 - t0) * 1000, 'ms')

    t0 = time.perf_counter()
    proof = testCase.Proof(chal)
    t1 = time.perf_counter()
    print('Proof time :', (t1 - t0) * 1000, 'ms')

    t0 = time.perf_counter()
    result = testCase.Verify(chal, commit, proof)
    t1 = time.perf_counter()
    print('Verification time :', (t1 - t0) * 1000, 'ms')

    print(result)

