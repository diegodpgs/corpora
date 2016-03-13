# .
#    , va durer longtemps ? oui . il
#    , mon meilleur ami de fac . c'etait
#    y a longtemps , en 2005 . j'avais

f = open('vocabulary_hiato.txt').read().split('\n')

words_dic = {}
actual_word = ''
for line in f:
	if len(line) != 0:
		words = line.split()
		if len(words) == 1:
			if words[0] not in words_dic:
				words_dic[words[0]] = []
			actual_word = words[0]

		if line[0:3] == '   ':
			words_dic[actual_word].append(line)


f2 = open('vocabulary_francais_hiato.txt','w')
keys = words_dic.keys()
keys.sort()

for key in keys:
	word = key
	sentences = words_dic[key]

	f2.write(word+'\n')
	for s in sentences:
		f2.write(s+'\n')

	f2.write('\n')
