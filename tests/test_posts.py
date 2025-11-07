import unittest
from app import create_app, db
from app.posts.models import Post, PostCategory

class PostTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        """
        Тест US01: Створення нового поста.
        """
        response = self.client.post('/post/create', data={
            'title': 'My first test post',
            'content': 'This is TDD!', 
            'category': 'tech',
            'publish_date': '2025-11-04T12:00'
        }, follow_redirects=True)
        response_data = response.data.decode('utf-8')

        self.assertEqual(response.status_code, 200, "Сторінка не повернула 'OK' (200)")
        self.assertIn('Post added successfully', response_data, "Flash-повідомлення не знайдено")

        post = db.session.scalar(db.select(Post).filter_by(title="My first test post"))
        self.assertIsNotNone(post, "Пост не було створено в БД")
        self.assertEqual(post.content, "This is TDD!")
        self.assertEqual(post.category, PostCategory.tech)


    def test_list_posts(self):
        """
        Тест US02: Перегляд списку всіх постів.
        """
        post1 = Post(title="Перший Пост", content="Вміст 1", category=PostCategory.news)
        post2 = Post(title="Другий Пост", content="Вміст 2", category=PostCategory.tech)
        db.session.add_all([post1, post2])
        db.session.commit()

        response = self.client.get('/post/')
        response_data = response.data.decode('utf-8') 

        self.assertEqual(response.status_code, 200)
        self.assertIn("Перший Пост", response_data) 
        self.assertIn("Другий Пост", response_data) 

    def test_view_post_detail(self):
        """
        Тест US03: Перегляд деталей одного поста.
        """
        post = Post(title="Детальний Пост", content="Повний детальний вміст", category=PostCategory.publication)
        db.session.add(post)
        db.session.commit()
        
        self.assertIsNotNone(post.id)
        
        response = self.client.get(f'/post/{post.id}')
        response_data = response.data.decode('utf-8') 

        self.assertEqual(response.status_code, 200)
        self.assertIn("Детальний Пост", response_data) 
        self.assertIn("Повний детальний вміст", response_data) 
    def test_update_post(self):
        """
        Тест US04: Редагування існуючого поста.
        """
        post = Post(title="Старий Заголовок", content="Старий вміст", category=PostCategory.news)
        db.session.add(post)
        db.session.commit()

        response = self.client.post(f'/post/{post.id}/update', data={
            'title': 'Новий Оновлений Заголовок',
            'content': 'Новий оновлений вміст',
            'category': 'tech', 
            'publish_date': post.posted.strftime("%Y-%m-%dT%H:%M") 
        }, follow_redirects=True)
        response_data = response.data.decode('utf-8') 
        self.assertEqual(response.status_code, 200)
        self.assertIn("Пост оновлено!", response_data) 

        updated_post = db.get_or_404(Post, post.id)
        self.assertEqual(updated_post.title, "Новий Оновлений Заголовок")
        self.assertEqual(updated_post.category, PostCategory.tech)

    def test_delete_post(self):
        """
        Тест US05: Видалення існуючого поста.
        """
        post = Post(title="Пост для Видалення", content="...", category=PostCategory.other)
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