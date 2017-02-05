from app import app
from generative_net import GenerativeNetwork

@app.route('/')
@app.route('/index')
def index():
    net = GenerativeNetwork("sonnets.txt", "weights.hdf5")
    message = net.generate()

    output = ""
    for line in message:
        output += "<p>" + line + "</p>"

    return output
