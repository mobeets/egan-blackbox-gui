import re
from urllib2 import urlopen

TWEET_URL = "https://twitter.com/nyerfiction/status/207985498579419136"

CHAPTER_KEY = '${CHAPTER}'
PREV_CHAPTER_KEY = '${PREV_CHAPTER}'
NEXT_CHAPTER_KEY = '${NEXT_CHAPTER}'
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
NEW_TWEET_CONTENT = """<p class="js-tweet-text tweet-text" style="height:120px;"><span id="{0}"></span><span id="{1}"></span></p>""".format(TYPED_DIV_VAL, LINK_DIV_VAL)

OLD_TITLE = """<title>Twitter / NYerFiction: Human beings are fiercely, ...</title>"""
NEW_TITLE = """<title>{0}</title>""".format(TITLE_KEY)

OLD_BG_IMAGE = """https://abs.twimg.com/images/themes/theme1/bg.png"""
NEW_BG_IMAGE = """/templates/bb2.jpg"""

OLD_USERNAME = """>New Yorker Fiction<"""
NEW_USERNAME = """>Black Box<"""

OLD_HANDLE = """@</s><b>NYerFiction<"""
NEW_HANDLE = """</s><b>by Jennifer Egan<"""

OLD_FOLLOW = """<i class="follow"></i> Follow"""
NEW_FOLLOW = """<i class="follow"></i> <span class="typing-status">Pause</span>"""

OLD_FOLLOW_BTN = """<button class="js-follow-btn follow-button btn" type="button">"""
NEW_FOLLOW_BTN = """<button class="js-follow-btn follow-button btn" type="button" onclick="PauseButtonClicked();">"""

OLD_TWITTER_PROFILE = 'href="/NYerFiction"'
NEW_TWITTER_PROFILE = 'href="http://www.newyorker.com/fiction/features/2012/06/04/120604fi_fiction_egan"'

OLD_DATE = """7:03 PM - 30 May 12<"""
NEW_DATE = """7:03 PM - 30 May 12 / via <a href="https://twitter.com/nyerfiction">@NYerFiction</a><"""

OLD_REPLY = """Reply"""
NEW_REPLY = """View tweet"""

OLD_FAVORITE = """Favorite"""
NEW_FAVORITE = """About"""

OLD_RETWEET = """Retweet"""
NEW_RETWEET = """Link here"""

OLD_REPLY_BTN = 'data-modal="tweet-reply" href="#"'
NEW_REPLY_BTN = 'data-modal="tweet-reply" href="https://twitter.com/nyerfiction/status/"'

OLD_RETWEET_BTN = 'data-modal="tweet-retweet" href="#"'
NEW_RETWEET_BTN = 'data-modal="tweet-retweet" href="/chapter/${CHAPTER}/"'

OLD_FAVE_BTN = 'class="with-icn favorite js-tooltip" href="#"'
NEW_FAVE_BTN = 'class="with-icn favorite js-tooltip" href="http://blog.jehosafet.com/2013/11/jennifer-egans-black-box-full-text.html"'

OLD_BUTTON_1 = 'title="Direct messages"'
NEW_BUTTON_1 = 'title="Direct messages" style="visibility: hidden; display: none;"'

OLD_BUTTON_2 = 'title="Compose new Tweet"'
NEW_BUTTON_2 = 'title="Compose new Tweet" style="visibility: hidden; display: none;"'

OLD_BUTTON_3 = 'href="https://www.twitter.com/settings/account"'
NEW_BUTTON_3 = 'href="https://github.com/mobeets/egan-blackbox-gui"'

OLD_FOOTER = """inline-reply-tweetbox swift">"""
NEW_FOOTER = """inline-reply-tweetbox swift"><div class="module site-footer slim-site-footer">
  <div class="flex-module"><ul class=""><li><span class="prev_chapter"></span></li><li><ul><span class="this_chapter">CHAPTER {0}</span></ul></li><li><span class="next_chapter"></span></li></ul></div></div>""".format(CHAPTER_KEY)

OLD_COPYRIGHT = """<div class="permalink-footer">
  <div class="module site-footer slim-site-footer">"""
NEW_COPYRIGHT = """<div class="permalink-footer" style="visibility: hidden; display: none;">
  <div class="module site-footer slim-site-footer">"""

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
    html = html.replace(OLD_FOLLOW, NEW_FOLLOW)
    html = html.replace(OLD_FOLLOW_BTN, NEW_FOLLOW_BTN)
    html = html.replace(OLD_TWITTER_PROFILE, NEW_TWITTER_PROFILE)
    html = html.replace(OLD_DATE, NEW_DATE)
    html = html.replace(OLD_FAVORITE, NEW_FAVORITE)
    html = html.replace(OLD_RETWEET, NEW_RETWEET)
    html = html.replace(OLD_REPLY, NEW_REPLY)
    html = html.replace(OLD_BUTTON_1, NEW_BUTTON_1)
    html = html.replace(OLD_BUTTON_2, NEW_BUTTON_2)
    html = html.replace(OLD_BUTTON_3, NEW_BUTTON_3)
    html = html.replace(OLD_FOOTER, NEW_FOOTER)
    html = html.replace(OLD_COPYRIGHT, NEW_COPYRIGHT)
    html = html.replace(OLD_REPLY_BTN, NEW_REPLY_BTN)
    html = html.replace(OLD_RETWEET_BTN, NEW_RETWEET_BTN)
    html = html.replace(OLD_FAVE_BTN, NEW_FAVE_BTN)
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
    regex = r'href="([^"]*)"'
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
        . Fix tweet date: for each original tweet
        . Fix Search button: filter tweets by query

        . Make static, i.e. no external links...download twitter's style stuff so it won't be effected by changes

    """
    html = open(infile).read()

    html = strip_tweet_stats(html)
    html = remove_urls(html)
    html = add_js_libs(html, js_libs_infile)
    html = replace_old_new(html)

    open(outfile, 'w').write(html)

if __name__ == '__main__':
    write_template()
