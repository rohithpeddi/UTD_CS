import argparse
import math
import random
from nltk.tokenize import sent_tokenize, word_tokenize
from typing import List
from typing import Tuple
from typing import Generator


# Generator for all n-grams in text
# n is a (non-negative) int
# text is a list of strings
# Yields n-gram tuples of the form (string, context), where context is a tuple of strings
def get_ngrams(n: int, text: List[str]) -> Generator[Tuple[str, Tuple[str, ...]], None, None]:
    # 1. Pad with (n-1) start tokens and 1 end token to text
    START_TOKEN = '<s>'
    END_TOKEN = '</s>'

    modified_text = [START_TOKEN]*(n-1)
    modified_text.extend(text)
    modified_text.append(END_TOKEN)

    #print(modified_text)

    # 2. Create tuples of the form (string, context)
    ngram_list = list(zip(*[modified_text[i:] for i in range(n)]))

    for ngram in ngram_list:
        yield tuple((ngram[n-1], tuple(ngram[:n-1])))


# Loads and tokenizes a corpus
# corpus_path is a string
# Returns a list of sentences, where each sentence is a list of strings
def load_corpus(corpus_path: str) -> List[List[str]]:
    document = open(corpus_path).read()
    paragraphs = document.split('\n\n')

    sentences = []
    for paragraph in paragraphs:
        sentences.extend(sent_tokenize(paragraph))

    words = []
    for sentence in sentences:
        words.append(word_tokenize(sentence))

    return words

# Builds an n-gram model from a corpus
# n is a (non-negative) int
# corpus_path is a string
# Returns an NGramLM
def create_ngram_lm(n: int, corpus_path: str) -> 'NGramLM':
    corpus = load_corpus(corpus_path)
    ngram_lm = NGramLM(n)
    
    for text in corpus:
        ngram_lm.update(text)

    return ngram_lm


# An n-gram language model
class NGramLM:
    def __init__(self, n: int):
        self.n = n
        self.ngram_counts = {}
        self.context_counts = {}
        self.vocabulary = set()

    # Updates internal counts based on the n-grams in text
    # text is a list of strings
    # No return value
    def update(self, text: List[str]) -> None:
        self.vocabulary |= set(text)
        self.vocabulary |= set(['</s>'])
        for ngram in get_ngrams(self.n, text):
            self.ngram_counts[ngram] = self.ngram_counts.get(ngram, 0) + 1
            self.context_counts[ngram[1]] = self.context_counts.get(ngram[1], 0) + 1


    # Calculates the MLE probability of an n-gram
    # word is a string
    # context is a tuple of strings
    # delta is an float
    # Returns a float
    def get_ngram_prob(self, word: str, context: Tuple[str, ...], delta=.0) -> float:
        context_count = self.context_counts.get(context, 0)
        ngram_count = self.ngram_counts.get((word, context), 0)
        if delta == 0:
            if context_count == 0:
                return 1/(len(self.vocabulary))
            else:
                return ngram_count/context_count
        else:
            return (ngram_count + delta)/(context_count + (delta * len(self.vocabulary)))

    # Calculates the log probability of a sentence
    # sent is a list of strings
    # delta is a float
    # Returns a float
    def get_sent_log_prob(self, sent: List[str], delta=.0) -> float:
        sent_prob = 0
        for ngram in get_ngrams(self.n, sent):
            ngram_prob = self.get_ngram_prob(ngram[0], ngram[1], delta)
            try:
                sent_prob += math.log2(ngram_prob)
            except:
                sent_prob += float('-inf')
        return sent_prob

    # Calculates the perplexity of a language model on a test corpus
    # corpus is a list of lists of strings
    # Returns a float
    def get_perplexity(self, corpus: List[List[str]]) -> float:
        corpus_size = 0
        corpus_sent_prob = 0
        
        for sent in corpus:
            corpus_size = corpus_size + len(sent)
            sent_prob = self.get_sent_log_prob(sent)
            corpus_sent_prob = corpus_sent_prob + sent_prob

        avg_log_prob = (-1)*(corpus_sent_prob/corpus_size)
        return math.pow(2, avg_log_prob)

    # Samples a word from the probability distribution for a given context
    # context is a tuple of strings
    # delta is an float
    # Returns a string
    def generate_random_word(self, context: Tuple[str, ...], delta=.0) -> str:
        sorted_vocab = sorted(self.vocabulary)
        r = random.random()
        prev_probability = 0
        current_probability = 0
        for word in sorted_vocab:
            ngram_probability = self.get_ngram_prob(word, context, delta)
            current_probability = current_probability + ngram_probability
            if prev_probability < r <= current_probability:
                #print(word)
                return word
            prev_probability = prev_probability + ngram_probability

    # Generates a random sentence
    # max_length is an int
    # delta is a float
    # Returns a string
    def generate_random_text(self, max_length: int, delta=.0) -> str:
        if max_length == 0:
            return ''
        current_length = 0
        text = ['<s>']*(self.n-1)
        first_word = self.generate_random_word(tuple(text), delta)
        current_length = current_length + 1
        text.append(first_word)
        sent_end = False
        while current_length < max_length and not sent_end:
            word = self.generate_random_word(tuple(text[-(self.n-1):]), delta)
            text.append(word)
            current_length = current_length + 1
            if word == '</s>':
                sent_end = True

        #print(text)
        return ' '.join(text[self.n-1:])


def main(corpus_path: str, delta: float, seed: int):
    bigram_lm = create_ngram_lm(2, corpus_path)
    s1 = 'love Science'
    s2 = 'I love Computer Science'

    print(bigram_lm.get_perplexity([word_tokenize(s1)]))
    print(bigram_lm.get_perplexity([word_tokenize(s2)]))

    # trigram_lm = create_ngram_lm(3, corpus_path)
    # s1 = 'God has given it to me, let him who touches it beware!'
    # s2 = 'Where is the prince, my Dauphin?'
    #print(trigram_lm.get_sent_log_prob(word_tokenize(s1), delta))
    #print(trigram_lm.get_sent_log_prob(word_tokenize(s2), delta))
    #print(trigram_lm.get_perplexity([word_tokenize(s1), word_tokenize(s2)]))

    # print('----------------------UNIGRAM----------------------------')
    # unigram_lm = create_ngram_lm(1, corpus_path)
    # for i in range(5):
    #     print(unigram_lm.generate_random_text(10))
    #
    # print('----------------------TRIGRAM-----------------------------------')
    # trigram_lm = create_ngram_lm(3, corpus_path)
    # for i in range(5):
    #     print(trigram_lm.generate_random_text(10))
    #
    # print('----------------------PENTAGRAM----------------------------------')
    # pentagram_lm = create_ngram_lm(5, corpus_path)
    # for i in range(5):
    #     print(pentagram_lm.generate_random_text(10))
    # print('----------------------------------------------------------------')

if __name__ == '__main__':
    #E: / UTD / SEM3 / NLP / ASSIGNMENTS / HW1 / Files / shakespeare.txt
    parser = argparse.ArgumentParser(description="CS6320 HW1")
    # parser.add_argument('corpus_path', nargs="?", type=str, default='warpeace.txt', help='Path to corpus file')
    # parser.add_argument('corpus_path', nargs="?", type=str, default='E:/UTD/SEM3/NLP/ASSIGNMENTS/HW1/Files/shakespeare.txt', help='Path to corpus file')
    parser.add_argument('corpus_path', nargs="?", type=str, default='E:/UTD/SEM3/NLP/ASSIGNMENTS/HW1/Files/sample.txt', help='Path to corpus file')
    parser.add_argument('delta', nargs="?", type=float, default=.5, help='Delta value used for smoothing')
    parser.add_argument('seed', nargs="?", type=int, default=82761904, help='Random seed used for text generation')
    args = parser.parse_args()
    random.seed(args.seed)
    main(args.corpus_path, args.delta, args.seed)
