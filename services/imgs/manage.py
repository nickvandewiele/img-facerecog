# users-service/manage.py
import os
import csv
import unittest
from flask_script import Manager
from sqlalchemy import exc

from project import create_app, db
from project.api.models import Image
from project.api.fbr import recognize

app = create_app()
manager = Manager(app)

@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def seed_db():
    """Seeds the database with 2 images."""
    db.session.add(Image(path=os.path.join('project', 'examples', 'connie.jpg')))
    db.session.add(Image(path=os.path.join('project', 'examples', 'NicksParty-50.jpg')))
    db.session.commit()

@manager.command
def load_examples():
    '''Seeds the database with all the images found in the project/examples/* folder.'''
    imgs = {}

    walk_dir = os.path.join('project', 'examples')
    assert os.path.isdir(walk_dir)

    imgid = 0
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            _, ext = os.path.splitext(file_path)
            if ext.lower() in ['.jpg', '.png']:
                imgs[imgid] = file_path
                imgid += 1    

    for k, fpath in imgs.items():
        db.session.add(Image(path=fpath))
    db.session.commit()

@manager.command
def recognize_ex():
    ''' Iterate over database images, and make call to the FB recognize API, if no
    names have been found.'''

    imgs = Image.query.all()

    imgs = list(filter(lambda img: img.names is None, imgs))

    print('No. of images to be tagged: {}'.format(len(imgs)))
    try:
        for img in imgs:
            img_path = os.path.abspath(img.path)
            print(img_path)
            assert os.path.isfile(img_path), 'Could not find image path: {}'.format(img_path)

            resp = recognize(img_path)

            if resp:
                names = list(map(lambda d: d['name'], resp))
                print('Identified names: {}'.format(names))
                img.names = ','.join(names)            
            else:
                print('No recognized names for {}'.format(img_path))
                pass
        db.session.commit()
 
    except exc.IntegrityError as e:
        db.session.rollback()

if __name__ == '__main__':
    manager.run()