#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk


"""
	This class retrieval patterns of a corpora using lexemes and POS as input.
	In order to retrieval the patterns is used a similar approach to regular expression.

	Example.   am [doing,,playing]  
						 retrieval all patterns of length to be defined that contain
						 the word am followed by the words doing OR playing

			   [you,we,they] did|saw|played [it] 
			   			 retrieval all patterns athat contain the words you OR we OR they followed by
			   			 the word did OR saw OR played which are followed by the word it.


"""
#   plan text = list of strings ex. ["abc def ghi","efg hij",...]
#   
#	-------------          ---------------------
#  |             | index  | dictionary of words | where index position in the corpus
#  |  PLAN TEXT  |------->| list of words       |    words {word-1: [index-1,index-2,index-3...index-n],... word-n}
#  | characters  |        |                     |    list of words [w1,w2...wn]
#   -------------          ---------------------
#
#  
#		                   -------------
#     list of             | [a1X1b1]    | where a1 are the words on the left side
#  ---------------------->| [a2X2b2...] |       b1 are the words on the right side
#   central words         |             |        X is a central word
#   		               -------------        [] is a list
#
#
#		                       --------------------
#  	apply left,right,coringa  | list of words      | 
#  -------------------------->| contain            |
#  		                      | these configuration|
#   		                   --------------------
#
#
#
#
#				

class Retrieval:

	def __init__(self):
		self.dicionary_word = {}
		self.dicionary_pos 	= {}
		self.corpora_word 	= []
		self.corpora_pos 	= []
		self.result = None

	"""
	  Index the file
	 		words {word-1: [index-1,index-2,index-3...index-n],... word-n}a
	 		a word using pos 'has|VB'

	"""
	def indexFile(self,file_name,percent_data=1.0):
		corpora = open(file_name).read().lower()
		size_corpora = len(corpora)*percent_data

		corpora = corpora[0:int(size_corpora)]
		corpora = corpora.split()
		
		for index in xrange(len(corpora)):

			if len(corpora[index].split("|")) == 2:
				word = corpora[index].split("|")[0]
				self.corpora_word.append(word)

				if word not in self.dicionary_word:
					self.dicionary_word[word] = []

				self.dicionary_word[word].append(len(self.corpora_word)-1)

				pos = corpora[index].split("|")[1]
				self.corpora_pos.append(pos)

				if pos not in self.dicionary_pos:
					self.dicionary_pos[pos] = []

				self.dicionary_pos[pos].append(len(self.corpora_pos)-1)

	"""
		Build a wordbook

		dic_words: 
			       words {word-1: [index-1,index-2,index-3...index-n],... word-n}

		corpora:
					a list of words OR pos

		dicionary
					a dicionary of words OR pos

		central_words:
					a list of central words

		size_window:
					size of the windows on the left and right side of the central words


		@return 
				a wordbook (a,b are index of the corpora)
				    [[-an... -a2,-a1,X,a1,a2...am,INDEX], (where index is the position of the central word)
				     [-bn1... -b2,-b1,X,b1,b2...bm1,INDEX]]
	"""
	def findCentralWords(self,corpora,dicionary,central_words,size_window):

		#storage the indexes of central words ex the this list will be [1,34,81...]
		list_of_index_temp = dicionary[central_words[0]]
		print "CENTRAL WORDS = ",central_words
		wordbook = []
		corpora_size = len(corpora)
		

		for index in xrange(1,len(central_words)):
			list_of_index_temp.extend(dicionary[central_words[index]])

		print "Registers found: %d" % len(list_of_index_temp)
		for index_central_word in list_of_index_temp:
			#[.....X]
			
			left  = max(0,index_central_word-size_window)
			#[X.....]
			right = min(corpora_size,index_central_word+size_window+1)
			wordbook.append(range(left,right))
			wordbook[-1].append(index_central_word-left)

		print "Wordbook: %d" % len(wordbook)
		return wordbook

	"""
	   		@return all samples that has the specific words in the first index before the central word
	   			TODO in future example for all index shifted

	   		direction           = {<-, ->}
	   		words               = [word1,word2,word3...]
	   		corpora             = a list of words OR pos

	   		example

	   		specificWords('<-',
	   						self.corpora_word
	   						['a','f'],
	   						[['a','b','f','x','d','g'],['d','b','d','x','a','h','g']])
											

						return  [['a','b','f','x','d','g']]
	"""
	def specificWords(self,direction,corpora,words,wordbook):
		newdata = []

		if direction == "<-":
			for sample in wordbook:
				index_central_word = sample[-1]

				if index_central_word-1 >= 0:

					if corpora[sample[index_central_word-1]] in words:
						newdata.append(sample)

		else:
			for sample in wordbook:
				index_central_word = sample[-1]

				if index_central_word+1 < len(sample):

					if corpora[sample[index_central_word+1]] in words:
						newdata.append(sample)


		
		return newdata

	"""
			@return all samples with a specific windows size

	   		direction        = {<-, ->}
	   		sizeWindow       = [1..n]
	   		

	   		example

	   		coringaWords('<-',
	   						[['a','b','f','x','d','g'],['d','b','d','x','a','h','g']],
	   						1)
											

						return  [['f','x','d','g'],['d','x','a','h','g']]
	"""
	def coringaWords(self,direction,wordbook,sizeWindow):
		newordbook = []
		

		if direction == "<-":
			for sample in wordbook:
				index_central_word = sample[-1]
				if len(sample)-1 > index_central_word-1 >= 0:
					newordbook.append(sample[max(0,index_central_word-sizeWindow):])

					#add the index of the central word if the slices cut off that information
					if type(newordbook[-1][-1]) == int:
						newordbook[-1][-1] = index_central_word - max(0,index_central_word-sizeWindow)
					else:
						newordbook[-1].append(index_central_word - max(0,index_central_word-sizeWindow))

		else:
			for sample in wordbook:
				index_central_word = sample[-1]

				if len(sample)-1 > index_central_word-1 >= 0:
					newordbook.append(sample[0:min(index_central_word+sizeWindow,len(sample))])

					#add the index of the central word if the slices cut off that information
					if type(newordbook[-1][-1]) != int:
						newordbook[-1].append(sample[-1])

		return newordbook

	"""

		@variable = [], *, *[],SPACE,
		@side = LEFT,RIGHT
		@data = coreWord("X",10)
	    data = [[-a10... -a2,-a1,X,a1,a2...a10],
				[-b10... -b2,-b1,X,b1,b2...b10]]
	   .....
	"""
	def parserLR(self,variable,corpora,wordbook,side):
		
		direction = '->'

		if side == "LEFT":
			direction = '<-'

		#LEFT  = E[]
		if "[" in variable:
			#E = * ------------------------> LEFT =  [] c
			words = variable.split("[")[1].split("]")[0].split(",,")
			wordbook = self.specificWords(direction,corpora,words,wordbook)
			#E = * ------------------------> LEFT = *[] c
			if "*" in variable:
				try:
					if side == "LEFT":
						sizeWindow = int(variable.split("[")[0].split("*")[1])
					else:
						sizeWindow = int(variable.split("]")[1].split("*")[1])
					print sizeWindow
					wordbook = self.coringaWords(direction,wordbook,sizeWindow  + len(words))
				except:
					return ["ERROR:< Size of the Window was not defined for Coringa>"]
		#LEFT  = E		
		elif "*" in variable:
			#E = *
			#E = * ------------------------> LEFT =  * c
			try:
				sizeWindow = int(variable.split("*")[1])

				if side == "RIGHT":
					sizeWindow += 1

				wordbook = self.coringaWords(direction,wordbook,sizeWindow)
			except:
				return ["ERROR:< Size of the Window was not defined for Coringa>"]
		else:
			print "No filter was applied"

		return wordbook

	"""
		@input_expression (it will be considered a valid input)
			a list 
			

			A = LEFT c RIGHT |  LEFT c|c RIGHT
			LEFT  = E[] | E
			RIGHT = []E | E
			E = lambda | *n  (n is a number)

			example:			 
	"""
	def search(self,input_expression,size_window,POS_SELECTED=False):
		
		dicionary = self.dicionary_word
		corpora = self.corpora_word

		if POS_SELECTED:
			dicionary = self.dicionary_pos
			corpora = self.corpora_pos

		wordbook = None
		central_words = None
		#A = c

		central_words = [input_expression[0]]

		#A = LEFT c
		if "[" in input_expression[0] or "*" in input_expression[0]:
			central_words = [input_expression[1]]


		if "|" in central_words[0]:
			central_words = central_words[0].split("|")

		
		wordbook = self.findCentralWords(corpora,dicionary,central_words,size_window)

		#A = LEFT c
		if "[" in input_expression[0] or "*" in input_expression[0]:
			wordbook = self.parserLR(input_expression[0],corpora,wordbook,"LEFT")
			

		#A = c RIGHT
		if "]" in input_expression[-1] or "*" in input_expression[-1]:
			wordbook = self.parserLR(input_expression[-1],corpora,wordbook,"RIGHT")
			
		print "%d results was found" % len(wordbook)
		self.result =  wordbook

	def show(self,list_size=100):
		

		while True:
			output = {}
			corpora = self.corpora_word
			option = input("Choose the option to print:\n\n1 - Lexemes\n2 - POS\n3 - Lexemes and Pos\n 4 - Quit\n: ")

			if option == 2:
				corpora = self.corpora_pos
			elif option == 4:
				break


			for w in self.result:
				words = [corpora[index] for index in w[0:-1]]

				if option == 3:
					words = [corpora[index]+"|"+self.corpora_pos[index] for index in w[0:-1]]
				w = " ".join(words)

				
				for y in words:
					if len(y) == 0:
						print words

				if w not in output:
					output[w] = 0

				output[w] += 1

			output_sorted = zip(output.values(),output.keys())
			output_sorted.sort()
			output_sorted = output_sorted[::-1]

			for o in output_sorted[0:min(len(output_sorted),list_size)]:
				print "%d - %s" % (o[0],o[1])


def runLexeme(retrieval_obj):
	pattern = raw_input("Type the pattern \n\n%s \n: " % ("""A = LEFT c RIGHT |  LEFT c|c RIGHT
																  LEFT  = E[] | E (values in [] separated by ,,)
																  RIGHT = []E | E
																  E = lambda | *n  (n is a number)

																  example:  '*2[he,,she] has [been]*2'
																  """))
		
	length_instance = input("Type the length of the instance: ")
	instances = input("Type the number of instances: ")
	retrieval_obj.search(pattern.split(),length_instance)
	retrieval_obj.show(instances)	

def runPOS(retrieval_obj):
	
	pos = 	"""
					
					AJ - Adjective
					AV - Adverb
					CJ - Conjuction
					DT - Determiner
					V1 - Irregular Present Tense
					V2 - Irregular Past Tense
					VP - Irregular Past Participle
					VM - Modal Verb
					OO - No Definition
					NB - Number
					NN - Nouns
					PR - Pronoun
					PP - Preposition
					PC - Punctuation
					VC - Verb Continuous
					VB - Verb
					
			"""
	print pos
	pattern = raw_input("Type the pattern \n\n%s \n: " % ("""A = LEFT c RIGHT |  LEFT c|c RIGHT
																  LEFT  = E[] | E (values in [] separated by ,,)
																  RIGHT = []E | E
																  E = lambda | *n  (n is a number)

																  example:  'eg. *2[PR,,DT] VP [DT]*2'
																  """))
		
	length_instance = input("Type the length of the instance: ")
	instances = input("Type the number of instances: ")
	retrieval_obj.search(pattern.lower().split(),length_instance,True) #POS_SELECTED=True
	retrieval_obj.show(instances)



if "__main__":
	C = Retrieval()
	#C.indexFile("/Users/diegopedro/Documents/corpora/data/pos/corpora_tagged_authors_30_2010.txt",1.0)
	C.indexFile("/Users/diegopedro/Documents/corpora/data/pos/corpora_tagged_gutemberg.txt",.2)
	while True:
		try:
			option = input(""" Choose the following options
			1 - Lexeme       	eg. *2[he,,she] has [been]*2
			2 - POS          	eg. *2[PR,,DT] VP [DT]*2
			3 - Quit
					   """)
		except:
			continue

		if option == 1:
			runLexeme(C)

		elif option == 2:
			runPOS(C)

		else:
			break


			



