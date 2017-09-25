from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import UserProfile


class UserProfileCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)

    class Meta:
        model = UserProfile
        fields = ("email",)


class UserProfileChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(UserProfileChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = UserProfile
        fields = ("email",)
