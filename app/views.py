from app import app
from flask import render_template, request
from random import randint
from .forms import SonnetForm
from network.generate import GenerativeNetwork

net = GenerativeNetwork("sonnets.txt", "app/static/model.yaml", "app/static/weights.hdf5")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/write', methods=['GET', 'POST'])
def sonnet():
    if request.method == 'GET':
        seed = net.make_seed()
        seed_tag = tag_seed(seed)

        sonnet_form = SonnetForm()
        sonnet_form.seed.data = seed
        sonnet_form.seed_tag.data = seed_tag

        return render_template('intro.html',
                               title='ROBOT SHAKESPEARE',
                               form=sonnet_form)

    if request.method == 'POST':
        old_seed = request.form['seed']
        old_seed_tag = request.form['seed_tag']
        old_seed_phrase = request.form['seed_phrase']

        if old_seed_phrase:
            old_seed_tag = old_seed_phrase
            old_seed = net.make_seed(old_seed_phrase)

        message = format_sonnet(net.generate(old_seed))

        # Make a new seed
        seed = net.make_seed()
        seed_tag = tag_seed(seed)

        # Make the form
        sonnet_form = SonnetForm()
        sonnet_form.seed.data = seed
        sonnet_form.seed_tag.data = seed_tag
        sonnet_form.seed_phrase.data = ""

        return render_template('sonnet.html',
                               title='ROBOT SHAKESPEARE',
                               message=message,
                               old_seed_tag=old_seed_tag,
                               form=sonnet_form)


def format_sonnet(text):
    formatted = text.split("\n")

    # The first and last line cut off in the middle, so we'll ditch them
    formatted = formatted[1:len(formatted) - 1]

    # Eliminate empty strings, strings that are just newlines, or other improper strings
    formatted = [string for string in formatted if len(string) > 3]

    # Put a period on our last string, replacing other punctuation if it's there.
    if formatted[-1][-1].isalnum():
        formatted[-1] += "."
    else:
        formatted[-1] = formatted[-1][:-1] + "."

    return formatted


def tag_seed(seed):
    # Grab a chunk of three words
    word_list = seed.split()
    i = randint(1, len(word_list) - 3)

    bad_start_end = set(['on', 'of', 'from', "I", "O!", "and", "be", 'or', 'the', 'than', 'with', 'by'])
    bad_start = set(['of'])
    bad_end = set(['no', 'an', 'if'])

    words = []
    for i, word in enumerate(word_list[i:i + 3]):
        if not word == "I" and not word == "O!":
            word = word.strip("',.;-!:?").lower()
        if i == 0 and word not in bad_start_end | bad_start:
            words.append(word)
        if i == 1:
            words.append(word)
        if i == 2 and word not in bad_start_end | bad_end:
            words.append(word)

    tag = " ".join(words)
    return tag
