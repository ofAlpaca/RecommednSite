from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from registration.users import UsernameField
# Create your models here.

TAG_CHOICE = (
    ('a', 'Asia'),
    ('a2', 'Animals'),
    ('b', 'Blacks'),
    ('c', 'Celebrity'),
    ('d', 'Dank'),
    ('f', 'Female'),
    ('g', 'Games'),
    ('h', 'Hitler'),
    ('i', 'Internet'),
    ('j', 'JoJoRef'),
    ('k', 'Kim Jong-un'),
    ('l', 'Lifehack'),
    ('m', 'Math'),
    ('n', 'Net Neutrality'),
    ('p', 'PC'),
    ('r', 'Religion'),
    ('r2', 'Russian'),
    ('s', 'Singer'),
    ('t', 'Taiwan'),
    ('u', 'USA'),
    ('v', 'Vehicle'),
    ('w', 'Welcom to HELL'),
    ('y', 'Yes/No'),
)

class Post(models.Model):
    title = models.CharField(max_length=120)
    ck_content = RichTextUploadingField('Content', default='')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    last_mod = models.DateTimeField()
    tags = MultiSelectField(choices=TAG_CHOICE, max_choices=4)

    def get_tags_as_list(self):
        ls = str(self.tags)
        return ls.split(',')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname_field = models.CharField(max_length=50)
    lastname_field = models.CharField(max_length=50)
    intro = models.TextField(max_length=255, blank=True)
    photo_url = models.URLField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    subs = models.ManyToManyField(User, blank=True, related_name='+' )
    subers = models.ManyToManyField(User, blank=True, related_name='+' )
    
class M_UserArticle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    readed_article = models.ManyToManyField(Post, blank=True, related_name='+' )

class UserLikePost(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)