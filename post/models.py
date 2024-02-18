from django.db import models
from account.models import MyUser
from game.models import Game, Challenge
from core.models import Challenge, SubmitChallenge

from django.utils import timezone

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'posts/user_{0}/{1}/social/{2}'.format(instance.user.id, instance.challenge.id, filename)

REWARD_CHOICES = (
    ('social', 'social'),
    ('object', 'object')
)

class Post(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    submit_challenge = models.ForeignKey(SubmitChallenge, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=100, null=True, blank=True)
    liked = models.ManyToManyField(MyUser, default=None, blank=True, related_name='liked')
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    type_of_reward = models.CharField(max_length=50, choices=REWARD_CHOICES)

    @property
    def date(self):
        return self.created_date.strftime('%Y-%m-%d')

    def approve(self):
        self.is_approved = True
        self.save()

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    # @property
    # def image(self):
    #     if not self.submit_challenge:
    #         return self.image.url
    #     return self.submit_challenge.image.url

    @property
    def commented(self):
        return self.comments.all().count()

    @property
    def comments(self):
        return self.comments.all()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text



class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post)
