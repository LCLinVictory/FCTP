# -*- coding: utf-8 -*-
"""
Created on  2018

@author: LCL
"""

from __future__ import division # for / and //
from collections import Counter # for merge dict
import matplotlib.pyplot as plt

from tools import Init

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

hashidxListLen = 0
Num = 0
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
    
def FindP_Np_wildcard_ViolentSearch(FieldList, Lm, N, RulepDicOld):    #FieldList[i] <- [RID, FieldValue, wildcardPosition]
    return ()   # N!


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
###############################################################################
'''

#RuleList, linenum = Init("ACL1_10K") # [RID, sa, da, sp, dp, prtcl]
#N = len(RuleList)
#
#FieldList = []
#for i in range(N):
#    FieldList.append([RuleList[i][0], RuleList[i][3]])
#Num1 = 0
#RulepDicDP = {}
#for item in FieldList:
#    if item[1] != '*'*16:
#        Num1 += 1
#        RulepDicDP[item[0]] = 0
#        
#FieldList = []  #FieldList[i] <- [RID, FieldValue]
#for i in range(N):wildcardNum
#    FieldList.append([RuleList[i][0], RuleList[i][3]]) 
#L = 16
#p1, M1, idx1, Np1, NpDic1, RulepDic =  FindP_Np(FieldList, L, N, {})
#print (104*N - p1*Np1) / (104*N)  # 104 is five-tuple bit length


'''
##  Find first p bit of Field_n ###############################################
'''
#FieldInfoList = [('sa', 8), ('da', 8), ('sp', 16), ('dp', 16), ('prtcl', 8)]
#FieldInfoList = [('sa', 8)]
#ResultList = []
#FileList = ['ACL1_10K', 'ACL2_10K', 'ACL3_10K', 'ACL4_10K', 'ACL5_10K',\
#             'FW1_10K', 'FW2_10K', 'FW3_10K', 'FW4_10K', 'FW5_10K',\
#             'IPC1_10K', 'IPC2_10K']
#
#for m in range(len(FileList)):
#    RuleList, linenum = Init(FileList[m]) # [RID, sa, da, sp, dp, prtcl]
#    N = len(RuleList)
#    tmpresult = []
#    for n in range(len(FieldInfoList)):
#        FieldList = []  #FieldList[i] <- [RID, FieldValue, wildcardPosition]
#        for i in range(N):
#            wildcardFlag = RuleList[i][n+1].find('*')
#            FieldList.append([RuleList[i][0], RuleList[i][n+1], wildcardFlag])
#        L = FieldInfoList[n][1]
#        #for L in range(16, 20, 2):
#        p, M, idx, Np, NpDic, RulepDic =  FindP_Np(FieldList, L, N, {})#RulepDicSP)
#        tmpresult.append((L, FieldInfoList[n][0], (p*Np) / (104*N), idx))  # 104 is five-tuple bit length
#    ResultList.append((FileList[m], tmpresult))
#    print("m = ", m)
#
#f = open('Result.txt', 'w')
#for item in ResultList:
#    f.write(str(item) + '\n')
#f.close()

'''
##  Find last p bit wildcard of Field_m    ###################################
'''
#FieldInfoList = [('sa', 32), ('da', 32), ('sp', 16), ('dp', 16), ('prtcl', 8)]
##FieldInfoList = [('sa', 32)]
#ResultList = []
#FileList = ['ACL1_10K', 'ACL2_10K', 'ACL3_10K', 'ACL4_10K', 'ACL5_10K',\
#             'FW1_10K', 'FW2_10K', 'FW3_10K', 'FW4_10K', 'FW5_10K',\
#             'IPC1_10K', 'IPC2_10K']
#
#for m in range(len(FileList)):
#    RuleList, linenum = Init(FileList[m]) # [RID, sa, da, sp, dp, prtcl]
#    N = len(RuleList)
#    tmpresult = []
#    for n in range(len(FieldInfoList)):
#        FieldList = []  #FieldList[i] <- [RID, FieldValue, wildcardPosition]
#        for i in range(N):
#            wildcardFlag = RuleList[i][n+1].find('*')
#            FieldList.append([RuleList[i][0], RuleList[i][n+1], wildcardFlag])
#        Lm = FieldInfoList[n][1]
#        #for Lm in range(16, 20, 2):
#        p, Np, MemDic, RulepDic =  FindP_Np_wildcard(FieldList, Lm, N, {})#RulepDicSP)
#        tmpresult.append((Lm, FieldInfoList[n][0], (p*Np) / (104*N), p, Np))  # 104 is five-tuple bit length
#    ResultList.append((FileList[m], tmpresult))
#    print("m = ", m)
#
#f = open('Result.txt', 'w')
#for item in ResultList:
#    f.write(str(item) + '\n')
#f.close()
#
#
##   https://blog.csdn.net/liangzuojiayi/article/details/78187704 
#tmpcnames = ['royalblue', 'crimson', 'forestgreen', 'darkorchid', 'darkorange']
#plt.figure(figsize=(16,9))
#setwidth = 0.15
#for n in range(len(FieldInfoList)):
#    x = [i+1+n*setwidth for i in range(len(ResultList))]
#    y = []
#    for j in range(len(ResultList)):
#        tmpList = ResultList[j][1]
#        y.append(tmpList[n][2])
#    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n], edgecolor = 'white', label='$'+FieldInfoList[n][0].upper()+'$', lw=1)
#x = [i+1+(len(FieldInfoList) / 2)*setwidth for i in range(len(ResultList))]
#plt.xticks(x, ('ACL1', 'ACL2', 'ACL3', 'ACL4', 'ACL5', 'FW1', 'FW2', 'FW3', 'FW4', 'FW5', 'IPC1', 'IPC2'))
#plt.ylabel("Percent")
#plt.title('Field Compressed')
#plt.legend(loc='upper right') #'lower right') 'best')
#plt.legend()
#plt.show()

'''
##  Find last p bit wildcard of Field_m --> Combination    ####################
'''

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
            tmpNumList.append(p*Np)
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
    
    for m in range(len(FileList)):
        RuleList, linenum = Init(FileList[m]) # RuleList[i] <- [RID, sa, da, sp, dp, prtcl]
        N = len(RuleList)
        CombinationResult = []
        
        foundFieldDic = {}
        RulepDicOld = {}
        for c in range(CombinationNum):
            foundFieldDicNew, RulepDicNew, tmpresultItem = CombinationFind(RuleList, N, FieldInfoList, foundFieldDic, RulepDicOld, stride_s, cluster_n)
            if RulepDicNew == {} :
                break
            foundFieldDic = foundFieldDicNew
            RulepDicOld = RulepDicNew   #!!!
            #print foundFieldDic
            CombinationResult.append(tmpresultItem) # tmpresultItem <- (Lm, FieldName, p*Np / 104*N, p, Np)
            #print tmpresultItem
        
        M = 0
        tmplen = 0
        tmpResultDic = {}
        for c in range(len(CombinationResult)-1):
            M += (CombinationResult[c][-2] + tmplen) * (CombinationResult[c][-1] - CombinationResult[c+1][-1])
            tmpResultDic[c] = (M + (CombinationResult[c][-2] + tmplen) * CombinationResult[c+1][-1]) / (104*N)
            tmplen += CombinationResult[c][-2]
        M += (CombinationResult[-1][-2] + tmplen) * CombinationResult[-1][-1]
        for c in range(len(CombinationResult)-1, CombinationNum):
            tmpResultDic[c] = M / (104*N)
        print(FileList[m],M / (104*N))
        #print("m = ", m)
        ResultList.append(tmpResultDic)
    return ResultList

def CombinationVertical(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n):
    ResultList = []
    
    for m in range(len(FileList)):
        RuleList, linenum = Init(FileList[m]) # RuleList[i] <- [RID, sa, da, sp, dp, prtcl]
        N = len(RuleList)
        CombinationResult = []
        RuleElseSet = set([item[0] for item in RuleList])   # Init: all RID
        
        RulepDicOld = {}
        
        foundFieldDic = {}
        RulepDicOld = {}
        for c in range(CombinationNum):
            foundFieldDicNew, RulepDicNew, tmpresultItem = CombinationFind(RuleList, N, FieldInfoList, foundFieldDic, RulepDicOld, stride_s, cluster_n)
            if RulepDicNew == {} :
                break
            #foundFieldDic = foundFieldDicNew
            RuleElseSet = RuleElseSet - set(RulepDicNew)
            RulepDicOld = dict(zip(RuleElseSet, [1]*len(RuleElseSet)))
            #print foundFieldDic
            CombinationResult.append(tmpresultItem) # tmpresultItem <- (Lm, FieldName, p*Np / 104*N, p, Np)
            #print tmpresultItem
            if RulepDicOld == {} :
                break
        
        M = 0
        tmpResultDic = {}
        for c in range(len(CombinationResult)):
            M += CombinationResult[c][-2] * CombinationResult[c][-1]
            tmpResultDic[c] = M / (104*N)
        for c in range(len(CombinationResult), CombinationNum):
            tmpResultDic[c] = M / (104*N)
        print(FileList[m],M / (104*N))
        #print("m = ", m)
        ResultList.append(tmpResultDic)
    
    return ResultList
    
def CombinationVertical_Horizontal(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n):
    ResultList = []
    
    for m in range(len(FileList)):
        RuleList, linenum = Init(FileList[m]) # RuleList[i] <- [RID, sa, da, sp, dp, prtcl]
        N = len(RuleList)
        v_CombinationResult = []
        RuleElseSet = set([item[0] for item in RuleList])   # Init: all RID
        
        v_foundFieldDic = {}
        v_RulepDicOld = {}
        for cv in range(CombinationNum):
            v_foundFieldDicNew, v_RulepDicNew, v_tmpresultItem = CombinationFind(RuleList, N, FieldInfoList, v_foundFieldDic, v_RulepDicOld, stride_s, cluster_n)
            if v_RulepDicNew == {} :  # can not find field to compress
                break
            #------------------------------------------------------------------
            h_foundFieldDic = v_foundFieldDicNew
            h_RulepDicOld = v_RulepDicNew
            h_CombinationResult = [v_tmpresultItem]    # Add the first item
            for ch in range(CombinationNum-1):
                h_foundFieldDicNew, h_RulepDicNew, h_tmpresultItem = CombinationFind(RuleList, N, FieldInfoList, h_foundFieldDic, h_RulepDicOld, stride_s, cluster_n)
                if h_RulepDicNew == {}: # can not find field to compress
                    break
                h_foundFieldDic = h_foundFieldDicNew
                h_RulepDicOld = h_RulepDicNew   #!!!
                h_CombinationResult.append(h_tmpresultItem) # tmpresultItem <- (Lm, FieldName, p*Np / 104*N, p, Np)
                
            h_M = 0
            tmplen = 0
            tmpResultDic = {}
            for ch in range(len(h_CombinationResult)-1):
                h_M += (h_CombinationResult[ch][-2] + tmplen) * (h_CombinationResult[ch][-1] - h_CombinationResult[ch+1][-1])
                tmpResultDic[ch] = (h_M + (h_CombinationResult[ch][-2] + tmplen) * h_CombinationResult[ch+1][-1])
                tmplen += h_CombinationResult[ch][-2]
            try:
                h_M += (h_CombinationResult[-1][-2] + tmplen) * h_CombinationResult[-1][-1]
            except:
                print('h_CombinationResult -> ',h_CombinationResult)
            for ch in range(len(h_CombinationResult)-1, CombinationNum):
                tmpResultDic[ch] = h_M
            #------------------------------------------------------------------
            RuleElseSet = RuleElseSet - set(v_RulepDicNew)
            v_RulepDicOld = dict(zip(RuleElseSet, [1]*len(RuleElseSet)))
            v_CombinationResult.append((v_tmpresultItem, h_M, tmpResultDic)) # tmpresultItem <- (Lm, FieldName, p*Np / 104*N, p, Np)
            if v_RulepDicOld == {} :
                break
        #print(v_CombinationResult)
        #print('len(v_CombinationResult)', len(v_CombinationResult))
        tmpResultDic = {}
        for cN in range(CombinationNum):
            M = 0
            for cv in range(len(v_CombinationResult)):     
                M += v_CombinationResult[cv][2][cN]
            tmpResultDic[cN] = M / (104*N)
            #print(M / (104*N))
        print(FileList[m],M / (104*N))
        ResultList.append(tmpResultDic)
        
    return ResultList

def DrawFCT_Combination():
    stride_s = 4
    cluster_n = 8
    FieldInfoList = [('sa', 32), ('da', 32), ('sp', 16), ('dp', 16), ('prtcl', 8)]
    #FieldInfoList = [('sa', 32)]
    ResultList = []
    FileList = ['ACL1_10K', 'ACL2_10K', 'ACL3_10K', 'ACL4_10K', 'ACL5_10K',\
                 'FW1_10K', 'FW2_10K', 'FW3_10K', 'FW4_10K', 'FW5_10K',\
                 'IPC1_10K', 'IPC2_10K']
    #FileList = ['ACL1_10K']
    CombinationNum = 4
    
    ResultList = CombinationHorizontal(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n)
    #ResultList = CombinationVertical(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n)
    #ResultList = CombinationVertical_Horizontal(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n)
    MaxResultList = MaxCompressedPresent(FieldInfoList, FileList)   # MaxResultList[i] <- (FileName, M / 104*N)
    
    #   https://blog.csdn.net/liangzuojiayi/article/details/78187704 
    tmpcnames = ['royalblue', 'crimson', 'forestgreen', 'darkorchid', 'darkorange']
    plt.figure(figsize=(16,9))
    setwidth = 0.15
    for n in range(CombinationNum):
        x = [i+1+n*setwidth for i in range(len(ResultList))]
        y = []
        for j in range(len(ResultList)):
            tmpResultDic = ResultList[j]
            y.append(tmpResultDic[n])
        plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n], edgecolor = 'white', label='$Combination-'+str(n+1)+'$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    x = [i+1+(n+1)*setwidth for i in range(len(MaxResultList))]
    y = []
    for j in range(len(MaxResultList)):
        y.append(MaxResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n+1], edgecolor = 'white', label='$MaxCompressed$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    x = [i+1+(len(FieldInfoList) / 2)*setwidth for i in range(len(ResultList))]
    plt.xticks(x, ('ACL1', 'ACL2', 'ACL3', 'ACL4', 'ACL5', 'FW1', 'FW2', 'FW3', 'FW4', 'FW5', 'IPC1', 'IPC2'))
    plt.ylabel("Percent")
    plt.title('Field Compressed Combination-Horizontal')
    plt.legend(loc='upper right') #'lower right') 'best')
    plt.legend()
    plt.show()
    
print 'p'
DrawFCT_Combination()
        