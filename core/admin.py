from django.contrib import admin
from .models import Profile, UserGame, UserChallenge, Reward, SubmitChallenge, ReceivedPoint, Privacy, Conditions, Credits

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'credits']
    search_fields = ['email', 'credits']

@admin.register(UserGame)
class UserGameAdmin(admin.ModelAdmin):
    list_display = ['profile', 'profile_user_id', 'games']

@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ['profile', 'challenge', 'image']

@admin.register(SubmitChallenge)
class SubmitChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'challenge', 'image']

@admin.register(ReceivedPoint)
class ReceivedPointAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'challenge', 'received_for']


@admin.register(Privacy)
class PrivacyAdmin(admin.ModelAdmin):
    list_display = ['text', 'created_at', 'updated_at']


@admin.register(Conditions)
class ConditionsAdmin(admin.ModelAdmin):
    list_display = ['text', 'created_at', 'updated_at']


@admin.register(Credits)
class CreditsAdmin(admin.ModelAdmin):
    list_display = ['text', 'created_at', 'updated_at']