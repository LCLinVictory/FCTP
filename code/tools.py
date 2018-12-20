# -*- coding: utf-8 -*-
"""
Created on Sat Dec 01 21:52:18 2018

@author: LCL
"""

from __future__ import division # for / and //
#from collections import Counter # for merge dict

'''
https://blog.csdn.net/fred1653/article/details/51255530 
'''
class TrieNode(object):
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.data = {}
        self.is_leaf = False
        self.is_bound = False
        self.parent = None

class Trie(object):
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for letter in word:
            child = node.data.get(letter)
            if not child:
                node.data[letter] = TrieNode()
                node.data[letter].parent = node
            node = node.data[letter]
        node.is_leaf = True

    def search(self, downbound, upbound):
        if int(upbound) < int(downbound):
            return -1
        
        upnode = self.root
        for item in upbound:
            upnode = upnode.data.get(item)
            upnode.is_bound = True
            if not upnode:
                return -1
        upnode_cpoy = upnode
        
        downnode = self.root
        for item in downbound:
            downnode = downnode.data.get(item)
            downnode.is_bound = True
            if not downnode:
                return -1
        downnode_copy = downnode
        
        convergenode = upnode
        tmpup = upnode
        tmpdown = downnode
        while convergenode != self.root:    # !
            tmpup = tmpup.parent
            tmpdown = tmpdown.parent
            if tmpup == tmpdown:
                convergenode = tmpup
                break
        
        downprefix = []
        rchildfirst = False
        if downnode.is_leaf == True:
            if downnode.parent.data['0'] == downnode:
                downprefix.append('*')
            else:
                downprefix.append('1')
                rchildfirst = True
            downnode = downnode.parent
            while downnode != convergenode:
                if downnode.parent.data['1'] == downnode:
                    for i in range(len(downprefix)):
                        downprefix[i] = '1' + downprefix[i]
                    rchildfirst = True
                else:
                    if rchildfirst == True:
                        for i in range(len(downprefix)):
                            downprefix[i] = '0' + downprefix[i]
                        if downnode.parent.data['1'].is_bound == False:
                            downprefix.append('1' + (len(downprefix[0]) - 1)*'*')
                    else:
                        for i in range(len(downprefix)):
                            if downnode.parent.data['1'].is_bound == False:
                                downprefix[i] = '*' + downprefix[i]
                            else:
                                downprefix[i] = '0' + downprefix[i]
                downnode = downnode.parent
        #print('downprefix:', downprefix)
        upprefix = []
        lchildfirst = False
        if upnode.is_leaf == True and upnode.parent != convergenode:
            if upnode.parent.data['1'] == upnode:
                upprefix.append('*')
            else:
                upprefix.append('0')
                lchildfirst = True
            upnode = upnode.parent
            while upnode != convergenode:
                if upnode.parent.data['0'] == upnode:
                    for i in range(len(upprefix)):
                        upprefix[i] = '0' + upprefix[i]
                    lchildfirst = True
                else:
                    if lchildfirst == True:
                        for i in range(len(upprefix)):
                            upprefix[i] = '1' + upprefix[i]
                        if upnode.parent.data['0'].is_bound == False:
                            upprefix.append('0' + (len(upprefix[0]) - 1)*'*')
                    else:
                        for i in range(len(upprefix)):
                            if upnode.parent.data['0'].is_bound == False:
                                upprefix[i] = '*' + upprefix[i]
                            else:
                                upprefix[i] = '1' + upprefix[i]
                upnode = upnode.parent
        #print('upprefix:', upprefix)
        while upnode_cpoy != convergenode:
            downnode_copy.is_bound = False
            downnode_copy = downnode_copy.parent
            upnode_cpoy.is_bound = False
            upnode_cpoy = upnode_cpoy.parent
        
        prefixList = downprefix + upprefix
        while convergenode != self.root:
            if convergenode.parent.data['0'] == convergenode:
                tmpchr = '0'
            else:
                tmpchr = '1'
            for i in range(len(prefixList)):
                prefixList[i] = tmpchr + prefixList[i]
            convergenode.is_bound = False
            convergenode = convergenode.parent
        
        return prefixList

def int2binary(bitlen, number):
    return (bitlen - len(bin(number)[2:]))*'0' + bin(number)[2:]

def addr2dec(addr):
    "将点分十进制IP地址转换成十进制整数"
    items = [int(x) for x in addr.split(".")]
    return sum([items[i] << [24, 16, 8, 0][i] for i in range(4)])
 
def dec2addr(dec):
    "将十进制整数IP转换成点分十进制的字符串IP地址"
    return ".".join([str(dec >> x & 0xff) for x in [24, 16, 8, 0]])

def Init(FileName):
    trie = Trie()
    BitLen = 16
    for i in range(pow(2, BitLen)):
        string = int2binary(BitLen, i)
        trie.insert(string)
    
    f = open('../data/'+FileName, 'r')
    line = f.readline()
    RID = 0
    RuleList = []
    linenum = 1
    while line:
        tmpList = line.split('\t')[:-1]
        sa, saprefix = tmpList[0][1:].split('/')
        saprefix = int(saprefix)
        tmpstr = bin(addr2dec(sa))[2:]
        sa = (32 - len(tmpstr))*'0' + tmpstr
        sa = sa[:saprefix] + (32 - saprefix)*'*'
        
        da, daprefix = tmpList[1].split('/')
        daprefix = int(daprefix)
        tmpstr = bin(addr2dec(da))[2:]
        da = (32 - len(tmpstr))*'0' + tmpstr
        da = da[:daprefix] + (32 - daprefix)*'*'
        
        spl, sph = tmpList[2].split(' : ')
        if spl == sph:
            spList = [int2binary(16, int(sph))]
        elif sph == '65535' and spl == '0':
            spList = [16 * '*']
        else:
            #   Range
            spList = trie.search(int2binary(BitLen, int(spl)), int2binary(BitLen, int(sph)))
            spList = list(set(spList))
            
        dpl, dph = tmpList[3].split(' : ')
        if dpl == dph:
            dpList = [int2binary(16, int(dph))]
        elif dph == '65535' and dpl == '0':
            dpList = [16 * '*']
        else:
            #   Range
            dpList = trie.search(int2binary(BitLen, int(dpl)), int2binary(BitLen, int(dph)))
            dpList = list(set(dpList))
            
        prtcl, prtclprefix = tmpList[4][2:].split('/')
        if cmp(prtclprefix, '0x00') == 0:   # wildcard
            prtcl = 8 * '*'
        else:    
            tmpstr = bin(int(prtcl, 16))[2:]
            prtcl = (8 - len(tmpstr))*'0' + tmpstr
        
        for spitem in spList:
            for dpitem in dpList:
                RuleList.append([RID, sa, da, spitem, dpitem, prtcl])
                RID += 1
        line = f.readline()
        linenum += 1
    f.close()
    
    return (RuleList, linenum)  # RuleList[i] = [RID, sa, da, sp, dp, prtcl], linenum is real rule numbers