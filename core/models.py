from django.db import models

from account.models import MyUser
from game.models import Game, Challenge

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploads/profile/user_{0}/dp/{1}'.format(instance.user.id, filename)

def user_directory_game_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploads/profile/user_{0}/{1}/{2}'.format(instance.user.id, instance.challenge.title, filename)

class MyModel(models.Model):
    upload = models.FileField(upload_to=user_directory_path)

class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path, default='uploads/profile/default.jpeg')
    following = models.ManyToManyField(MyUser, default=None, blank=True, related_name='following')
    credits = models.IntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    @property
    def posts(self):
        return self.user.post_set.filter(is_approved=True)[:4]

    @property
    def posted(self):
        return self.user.post_set.filter(is_approved=True).count()

    def email(self):
        return self.user.email

class UserGame(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='usergame')
    game_tours = models.ManyToManyField(Game, default=None, blank=True, related_name='game_tours')
    challenges = models.ManyToManyField(Challenge, default=None, blank=True, related_name='challenges')

    def __str__(self):
        return str(self.profile)

    @property
    def profile_user_id(self):
        return self.profile.user.id

    @property
    def games(self):
        return self.game_tours.all().count()

class UserChallenge(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_game_path)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.profile, self.challenge)

class Reward(models.Model):
    welcome = models.IntegerField()
    per_post = models.IntegerField()

    def __str__(self):
        return 'Welcome Reward {} & Per Post Reward {}'.format(int(self.welcome), int(self.per_post))


class SubmitChallenge(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='submitchallenges')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_game_path)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField()

    def __str__(self):
        return '{} for {} in {} challenge'.format(self.user, self.game, self.challenge)
    
    @property
    def username(self):
        return str(self.user.first_name, self.user.last_name)


RECEIVED_CHOICES = (
    ('content', 'content'),
    ('submission', 'submission')
)

class ReceivedPoint(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='points_received')
    points = models.IntegerField()
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    received_for = models.CharField(max_length=20, choices=RECEIVED_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.user, self.points)

    def save(self, *args, **kwargs):
        self.game = self.challenge.game
        return super(ReceivedPoint, self).save(*args, **kwargs)


class Privacy(models.Model):
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Privacy'
        verbose_name_plural = 'Privacy'

    def __str__(self):
        return '{}...'.format(self.text[:20])


class Conditions(models.Model):
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Conditions'
        verbose_name_plural = 'Conditions'

    def __str__(self):
        return '{}...'.format(self.text[:20])


class Credits(models.Model):
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Credits'
        verbose_name_plural = 'Credits'

    def __str__(self):
        return '{}...'.format(self.text[:20])