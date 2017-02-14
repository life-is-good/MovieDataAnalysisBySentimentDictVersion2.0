# -*- coding: utf-8 -*-
import wordDivision
import codecs
import os
import re

def get_data(filepath):
    fileHandler = open(filepath)
    data = fileHandler.read()
    if data[:3] == codecs.BOM_UTF8:
        data = data[3:]
    if data[-1] == '\n':
        data = data[:-1]
    _data = data.decode('utf-8').split('\n')
    data = []
    for word in _data:
        if word != u'':
            data.append(word)
    return data

path = os.path.dirname(os.path.abspath(__file__))

# 导入 sentiment dictionary，情感极性词
posdict = get_data(
    path + '/sentiment dictionary/positive and negative dictionary/posdict.txt')  # 肯定极性，如：爱，安，好，帮，多
negdict = get_data(
    path + '/sentiment dictionary/positive and negative dictionary/negdict.txt')  # 否定极性，如：矮，悲，笨，差，少
#导入极性词典，不同的维度应该有不同的词典，这里暂时只用同一个
posMVdict = get_data(path + '/sentiment dictionary/positive and negative dictionary/posdict.txt')  # 肯定极性
negMVdict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negdict.txt')  # 否定极性
posdaoyandict = get_data(path + '/sentiment dictionary/positive and negative dictionary/posdict.txt')  # 肯定极性
negprodict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negdict.txt')  # 否定极性
posstardict = get_data(path + '/sentiment dictionary/positive and negative dictionary/posdict.txt')  # 肯定极性
negstardict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negdict.txt')  # 否定极性

disstatusdict=get_data(path + '/sentiment dictionary/disturb dictionary/disturb status.txt')


# 导入 adverbs of degree dictionary,程度副词
mostdict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/most.txt')  # 最高级，如：极，极尽，极端，充分，绝顶，，正面因子2.5，反转因子-0.5
verydict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/very.txt')  # 很高级，如：over，过度，过,很，老，不为过，正面因子2.0，反转因子-0.2
moredict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/more.txt')  # 较高级，如：大不了，更，越加，越，但是，足足，正面因子1.5
ishdict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/ish.txt')  # 次高级：如：一点儿，一些，比较，怪，好生，正面因子0.5
insufficientdict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/insufficiently.txt')  # 略高级：如：半点儿，微，略，不怎么，正面因子0.3
ordinarydict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/ordinary.txt')  # 普通级：只有一个词：一般，正面因子0.2
advicedict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/advice.txt')  # 建议级：有四个：希望，建议，可以，应该，正面因子-0.2
inversedict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/inverse.txt')  # 否定级，如：不，没，无，非，不然，正面因子-1.0

# 导入 dynamic dictionary，一些常要结合语境判断的特殊词
dynamic_sentiment = get_data(
    path + '/sentiment dictionary/dynamic dictionary/dynamic sentiment.txt')  # 结合语境的情感极性词，有：大，小，高，低，多，少，紧，浓，淡
dynamic_inverse = get_data(
    path + '/sentiment dictionary/dynamic dictionary/dynamic inverse.txt')  # 结合特殊极性词后与常规极性相反的词，有：价格，人，和dynamic_sentiment的词相结合时，极性逆转
dynamic_remove = get_data(
    path + '/sentiment dictionary/dynamic dictionary/dynamic remove.txt')  # 结合特殊极性词后无意义的词，有：山，爬山，时间（我觉得这个地方最后的时间应该是爬山时间之类的，而不能仅仅是时间）
dynamic_property = get_data(
    path + '/sentiment dictionary/dynamic dictionary/dynamic property.txt')  # 同时是副词也是极性词的词，如：老，好，没多大，贼，没有等

#计算pos/neg的参数
most_para = 2.5
most_inverse = -0.5
very_para = 2.0
very_inverse = -0.2
more_para = 1.5
ish_para = 0.5
insufficient_para = 0.3

#计算score的参数
average_score = 6.5
max_score = 10.0
min_score = 0.0
root_para = 0.6
multi_para = 1.7
advice_para = - 0.2
inverse_para = - 1.0
ordinary_para = 0.2
neg_reduce = 1


def score_trans(count):  #通过对(poscount-negcount)进行处理，得到分数
    if count < -3:
        score = 8 / ( abs(count) - 1 )
    elif count < 0:
        score = 5 + count
    elif count < 1:
        score = 5 + count
    elif count < 3:
        score = 5.5 + count * 0.5
    else:
        score = 10 - 1 / ( count - 2 )
    return score

def wordCal(word, sentiment_value, inver_num):  #根据情感词之前的程度副词对pos/neg_temp进行处理
    if word in mostdict:
        if inver_num == 1:
            sentiment_value *= most_inverse
        else:
            sentiment_value *= most_para
    elif word in verydict:
        if inver_num == 1:
            sentiment_value *= very_inverse
        else:
            sentiment_value *= very_para
    elif word in moredict:
        sentiment_value *= more_para
    elif word in ishdict:
        sentiment_value *= ish_para
    elif word in insufficientdict:
        sentiment_value *= insufficient_para
    elif word in inversedict:
        sentiment_value *= inverse_para
        inver_num += 1
    elif word in advicedict:
        sentiment_value *= advice_para
    return sentiment_value, inver_num

def wordMatch(words,paraposdict,paranegdict):#判断words中是否包含程度副词，极性词，干扰词
    match = []    
    #是否包含干扰词，极性词    
    for word in disstatusdict:
        if words.find(word) != -1 and '' != word:
            match.append(word)
    for word in paraposdict:
        if words.find(word) != -1 and '' != word:
            match.append(word)
    for word in paranegdict:
        if words.find(word) != -1 and '' != word:
            match.append(word)
    #是否包含程度词
    for word in mostdict:
        if words.find(word) != -1 and '' != word:
            match.append(word)
    for word in verydict:
        if words.find(word) != -1 and '' != word:
            match.append(word)
    for word in moredict:
        if words.find(word) != -1 and '' != word:
            match.append(word)
    for word in ishdict:
        if words.find(word) != -1 and '' != word:
            match.append(word)
    for word in insufficientdict:
        if words.find(word) != -1 and '' != word:
            match.append(word)
    for word in advicedict:
        if words.find(word) != -1 and '' != word:
            match.append(word)
    for word in inversedict: 
        if words.find(word) != -1 and '' != word:
            match.append(word)
    if len(match) > 0:
        return list(set(match))
    else:
        return 0
        
#将匹配极性词，副词放在一起    
def divContent(content,paraposdict,paranegdict,classification):
    seg_content = list(wordDivision.cut(content))
    n = len(seg_content)
    i = 0
    while (i<n):                #执行完这个循环以后，按结巴分词所分的词组成的列表seg_content会变成程度副词，极性词，以及包含程度副词的词再分割的程度副词和前缀后缀组成的列表       
        words =  seg_content[i]    #words为分词后的每个词
        if not(words in mostdict or words in verydict or words in moredict or words in ishdict or
               words in insufficientdict or words in inversedict or words in posdict or 
               words in negdict or words in paraposdict or words in paranegdict or words in classification): #如果words本身就是程度副词或极性词，则跳过，若不在词库中，再继续分析,此处posdict和negdict必须包含所有的极性词（包括干扰词）(此处也可以将posdict和negdict拆分成所有的极性词典)
               if wordMatch(words,paraposdict,paranegdict) != 0:#匹配副词，极性词
                   word = []
                   newwords = []
                   word = wordMatch(words,paraposdict,paranegdict)  #返回匹配到的词组成的列表
                   cut = '('
                   for w in word:
                       cut = cut + w + '|'
                   cut = cut + ')'                 #将分隔符写成（--|--|--）形式，为了后面添加的时候可以把分割的词也添加进去      
                   newwords = re.split(cut,words)
                   del seg_content[i]
                   j = 0
                   for nw in newwords:
                       if nw:
                           seg_content.insert(i,nw)
                           i += 1
                       else:
                           j += 1
                   i -= 1
                   n = n-1+len(newwords)-j
        i += 1
    
    n = len(seg_content)
    i = 0
    while(i < n-1):
        words = seg_content[i]
        words_next = seg_content[i+1]
        if(words in paraposdict or words in paranegdict) and (words_next != u'，'):
            seg_content.insert(i+1,u'，')
            i += 1
            n += 1
        i += 1
    
    print '/'.join(seg_content)
    
    return seg_content

def sentimentScoreStar(content,classification):

    i = 0  # word position counter
    a = 0  # sentiment word position
    poscount = 0  # count a positive word
    negcount = 0  # count a negative word
    poscountlist=[0]
    negcountlist=[0]

    seg_content=divContent(content,posstardict,negstardict,classification)

    for word in seg_content:
        if word in dynamic_property:  #判断动态词性的词是情感词还是程度副词，比如 “老”，“好”，如果是，再详细判断
            k = i + 1
            flag = 0
            for postword in seg_content[k:]:  #对这个词后的所有词扫描
                if postword == u'，' or postword == u'的':  #如果先发现“，”或者“的”，说明这个词是情感极性词。跳出扫描
                    break
                if postword in posdict or postword in negdict:  #如果先发现有词语在极性词当中，说明这个词是程度副词，重新扫描下一个词
                    flag = 1
            if flag == 1:
                i += 1
                continue
        if word in posstardict:  #如果是极性词的肯定词
            #print 'pos', word  #test
            pos_temp = 1
            inver_num = 0  #记录反转词的个数
            t = i - 1
            while (seg_content[t] != u'，' and t > -1):  #如果这个词不是第一个词，前面也不是“，”，就一直向前找到seg_content[t]为逗号或者t=-1为止
                t -= 1
            if i > 0 and t + 1 > a:
                a = t + 1
            for w in seg_content[a:i]:
                #print w + str(a) + str(i)
                pos_temp, inver_num = wordCal(w, pos_temp, inver_num)  #
                #print str(pos_temp), str(inver_num)
            a = i + 1
            poscountlist.append(pos_temp)
            # print poscount      #test
        elif word in negstardict:
            #print 'neg', word  #test
            neg_temp = 1
            if word in ordinarydict:
                neg_temp *= ordinary_para
            inver_num = 0
            t = i - 1
            while (seg_content[t] != u'，' and t > -1):
                t -= 1
            if i > 0 and t + 1 > a:
                a = t + 1
            print i, t, a  #test
            for w in seg_content[a:i]:
                neg_temp, inver_num = wordCal(w, neg_temp, inver_num)  #
                #print w, neg_temp, inver_num  #test
            a = i + 1
            negcountlist.append(neg_temp)
            #print "negcount=" + str(negcount)
        i += 1
    poscountSorted=sorted(poscountlist)
    negcountSorted=sorted(negcountlist)
    poscount=poscountSorted[-1]+poscountSorted[0]
    negcount=negcountSorted[-1]+negcountSorted[0]
    return score_trans(poscount - negcount)