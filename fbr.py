import os
from configparser import ConfigParser

from fbrecog import FBRecog

def read_config(ini):
    '''read user access token, and fb_dtsg'''
    dict1 = {}

    SECTION = 'FB'

    config = ConfigParser()
    config.read(ini)
    options = config.options(SECTION)

    for option in options:
            dict1[option] = config.get(SECTION, option)
    return dict1

    print(dict1)

def read_cookie(ck):
    with open(ck, 'r') as f_in:
        cookie = f_in.read()
    return cookie

def recognize(img):
    '''
    returns a list of dictionaries
    [{'certainity': 0.999, 'name': 'XXX'}, ...]
    '''
    options = read_config('config.ini')

    access_token = options['access_token']
    fb_dtsg = options['fb_dtsg']
    cookie = read_cookie('cookie.txt')

    return FBRecog(access_token, cookie, fb_dtsg).recognize(img)

def test_recognize():
    img = os.path.join('imgs', 'NicksParty-50.jpg')
    resp = recognize(img)

    expected = ['IYun Hsieh', 'Perman Jo']
    for entry in resp:
        assert entry['name'] in expected

if __name__ == "__main__":
    test_recognize()