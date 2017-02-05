import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation
from random import randint
import sys

with open("sonnets.txt") as corpus_file:
    corpus = corpus_file.read()

# Get a unique identifier for each char in the corpus, then make some dicts to ease encoding and decoding
chars = sorted(list(set(corpus)))
encoding = {c: i for i, c in enumerate(chars)}
decoding = {i: c for i, c in enumerate(chars)}

num_chars = len(chars)
sentence_length = 50
corpus_length = len(corpus)
weights = "weights-29-0.8985.hdf5"

model = Sequential()
model.add(LSTM(256, input_shape=(sentence_length, num_chars)))
model.add(Dense(num_chars))
model.add(Activation('softmax'))
model.load_weights(weights)
model.compile(loss='categorical_crossentropy', optimizer='adam')

phrase = ""

if phrase:
    phrase_length = len(phrase)
    seed_pattern = ""
    for i in range (0, sentence_length):
        seed_pattern += phrase[i % phrase_length]
else:
    seed = randint(0, corpus_length - sentence_length)
    seed_pattern = corpus[seed:seed + sentence_length]

print("Seed pattern:")
print(seed_pattern)
print("---------")

X = np.zeros((1, sentence_length, num_chars), dtype=np.bool)
for i, character in enumerate(seed_pattern):
    X[0, i, encoding[character]] = 1

out = ""

for i in range(500):
    prediction = np.argmax(model.predict(X, verbose=0))

    out += decoding[prediction]

    activations = np.zeros((1, 1, num_chars), dtype=np.bool)
    activations[0, 0, prediction] = 1
    X = np.concatenate((X[:, 1:, :], activations), axis=1)

print(out)