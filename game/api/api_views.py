from .serializers import GameSerializer, ChallengeSerializer, GameDetailSerializer, EventGameSerializer, SubmitChallengeSerializer, GameChallengeSerializer
from game.models import Game, Challenge, EventGame
from core.models import Profile, SubmitChallenge, ReceivedPoint
from post.models import Post
from account.models import MyUser
from django.db.models import Q, Case, Count, When

from rest_framework.views import APIView
from rest_framework.response import Response

from trend.pagination import CustomPagination

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from trend.utils import get_districts_dict, get_districts_list

from rest_framework.decorators import api_view, permission_classes, authentication_classes

from django.db import connection

import datetime
today = datetime.datetime.now().date()

disctrits_dict = get_districts_dict()
districts = get_districts_list()

import json
"""

Query TO order by lat lon distance
Here :
23.686 is lat of user
90.3563 is lon of user

SELECT * FROM (
                    SELECT *,
                        (
                            (
                                (
                                    acos(
                                        sin(( 23.6850 * pi() / 180))
                                        *
                                        sin(( lat * pi() / 180)) + cos(( 23.6850 * pi() /180 ))
                                        *
                                        cos(( lat * pi() / 180)) * cos((( 90.3563 - lon) * pi()/180)))
                                ) * 180/pi()
                            ) * 60 * 1.1515 * 1.609344
                        )
                    as distance FROM game
                ) game
                WHERE distance <= 10000
                ORDER BY distance;
"""


def is_available(serializer_data):
    resultant_serializer = list()

    for game in serializer_data:
        data = game
        id = data['id']
        game = Game.objects.get(pk=id)
        if game.eventgame.num_players<game.min_players:
            data.update({"available": False})
        else:
            data.update({"available": True})
        resultant_serializer.append(data)
    
    return resultant_serializer


class GameClassicAPIView(APIView, CustomPagination):
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        sort = request.query_params.get('sort', None)
        difficulty = request.query_params.get('difficulty', None)
        difficulty_sort = request.query_params.get('difficulty_sorting', None)
        credit = request.query_params.get('credits', None)
        game_type = request.query_params.get('game_type', None)
        province = request.query_params.get('province')

        user = request.user
        # if not sort and not difficulty_sort and not user.is_anonymous and user.profile.latitude and not province:
        #     cursor = connection.cursor()
        #     cursor.execute("""SELECT id FROM (
        #                 SELECT *,
        #                     (
        #                         (
        #                             (
        #                                 acos(
        #                                     sin(( {0} * pi() / 180))
        #                                     *
        #                                     sin(( location_latitude * pi() / 180)) + cos(( {0} * pi() /180 ))
        #                                     *
        #                                     cos(( location_latitude * pi() / 180)) * cos((( {1} - location_longitude) * pi()/180)))
        #                             ) * 180/pi()
        #                         ) * 60 * 1.1515 * 1.609344
        #                     )
        #                 as distance FROM game_game
        #             ) game
        #             ORDER BY distance;""".format(user.profile.latitude, user.profile.longitude))
        #     rows = cursor.fetchall()
        #     games_ids = []
        #     for row in rows:
        #         games_ids.append(int(row[0]))
        #     print('games ids : ', games_ids)

        #     games = Game.objects.filter(id__in=games_ids)
        #     games = games.filter(status=True)
        #     print('games: ', games)
            # games = list(games)
            # games.sort(key=lambda game: games_ids.index(game.id))
        
        if province:
            if province not in districts:
                return Response({
                    "status": False,
                    "message": "Province should be from available options."
                })
            else:
                games = Game.objects.filter(Q(status=True) & Q(end_date__gt=today) & Q(province=province)).order_by('-created_at')

        elif not sort and not difficulty_sort and not user.is_anonymous and user.province:
            cursor = connection.cursor()
            cursor.execute("""SELECT id FROM (
                        SELECT *,
                            (
                                (
                                    (
                                        acos(
                                            sin(( {0} * pi() / 180))
                                            *
                                            sin(( location_latitude * pi() / 180)) + cos(( {0} * pi() /180 ))
                                            *
                                            cos(( location_latitude * pi() / 180)) * cos((( {1} - location_longitude) * pi()/180)))
                                    ) * 180/pi()
                                ) * 60 * 1.1515 * 1.609344
                            )
                        as distance FROM game_game
                    ) game
                    ORDER BY distance;""".format(disctrits_dict[user.province]['latitude'], disctrits_dict[user.province]['longitude']))
            rows = cursor.fetchall()
            games_ids = []
            for row in rows:
                games_ids.append(int(row[0]))
            print('games ids : ', games_ids)

            games = Game.objects.filter(Q(id__in=games_ids) & Q(end_date__gt=today) & Q(status=True))
            games = games.filter(status=True)
            print('games: ', games)
        elif not user.is_anonymous and province:
            if disctrits_dict[province]:
                cursor = connection.cursor()
                cursor.execute("""SELECT id FROM (
                            SELECT *,
                                (
                                    (
                                        (
                                            acos(
                                                sin(( {0} * pi() / 180))
                                                *
                                                sin(( location_latitude * pi() / 180)) + cos(( {0} * pi() /180 ))
                                                *
                                                cos(( location_latitude * pi() / 180)) * cos((( {1} - location_longitude) * pi()/180)))
                                        ) * 180/pi()
                                    ) * 60 * 1.1515 * 1.609344
                                )
                            as distance FROM game_game
                        ) game
                        ORDER BY distance;""".format(disctrits_dict[province]['latitude'], disctrits_dict[province]['longitude']))
                rows = cursor.fetchall()
                games_ids = []
                for row in rows:
                    games_ids.append(int(row[0]))
                print('games ids : ', games_ids)

                games = Game.objects.filter(Q(id__in=games_ids)  & Q(end_date__gt=today) & Q(status=True))
                games = games.filter(status=True)
                print('games: ', games)
                # games = list(games)
                # games.sort(key=lambda game: games_ids.index(game.id))
                preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(games_ids)])
                games = games.order_by(preserved)
            else:
                games = Game.objects.filter(Q(status=True) & Q(end_date__gt=today))
        else:
            games = Game.objects.filter(Q(status=True) & Q(end_date__gt=today))

        if game_type:
            if game_type == 'single':
                games = games.filter(category='Classic')
            elif game_type == 'group':
                games = games.filter(category='Event')

        if difficulty:
            if difficulty == 'easy':
                games = games.filter(difficulty='easy')

            elif difficulty == 'medium':
                games = games.filter(difficulty='medium')
            
            elif difficulty == 'hard':
                games = games.filter(difficulty='hard')

        if sort:
            if sort == 'latest':
                games = games.order_by('-created_at')
            else:
                games = games.order_by('created_at')

        # elif sort == 'lucrative':
        #     games = Game.objects.filter(Q(status=True)).order_by('-total_point')

        if credit:
            if credit == 'high':
                games = games.order_by('-total_point')
            else:
                games = games.order_by('total_point')


        if difficulty_sort:
            games_easy = games.filter(difficulty='easy')
            games_medium = games.filter(difficulty='medium')
            games_hard = games.filter(difficulty='hard')

            if difficulty_sort == 'high':
                games = []
                for game in games_hard:
                    games.append(game)
                for game in games_medium:
                    games.append(game)
                for game in games_easy:
                    games.append(game)
            else:
                games = []
                for game in games_easy:
                    games.append(game)
                for game in games_hard:
                    games.append(game)
                for game in games_medium:
                    games.append(game)


        if province:
            pass
        elif not sort and not difficulty_sort and not user.is_anonymous and user.profile.latitude:
            games = list(games)
            games.sort(key=lambda game: games_ids.index(game.id))
        
        elif not user.is_anonymous and province and disctrits_dict[province] and not difficulty_sort and not sort:
            print('Province is: ', province)
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(games_ids)])
            games = games.order_by(preserved)
                
        data = self.paginate_queryset(games, request, view=self)
        serializer = GameSerializer(data, many=True)
        return self.get_paginated_response(serializer.data)


class GameEventAPIView(APIView, CustomPagination):
    def get(self, request):
        sort = request.query_params.get('sort', None)
        if sort == 'new':
            games = Game.objects.filter(Q(category='Event') & Q(status=True)).order_by('-created_at')
        elif sort == 'easy':
            # games = Game.objects.filter(Q(category='Classic') & Q(status=True))
            # CASE_SQL = '(case when difficulty="easy" then 1 when difficulty="medium" then 2 when difficulty="hard" then 3 end)' 
            # games = Game.objects.filter(Q(category='Event') & Q(status=True)).extra(select={'difficulty_order': CASE_SQL}, order_by=['difficulty_order'])
            games = []
            games_easy = Game.objects.filter(Q(category='Event') & Q(status=True) & Q(difficulty='easy'))
            games_medium = Game.objects.filter(Q(category='Event') & Q(status=True) & Q(difficulty='medium'))
            games_hard = Game.objects.filter(Q(category='Event') & Q(status=True) & Q(difficulty='hard'))
            for game in games_easy:
                games.append(game)
            for game in games_medium:
                games.append(game)
            for game in games_hard:
                games.append(game)

        elif sort == 'lucrative':
            games = Game.objects.filter(Q(category='Event') & Q(status=True)).order_by('-total_point')
        else:
            games = Game.objects.filter(Q(category='Event') & Q(status=True))
        data = self.paginate_queryset(games, request, view=self)
        serializer = GameSerializer(data, many=True)
        resultant_serializer = list()
        resultant_serializer = is_available(serializer.data)
        return self.get_paginated_response(resultant_serializer)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def GameDetailAPIView(request):
    try:
        id = request.query_params.get('game_id')
        if id == '':
            return Response({"error": "Id parameter is required"})
        if not Game.objects.filter(pk=int(id)).exists():
            return Response({"Error": "No Game Found!"})
        game = Game.objects.get(pk=id)
        if not game.status:
                return Response({"error": "Game doesn't exist"})
    except Game.DoesNotExist:
        return Response({"error": "No Game Found!"}, status=404)

    if request.method == 'GET':

        if game.category == 'Event' and game.eventgame.num_players<game.min_players:
            event = EventGame.objects.get(game=game)
            serializer = EventGameSerializer(event)
            if MyUser.objects.filter(pk=request.user.id).exists():
                user = request.user
                user = MyUser.objects.get(pk=user.id)
                if user not in event.participants.all():
                    result = {"status": True, "available": False, "join": True}
                else:
                    result = {"status": True, "available": False, "join": False}
            else:
                result = {"status": True, "available": False, "join": False}
            result.update(serializer.data)
            return Response(result)

        else:
            serializer = GameDetailSerializer(game, context={ 'request': request})
            # images = []
            # if game.image:
            #     images.append({"image":"{}".format(game.image.url)})
            # if game.image1:
            #     images.append({"image":"{}".format(game.image1.url)})
            # if game.image2:
            #     images.append({"image":"{}".format(game.image2.url)})
            # if game.image3:
            #     images.append({"image":"{}".format(game.image3.url)})

            if request.user in game.joined_players.all():
                join = True
            else:
                join = False

            result = {}
            result.update(serializer.data)
            # result.update({"status": True, "available": True, "join": join, "images": images})
            result.update({"status": True, "available": True, "join": join})
            return Response(result)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def GameJoinAPIView(request):
    try:
        id = request.data.get('game_id', None)
        if id == '':
            return Response({"error": "Id parameter is required"})
        if not Game.objects.filter(pk=int(id)).exists():
            return Response({"Error": "No Game Found!"})
        game = Game.objects.get(pk=id)
        if not game.status:
                return Response({"error": "Game doesn't exist"})
    except Game.DoesNotExist:
        return Response({"error": "No Game Found!"}, status=404)

    if request.method == 'POST':

        if not request.user.is_anonymous:
            if request.user not in game.joined_players.all():
                game.joined_players.add(request.user)
                game.save()
                return Response({"status": True, "join": True})
            else:
                return Response({"status": False, "msg": "Already Joined"})
        return Response({"status": False, "msg": "Authentication Required!"})

"""
class ChallengeDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        try:
            user = request.user
            id = request.query_params.get('challenge_id')
            challenge = Challenge.objects.get(pk=id)
            if not challenge.status:
                return Response({"error": "Challenge doesn't exist"})
        except Challenge.DoesNotExist:
            return Response({"error": "No Challenge Found!"}, status=404)

        if challenge.game.category == 'Event' and challenge.game.eventgame.num_players<challenge.game.min_players:
            return Response({"error": "Challenge isn't available!"})

        serializer = ChallengeSerializer(challenge)
        images = []
        if challenge.image:
            images.append({"image":"{}".format(challenge.image.url)})
        if challenge.image1:
            images.append({"image":"{}".format(challenge.image1.url)})
        if challenge.image2:
            images.append({"image":"{}".format(challenge.image2.url)})
        if challenge.image3:
            images.append({"image":"{}".format(challenge.image3.url)})

        if SubmitChallenge.objects.filter(user=user, challenge=challenge, game=challenge.game).exists():
            submit_challenge = SubmitChallenge.objects.get(user=user, challenge=challenge, game=challenge.game)
            challenge_complete_status = True
            if Post.objects.filter(user=user, challenge=submit_challenge).exists():
                post = Post.objects.get(user=user, challenge=submit_challenge)
                post_status = True
                if post.text == '':
                    review_status = False
                else:
                    review_status = True
            else:
                post_status = False
                review_status = False
        else:
            post_status = False
            challenge_complete_status = False
            review_status = False

        result = {"status": True, "images": images, "challenge_complete_status": challenge_complete_status, 'post_status': post_status, 'review_status': review_status}
        result.update(serializer.data)
        return Response(result, status=200)
"""


class ChallengeDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        try:
            user = request.user
            id = request.query_params.get('challenge_id')
            challenge = Challenge.objects.get(pk=id)
            if not challenge.status:
                return Response({"error": "Challenge doesn't exist"})
        except Challenge.DoesNotExist:
            return Response({"error": "No Challenge Found!"}, status=404)

        if challenge.game.category == 'Event' and challenge.game.eventgame.num_players<challenge.game.min_players:
            return Response({"error": "Challenge isn't available!"})

        serializer = GameChallengeSerializer(challenge, context={ 'request': request})
        # images = []
        # if challenge.image:
        #     images.append({"image":"{}".format(challenge.image.url)})
        # if challenge.image1:
        #     images.append({"image":"{}".format(challenge.image1.url)})
        # if challenge.image2:
        #     images.append({"image":"{}".format(challenge.image2.url)})
        # if challenge.image3:
        #     images.append({"image":"{}".format(challenge.image3.url)})

        # result = {"status": True, "images": images}
        result = {"status": True}
        result.update(serializer.data)
        return Response(result, status=200)


class JoinEventAPIView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        try:
            id = request.data.get('game_id')
            game = Game.objects.get(pk=id)
            if game.category != 'Event':
                return Response({"error": "Cannot Join This Game"})
        except Game.DoesNotExist:
            return Response({"error": "Game does not exist"})

        if request.method == 'POST':
            event = EventGame.objects.get(game=game)
            if request.user not in event.participants.all():
                event.participants.add(request.user)
                event.num_players += 1
                event.save()
            else:
                event.participants.remove(request.user)
                event.num_players -= 1
                event.save()
            serializer = EventGameSerializer(event)
            if request.user not in event.participants.all():
                if game.eventgame.num_players>=game.min_players:
                    result = {"status": True, "available": True, "join": True}
                else:
                    result = {"status": True, "available": False, "join": True}
            else:
                if game.eventgame.num_players>=game.min_players:
                    result = {"status": True, "available": True, "join": False}
                else:
                    result = {"status": True, "available": False, "join": False}
            result.update(serializer.data)
            return Response(result)


from django.http import JsonResponse

from .object_detection import get_image_detection


class SubmitChallengeAPIView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        try:
            try:
                image_init = request.FILES.get('image', None)
                if not image_init:
                    return Response({"status": False, "error": "field is necessary!"})
                challenge_id = int(request.data.get('challenge_id'))
                challenge = Challenge.objects.get(pk=challenge_id)
                game = challenge.game
                if not challenge.status or not game.status:
                    return Response({"status": False, "error": "Challenge Not Available!"})

                if not challenge.trophy:
                    return Response({"status": False, "error": "this challenge does not have any submission task!"})
                
                if not challenge.object_type:
                    return Response({"status": False, "error": "this challenge does not have any submission task!"})
                
                if SubmitChallenge.objects.filter(user=user, challenge=challenge, game=game).exists():
                    return Response({"status": False, "response": False, "msg": "Già inviato!", "error": "Già inviato!"})

            except Challenge.DoesNotExist:
                return Response({"status": False, "error": "La sfida non esiste!", "msg": "La sfida non esiste!"})

            args = {
                "image": request.FILES['image'].read(),
                # "image": request.data.get('image'),
                "class": str(challenge.object_type)
            }
        except Exception:
            args = {}

        try:
            print(args)
            image, class_to_detect = args["image"], args["class"]
        except KeyError:
            return JsonResponse({"status": False, "response": None, "image": None, "error": "Parametri errati", "msg": "Parametri errati"})

        detections, image = get_image_detection(image, class_to_detect=class_to_detect)
        # detections = ''

        if detections is False:
            return JsonResponse({"status": False, "response": None, "image": None, "error": "Immagine non nel formato corretto", "msg": "Immagine non nel formato corretto"})

        if len(detections) > 0:

            submit_challenge = SubmitChallenge.objects.create(user=request.user, challenge=challenge, game=challenge.game, points=challenge.trophy.points, image=image_init)
            # serializer = SubmitChallengeSerializer(submit_challenge, data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()

            # challenges = game.games.all()
            # initial_submission = True
            # for chal in challenges:
            #     if initial_submission:
            #         if SubmitChallenge.objects.filter(user=user, challenge=chal, game=game, points=chal.points).exists():
            #             print("Is Available: ", chal)
            #         else:
            #             initial_submission = False
            #             print("Not Available: ", chal)
            # if initial_submission:
            #     user.profile.credits += game.total_point

            user.profile.credits += challenge.trophy.points
            user.profile.usergame.game_tours.add(game)
            user.profile.usergame.challenges.add(challenge)
            user.profile.usergame.save()
            user.profile.save()

            ReceivedPoint.objects.create(user=user, points=challenge.trophy.points, challenge=challenge, received_for='submission')

            return JsonResponse({"status": True, "response": True, "challenge_id": challenge_id, "error": None,"msg": "Congratulazioni! Immagine inviata con successo.", "reward": challenge.trophy.image.url })

        else:
            return JsonResponse({"status": False, "response": False, "error": None, "msg": "Non inviato, riprova."})

# class SubmitChallengeAPIView(APIView):

#     def post(self, request):
#         return Response({"status": True})



class SubmitChallengeAPIView1(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        try:
            user = request.user
            image = request.FILES.get('image', None)
            challenge_id = int(request.data.get('challenge_id'))
            challenge = Challenge.objects.get(pk=challenge_id)
            game = challenge.game
            if not challenge.status or not game.status:
                return Response({"error": "Challenge Not Available!"})
        except Challenge.DoesNotExist:
            return Response({"error": "No Challenge Found!"})
        
        if SubmitChallenge.objects.filter(user=request.user, challenge=challenge, game=challenge.game).exists():
            return Response({"error": "Esiste già!"})

        submit_challenge = SubmitChallenge.objects.create(user=request.user, challenge=challenge, game=challenge.game, points=challenge.trophy.points, image=image)
        # serializer = SubmitChallengeSerializer(submit_challenge, data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        user.profile.credits += challenge.trophy.points
        user.profile.usergame.game_tours.add(game)
        user.profile.usergame.save()
        user.profile.save()

        return Response({"status": True, "result": "Done!"})




from django.db.models import Count, Sum

class RankingAPIView(APIView):

    def get(self, request):
        game_id = request.query_params.get('game_id')
        if game_id:
            try:
                game = Game.objects.get(pk=game_id)
                if not game.status:
                    return Response({"error": "Game Unavailable!"})    
            except Game.DoesNotExist:
                return Response({"error": "Game Doesn't Exists!"})

            ranks = ReceivedPoint.objects.filter(challenge__game=game).values('user').annotate(sum=Sum('points')).order_by('-sum')
        else:
            ranks = ReceivedPoint.objects.all().values('user').annotate(sum=Sum('points')).order_by('-sum')
        print(ranks)
        
        listing = list()

        for rank in ranks:
            print(rank['user'], rank['sum'])
            temp = {}
            user = MyUser.objects.get(pk=int(rank['user']))
            temp['user_id'] = str(user.id)
            temp['username'] = user.first_name + ' ' + user.last_name
            temp['image'] = user.profile.image.url
            temp['points'] = str(rank['sum'])
            listing.append(temp)

        return Response({"status": True, "result": listing})
