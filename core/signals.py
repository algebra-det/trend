# from account.models import MyUser
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Profile

# @receiver(post_save, sender=MyUser)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance, credits=100)

# @receiver(post_save, sender=MyUser)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()