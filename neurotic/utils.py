import six

COLOR_NAMES = ('red', 'green', 'blue', 'magenta', 'cyan', 'gray')
COLORS = dict(zip(COLOR_NAMES, range(31, 38)))
BACKGROUND_COLORS = dict(zip(COLOR_NAMES, range(41, 48)))

if six.PY3:
    OK = '\u2713'
    ERROR = '\u2717'
else:
    OK = u'\u2713'.encode('utf8')
    ERROR = u'\u2717'.encode('utf8')

def color(text, color=None, background=None):
    if color:
        text = '\033[%dm%s\033[0m' % (COLORS[color], text)
    if background:
        text = '\033[%dm%s\033[0m' % (BACKGROUND_COLORS[background], text)
    return text
