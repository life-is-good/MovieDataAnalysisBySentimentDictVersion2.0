# -*- coding: utf-8 -*-
import os
import codecs
import re

def splitsentence(keywords,wordlist,remark):  
    #将关键字列表连成：--|--|-- 的形式    
    str1 = ''
    for item in wordlist:
        str1 = str1+item+'|'
    str1= str1[:-1]

    point = u'[\s|\.|。|\?|\？|!|！|；|;|(|（|)|）|…|～|~|#|-|_]'
    comma = u'[,|，]'

    pp = re.compile(point)#按照句号分句
    pc = re.compile(comma)#按照逗号分句

    resultdict = {}#分句结束之后的字典

    for sentence in re.split(pp,remark):
        if sentence:#对每个大句子
            flag = 0
            for sent in re.split(pc,sentence):
                if sent:
                    match = re.findall(str1,sent)
                    if(match):
                        for j in range(len(keywords)):
                            if(set(match) & set(keywords[j])):
                                flag = 1
                                resultdict.setdefault(keywords[j][0],[]).append(sent)
                                index = j
                    elif flag == 1:
                        resultdict.setdefault(keywords[index][0],[]).append(sent)
                    else:
                        resultdict.setdefault(u"无关键字",[]).append(sent)
    returndict = {}
    for k,v in resultdict.items():
        s = ""
        for i in v:
            s = s+u"，"+i
        returndict[k] = s
    
    return returndict
        
                                    
                        
    
















