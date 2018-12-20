# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 21:10:00 2018

@author: LCL
"""

from __future__ import division # for / and //
from collections import Counter # for merge dict
from itertools import permutations    # for N! permutations
import numpy as np
from tools import Init  # call Init function

def HashIdxPrefix(string):
    idxFlag = 0     # 0 is exact, -1 is wildcard, else is prefix
    if '*' not in string:
        idxFlag = 0
        return ([string], idxFlag)
    if string == '*'*len(string):
        idxFlag = -1
        return ([], idxFlag)
        #return ([(len(string) - len(bin(i)[2:]))*'0' + bin(i)[2:] for i in range(pow(2, len(string)))], idxFlag)
    # 修改HashIdx，同时(或者) 将findP_NP函数中调用提前，预先准备
    idxFlag = string.find('*')
    return ([string[:idxFlag] + bin(i)[2:] for i in range(pow(2, len(string[idxFlag:])))], idxFlag)
#print HashIdxPrefix('*'*12)

##  Range-to-prefix TEST
#trie = Trie()
#BitLen = 16
#for i in range(pow(2, BitLen)):
#    string = int2binary(BitLen, i)
#    trie.insert(string)
#range_to_prefixList = trie.search(int2binary(BitLen, 0), int2binary(BitLen, 11))
#range_to_prefixList = list(set(range_to_prefixList))
#Num = 0
#for item in range_to_prefixList:
#    Num += len(HashIdxPrefix(item)[0])
#print Num

def FindP_Np(FieldList, L, N, RulepDicOld):
    global hashidxListLen, Num
    NpDic = {}
    MemDic = {}
    for p in range(1, L):
        Table = {}
        wildcardNum = 0
        for n in range(0, N):
            Num = n
            if (RulepDicOld == {})or (FieldList[n][0] in RulepDicOld.keys()) :
                hashidxList, idxFlag = HashIdxPrefix(FieldList[n][1][:p])
                hashidxListLen = len(hashidxList)
                #if len(hashidxList) == 65536:   #   1****************, 0****************
                #    print(FieldList[n][1][:p])
                if idxFlag == -1:   # wildcard
                    wildcardNum += 1
                else:
                    #   https://www.cnblogs.com/fh-fendou/p/7515775.html
                    tmpTable = dict(zip(hashidxList, [1]*len(hashidxList)))
                    #   https://www.cnblogs.com/zhaoyingjie/p/8559592.html
                    Table = dict(Counter(Table)+Counter(tmpTable))
        if Table == {}:
            NpDic[p] = ('*'*p, N)
        else:
            idx = max(Table, key=Table.get)
            NpDic[p] = (idx, Table[idx] + wildcardNum)
        MemDic[p] = p*NpDic[p][1]   
        print('p = ', p)
    #print NpDic
    p = max(MemDic, key=MemDic.get)
    idx = NpDic[p][0]
    
    RulepDicNew = {}
    '''
    for n in range(0, N):
        if (RulepDicOld == {})or (FieldList[n][0] in RulepDicOld.keys()) :
            hashidxList = HashIdxPrefix(FieldList[n][1][:p])[0]
            if idx in hashidxList:
                RulepDicNew[FieldList[n][0]] = 0
    '''
    return (p, MemDic[p], idx, NpDic[p][1], NpDic, RulepDicNew)

def FindP_Np_wildcard(FieldList, Lm, N, RulepDicOld):    #FieldList[i] <- [RID, FieldValue, wildcardPosition]
    NpDic = {}
    MemDic = {}
    for p in range(1, Lm+1):
        NpDic[p] = [0, {}]
        MemDic[p] = 0
    
    for p in range(1, Lm+1):
        for n in range(0, N):
            if (RulepDicOld == {})or (FieldList[n][0] in RulepDicOld.keys()) :
                RID = FieldList[n][0]
                wildcardPosition = FieldList[n][2]
                if wildcardPosition != -1 and wildcardPosition <= Lm-p:    
                    NpDic[p][0] += 1
                    NpDic[p][1][RID] = 0
        if NpDic[p][0] != len(NpDic[p][1]):
            print('Error')
        MemDic[p] = p*NpDic[p][0]
    p = max(MemDic, key=MemDic.get)
    return (p, NpDic[p][0], MemDic, NpDic[p][1])

def MaxCompressedPresent(FieldInfoList, FileList):
    ResultList = []
    for m in range(len(FileList)):
        RuleList, linenum = Init(FileList[m]) # [RID, sa, da, sp, dp, prtcl]
        N = len(RuleList)
        M = 0
        for n in range(len(FieldInfoList)):
            for i in range(N):
                wildcardFlag = RuleList[i][n+1].find('*')
                if wildcardFlag != -1:
                    M += len(RuleList[i][n+1]) - wildcardFlag
        ResultList.append((FileList[m], M / (104 * N)))
    return ResultList

'''
##  Find last p bit wildcard of Field_m --> Combination    ####################
'''

def CountWildcardMatrix(AllFieldList, L, N, stride_s, cluster_n):   # AllFieldList[i] <- L-bit, len(AllFieldList) <- N 
    wildcardMatrixCount = 0
    for n in range(0, N-(N%cluster_n), cluster_n):
        for j in range(0, L-(L%stride_s), stride_s):
            tmpwildcardMatrixFlag = True
            for i in range(0, cluster_n):
                if cmp(AllFieldList[n + i][j:j+stride_s], '*'*stride_s) != 0:
                    tmpwildcardMatrixFlag = False
                    break
            if tmpwildcardMatrixFlag == True:
                wildcardMatrixCount += 1
    return wildcardMatrixCount

def CombinationFind(RuleList, N, FieldInfoList, foundFieldDic, RulepDicOld, stride_s, cluster_n):
    tmpFieldList = []
    tmpNumList = []
    tmpresult = []
    for n in range(len(FieldInfoList)):
        if n not in foundFieldDic.keys():
            FieldList = []  #FieldList[i] <- [RID, FieldValue, wildcardPosition]
            for i in range(N):
                if (RulepDicOld == {}) or (RuleList[i][0] in RulepDicOld.keys()):
                    wildcardFlag = RuleList[i][n+1].find('*')
                    FieldList.append([RuleList[i][0], RuleList[i][n+1], wildcardFlag])
            Lm = FieldInfoList[n][1]
            p, Np, MemDic, RulepDic =  FindP_Np_wildcard(FieldList, Lm, len(FieldList), {})
            tmpresult.append((Lm, FieldInfoList[n][0], (p*Np) / (104*N), p, Np))  # 104 is five-tuple bit length
            tmpNumList.append((p*Np) // (stride_s*cluster_n))     # Greedy choice way, or: (p*Np) // (stride_s*cluster_n)
            tmpFieldList.append([n, RulepDic])
            #print('n = ', n)
    maxidx = tmpNumList.index(max(tmpNumList))
    foundFieldDicNew = foundFieldDic
    RulepDicNew = {}   # IF p<stride_s or Np<cluster_n
    tmpresultItem = ()
    if tmpresult[maxidx][-2] >= stride_s and tmpresult[maxidx][-1] >= cluster_n :
        maxfield = tmpFieldList[maxidx][0]
        RulepDicNew = tmpFieldList[maxidx][1]
        #print('maxfield = ', maxfield)
        #print tmpresult[maxidx]
        
        tmpTable = dict(zip([maxfield], [1]))
        foundFieldDicNew = dict(Counter(foundFieldDic)+Counter(tmpTable))
        tmpresultItem = tmpresult[maxidx]
    
    return (foundFieldDicNew, RulepDicNew, tmpresultItem)

def CombinationHorizontal(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n):
    ResultList = []
    RIDOrderList = []
    
    for m in range(len(FileList)):
        RuleList, linenum = Init(FileList[m]) # RuleList[i] <- [RID, sa, da, sp, dp, prtcl]
        #L = 104
        N = len(RuleList)
        CombinationResult = []
        AllRuleSet = set([item[0] for item in RuleList])   # Init: all RID
        
        foundFieldDic = {}
        RulepDicOld = {}
        for c in range(CombinationNum):
            foundFieldDicNew, RulepDicNew, tmpresultItem = CombinationFind(RuleList, N, FieldInfoList, foundFieldDic, RulepDicOld, stride_s, cluster_n) # tmpresultItem <- (Lm, FieldName, p*Np / 104*N, p, Np)
            if RulepDicNew == {} :
                break
            foundFieldDic = foundFieldDicNew
            RulepDicOld = RulepDicNew   #!!!
            #print foundFieldDic
            CombinationResult.append((tuple(RulepDicNew.keys()), tmpresultItem))
        
        M = 0
        tmpResultDic = {}
        tmpRIDOrderDic = {}
        RuleElseList = list(AllRuleSet - set(CombinationResult[0]))
        RuleElseList.sort()
        tmplist = []
        #print('RuleElseList', len(RuleElseList))
        for c in range(len(CombinationResult)):
            tmplist = list(CombinationResult[c][0])
            tmplist.sort()
            M = 0
            for cr in range(c, 0, -1):
                tmplt = list(set(CombinationResult[cr-1][0]) - set(CombinationResult[cr][0]))
                tmplt.sort()
                tmplist += tmplt
                tmpNum = CombinationResult[cr][1][-1]
                tmpLen = CombinationResult[cr][1][-2]
                M += (tmpLen - tmpLen%stride_s) * (tmpNum - tmpNum%cluster_n)       # each field length of five-tuple is a power of 2, find wildcard-PE from behind
            tmpNum = CombinationResult[0][1][-1]
            tmpLen = CombinationResult[0][1][-2]
            M += (tmpLen - tmpLen%stride_s) * (tmpNum - tmpNum%cluster_n) 
            tmplist += RuleElseList     # current RID order for c
            '''
            #tmpAllFieldList = [''.join(RuleList[n][1:]) for n in tmplist]
            ##print('tmpAllFieldList', len(tmpAllFieldList), N)
            #wildcardMatrixCount = CountWildcardMatrix(tmpAllFieldList, L, len(tmpAllFieldList), stride_s, cluster_n)
            ##print('wildcardMatrixCount', wildcardMatrixCount)
            #M = wildcardMatrixCount * stride_s * cluster_n
            '''
            tmpResultDic[c] = M / (104*N)
            tmpRIDOrderDic[c] = tmplist
        for c in range(len(CombinationResult), CombinationNum):
            tmpResultDic[c] = M / (104*N)
            tmpRIDOrderDic[c] = tmplist
        print('Horizontal',FileList[m],M / (104*N))
        #print(tmpResultDic)
        ResultList.append(tmpResultDic)
        RIDOrderList.append(tmpRIDOrderDic)
    return (ResultList, RIDOrderList)

def CombinationVertical(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n):
    ResultList = []
    RIDOrderList = []
    
    for m in range(len(FileList)):
        RuleList, linenum = Init(FileList[m]) # RuleList[i] <- [RID, sa, da, sp, dp, prtcl]
        #L = 104
        N = len(RuleList)
        CombinationResult = []
        AllRuleSet = set([item[0] for item in RuleList])   # Init: all RID
        RuleElseSet = AllRuleSet
        
        RulepDicOld = {}
        
        foundFieldDic = {}
        RulepDicOld = {}
        for c in range(CombinationNum):
            foundFieldDicNew, RulepDicNew, tmpresultItem = CombinationFind(RuleList, N, FieldInfoList, foundFieldDic, RulepDicOld, stride_s, cluster_n) # tmpresultItem <- (Lm, FieldName, p*Np / 104*N, p, Np)
            if RulepDicNew == {} :
                break
            RuleElseSet = RuleElseSet - set(RulepDicNew)
            RulepDicOld = dict(zip(RuleElseSet, [1]*len(RuleElseSet)))
            CombinationResult.append((tuple(RulepDicNew.keys()), tmpresultItem))
            #print tmpresultItem
            if RulepDicOld == {} :
                break
        
        M = 0
        tmpResultDic = {}
        tmpRIDOrderDic = {}
        tmpList = []
        tmpcurrentlist = list(AllRuleSet)
        for c in range(len(CombinationResult)):
            # Order RID
            tmplt = list(CombinationResult[c][0])
            tmplt.sort()
            tmpList += tmplt
            tmplt = list(AllRuleSet - set(tmpList))
            tmplt.sort()
            tmpcurrentlist = tmpList + tmplt    # current RID order for c
            # Compute M
            tmpNum = CombinationResult[c][1][-1]
            tmpLen = CombinationResult[c][1][-2]
            M += (tmpLen - tmpLen%stride_s) * (tmpNum - tmpNum%cluster_n) 
            '''
            #tmpAllFieldList = [''.join(RuleList[n][1:]) for n in tmpcurrentlist]
            #wildcardMatrixCount = CountWildcardMatrix(tmpAllFieldList, L, N, stride_s, cluster_n)
            ##print('wildcardMatrixCount',wildcardMatrixCount)
            #M = wildcardMatrixCount * stride_s * cluster_n
            '''
            tmpResultDic[c] = M / (104*N)
            tmpRIDOrderDic[c] = tmpcurrentlist
        for c in range(len(CombinationResult), CombinationNum):
            tmpResultDic[c] = M / (104*N)
            tmpRIDOrderDic[c] = tmpcurrentlist
        print('Vertical', FileList[m],M / (104*N))
        ResultList.append(tmpResultDic)
        RIDOrderList.append(tmpRIDOrderDic)
    return (ResultList, RIDOrderList)
    
def CombinationMix(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n):
    ResultList = []
    RIDOrderList = []
    
    for m in range(len(FileList)):
        RuleList, linenum = Init(FileList[m]) # RuleList[i] <- [RID, sa, da, sp, dp, prtcl]
        #L = 104
        N = len(RuleList)
        v_CombinationResult = []
        AllRuleSet = set([item[0] for item in RuleList])   # Init: all RID
        RuleElseSet = AllRuleSet
        
        v_foundFieldDic = {}
        v_RulepDicOld = {}
        for cv in range(CombinationNum):
            v_foundFieldDicNew, v_RulepDicNew, v_tmpresultItem = CombinationFind(RuleList, N, FieldInfoList, v_foundFieldDic, v_RulepDicOld, stride_s, cluster_n)
            if v_RulepDicNew == {} :  # can not find field to compress
                break
            #------------------------------------------------------------------
            h_foundFieldDic = v_foundFieldDicNew
            h_RulepDicOld = v_RulepDicNew
            h_CombinationResult = [(tuple(v_RulepDicNew.keys()), v_tmpresultItem)]    # Add the first item
            for ch in range(CombinationNum - 1):
                h_foundFieldDicNew, h_RulepDicNew, h_tmpresultItem = CombinationFind(RuleList, N, FieldInfoList, h_foundFieldDic, h_RulepDicOld, stride_s, cluster_n)
                if h_RulepDicNew == {}: # can not find field to compress
                    break
                h_foundFieldDic = h_foundFieldDicNew
                h_RulepDicOld = h_RulepDicNew   #!!!
                h_CombinationResult.append((tuple(h_RulepDicNew.keys()), h_tmpresultItem)) # tmpresultItem <- (Lm, FieldName, p*Np / 104*N, p, Np)
                
            M = 0
            h_tmpResultDic = {}
            tmplist = []
            for ch in range(len(h_CombinationResult)):
                #'''
                FieldName = h_CombinationResult[ch][1][1]
                pNum = h_CombinationResult[ch][1][-1]
                pLen = h_CombinationResult[ch][1][-2]
                print(cv, ch, pLen, pNum, FieldName)
                #'''
                tmplist = list(h_CombinationResult[ch][0])
                tmplist.sort()
                M = 0
                for cr in range(ch, 0, -1):
                    tmplt = list(set(h_CombinationResult[cr-1][0]) - set(h_CombinationResult[cr][0]))
                    tmplt.sort()
                    tmplist += tmplt
                    tmpNum = h_CombinationResult[cr][1][-1]
                    tmpLen = h_CombinationResult[cr][1][-2]
                    M += (tmpLen - tmpLen%stride_s) * (tmpNum - tmpNum%cluster_n)       # each field length of five-tuple is a power of 2, find wildcard-PE from behind
                tmpNum = h_CombinationResult[0][1][-1]
                tmpLen = h_CombinationResult[0][1][-2]
                M += (tmpLen - tmpLen%stride_s) * (tmpNum - tmpNum%cluster_n) 
                h_tmpResultDic[ch] = (tuple(tmplist), M)
            for ch in range(len(h_CombinationResult), CombinationNum):
                h_tmpResultDic[ch] = (tuple(tmplist), M)
            #------------------------------------------------------------------
            RuleElseSet = RuleElseSet - set(v_RulepDicNew)
            v_RulepDicOld = dict(zip(RuleElseSet, [1]*len(RuleElseSet)))
            v_CombinationResult.append(h_tmpResultDic)
            if v_RulepDicOld == {} :
                break
        #print(v_CombinationResult)
        #print('len(v_CombinationResult)', len(v_CombinationResult))
        M = 0
        v_tmpResultDic = {}
        v_tmpRIDOrderDic = {}   # Need to Fix 2018.12.14
        tmpcurrentlist = list(AllRuleSet)
        for cv in range(len(v_CombinationResult)):
            # Order RID
            tmpList = []
            for cr in range(0, cv):
                tmpDic = v_CombinationResult[cr]
                tmplt = list(tmpDic[cv][0])  # has been sorted !
                tmpList += tmplt
            tmplt = list(AllRuleSet - set(tmpList))
            tmplt.sort()
            tmpcurrentlist = tmpList + tmplt
            # Compute M
            M = 0
            for cN in range(0, cv+1):
                M += v_CombinationResult[cN][cv][1]
            '''
            #tmpAllFieldList = [''.join(RuleList[n][1:]) for n in tmpcurrentlist]
            #wildcardMatrixCount = CountWildcardMatrix(tmpAllFieldList, L, N, stride_s, cluster_n)
            #print('wildcardMatrixCount',wildcardMatrixCount)
            #M = wildcardMatrixCount * stride_s * cluster_n
            '''
            v_tmpResultDic[cv] = M / (104*N)
            v_tmpRIDOrderDic[cv] = tuple(tmpcurrentlist)
        for cv in range(len(v_CombinationResult), CombinationNum):
            # Order RID
            tmpList = []
            for cr in range(0, len(v_CombinationResult)):
                tmpDic = v_CombinationResult[cr]
                tmplt = list(tmpDic[cv][0])  # has been sorted !
                tmpList += tmplt
            tmplt = list(AllRuleSet - set(tmpList))
            tmplt.sort()
            tmpcurrentlist = tmpList + tmplt
            # Compute M
            M = 0
            for cN in range(0, len(v_CombinationResult)):
                M += v_CombinationResult[cN][cv][1]
            v_tmpResultDic[cv] = M / (104*N)
            v_tmpRIDOrderDic[cv] = tuple(tmpcurrentlist)
        print('Mix', FileList[m],M / (104*N), len(tmpcurrentlist), N, N/linenum, len(v_CombinationResult))
        #print(v_tmpResultDic)
        ResultList.append(v_tmpResultDic)
        RIDOrderList.append(v_tmpRIDOrderDic)
    return (ResultList, RIDOrderList)

def Combination_ViolentSearch(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n):
    ResultList = []
    for m in range(len(FileList)):
        RuleList, linenum = Init(FileList[m]) # RuleList[i] <- [RID, sa, da, sp, dp, prtcl]
        L = 104     # five-tuple
        N = len(RuleList)
        
        if N < cluster_n:
            ResultList.append((FileList[m], 0.0, ()))
            continue
        
        tmpNList = np.arange(N).tolist()
        permutationList = list(permutations(tmpNList, N)) # N! kinds
        print('len(permutationList)', len(permutationList), N)
        MaxwildcardMatrixCount = 0
        maxItem = ()
        for Item in permutationList:
            tmpAllFieldList = [''.join(RuleList[n][1:]) for n in Item]
            wildcardMatrixCount = CountWildcardMatrix(tmpAllFieldList, L, N, stride_s, cluster_n)
            if MaxwildcardMatrixCount < wildcardMatrixCount:
                MaxwildcardMatrixCount = wildcardMatrixCount
                maxItem = Item
        M = MaxwildcardMatrixCount * stride_s *cluster_n
        ResultList.append((FileList[m], M / (104 * N), maxItem))
        print('maxItem',[''.join(RuleList[n][1:]) for n in maxItem])
        print('ViolentSearch', FileList[m],M / (104*N))
    return ResultList

def OrderRuleList(FieldInfoList, FileList, RIDOrderList, CombinationNum, stride_s, cluster_n):
    if len(FileList) != len(RIDOrderList):
        print('Error')
        return False
    for m in range(len(FileList)):
        RuleList, linenum = Init(FileList[m]) # RuleList[i] <- [RID, sa, da, sp, dp, prtcl]
        fw = open('Order_'+str(CombinationNum)+'_'+str(stride_s)+'_'+str(cluster_n)+FileList[m], 'w')
        for n in RIDOrderList[m][CombinationNum-1]:
            fw.write('\t'.join(RuleList[n][1:])+'\n')
        fw.close()
    return True

def CountResultRule(FieldInfoList, FileList, RIDOrderList, CombinationNum, stride_s, cluster_n):
    if len(FileList) != len(RIDOrderList):
        print('Error')
        return []
    CountResultList = []
    for m in range(len(FileList)):
        RuleList, linenum = Init(FileList[m]) # RuleList[i] <- [RID, sa, da, sp, dp, prtcl]
        L = 104     # five-tuple
        N = len(RuleList)
        
        OldAllFieldList = [''.join(RuleList[n][1:]) for n in range(N)]
        OldwildcardMatrixCount = CountWildcardMatrix(OldAllFieldList, L, N, stride_s, cluster_n)
        
        tmpAllFieldList = [''.join(RuleList[n][1:]) for n in RIDOrderList[m][CombinationNum-1]]
        wildcardMatrixCount = CountWildcardMatrix(tmpAllFieldList, L, N, stride_s, cluster_n)
        CountResultList.append((FileList[m], (wildcardMatrixCount*stride_s*cluster_n) / (104 * N), (OldwildcardMatrixCount*stride_s*cluster_n) / (104 * N)))
    return CountResultList