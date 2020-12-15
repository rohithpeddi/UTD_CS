import torchtext
import nltk
nltk.download('punkt')

START = '<s>'
END = '</s>'
MAX_LEN = 50


# Fill in the constructor options for src and tgt to perform tokenization and preprocessing
# You can use the global variables START, END, and MAX_LEN, as well as nltk.word_tokenize()
src = torchtext.data.Field(
    tokenize=lambda x: x.split(','),
    )
tgt = torchtext.data.Field(
    include_lengths=True,
    init_token=START,
    eos_token=END,
    lower=True,
    tokenize=lambda x: nltk.word_tokenize(x),
    )


train_data, test_data = torchtext.data.TabularDataset.splits(
    path='E:/UTD/SEM3/NLP/ASSIGNMENTS/HW5/content/', train='train.txt', test='test.txt', format='tsv',
    fields=[('src', src), ('tgt', tgt)],
    filter_pred=lambda x: len(x.tgt) <= MAX_LEN,
    skip_header=True
    )

src.build_vocab(train_data, max_size=50000)
tgt.build_vocab(train_data, max_size=50000)

print('Source and target vocabulary size')
print(len(src.vocab.stoi))
print(len(tgt.vocab.stoi))

print('\nSource and target vocabulary items')
print(list(src.vocab.stoi.keys())[:10])
print(list(tgt.vocab.stoi.keys())[:10])

print('\nNumber of training pairs: %d' % len(train_data.examples))
print('\nNumber of test pairs: %d' % len(test_data.examples))

print('\nTraining source and target')
print(train_data.examples[0].src)
print(train_data.examples[0].tgt)

import torch
import torch.nn as nn
import torch.nn.functional as F


class Encoder(nn.Module):

    # Fill in this constructor
    # The arguments input_size and hidden_size are ints
    # No return value
    def __init__(self, vocab_size, hidden_size):
        super(Encoder, self).__init__()
        self.hidden_size = hidden_size
        # Fill in more lines

        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)

    # Fill in this method
    # The return type should be a torch.Tensor
    def initialize_hidden_state(self):
        return torch.zeros(1, 1, self.hidden_size)

        # return torch.zeros(1, 1, self.hidden_size, device='cuda')

    # Fill in this method
    # The arguments input_sequence and hidden_state are torch.Tensors
    # The return type should be a torch.Tensor
    def forward(self, input_sequence, hidden_state):
        embeddings = self.embedding(input_sequence)
        output, hidden_state = self.gru(embeddings, hidden_state)
        return hidden_state


HIDDEN_SIZE = 128

# encoder = Encoder(len(src.vocab), HIDDEN_SIZE).to('cuda')
encoder = Encoder(len(src.vocab), HIDDEN_SIZE)
print(encoder)


class Decoder(nn.Module):

    # Fill in this constructor
    # The arguments hidden_size and vocab_size are ints
    # No return type
    def __init__(self, hidden_size, vocab_size):
        super(Decoder, self).__init__()
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)
        self.out = nn.Linear(hidden_size, vocab_size)
        self.softmax = nn.LogSoftmax(dim=2)

    # Fill in this method
    # The arguments prev_word and hidden_state are torch.Tensors
    # The return type should be a tuple (output, hidden_state), which are both torch.Tensors
    def forward(self, prev_word, hidden_state):
        word_embedding = self.embedding(prev_word)
        # word_embedding = F.relu(word_embedding)
        output, updated_hidden_state = self.gru(word_embedding, hidden_state)
        prob_dist_output = self.softmax(self.out(output))
        return prob_dist_output, updated_hidden_state


#decoder = Decoder(HIDDEN_SIZE, len(tgt.vocab)).to('cuda')
decoder = Decoder(HIDDEN_SIZE, len(tgt.vocab))
print(decoder)

import random


# Fill in this function
# The arguments input_sequence and target_sequence are torch.Tensors
# The argument target_length is an int
# The argument tgt_vocab is a torchtext.vocab.Vocab object
# The arguments encoder and decoder are our Encoder and Decoder
# The arguments encoder_optimizer and decoder_optimizer are torch.optim.Optimizers
# The argument loss_function is a torch.nn loss function class
# The argument teacher_forcing_ratio is a float
# The return type should be a float
def train(input_sequence, target_sequence, target_length, tgt_vocab,
          encoder, decoder, encoder_optimizer, decoder_optimizer,
          loss_function, teacher_forcing_ratio=0.5):
    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    # Fill in the encoder part and setting up for the decoder part here
    encoder_init_hidden = encoder.initialize_hidden_state()
    encoder_final_hidden = encoder.forward(input_sequence, encoder_init_hidden)

    decoder_hidden = encoder_final_hidden
    #decoder_prev_word = torch.tensor([[tgt_vocab.stoi(START)]], device='cuda')
    decoder_prev_word = torch.tensor([[tgt_vocab.stoi[START]]])

    loss = 0

    # Fill in the decoder loop here

    for decoder_index in range(target_length):
        decoder_output, decoder_hidden = decoder.forward(decoder_prev_word, decoder_hidden)
        loss += loss_function((decoder_output.squeeze()).unsqueeze(0), target_sequence[decoder_index])

        use_teacher_forcing = random.random() < teacher_forcing_ratio

        if use_teacher_forcing:
            decoder_prev_word = target_sequence[decoder_index].unsqueeze(0)
        else:
            topv, topi = decoder_output.topk(1)
            decoder_prev_word = (topi.squeeze().detach()).view(1, 1)


    loss.backward()
    encoder_optimizer.step()
    decoder_optimizer.step()
    return loss.item() / target_length



from torch import optim

# Run training epochs and report the average loss per epoch
def train_epochs(train_data, tgt_vocab, encoder, decoder,
                num_epochs=1, learning_rate=0.01, teacher_forcing_ratio=0.5):
  encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
  decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)
  loss_function = nn.NLLLoss()

  # data_generator = torchtext.data.Iterator(
  #     dataset=train_data,
  #     batch_size=1,
  #     device='cuda',
  # )

  data_generator = torchtext.data.Iterator(
      dataset=train_data,
      batch_size=1,
      # device='cuda',
  )

  for e in range(num_epochs):
    print('Epoch %d' %e)
    count, epoch_loss = 0, 0
    for training_example in data_generator.__iter__():
      input_sequence = getattr(training_example, 'src')
      target_sequence, target_length = getattr(training_example, 'tgt')

      epoch_loss += train(input_sequence, target_sequence, target_length, tgt_vocab,
                          encoder, decoder, encoder_optimizer, decoder_optimizer,
                          loss_function, teacher_forcing_ratio)
      count += 1
    print('Loss %f' % (epoch_loss.item() / count))



import datetime

print(datetime.datetime.now())
train_epochs(train_data, tgt.vocab, encoder, decoder, num_epochs=1)
print(datetime.datetime.now())


encoder.load_state_dict(torch.load('E:/UTD/SEM3/NLP/ASSIGNMENTS/HW5/content/hw5.encoder'))
decoder.load_state_dict(torch.load('E:/UTD/SEM3/NLP/ASSIGNMENTS/HW5/content/hw5.decoder'))


# Fill in this function
# The argument input_sequence is a torch.Tensor
# The arguments src_vocab and tgt_vocab are torchtext.vocab.Vocab objects
# The arguments encoder and decoder are our Encoder and Decoder
# The argument max_length is an int
# The return type should be a list of strings
def generate(input_sequence, src_vocab, tgt_vocab, encoder, decoder, max_length=MAX_LEN):
    generated_words = []

    with torch.no_grad():
        # Fill in the encoder part and setting up for the decoder part here
        encoder_init_hidden = encoder.initialize_hidden_state()
        print(input_sequence.shape)
        encoder_final_hidden = encoder.forward(input_sequence, encoder_init_hidden)
        print(encoder_final_hidden.shape)

        decoder_hidden = encoder_final_hidden
        #decoder_prev_word_index = torch.tensor([[tgt_vocab.stoi[START]]], device='cuda')
        decoder_prev_word_index = torch.tensor([[tgt_vocab.stoi[START]]])

        print(decoder_prev_word_index.shape)

        # Fill in the decoder loop here
        for decoder_index in range(max_length):
            decoder_output, decoder_hidden = decoder.forward(decoder_prev_word_index, decoder_hidden)

            topv, topi = decoder_output.topk(1)
            decoder_prev_word_index = topi.squeeze().detach()
            decoder_prev_word = tgt_vocab.itos[decoder_prev_word_index.item()]
            if decoder_prev_word == END:
                break
            if decoder_prev_word == START:
                continue

            generated_words.append(decoder_prev_word)
            decoder_prev_word_index = decoder_prev_word_index.view(1, 1)


for i in range(5):
    input = random.choice(train_data.examples).src
    print(input)
    #input_sequence = torch.tensor([src.vocab.stoi[word] for word in input], device='cuda').unsqueeze(1)
    input_sequence = torch.tensor([src.vocab.stoi[word] for word in input]).unsqueeze(1)
    print(' '.join(generate(input_sequence, src.vocab, tgt.vocab, encoder, decoder)))
    print()

import math

# Fill in this function
# The arguments generated_words and target_words are lists of strings
# The return type should be a float
def bleu(generated_words, target_words, n=4):
    reference_length = len(target_words)
    output_length = len(generated_words)

    target_ngram_counts = compute_ngram_counts(target_words, n)
    generated_ngram_counts = compute_ngram_counts(generated_words, n)

    common_ngrams = generated_ngram_counts.keys() & target_ngram_counts.keys()

    ngram_matches_by_n = [0] * n
    possible_ngram_matches_by_n = [0] * n
    # print(common_ngrams)

    for ngram in common_ngrams:
        ngram_matches_by_n[len(ngram) - 1] += min(generated_ngram_counts[ngram], target_ngram_counts[ngram])

    for ngram_length in range(1, n + 1):
        possible_matches = output_length - ngram_length + 1
        if possible_matches > 0:
            possible_ngram_matches_by_n[ngram_length - 1] += possible_matches

    precisions = [0] * n
    for i in range(0, n):
        precisions[i] = (float(ngram_matches_by_n[i]) / possible_ngram_matches_by_n[i]) if (possible_ngram_matches_by_n[i] > 0) else 0.0

    if min(precisions) > 0:
        p_log_sum = sum((1. / n) * math.log(p) for p in precisions)
        precision_product = math.exp(p_log_sum)
    else:
        precision_product = 0

    brevity_penalty = min(1.0, float(output_length) / reference_length)

    return precision_product * brevity_penalty


def compute_ngram_counts(token_list, max_order):
    # Generate ngram tuples and store them in dictionary of counts for that tuple
    ngram_counts_dict = {}
    for order in range(1, max_order + 1):
        for idx in range(0, len(token_list) - order + 1):
            ngram = tuple(token_list[idx : idx + order])
            # print(ngram)
            # print(segment[i:i+order])
            if ngram in ngram_counts_dict:
                ngram_counts_dict[ngram] += 1
            else:
                ngram_counts_dict[ngram] = 1

    return ngram_counts_dict