#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sequences import *


class Indexer:	

	def __init__(self):
		self.dicionary_word = {}
		self.dicionary_index = {}
		self.corpora = None

	#@private
	def tokenize(self,stream):
		punc = '.,;:!()[]?'

		for p in punc:
			stream = stream.replace(p,' %s ' % p)
			stream = stream.replace('  ',' ')
		stream = stream.lower()
		stream = stream.replace('\n','')	

		return stream.split()

	#@ stream could be a big string of characters or a list of words
	def index(self,stream):
		if type(stream) != list:
			stream = self.tokenize(stream)
		

		self.corpora = stream

		for index in xrange(len(stream)):

			if stream[index] not in self.dicionary_word:
				self.dicionary_word[stream[index]] = []

			self.dicionary_word[stream[index]].append(index)
			self.dicionary_index[index] = stream[index]

	#@ get all index of specific word in a text
	def getWordIndex(self,word):
		return self.dicionary_word[word]

	#@ return size sentences of a specific length which contem a specific word
	def getSentences(self,word,size=0,leftsize=3,rightsize=3):

		indexwords = self.dicionary_word[word]
		sentences = []

		if size != 0:
			indexwords = indexwords[0:min(size,len(indexwords)-1)]

		for index in indexwords:
			left  = max(0,index-leftsize)
			right = min(len(self.corpora),rightsize+index)
			if len(self.corpora[left:right]) == leftsize+rightsize:
				sentences.append(self.corpora[left:right])

		return sentences


	def getTheMostProbableSentence(self,sentences,ngram):
		unigram = getUnigram(self.corpora)
		for p in [',','.']:
			unigram[p] = 0

		bigram = getBigram(self.corpora)

		for w1,ws2 in bigram.iteritems():
			for n in [',','.']:
				bigram[w1][n] = -1000
				bigram[n][w1] = -1000

		trigram = getTrigram(self.corpora)
		sentences_odds = []

		if ngram == 1:

			for sentence in sentences:
				
				probabilities = 0

				for word in sentence:
					probabilities += unigram[word]

				sentences_odds.append((probabilities,sentence))

			sentences_odds.sort()

		elif ngram == 2:

			for sentence in sentences:
				
				probabilities = 0

				for index in xrange(1,len(sentence)):
					word = sentence[index-1]+"_"+sentence[index]
					
					probabilities += bigram[sentence[index-1]][sentence[index]]
					
				#print probabilities
				sentences_odds.append((probabilities,sentence))


		return sentences_odds[::-1]


	def getBestSentences(self,word,size=0,leftsize=3,rightsize=3,ngram=1):
		sentences = self.getSentences(word,size,leftsize,rightsize)
		best_sentences = self.getTheMostProbableSentence(sentences,ngram)

		for index in xrange(len(best_sentences)):

			left  = " ".join(best_sentences[index][1][0:6])
			rigth = " ".join(best_sentences[index][1][7:])

			best_sentences[index] = "%s %s %s" % (left.rjust(40),best_sentences[index][1][6],rigth.ljust(20))
			

		return best_sentences[0:min(3,len(best_sentences))]




i = Indexer()
f = open('francais.txt').read()
fw = open('vocabulary_hiato.txt','w')
i.index(f)

unigram = sortNgram(getUnigram(i.corpora))[::-1]

def hasHiato(word):
	hiato = ['am', 'an', 'em', 'en', 'om', 'on', 'im', 'in', 'um', 'un', 'ai', 'au', 'ei', 'eu', 'ou', 'oi', 'gn', 'ill']

	for h in hiato:
		if h in word:
			return True

	return False

for index in xrange(1000):
	word = unigram[index][1]
	rightwindow = 6
	leftwindow = 6

	if hasHiato(word):
		sentences = i.getBestSentences(word,0,5,6,2)
		fw.write('%s\n' % word)
		for s in sentences:
			fw.write('   %s\n' % (s))
		fw.write('\n')

		if index % 10 == 0:
			print '%d%% computed' % (index/10)






			