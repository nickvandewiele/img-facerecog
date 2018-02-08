import os
from configparser import ConfigParser

from fbrecog import FBRecog

def read_config(ini):
    '''read user access token, and fb_dtsg'''

    assert os.path.isfile(ini), 'Could not find .ini file: {}...'.format(ini)

    dict1 = {}

    SECTION = 'FB'

    config = ConfigParser()
    config.read(ini)
    options = config.options(SECTION)

    for option in options:
        dict1[option] = config.get(SECTION, option)
    return dict1


def read_cookie(ck):
    with open(ck, 'r') as f_in:
        cookie = f_in.read()
    return cookie

def recognize(img_path):
    '''
    - input is an absolute path to an image.
    - makes call to FB graph API to recognize faces in the picture.
    - returns a list of dictionaries [{'certainity': 0.999, 'name': 'XXX'}, ...]
    '''
    options = read_config('config.ini')

    access_token = options['access_token']
    fb_dtsg = options['fb_dtsg']
    cookie = read_cookie('cookie.txt')

    assert os.path.isfile(img_path), 'Could not find image file: {}'.format(img_path)

    return FBRecog(access_token, cookie, fb_dtsg).recognize(img_path)
    