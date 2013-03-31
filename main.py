#!/usr/bin/env python
# coding=utf-8
#        中文词频分词算法练习
#        C19<classone2010@gmail.com>
#        算法源自http://www.matrix67.com/blog/archives/5044
#        效率低下仅供好玩
from math import log
from time import sleep
import collections;Counter = collections.Counter
#{word:{'lnei':[],'rnei':[],'freq':0.222,....}
def gen_words(origin_str,maxlength=2):
    #将所有可能的文字切片列出。并统计好其出现频率及所有左右邻字  增加认可的词的长度会让内存占用翻倍增长。。内存多的同学可以玩玩。
    i = 1
    words = {}
    maxlength = maxlength+1
    totallength = len(origin_str)
    for j in range(1,maxlength):
        for i in range(1,len(origin_str)-j+1):
            aslice = origin_str[i:i+j]
            if words.__contains__(aslice):
                words[aslice]['freq'] += 1
            else:
                if len(aslice) > 1:
                    words.update({aslice:{'lnei':[],'rnei':[],'freq':1}})
                else:
                    words.update({aslice:{'freq':1}})
            if len(aslice) > 1:
                lnei = origin_str[i-1:i] if i-1>0 else None
                rnei = origin_str[i+j:i+j+1] if i+j+1 <= totallength-j+1 else None
                if lnei:words[aslice]['lnei'].append(lnei)
                if rnei:words[aslice]['rnei'].append(rnei)
        ''''i += 1
        i %= 1000
        if i == 1:sleep(0.001)'''
    for word in words:
        words[word]['freq'] = words[word]['freq']/totallength*len(word)
    return words

cutter = lambda tmp:[(tmp[:i],tmp[i:]) for i in range(1,len(tmp))]

#得分综合
def point_count(words):
        for word in words:
            if len(word) > 1:
                words[word].update({'poly':_poly_count(word,words)})
        return {word:{'freq':words[word]['freq'],
                      'poly':_poly_count(word,words),
                      'flex':_flex_count(word,words)} for word in words if _point_count(word,words) > 10**(-5)}
def _point_count(word,words):
    try:
        if len(word) <= 1:return False
        return words[word]['freq']*_poly_count(word,words)*_flex_count(word,words)
    except Exception as e:
        print(e)
#自由度
def _flex_count(word,words,i=1):
    return min(__flex_count(words[word]['lnei']),__flex_count(words[word]['rnei']))
def __flex_count(neighbors):
    counter = Counter(neighbors)
    length  = len(neighbors)
    if length == 0:return 1
    entropy = sum([-(counter[a]/length)*log(counter[a]/length) for a in counter])
    return entropy
#聚合度
def _poly_count(aslice, words):
    try:
        if len(aslice) == 1:return 1
        m = max([words[s1]['freq']*words[s2]['freq'] for s1,s2 in cutter(aslice)])
        return words[aslice]['freq']/m if m > 0 else 1
    except Exception as e:
        print(e)


ori = open('material.txt','r',encoding='utf8').read()

words = gen_words(ori)
words = point_count(words)  
result = [word for word,value in sorted(words.items(),key = lambda n:n[1]['poly']*n[1]['flex']*n[1]['freq'],reverse=True)]
open('result.txt','w+').write(result.__repr__())
print('ok')


