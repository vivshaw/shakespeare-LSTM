import re
from app import app
from flask import render_template, request
from random import randint
from generative_net import GenerativeNetwork
from .forms import SonnetForm


def tag_seed(seed):
    # Grab a chunk of four words
    word_list = seed.split()
    i = randint(1, len(word_list) - 3)

    bad_start_end = ['on', 'of', 'from', "I", "O!", "and", "be", 'or', 'the']

    words = []
    for i, word in enumerate(word_list[i:i + 3]):
        if not word == "I" and not word == "O!":
            word = word.strip("',.;-!:?").lower()
        if i == 0 or i == 2:
            if word not in bad_start_end:
                words.append(word)
        else:
            words.append(word)

    tag = " ".join(words)
    return tag


@app.route('/write', methods=['GET', 'POST'])
def index():

    net = GenerativeNetwork("sonnets.txt", "model.yaml", "weights.hdf5")

    if request.method == 'GET':
        seed = net.make_seed()
        seed_tag = tag_seed(seed)

        sonnet_form = SonnetForm()
        sonnet_form.seed.data = seed
        sonnet_form.seed_tag.data = seed_tag

        return render_template('index.html',
                               title='0x53 48 41 4b 45',
                               form=sonnet_form)

    if request.method == 'POST':
        old_seed = request.form['seed']
        old_seed_tag = request.form['seed_tag']
        old_seed_phrase = request.form['seed_phrase']

        if old_seed_phrase:
            old_seed_tag = old_seed_phrase
            old_seed = net.make_seed(old_seed_phrase)

        message = net.generate(old_seed)

        # Make a new seed
        seed = net.make_seed()
        seed_tag = tag_seed(seed)

        # Make the form
        sonnet_form = SonnetForm()
        sonnet_form.seed.data = seed
        sonnet_form.seed_tag.data = seed_tag
        sonnet_form.seed_phrase.data = ""

        return render_template('sonnet.html',
                               title='0x53 48 41 4b 45',
                               message=message,
                               old_seed_tag=old_seed_tag,
                               form=sonnet_form)


@app.route('/')
def cover():
    return render_template('cover.html')