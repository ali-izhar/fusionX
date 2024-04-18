import unittest

class TestFlaskApp(unittest.TestCase):
    def test_run_app(self):
        from app import create_app
        app = create_app()
        with app.test_client() as client:
            # Make a test request to the root endpoint
            response = client.get('/')
            # Assert that the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()

# python -m unittest discover -s tests


# import pytest
# from app import create_app

# @pytest.fixture
# def app():
#     app = create_app()
#     return app

# @pytest.fixture
# def client(app):
#     return app.test_client()

# def test_index(client):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert b"Hello, World!" in response.data

# if __name__ == '__main__':
#     pytest.main()
