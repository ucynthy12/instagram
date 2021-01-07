from django.test import TestCase
from .models import Post,Profile,Comment,Follow
from django.contrib.auth.models import User
# Create your tests here.

class TestPost(TestCase):
    
    def setUp(self):
        self.profile = Profile(name='cynthia',user=User(username='ucynthy12'),bio='Mother of two')
        self.profile.save()
        
        self.post_test = Post(name='test',caption='this is a test',user=self.profile)

    def test_instance(self):
        self.assertTrue(isinstance(self.post_test,Post))
    
    def test_save_post(self):
        self.post_test.save_image()
        posts = Post.objects.all()
        self.assertTrue(len(posts)>0)
    def test_save_profile(self):
        self.profile_test.save()
        after = Profile.objects.all()
        self.assertTrue(len(after) > 0)

    def test_delete_image(self):
        self.image_test.delete_image()
        after = Profile.objects.all()
        self.assertTrue(len(after) < 1)


class TestProfile(TestCase):
    def setUp(self):
        self.user = User(username='cynthia')
        self.user.save()

        self.profile_test = Profile(id=1, name='image', profile_picture='default.jpg', bio='this is a test profile',user=self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile_test, Profile))

    def test_save_profile(self):
        self.profile_test.save_user_profile()
        after = Profile.objects.all()
        self.assertTrue(len(after) > 0)