import re
import sys

import nltk
import numpy
from sklearn.linear_model import LogisticRegression


negation_words = set(['not', 'no', 'never', 'nor', 'cannot'])
negation_enders = set(['but', 'however', 'nevertheless', 'nonetheless'])
sentence_enders = set(['.', '?', '!', ';'])


# Loads a training or test corpus
# corpus_path is a string
# Returns a list of (string, int) tuples
def load_corpus(corpus_path):
    document = open(corpus_path).read()
    sentences = document.split('\n')

    data = []
    for index in range(len(sentences)):
        sentence = sentences[index]
        if not len(sentence.strip()) == 0:
            snippet_label = sentence.split('\t')
            snippet_string = snippet_label[0]
            label = int(snippet_label[1])
            snippet = snippet_string.split(' ')
            data.append((snippet, label))
    return data


# Checks whether or not a word is a negation word
# word is a string
# Returns a boolean
def is_negation(word):
    if word in negation_words:
        return True
    elif word.endswith('n\'t'):
        return True
    return False


# Modifies a snippet to add negation tagging
# snippet is a list of strings
# Returns a list of strings
def tag_negation(snippet):
    snippet_pos = nltk.pos_tag(snippet)
    N = len(snippet)
    META = 'NOT_'
    for index in range(N):
        if (snippet[index] in sentence_enders) or (snippet[index] in negation_enders) \
                or (snippet_pos[index][1] == 'JJR') or (snippet_pos[index][1] == 'RBR'):
            break
        if is_negation(snippet[index]):
            if (index < N-1) and snippet[index] is 'not' and snippet[index+1] is 'only':
                break
            elif index < N-1:
                snippet[index+1] = META + snippet[index+1]
    return snippet


# Assigns to each unigram an index in the feature vector
# corpus is a list of tuples (snippet, label)
# Returns a dictionary {word: index}
def get_feature_dictionary(corpus):
    index = 0
    word_index = {}
    for snippet_label_tuple in corpus:
        for word in snippet_label_tuple[0]:
            if not (word in word_index):
                word_index[word] = index
                index += 1
    return word_index


# Converts a snippet into a feature vector
# snippet is a list of tuples (word, pos_tag)
# feature_dict is a dictionary {word: index}
# Returns a Numpy array
def vectorize_snippet(snippet, feature_dict):
    N = len(feature_dict)
    snippet_vector = numpy.zeros(N)
    for word in snippet:
        if word in feature_dict:
            snippet_vector[feature_dict[word]] += 1
    return snippet_vector


# Trains a classification model (in-place)
# corpus is a list of tuples (snippet, label)
# feature_dict is a dictionary {word: label}
# Returns a tuple (X, Y) where X and Y are Numpy arrays
def vectorize_corpus(corpus, feature_dict):
    n = len(corpus)
    d = len(feature_dict)

    X = numpy.empty((n, d))
    Y = numpy.empty(n)

    for index in range(n):
        snippet = corpus[index][0]
        label = corpus[index][1]
        snippet_vector = vectorize_snippet(snippet, feature_dict)
        X[index] = snippet_vector
        Y[index] = label

    return X, Y


# Performs min-max normalization (in-place)
# X is a Numpy array
# No return value
def normalize(X):
    (n, d) = X.shape
    for index in range(d):
        column = X[:, index]
        minimum = column.min()
        maximum = column.max()
        if maximum == minimum:
            continue
        else:
            X[:, index] = (column-minimum) / (maximum-minimum)


# Trains a model on a training corpus
# corpus_path is a string
# Returns a LogisticRegression
def train(corpus_path):
    corpus = load_corpus(corpus_path)
    tagged_corpus = []
    n = len(corpus)
    for index in range(n):
        snippet = corpus[index][0]
        label = corpus[index][1]
        tagged_snippet = tag_negation(snippet)
        tagged_corpus.append((tagged_snippet, label))
    feature_dict = get_feature_dictionary(tagged_corpus)
    (X, Y) = vectorize_corpus(tagged_corpus, feature_dict)
    normalize(X)
    model = LogisticRegression().fit(X, Y)
    return model, feature_dict


# Calculate precision, recall, and F-measure
# Y_pred is a Numpy array
# Y_test is a Numpy array
# Returns a tuple of floats
def evaluate_predictions(Y_pred, Y_test):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    n = len(Y_pred)
    for index in range(n):
        predicted_label = Y_pred[index]
        true_label = Y_test[index]
        if true_label == 1 and predicted_label == 1:
            true_positives += 1
        elif true_label == 0 and predicted_label == 1:
            false_positives += 1
        elif true_label == 1 and predicted_label == 0:
            false_negatives += 1
    precision = (true_positives / (true_positives + false_positives))
    recall = (true_positives / (true_positives + false_negatives))
    f_measure = 2*(precision * recall)/(precision + recall)
    return precision, recall, f_measure


# Evaluates a model on a test corpus and prints the results
# model is a LogisticRegression
# corpus_path is a string
# Returns a tuple of floats
def test(model, feature_dict, corpus_path):
    test_corpus = load_corpus(corpus_path)
    tagged_test_corpus = []
    n = len(test_corpus)
    for index in range(n):
        snippet = test_corpus[index][0]
        label = test_corpus[index][1]
        tagged_snippet = tag_negation(snippet)
        tagged_test_corpus.append((tagged_snippet, label))
    (X_test, Y_test) = vectorize_corpus(tagged_test_corpus, feature_dict)
    normalize(X_test)
    Y_pred = model.predict(X_test)
    return evaluate_predictions(Y_pred, Y_test)


# Selects the top k highest-weight features of a logistic regression model
# logreg_model is a trained LogisticRegression
# feature_dict is a dictionary {word: index}
# k is an int
def get_top_features(logreg_model, feature_dict, k=1):
    weight_vector = logreg_model.coef_.reshape(-1, 1)
    index_weight = []
    for index in range(len(weight_vector)):
        index_weight.append((index, weight_vector[index]))
    feature_weight = []
    index_weight.sort(key=lambda x: -abs(x[1]))
    features = list(feature_dict.keys())
    for feature_weight_tuple in index_weight:
        feature_index = feature_weight_tuple[0]
        weight = feature_weight_tuple[1]
        feature = features[feature_index]
        feature_weight.append((feature, weight))
    return feature_weight[:k]


def main(args):
    model, feature_dict = train('E:/UTD/SEM3/NLP/ASSIGNMENTS/HW2/Files/train.txt')

    print(test(model, feature_dict, 'E:/UTD/SEM3/NLP/ASSIGNMENTS/HW2/Files/test.txt'))

    weights = get_top_features(model, feature_dict, 10)
    for weight in weights:
        print(weight)
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
