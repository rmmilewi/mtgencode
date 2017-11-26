import collections
import re
import sys
import time

def count_ngrams(lines, min_length=1, max_length=6):
    """Iterate through given lines iterator (file object or list of
    lines) and return n-gram frequencies. The return value is a dict
    mapping the length of the n-gram to a collections.Counter
    object of n-gram tuple and number of times that n-gram occurred.
    Returned dict includes n-grams of length min_length to max_length.
    """
    lengths = range(min_length, max_length + 1)
    ngrams = {length: collections.Counter() for length in lengths}
    queue = collections.deque(maxlen=max_length)

    # Helper function to add n-grams at start of current queue to dict
    def add_queue():
        current = tuple(queue)
        for length in lengths:
            if len(current) >= length:
                ngrams[length][current[:length]] += 1

    # Loop through all lines and words and add n-grams to dict
    for line in lines:
        for word in line:
            queue.append(word)
            if len(queue) >= max_length:
                add_queue()

    # Make sure we get the n-grams at the tail end of the queue
    while len(queue) > min_length:
        queue.popleft()
        add_queue()

    return ngrams
	
def print_most_frequent(ngrams, num=10):
    """Print num most common n-grams of each length in n-grams dict."""
    for n in sorted(ngrams):
        print('----- {} most common {}-grams -----'.format(num, n))
        for gram, count in ngrams[n].most_common(num):
            print('{0}: {1}'.format(' '.join(gram), count))
        print('')
        
def build_vocab(txts):
	txts = [item for sublist in txts for item in sublist]
	word_counts = collections.Counter(txts)
	# Mapping from index to word
	vocabulary_inv = [x[0] for x in word_counts.most_common()]
	vocabulary_inv = list(sorted(vocabulary_inv))
	# Mapping from word to index
	vocabulary = {x: i for i, x in enumerate(vocabulary_inv)}
	#print(word_counts.most_common())
	#print("vocab size: ",len(vocabulary))
	return [vocabulary, vocabulary_inv]


def compress_demo(cards):
        #translation_dict = {"enters the battlefield" : "Ceob",
        #"end of turn": "Ceot", "creature" : "Ctc", "instant" :"Cti", "sorcery":"Cts","artifact":"Cta", "planeswalker":"Ctp", "enchantment" : "Cte"}
        cardtxts = [ card.text_words for card in cards]
        cardtxts = [item for sublist in cardtxts for item in sublist]
        word_counts = collections.Counter(cardtxts).most_common()[0:200]
        translation_dict = {}
        t_index = 0
        for word, _ in word_counts:
                replacement = "C{0}".format(t_index)
                if len(replacement) < len(word):
                        translation_dict[word] = "C{0}".format(t_index)
                        t_index += 1
        #vocabulary_inv = [x[0] for x in word_counts.most_common()]
        #vocabulary_inv = list(sorted(vocabulary_inv))
        #translation_dict = {}
        #for i in range(100):
                
        
        
        lensum = 0
        len_reduced_sum = 0
        for card in cards:
                mtext = card.text.text
                lensum += len(mtext)
                keys = reversed(sorted(list(translation_dict.keys())))
                for target in keys:
                        mtext = mtext.replace(target,translation_dict[target])
                len_reduced_sum += len(mtext)
                card.text.text = mtext
        print("number of characters (original):",lensum)
        print("number of characters (compressed):",len_reduced_sum)
        print("reduction: {0}%".format( 100 * (1 - (len_reduced_sum / lensum))))
