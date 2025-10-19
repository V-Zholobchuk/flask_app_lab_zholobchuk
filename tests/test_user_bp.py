import unittest
from app import app 
class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування тестового клієнта перед кожним тестом."""
        app.config["TESTING"] = True 
        self.client = app.test_client() 

    def tearDown(self):
        """Виконується після кожного тесту (тут нічого не робимо)."""
        pass

    def test_greetings_page(self):
        """Тест маршруту /hi/<name>."""
        response = self.client.get("/hi/John?age=30") [cite: 186]

        self.assertEqual(response.status_code, 200) [cite: 187]
        self.assertIn(b"JOHN", response.data) [cite: 188]
        self.assertIn(b"30", response.data) [cite: 189]

    def test_admin_page(self):
        """Тест маршруту /admin, який перенаправляє."""
        response = self.client.get("/admin", follow_redirects=True) [cite: 191]

        self.assertEqual(response.status_code, 200) [cite: 192]
        self.assertIn(b"ADMINISTRATOR", response.data) [cite: 193]
        self.assertIn(b"45", response.data) [cite: 193]

if __name__ == "__main__":
    unittest.main()