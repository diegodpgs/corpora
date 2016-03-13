import random
import nltk

from ngrams import *




"""
  


  Best sequence
  eg.  for  she were today (if there is not any appearence of 'she were today')

        	she <is> today
        	she <was> <yesterday>

  Generate
  		random      [w1,w2,w3][w2,w3,w4][w3,w4,w5]...
  		r.prob      [w1,w2,w3]hp[w2,w3,w4].... the higher probability trigram that has w2 and w3 and not w1



"""


################# Reviwed #################
def nextWord(ngram,sentence,rank=1,randomize=False):
	"""
		show most likely word to following the sequence of words.
		Ex. 
			INPUT  ['where','to','buy','a'],rank=2
			OUTPUT ['where','to','buy','a',['car','house']]

			INPUT ['where','to','buy','a'],rank=2, randomize=True
			OUTPUT ['where','to','buy','a',['has','you']]

		ngram : unigram, bigram,trigram...
		sentence : stream of words
			ex. ['where','to','buy']

		rank: how many words want to show
	"""
	
	type_ngram = detectNgram(ngram)

	if type_ngram < 2:
		raise NameError("Type of Ngram cannot be lower than 2, for unigrans use generateTextByNgram")

	if len(sentence) >= type_ngram:
		raise NameError("so much words to process <nextWord:function> %d" % len(sentence))

	if len(sentence)+1 < type_ngram:
		raise NameError("insufficiente words to process <nextWord:function> %d " % len(sentence))

	if type_ngram == 2:
		if sentence[-1] in ngram:
			ngram_sorted = sortNgram(ngram[sentence[-1]])

			limite_rank = min(rank,len(ngram_sorted))
			most_frequent_words = [n[1]for n in ngram_sorted[-limite_rank:]]
			sentence.append(most_frequent_words)
				
		else:
			ngram_sorted = sortNgram(ngram)
			sentence.pop() #delete the last word since it was not found in the bigrams
						#eg.  she is <the word is was not found in the bigrams[she][is]
			limite_rank = min(rank,len(ngram_sorted))
			sentence.append([w[1].split("_")[-1] for w in ngram_sorted[-limite_rank:]]) 
			#since the simbol '_' is used to separete unigrams
			#eg.  she_is

	elif type_ngram == 3:
		if sentence[-2] in ngram: #ex  [she] is | 'she' in ngram
			if sentence[-1] in ngram[sentence[-2]]: #ex 'is' in ngram[she]

				unigrams = ngram[sentence[-2]][sentence[-1]]  #ex. ngram[she][is] = [cute,pretty,tall,smart...]
				ngram_sorted = sortNgram(unigrams)      #ex. sort by most frequents
				limite_rank = min(rank,len(ngram_sorted))
				sentence.append([w[1] for w in ngram_sorted[-limite_rank:]])
			else:
				bigrams = ngram[sentence[-2]]
				ngram_sorted = sortNgram(bigrams)
				sentence.pop() #delete the last word since it was not found in the bigrams
							#eg.  she is <the word is was not found in the bigrams[she][is]
				
				limite_rank = min(rank,len(ngram_sorted))
				sentence.append([w[1].split("_")[-1] for w in ngram_sorted[-limite_rank:]]) 
				#since the simbol '_' is used to separete unigrams
				#eg.  she_is
		else:
			ngram_sorted = sortNgram(ngram)
			sentence.pop() #delete the last word since it was not found in the trigrams
						#eg.  she is pretty <the word is was not found in the trigram[she][is][pretty]
			limite_rank = min(rank,len(ngram_sorted))
			sentence.append([w[1].split("_")[-1] for w in ngram_sorted[-limite_rank:]]) 
			#since the simbol '_' is used to separete unigrams
			#eg.  she_is_pretty


	if randomize:
		#print words
		sentence[-1] = [sentence[-1][random.randint(0,len(sentence[-1])-1)]]

	return sentence
	


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
		seed = nextWord(ngram,seed,rank,True)
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


	file_corpus = open("/Users/diegopedro/Documents/NLP/Archive/corpora/data/citations/authors_30_2010.txt").read()
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



if "__main__":
	text = open('newyorker_100K.txt').read()
	timet = time.time()
	tokens = nltk.word_tokenize(text.encode('UTF-8'))
	bigram = getBigram(tokens)
	trigram = getTrigram(tokens)

	print generateTextByNgram(trigram,20)