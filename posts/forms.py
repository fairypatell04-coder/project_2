from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from accounts.models import Profile


# -------------------------
# Registration
# -------------------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

# -------------------------
# Edit Profile
# -------------------------
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'}),
                   'email': forms.EmailInput(attrs={'class':'form-control'})}

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
        widgets = {'bio': forms.Textarea(attrs={'class':'form-control', 'rows':3})}

# -------------------------
# Post Form
# -------------------------
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {'content': forms.Textarea(attrs={'class':'form-control','rows':3})}

# -------------------------
# Comment Form
# -------------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'class':'form-control','rows':3})}
