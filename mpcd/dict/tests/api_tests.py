import json

from django.contrib.auth import get_user_model
from django.http import response

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, HeaderDict

from rest_framework.test import APIRequestFactory

from mpcd.dict.models import (
    Category,
    Definition,
    Dictionary,
    Entry,
    LoanWord,
    Reference,
    Translation,
    Word,
)

class UserAuthenticationTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('test_user','test_password',is_superuser=True)
        Dictionary.objects.create(slug='test')
        self.token = Token.objects.create(user=self.user)

    def test_check_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('api:user-me'))
        self.assertEqual(response.status_code,200)
        json_response = response.json()
        self.assertEqual(json_response['username'],'test_user')

    def test_create_entry(self):
        data = {
            "dict": {
                "slug": "test"
            },
            "lemma": {
                "word": "test",
                "language": "eng"
            },
            "loanwords": [
                {
                    "word": "testloan",
                    "language": "eng",
                    "translations": [
                        {
                            "language": "eng",
                            "meaning": "test"
                        }
                    ]
                }
            ],
            "translations": [
                {
                    "language": "eng",
                    "meaning": "test"
                },
            ],
            "definitions": [
                {
                    "definition": "test",
                    "language": "eng"
                }
            ],
            "categories": [
                {
                    "category": "econom"
                }
            ],
            "references": [
            ],
            "comment": ""
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse('api:entry-list'),data=data,format='json',)
        print(response.json())
        self.assertEqual(response.status_code,201)
        self.assertEqual()

