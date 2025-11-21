# -*- coding: utf-8 -*-
import unittest
from app import create_app, db
from app.users.models import User

class AuthTestCase(unittest.TestCase):
    
    def setUp(self):
        # Використовуємо конфігурацію для тестів (БД в пам'яті, CSRF вимкнено)
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register(self, username, email, password):
        """Допоміжна функція для реєстрації"""
        return self.client.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=password
        ), follow_redirects=True)

    def login(self, email, password):
        """Допоміжна функція для входу"""
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Допоміжна функція для виходу"""
        return self.client.get('/logout', follow_redirects=True)

    # --- ТЕСТИ ---

    def test_registration(self):
        """Тест реєстрації нового користувача"""
        response = self.register('testuser', 'test@test.com', 'password123')
        response_data = response.data.decode('utf-8')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Account created', response_data)
        
        # Перевіряємо, чи користувач з'явився в БД
        user = db.session.scalar(db.select(User).filter_by(username='testuser'))
        self.assertIsNotNone(user)

    def test_login_logout(self):
        """Тест входу та виходу"""
        # Спочатку реєструємо
        self.register('loginuser', 'login@test.com', 'password123')
        
        # 1. Вхід з правильними даними
        response = self.login('login@test.com', 'password123')
        response_data = response.data.decode('utf-8')
        self.assertIn('Ви успішно увійшли', response_data)
        
        # 2. Вихід
        response = self.logout()
        response_data = response.data.decode('utf-8')
        self.assertIn('Ви успішно вийшли', response_data) # Або 'You have been logged out' (як у вас написано)

        # 3. Вхід з неправильним паролем
        response = self.login('login@test.com', 'wrongpass')
        response_data = response.data.decode('utf-8')
        self.assertIn('Вхід не вдався', response_data)

if __name__ == '__main__':
    unittest.main()