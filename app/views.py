from app import app
from flask import render_template, request
from generative_net import GenerativeNetwork

@app.route('/', methods=['GET', 'POST'])
def index():
    net = GenerativeNetwork("sonnets.txt", "model.yaml", "weights.hdf5")
    if request.method == 'GET':
        return render_template('index.html',
                               title="0x53 48 41 4b 45")

    if request.method == 'POST':
        message = net.generate()

        return render_template('index.html',
                               title="0x53 48 41 4b 45",
                               message=message)
