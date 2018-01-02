from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget 
from registration.forms import RegistrationFormUniqueEmail
from .models import Post, UserProfile, UserLikePost
from registration.users import UsernameField

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'ck_content', 'tags')

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


class UserProfileRegistrationForm(RegistrationFormUniqueEmail):
    # field = forms.CharField(max_length=10)
    firstname_field = forms.CharField(max_length=50)
    lastname_field = forms.CharField(max_length=50)
    intro = forms.CharField(max_length=255)
    photo_url = forms.URLField()
    location = forms.CharField(max_length=255)

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileRegistrationForm


class UserLikePostForm(forms.ModelForm):
    class Meta:
        model = UserLikePost
        fields = '__all__'

class UserLikePostAdmin(admin.ModelAdmin):
    form = UserLikePostForm

admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile)
admin.site.register(UserLikePost, UserLikePostAdmin)