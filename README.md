# shakespeare-LSTM

![Robot Shakespeare](https://vivshaw.github.io/images/robot-shakespeare-teaser.png)

a Keras neural network trained to write Shakespearean sonnets, with an [interactive Flask interface](http://robot-shakespeare.herokuapp.com/).

## Requirements

```
pip install tensorflow
pip install keras
pip install h5py
pip install Flask
pip install Flask-wtf
pip install gunicorn
```

## Training the network

```
python network/train.py
```

The weights will be checkpointed as hdf5 files with the format `weights-{epoch:02d}-{loss:.3f}.hdf5` and the model will be dumped as `model.yaml`. If you wish to use a different corpus, just drop it in & edit `network/train.py`.

## Generating text
Edit `network/generate.py` to use your new weights and model if desired, then:

```
python network/generate.py
```

## Typical output 

```
ake thee of thy sweet self dost see,
From heaven thee, as the beauty of thy didge?
Then were thou art my love whose soor coll, and she vounes,
That in my stars in his praise the ever wor,
Whose whould his spiret the deser thee is bart,
  And thou thy self dost thou mayst live in thee
  Then do I not the wrose to deepile lease.

The worthous shalt be bland nor my seas,
With pentter than the owness doth bear,
Where that beauty like of many a forming.
Thou art as find in that which the thing thee,
```

## Running the Flask app

```
python run-flask.py
```

If you wish to use different weights and model than I did, put them in `app/static/model.yaml` and `app/static/weights.hdf5`

## Heroku deployment

Should be as easy as:

```
heroku create
git push heroku master
```

You may need to `heroku ps:scale web=1` if it doesn't do so automatically.
