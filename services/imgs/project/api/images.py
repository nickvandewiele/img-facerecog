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
    '''
    GET: Show all the images in the database.
    '''

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


@imgs_blueprint.route('/images', methods=['POST'])
def add_image():
    '''
    POST: add new image to the database.
    
    If the path of the image already exists in the database, only overwrite if 
    a name is added to the record.

    '''    

    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }

    if not post_data:
        return jsonify(response_object), 400


    path = post_data.get('path')
    names = post_data.get('names')

    try:
        image = Image.query.filter_by(path=path).first()
        if not image:
            db.session.add(Image(path=path, names=names))
            db.session.commit()

            response_object = {
                        'status': 'success',
                        'message': f'{path} was added!'
                    }
            return jsonify(response_object), 201        
        else:

            if image.names is not None:
                response_object['message'] = 'Sorry. That image already exists.'
                return jsonify(response_object), 400
            elif names:
                image.names = names
                db.session.commit()

                response_object = {
                            'status': 'success',
                            'message': f'{path} was updated!'
                        }
                return jsonify(response_object), 201
            else:
                response_object['message'] = 'Name was not contained in payload.'
                return jsonify(response_object), 400

    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400

    