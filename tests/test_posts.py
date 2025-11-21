# -*- coding: utf-8 -*-
import unittest
from app import create_app, db
from app.posts.models import Post, PostCategory
from app.users.models import User # <-- Додаємо імпорт User

class PostTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # --- Створюємо тестового юзера ---
        self.user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(self.user)
        db.session.commit()
        self.user_id = self.user.id # Зберігаємо ID для тестів

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        """Тест US01: Створення нового поста."""
        response = self.client.post('/post/create', data={
            'title': 'My first test post',
            'content': 'This is TDD!',
            'category': 'tech',
            'publish_date': '2025-11-04T12:00',
            'author_id': self.user_id  # <-- ДОДАЄМО author_id
        }, follow_redirects=True)
        
        response_data = response.data.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Post added successfully', response_data)

        post = db.session.scalar(db.select(Post).filter_by(title="My first test post"))
        self.assertIsNotNone(post)
        self.assertEqual(post.content, "This is TDD!")
        # Перевіряємо, що пост прив'язався до юзера
        self.assertEqual(post.user_id, self.user_id) 

    def test_list_posts(self):
        """Тест US02: Перегляд списку всіх постів."""
        # Створюємо пости, прив'язані до нашого юзера
        post1 = Post(title="Перший Пост", content="Вміст 1", category=PostCategory.news, user=self.user)
        post2 = Post(title="Другий Пост", content="Вміст 2", category=PostCategory.tech, user=self.user)
        db.session.add_all([post1, post2])
        db.session.commit()

        response = self.client.get('/post/')
        response_data = response.data.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Перший Пост", response_data)
        self.assertIn("Другий Пост", response_data)

    def test_view_post_detail(self):
        """Тест US03: Перегляд деталей одного поста."""
        post = Post(title="Детальний Пост", content="Повний детальний вміст", category=PostCategory.publication, user=self.user)
        db.session.add(post)
        db.session.commit()
        
        response = self.client.get(f'/post/{post.id}')
        response_data = response.data.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Детальний Пост", response_data)

    def test_update_post(self):
        """Тест US04: Редагування існуючого поста."""
        post = Post(title="Старий Заголовок", content="Старий вміст", category=PostCategory.news, user=self.user)
        db.session.add(post)
        db.session.commit()

        response = self.client.post(f'/post/{post.id}/update', data={
            'title': 'Новий Оновлений Заголовок',
            'content': 'Новий оновлений вміст',
            'category': 'tech', 
            'publish_date': post.posted.strftime("%Y-%m-%dT%H:%M"),
            'author_id': self.user_id # <-- ДОДАЄМО author_id
        }, follow_redirects=True)
        
        response_data = response.data.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Пост оновлено!", response_data)

        updated_post = db.session.get(Post, post.id)
        self.assertEqual(updated_post.title, "Новий Оновлений Заголовок")

    def test_delete_post(self):
        """Тест US05: Видалення існуючого поста."""
        post = Post(title="Пост для Видалення", content="...", category=PostCategory.other, user=self.user)
        db.session.add(post)
        db.session.commit()
        
        post_id = post.id 

        response = self.client.post(f'/post/{post_id}/delete', follow_redirects=True)
        response_data = response.data.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Пост успішно видалено", response_data)

        deleted_post = db.session.get(Post, post_id)
        self.assertIsNone(deleted_post)

if __name__ == '__main__':
    unittest.main()