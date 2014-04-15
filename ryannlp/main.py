#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Ryan Liu
# Created Time : 2014年03月27日 星期四 09时36分02秒
import spell.spell
from spell import *

import seg.seg
from seg import *

import tag.tag
from tag import *

#import textrank.textrank
#from textrank import *


class RyanNLP(object):
    """This is the basic class, combine all the functions using
    in Chinese language processing"""
    def __init__(self,docs):
        self.docs = docs;

        self.speller = spell.Spell()

        self.segger = seg.Seg()

        self.tagger = tag.Tag()

        #self.word_rank = textrank.KeywordTextRank(docs)

        self.train()

    def setMeta(self,docs):
        self.docs = docs

    @property
    def simp(self):
        return toSimple(self.docs)

    @property
    def comp(self):
        return toComple(self.docs)

    @property
    def spell(self):#Spell the Chinese words
        return self.speller.toSpell(self.docs)
        pass

    @property
    def gen(self):
        try:
            self.docs = self.docs.strip().split()
        except:
            pass
        return self.speller.genSentence(self.docs)
        pass

    @property
    def words(self):
        self.temp = self.segger.segger.seg(list(self.docs))
        return " ".join(self.temp)

    @property
    def tag(self):
        self.temp = self.docs.split(' ')
        if len(self.temp) == 1:
            self.temp = self.segger.segger.seg(list(self.docs))

        return self.tagger.tagger.tag(self.temp)
        pass

    def extractWord(self,num=1):
        #self.word_rank = textrank.KeywordTextRank(docs)
        #self.word_rank.solve
        #self.get_top(num)
        pass

    def extractSentence(self,num=1):
        pass

    @property
    def classfication(self):
        pass

    @property
    def sentiment(self):
        pass

    def train(self):
        #self.speller.train('spell/dCorpus.txt')
        self.segger.train('seg/data.txt')
        #self.tagger.train('tag/1998011.txt')
        pass



if __name__ == "__main__":
    
    m = RyanNLP(u"在最威胁手机领域里，手机很好")
    print m.words
    #print m.simp

    #m.docs = m.simp
    #print m.comp

    #m.docs = u"重复的完成繁重的任务"
    #print m.spell


    #m.setMeta(u"今天天气不错，挺风和日丽的。")
    #print m.seg
    #print m.tag

