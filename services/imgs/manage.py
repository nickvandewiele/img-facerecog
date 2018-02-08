# users-service/manage.py
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
    """Seeds the database."""
    db.session.add(Image(path='F:/Pictures/2011-07/IMG_0024.JPG'))
    db.session.add(Image(path='F:/Pictures/2011-06/IMG_0002.JPG'))
    db.session.commit()

@manager.command
def seed_csv():
    """Seeds the database with the csv."""

    imgs = load_csv_into_dict('imgs.csv')
    for k, fpath in imgs.items():
        db.session.add(Image(path=fpath))
    db.session.commit()


def load_csv_into_dict(fpath):
    imgs = {}
    with open(fpath, 'r', errors='ignore') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.

        for row in reader:  
            imgid, imgpath = row[0], row[1:]
            imgpath = ','.join(imgpath)
            print(imgpath)
            imgs[imgid] = imgpath

    return imgs

if __name__ == '__main__':
    manager.run()