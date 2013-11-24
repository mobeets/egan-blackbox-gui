import re
from urllib2 import urlopen

TWEET_URL = "https://twitter.com/nyerfiction/status/207985498579419136"

TITLE_KEY = '${TITLE}'
TYPED_DIV_VAL = 'typed'
LINK_DIV_VAL = 'tcolink'

DIV_STATS = """<ul class="stats">""", """</ul>"""

OLD_SCRIPT = """<script src="https://abs.twimg.com/c/swift/en/init.50f1dad2666e8a8d6b901950eb366dd58226ce51.js" async></script>"""
NEW_SCRIPT = """"""

OLD_TWEETER = """>Reply to @NYerFiction"""
NEW_TWEETER = """style="visibility: hidden; display: none;">"""

OLD_DROPDOWN = """div class="dropdown">"""
NEW_DROPDOWN = """div class="dropdown" style="visibility: hidden; display: none;">"""

OLD_TWEET_CONTENT = """<p class="js-tweet-text tweet-text">Human beings are fiercely, primordially resilient.</p>"""
NEW_TWEET_CONTENT = """<p class="js-tweet-text tweet-text" style="height:80px;"><span id="{0}"></span><span id="{1}"></span></p>""".format(TYPED_DIV_VAL, LINK_DIV_VAL)

OLD_TITLE = """<title>Twitter / NYerFiction: Human beings are fiercely, ...</title>"""
NEW_TITLE = """<title>{0}</title>""".format(TITLE_KEY)

OLD_BG_IMAGE = """https://abs.twimg.com/images/themes/theme1/bg.png"""
NEW_BG_IMAGE = """/templates/bb2.jpg"""

OLD_USERNAME = """>New Yorker Fiction<"""
NEW_USERNAME = """>Black Box<"""

OLD_HANDLE = """@</s><b>NYerFiction<"""
NEW_HANDLE = """</s><b>Jennifer Egan<"""

"""
http://12factor.net/backing-services

See that footer? A Prev/Next for each chapter would be nice.

"""
def replace_old_new(html):
    """
    todo: fetch current twitter html, once logged-in?
    """
    html = html.replace(OLD_TWEET_CONTENT, NEW_TWEET_CONTENT)
    html = html.replace(OLD_TITLE, NEW_TITLE)
    html = html.replace(OLD_SCRIPT, NEW_SCRIPT)
    html = html.replace(OLD_BG_IMAGE, NEW_BG_IMAGE)
    html = html.replace(OLD_USERNAME, NEW_USERNAME)
    html = html.replace(OLD_HANDLE, NEW_HANDLE)
    html = html.replace(OLD_TWEETER, NEW_TWEETER)
    html = html.replace(OLD_DROPDOWN, NEW_DROPDOWN)
    return html
    # x = urlopen(TWEET_URL)
    # y = x.readlines()
    # return '\n'.join(y)

def strip_tweet_stats(html):
    """
    Remove Retweets and Favorites
    """
    if DIV_STATS[0] not in html:
        return html
    before, after = html.split(DIV_STATS[0])
    _, _, after = after.partition(DIV_STATS[1])
    return before + after

def remove_urls(html):
    """
    if len(url) > 1 and not url.startswith('//')
    """
    regex = r'href="([^"]*")'
    remover = lambda match: match.group(0) if (len(match.group(1)) <= 1 or match.group(1).startswith('//') or match.group(1).startswith('http')) else 'href="' + 'https://www.twitter.com' + match.group(1) + '"'
    return re.sub(regex, remover, html)

def add_js_libs(html, jsfile):
    """
    Adds code for jquery and typed.js
    """
    js = open(jsfile).read()
    before, head, after = html.partition('<head>')
    return before + head + js + after

def write_template(infile, outfile, js_libs_infile):
    """
    todo:
        . change NYerFiction title
        . change all links to something fun
            . add pause button, link to current message, etc.
            . add tweet date
        . add prev/next
        . given url, add chapters
            . load up actual tweet json
    """
    html = open(infile).read()

    html = replace_old_new(html)
    html = strip_tweet_stats(html)
    html = remove_urls(html)
    html = add_js_libs(html, js_libs_infile)

    open(outfile, 'w').write(html)

if __name__ == '__main__':
    write_template()
