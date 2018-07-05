import unittest

from app import create_app, db


class TestBucketlist(unittest.TestCase):

    def setUp(self):
        from app.models import Bucketlist
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()
            bucketlist = Bucketlist(name='Go to Delaware')
            bucketlist.save()
            self.bucketlist_id = bucketlist.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_bucketlist_creation(self):
        res = self.client().post(
            '/bucketlists/', data={'name': 'Go to BoraBora'}
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to BoraBora', str(res.data))

    def test_list_bucketlists(self):
        res = self.client().get('/bucketlists/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Delaware', str(res.data))

    def test_get_bucketlist(self):
        res = self.client().get('/bucketlists/{}/'.format(self.bucketlist_id))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Delaware', str(res.data))

    def test_edit_bucketlist(self):
        self.client().post(
            '/bucketlists/',
            data={'name': 'Eat, pray, love'}
        )
        res =self.client().put(
            '/bucketlists/1/',
            data={
                'name': 'Eat, pray, die!'
            }
        )
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/bucketlists/1/')
        self.assertIn('die', str(res.data))

    def test_delete_bucketlist(self):
        self.client().post(
            '/bucketlists/',
            data={'name': 'Eat, pray, love'}
        )
        res = self.client().delete('/bucketlists/1/')
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/bucketlists/1/')
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
