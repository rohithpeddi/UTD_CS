from collections import defaultdict
from itertools   import product
from sys         import stdout

import math
import numpy as np
import time


class IBM:
    """Class containing the IBM2 Model"""

    def __init__(self):
        self.t = None
        self.q = None

    def uniform(self, corpus):
        """Model initialized using a normalized uniform initialization on the corpus"""
        return self.compute_initial_paramters(corpus, lambda n: [1 / float(n)] * n)

    def compute_initial_paramters(self, corpus, g):
        """Initialize the model with normalized parameters using generator g"""

        start = time.time()
        lens = set()
        en_vocab = set()
        fr_vocab = set()

        # "Compute all possible alignments..."
        for sentence_index in range(len(corpus)):
            french_sentence, english_sentence = corpus[sentence_index]
            lens.add((len(english_sentence), len(french_sentence)))
            for french_word in french_sentence:
                fr_vocab.add(french_word)
            for english_word in english_sentence:
                en_vocab.add(english_word)

        # "Compute initial probabilities for each alignment..."
        t = dict()
        for english_word in en_vocab:
            for french_word in fr_vocab:
                t[(french_word, english_word)] = g(len(fr_vocab))

        # "Compute initial probabilities for each distortion..."
        q = dict()
        for sentence_index, (l, m) in enumerate(lens):
            for i in range(1, m+1):
                p_values = g(l)
                for j in range(1, l+1):
                    q[(j, i, l, m)] = p_values[j-1]

        self.t = t
        self.q = q
        print("\rInit     100.00%% (Elapsed: %.2fs)" % (time.time() - start))

    def em_train(self, corpus, n=10, s=1):
        """Run several iterations of the EM algorithm on the model"""
        for k in range(s, n+s):
            print('ITERATION : ' + str(s))
            self.em_iter(corpus)

    def em_iter(self, corpus):
        """Run a single iteration of the EM algorithm on the model"""
        start = time.time()
        likelihood = 0.0
        c1 = defaultdict(float) # ei aligned with fj
        c2 = defaultdict(float) # ei aligned with anything
        c3 = defaultdict(float) # wj aligned with wi
        c4 = defaultdict(float) # wi aligned with anything

        # The E-Step
        for sentence_index in range(len(corpus)):
            french_sentence, english_sentence = corpus[sentence_index]
            l = len(english_sentence) 
            m = len(french_sentence)

            for i in range(1, m):
                num = [self.q[(j+1, i, l, m)] * self.t[(french_sentence[i - 1], english_sentence[j])] for j in range(0, l)]
                den = float(sum(num))
                likelihood += math.log(den)

                for j in range(0, l):

                    delta = num[j] / den

                    c1[(french_sentence[i - 1], english_sentence[j])] += delta
                    c2[(english_sentence[j],)]          += delta
                    c3[(j, i, l, m)]        += delta
                    c4[(i, l, m)]          += delta

        # The M-Step
        self.t = defaultdict(float, {k: v / c2[k[1:]] for k, v in c1.iteritems() if v > 0.0})
        self.q = defaultdict(float, {k: v / c4[k[1:]] for k, v in c3.iteritems() if v > 0.0})

        duration = (time.time() - start)
        print("\rPass %2d: 100.00%% (Elapsed: %.2fs) (Log-likelihood: %.5f)" % (passnum, duration, likelihood))
        return likelihood, duration


corpus = [tuple((['le', 'chien'], ['the', 'dog'])),
          tuple((['petit', 'chien'], ['little', 'dog'])),
          tuple((['chien', 'noir'], ['black', 'dog']))]

model = IBM()
model.uniform(corpus)
model.em_train(corpus)