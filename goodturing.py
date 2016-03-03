# -*- coding:utf-8 -*-
'''
Created on 2015年12月26日

@author: yuxuan
'''
import codecs
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class good_turing():
    def __init__(self):
        self.LexiconHead = []
        self.bigram_dict = []
        self.dict_bigram_num = dict()
        self.dict_word_num = dict()
        self.word_sum = 0
        #self.bigram_not_zero = 0

    def load_freq(self):
        logging.info("load word_freq.txt..")
        word_freq = codecs.open('word_freq.txt', 'r', 'gbk')
        for lines in word_freq.readlines():
            words = lines.strip().split('\t')
            if int(words[1]) not in self.dict_word_num:
                self.dict_word_num[int(words[1])] = 1
            else:
                self.dict_word_num[int(words[1])] += 1
            self.LexiconHead.append([words[0],int(words[1]),0])
            self.word_sum += int(words[1])
        word_freq.close()
        logging.info("load bigram_freq.txt..")
        bigram_freq = codecs.open('bigram_freq.txt', 'r', 'gbk')
        for lines in bigram_freq.readlines():
            words = lines.strip().split('\t')
            if int(words[2]) not in self.dict_bigram_num:
                self.dict_bigram_num[int(words[2])] = 1
            else:
                self.dict_bigram_num[int(words[2])] += 1
            self.bigram_dict.append([(words[0],words[1]), int(words[2]), 0])
            #self.bigram_not_zero += int(words[2])

    def goodTuring(self):
        for i in self.LexiconHead:
            if i[1]+1 not in self.dict_word_num:
                i[2] = 0.1*i[1]/self.word_sum
            else:
                i[2] = 0.1*(i[1]+1)*self.dict_word_num[i[1]+1]/(self.dict_word_num[i[1]]*self.word_sum)
        bigram_sum = pow(len(self.LexiconHead), 2)
        for i in self.bigram_dict:
            if i[1]+1 not in self.dict_bigram_num:
                i[2] = 0.1*i[1]/bigram_sum
            else:
                i[2] = 0.1*(i[1]+1)*self.dict_bigram_num[i[1]+1]/(self.dict_bigram_num[i[1]]*bigram_sum)
        bigram_zero = 2.0*self.dict_bigram_num[1]/((bigram_sum-len(self.bigram_dict))*bigram_sum)
        self.bigram_dict.append([('0','0'),0,bigram_zero])

    def print2txt(self):
        import math
        word_freq_dict = dict()
    	persum = sum([i[2] for i in self.LexiconHead])
        word_freq = codecs.open('word_pre.txt', 'w', 'gbk')
        for i in self.LexiconHead:
            word_freq.write(i[0]+'\t'+str(i[1])+'\t'+str(math.log(i[2]/persum))+'\r\n')
            word_freq_dict[i[0]] = i[2]/persum
        word_freq.close()
        logging.info("done, write word_pre.txt..")
        for i in self.bigram_dict:
            if i[0][0] != '0':
                i[2] = i[2]/word_freq_dict[i[0][0]]
        persum = sum([i[2] for i in self.bigram_dict])
        bigram_freq = codecs.open('bigram_pre.txt', 'w', 'gbk')
        for i in self.bigram_dict:
            bigram_freq.write(i[0][0]+'\t'+i[0][1]+'\t'+str(i[1])+'\t'+str(math.log(i[2]/persum))+'\r\n')
        bigram_freq.close()
        logging.info("done, write bigram_pre.txt..")

if __name__ == '__main__':
    turing = good_turing()
    turing.load_freq()
    turing.goodTuring()
    turing.print2txt()