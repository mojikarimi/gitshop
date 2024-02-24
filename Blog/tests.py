from django.test import TestCase
from .models import Category


# Create your tests here.
class CategoryBlogTest(TestCase):
    databases = ['blog']

    def setUp(self):
        category = Category.objects.create(title='magazine')
        return category

    def test_category_blog(self):
        cat = self.setUp()
        category = Category.objects.get(pk=cat.pk)
        self.assertEqual(category.title, 'magazine')
