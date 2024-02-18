from django import forms
from core.models import SubmitChallenge, Reward, Privacy, Conditions, Credits

from django.contrib.auth.views import PasswordResetForm

from account.models import MyUser as UserModel

import unicodedata
def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()

class SubmitChallengeForm(forms.ModelForm):
    class Meta:
        model = SubmitChallenge
        fields = ['image']

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['welcome']

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and u.is_admin and
            _unicode_ci_compare(email, getattr(u, email_field_name))
        )

class PrivacyForm(forms.ModelForm):
    class Meta:
        model = Privacy
        fields = ['text',]


class ConditionsForm(forms.ModelForm):
    class Meta:
        model = Conditions
        fields = ['text',]


class CreditsForm(forms.ModelForm):
    class Meta:
        model = Credits
        fields = ['text',]