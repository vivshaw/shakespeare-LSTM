import re
from app import app
from flask import render_template, request
from random import randint
from generative_net import GenerativeNetwork
from .forms import SonnetForm

def tag_seed(seed):
    word_list = seed.split(" ")
    i = randint(1, len(word_list) - 3)
    words = word_list[i:i + 3]
    return " ".join(words)


@app.route('/', methods=['GET', 'POST'])
def index():

    net = GenerativeNetwork("sonnets.txt", "model.yaml", "weights.hdf5")
    if request.method == 'GET':
        seed = net.make_seed()
        seed_tag = tag_seed(seed)

        sonnet_form = SonnetForm(seed=seed, seed_tag=seed_tag)

        return render_template('index.html',
                               title='0x53 48 41 4b 45',
                               form=sonnet_form,
                               seed_tag=seed_tag)

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

        sonnet_form = SonnetForm(seed=seed, seed_tag=seed_tag)

        return render_template('sonnet.html',
                               title= '0x53 48 41 4b 45',
                               message=message,
                               old_seed_tag=old_seed_tag,
                               seed_tag=seed_tag,
                               form=sonnet_form)
