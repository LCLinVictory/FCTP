# -*- coding: utf-8 -*-
"""
Created on  2018

@author: LCL
"""

from __future__ import division # for / and //
'''
import matplotlib as mpl        # for Linux VM-129-211-ubuntu 4.4.0-135-generic
mpl.use('Agg')
'''
import matplotlib.pyplot as plt

from process_unit import CombinationHorizontal, CombinationVertical, CombinationMix, MaxCompressedPresent, CountResultRule

'''
####Test Area##################################################################
'''
from tools import Init  # call Init function
from process_unit import CombinationFind

def Test_CombinationMix(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n):
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
            h_CombinationResult = [(tuple(v_RulepDicNew.keys()), v_tmpresultItem, [])]    # Add the first item
            for ch in range(CombinationNum - 1):
                h_foundFieldDicNew, h_RulepDicNew, h_tmpresultItem = CombinationFind(RuleList, N, FieldInfoList, h_foundFieldDic, h_RulepDicOld, stride_s, cluster_n)
                if h_RulepDicNew == {}: # can not find field to compress
                    break
                
                #---Max Padding---
                m_MaxPaddingResult = []
                #print('T->', len(h_RulepDicNew), len(h_RulepDicOld))
                if (len(h_RulepDicNew) / len(h_RulepDicOld)) < (2/3) :
                    m_foundFieldDic = h_foundFieldDic
                    tmpRuleElseSet = set(h_RulepDicOld) - set(h_RulepDicNew)
                    m_RulepDicOld = dict(zip(tmpRuleElseSet, [1]*len(tmpRuleElseSet)))
                    for cm in range(len(FieldInfoList) - len(m_foundFieldDic)):
                        m_foundFieldDicNew, m_RulepDicNew, m_tmpresultItem = CombinationFind(RuleList, N, FieldInfoList, m_foundFieldDic, m_RulepDicOld, stride_s, cluster_n)
                        if m_RulepDicNew == {}:
                            break
                        m_foundFieldDic = m_foundFieldDicNew
                        m_RulepDicOld = m_RulepDicNew
                        m_MaxPaddingResult.append((tuple(m_RulepDicNew.keys()), m_tmpresultItem))
                #-----------------
                
                h_foundFieldDic = h_foundFieldDicNew
                h_RulepDicOld = h_RulepDicNew   #!!!
                h_CombinationResult.append((tuple(h_RulepDicNew.keys()), h_tmpresultItem, m_MaxPaddingResult)) # tmpresultItem <- (Lm, FieldName, p*Np / 104*N, p, Np)
                
            M = 0
            h_tmpResultDic = {}
            tmplist = []
            for ch in range(len(h_CombinationResult)):
                '''
                FieldName = h_CombinationResult[ch][1][1]
                pNum = h_CombinationResult[ch][1][-1]
                pLen = h_CombinationResult[ch][1][-2]
                print(cv, ch, pLen, pNum, FieldName)
                '''
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
            
            #---Max Padding---
            M_mp = 0
            for ch in range(len(h_CombinationResult)):
                m_MaxPaddingResult  = h_CombinationResult[ch][2]
                if m_MaxPaddingResult != []:
                    for cm in range(len(m_MaxPaddingResult)):
                        tmpNum = m_MaxPaddingResult[cm][1][-1]
                        tmpLen = m_MaxPaddingResult[cm][1][-2]
                        #print('MP',ch, cm, tmpLen, tmpNum, m_MaxPaddingResult[cm][1][1])
                        M_mp += (tmpLen - tmpLen%stride_s) * (tmpNum - tmpNum%cluster_n)
            M += M_mp
            h_tmpResultDic[len(h_CombinationResult)-1] = (tuple(tmplist), M)
            #-----------------
            
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
        v_tmpRIDOrderDic = {}
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

'''
####Test Area##################################################################
'''

def DrawFCT_Combination(CMD, CombinationNum, stride_s, cluster_n):
    FieldInfoList = [('sa', 32), ('da', 32), ('sp', 16), ('dp', 16), ('prtcl', 8)]
    #FieldInfoList = [('sa', 32)]
    ResultList = []
    FileList = ['ACL1_10K', 'ACL2_10K', 'ACL3_10K', 'ACL4_10K', 'ACL5_10K',\
                 'FW1_10K', 'FW2_10K', 'FW3_10K', 'FW4_10K', 'FW5_10K',\
                 'IPC1_10K', 'IPC2_10K']
    #FileList = ['FW4_10K']
    TitleCMD = ''
    print('CombinationNum = '+str(CombinationNum)+' | stride_s= '+str(stride_s)+', cluster_n='+str(cluster_n))
    
    if CMD == 'h' :
        ResultList, RIDOrderList = CombinationHorizontal(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n)
        TitleCMD = 'Horizontal'
    elif CMD =='v' :
        ResultList, RIDOrderList = CombinationVertical(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n)
        TitleCMD = 'Vertical'
    elif CMD == 'mix':
        ResultList, RIDOrderList = CombinationMix(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n)
        TitleCMD = 'Mix'
    else:
        print('Error')
        return
    ##print('len(ResultList)', len(ResultList))
    '''
    OrderRuleList(FieldInfoList, FileList, RIDOrderList, CombinationNum, stride_s, cluster_n)
    '''
    #ViolentResultList = Combination_ViolentSearch(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n)
    MaxResultList = MaxCompressedPresent(FieldInfoList, FileList)   # MaxResultList[i] <- (FileName, M / 104*N)
    
    #   https://blog.csdn.net/liangzuojiayi/article/details/78187704 
    tmpcnames = ['royalblue', 'crimson', 'forestgreen', 'darkorchid', 'darkorange', 'gainsboro']
    plt.figure(figsize=(16,9))
    setwidth = 0.15
    for n in range(CombinationNum):
        x = [i+1+n*setwidth for i in range(len(ResultList))]
        y = []
        for j in range(len(ResultList)):
            tmpResultDic = ResultList[j]
            y.append(tmpResultDic[n])
        plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n], edgecolor = 'white', label='$Combination-'+str(n+1)+'$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    '''
    #   Violent
    x = [i+1+(n+1)*setwidth for i in range(len(ViolentResultList))]
    y = []
    for j in range(len(ViolentResultList)):
        y.append(ViolentResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n+1], edgecolor = 'white', label='$ViolentCompressed$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    '''
    #   Max
    x = [i+1+(n+1)*setwidth for i in range(len(MaxResultList))]
    y = []
    for j in range(len(MaxResultList)):
        y.append(MaxResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n+1], edgecolor = 'white', label='$MaxCompressed$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    
    x = [i+1+(len(FieldInfoList) / 2)*setwidth for i in range(len(ResultList))]
    plt.xticks(x, ('ACL1', 'ACL2', 'ACL3', 'ACL4', 'ACL5', 'FW1', 'FW2', 'FW3', 'FW4', 'FW5', 'IPC1', 'IPC2'))
    plt.ylabel("Percent")
    plt.title('Field Compressed Combination-'+TitleCMD)
    plt.legend(loc='upper right') #'lower right') 'best')
    plt.legend()
    plt.savefig('./pic/Field Compressed Combination-'+TitleCMD+'_'+str(stride_s)+'_'+str(cluster_n)+'.jpeg')
    #plt.show()

def DrawFCT_Mix_Compare(CombinationNum, stride_s, cluster_n):
    FieldInfoList = [('sa', 32), ('da', 32), ('sp', 16), ('dp', 16), ('prtcl', 8)]
    #FieldInfoList = [('sa', 32)]
    ResultList = []
    FileList = ['ACL1_10K', 'ACL2_10K', 'ACL3_10K', 'ACL4_10K', 'ACL5_10K',\
                 'FW1_10K', 'FW2_10K', 'FW3_10K', 'FW4_10K', 'FW5_10K',\
                 'IPC1_10K', 'IPC2_10K']
    FileList = ['FW3_10K']
    TitleCMD = 'Compare'
    print('CombinationNum = '+str(CombinationNum)+' | stride_s= '+str(stride_s)+', cluster_n='+str(cluster_n))
    
    #ResultList, RIDOrderList = CombinationMix(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n)
    ResultList, RIDOrderList = Test_CombinationMix(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n)
    ##print('len(ResultList)', len(ResultList))
    '''
    OrderRuleList(FieldInfoList, FileList, RIDOrderList, CombinationNum, stride_s, cluster_n)
    '''
    CountResultList = CountResultRule(FieldInfoList, FileList, RIDOrderList, CombinationNum, stride_s, cluster_n)
    #ViolentResultList = Combination_ViolentSearch(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n)
    MaxResultList = MaxCompressedPresent(FieldInfoList, FileList)   # MaxResultList[i] <- (FileName, M / 104*N)
    #   https://blog.csdn.net/liangzuojiayi/article/details/78187704 
    tmpcnames = ['royalblue', 'crimson', 'forestgreen', 'darkorchid', 'darkorange', 'gainsboro']
    plt.figure(figsize=(16,9))
    setwidth = 0.15
    n = -1
    
    '''
    # --Old--
    n += 1
    x = [i+1+n*setwidth for i in range(len(CountResultList))]
    y = []
    for j in range(len(CountResultList)):
        y.append(CountResultList[j][2])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n], edgecolor = 'white', label='$OLD$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    '''
    # --Mix--
    n += 1
    x = [i+1+n*setwidth for i in range(len(ResultList))]
    y = []
    for j in range(len(ResultList)):
        tmpResultDic = ResultList[j]
        y.append(tmpResultDic[CombinationNum-1] / MaxResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n], edgecolor = 'white', label='$Mix-'+str(CombinationNum)+'$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    # --Count--
    n += 1
    x = [i+1+n*setwidth for i in range(len(CountResultList))]
    y = []
    for j in range(len(CountResultList)):
        y.append(CountResultList[j][1] / MaxResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n], edgecolor = 'white', label='$CountMatrix$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    '''
    # --Violent--
    x = [i+1+(n+1)*setwidth for iFileList in range(len(ViolentResultList))]
    y = []
    for j in range(len(ViolentResultList)):
        y.append(ViolentResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n+1], edgecolor = 'white', label='$ViolentCompressed$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    '''
    '''
    # --Max--
    n += 1
    x = [i+1+n*setwidth for i in range(len(MaxResultList))]
    y = []
    for j in range(len(MaxResultList)):
        y.append(MaxResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n], edgecolor = 'white', label='$MaxCompressed$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    '''
    x = [i+1+(n/2)*setwidth for i in range(len(ResultList))]
    plt.xticks(x, tuple(FileList))
    plt.ylabel("Percent")
    plt.title('Field Compressed Combination-'+TitleCMD)
    plt.legend(loc='upper right') #'lower right') 'best')
    plt.legend()
    plt.savefig('../pic/Field Compressed Combination-'+TitleCMD+'_'+str(stride_s)+'_'+str(cluster_n)+'.jpeg')
    #plt.show()

#import click
#@click.command()
#@click.option('-cmd', type=click.Choice(['h','v', 'mix']), required=True, help='Combination kind: Horizontal(h), Vertical(v), Mix(mix)')
#@click.option('-cbn', type=int, required=True, help='Combination numbers')
#@click.option('--stride', type=int, default=4, help='stride_s, default is 4')
#@click.option('--cluster', type=int, default=8, help='cluster_n, default is 8')
#
#def process(cmd, cbn, stride, cluster):
#    """Ex. process.py -cmd=h -cbn=4"""
#    click.echo(DrawFCT_Combination(cmd, cbn, stride, cluster))
#
#
#if __name__ == "__main__":
#    process()

#DrawFCT_Combination('mix', 5, 4, 8)
DrawFCT_Mix_Compare(1, 4, 8)