print('Distributional similarity program')
print '*'*6

file = open('dist-similarity.txt', 'r').read()
num_chars = len(file)
num_lines = file.count('\n')

split_file = file.split()

import string
dict_of_words = {}
words = [word.strip(string.punctuation).lower() for word in split_file]
for word in words:
	count = dict_of_words.get(word, 0)
	dict_of_words[word] =  count + 1


count_by_words = dict((v,k) for k,v in dict_of_words.iteritems())

res = sorted(count_by_words, reverse=True)
res = res[0:20] #top 20 words
top20words = [count_by_words[count] for count in res]

WINDOW_SIZE = 5

vector_words = ['obama', 'president', 'bush', 'afghanistan', 'iraq', 'war']
vector_words_context_counts = []

# FOR EACH WORD VECTOR:
# 1) GET ALL INDEXES OF WORD OCCURENCE
# 2) FORM A WINDOW OF 5 AROUND THE INDEX, REMOVING THE WORD TO GET A LIST OF SIZE 4
# 3) CHECK IF EACH WORD IS IN THE TOP20, UPDATING COUNT IF SO
# 4) ADD THE DICTIONARY OF COUNTS TO THE LIST OF DICTS (THE LIST SIZE = 6 AT THE END, ONE FOR EACH VEC_WORD)

for vec_word in vector_words:
	indexes = []
	dict_of_context_counts = {key:0 for key in top20words}
	if vec_word in words:
		indexes = [i for i,w in enumerate(words) if w == vec_word]

	for index in indexes:
		window = words[index-2 : index+3]
		window.remove(vec_word)

		for word in window:
			if word in dict_of_context_counts.keys():
				dict_of_context_counts[word] = dict_of_context_counts[word] + 1

	vector_words_context_counts.append(dict_of_context_counts)

# Get sum of squares value for each word vector
list_sum_of_squares = []
import math 

for count_dict in vector_words_context_counts:
	sum = 0 
	for count in count_dict.values():
		sum = sum + (count*count)
	list_sum_of_squares.append(sum)

list_sum_of_squares = [math.sqrt(val) for val in list_sum_of_squares]
dict_sum_of_squares = dict(zip(vector_words, list_sum_of_squares))

import itertools
similarity_combinations = [pair for pair in itertools.combinations(vector_words, 2)]
vector_words_context_counts = dict(zip(vector_words, vector_words_context_counts))


for pair in similarity_combinations:
	sum_of_products = 0
	context_count_1 = vector_words_context_counts[pair[0]]
	context_count_2 = vector_words_context_counts[pair[1]]

	for count in context_count_1:
		sum_of_products = sum_of_products + (context_count_1[count] * context_count_2[count])

	sqrt1 = dict_sum_of_squares[pair[0]]
	sqrt2 = dict_sum_of_squares[pair[1]]

	similarity_result = sum_of_products / float((sqrt1 * sqrt2))
	print 'similarity for {} and {} is {}'.format(pair[0], pair[1], similarity_result)


