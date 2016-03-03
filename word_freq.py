# -*- coding:utf-8 -*-
'''
Created on 2015年12月26日

@author: yuxuan
'''

import codecs
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 词条
class HeadWordItem():
    wordid = -1
    word_pinyin = None
    freq = 0

class word_freq():
    def __init__(self):
        self.LexiconHead = dict()
        self.split_word = ''
        self.word_num = 0
        self.bigram_dict = dict() # 计算bigrame frequency
        self.LexiconHead_list = []

    def load_word(self):
        lexicon_file = codecs.open('lexicon.txt', 'r', 'gbk')
        for lines in lexicon_file.readlines():
            if len(lines) > 0:
                wordlist = lines.strip().split('\t')
                worditem = HeadWordItem()
                worditem.wordid = self.word_num
                self.word_num += 1
                worditem.word_pinyin = wordlist[1]
                self.LexiconHead[wordlist[0]] = worditem

                self.LexiconHead_list.append(wordlist[0])

        lexicon_file.close()
        split_file = codecs.open('split_word.txt', 'r', 'gbk')
        for lines in split_file.readlines():
            self.split_word = self.split_word + lines.strip() + '|'
        split_file.close()

    def forward_max_match(self):
        import os,glob,re
        self.load_word()
        logging.info("done, load lexicon.txt !!")
        path = sys.path[0]
        for filename in glob.glob(path+'\\人民日报96年语料\\*'.decode('utf8').encode('gbk')):
            logging.info("process "+filename+' ...')
            file_open = codecs.open(filename, 'r', 'gbk', 'ignore')
            alllines = ''
            for lines in file_open.readlines():
                alllines += lines.strip()
            for subline in re.split(self.split_word, alllines):
                begin = 0
                end = len(subline)
                first_word = -1; current_word = -1 # 前一个词id 当前词id
                while(end>0 and begin<len(subline)):
                    if begin == end:
                        begin += 1
                        end = len(subline)
                        continue
                    subword = subline[begin:end]
                    if subword in self.LexiconHead:
                        self.LexiconHead[subword].freq += 1
                        current_word = self.LexiconHead[subword].wordid
                        begin = end
                        end = len(subline)
                        if first_word != -1:
                            if (first_word, current_word) not in self.bigram_dict:
                                self.bigram_dict[(first_word, current_word)] = 1
                            else:
                                self.bigram_dict[(first_word, current_word)] += 1
                        first_word = current_word
                    else:
                        end -= 1
        logging.info("done, forward_max_match..")

    def print2txt(self):
        word_freq = codecs.open('word_freq.txt', 'w', 'gbk')
        for i in sorted(self.LexiconHead.items(), key=lambda x:x[1].freq, reverse=True):
            word_freq.write(i[0]+'\t'+str(i[1].freq)+'\r\n')
        word_freq.close()
        logging.info("done, write word_freq.txt..")
        bigram_freq = codecs.open('bigram_freq.txt', 'w', 'gbk')
        for i in sorted(self.bigram_dict.items(), key=lambda x:x[1], reverse=True):
            printline = self.LexiconHead_list[i[0][0]] + '\t'
            printline +=  (self.LexiconHead_list[i[0][1]] + '\t')
            printline += (str(i[1]) + '\r\n')
            bigram_freq.write(printline)
        bigram_freq.close()
        logging.info("done, write bigram_freq.txt..")

if __name__ == '__main__':
    freqcy = word_freq()
    freqcy.forward_max_match()
    freqcy.print2txt()
