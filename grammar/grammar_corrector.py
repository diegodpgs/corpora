from analyse import *


#minimum = 4
def corrector(file_name):
	bigram = getBigram()
	trigram = getTrigram()

	file_text = open(file_name).read().replace("\n",' ').replace(",",' ').lower()
	file_text = file_text.split()
	for index in xrange(0,len(file_text)-3,3):
		sequence = file_text[index:index+3]

		try:
			trigram[sequence[0]][sequence[1]][sequence[2]]
			print " ".join(sequence),
		except:
			
			try:
				trigrams = trigram[sequence[0]][sequence[1]]
				values = trigrams.values()
				keys = trigrams.keys()
				top10 = getTop10(keys,values)
				index = 0

				
				while index < len(top10):
					if top10[index] in bigram[top10[index]] and (file_text[index+3] in bigram[top10[index]]):
						seq_correct = ' '.join([sequence[0],sequence[1],top10[index]])
						print '<<%s|%s>>' % (" ".join(sequence),seq_correct),
						break
					else:
						index += 1

			except:
				print "*".join(sequence),
				continue
				

corrector("test.txt")

