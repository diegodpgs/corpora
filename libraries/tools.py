import nltk

from markovgeneration import *
from sequences import *



file_corpus = open("/Users/diegopedro/Documents/corpora/data/gutemberg_2.txt").read()
corpus = nltk.word_tokenize(file_corpus.lower().decode("utf-8"))
unigram = getUnigram(corpus)
bigram  = getBigram(corpus)
trigram = getTrigram(corpus)
fourgram = getFourgram(corpus) 

while True:
	ngram = fourgram
	type_ngram = input("Type of Ngram: ")
	words = raw_input("Type at least %d words separated by ,, ex. she,,is: " % type_ngram)
	rank = input("Type the number of entries: ")

	try:
		words = words.split(",,")
		if type_ngram == 1:
			ngram = unigram
		elif type_ngram == 2:
			ngram = bigram
		elif type_ngram == 3:
			ngram = trigram

		type_ngram -=  1 # -1 for the slices in the call of nextWord function
		result = nextMostProbablyWord(ngram,words[-type_ngram:],rank)
		
		result = result[-1][::-1]
		for r in result:
			print "%s %s" % (" ".join(words),r)

	except Exception as instance:
		print instance.args





