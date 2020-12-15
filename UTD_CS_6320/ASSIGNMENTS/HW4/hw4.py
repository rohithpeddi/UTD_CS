import nltk
import torch
import random
from math import sqrt
import torch.nn.functional
from nltk.corpus import brown
from collections import Counter

brown_corpus = brown.sents()
brown_corpus = brown_corpus[:int(len(brown_corpus)/3)]
print(brown_corpus[0])

def lowercase_corpus(original_corpus):
  lowercased_corpus = []
  for sentence in original_corpus:
    lowercased_sentence = []
    for token in sentence:
      lowercased_sentence.append(token.lower())
    lowercased_corpus.append(lowercased_sentence)
  return lowercased_corpus

corpus = lowercase_corpus(brown_corpus)
print(corpus[0])



# Fill in this code snippet to count how many times each word occurs in the training corpus.
# The argument corpus is a list of lists of strings
# The return type should be a dictionary (or collections.Counter)
def get_word_counts(corpus):
  word_count_dict = {}
  for sentence in corpus:
    for token in sentence:
      if token in word_count_dict:
        word_count_dict[token] += 1
      else:
        word_count_dict[token] = 1
  return word_count_dict

word_counts = get_word_counts(corpus)
print(len(word_counts))

# Fill in this code snippet to replace words in the training corpus that occur only once with "<unk>"
# The argument corpus is a list of lists of strings
# The argument word_counts is a dictionary (or collections.Counter)
# No return value; modifies corpus in place
def replace_rare_words(corpus, word_counts):
  UNK = "<unk>"
  for i in range(len(corpus)):
    sentence = corpus[i]
    for j in range(len(sentence)):
      if word_counts[sentence[j]] == 1:
        sentence[j] = UNK
  return

replace_rare_words(corpus, word_counts)
new_word_counts = get_word_counts(corpus)
print(len(new_word_counts))

vocabulary = list(new_word_counts.keys())
vocabulary.extend(['<s>', '</s>'])
vocabulary.sort()
print(len(vocabulary))

vocabulary = {vocabulary[i]:i for i in range(len(vocabulary))}


# Fill in this code snippet to convert a word into a one-hot vector
# The argument word is a string
# The argument vocabulary is a dictionary {string: int}
# The return type should be a torch.Tensor of size |V|
def convert_to_one_hot(word, vocabulary):
  vec = torch.zeros(len(vocabulary))
  vec[vocabulary[word]] = 1
  return vec

print(convert_to_one_hot('!', vocabulary))

# Fill in this code snippet to convert the training data into (word_index, [context_vectors]) pairs
# The argument corpus is a list of lists of strings
# The argument vocabulary is a dictionary {string: int}
# The argument k is an int
# The yield type should be a list of tuples (int, list of torch.Tensors)
def generate_training_pairs(corpus, vocabulary, k=4):
  sent_seq = list(range(0, len(corpus)))
  random.shuffle(sent_seq)
  for i in range(0, len(corpus)):
    sent = corpus[sent_seq[i]]
    modified_sent = ['<s>']*k + sent + ['</s>']
    word_seq = list(range(4, len(modified_sent)))
    random.shuffle(word_seq)
    for word_index in word_seq:
      word = modified_sent[word_index]
      context_vectors = []
      for j in range(1, k+1):
        context_vectors.append(convert_to_one_hot(modified_sent[word_index-j], vocabulary))
      yield tuple((vocabulary[word], context_vectors))

for word, _ in generate_training_pairs(corpus, vocabulary):
  print(word)
  break
for word, _ in generate_training_pairs(corpus, vocabulary):
  print(word)
  break
for word, _ in generate_training_pairs(corpus, vocabulary):
  print(word)
  break


# Fill in this function to initialize a parameter using Xavier initialization
# Also turn on Pytorch's automatic gradient calculations
# The argument parameter_size is a tuple of ints
# The return type should be a torch.Tensor
def initialize_parameter(parameter_size):
  n_in, n_out = parameter_size
  params = torch.empty((n_in, n_out)).normal_(mean=0, std=sqrt(2/(n_in+n_out)))
  params.requires_grad_()
  return params

class NLM:

  # Fill in this function to initialize parameters of the appropriate sizes
  # The argument vocabulary_size is an int
  # The argument embedding_length is an int
  # No return value
  def __init__(self, vocabulary_size, embedding_length=64, k=4):
    self.E = initialize_parameter((embedding_length, vocabulary_size))
    total_context = k*embedding_length
    self.W_1 = initialize_parameter((total_context, total_context))
    self.b_1 = initialize_parameter((total_context, 1))
    self.W_2 = initialize_parameter((vocabulary_size, total_context))
    self.b_2 = initialize_parameter((vocabulary_size, 1))

  # Fill in this function to run the network and produce the output y_hat
  # The argument context is a list of torch.Tensors
  # The return type should be a torch.Tensor
  def forward_pass(self, context):
    # x = torch.Tensor()
    context_tensors = []
    for j in range(len(context)):
      w_j = context[j]
      e_j = torch.matmul(self.E, w_j)
      # x = torch.cat((x, e_j))
      context_tensors.append(e_j)
    x = torch.cat(context_tensors)
    h = torch.tanh(torch.matmul(self.W_1, x).reshape(-1, 1) + self.b_1)
    y_out = torch.nn.functional.log_softmax((torch.matmul(self.W_2, h) + self.b_2))
    return y_out

model = NLM(len(vocabulary))
print(model)


import datetime

# Fill in this code snippet to train the neural network
# The argument model is an NLM
# The argument corpus is a list of lists of strings
# The argument vocabulary is a dictionary {string: int}
# The argument learning_rate is a float
# No return value
def train(model, corpus, vocabulary, learning_rate=0.1):
  for (word_index, context_vectors) in generate_training_pairs(corpus, vocabulary):
    y_out = model.forward_pass(context_vectors)
    loss = -y_out[word_index]
    loss.backward()

    with torch.no_grad():
      model.W_2 -= (learning_rate) * model.W_2.grad
      model.b_2 -= (learning_rate) * model.b_2.grad
      model.W_1 -= (learning_rate) * model.W_1.grad
      model.b_1 -= (learning_rate) * model.b_1.grad
      model.E -= (learning_rate) * model.E.grad

    model.W_2.grad.zero_()
    model.b_2.grad.zero_()
    model.W_1.grad.zero_()
    model.b_1.grad.zero_()
    model.E.grad.zero_()

print(datetime.datetime.now())
train(model, corpus, vocabulary)
print(datetime.datetime.now())

