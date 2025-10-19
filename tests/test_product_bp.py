import unittest
from app import app 

class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування тестового клієнта."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_list_page(self):
        """Тест сторінки /products/ (зі списком товарів)."""
        
        response = self.client.get("/products/")         
        response_data = response.data.decode('utf-8')
        
        self.assertEqual(response.status_code, 200)
        
        self.assertIn("Наші товари", response_data) 
        
        self.assertIn("Ноутбук", response_data) 
        self.assertIn("1500", response_data)
        self.assertIn("Миша", response_data)

if __name__ == "__main__":
    unittest.main()