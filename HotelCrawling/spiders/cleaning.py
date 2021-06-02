import re

def clean_text(s):
    if not s:
        return ''
    if len(s) > 0:
        return re.sub('\n', '', s).strip()
    else:
        return ''


def clean_text_list(text_list):
    if not text_list:
        return []
    if len(text_list) > 0:
        text_list = list(set(text_list))
        return [clean_text(text) for text in text_list if text != '\n']
    else:
        return []


def get_date_from_string(s): # '... Ngay xx thang xx nam xx'
    if not s:
        return None
    idx = s.find('Ngày')
    if idx != -1:
        s = s[idx:].split()
        return s[1] + '/' + s[3] + '/' + s[5]
    else:
        return None