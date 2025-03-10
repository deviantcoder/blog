from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('username')

        if (username is None) or (password is None):
            return None
        
        try:
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)

            if user.check_password(password):
                return user
        except User.DoesNotExist:
            User().set_password(password)
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None