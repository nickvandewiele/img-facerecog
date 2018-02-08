from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc

from project.api.models import Image
from project import db

imgs_blueprint = Blueprint('images', __name__, template_folder='./templates')


@imgs_blueprint.route('/imgs/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@imgs_blueprint.route('/imgs', methods=['GET'])
def get_all_images():
    """Get all users"""
    response_object = {
        'status': 'success',
        'data': {
            'images': [image.to_json() for image in Image.query.all()]
        }
    }
    return jsonify(response_object), 200

@imgs_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['path']
        db.session.add(Image(path='F:/Pictures/2011-07/IMG_0024.JPG'))
        db.session.commit()
    images = Image.query.all()
    return render_template('index.html', images=images)
