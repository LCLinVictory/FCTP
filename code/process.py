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
import sys
import numpy as np

from process_unit import CombinationHorizontal, CombinationVertical, CombinationMix, MaxCompressedPresent, CountResultRule, CombinationMix_MaxPadding

def DrawWeeBV_Combination(DataFlag, CMD, CombinationNum, stride_s, cluster_n):
    #   ---Five Tuple---
    FiveTupleFieldInfoList = [('sa', 32), ('da', 32), ('sp', 16), ('dp', 16), ('prtcl', 8)]
    FiveTupleFileList = ['ACL1_10K', 'ACL2_10K', 'ACL3_10K', 'ACL4_10K', 'ACL5_10K']#,\
    '''
                 'ACL1_10K', 'ACL2_10K', 'ACL3_10K', 'ACL4_10K', 'ACL5_10K',\
                 'FW1_10K', 'FW2_10K', 'FW3_10K', 'FW4_10K', 'FW5_10K',\
                 'IPC1_10K', 'IPC2_10K' \
                 'IPC1_5K', 'IPC1_10K', 'IPC2_5K', 'IPC2_10K']
    '''
    FiveTupleCombinationList = [1-1, 3-1, 5-1]   #[n for n in range(CombinationNum)]
    #   ---OpenFlow 1.0---
    OpenFlowFieldInfoList = [# (Fieldname Fieldlen)
                            ('in_port', 16), \
                            ('dl_src', 48), \
                            ('dl_dst', 48), \
                            ('eth_type', 16), \
                            ('dl_vlan', 12), \
                            ('dl_vlan_pcp', 3), \
                            ('nw_src', 32), \
                            ('nw_dst', 32), \
                            ('nw_tos', 6), \
                            ('nw_proto', 8), \
                            ('tp_src', 16), \
                            ('tp_dst', 16)]
    OpenFlowFileList = ['OF1_5K', 'OF1_10K', 'OF2_5K', 'OF2_10K']
    '''
                        ['OF1_1K', 'OF2_1K', 'OF1_10K', 'OF2_10K', 'OF1_20K', 'OF2_20K',\
                        'OF1_50K', 'OF2_50K']
    '''
    OpenFlowCombinationList = [2-1, 8-1, 12-1]    #   [2-1, 4-1, 8-1, 10-1, 12-1]
    
    if DataFlag == '5' :
        TitleCMD = 'FiveTuple_'
        FieldInfoList = FiveTupleFieldInfoList
        FileList = FiveTupleFileList
        CombinationList = FiveTupleCombinationList
        LAll = 104
    elif DataFlag == 'of' :
        TitleCMD = 'OpenFlow_'
        FieldInfoList = OpenFlowFieldInfoList
        FileList = OpenFlowFileList
        CombinationList = OpenFlowCombinationList
        LAll = 253
    else:
        print('Unkown DataFlag')
        sys.exit(0)
    
    ResultList = []
    print('CombinationNum = '+str(CombinationNum)+' | stride_s= '+str(stride_s)+', cluster_n='+str(cluster_n))
    
    if CMD == 'h' :
        ResultList, RIDOrderList = CombinationHorizontal(FieldInfoList, FileList, LAll, CombinationNum, stride_s, cluster_n)
        TitleCMD += 'Horizontal'
    elif CMD =='v' :
        ResultList, RIDOrderList = CombinationVertical(FieldInfoList, FileList, LAll, CombinationNum, stride_s, cluster_n)
        TitleCMD += 'Vertical'
    elif CMD == 'mix':
        ResultList, RIDOrderList, AdditionList = CombinationMix(FieldInfoList, FileList, LAll, CombinationNum, stride_s, cluster_n)
        TitleCMD += 'Mix'
    else:
        print('Error')
        return
    ##print('len(ResultList)', len(ResultList))
    '''
    OrderRuleList(FieldInfoList, FileList, LAll, RIDOrderList, CombinationNum, stride_s, cluster_n)
    '''
    #ViolentResultList = Combination_ViolentSearch(FieldInfoList, FileList, LAll, CombinationNum, stride_s, cluster_n)
    #MaxResultList = MaxCompressedPresent(DataFlag, FieldInfoList, FileList, LAll)   # MaxResultList[i] <- (FileName, M / LAll*N)
    
    #   ---Draw---
    #   https://blog.csdn.net/liangzuojiayi/article/details/78187704 
    tmpcnames = ['royalblue', 'crimson', 'yellowgreen', 'darkorchid', 'darkorange', 'gainsboro']
    plt.figure(figsize=(20,9))
    setwidth = 0.15
    
    tmpIndx = 0
    
    x = [i+1+(tmpIndx)*setwidth for i in range(len(AdditionList))]
    yStride = []
    for j in range(len(AdditionList)):
        yStride.append(int(AdditionList[j] * (pow(2, stride_s) / stride_s) / (8*1024)))
    plt.bar(x, yStride, alpha=1, width = setwidth, facecolor = tmpcnames[tmpIndx], edgecolor = 'white', label='$StrideBV/TPBV$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    tmpIndx += 1
    
    for n in CombinationList:
        x = [i+1+tmpIndx*setwidth for i in range(len(ResultList))]
        y = []
        for j in range(len(ResultList)):
            tmpResultDic = ResultList[j]
            y.append(int(yStride[j] * (1 - tmpResultDic[n])))
        plt.bar(x, y, alpha=1, width = setwidth, facecolor = tmpcnames[tmpIndx], edgecolor = 'white', label='$WeeBV-cbN='+str(n+1)+'$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
        tmpIndx += 1
    '''
    #   Violent
    x = [i+1+(n+1)*setwidth for i in range(len(ViolentResultList))]
    y = []
    for j in range(len(ViolentResultList)):
        y.append(ViolentResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n+1], edgecolor = 'white', label='$ViolentCompressed$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    '''
    '''
    #   Max
    x = [i+1+(tmpIndx)*setwidth for i in range(len(MaxResultList))]
    y = []
    for j in range(len(MaxResultList)):
        y.append(MaxResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[tmpIndx], edgecolor = 'white', label='$MaxCompressed$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    '''
    
    x = [i+1+((len(CombinationList)+1) / 2)*setwidth for i in range(len(ResultList))]
    plt.xticks(x, tuple(FileList), fontsize=30)
    plt.xlim(0.0, x[-1]+1)
    plt.ylim(0.0, max(yStride)*1.2)
    plt.yticks(fontsize=28)
    plt.ylabel("KB", fontsize=30)
    #plt.title('Field Compressed Combination-'+TitleCMD)
    plt.legend(ncol=1, fontsize=30, loc='upper left') #'lower right') 'best')
    #plt.legend()
    plt.grid(ls='--', axis='y', c='slategray')
    plt.savefig('../pic/Field Compressed Combination-'+TitleCMD+'_'+str(stride_s)+'_'+str(cluster_n)+'.pdf', bbox_inches='tight')
    #plt.show()

def DrawWeeBV_Mix_Compare(DataFlag, CombinationNum, stride_s, cluster_n):
    #   ---Five Tuple---
    FiveTupleFieldInfoList = [('sa', 32), ('da', 32), ('sp', 16), ('dp', 16), ('prtcl', 8)]
    FiveTupleFileList = ['FW1_10K', 'FW2_10K', 'FW3_10K', 'FW4_10K', 'FW5_10K']    #['IPC1_5K', 'IPC1_10K', 'IPC2_5K', 'IPC2_10K']#,\
    '''
                 'ACL1_10K', 'ACL2_10K', 'ACL3_10K', 'ACL4_10K', 'ACL5_10K',\
                 'FW1_10K', 'FW2_10K', 'FW3_10K', 'FW4_10K', 'FW5_10K',\
                 'IPC1_10K', 'IPC2_10K']
                 'IPC1_5K', 'IPC1_10K', 'IPC2_5K', 'IPC2_10K'
    '''
    #   ---OpenFlow 1.0---
    OpenFlowFieldInfoList = [# (Fieldname Fieldlen)
                            ('in_port', 16), \
                            ('dl_src', 48), \
                            ('dl_dst', 48), \
                            ('eth_type', 16), \
                            ('dl_vlan', 12), \
                            ('dl_vlan_pcp', 3), \
                            ('nw_src', 32), \
                            ('nw_dst', 32), \
                            ('nw_tos', 6), \
                            ('nw_proto', 8), \
                            ('tp_src', 16), \
                            ('tp_dst', 16)]
    OpenFlowFileList = ['OF1_5K', 'OF1_10K', 'OF2_5K', 'OF2_10K']
    '''
                        ['OF1_1K', 'OF2_1K', 'OF1_10K', 'OF2_10K', 'OF1_20K', 'OF2_20K',\
                        'OF1_50K', 'OF2_50K']
    '''
    
    if DataFlag == '5' :
        TitleCMD = 'FiveTuple_'
        FieldInfoList = FiveTupleFieldInfoList
        FileList = FiveTupleFileList
        #CombinationList = FiveTupleCombinationList
        LAll = 104
    elif DataFlag == 'of' :
        TitleCMD = 'OpenFlow_'
        FieldInfoList = OpenFlowFieldInfoList
        FileList = OpenFlowFileList
        #CombinationList = OpenFlowCombinationList
        LAll = 253
    else:
        print('Unkown DataFlag')
        sys.exit(0)
    
    ResultList = []
    print('CombinationNum = '+str(CombinationNum)+' | stride_s= '+str(stride_s)+', cluster_n='+str(cluster_n))
    
    TitleCMD += 'Compare'
    #ResultList, RIDOrderList = CombinationMix(FieldInfoList, FileList, LAll, CombinationNum, stride_s, cluster_n)
    ResultList, RIDOrderList, WOMPList = CombinationMix_MaxPadding(FieldInfoList, FileList, LAll, CombinationNum, stride_s, cluster_n)
    ##print('len(ResultList)', len(ResultList))
    '''
    OrderRuleList(FieldInfoList, FileList, LAll, RIDOrderList, CombinationNum, stride_s, cluster_n)
    '''
    CountResultList = CountResultRule(FieldInfoList, FileList, LAll, RIDOrderList, CombinationNum, stride_s, cluster_n)
    #ViolentResultList = Combination_ViolentSearch(FieldInfoList, FileList, CombinationNum, stride_s, cluster_n)
    MaxResultList = MaxCompressedPresent(DataFlag, FieldInfoList, FileList, LAll)   # MaxResultList[i] <- (FileName, M / LAll*N)
    
    #   https://blog.csdn.net/liangzuojiayi/article/details/78187704 
    tmpcnames = ['royalblue', 'darkorange', 'forestgreen', 'darkorchid', 'crimson', 'gainsboro']
    plt.clf()
    plt.figure(figsize=(20,8))
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
        y.append(WOMPList[j] / MaxResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n], edgecolor = 'white', label='$WeeBV$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    # --Mix + MaxPadding--
    n += 1
    x = [i+1+n*setwidth for i in range(len(ResultList))]
    y = []
    for j in range(len(ResultList)):
        tmpResultDic = ResultList[j]
        y.append(tmpResultDic[CombinationNum-1] / MaxResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n], edgecolor = 'white', label='$WeeBV+MaxPadding$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
    # --Count/Upstream--
    n += 1
    x = [i+1+n*setwidth for i in range(len(ResultList))]
    y = []
    for j in range(len(CountResultList)):
        y.append(CountResultList[j][1] / MaxResultList[j][1])
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[n], edgecolor = 'white', label='$WeeBV+UpstreamRule$', lw=1)     # hatch = /, \, |, -, +, x, o, O, ., *
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
    x = [i+1+(3 / 2)*setwidth for i in range(len(ResultList))]
    y = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
    yStr = ['0%', '20%', '40%', '60%', '80%', '100%', ' ']
    plt.xticks(x, tuple(FileList), fontsize=30)
    plt.xlim(0.0, x[-1]+1)
    plt.yticks(y, tuple(yStr), fontsize=28)
    plt.ylim(0.0, 1.2)
    plt.ylabel("Percentage", fontsize=30)
    #plt.title('Field Compressed Combination-'+TitleCMD)
    plt.legend(ncol=3, fontsize=30, loc='upper center') #'lower right') 'best')
    #plt.legend(ncol=1, fontsize=25, loc='upper left').get_frame().set_facecolor('none')
    plt.grid(ls='--', axis='y', c='slategray')
    plt.savefig('../pic/Field Compressed Combination-'+TitleCMD+'_'+str(stride_s)+'_'+str(cluster_n)+'.pdf', bbox_inches='tight')
    #plt.show()

def DrawMaxCompressed():
    #   ---Five Tuple---
    FiveTupleFieldInfoList = [('sa', 32), ('da', 32), ('sp', 16), ('dp', 16), ('prtcl', 8)]
    FiveTupleFileList = ['ACL1_10K', 'ACL2_10K', 'ACL3_10K', 'ACL4_10K', 'ACL5_10K',\
                 'FW1_10K', 'FW2_10K', 'FW3_10K', 'FW4_10K', 'FW5_10K',\
                 'IPC1_10K', 'IPC2_10K']
    
    #   ---OpenFlow 1.0---
    OpenFlowFieldInfoList = [# (Fieldname Fieldlen)
                            ('in_port', 16), \
                            ('dl_src', 48), \
                            ('dl_dst', 48), \
                            ('eth_type', 16), \
                            ('dl_vlan', 12), \
                            ('dl_vlan_pcp', 3), \
                            ('nw_src', 32), \
                            ('nw_dst', 32), \
                            ('nw_tos', 6), \
                            ('nw_proto', 8), \
                            ('tp_src', 16), \
                            ('tp_dst', 16)]
    OpenFlowFileList = ['OF1_5K', 'OF1_10K', 'OF2_5K', 'OF2_10K']
    
    TitleCMD = 'MaxCompressed'
    MaxResultList5 = MaxCompressedPresent('5', FiveTupleFieldInfoList, FiveTupleFileList, 104)   # MaxResultList[i] <- (FileName, M / LAll*N)
    MaxResultListOF = MaxCompressedPresent('of', OpenFlowFieldInfoList, OpenFlowFileList, 253)   # MaxResultList[i] <- (FileName, M / LAll*N)
    
    #   https://blog.csdn.net/liangzuojiayi/article/details/78187704 
    tmpcnames = ['royalblue', 'darkorange', 'forestgreen', 'darkorchid', 'crimson', 'dimgray']
    plt.clf()
    plt.figure(figsize=(16,6))
    setwidth = 0.4
    n = -1
    
    # --Max--
    n += 1
    x = [i+1+n*setwidth for i in range(len(MaxResultList5) + len(MaxResultListOF))]
    y = []
    for j in range(len(MaxResultList5)):
        y.append(MaxResultList5[j][1])
    for j in range(len(MaxResultListOF)):
        y.append(MaxResultListOF[j][1])
    for j in range(len(y)):
        print(y[j])
    print(np.mean(y[:-4]), max(y[:-4]), min(y[:-4]))
    plt.bar(x, y, alpha=0.9, width = setwidth, facecolor = tmpcnames[-1], edgecolor = 'white', lw=3)     # hatch = /, \, |, -, +, x, o, O, ., *
    
    x = [i+1+n*setwidth-setwidth*0.5 for i in range(len(MaxResultList5) + len(MaxResultListOF))]
    plt.xticks(x, tuple(FiveTupleFileList+OpenFlowFileList), fontsize=30, rotation=45)
    plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], ('0%', '20%', '40%', '60%', '80%', '100%'), fontsize=28)
    plt.ylim(0.0, 1.0)
    plt.ylabel("Percentage", fontsize=30)
    plt.grid(ls='--', axis='y', c='slategray')
    plt.savefig('../pic/'+TitleCMD+'.pdf', bbox_inches='tight')

import click
@click.command()
@click.option('-cmd', type=click.Choice(['cbn','cmp', 'max']), required=True, help='Command kinds: Combination(cbn), Compare(cmp), MaxCompressed(max)')
@click.option('-rtype', type=str, required=True, help='ruleset type: 5-tuple(5), OpenFlow1.0(of)')
@click.option('--stride', type=int, default=4, help='stride_s, default is 4')
@click.option('--cluster', type=int, default=8, help='cluster_n, default is 8')

def process(cmd, rtype, stride, cluster):
    """WeeBV -> draw analyze result of various rulesets \n\n Ex. process.py -cmd=cbn -rtype=5"""
    if rtype == '5' :
            filednum = 5
    elif rtype == 'of' :
        filednum = 12
    if cmd == 'cbn' :
        click.echo(DrawWeeBV_Combination(rtype, 'mix', filednum, stride, cluster))
    elif cmd == 'cmp' :
        click.echo(DrawWeeBV_Mix_Compare(rtype, filednum, stride, cluster))
    elif cmd == 'max' :
        click.echo(DrawMaxCompressed())


if __name__ == "__main__":
    process()

##Some Examples
#DrawWeeBV_Combination('5', 'mix', 5, 4, 8)
#DrawWeeBV_Combination('of', 'mix', 12, 4, 8)
#DrawWeeBV_Mix_Compare('5', 5, 4, 8)
#DrawWeeBV_Mix_Compare('of', 12, 4, 8)
#DrawMaxCompressed()