import unittest
from app import app

class CoAPWebTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'User UI', response.data)

    def test_nodes_api(self):
        response = self.app.get('/api/nodes')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertTrue(any('ipv6' in node for node in data))

    def test_user_nodes_api(self):
        # Add a node
        node = {"ipv6": "fd12:3456::eae:5fff:fe6d:4eca", "type": "LED"}
        response = self.app.post('/api/user_nodes', json=node)
        self.assertEqual(response.status_code, 200)
        # Get user nodes
        response = self.app.get('/api/user_nodes')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn(node, data)

    def test_led_control_api(self):
        # Test invalid action
        response = self.app.post('/api/led/fd12:3456::eae:5fff:fe6d:4eca/invalid')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'error')

if __name__ == '__main__':
    unittest.main()
