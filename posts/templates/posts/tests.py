
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass123')

    def test_create_post(self):
        p = Post.objects.create(author=self.user, content='Hello world')
        self.assertEqual(str(p), f"Post {p.id} by tester")
        self.assertEqual(p.total_likes(), 0)
