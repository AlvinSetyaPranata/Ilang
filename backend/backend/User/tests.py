from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post


user_model = get_user_model()

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        user = user_model.objects.create(
            username="alvinsetyapranata3",
            phone="6287850506951",
            bio="Hi there",
            image="https://hellowolr.com",
            email="hellowlrods@gmail.com"
        )

        user.save()


    def test_user_register(self):
        self.assertEquals(
            bool(user_model.objects.filter(username="alvinsetyapranata3")),
            True
        )

