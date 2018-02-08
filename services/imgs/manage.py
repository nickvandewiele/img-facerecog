# users-service/manage.py
import os
import csv
import unittest
from flask_script import Manager

from project import create_app, db
from project.api.models import Image

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

if __name__ == '__main__':
    manager.run()