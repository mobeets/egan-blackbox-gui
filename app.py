import os
import json
import random
import string

import cherrypy
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'], input_encoding='utf-8')

from init import write_template, TYPED_DIV_VAL, LINK_DIV_VAL

HTML_TEMPLATE_FILE = 'index.html'
IN_HTML_FILE = 'templates/og_index.html'
OUT_HTML_FILE = 'templates/' + HTML_TEMPLATE_FILE
JS_LIBS_FILE = 'js/head.js'
TWEETS_FILE = 'blackbox.json'

TITLE = '''Jennifer Egan's "Black Box"'''
class Root(object):
    def __init__(self, infile, tweets):
        self.infile = infile
        self.all_tweets = tweets
        self.chapter_numbers = [int(x) for x in self.all_tweets.keys()]
        self.max_number = max(self.chapter_numbers)

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/chapter/1")

    def fake_tco_link(self):
        N = 6
        url = random.sample(string.letters, N)
        url = ''.join(url)
        return 't.co/{0}...'.format(url)

    @cherrypy.expose
    def tweets(self, number=None):
        if number not in self.all_tweets:
            print 'ERROR: {0} is not a key in all_tweets'.format(number)
            return json.dumps(["Sorry, something went wrong."])
        tweet_msgs = [tweet['text'] for tweet in reversed(self.all_tweets[number])]
        next_number = int(number) + 1
        next_link = ''
        if next_number == self.max_number:
            tweet_msgs += ['[THE END]'.format(TITLE)]
        else:
            tweet_msgs += ['[This is the end of chapter {0}. Click the link to continue.] '.format(number, TITLE)]
            next_link = '<a href="/chapter/{0}">{1}</a>'.format(next_number, self.fake_tco_link())
        return json.dumps({'tweet_msgs': tweet_msgs, 'next_link': next_link})

    @cherrypy.expose
    def chapter(self, number=None):
        tweet_msgs = []
        tmp = lookup.get_template(self.infile)
        return tmp.render(TITLE=TITLE, TYPED_DIV_VAL=TYPED_DIV_VAL, LINK_DIV_VAL=LINK_DIV_VAL, CHAPTER=number)

def load_tweets(infile):
    return json.load(open(infile))

def main():
    write_template(IN_HTML_FILE, OUT_HTML_FILE, JS_LIBS_FILE)
    cherrypy.config.update({'server.socket_host': '0.0.0.0',})
    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})

    ROOTDIR = os.path.dirname(os.path.abspath(__file__))
    conf = {
        '/': {
            'tools.staticdir.root': ROOTDIR,
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
        },
        '/templates': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'templates'
        }
    }

    tweets = load_tweets(TWEETS_FILE)
    cherrypy.quickstart(Root(HTML_TEMPLATE_FILE, tweets), '/', config=conf)

if __name__ == '__main__':
    main()
