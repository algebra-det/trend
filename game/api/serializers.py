from account.models import MyUser
from core import models
from game.models import Game, Challenge, EventGame, Promotion, challenge_directory_path
from core.models import ReceivedPoint, UserGame, SubmitChallenge
from post.models import Post

from reward.api.serializers import TrophySerializer, MagicBoxSerializer

from rest_framework import serializers

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        exclude = ['game', 'created_at', 'updated_at']


class GameSerializer(serializers.ModelSerializer):
    difficulty = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Game
        exclude = ['created_at', 'updated_at', 'min_players', 'joined_players']
    
    def get_images(self, game):
        images = []
        if game.image:
            images.append({"image":"{}".format(game.image.url)})
        if game.image1:
            images.append({"image":"{}".format(game.image1.url)})
        if game.image2:
            images.append({"image":"{}".format(game.image2.url)})
        if game.image3:
            images.append({"image":"{}".format(game.image3.url)})
        return images
    
    def get_difficulty(self, game):
        if game.difficulty == 'easy':
            return 'Facile'
        elif game.difficulty == 'medium':
            return 'Media'
        else:
            return 'Difficile'


class ChallengeSerializer(serializers.ModelSerializer):
    get_images = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        exclude = ['created_at', 'updated_at', 'image', 'image1', 'image2', 'image3']

    def get_images(self, challenge):
        images = []
        if challenge.image:
            images.append({"image":"{}".format(challenge.image.url)})
        if challenge.image1:
            images.append({"image":"{}".format(challenge.image1.url)})
        if challenge.image2:
            images.append({"image":"{}".format(challenge.image2.url)})
        if challenge.image3:
            images.append({"image":"{}".format(challenge.image3.url)})
        return images
        # Depth will elaborate the 'game' fields in this challenges model
        # depth = 1


class UserChallengeSerializer(serializers.ModelSerializer):
    game_title = serializers.SerializerMethodField()
    points_earned = serializers.SerializerMethodField()
    challenge_id = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ('challenge_id', 'title', 'image', 'game', 'game_title', 'points_earned', 'images')
    
    def get_challenge_id(self, challenge):
        return challenge.id

    def get_game_title(self, challenge):
        return challenge.game.title
    
    def get_points_earned(self, challenge):
        if challenge.trophy:
            return challenge.trophy.points
        elif challenge.magic_box:
            return challenge.magic_box.points
        return 0


    def get_images(self, challenge):
        images = []
        if challenge.image:
            images.append({"image":"{}".format(challenge.image.url)})
        if challenge.image1:
            images.append({"image":"{}".format(challenge.image1.url)})
        if challenge.image2:
            images.append({"image":"{}".format(challenge.image2.url)})
        if challenge.image3:
            images.append({"image":"{}".format(challenge.image3.url)})
        return images

# class GameChallengeSerializer(serializers.ModelSerializer):
#     challenge_complete_status = serializers.SerializerMethodField()
#     post_status = serializers.SerializerMethodField()
#     review_status = serializers.SerializerMethodField()
#     trophy = serializers.SerializerMethodField()
#     magic_box = serializers.SerializerMethodField()

#     class Meta:
#         model = Challenge
#         exclude = ['created_at', 'updated_at', 'image1', 'image2', 'image3', 'game']
    
#     def get_challenge_complete_status(self, challenge):
#         user = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             user = request.user
#         if user and not user.is_anonymous:
#             submit_challenge = SubmitChallenge.objects.filter(user=user, challenge=challenge, game=challenge.game)
#             if submit_challenge:
#                 return True
#             else:
#                 print('not available')
#                 return False
#         else:
#             print('Never went through')
#             return False
    
#     def get_post_status(self, challenge):
#         user = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             user = request.user
#         if user and not user.is_anonymous:
#             submit_challenge = SubmitChallenge.objects.filter(user=user, challenge=challenge, game=challenge.game)
#             if submit_challenge:
#                 post = Post.objects.filter(user=user, challenge=submit_challenge.first())
#                 if post:
#                     return True
#                 else:
#                     return False
#             else:
#                 return False
#         else:
#             return False
    
#     def get_review_status(self, challenge):
#         user = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             user = request.user
#         if user and not user.is_anonymous:
#             submit_challenge = SubmitChallenge.objects.filter(user=user, challenge=challenge, game=challenge.game)
#             if submit_challenge:
#                 post = Post.objects.filter(user=user, challenge=submit_challenge.first())
#                 if post:
#                     if post.first().text:
#                         return True
#                     else:
#                         return False
#                 else:
#                     return False
#             else:
#                 return False
#         else:
#             return False
    
#     def get_trophy(self, challenge):
#         trophy = challenge.trophy
#         if trophy:
#             return True
#         return False
    
#     def get_magic_box(self, challenge):
#         magic_box = challenge.magic_box
#         if magic_box:
#             return True
#         return False


class GameChallengeSerializer(serializers.ModelSerializer):
    challenge_complete_status = serializers.SerializerMethodField()
    submission_status = serializers.SerializerMethodField()
    post_status = serializers.SerializerMethodField()
    trophy = serializers.SerializerMethodField()
    magic_box = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    trophy_points = serializers.SerializerMethodField()
    magic_box_points = serializers.SerializerMethodField()
    game = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        exclude = ['created_at', 'updated_at', 'image1', 'image2', 'image3']
    
    def get_game(self, challenge):
        game = challenge.game
        response = {
            'id': game.id,
            'title': str(game.title),
            'image': game.image.url
        }
        return response

    def get_images(self, challenge):
        images = []
        if challenge.image:
            images.append({"image":"{}".format(challenge.image.url)})
        if challenge.image1:
            images.append({"image":"{}".format(challenge.image1.url)})
        if challenge.image2:
            images.append({"image":"{}".format(challenge.image2.url)})
        if challenge.image3:
            images.append({"image":"{}".format(challenge.image3.url)})
        return images
    
    def get_challenge_complete_status(self, challenge):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user and not user.is_anonymous:
            post = Post.objects.filter(user=user, challenge=challenge, text__isnull=False)
            if post:
                return True
            else:
                print('not available')
                return False
        else:
            print('Never went through')
            return False

    def get_submission_status(self, challenge):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user and not user.is_anonymous:
            if challenge.trophy:
                if SubmitChallenge.objects.filter(user=user, challenge=challenge).exists():
                    return True
                else:
                    return False
            else:
                print('not available')
                return False
        else:
            print('Never went through')
            return False

    def get_post_status(self, challenge):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user and not user.is_anonymous:
            if challenge.trophy:
                submit_challenge = SubmitChallenge.objects.filter(user=user, challenge=challenge)
                if submit_challenge.exists():
                    if Post.objects.filter(user=user, challenge=challenge, submit_challenge=submit_challenge.first()).exists():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                print('not available')
                return False
        else:
            print('Never went through')
            return False
    
    def get_trophy(self, challenge):
        trophy = challenge.trophy
        if trophy:
            return True
        return False
    
    def get_magic_box(self, challenge):
        magic_box = challenge.magic_box
        if magic_box:
            return True
        return False
    
    def get_trophy_points(self, challenge):
        trophy = challenge.trophy
        if trophy:
            return trophy.points
        return False
    
    def get_magic_box_points(self, challenge):
        magic_box = challenge.magic_box
        if magic_box:
            return magic_box.points
        return False

    def get_distance(self, challenge):
        return ''


# class GameDetailSerializer(serializers.ModelSerializer):
#     challenges = GameChallengeSerializer(many=True, read_only=True)

#     class Meta:
#         model = Game
#         exclude = ['created_at', 'updated_at', 'image', 'image1', 'image2', 'image3', 'min_players']

class ParticipantSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'image')
    
    def get_image(self, user):
        return user.profile.image.url

class GameDetailSerializer(serializers.ModelSerializer):
    challenges = serializers.SerializerMethodField()
    promotions = serializers.SerializerMethodField()
    difficulty = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    

    class Meta:
        model = Game
        exclude = ['created_at', 'updated_at', 'image', 'image1', 'image2', 'image3', 'min_players', 'joined_players']
    
    def get_participants(self, game):
        data = ReceivedPoint.objects.filter(challenge__game=game).select_related('user')
        participants_id = []
        for i in data:
            participants_id.append(i.user.id)
        users = MyUser.objects.filter(id__in=participants_id)
        serializer = ParticipantSerializer(users, many=True)
        return serializer.data
    
    def get_images(self, game):
        images = []
        if game.image:
            images.append({"image":"{}".format(game.image.url)})
        if game.image1:
            images.append({"image":"{}".format(game.image1.url)})
        if game.image2:
            images.append({"image":"{}".format(game.image2.url)})
        if game.image3:
            images.append({"image":"{}".format(game.image3.url)})
        return images

    def get_challenges(self, game):
        request = self.context.get("request")
        challenges = Challenge.objects.filter(game=game, status=True)
        serializer = GameChallengeSerializer(challenges, context={ 'request': request}, many=True)
        return serializer.data
    
    def get_promotions(self, game):
        promotions = Promotion.objects.filter(game=game)
        if len(promotions) == 1:
            return []
        serializer = PromotionSerializer(promotions, many=True)
        return serializer.data

    def get_difficulty(self, game):
        if game.difficulty == 'easy':
            return 'Facile'
        elif game.difficulty == 'medium':
            return 'Media'
        else:
            return 'Difficile'



class EventGameSerializer(serializers.ModelSerializer):
    challenges = serializers.SerializerMethodField()
    game_id = serializers.SerializerMethodField('get_game_id')
    game = serializers.SerializerMethodField('get_game')
    location = serializers.SerializerMethodField('get_location')
    participants_required = serializers.SerializerMethodField('get_participants_required')
    participants_missing = serializers.SerializerMethodField('get_participants_missing')

    class Meta:
        model = EventGame
        fields = ['game_id', 'game', 'location', 'participants_required', 'participants_missing']

    def get_challenges(self, game):
        request = self.context.get("request")
        challenges = Challenge.objects.filter(game=game, status=True)
        serializer = GameChallengeSerializer(challenges, context={ 'request': request}, many=True)
        return serializer.data

    def get_game_id(self, event):
        return event.game.id
    
    def get_game(self, event):
        return event.game.title
    
    def get_location(self, event):
        return event.game.location_name

    def get_participants_required(self, event):
        return event.game.min_players

    def get_participants_missing(self, event):
        return int(event.game.min_players - event.num_players)

class SubmitChallengeSerializer(serializers.ModelSerializer):
    challenge_id = serializers.SerializerMethodField('get_challenge_id')

    class Meta:
        model = SubmitChallenge
        fields = ['user', 'game', 'challenge_id', 'challenge', 'image', 'points']
        read_only_fields = ['challenge_id',]
    
    def get_challenge_id(self, submitchallenge):
        return int(submitchallenge.challenge.id)

class CompletedToursSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'title', 'image', 'category', 'total_point')