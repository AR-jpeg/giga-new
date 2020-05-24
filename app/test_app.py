import unittest
import app

class Tests(unittest.TestCase):

    def test_user(self):
        result = app.User(email='araoudupi@gmail.com', is_signed_in="F", username='aditya', hashed_password=b'123213', user_id='123')
        self.assertEqual()