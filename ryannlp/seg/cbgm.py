#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Ryan Liu
# Created Time : 2014年03月05日 星期三 20时19分30秒


from __future__ import division
import sys
sys.path.append('../core')
from core import frenquency
import math

class CharacterBasedGenerativeModel(object):
    """This is character based generatve model for taging"""
    def __init__(self):

        self.uni = frenquency.NormalProb()
        self.big = frenquency.NormalProb()
        self.tri = frenquency.NormalProb()

        self.lam1 = self.lam2 = self.lam3 = 0.0

        self.allState = ('b','m','e','s')

        self.wordState  = {}

    def train(self,data):

        for sentence in data:
            tagnow = [('','P'),('','P')]
            #sentence.append((u'EOF',u'EOF')) # Add a EOS to every sentence

            for word,tag in sentence:

                self.wordState.setdefault(word,set())
                self.wordState[word].add(tag)

                tagnow.append((word,tag)) # Use word tag pair to process following

                self.uni.add((word,tag),1)
                self.big.add(tuple(tagnow[1:]),1)
                self.tri.add(tuple(tagnow[:]),1)

                tagnow = tagnow[1:]

        t1 = t2 = t3 = 0 # Delete insertion 

        for item in self.tri.allItems():

            case3 = 0 if (self.big.getCount(item[:2]) - 1 ) == 0 else (self.tri.getCount(item) - 1)     / (self.big.getCount(item[:2]) - 1)

            case2 = 0 if (self.uni.getCount(item[1]) - 1)   == 0 else (self.big.getCount(item[1:]) -1 ) / (self.uni.getCount(item[1]) - 1)

            case1 = 0 if (self.uni.getTotle() - 1)          == 0 else (self.uni.getCount(item[2]) -1 )  / (self.uni.getTotle() - 1)


            if case3 >= case2 and case3 >= case1:
                t3 += self.tri.getCount(item)

            elif case2 >= case1 and case2 >= case3:
                t2 += self.tri.getCount(item)

            elif case1 >= case2 and case1 >= case3:
                t1 += self.tri.getCount(item)

        self.lam1 = float(t1)/(t1+t2+t3)
        self.lam2 = float(t2)/(t1+t2+t3)
        self.lam3 = float(t3)/(t1+t2+t3)

    def log_prob(self,s1,s2,s3):

        unif = self.lam1 * self.uni.getCount(s3) / self.uni.getTotle()
        bigf = 0 if self.uni.getCount(s2) == 0      else self.lam2 * self.big.getCount((s2,s3)) / self.uni.getCount(s2)
        trif = 0 if self.big.getCount((s1,s2)) == 0 else self.lam3 * self.tri.getCount((s1,s2,s3))/self.big.getCount((s1,s2))

        if unif + bigf + trif == 0:
            return float('-300')
        return math.log(unif+bigf+trif)

    def interpretSeg(self,data):
        temp = ""
        wordset = []

        for item in data:
            if item[1] == u'P':
                continue
            elif item[1] == u'e':
                temp += item[0]
                wordset.append(temp)
                temp = ""
            elif item[1] == u'EOF':
                if temp:
                    wordset.append(temp)
            elif item[1] == u'b' or item[1] == u's':
                if temp:
                    wordset.append(temp)
                temp = item[0]
            else:
                temp += item[0]

        return wordset

    def seg(self,sentence):
        tagnow = [ [ ( (u'',u'P'),(u'',u'P') ),   0.0] ]
        for word in sentence:
            #print word
            stateset = self.wordState.get(word,self.allState)
            #print stateset

            tagpre = tagnow[:]

            tagnow = []
            tagtemp = {}

            for state in stateset:
                for item in tagpre:

                    tritutle = (item[0][-2],item[0][-1],(word,state))

                    probnow = item[1]
                    probnow += self.log_prob(*tritutle)

                    statenow = list(item[0])
                    statenow.append((word,state))

                    if (statenow[-2],statenow[-1]) not in tagtemp or probnow > tagtemp[(statenow[-2],statenow[-1])][1]:
                        tagtemp[(statenow[-2],statenow[-1])] = [tuple(statenow),probnow]

                    #tagtemp.append([tuple(statenow),probnow])
                #print tagtemp
                #print tagtemp
                #findmax = max(tagtemp,key=lambda x:x[1])

            tagnow = tagtemp.values()
            #tagnow.append(findmax)
        tagnow = sorted(tagnow,key=lambda x:x[1],reverse = True)[0]
        tagnow = tagnow[0]
        return self.interpretSeg(tagnow)

