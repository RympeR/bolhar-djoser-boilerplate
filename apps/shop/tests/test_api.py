from rest_framework.test import APITestCase
from django.urls import reverse

from apps.shop.models import Category


class CategoryApiTestCase(APITestCase):

    def test_get(self):
        category = Category.objects.create(
            name='test',
            display=True,
        )
        url = reverse('categories-list')
        print(url)
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(category.pk, response.data['results'][0]['id'])
        