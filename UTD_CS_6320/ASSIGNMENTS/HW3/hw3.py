import sys

from nltk.corpus import brown
import numpy
from scipy.sparse import csr_matrix
from sklearn.linear_model import LogisticRegression


# Load the Brown corpus with Universal Dependencies tags
# proportion is a float
# Returns a tuple of lists (sents, tags)
def load_training_corpus(proportion=1.0):
    brown_sentences = brown.tagged_sents(tagset='universal')
    num_used = int(proportion * len(brown_sentences))

    corpus_sents, corpus_tags = [None] * num_used, [None] * num_used
    for i in range(num_used):
        corpus_sents[i], corpus_tags[i] = zip(*brown_sentences[i])
    return (corpus_sents, corpus_tags)


# Generate word n-gram features
# words is a list of strings
# i is an int
# Returns a list of strings
def get_ngram_features(words, i):
    N = len(words)
    END_TOKEN = '</s>'
    START_TOKEN = '<s>'
    ngram_features=[]
    neighbours = [START_TOKEN, START_TOKEN, END_TOKEN, END_TOKEN]

    if i >= 1:
        neighbours[1] = words[i-1]
    if i >= 2:
        neighbours[0] = words[i-2]
    if i < N-1:
        neighbours[2] = words[i+1]
    if i < N-2:
        neighbours[3] = words[i+2]

    ngram_features.append('prevbigram-' + str(neighbours[1]))
    ngram_features.append('nextbigram-' + str(neighbours[2]))
    ngram_features.append('prevskip-' + str(neighbours[0]))
    ngram_features.append('nextskip-' + str(neighbours[3]))
    ngram_features.append('prevtrigram-' + str(neighbours[1]) + '-' + str(neighbours[0]))
    ngram_features.append('nexttrigram-' + str(neighbours[2]) + '-' + str(neighbours[3]))
    ngram_features.append('centertrigram-' + str(neighbours[1]) + '-' + str(neighbours[2]))

    return ngram_features


# Generate word-based features
# word is a string
# returns a list of strings
def get_word_features(word):
    # print(word)
    word_features = ['word-' + word]

    if word[0].isupper():
        word_features.append('capital')

    if word.isupper():
        word_features.append('allcaps')

    contains_number = False
    contains_hyphen = False

    wordshape = ''
    short_wordshape = ''
    for i in range(len(word)):
        
        if word[i].isupper():
            wordshape += 'X'
        elif word[i].islower():
            wordshape += 'x'
        elif word[i].isdigit():
            wordshape += 'd'
            contains_number = True
        elif word[i] == '-':
            contains_hyphen=True
            wordshape += '-'
        else:
            wordshape += word[i]
            
        if i > 0:
            if wordshape[i-1] is not wordshape[i]:
                short_wordshape += wordshape[i]
        else:
            short_wordshape += wordshape[i]
    
    word_features.append('wordshape-' + wordshape)
    word_features.append('short-wordshape-' + short_wordshape)
    
    if contains_number:
        word_features.append('number')
    
    if contains_hyphen:
        word_features.append('hyphen')
        
    for i in range(min(len(word), 4)):
        word_features.append('prefix-' + str(i+1) + '-' + word[0:i+1])
        word_features.append('suffix-' + str(i+1) + '-' + word[len(word)-(i+1):])

    return word_features


# Wrapper function for get_ngram_features and get_word_features
# words is a list of strings
# i is an int
# prevtag is a string
# Returns a list of strings
def get_features(words, i, prevtag):
    ngram_features = get_ngram_features(words, i)
    word_features = get_word_features(words[i])

    features = []
    features.extend(ngram_features)
    features.extend(word_features)
    features.append('tagbigram-' + prevtag)

    features = list(map(lambda x: x if "wordshape" in x else x.lower(), features))

    return features


# Remove features that occur fewer than a given threshold number of time
# corpus_features is a list of lists, where each sublist corresponds to a sentence and has elements that are lists of strings (feature names)
# threshold is an int
# Returns a tuple (corpus_features, common_features)
def remove_rare_features(corpus_features, threshold=5):

    feature_count_dict = {}
    for i in range(len(corpus_features)):
        sentence_features = corpus_features[i]
        for j in range(len(sentence_features)):
            word_features = sentence_features[j]
            for k in range(len(word_features)):
                if word_features[k] in feature_count_dict:
                    feature_count_dict[word_features[k]] += 1
                else:
                    feature_count_dict[word_features[k]] = 1

    corpus_features_modified = []
    for i in range(len(corpus_features)):
        sentence_features = corpus_features[i]
        sentence_features_modified = []
        for j in range(len(sentence_features)):
            word_features = sentence_features[j]
            word_features_modified = []
            for k in range(len(word_features)):
                feature = word_features[k]
                if feature_count_dict[feature] >= threshold:
                    word_features_modified.append(feature)
            sentence_features_modified.append(word_features_modified)
        corpus_features_modified.append(sentence_features_modified)
            # word_features_pruned = word_features.copy()
            # for k in range(len(word_features)):
            #     feature = word_features[k]
            #     if feature_count_dict[feature] < threshold:
            #         word_features_pruned.remove(feature)
            # sentence_features[j] = word_features_pruned

    rare_features = set()
    common_features = set()

    for feature in feature_count_dict:
        if feature_count_dict[feature] < threshold:
            rare_features.add(feature)
        else:
            common_features.add(feature)

    return corpus_features_modified, common_features


# Build feature and tag dictionaries
# common_features is a set of strings
# corpus_tags is a list of lists of strings (tags)
# Returns a tuple (feature_dict, tag_dict)
def get_feature_and_label_dictionaries(common_features, corpus_tags):
    index = 0
    feature_dict = {}
    for feature in common_features:
        feature_dict[feature] = index
        index += 1

    tags = set()
    for i in range(len(corpus_tags)):
        sentence_tags = corpus_tags[i]
        for j in range(len(sentence_tags)):
            word_tag = sentence_tags[j]
            tags.add(word_tag)

    index = 0
    tag_dict = {}
    for tag in tags:
        tag_dict[tag] = index
        index += 1
    return feature_dict, tag_dict


# Build the label vector Y
# corpus_tags is a list of lists of strings (tags)
# tag_dict is a dictionary {string: int}
# Returns a Numpy array
def build_Y(corpus_tags, tag_dict):
    corpus_tags_flattened = []
    for i in range(len(corpus_tags)):
        sentence_tags = corpus_tags[i]
        for j in range(len(sentence_tags)):
            tag = sentence_tags[j]
            corpus_tags_flattened.append(tag_dict[tag])
    Y = numpy.array(corpus_tags_flattened)
    # Y = numpy.array(corpus_tags_flattened).reshape(-1, 1)
    return Y

# Build a sparse input matrix X
# corpus_features is a list of lists, where each sublist corresponds to a sentence and has elements that are lists of strings (feature names)
# feature_dict is a dictionary {string: int}
# Returns a Scipy.sparse csr_matrix
def build_X(corpus_features, feature_dict):

    rows = []
    cols = []

    word_index = -1
    for i in range(len(corpus_features)):
        sentence_features = corpus_features[i]
        for j in range(len(sentence_features)):
            word_features = sentence_features[j]
            word_index += 1
            for feature in word_features:
                if feature in feature_dict:
                    rows.append(word_index)
                    cols.append(feature_dict[feature])

    total_words = word_index
    values = [1] * len(rows)
    np_rows = numpy.array(rows)
    np_cols = numpy.array(cols)
    np_values = numpy.array(values)

    print('ROWS: ' + str(len(np_rows)) + ', COLUMNS: ' + str(len(np_cols)) + ', TOTAL WORDS: ' + str(total_words))
    return csr_matrix((np_values, (np_rows, np_cols)), shape=(total_words + 1, len(feature_dict)))


# Train an MEMM tagger on the Brown corpus
# proportion is a float
# Returns a tuple (model, feature_dict, tag_dict)
def train(proportion=1.0):
    META_TAG = '<S>'
    corpus_sents, corpus_tags = load_training_corpus(proportion)

    corpus_features = []
    for i in range(len(corpus_sents)):
        sentence_features = []
        sentence = corpus_sents[i]
        tag_sequence = corpus_tags[i]
        for j in range(len(sentence)):
            word_features = get_features(sentence, j, META_TAG if j==0 else tag_sequence[j-1])
            sentence_features.append(word_features)
        corpus_features.append(sentence_features)

    corpus_features, common_features = remove_rare_features(corpus_features, threshold=5)
    feature_dict, tag_dict = get_feature_and_label_dictionaries(common_features, corpus_tags)

    X = build_X(corpus_features, feature_dict)
    Y = build_Y(corpus_tags, tag_dict)

    model = LogisticRegression(class_weight='balanced', solver='saga', multi_class='multinomial').fit(X, Y)
    return model, feature_dict, tag_dict


# Load the test set
# corpus_path is a string
# Returns a list of lists of strings (words)
def load_test_corpus(corpus_path):
    with open(corpus_path) as inf:
        lines = [line.strip().split() for line in inf]
    return [line for line in lines if len(line) > 0]


# Predict tags for a test sentence
# test_sent is a list containing a single list of strings
# model is a trained LogisticRegression
# feature_dict is a dictionary {string: int}
# reverse_tag_dict is a dictionary {int: string}
# Returns a tuple (Y_start, Y_pred)
def get_predictions(test_sent, model, feature_dict, reverse_tag_dict):
    N = len(test_sent)
    T = len(reverse_tag_dict)
    Y_pred = numpy.empty((N-1, T, T))

    for i in range(0, N-1):
        features = []
        for j in range(T):
            tag = reverse_tag_dict[j]
            features.append(get_features(test_sent, i+1, tag))
        X = build_X([features], feature_dict)
        y_pred = model.predict_log_proba(X)
        Y_pred[i] = y_pred

    word_0_features = get_features(test_sent, 0, '<S>')
    X_0 = build_X([[word_0_features]], feature_dict)
    Y_start = numpy.array(model.predict_log_proba(X_0)).reshape(1, -1)

    return Y_start, Y_pred


# Perform Viterbi decoding using predicted log probabilities
# Y_start is a Numpy array of size (1, T)
# Y_pred is a Numpy array of size (n-1, T, T)
# Returns a list of strings (tags)
def viterbi(Y_start, Y_pred):
    N, T, C = Y_pred.shape
    N = N+1

    V = numpy.empty((N, T))
    BP = numpy.empty((N, T))

    V[0] = Y_start
    for n in range(1, N):
        for t in range(T):
            temp = numpy.empty(T)
            for tp in range(T):
                temp[tp] = V[n-1][tp] + Y_pred[n-1][tp][t]
            V[n][t] = numpy.max(temp)
            BP[n][t] = int(numpy.argmax(temp))

    # tags = [int(numpy.argmax(V[N - 1]))]
    # for n in reversed(range(1, N-1)):
    #     tags.insert(0, int(BP[n, tags[0]]))
    #
    # return tags
    tags = []
    bp_t = int(numpy.argmax(V[N - 1]))
    # # max_at_position = -numpy.inf
    # # max_tag = 0
    # # for t in range(T):
    # #     if V[N-1][t] > max_at_position:
    # #         max_at_position = V[N-1][t]
    # #         max_tag = t
    #
    for n in range(N):
        position = N-1-n
        tags.append(bp_t)
        bp_t = int(BP[position][bp_t])

    tags.reverse()
    return tags

# Predict tags for a test corpus using a trained model
# corpus_path is a string
# model is a trained LogisticRegression
# feature_dict is a dictionary {string: int}
# tag_dict is a dictionary {string: int}
# Returns a list of lists of strings (tags)
def predict(corpus_path, model, feature_dict, tag_dict):
    test_corpus = load_test_corpus(corpus_path)
    reverse_tag_dict = {}
    for tag in tag_dict:
        reverse_tag_dict[tag_dict[tag]] = tag

    predictions = []
    for i in range(len(test_corpus)):
        sentence = test_corpus[i]
        Y_start, Y_pred = get_predictions(sentence, model, feature_dict, reverse_tag_dict)
        tag_sequence = viterbi(Y_start, Y_pred)
        tags = []
        for tag_index in tag_sequence:
            tags.append(reverse_tag_dict[int(tag_index)])
        predictions.append(tags)
    return predictions
            

def main(args):
    model, feature_dict, tag_dict = train(0.05)

    predictions = predict('test.txt', model, feature_dict, tag_dict)
    for test_sent in predictions:
        print(test_sent)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
