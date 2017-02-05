import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation
from random import randint
import timeit

class GenerativeNetwork:
    def __init__(self, corpus_path, weights):
        with open(corpus_path) as corpus_file:
            self.corpus = corpus_file.read()

        # Get a unique identifier for each char in the corpus,
        # then make some dicts to ease encoding and decoding
        self.chars = sorted(list(set(self.corpus)))
        self.encoding = {c: i for i, c in enumerate(self.chars)}
        self.decoding = {i: c for i, c in enumerate(self.chars)}

        # Some useful vars
        self.num_chars = len(self.chars)
        self.sentence_length = 50
        self.corpus_length = len(self.corpus)

        # Build our network
        self.model = Sequential()
        self.model.add(LSTM(256, input_shape=(self.sentence_length, self.num_chars)))
        self.model.add(Dense(self.num_chars))
        self.model.add(Activation('softmax'))
        self.model.load_weights(weights)
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')

    def generate(self, seed_phrase=""):
        seed_pattern = self.make_seed(seed_phrase)
        generated_text = ""

        X = np.zeros((1, self.sentence_length, self.num_chars), dtype=np.bool)
        for i, character in enumerate(seed_pattern):
            X[0, i, self.encoding[character]] = 1

        for i in range(500):
            prediction = np.argmax(self.model.predict(X, verbose=0))

            generated_text += self.decoding[prediction]

            activations = np.zeros((1, 1, self.num_chars), dtype=np.bool)
            activations[0, 0, prediction] = 1
            X = np.concatenate((X[:, 1:, :], activations), axis=1)

        formatted_text = self.format(generated_text)
        return formatted_text

    def make_seed(self, seed_phrase):
        if seed_phrase:
            phrase_length = len(seed_phrase)
            pattern = ""
            for i in range (0, self.sentence_length):
                pattern += seed_phrase[i % phrase_length]
        else:
            seed = randint(0, self.corpus_length - self.sentence_length)
            pattern = self.corpus[seed:seed + self.sentence_length]

        return pattern

    def format(self, text):
        formatted = text.split("\n")
        formatted = formatted[1:len(formatted) - 1]
        if formatted[-1][-1].isalnum():
            formatted[-1] += "."
        else:
            formatted[-1] = formatted[-1][:-1] + "."

        return formatted
