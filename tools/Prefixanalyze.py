# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:27:14 2018

@author: LCL
"""
from __future__ import division # for / and //
from tools import Init

import matplotlib.pyplot as plt

#   https://blog.csdn.net/qq_26376175/article/details/67637151
mkrname = {
'.':    "point marker",
',':    "pixel marker",
'o':    "circle marker",
'v':    "triangle_down marker",
'^':    "triangle_up marker",
'<':    "triangle_left marker", #
'*':    "star marker",  #
'h':    "hexagon1 marker",
'H':    "hexagon2 marker",  #
'+':    "plus marker",  
'x':    "x marker",
'D':    "diamond marker",   #
'd':    "thin_diamond marker"}  #

cnames = {
'aliceblue':            '#F0F8FF',
'antiquewhite':         '#FAEBD7',
'aqua':                 '#00FFFF',
'aquamarine':           '#7FFFD4',
'azure':                '#F0FFFF',
'beige':                '#F5F5DC',
'bisque':               '#FFE4C4',
'black':                '#000000',
'blanchedalmond':       '#FFEBCD',
'blue':                 '#0000FF',
'blueviolet':           '#8A2BE2',
'brown':                '#A52A2A',
'burlywood':            '#DEB887',
'cadetblue':            '#5F9EA0',
'chartreuse':           '#7FFF00',
'chocolate':            '#D2691E',
'coral':                '#FF7F50',
'cornflowerblue':       '#6495ED',
'cornsilk':             '#FFF8DC',
'crimson':              '#DC143C',
'cyan':                 '#00FFFF',
'darkblue':             '#00008B',
'darkcyan':             '#008B8B',
'darkgoldenrod':        '#B8860B',
'darkgray':             '#A9A9A9',
'darkgreen':            '#006400',
'darkkhaki':            '#BDB76B',
'darkmagenta':          '#8B008B',
'darkolivegreen':       '#556B2F',
'darkorange':           '#FF8C00',
'darkorchid':           '#9932CC',
'darkred':              '#8B0000',
'darksalmon':           '#E9967A',
'darkseagreen':         '#8FBC8F',
'darkslateblue':        '#483D8B',
'darkslategray':        '#2F4F4F',
'darkturquoise':        '#00CED1',
'darkviolet':           '#9400D3',
'deeppink':             '#FF1493',
'deepskyblue':          '#00BFFF',
'dimgray':              '#696969',
'dodgerblue':           '#1E90FF',
'firebrick':            '#B22222',
'floralwhite':          '#FFFAF0',
'forestgreen':          '#228B22',
'fuchsia':              '#FF00FF',
'gainsboro':            '#DCDCDC',
'ghostwhite':           '#F8F8FF',
'gold':                 '#FFD700',
'goldenrod':            '#DAA520',
'gray':                 '#808080',
'green':                '#008000',
'greenyellow':          '#ADFF2F',
'honeydew':             '#F0FFF0',
'hotpink':              '#FF69B4',
'indianred':            '#CD5C5C',
'indigo':               '#4B0082',
'ivory':                '#FFFFF0',
'khaki':                '#F0E68C',
'lavender':             '#E6E6FA',
'lavenderblush':        '#FFF0F5',
'lawngreen':            '#7CFC00',
'lemonchiffon':         '#FFFACD',
'lightblue':            '#ADD8E6',
'lightcoral':           '#F08080',
'lightcyan':            '#E0FFFF',
'lightgoldenrodyellow': '#FAFAD2',
'lightgreen':           '#90EE90',
'lightgray':            '#D3D3D3',
'lightpink':            '#FFB6C1',
'lightsalmon':          '#FFA07A',
'lightseagreen':        '#20B2AA',
'lightskyblue':         '#87CEFA',
'lightslategray':       '#778899',
'lightsteelblue':       '#B0C4DE',
'lightyellow':          '#FFFFE0',
'lime':                 '#00FF00',
'limegreen':            '#32CD32',
'linen':                '#FAF0E6',
'magenta':              '#FF00FF',
'maroon':               '#800000',
'mediumaquamarine':     '#66CDAA',
'mediumblue':           '#0000CD',
'mediumorchid':         '#BA55D3',
'mediumpurple':         '#9370DB',
'mediumseagreen':       '#3CB371',
'mediumslateblue':      '#7B68EE',
'mediumspringgreen':    '#00FA9A',
'mediumturquoise':      '#48D1CC',
'mediumvioletred':      '#C71585',
'midnightblue':         '#191970',
'mintcream':            '#F5FFFA',
'mistyrose':            '#FFE4E1',
'moccasin':             '#FFE4B5',
'navajowhite':          '#FFDEAD',
'navy':                 '#000080',
'oldlace':              '#FDF5E6',
'olive':                '#808000',
'olivedrab':            '#6B8E23',
'orange':               '#FFA500',
'orangered':            '#FF4500',
'orchid':               '#DA70D6',
'palegoldenrod':        '#EEE8AA',
'palegreen':            '#98FB98',
'paleturquoise':        '#AFEEEE',
'palevioletred':        '#DB7093',
'papayawhip':           '#FFEFD5',
'peachpuff':            '#FFDAB9',
'peru':                 '#CD853F',
'pink':                 '#FFC0CB',
'plum':                 '#DDA0DD',
'powderblue':           '#B0E0E6',
'purple':               '#800080',
'red':                  '#FF0000',
'rosybrown':            '#BC8F8F',
'royalblue':            '#4169E1',
'saddlebrown':          '#8B4513',
'salmon':               '#FA8072',
'sandybrown':           '#FAA460',
'seagreen':             '#2E8B57',
'seashell':             '#FFF5EE',
'sienna':               '#A0522D',
'silver':               '#C0C0C0',
'skyblue':              '#87CEEB',
'slateblue':            '#6A5ACD',
'slategray':            '#708090',
'snow':                 '#FFFAFA',
'springgreen':          '#00FF7F',
'steelblue':            '#4682B4',
'tan':                  '#D2B48C',
'teal':                 '#008080',
'thistle':              '#D8BFD8',
'tomato':               '#FF6347',
'turquoise':            '#40E0D0',
'violet':               '#EE82EE',
'wheat':                '#F5DEB3',
'white':                '#FFFFFF',
'whitesmoke':           '#F5F5F5',
'yellow':               '#FFFF00',
'yellowgreen':          '#9ACD32'}

def Analyze(FieldList, L, N):
    PrefixDic = {}
    for i in range(0, L):
        PrefixDic[i] = []
    for item in FieldList:  #FieldList[i] <- [RID, FieldValue]
        RID = item[0]
        FieldValue = item[1]
        tmpidx = FieldValue.find('*')
        '''
        if tmpidx == -1:
            tmpidx = L
        try:
            PrefixDic[tmpidx].append(RID)
        except:
            PrefixDic[tmpidx] = []
        '''    
        if tmpidx != -1:
            for i in range(tmpidx, L):
                PrefixDic[i].append(RID)
        
    return PrefixDic

'''
###############################################################################
'''

#def drawAnalyze(FieldInfoList):

FieldInfoList = [('sa', 32), ('da', 32), ('sp', 16), ('dp', 16), ('prtcl', 8)]
FieldInfoList = [('sa', 32)]

idxFileListDic = {'sa':1, 'da':2, 'sp':3, 'dp':4, 'prtcl':5}
titleDic = {'sa':'Source IP Address', 'da':'Destination IP Address', 'sp':'Source Port', 'dp':'Destination Port', 'prtcl':'Protocol'}
AnalyzeList = []
FileList = ['ACL1_10K', 'ACL2_10K', 'ACL3_10K', 'ACL4_10K', 'ACL5_10K',\
             'FW1_10K', 'FW2_10K', 'FW3_10K', 'FW4_10K', 'FW5_10K',\
             'IPC1_10K', 'IPC2_10K']
             
for m in range(len(FileList)):
    RuleList, linenum = Init(FileList[m]) # [RID, sa, da, sp, dp, prtcl]
    N = len(RuleList)
    tmpresult = []
    for n in range(len(FieldInfoList)):
        FieldList = []  #FieldList[i] <- [RID, FieldValue]
        for i in range(N):
            FieldList.append([RuleList[i][0], RuleList[i][idxFileListDic[FieldInfoList[n][0]]]])
        L = FieldInfoList[n][1]
        PrefixDic = Analyze(FieldList, L, N)
        tmplist = []
        for tmpkey in sorted(PrefixDic.keys()):
            tmplist.append((tmpkey, len(list(set(PrefixDic[tmpkey]))) / N))    # de-duplication
        tmpresult.append([FieldInfoList[n][0], tmplist])
    AnalyzeList.append((FileList[m], tmpresult))
    print('m = '+str(m), 'linenum / N = '+str(linenum / N))
        
f = open('Analyze.txt', 'w')
for item in AnalyzeList:
    f.write(str(item) + '\n')
f.close()


tmpcnames = ['cornflowerblue', 'crimson', 'limegreen']
mlist = ['<', '*', 'H', 'D', 'd', '<', '*', 'H', 'D', 'd', '<', '*']

clist = []
for i in range(12):
    #clist.append(sorted(cnames.keys())[i+8])
    clist.append(tmpcnames[i // 5])
    #mlist.append(sorted(mkrname.keys())[i])

plt.figure(figsize=(16*2,9*2))
for i in range(len(AnalyzeList)):
    tmpList = AnalyzeList[i][1][0][1]
    x = []
    y = []
    for tmpitem in tmpList:
        x.append(tmpitem[0])
        y.append(tmpitem[1])
    plt.plot(x,y,label = '$'+AnalyzeList[i][0].replace('_', '-')+'$',color = clist[i],marker = mlist[i],linewidth=1.5)
plt.xlim(0.0, L + (5 - L % 5))
plt.ylim(0.0, 1.0)
plt.xlabel("Wildcard Position")
plt.ylabel("Percent")
plt.title(titleDic[FieldInfoList[n][0]])
plt.legend(loc='upper right') #'lower right') 'best')
plt.legend()
plt.show()