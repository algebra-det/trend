# from game.models import Game, EventGame
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# @receiver(post_save, sender=Game)
# def create_event_game(sender, instance, created, **kwargs):
#     if created:
#         if instance.category == 'Event':
#             EventGame.objects.create(game=instance)

# @receiver(post_save, sender=Game)
# def save_event_game(sender, instance, **kwargs):
#     instance.eventgame.save()