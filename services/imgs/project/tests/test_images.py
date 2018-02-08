import os

import json
import unittest

from project import db
from project.api.models import Image
from project.tests.base import BaseTestCase


def add_image(fpath, names=None):
    image = Image(path=fpath, names=names)
    db.session.add(image)
    db.session.commit()
    return image

class TestImageService(BaseTestCase):
    """Tests for the Images Service."""

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_recognize(self):
        """Ensure get single image recognized behaves correctly."""
        image = add_image(os.path.join('project', 'examples', 'NicksParty-50.jpg'))
        with self.client:
            response = self.client.get(f'/recognize/{image.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)

            fb_resp = data['data']['resp']
            for entry in fb_resp:
                self.assertIn(entry['name'], ['IYun Hsieh', 'Perman Jo'])

            self.assertIn('success', data['status'])

    def test_main_no_images(self):
        """Ensure the main route behaves correctly when no images have been
    added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Images</h1>', response.data)
        self.assertIn(b'<p>No images!</p>', response.data)

    def test_main_with_images(self):
        """Ensure the main route behaves correctly when images have been
    added to the database."""
        img1 = add_image(os.path.join('project', 'examples', 'Foo.jpg'))
        img2 = add_image(os.path.join('project', 'examples', 'Bar.jpg'))

        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Images</h1>', response.data)
            self.assertNotIn(b'<p>No images!</p>', response.data)
            self.assertIn(b'Foo', response.data)
            self.assertIn(b'Bar', response.data)

    def test_main_with_images_with_names(self):
        """Ensure the main route behaves correctly when image with an
        associated name has been added to the database."""
        img1 = add_image(os.path.join('project', 'examples', 'Foo.jpg'), names='Foo')

        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Images</h1>', response.data)
            self.assertNotIn(b'<p>No images!</p>', response.data)
            self.assertIn(b'Foo', response.data)
            self.assertIn(b'Foo', response.data)

    def test_main_post(self):
        """Ensure a post on the main page leads to a new entry in the database."""
        dummy_path = os.path.join('project', 'examples', 'Foo.jpg')
        with self.client:
            response = self.client.post(
                '/images',
                data=json.dumps({
                    'path': dummy_path,
                    'names': 'Foo'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('{} was added!'.format(dummy_path), data['message'])
            self.assertIn('success', data['status'])

    def test_update_record(self):
        '''Ensure that a record can be updated in the database.'''

        # add image without a name
        dummy_path = os.path.join('project', 'examples', 'Foo.jpg')
        img1 = add_image(dummy_path)

        # post the same image path, but add a name now.
        with self.client:
            response = self.client.post(
                '/images',
                data=json.dumps({
                    'path': dummy_path,
                    'names': 'Foo'
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('{} was updated!'.format(dummy_path), data['message'])
            self.assertIn('success', data['status'])

            # check if the Image object in the database contains the expected name
            img2 = Image.query.filter_by(path=dummy_path).first()
            self.assertEqual(img2.names, 'Foo')



if __name__ == '__main__':
    unittest.main()    