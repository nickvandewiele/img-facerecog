import os

from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc

from project.api.models import Image
from project import db

from project.api.fbr import recognize

imgs_blueprint = Blueprint('images', __name__, template_folder='./templates')

@imgs_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    '''ping-pong for sanity check.'''
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@imgs_blueprint.route('/', methods=['GET'])
def index():
    '''Show all the images in the database.'''
    images = Image.query.all()
    return render_template('index.html', images=images)

@imgs_blueprint.route('/recognize/<img_id>', methods=['GET'])
def recognize_img(img_id):
    '''make a call to the FB recognize API for the image whose ID is provided'''
    post_data = request.get_json()

    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }


    img = Image.query.filter_by(id=int(img_id)).first()
    if not img:
        return jsonify(response_object), 404
    else:
        img_path = os.path.abspath(img.path)
        assert os.path.isfile(img_path), 'Could not find image path: {}'.format(img_path)

        resp = recognize(img_path)

        response_object = {
            'status': 'success',
            'data': {
                'resp': resp
            }
        }
        return jsonify(response_object), 200