#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Ryan Liu
# Created Time : 2014年03月27日 星期四 09时36分02秒
from spell import *


class RyanNLP(object):
    """This is the basic class, combine all the functions using
    in Chinese language processing"""

    def __init__(self,docs):
        self.docs = docs;

    @property
    def simp(self):
        return toSimple(self.docs)

    @property
    def comp(self):
        return toComple(self.docs)

    @property
    def spell(self):#Spell the Chinese words
        pass

    @property
    def gen(self):
        pass

    @property
    def seg(self):
        pass

    @property
    def tag(self):
        pass

    def extractWord(self,num=1):
        pass

    def extractSentence(self,num=1):
        pass

    @property
    def classfication(self):
        pass

    @property
    def sentiment(self):
        pass

    def train(self,train_type,data):
        pass



if __name__ == "__main__":
    
    m = RyanNLP(u"本条目當前的標題「繁体中文」為暫定名稱，可能為原創、不准确或者具爭議性。 ... 注意：本條目可能有部分字元無法顯示，")
    st =  m.simp
    k = RyanNLP(st)
    print k.comp