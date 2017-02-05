import re
from app import app
from flask import render_template, request
from random import randint
from generative_net import GenerativeNetwork

@app.route('/', methods=['GET', 'POST'])
def index():
    net = GenerativeNetwork("sonnets.txt", "model.yaml", "weights.hdf5")
    if request.method == 'GET':
        return render_template('index.html',
                               title="0x53 48 41 4b 45")

    if request.method == 'POST':
        seed_phrase = request.form['seed']
        seed = net.make_seed(seed_phrase)
        message = net.generate(seed)

        if not seed_phrase:
            word_list = seed.split(" ")
            i = randint(1, len(word_list) - 3)
            words = word_list[i:i + 3]
            seed_phrase = " ".join(words)

        return render_template('index.html',
                               title="0x53 48 41 4b 45",
                               message=message,
                               seed=seed_phrase)
