from flask_frozen import Freezer
from mania30 import app

import datetime

x = datetime.datetime.now()
a = x.strftime("%U")

app.config['FREEZER_DESTINATION'] = a
app.config['FREEZER_STATIC_IGNORE'] = ['*.mp3']

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()