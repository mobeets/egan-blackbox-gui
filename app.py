import os
import json
import random
import string
from datetime import datetime, timedelta

import cherrypy
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'], input_encoding='utf-8')

HTML_TWEET_TEMPLATE_FILE = 'tweet.html'
HTML_SEARCH_TEMPLATE_FILE = 'search.html'
TWEETS_FILE = 'blackbox.json'

TITLE = '''Jennifer Egan's "Black Box"'''
class Root(object):
    def __init__(self, tweets):
        self.all_tweets = tweets
        self.chapter_numbers = [int(x) for x in list(self.all_tweets.keys())]
        self.max_number = max(self.chapter_numbers)
        self.ntweets = dict((ch, len(ts)) for ch, ts in self.all_tweets.items())

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/chapter/1")

    @cherrypy.expose
    def search(self, query=None):
        query = query.lower() if query else ''
        res = {}
        for ch, ts in self.all_tweets.items():
            ch = int(ch)
            for i, t in enumerate(reversed(ts)):
                if query and query in t['text']:
                    if ch not in res:
                        res[ch] = []
                    res[ch].append((i, t))
        out = 'Search results for <i>{0}</i>...<hr>'.format(query)
        for ch in sorted(res):
            ts = res[ch]
            out += '<h3>{0}</h3><ul>\n'.format(ch)
            for i, t in ts:
                url = '/chapter/{0}/{1}'.format(ch, i+1)
                out += '<li>{0} <a href="{1}">[link]</a></li>\n'.format(t['text'], url)
            out += '</ul>'
        tmp = lookup.get_template(HTML_SEARCH_TEMPLATE_FILE)
        # print out
        return tmp.render(title=TITLE, content=out)

    def fake_tco_link(self):
        N = 6
        url = random.sample(string.ascii_letters, N)
        url = ''.join(url)
        return 't.co/{0}...'.format(url)

    def convert_twitter_dt_str(self, tweet):
        t_dt_str = tweet['created_at']
        t_dt = datetime.strptime(t_dt_str, '%a %b %d %H:%M:%S +0000 %Y')
        t_dt = t_dt - timedelta(hours=5)
        return t_dt.strftime('%I:%M %p, %Y %b %d')

    @cherrypy.expose
    def tweets(self, number=None, offset=None):
        if number not in self.all_tweets:
            print('ERROR: {0} is not a key in all_tweets'.format(number))
            return json.dumps(["Sorry, something went wrong."])
        offset = int(offset) if offset else 1
        tweet_msgs = [tweet['text'] for tweet in reversed(self.all_tweets[number])][offset-1:]
        tweet_urls = [tweet['url'] for tweet in reversed(self.all_tweets[number])] # keep all for head.js jquery stuff
        tweet_dt_strs = [self.convert_twitter_dt_str(tweet) for tweet in reversed(self.all_tweets[number])]
        next_number = int(number) + 1
        next_link = ''
        if next_number > self.max_number:
            tweet_msgs += ['[THE END]'.format(TITLE)]
        else:
            tweet_msgs += ['[This is the end of chapter {0}. Click the link to continue.] '.format(number, TITLE)]
            next_link = '<a href="/chapter/{0}">{1}</a>'.format(next_number, self.fake_tco_link())
        return json.dumps({'tweet_msgs': tweet_msgs, 'tweet_urls': tweet_urls, 'tweet_dt_strs': tweet_dt_strs, 'next_link': next_link})

    @cherrypy.expose
    def chapter(self, number=None, offset=None):
        try:
            no = int(number)
            if no > self.max_number:
                raise cherrypy.HTTPRedirect("/chapter/1")
        except:
            raise cherrypy.HTTPRedirect("/chapter/1")
        prev_ch = '<a href="/chapter/{0}">PREV</a> -'.format(no-1) if no > 1 else ''
        next_ch = '- <a href="/chapter/{0}">NEXT</a>'.format(no+1) if no < self.max_number else ''
        of = 1
        if offset:
            try:
                of = int(offset)
                if of < 1 or of > self.ntweets[number]:
                    raise cherrypy.HTTPRedirect("/chapter/" + str(no))
            except:
                raise cherrypy.HTTPRedirect("/chapter/" + str(no))
        tweet_msgs = []
        tmp = lookup.get_template(HTML_TWEET_TEMPLATE_FILE)
        return tmp.render(title=TITLE, CHAPTER=number, OFFSET=of, NEXT_CHAPTER=next_ch, PREV_CHAPTER=prev_ch)

def load_tweets(infile):
    return json.load(open(infile))

def main():
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
        },
        '/favicon.ico': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(ROOTDIR, 'static', 'favicon.ico')
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    }

    tweets = load_tweets(TWEETS_FILE)
    cherrypy.quickstart(Root(tweets), '/', config=conf)

if __name__ == '__main__':
    main()
