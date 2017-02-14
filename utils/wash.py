# -*- coding: utf-8 -*-
import os
import xlwt
import xlrd
import ConfigParser
import codecs

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

#清洗
def wash(sheet_num,column_comment_num,old_input_file,col_comment,nrows):
    #读取关键字
    classification = []              
    kw_path = os.path.join(os.getcwd(),'comment\keywords')  # 获取当前脚本文件路径并在其后加上\keywords
    for kw_file in os.listdir(kw_path):  # 获取kw_path目录下所有文件，并将每个文件变成列表data模式，然后再添加到列表classfication
        classification.extend(get_data(os.path.join(kw_path, kw_file)))
            
    #包含关键字的和不包含关键字的列表
    includekeywords = []
    nokeywords = []
    for i in range(nrows):
        flag = 0#测试是否存到有关键字的列表里面
        for word in classification:
            if word in col_comment[i]:
                flag = 1
                includekeywords.append(col_comment[i])
                break
        if flag == 0:
            nokeywords.append(col_comment[i])

    #将包含关键字的写到新的文件中
    new_table = xlwt.Workbook()
    sheet = new_table.add_sheet("include")
    sheet.write(0,0,u"包含关键词的评论")
    includekeywords = list(set(includekeywords))#去重      
    for i in range(len(includekeywords)):
        sheet.write(i+1,0,includekeywords[i])
    new_table.save(os.getcwd()+'\\new_table.xls')
    
    #将不包含关键字的写到新的文件中
    new_no_table = xlwt.Workbook()
    sheet = new_no_table.add_sheet("noinclude")
    sheet.write(0,0,u"不包含关键词的评论")
    nokeywords = list(set(nokeywords))     
    for i in range(len(nokeywords)):
        sheet.write(i+1,0,nokeywords[i])
    new_no_table.save(os.getcwd()+'\\new_no_table.xlsx')    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
