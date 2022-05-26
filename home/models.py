from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    body=models.CharField(max_length=300)
    slug=models.SlugField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created','body')

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('home:post',kwargs={'post_id':self.id,'post_slug':self.slug})
    def like_count(self):
        return self.post_like.count()

    def can_like(self,user):
        check_user=user.user_like.filter(post=self)
        if check_user.exists():
            return True
        else:
            return False


class Relation(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.from_user} is following {self.to_user}")


class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment_post')
    body=models.TextField(max_length=200)
    replay=models.ForeignKey('self',on_delete=models.CASCADE,related_name='replays',blank=True,null=True)
    is_replay=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.user.username}-{self.body}-{self.created}")


class PostLike(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_like')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_like')

    def __str__(self):
        return f"{self.user.username} liked {self.post.slug}"
