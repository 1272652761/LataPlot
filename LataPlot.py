# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 22:20:55 2017

@author: Tristone
"""
from tkinter import*
import tkinter.font as tkFont
aaa = ''
err = open('errorlog.txt','w')   #错误日志
#固定参数设置区
color = 'black'
colortree = []
width = 1000
height = width*0.618
background = '#FFFFFF'
radius = 1.5
#窗口设置区
root=Tk()
root.title('Lata Plotter')
root.resizable(False,False)
can = Canvas(root,width = width,height = height,bg = background)                    #画布创建

#--------------------------------------------------------------------------------------------------
#默认值
#--------------------------------------------------------------------------------------------------
origin1 = 0
origin2 = 0
xtick = []
ytick = []
origin1tree = []
origin2tree = []
rot = 0
strzone = 0
rottree = []
scale1 = 1
scale2 = 1
scale1tree = []
scale2tree = []
label = []
title = []
t = []         #t是一个二维数组，每个元素代表一行循环绘图语句，每个元素包含[begin,end,step,x_ptr,y_ptr],其中五个指针指向语法树
T = 1       #T啥也不是，因为他的值在具体的语句中别处指定 
T1_value = []
T2_value = []
stmt = []
#--------------------------------------------------------------------------------------------------
#词法分析器
#--------------------------------------------------------------------------------------------------
import math    #函数地址
import sys     #匹配错了跑路专用库
NULL = 0
ERROR = -1
IGNORE = -2
#the length of Type_token is 23
Token_Tab = [['CONST_ID',	"PI",	3.1415926,	NULL],['CONST_ID',	"E",2.71828,NULL],['T',"T",0.0,	NULL],['FUNC',"SIN",0.0,math.sin],
             ['FUNC',	"COS",0.0,math.cos],['FUNC',"TAN",0.0,math.tan],['FUNC',"LN",	0.0,math.log],['FUNC',"EXP",0.0,math.exp],
             ['FUNC',"SQRT",0.0,math.sqrt],['ORIGIN',"ORIGIN",0.0,NULL],['SCALE',"SCALE",0.0,NULL],['ROT',"ROT",	0.0,NULL],
             ['IS',"IS",	0.0,NULL],['FOR',"FOR",	0.0,NULL],['FROM',"FROM",0.0,	NULL],['TO',"TO",0.0,	NULL],['STEP',"STEP",0.0,NULL],
             ['DRAW',"DRAW",0.0,NULL],['SEMICO',';',NULL,NULL],['L_BRACKET','(',NULL,NULL],['R_BRACKET',')',NULL,NULL],
             ['COMMA',',',NULL,NULL],['PLUS','+',NULL,NULL],['MINUS','-',NULL,NULL],['MUL','*',NULL,NULL],['DIV','/',NULL,NULL],
             ['POWER','**',NULL,NULL],['NONTOKEN','#',NULL,NULL],['COLOR','YELLOW',NULL,NULL],['COLORS','COLOR',NULL,NULL],
             ['COLOR','BLACK',NULL,NULL],['COLOR','PINK',NULL,NULL],['COLOR','BLUE',NULL,NULL],['COLOR','GREEN',NULL,NULL],
             ['COLOR','RED',NULL,NULL],['LEGEND','LEGEND',NULL,NULL],['TITLE','TITLE',NULL,NULL],['XTICKS','XTICKS',NULL,NULL],
             ['YTICKS','YTICKS',NULL,NULL],['NUM','NUM',NULL,NULL],['FSIZE','FSIZE',NULL,NULL],['TSIZE','TSIZE',NULL,NULL],]
DFA = {'BEGIN':0,'END':[1,2,3,4,5,6,7],'chartype':['letter','digit','*','/','-','+',',',';','(',')','.',' ','\t','\n'],'TABLE':
       [{'letter':1,'digit':2,'*':4,'/':6,'-':7,'+':5,',':5,';':5,'(':5,')':5,'.':-1,' ':-2,'\t':-2,'\n':-2},           #\n\t表示是否有误
       {'letter':1,'digit':1,'*':-1,'/':-1,'-':-1,'+':-1,',':-1,';':-1,'(':-1,')':-1,'.':-1,' ':-2,'\t':-2,'\n':-2},
       {'letter':-1,'digit':2,'*':-1,'/':-1,'-':-1,'+':-1,',':-1,';':-1,'(':-1,')':-1,'.':3,' ':-2,'\t':-2,'\n':-2},
       {'letter':-1,'digit':3,'*':-1,'/':-1,'-':-1,'+':-1,',':-1,';':-1,'(':-1,')':-1,'.':-1,' ':-2,'\t':-2,'\n':-2},
       {'letter':-1,'digit':-1,'*':5,'/':-1,'-':-1,'+':-1,',':-1,';':-1,'(':-1,')':-1,'.':-1,' ':-2,'\t':-2,'\n':-2},
       {'letter':-1,'digit':-1,'*':-1,'/':-1,'-':-1,'+':-1,',':-1,';':-1,'(':-1,')':-1,'.':-1,' ':-2,'\t':-2,'\n':-2},
       {'letter':-1,'digit':-1,'*':-1,'/':5,'-':-1,'+':-1,',':-1,';':-1,'(':-1,')':-1,'.':-1,' ':-2,'\t':-2,'\n':-2},
       {'letter':-1,'digit':-1,'*':-1,'/':-1,'-':5,'+':-1,',':-1,';':-1,'(':-1,')':-1,'.':-1,' ':-2,'\t':-2,'\n':-2}]}
#the table 遇到ERROR返回-1，遇到空格什么的返回-2

#状态转移机
def smove(DFA,state,nextchar):
    TABLE = DFA['TABLE']
    if nextchar <= 'Z' and nextchar >= 'A':
        nextchar = 'letter'
    else:
        if nextchar >='0' and nextchar <= '9':
            nextchar = 'digit'
        else:
            if nextchar not in DFA['chartype']:
                err.write('Unrecognized characters.(You may have entered Chinese)\n')
                err.close()
                sys.exit()
    return TABLE[state][nextchar]

#词法分析器
def Lexer(raw_string,DFA):
    global strzone
    global aaa
    #程序代码预处理部分
    RAW_STRING = raw_string
    #将; , + ( ) 前后加上空格
    #将* / -前后加上空格
    #将** // --前后加上空格
    NEW_STRING = ''
    i = 0
    while i <= len(RAW_STRING)-1:
        if strzone == 0:
            if RAW_STRING[i] == ';' or RAW_STRING[i] == ',' or RAW_STRING[i] == '+' or RAW_STRING[i] == '(' or RAW_STRING[i] == ')':
                NEW_STRING = NEW_STRING + '\n' + RAW_STRING[i] + '\n'
            else:
                if RAW_STRING[i] == '*':
                    if RAW_STRING[i] == RAW_STRING[i+1]:
                        NEW_STRING = NEW_STRING + '\n' + RAW_STRING[i] + RAW_STRING[i+1] + '\n'
                        i = i + 1
                    else:
                        NEW_STRING = NEW_STRING + '\n' + RAW_STRING[i] + '\n'
                else:
                    if RAW_STRING[i] == '\n' or RAW_STRING[i] == '\t' or RAW_STRING[i] == ' ':
                        NEW_STRING = NEW_STRING + '\n'
                    else:
                        if RAW_STRING[i] == '/' or RAW_STRING[i] == '-':
                            if RAW_STRING[i] == RAW_STRING[i+1]:
                                NEW_STRING = NEW_STRING + '\n' + RAW_STRING[i] + RAW_STRING[i] + '\n'
                                i = i + 2 
                                while i!=len(RAW_STRING) and RAW_STRING[i] != '\n':
                                    i = i + 1
                                i = i - 1
                            else:
                                NEW_STRING = NEW_STRING + '\n' + RAW_STRING[i] + '\n'
                        else:
                            if RAW_STRING[i] == '\'':
                                strzone = 1 - strzone
                                NEW_STRING = NEW_STRING + RAW_STRING[i]
                            else:
                                NEW_STRING = NEW_STRING + RAW_STRING[i]
            i = i + 1
        else:
            if RAW_STRING[i] == '\'':
                strzone = 1 - strzone
                NEW_STRING = NEW_STRING + RAW_STRING[i]
            else:
                NEW_STRING = NEW_STRING + RAW_STRING[i]
            i = i + 1
    #给原始代码加回车
    TEMP_STRING = NEW_STRING.split('\n')
    NEW_STRING = []
    #删除无用元素并转化为大写
    for j in range(len(TEMP_STRING)):
        if TEMP_STRING[j] != '':
            if '\'' not in TEMP_STRING[j]:
                NEW_STRING.append(TEMP_STRING[j].upper())
            else:
                NEW_STRING.append(TEMP_STRING[j])
    #预处理完毕，已转化为列表NEW_STRING
    stream = []                       #返回的记号流
    for i in range(len(NEW_STRING)):
        cur_token = NEW_STRING[i]
        if cur_token[0] == '\'':
            stream.append(['STRING',cur_token[1:len(cur_token)-1],NULL,NULL])
            continue
        cur_stat = DFA['BEGIN']
        #状态转移代码，终态为cur_stat
        for j in range(len(cur_token)):
            cur_stat = smove(DFA,cur_stat,cur_token[j])
            if cur_stat == -1:    #出错时退出
                break
        #对于列表的每一个字符串元素，计算其最终态
        if cur_stat not in DFA['END']:                  #DFA状态出错时报错并增加ERRORTOKEN
            print('Error in lexer: You have an invalid word.\n')
            err.write('Error in lexer: You have an invalid word.\n')
            stream.append(['ERRORTOKEN',cur_token,NULL,NULL])
        else:                                           #DFA未出错时增加该有的token_type
            if '0' in cur_token or '1' in cur_token or '2' in cur_token or '3' in cur_token or '4' in cur_token or '5' in cur_token or '6' in cur_token or '7' in cur_token or '8' in cur_token or '9' in cur_token:                        #是数值则增加数值类型
                num = float(cur_token)
                stream.append(['NUMBER',cur_token,num,NULL])
            else:                                       #非数值则增加该有的类型
                for j in range(len(Token_Tab)):
                    if cur_token == Token_Tab[j][1]:
                        stream.append(Token_Tab[j])
    stream.append(['NONTOKEN','#',NULL,NULL])
    aaa = stream
    return stream

#--------------------------------------------------------------------------------------------------
#语法分析器
#--------------------------------------------------------------------------------------------------
#采用递归下降子程序编写
#产生式如下：
#Program  → Statement SEMICO Program |ε
#Statement →  OriginStatment | ScaleStatment |  RotStatment  | ForStatment
#OriginStatment → ORIGIN IS L_BRACKET Expression COMMA Expression R_BRACKET
#ScaleStatment  → SCALE IS L_BRACKET Expression COMMA Expression R_BRACKET
#RotStatment → ROT IS Expression
#ForStatment → FOR T FROM Expression TO Expression STEP Expression DRAW L_BRACKET Expression COMMA Expression R_BRACKET
#Expression → Term  Expression1
#Expression1→ PLUS Term Expression1| MINUS Term Expression1 |ε
#Term  → Factor Term1
#Term1 → MUL Factor Term1 | DIV Factor Term1 |ε
#Factor → PLUS Factor | MINUS Factor | Component
#Component  → Atom POWER Component | Atom
#Atom → CONST_ID  | T |  FUNC L_BRACKET  Expression  R_BRACKET |  L_BRACKET  Expression  R_BRACKET
#产生式疑点解释：
    #1.该产生式是消除了二义性的（表现在对加和乘的处理上），消除了左递归的文法
    #2.Factor表示特殊的一元运算：负数，正数与乘方
    #3.Atom表示基本的原子，但也包含了函数调用与括号改变优先级
#语法分析器主程序
idx = 0                               #词法流索引，用来标记运行到了哪个词法上
epsilon = 'NULL'                      #按空展开
#语法分析器
def Parser(raw_string):               
    stream = Lexer(raw_string,DFA)    #调用词法分析器
    RDS(stream)                             #使用递归下降子程序进行语法分析

#语法分析器的递归下降子程序实现
def RDS(stream):                      
    Program(stream)
    
#语法分析器Program
def Program(stream):
    global idx
    #按空展开
    if stream[idx][0] == 'NONTOKEN':
        return epsilon
    #匹配Statement
    Statement(stream)
    #匹配SEMICO
    if stream[idx][0] != 'SEMICO':
        print('\';\' IS REQUIRED.\n')
        err.write('\';\' IS REQUIRED.\n')
    else:
        idx = idx + 1                 #成功匹配后将其自增
    Program(stream)
    
#语法分析器Statement(python没有switchcase，心好累)
def Statement(stream):
    global stmt
    if stream[idx][0] == 'ORIGIN':
        OriginStatement(stream)
        stmt.append('ORIGIN')
    else:
        if stream[idx][0] == 'ROT':
            RotStatement(stream)
            stmt.append('ROT')
        else:
            if stream[idx][0] == 'SCALE':
                ScaleStatement(stream)
                stmt.append('SCALE')
            else:
                if stream[idx][0] == 'FOR':
                    ForStatement(stream)
                    stmt.append('FOR')
                else:
                    if stream[idx][0] == 'COLORS':
                        ColorStatement(stream)
                        stmt.append('COLORS')
                    else:
                        if stream[idx][0] == 'LEGEND':
                            LegendStatement(stream)
                            stmt.append('LEGEND')
                        else:
                            if stream[idx][0] == 'TITLE':
                                TitleStatement(stream)
                                stmt.append('TITLE')
                            else:
                                if stream[idx][0] == 'XTICKS':
                                    XticksStatement(stream)
                                    stmt.append('XTICKS')
                                else:
                                    if stream[idx][0] == 'YTICKS':
                                        YticksStatement(stream)
                                        stmt.append('YTICKS')
                                    else:
                                        print('Error in Parser: You have an invalid statement.\n')
                                        err.write('Error in Parser: You have an invalid statement.\n')
                    
def YticksStatement(stream):
    global ytick
    global idx
    idx = idx + 1
    if stream[idx][0] != 'STEP':
        print('\'STEP\' IS REQUIRED.\n')
        err.write('\'STEP\' IS REQUIRED.\n')
    else:
        idx = idx + 1
        l1 = Expression(stream)
        if stream[idx][0] != 'NUM':
            print('\'NUM\' IS REQUIRED.\n')
            err.write('\'NUM\' IS REQUIRED.\n')
        else:
            idx = idx + 1
            l2 = Expression(stream)
            if stream[idx][0] != 'TSIZE':
                print('\'TSIZE\' IS REQUIRED.\n')
                err.write('\'TSIZE\' IS REQUIRED.\n')
            else:
                idx = idx + 1
                l3 = Expression(stream)
                if stream[idx][0] != 'FSIZE':
                    print('\'FSIZE\' IS REQUIRED.\n')
                    err.write('\'FSIZE\' IS REQUIRED.\n')
                else:
                    idx = idx + 1
                    l4 = Expression(stream)
    ytick.append([l1,l2,l3,l4,NULL,NULL,NULL,NULL])
                    
def XticksStatement(stream):
    global xtick
    global idx
    idx = idx + 1
    if stream[idx][0] != 'STEP':
        print('\'STEP\' IS REQUIRED.\n')
        err.write('\'STEP\' IS REQUIRED.\n')
    else:
        idx = idx + 1
        l1 = Expression(stream)
        if stream[idx][0] != 'NUM':
            print('\'NUM\' IS REQUIRED.\n')
            err.write('\'NUM\' IS REQUIRED.\n')
        else:
            idx = idx + 1
            l2 = Expression(stream)
            if stream[idx][0] != 'TSIZE':
                print('\'TSIZE\' IS REQUIRED.\n')
                err.write('\'TSIZE\' IS REQUIRED.\n')
            else:
                idx = idx + 1
                l3 = Expression(stream)
                if stream[idx][0] != 'FSIZE':
                    print('\'FSIZE\' IS REQUIRED.\n')
                    err.write('\'FSIZE\' IS REQUIRED.\n')
                else:
                    idx = idx + 1
                    l4 = Expression(stream)
    xtick.append([l1,l2,l3,l4,NULL,NULL,NULL,NULL])

def TitleStatement(stream):
    global title
    global idx
    idx = idx + 1
    if stream[idx][0] != 'STRING':
        print('\'String\' IS REQUIRED.\n')
        err.write('\'IS\' IS REQUIRED.\n')
    else:
        strvalue = stream[idx][1]
        idx = idx + 1
        if stream[idx][0] != 'L_BRACKET':
            print('\'(\' IS REQUIRED.\n')
            err.write('\'(\' IS REQUIRED.\n')
        else:
            idx  = idx + 1
            l1 =  Expression(stream)
            if stream[idx][0] != 'COMMA':
                print('\',\' IS REQUIRED.\n')
                err.write('\',\' IS REQUIRED.\n')
            else:
                idx = idx + 1
                l2 =  Expression(stream)
                if stream[idx][0] != 'COMMA':
                    print('\',\' IS REQUIRED.\n')
                    err.write('\',\' IS REQUIRED.\n')
                else:
                    idx = idx + 1
                    l3 =  Expression(stream)
                    if stream[idx][0] != 'R_BRACKET':
                        print('\')\' IS REQUIRED.\n')
                        err.write('\')\' IS REQUIRED.\n')
                    else:
                        idx = idx + 1
                        title.append([strvalue,l1,l2,l3])

def LegendStatement(stream):
    global label
    global idx
    idx = idx + 1
    if stream[idx][0] != 'STRING':
        print('\'String\' IS REQUIRED.\n')
        err.write('\'IS\' IS REQUIRED.\n')
    else:
        strvalue = stream[idx][1]
        idx = idx + 1
        if stream[idx][0] != 'L_BRACKET':
            print('\'(\' IS REQUIRED.\n')
            err.write('\'(\' IS REQUIRED.\n')
        else:
            idx  = idx + 1
            l1 =  Expression(stream)
            if stream[idx][0] != 'COMMA':
                print('\',\' IS REQUIRED.\n')
                err.write('\',\' IS REQUIRED.\n')
            else:
                idx = idx + 1
                l2 =  Expression(stream)
                if stream[idx][0] != 'COMMA':
                    print('\',\' IS REQUIRED.\n')
                    err.write('\',\' IS REQUIRED.\n')
                else:
                    idx = idx + 1
                    l3 =  Expression(stream)
                    if stream[idx][0] != 'R_BRACKET':
                        print('\')\' IS REQUIRED.\n')
                        err.write('\')\' IS REQUIRED.\n')
                    else:
                        idx = idx + 1
                        label.append([strvalue,l1,l2,l3])

def ColorStatement(stream):
    global idx
    idx = idx + 1
    if stream[idx][0] != 'IS':
        print('\'IS\' IS REQUIRED.\n')
        err.write('\'IS\' IS REQUIRED.\n')
    else:
        idx = idx + 1
        if stream[idx][0] != 'COLOR':
            print('\'COLOR\' IS REQUIRED.\n')
            err.write('\'COLOR\' IS REQUIRED.\n')
        else:
            colortree.append(stream[idx][1])
            idx = idx + 1
            

def OriginStatement(stream):
    global idx
    global origin1
    global origin2
    global origin1tree
    global origin2tree
    idx = idx + 1
    if stream[idx][0] != 'IS':
        print('\'IS\' IS REQUIRED.\n')
        err.write('\'IS\' IS REQUIRED.\n')
    else:
        idx = idx + 1
        if stream[idx][0] != 'L_BRACKET':
            print('\'(\' IS REQUIRED.\n')
            err.write('\'(\' IS REQUIRED.\n')
        else:
            idx = idx + 1
            origin1tree.append(Expression(stream)) 
            if stream[idx][0] != 'COMMA':
                print('\',\' IS REQUIRED.\n')
                err.write('\',\' IS REQUIRED.\n')
            else:
                idx = idx + 1
                origin2tree.append(Expression(stream)) 
                if stream[idx][0] != 'R_BRACKET':
                    print('\')\' IS REQUIRED.\n')
                    err.write('\')\' IS REQUIRED.\n')
                else:
                    idx = idx + 1

def RotStatement(stream):
    global idx
    global rot
    global rottree
    idx = idx + 1
    if stream[idx][0] != 'IS':
        print('\'IS\' IS REQUIRED.\n')
        err.write('\'IS\' IS REQUIRED.\n')
    else:
        idx = idx + 1
        rottree.append(Expression(stream))

def ScaleStatement(stream):
    global idx
    global scale1
    global scale2
    global scale1tree
    global scale2tree
    idx = idx + 1
    if stream[idx][0] != 'IS':
        print('\'IS\' IS REQUIRED.\n')
        err.write('\'IS\' IS REQUIRED.\n')
    else:
        idx = idx + 1
        if stream[idx][0] != 'L_BRACKET':
            print('\'(\' IS REQUIRED.\n')
            err.write('\'(\' IS REQUIRED.\n')
        else:
            idx = idx + 1
            scale1tree.append(Expression(stream))
            if stream[idx][0] != 'COMMA':
                print('\',\' IS REQUIRED.\n')
                err.write('\',\' IS REQUIRED.\n')
            else:
                idx = idx + 1
                scale2tree.append(Expression(stream))
                if stream[idx][0] != 'R_BRACKET':
                    print('\')\' IS REQUIRED.\n')
                    err.write('\')\' IS REQUIRED.\n')
                else:
                    idx = idx + 1
    

def ForStatement(stream):
    global idx
    global t
    result = []
    idx = idx + 1
    if stream[idx][0] != 'T':
        print('\'T\' IS REQUIRED.\n')
        err.write('\'T\' IS REQUIRED.\n')
    else:
        idx = idx + 1
        if stream[idx][0] != 'FROM':
            print('\'FROM\' IS REQUIRED.\n')
            err.write('\'FROM\' IS REQUIRED.\n')
        else:
            idx = idx + 1
            result.append(Expression(stream))
            if stream[idx][0] != 'TO':
                print('\'TO\' IS REQUIRED.\n')
                err.write('\'TO\' IS REQUIRED.\n')
            else:
                idx = idx + 1
                result.append(Expression(stream))
                if stream[idx][0] != 'STEP':
                    print('\'STEP\' IS REQUIRED.\n')
                    err.write('\'STEP\' IS REQUIRED.\n')
                else:
                    idx = idx + 1
                    result.append(Expression(stream))
                    if stream[idx][0] != 'DRAW':
                        print('\'DRAW\' IS REQUIRED.\n')
                        err.write('\'DRAW\' IS REQUIRED.\n')
                    else:
                        idx = idx + 1
                        if stream[idx][0] != 'L_BRACKET':
                            print('\'(\' IS REQUIRED.\n')
                            err.write('\'(\' IS REQUIRED.\n')
                        else:
                            idx = idx + 1
                            result.append(Expression(stream))
                            if stream[idx][0] != 'COMMA':
                                print('\',\' IS REQUIRED.\n')
                                err.write('\',\' IS REQUIRED.\n')
                            else:
                                idx = idx + 1
                                result.append(Expression(stream))
                                if stream[idx][0] != 'R_BRACKET':
                                    print('\')\' IS REQUIRED.\n')
                                    err.write('\')\' IS REQUIRED.\n')
                                else:
                                    idx = idx + 1
    t.append(result)

class Node(object):
    def __init__(self):
        self.type = None         #五种类型（常量,T,函数,一元操作符（正负），二元操作符（加减乘除,乘方））（CON是常量，VAR是T，SINGLE是一元，DOUBLE是二元）
        self.lexeme = None       #是啥类就写啥类，不必理会这冷笑与暗箭
        self.lchild = None       #常量时存值，T时存引用地址
        self.rchild = None



#Expression → Term  Expression1
#Expression1→ PLUS Term Expression1| MINUS Term Expression1 |ε   #需要参数
#Term  → Factor Term1
#Term1 → MUL Factor Term1 | DIV Factor Term1 |ε                  #需要参数
def Expression(stream):
    lchild = Term(stream)
    result = Expression1(stream,lchild)
    return result

def Expression1(stream,lchild):
    global idx
    if stream[idx][0] == 'PLUS':
        idx = idx + 1
        mid = Node()
        mid.type = 'DOUBLE'
        mid.lexeme = 'PLUS'
        mid.lchild = lchild
        mid.rchild = Term(stream)
        result = Expression1(stream,mid)
    else:
        if stream[idx][0] == 'MINUS':
            idx = idx + 1
            mid = Node()
            mid.type = 'DOUBLE'
            mid.lexeme = 'MINUS'
            mid.lchild = lchild
            mid.rchild = Term(stream)
            result = Expression1(stream,mid)
        else:
            result = lchild
    return result

def Term(stream):
    lchild = Factor(stream)
    result = Term1(stream,lchild)
    return result

def Term1(stream,lchild):
    global idx
    if stream[idx][0] == 'MUL':
        idx = idx + 1
        mid = Node()
        mid.type = 'DOUBLE'
        mid.lexeme = 'MUL'
        mid.lchild = lchild
        mid.rchild = Factor(stream)
        result = Term1(stream,mid)
    else:
        if stream[idx][0] == 'DIV':
            idx = idx + 1
            mid = Node()
            mid.type = 'DOUBLE'
            mid.lexeme = 'DIV'
            mid.lchild = lchild
            mid.rchild = Factor(stream)
            result = Term1(stream,mid)
        else:
            result = lchild
    return result
#Factor → PLUS Factor | MINUS Factor | Component
#Component  → Atom POWER Component | Atom
#Atom → CONST_ID  | T |  FUNC L_BRACKET  Expression  R_BRACKET |  L_BRACKET  Expression  R_BRACKET
def Factor(stream):
    global idx
    if stream[idx][0] == 'PLUS':
        idx = idx + 1
        mid = Node()
        mid.type = 'SINGLE'
        mid.lexeme = 'PLUS1'
        mid.lchild = Term(stream)
    else:
        if stream[idx][0] == 'MINUS':
            idx = idx + 1
            mid = Node()
            mid.type = 'SINGLE'
            mid.lexeme = 'MINUS1'
            mid.lchild = Term(stream)
        else:
            mid = Component(stream)
    return mid

def Component(stream):
    global idx
    left = Atom(stream)
    if stream[idx][0] == 'POWER':
        idx = idx + 1
        mid = Node()
        mid.type = 'SINGLE'
        mid.lexeme = 'POWER'
        mid.lchild = left
        mid.rchild = Component(stream)
        result = mid
    else:
        result = left
    return result

def Atom(stream):
    global idx
    global T
    if stream[idx][0] == 'CONST_ID' or stream[idx][0] == 'NUMBER':
        result = Node()
        result.type = 'CON'
        result.lchild = stream[idx][2]
        idx = idx + 1
    else:
        if stream[idx][0] == 'T':
            result = Node()
            result.type = 'VAR'
            
            result.lchild = T
            idx = idx + 1
        else:
            if stream[idx][0] == 'FUNC':
                result = Node()
                result.type = 'FUNC'
                result.lexeme = stream[idx][3]
                idx = idx + 1
                if stream[idx][0] == 'L_BRACKET':
                    idx = idx + 1
                    result.lchild = Expression(stream)
                    if stream[idx][0] != 'R_BRACKET':
                        print('\' ) \'IS REQUIRED.\n')
                        err.write('\' ) \'IS REQUIRED.\n')
                    else:
                        idx = idx + 1
            else:
                if stream[idx][0] == 'L_BRACKET':
                    idx = idx + 1
                    result = Expression(stream)
                    if stream[idx][0] != 'R_BRACKET':
                        print('\' ) \'IS REQUIRED.\n')
                        err.write('\' ) \'IS REQUIRED.\n')
                    else:
                        idx = idx + 1
                else:
                    print('Current expression is not available.\n')
                    err.write('Current expression is not available.\n')
                    sys.exit()      
    return result

#--------------------------------------------------------------------------------------------------
#语义分析器
#--------------------------------------------------------------------------------------------------
#节点类型
#两元操作符
    #PLUS MINUS MUL DIV POWER
#一元操作符
    #PLUS1 MINUS1
#FUNC
#CON
#VAR
#origin1 = 0
#origin2 = 0
#rot = 0
#scale1 = 1
#scale2 = 1
#t = []         #t是一个二维数组，每个元素代表一行循环绘图语句，每个元素包含[begin,end,step,x_ptr,y_ptr],其中五个指针指向语法树
#T = None
def Semantic():
    global origin1
    global origin2
    global rot
    global scale1
    global scale2
    global t
    global T
    global T1_value
    global T2_value
    global origin1tree
    global origin2tree
    global rottree
    global scale1tree
    global scale2tree
    global color
    c = 0
    o = 0
    r = 0
    s = 0
    f = 0
    la = 0
    ti = 0
    xi = 0
    yi = 0
    for l in range(len(stmt)):
        if stmt[l] == 'ORIGIN':
            origin1 = Tree2Num(origin1tree[o])
            origin2 = Tree2Num(origin2tree[o])
            o = o + 1
        else:
            if stmt[l] == 'ROT':
                rot = Tree2Num(rottree[r])
                r = r + 1
            else:
                if stmt[l] == 'SCALE':
                    scale1 = Tree2Num(scale1tree[s])
                    scale2 = Tree2Num(scale2tree[s])
                    s = s + 1
                else:
                    if stmt[l] == 'COLORS':
                        color = colortree[c]
                        c = c + 1
                    else:
                        if stmt[l] == 'LEGEND':
                            label[la][1], label[la][2], label[la][3] = Tree2Num(label[la][1]), Tree2Num(label[la][2]), Tree2Num(label[la][3])
                            la = la + 1
                        else:
                            if stmt[l] == 'TITLE':
                                title[ti][1], title[ti][2], title[ti][3] = Tree2Num(title[ti][1]), Tree2Num(title[ti][2]), Tree2Num(title[ti][3])
                                ti = ti + 1
                            else:
                                if stmt[l] == 'XTICKS':
                                    xtick[xi][0],xtick[xi][1],xtick[xi][2],xtick[xi][3],xtick[xi][4],xtick[xi][5],xtick[xi][6],xtick[xi][7] = Tree2Num(xtick[xi][0]),Tree2Num(xtick[xi][1]),Tree2Num(xtick[xi][2]),Tree2Num(xtick[xi][3]),origin1,origin2,scale1,color
                                    xi = xi + 1
                                else:
                                    if stmt[l] == 'YTICKS':
                                        ytick[yi][0],ytick[yi][1],ytick[yi][2],ytick[yi][3],ytick[yi][4],ytick[yi][5],ytick[yi][6],ytick[yi][7] = Tree2Num(ytick[yi][0]),Tree2Num(ytick[yi][1]),Tree2Num(ytick[yi][2]),Tree2Num(ytick[yi][3]),origin1,origin2,scale2,color
                                        yi = yi + 1
                                    else:
                                        for j in range(5):
                                            if j == 3:
                                                num = int((t[f][1] - t[f][0])/t[f][2]) + 1
                                                for h in range(num):
                                                    T = float(h)*t[f][2] + t[f][0]
                                                    T1_value.append([Tree2Num(t[f][j]),origin1,origin2,rot,scale1,scale2,color])
                                            else:
                                                if j == 4:
                                                    num = int((t[f][1] - t[f][0])/t[f][2]) + 1
                                                    for h in range(num):
                                                        T = float(h)*t[f][2] + t[f][0]
                                                        T2_value.append([Tree2Num(t[f][j]),origin1,origin2,rot,scale1,scale2,color])
                                                    f = f + 1
                                                else:
                                                    t[f][j] = Tree2Num(t[f][j])

#将语法树转化为浮点数字
def Tree2Num(node):
    global T
    if node.lexeme == 'PLUS':
        result = Tree2Num(node.lchild) + Tree2Num(node.rchild)
    else:
        if node.lexeme == 'MINUS':
            result = Tree2Num(node.lchild) - Tree2Num(node.rchild)
        else:
            if node.lexeme == 'MUL':
                result = Tree2Num(node.lchild) * Tree2Num(node.rchild)
            else:
                if node.lexeme == 'DIV':
                    if Tree2Num(node.rchild) == 0:
                        print('You can\'t divide a number with 0.\n')
                        err.write('You can\'t divide a number with 0.\n')
                        sys.exit()  
                    else:
                        result = Tree2Num(node.lchild) / Tree2Num(node.rchild)
                else:
                    if node.lexeme == 'POWER':
                        result = math.pow(Tree2Num(node.lchild),Tree2Num(node.rchild))
                    else:
                        if node.lexeme == 'PLUS1':
                            result = Tree2Num(node.lchild)
                        else:
                            if node.lexeme == 'MINUS1':
                                result = -Tree2Num(node.lchild)
                            else:
                                if node.type == 'FUNC':
                                    result = node.lexeme(Tree2Num(node.lchild))
                                else:
                                    if node.type == 'CON':
                                        result = node.lchild
                                    else:
                                        if node.type == 'VAR':
                                            result = T
    return result
#--------------------------------------------------------------------------------------------------
#分析器运行脚本
#--------------------------------------------------------------------------------------------------

f = open('lataplot.txt')
raw_string = f.read()
f.close()
Parser(raw_string)
Semantic()
    #--------------------------------------------------------------------------------------------------
    #语义解释器
    #--------------------------------------------------------------------------------------------------
    #将坐标转化为绘图点
def Trans(x,y,xp,yp):    
    x_tran = xp + x
    y_tran = yp - y
    return x_tran,y_tran
    
    #语法分析变量设置区
    #xp,yp:转化后的原点坐标
    #scale:像素与坐标值的转化比例
    #T1_value,T2_value:分别为转化后可以直接画的坐标

#坐标变换
for i in range(len(T1_value)):                 #这个循环用来做尺度变换
    T1_value[i][0] = T1_value[i][0] * T1_value[i][4]
    T2_value[i][0] = T2_value[i][0] * T2_value[i][5]
for i in range(len(xtick)):
    xtick[i][0] = xtick[i][0]*xtick[i][6]
for i in range(len(ytick)):
    ytick[i][0] = ytick[i][0]*ytick[i][6]
    
for i in range(len(T1_value)):                 #这个循环用来做旋转变换+平移变换
    x1 = T1_value[i][0] * math.cos(T1_value[i][3]) + T2_value[i][0] * math.sin(T2_value[i][3])
    y1 = T2_value[i][0] * math.cos(T2_value[i][3]) - T1_value[i][0] * math.sin(T1_value[i][3])
    T1_value[i][0] = x1
    T2_value[i][0] = y1
for i in range(len(T1_value)):                 #原始坐标转化为真实坐标
    T1_value[i][0],T2_value[i][0] = Trans(T1_value[i][0],T2_value[i][0],T1_value[i][1],height - T1_value[i][2])
        
#图形绘制
for i in range(len(xtick)):                    #xtick语句
    for j in range(int(xtick[i][1])):
        point = xtick[i][4] + xtick[i][0]*(j+1)
        ft = tkFont.Font(family = 'Times',size = int(xtick[i][3]),weight = tkFont.BOLD)
        txt = can.create_text((point,height - xtick[i][5] + int(xtick[i][3])),font = ft,text = str(int(xtick[i][0]/xtick[i][6]*(j+1))))
        can.create_line(point,height - xtick[i][5],point,height - xtick[i][5] - xtick[i][2],fill=xtick[i][7])
for i in range(len(ytick)):                    #ytick语句
    for j in range(int(ytick[i][1])):
        point = height - ytick[i][5] - ytick[i][0]*(j+1)
        stry = str(int(ytick[i][0]/ytick[i][6]*(j+1)))
        length = int(len(stry)/2)+1
        ft = tkFont.Font(family = 'Times',size = int(ytick[i][3]),weight = tkFont.BOLD)
        txt = can.create_text((ytick[i][4] -  length * int(ytick[i][3]) ,point),font = ft,text = stry)
        can.create_line(ytick[i][4],point,ytick[i][4] + ytick[i][2],point,fill=ytick[i][7],width =2)

for i in range(len(title)):                    #TITLE语句
    ft = tkFont.Font(family = 'Helvetica',size = int(title[i][3]),weight = tkFont.BOLD)
    txt = can.create_text((title[i][1],title[i][2]),font = ft,text = title[i][0])
for i in range(len(label)):                    #LEGEND语句
    ft = tkFont.Font(family = 'Times',size = int(label[i][3]),weight = tkFont.BOLD)
    txt = can.create_text((label[i][1],label[i][2]),font = ft,text = label[i][0])
for i in range(len(T1_value)):                 #FOR语句
    can.create_oval(T1_value[i][0]-radius,T2_value[i][0]-radius,T1_value[i][0]+radius,T2_value[i][0]+radius,fill = T1_value[i][6])
can.pack()
root.mainloop()
err.close()
