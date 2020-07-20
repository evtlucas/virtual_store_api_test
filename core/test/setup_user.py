from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token


class SetupUser:

    @staticmethod
    def get_token():
        User = get_user_model()
        user = User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
        token = Token.objects.create(user=user)
        token.save()
        return token