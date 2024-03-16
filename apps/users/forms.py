from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1']
        exclude = ['password2',]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['password1'].help_text = None
    #     self.fields['password1'].label = 'Password'
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['password1'].help_text = None
        self.fields['password1'].label = 'Password'

    def save(self, commit=True):
        user = super().save(commit=False)
        # user.user = True
        if commit:
            user.save()
        return user
        


