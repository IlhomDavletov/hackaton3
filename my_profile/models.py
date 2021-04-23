from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save, post_delete

from account.models import MyUser
from tandyr_api import settings


class Profile(models.Model):
    GENDER = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )
    HOBBIES = (
        ('Sport', 'sport'),
        ('Movies', 'movies'),
        ('Books', 'books'),
        ('Programming', 'prog'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=120, blank=False)
    last_name = models.CharField(max_length=120, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    hobbies = models.CharField(max_length=20, choices=HOBBIES)

    # zip_code = models.CharField(max_length=5, validators=[MinLengthValidator(5)], blank=False)

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(create_profile, sender=MyUser)


def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except MyUser.DoesNotExist:
        pass
    else:
        instance.user.delete()
post_delete.connect(delete_user, sender=Profile)


class CodeImage(models.Model):
    image = models.ImageField(upload_to='images')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images')


class Review(models.Model):
    # problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='reviews')
    body = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
    class Meta:
        ordering = ('-created',)

class Like(models.Model):
    from_user = models.ForeignKey(MyUser, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(MyUser, related_name='to_user', on_delete=models.CASCADE)
    likes = models.BooleanField(default=False)

class Favourite(models.Model):
    user = models.ForeignKey(MyUser, related_name='user', on_delete=models.CASCADE)
    likes = models.ForeignKey(Like, related_name='like', on_delete=models.CASCADE)

# class Favorite(models.Model):
#     user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
#     favorite = models.BooleanField(default=False)