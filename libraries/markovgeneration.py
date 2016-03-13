import random
import nltk

from sequences import *




"""
  


  Best sequence
  eg.  for  she were today (if there is not any appearence of 'she were today')

        	she <is> today
        	she <was> <yesterday>

  Generate
  		random      [w1,w2,w3][w2,w3,w4][w3,w4,w5]...
  		r.prob      [w1,w2,w3]hp[w2,w3,w4].... the higher probability trigram that has w2 and w3 and not w1



"""


# 
# @ngram
# 		a ngram
#
#  
# @words  MIN=1 MAX=4
#		words to be used as seed
#		eg.  word ['it','is','good'] *see example bellow
#
#
# @rank
#		the top most frequentes
#
#
# @randomize
#		if that option is True then the return list will be only one value radomically choose from
#		the original list
#
#		example. [the,a,not,it]
#				 randomically choose 'not' the return will be [she,is,[not]]
#				   
#
#
# return
#			words[]
#			example. words = [she,is]
#					 [she,is,[the,a,not,it]]
#
#
###############
#
#
#    nextMostProbablyWord(trigram,['a','b'],3)	
#	 P(w|a,b) given w as any word in the corpus, return the three words (w1,w2,w3)
#			  that has the highest odd
#
#    3 in max(P(w|a,b))
#    
#
###############
def nextMostProbablyWord(ngram,words,rank=1,randomize=False):
	"""
		examples
		corpus  = "a b c d a b c a d d d a b c d a d b".split()
		
		
		Input: nextWord(getBigram(corpus),['b'])
		Output : ['b', ['c']] it's means that the most probable next word is c

		Input: nextWord(getBigram(corpus),['b'],2)
		Output : ['b', ['#','c']] it's means that the most probable next word is c and #

		Input: nextWord(getBigram(corpus),['b'],2,True)
		Output : ['b', ['#'] or ['c']] it's means that among the most two frequent words randomically
										will random '#' or 'c'

		Input: nextWord(getTrigram(corpus),['b','c'],2)
		Output : ['b','c' ['a','d']] it's means that the most probable next two words following 
		after 'b c' are 'a' and 'd'



	"""
	type_ngram = detectNgram(ngram)

	if type_ngram < 2:
		raise NameError("Type of Ngram cannot be lower than 2, for unigrans use generateTextByNgram")

	if len(words) >= type_ngram:
		raise NameError("too much words to process <nextWord:function> %d" % len(words))

	if len(words)+1 < type_ngram:
		raise NameError("insufficiente words to process <nextWord:function> %d " % len(words))

	if type_ngram == 2:
		if words[-1] in ngram:
			ngram_sorted = sortNgram(ngram[words[-1]])

			limite_rank = min(rank,len(ngram_sorted))
			most_frequent_words = [n[1]for n in ngram_sorted[-limite_rank:]]
			words.append(most_frequent_words)
				
		else:
			ngram_sorted = sortNgram(ngram)
			words.pop() #delete the last word since it was not found in the bigrams
						#eg.  she is <the word is was not found in the bigrams[she][is]
			limite_rank = min(rank,len(ngram_sorted))
			words.append([w[1].split("_")[-1] for w in ngram_sorted[-limite_rank:]]) 
			#since the simbol '_' is used to separete unigrams
			#eg.  she_is

	elif type_ngram == 3:
		if words[-2] in ngram: #ex  [she] is | 'she' in ngram
			if words[-1] in ngram[words[-2]]: #ex 'is' in ngram[she]

				unigrams = ngram[words[-2]][words[-1]]  #ex. ngram[she][is] = [cute,pretty,tall,smart...]
				ngram_sorted = sortNgram(unigrams)      #ex. sort by most frequents
				limite_rank = min(rank,len(ngram_sorted))
				words.append([w[1] for w in ngram_sorted[-limite_rank:]])
			else:
				bigrams = ngram[words[-2]]
				ngram_sorted = sortNgram(bigrams)
				words.pop() #delete the last word since it was not found in the bigrams
							#eg.  she is <the word is was not found in the bigrams[she][is]
				
				limite_rank = min(rank,len(ngram_sorted))
				words.append([w[1].split("_")[-1] for w in ngram_sorted[-limite_rank:]]) 
				#since the simbol '_' is used to separete unigrams
				#eg.  she_is
		else:
			ngram_sorted = sortNgram(ngram)
			words.pop() #delete the last word since it was not found in the trigrams
						#eg.  she is pretty <the word is was not found in the trigram[she][is][pretty]
			limite_rank = min(rank,len(ngram_sorted))
			words.append([w[1].split("_")[-1] for w in ngram_sorted[-limite_rank:]]) 
			#since the simbol '_' is used to separete unigrams
			#eg.  she_is_pretty


	if randomize:
		#print words
		words[-1] = [words[-1][random.randint(0,len(words[-1])-1)]]

	return words
	


# 
# @ngram 
# 		ngram data
# 
# @length
#		length of the text generated
#
#
#    w1,w2,w3  w2,w3,w4  w3,w4,w5
#
def generateTextByNgram(ngram,length):
	type_ngram = detectNgram(ngram)
	text_generate = ""

	if type_ngram == 1:
		tokens = ngram.keys()

		for t in xrange(length):
			text_generate += " "+ tokens[random.randint(0,len(tokens)-1)]

	elif type_ngram >= 2:
		ngram_sorted = sortNgram(ngram)

		for t in xrange(length-1):
			bigram = ngram_sorted[random.randint(0,len(ngram_sorted)-1)][1]
			text_generate += " "+" ".join(bigram.split("_"))

	return text_generate[1:]



# 
# @ngram 
# 		ngram data
# 
# @seed
#		a list of words to start the generation
#
#
# @length
#		length of the text generated
#
#
# @rank
#		the top most frequentes
#
#
#TODO is better choose automatically the seed?
def generateTextByNextWord(ngram,seed,length,rank):

	text_generate = " ".join(seed)+ " "
	type_ngram = detectNgram(ngram)

	for i in xrange(length):
		seed = nextMostProbablyWord(ngram,seed,rank,True)
		#print seed,
		if type_ngram == 2:
			seed = seed[-1]

		elif type_ngram == 3:
			seed = [seed[-2],seed[-1][0]]

		else:
			seed = [seed[-3],seed[-2],seed[-1][0]]
		#print seed
		text_generate += seed[-1]+" "

	return text_generate

def tests():
	corpus  = "a b c d a b c a d d d a b c d a d b".split()
	unigram = getUnigram(corpus)
	bigram  = getBigram(corpus)
	trigram = getTrigram(corpus)
	if not nextWord(trigram,['a','b'],3,1) == ['a','b',['c']]:
		raise NameError("Excepted ['a','b',['c']],but was %s" % str(nextWord(trigram,['a','b'],3,1)))
	else:
		print "TEST 1 - OK"
	####################################################################################


	file_corpus = open("/Users/diegopedro/Documents/corpora/data/citations/authors_30_2010.txt").read()
	corpus = nltk.word_tokenize(file_corpus.lower().decode("utf-8"))
	#unigram = getUnigram(corpus)
	bigram  = getBigram(corpus)
	trigram = getTrigram(corpus)
	#fourgram = getFourgram(corpus) 

	print generateTextByNextWord(bigram,['she'],100,8)
	print "#"*70
	print generateTextByNextWord(trigram,['she','has'],100,8)
	#print "#"*70
	#print generateTextByNextWord(fourgram,['she','has','been'],5,5)



