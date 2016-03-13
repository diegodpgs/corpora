from markovgeneration import *

"""
@author: Diego

	Take a text and expand that text in order to correct some missed words
	example

	Input           : I working at the UCSC researcher
	Output(expected): I <am> working at the UCSC <as> researcher

"""

file_ = open("text.txt").read().replace("\n"," ").replace(',','').lower()
file_ = file_.split()

def expand():
	new_text = [""]
	bigrams = getBigram()
	trigrams = getTrigram()
	

	for i in xrange(len(file_)-1):
		left = file_[i]
		right = file_[i+1]
		if left != new_text[-1]:
			new_text.append(left)

		if left not in bigrams:
			continue
		bigram = bigrams[left]
		bigram_sort = zip(bigram.values(),bigram.keys())
		bigram_sort.sort()
		counts = []
		

		for i in xrange(len(bigram_sort)):
			value,key = bigram_sort[i]

			if key in bigrams:
				bigram_temp = bigrams[key]

				if right in bigram_temp:
					counts.append((value,key))

		counts.sort()

		if len(counts) > 0 and counts[-1][-1] != new_text[-1]:
			b_count = 0
			r_count = 0

			if right in bigrams[left]:
				b_count += bigrams[left][right]

			if counts[-1][-1] in bigrams[left]:
				r_count += bigrams[left][counts[-1][-1]]

			if counts[-1][-1] in bigrams and right in bigrams[counts[-1][-1]]:
				r_count += bigrams[counts[-1][-1]][right]


			r_count = r_count/2.0


			if counts[-1][-1] not in trigrams[left]:
				r_count = 0

			elif right	not in trigrams[left][counts[-1][-1]]:
				r_count = 0

			else:
			 	r_count = r_count/(trigrams[left][counts[-1][-1]][right])
			
			#print r_count,b_count
 			if b_count < r_count:
 				new_text.append("<"+counts[-1][-1]+">")
	new_text.append(file_[-1])

	print " ".join(new_text)


expand()







