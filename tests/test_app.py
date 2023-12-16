import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from your_app_module import app, is_mysql_available, add_colis, post_route2, post_route3, get_route

class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up a test client
        self.app = app.test_client()

    @patch("your_app_module.mysql.connector.connect")
    def test_is_mysql_available(self, mock_connect):
        # Mock the MySQL connection
        mock_connect.return_value = MagicMock()

        # Call the function and assert
        result = is_mysql_available()
        self.assertTrue(result)

    @patch("your_app_module.mysql.connector.connect")
    def test_add_colis(self, mock_connect):
        # Mock the MySQL connection
        mock_connect.return_value = MagicMock()

        # Mock the request data
        mock_request_data = {
            "id": 1,
            "adresse_x": 123,
            "adresse_y": 456
        }

        # Mock the MySQL cursor
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (1, )  # Mock the result of the SELECT query

        # Make the request to the endpoint
        response = self.app.post('/add_colis', json=mock_request_data)

        # Assert the response status code
        self.assertEqual(response.status_code, 201)

        # Add more assertions if needed

    @patch("your_app_module.requests.post")
    def test_post_route2(self, mock_post):
        # Mock the POST request to the other microservice
        mock_post.return_value.status_code = 200

        # Mock the request data
        mock_request_data = {
            "colis_id": 1,
            "etat_colis": 1
        }

        # Make the request to the endpoint
        response = self.app.post('/postPosColisFromDevice', json=mock_request_data)

        # Assert the response status code
        self.assertEqual(response.status_code, 201)

        # Add more assertions if needed

    @patch("your_app_module.requests.post")
    def test_post_route3(self, mock_post):
        # Mock the POST request to the other microservice
        mock_post.return_value.status_code = 200

        # Mock the request data
        mock_request_data = {
            "camion_id": 1,
            "camion_pos_x": 123,
            "camion_pos_y": 456
        }

        # Make the request to the endpoint
        response = self.app.post('/postPosCamionFromDevice', json=mock_request_data)

        # Assert the response status code
        self.assertEqual(response.status_code, 201)

        # Add more assertions if needed

    @patch("your_app_module.mysql.connector.connect")
    @patch("your_app_module.mysql.connector.connect")
    def test_get_route(self, mock_connect1, mock_connect2):
        # Mock the MySQL connections
        mock_connect1.return_value = MagicMock()
        mock_connect2.return_value = MagicMock()

        # Mock the MySQL cursor
        mock_cursor = mock_connect2.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [(1, 2, 3, 4, 0)]  # Mock the result of the SELECT query

        # Make the request to the endpoint
        response = self.app.get('/getLivraison')

        # Assert the response status code
        self.assertEqual(response.status_code, 201)

        # Add more assertions if needed


if __name__ == '__main__':
    unittest.main()
