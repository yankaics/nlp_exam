# -*- coding:utf-8 -*-
'''
Created on 2015年12月26日

@author: yuxuan
'''
import codecs
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class yin2zi():
	"""docstring for yin2zi
		拼音转汉字
	"""
	def __init__(self):
		self.LexiconHead = dict()
		self.bigram_dict = dict()
		self.pinyin_word = dict()

	def load_pre_pinyi(self):
		word_freq = codecs.open('word_pre.txt', 'r', 'gbk')
		for lines in word_freq.readlines():
			words = lines.strip().split('\t')
			self.LexiconHead[words[0]] = float(words[2])
		word_freq.close()
		bigram_freq = codecs.open('bigram_pre.txt', 'r', 'gbk')
		for lines in bigram_freq.readlines():
			words = lines.strip().split('\t')
			self.bigram_dict[(words[0],words[1])] = float(words[3])
		bigram_freq.close()
		lexicon_file = codecs.open('lexicon.txt', 'r', 'gbk')
		for lines in lexicon_file.readlines():
			replace_lines = lines
			if len(lines) > 0:
				for i in '12345':
					replace_lines = replace_lines.replace(i, '')
				words = replace_lines.strip().split('\t')
				pinyin = words[1].split(' ')
				if tuple(pinyin) not in self.pinyin_word:
					self.pinyin_word[tuple(pinyin)] = [words[0]]
				else:
					self.pinyin_word[tuple(pinyin)].append(words[0])
		lexicon_file.close()
		logging.info("done, load already..")

	def pinyin2word(self, pinyin):
		# item in words_appear 'word':{'parent' 'begin' 'end' 'percent'}
		words_appear = dict()
		for i in range(1,len(pinyin)+1): # 找到所有可能长度的词
			begin_t = 0
			end_t = i
			while(end_t <= len(pinyin)):
				if tuple(pinyin[begin_t:end_t]) in self.pinyin_word:
					for words in self.pinyin_word[tuple(pinyin[begin_t:end_t])]:
						item_words_appear = dict()
						item_words_appear['parent'] = None
						item_words_appear['begin'] = begin_t
						item_words_appear['end'] = end_t-1
						item_words_appear['percent'] = self.LexiconHead[words]
						words_appear[words] = item_words_appear
				begin_t += 1
				end_t +=1
		return words_appear

	def find_max_per(self, words_appear, len_pinyin):
		for i in range(len_pinyin):
			for item_word in words_appear.items():
				if item_word[1]['end'] == i:
					if item_word[1]['begin'] != 0:
						max_per = float('-inf')
						for item_parent in words_appear.items():
							if item_parent[1]['end'] == (item_word[1]['begin']-1):
								if (item_parent[0],item_word[0]) in self.bigram_dict:
									bigram_between = self.bigram_dict[(item_parent[0],item_word[0])]
								else:
									bigram_between = self.bigram_dict[('0','0')]
								if max_per < bigram_between+item_parent[1]['percent']:
									max_per = bigram_between+item_parent[1]['percent']
									item_word[1]['parent'] = item_parent[0]
									item_word[1]['percent'] = max_per
					else:
						item_word[1]['percent'] = self.LexiconHead[item_word[0]]
		max_last = float('-inf')
		max_item = ''
		for item_word in words_appear.items():
			if (item_word[1]['end'] == (len_pinyin-1)) and (max_last < item_word[1]['percent']):
				max_last = item_word[1]['percent']
				max_item = item_word[0]
		item_word = max_item
		max_word = ''
		while(item_word):
			max_word = item_word + max_word
			item_word = words_appear[item_word]['parent']
		print max_word

	def input_pinyin(self,pinyin):
		pinyin = pinyin.strip().split()
		len_pinyin = len(pinyin)
		words_appear = self.pinyin2word(pinyin)
		self.find_max_per(words_appear, len_pinyin)

if __name__ == '__main__':
	pinyin_to_word = yin2zi()
	pinyin_to_word.load_pre_pinyi()
	while(1):
		pinyin = raw_input('拼音（键入q退出）：'.decode('utf8').encode('gbk'))
		if pinyin == 'q':
			break
		pinyin_to_word.input_pinyin(pinyin)