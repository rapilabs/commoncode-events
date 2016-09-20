import urllib
from collections import namedtuple
from datetime import datetime

import inflect
import requests
from flask import Flask, render_template
from whitenoise import WhiteNoise

flask = Flask(__name__)
app = WhiteNoise(flask, root='static/')

COMMONCODE_MEETUPS = (
    8084042,  # MelbDjango
    7138602,  # Meteor-Melbourne
    19140354, # MelbourneJS
)

Event = namedtuple('Event', ['name', 'when', 'description'])

p = inflect.engine()


def format_timestamp(timestamp):
    when = datetime.fromtimestamp(timestamp/1000)
    date = p.ordinal(when.day)
    return '{} {} {}'.format(when.strftime('%-I:%M%P, %a'), date, when.strftime('%B %Y'))


@flask.route('/')
def main():

    response = requests.get('https://api.meetup.com/2/events?{}'.format(urllib.parse.urlencode({
        'group_id': ','.join([str(x) for x in COMMONCODE_MEETUPS]),
    })))
    data = response.json()

    events = [
        Event(
            name='{}: {}'.format(item['group']['name'], item['name']),
            when=format_timestamp(item['time']),
            description=item['description']
        )
        for item in data['results']
    ]

    return render_template('layout.html', events=events)
