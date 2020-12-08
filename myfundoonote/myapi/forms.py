from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Creating class for creating model forms by inheriting UserCreatingForm
    UserCreationForm by default consists of username, password and confirm password
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",) #since UserCreationForm does not inlcude email, we have to add it.