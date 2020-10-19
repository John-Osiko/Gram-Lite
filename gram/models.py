from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# class SavedEmbeds(models.Model):
#     type = models.CharField(max_length=15)
#     provider_url = models.URLField()
#     provider_name = models.CharField(max_length=100)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     html = models.TextField()
#     width = models.IntegerField()
#     height = models.IntegerField()
#     thumbnail_url = models.URLField()
#     thumbnail_width = models.IntegerField()
#     thumbnail_height = models.IntegerField()
#     author_url = models.URLField()
#     author_name = models.CharField(max_length=100)
#     version = models.DecimalField(max_digits=4, decimal_places=2)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    bio = models.TextField(max_length=500, default="My Bio", blank=True)
    name = models.CharField(blank=True, max_length=120)
    location = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()


class Image(models.Model):
    image = models.ImageField(upload_to='posts/')
    name = models.CharField(max_length=250, blank=True)
    caption = models.CharField(max_length=250, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    p_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self):
        return f"/post/{self.id}"

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.user.name} Image'



class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    p_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user.name} Image'

    class Meta:
        ordering = ["-pk"]



class Follow(models.Model):
    followers = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'