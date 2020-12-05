import re
import time
import emoji
import string
from nlp_indo_word import kamus_alay_map, abbr_map, formal_map, stop_map

# ==========================================================================================================

try:
    uchr = unichr  # Python 2
    import sys
    if sys.maxunicode == 0xffff:
        # narrow build, define alternative unichr encoding to surrogate pairs
        # as unichr(sys.maxunicode + 1) fails.
        def uchr(codepoint):
            return (
                unichr(codepoint) if codepoint <= sys.maxunicode else
                unichr(codepoint - 0x010000 >> 10 | 0xD800) +
                unichr(codepoint & 0x3FF | 0xDC00)
            )
except NameError:
    uchr = chr  # Python 3

# Unicode 11.0 Emoji Component map (deemed safe to remove)
_removable_emoji_components = (
    (0x20E3, 0xFE0F),             # combining enclosing keycap, VARIATION SELECTOR-16
    range(0x1F1E6, 0x1F1FF + 1),  # regional indicator symbol letter a..regional indicator symbol letter z
    range(0x1F3FB, 0x1F3FF + 1),  # light skin tone..dark skin tone
    range(0x1F9B0, 0x1F9B3 + 1),  # red-haired..white-haired
    range(0xE0020, 0xE007F + 1),  # tag space..cancel tag
)
emoji_components = re.compile(u'({})'.format(u'|'.join([
    re.escape(uchr(c)) for r in _removable_emoji_components for c in r])),
    flags=re.UNICODE)

# ========================================================================================================


def remove_hashtags(text):
    all_hasht = {i:'' for i in text.split() if i[0] == '#'}
    if len(all_hasht) == 0:
        return text
    else:
        return replace_word_dict(text, all_hasht)

def replace_word_dict(text, dictionary): # from https://stackoverflow.com/questions/51102201/replace-a-string-using-dictionary-regex
    pattern = re.compile(r'(?<!\w)(' + '|'.join(re.escape(key) for key in dictionary.keys()) + r')(?!\w)')
    result = pattern.sub(lambda x: dictionary[x.group()], text)
    return result

def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def remove_html(text):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)

def remove_punc(txt):
    return txt.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).replace(' '*4, ' ').replace(' '*3, ' ').replace(' '*2, ' ').strip()

def extract_emojis(text):
    emojis = list(set(emoji.demojize(''.join(c for c in text if c in emoji.UNICODE_EMOJI), delimiters=('', ' ')).split()))
    if len(emojis) == 0:
        return ''
    elif len(emojis) != 0:
        emojis = ', '.join([re.sub('_', ' ', i) for i in emojis])
        return emojis


def extract_hasht(text):
    hasht = set([i for i in text.split() if i[0] == '#'])
    return ' '.join([split_hasht(i) for i in hasht])

def remove_username(string):
    return re.sub('@[^\s]+',' USER ', string)


# from https://stackoverflow.com/questions/44987406/regex-to-split-a-hashtag-into-words
def split_hasht(text):
    return " ".join([a for a in re.split('([A-Z][a-z]+)', text) if a][1:])


def remove_emoji(txt, remove_components=False):
    cleaned = emoji.get_emoji_regexp().sub(u'', txt)
    if remove_components:
        cleaned = emoji_components.sub(u'', cleaned)
    return cleaned

def remove_digits(txt):
    return re.sub("^\d+\s|\s\d+\s|\s\d+$", " angka ", txt)

def clean_text(txt, debug=False):
    start = time.time()
    
    txt = remove_username(txt)
    txt = remove_hashtags(txt)
    txt = remove_urls(txt)
    txt = remove_html(txt)
    txt = remove_emoji(txt)
    txt = remove_punc(txt)
    txt = remove_digits(txt)
    txt = replace_word_dict(txt, kamus_alay_map)
    txt = replace_word_dict(txt, abbr_map)
    txt = replace_word_dict(txt, formal_map)
    txt = replace_word_dict(txt, stop_map)

    txt = ' '.join(txt.split()).lower()
    if debug:
        print('finished, time: ', time.time()-start)


    return txt