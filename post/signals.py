from post.models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Post)
def create_event_game(sender, instance, created, **kwargs):
    if created:
        pass

@receiver(post_save, sender=Post)
def save_event_game(sender, instance, **kwargs):
    if instance.is_approved:
        # user = instance.user
        # challenge = instance.challenge
        # challenges = challenge.game.games.all()
        # initial_submission = True
        # for chal in challenges:
        #     if initial_submission:
        #         if Post.objects.filter(user=user, challenge=chal, text__isnull=False, submit_challenge__isnull=True, is_approved=True ).exists():
        #             print("Is Available: ", chal)
        #         else:
        #             initial_submission = False
        #             print("Not Available: ", chal)
        # if initial_submission:
        #     user.profile.credits += challenge.game.total_point
        #     user.profile.save()
        pass