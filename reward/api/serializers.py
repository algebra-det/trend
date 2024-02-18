from rest_framework import serializers
from reward.models import Trophy, MagicBox

class TrophySerializer(serializers.ModelSerializer):
    class Meta:
        model = Trophy
        exclude = ['id', 'title', 'image']


class MagicBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagicBox
        exclude = ['id', 'title', 'image']