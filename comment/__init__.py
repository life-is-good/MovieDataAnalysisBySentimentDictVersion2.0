# -*- coding: utf-8 -*-
import re  # 模块re：包含正则表达式的所有方法
from cal_score import sentimentScoreStar #模块cal_score:提供计算分数的函数方法
import os  # 模块os：提供了一个统一的操作系统接口函数
import codecs  # 模块codecs：编码转换
from utils import splitsentence as ss   #模块utils里面的splitsentence：对句子进行按照关键字重组

# 将filepath文件中的内容，分成行，并去掉其中空行后，加到data
def get_data(filepath):
    fileHandler = open(filepath)  # 对象fileHanlder：打开文件filepath，读取到fileHandler
    data = fileHandler.read()  # data：一次读取fileHandler全部内容到data
    if data[:3] == codecs.BOM_UTF8:  # 某些软件，如notepad，在保存一个以UTF-8编码的文件时，会在文件开始的地方插入三个不可见的字符（0xEF 0xBB 0xBF，即BOM)，若有，去除这三个字符
        data = data[3:]
    if data[-1] == '\n':
        # 除去最后一个换行符#
        data = data[:-1]
    _data = data.decode('utf-8').split('\n')  # 列表_data:将data用utf-8编码后按行分割，存储到_data
    data = []  # data：赋为空
    for word in _data:  # 将_data中的空行去掉，然后赋给data(此处只能去掉空行，而不能去掉有几个空格组成的行)
        if word != u'':
            # 添加元素#
            data.append(word)
    return data  # 返回data


classification = []  # classfication:对应评分项，顺序自己定
classification2 = [] # classfication2:对应关键词，顺序自己定
classification3 = [] # classfication3:对应关键词，顺序系统定
classification4 = [] #classfication4:对应关键字的列表集合
                
kw_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'keywords')  # 获取当前脚本文件路径并在其后加上\keywords
# os.listdir 获得当前目录中的内容#
for kw_file in os.listdir(kw_path):  # 获取kw_path目录下所有文件，并将每个文件变成列表data模式，然后再添加到列表classfication
    classification3.append(get_data(os.path.join(kw_path, kw_file)))
    classification4.extend(get_data(os.path.join(kw_path, kw_file)))
 
for category in classification3:
    if category[0] == u'剧情':
        classification2.append(category[0])
        classification.append([u'剧情评分'])
        break

for category in classification3:
    if category[0] == u'摄影':
        classification2.append(category[0])
        classification.append([u'摄影评分'])      
        break
        
for category in classification3:
    if category[0] == u'特效':
        classification2.append(category[0])
        classification.append([u'特效评分'])      
        break

for category in classification3:
    if category[0] == u'音乐':
        classification2.append(category[0])
        classification.append([u'音乐评分'])
        break

for category in classification3:
    if category[0] == u'导演':
        classification2.append(category[0])
        classification.append([u'导演评分'])      
        break
    
for category in classification3:
    if category[0] == u'演技':
        classification2.append(category[0])
        classification.append([u'演技评分'])      
        break
    
for category in classification3:
    if category[0] == u'颜':
        classification2.append(category[0])
        classification.append([u'颜值评分'])      
        break


classification.append([u'总评', u''])  # classfication里添加总评和空字符
classification2.append(u'总评')

path = os.path.dirname(os.path.abspath(__file__))

posMVdict = get_data(path + '/sentiment dictionary/positive and negative dictionary/posdict.txt')  # 肯定极性
negMVdict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negdict.txt')  # 否定极性
posdaoyandict = get_data(path + '/sentiment dictionary/positive and negative dictionary/posdict.txt')  # 肯定极性
negdaoyandict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negdict.txt')  # 否定极性
posstardict = get_data(path + '/sentiment dictionary/positive and negative dictionary/posdict.txt')  # 肯定极性
negstardict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negdict.txt')  # 否定极性

disstatusdict=get_data(path + '/sentiment dictionary/disturb dictionary/disturb status.txt')
diskeydict=get_data(path + '/sentiment dictionary/disturb dictionary/disturb keyword.txt')


#classification2.append(diskeydict)

# 类Comment：评价类
class Comment:
    def __init__(self, contents):  
        self.contents = contents  #contents:评价内容
        self.score = {}           #score:字典类型的分数，对应关键字和分数
        self.averagescore = 0
        
    def calScore(self):
        key_sent_dict = {}#关键词对应句子的字典
        key_sent_dict = ss.splitsentence(classification3,classification4,self.contents)
        
        for key,sent in key_sent_dict.items():
            if key != u"无关键字":
                for sent_disturb in disstatusdict:
                    sentDel = sent.replace(sent_disturb,"")
                for sentiment_word in posMVdict+negMVdict:
                    if sentDel.find(sentiment_word) != -1:
                        sent = sent.replace(sentiment_word,sentiment_word+u"，")
                        s = sentimentScoreStar(sent,classification4)
                        self.score.setdefault(key,s) #对应关键词打出分数
                    #self.score[key].append(s)#对应关键词打出分数
                    #self.score[-1].append(s) #总分数
                        break

    def printScore(self):
        sum = 0
        for k,v in self.score.items():
            print k+':'+str(v)
            sum = sum + v
        if len(self.score) != 0:
            self.averagescore = sum/len(self.score)
        else:
            pass
        self.score.setdefault(u"总评",self.averagescore)
        print "总评："+str(self.averagescore)
