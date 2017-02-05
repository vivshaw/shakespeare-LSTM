from app import app
from app.predicter_nnet import GenerativeNetwork

@app.route('/')
@app.route('/index')
def index():
    net = GenerativeNetwork("sonnets.txt", "weights-29-0.8985.hdf5")
    message = net.generate()

    output = ""
    for line in message:
        output += "<p>" + line + "</p>"

    return output
