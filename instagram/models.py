from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    profile_picture = models.ImageField(upload_to='pictures/')
    bio = models.TextField(default="My Bio", blank=True)
    name = models.CharField(max_length=120,blank=True)

    
   
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()


    def __str__(self):
        return f'{self.user.username} Profile'
class Post(models.Model):
    name = models.CharField(max_length=300,blank=True)
    image =  models.ImageField(upload_to = 'album/')
    caption = models.TextField()
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(User, related_name='likes',blank=True)
    posted = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def save_image(self):
        self.save()
    def delete_image(self):
        self.delete()
    @property
    def all_comments(self):
        return self.comments.all()

    @classmethod
    def update_caption(cls,id,caption):
        cls.objects.filter(id=id).update(caption=caption)
    
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.name} Post'
    
    class Meta:
        ordering =['-pk']



class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        ordering = ["-pk"]


class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'
