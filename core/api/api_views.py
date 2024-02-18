from rest_framework import serializers
from account.models import MyUser
from core.models import Profile, Privacy, Conditions, Credits, ReceivedPoint

from core.api.serializers import ProfileSerializer, ProfileFollowingSerialzier, ProfileDPSerializer, ProfileUpdateSerializer 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from trend.pagination import CustomPagination

from account.api.utils import sending_invite
from game.models import Game, Challenge
from game.api.serializers import CompletedToursSerializer


from trend import utils


districts_dict = utils.get_districts_dict()
districts_list = utils.get_districts_list()

# districts_dict = {
#     'Lombardy': {
#         'latitude': 45.585556,
#         'longitude': 9.930278,
#     },
#     'Non Valley': {
#         'latitude': 46.337353,
#         'longitude': 11.057293
#     }
# }


class GetListAPIView(APIView):
    def get(self, request):
        result = {'status': True, 'districts': districts_list}
        return Response(result)


class ProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    def get(self, request):
        try:
            id = request.query_params.get('user_id')
            user = MyUser.objects.get(pk=id)
            if user.is_admin or user.is_superuser:
                return Response({"error": "No Profile Found"})
            if not Profile.objects.filter(user=user).exists():
                return Response({"error": "No Profile Found!"}, status=204)
        except MyUser.DoesNotExist:
            return Response({"error": "User doesn't exist!"}, status=204)
        
        profile = user.profile
        serializer = ProfileSerializer(profile)
        newdict={'status': True}
        newdict.update(serializer.data)
        if not request.user.is_anonymous:
            if request.user != user:
                if user in request.user.profile.following.all():
                    newdict['follow'] = True
                else:
                    newdict['follow'] = False
            else:
                newdict['follow'] = False
        else:
            newdict['follow'] = False
        return Response(newdict, status=200)



class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def post(self, request):
        try:
            id = request.data.get('user_id')
            user = MyUser.objects.get(pk=id)
            if user.is_admin or user.is_superuser or user.is_staff:
                return Response({"error": "Can't Follow"})
        except MyUser.DoesNotExist:
            return Response({"error": "No User Found!"}, status=204)

        logged_in_user = request.user
        logged_in_profile = logged_in_user.profile
        if request.user != user:
            if user in logged_in_profile.following.all():
                logged_in_profile.following.remove(user)
                logged_in_profile.save()
                return Response({'status': True, "message": "Now you are not following {} {}".format(user.first_name, user.last_name)}, status=201)
            else:
                logged_in_profile.following.add(user)
                logged_in_profile.save()
                return Response({'status': True, "message": "Now you are following {} {}".format(user.first_name, user.last_name)}, status=201)
        else:
            return Response({"error": "you can't follow yourself!"}, status=204)



class FollowingsAPIView(APIView, CustomPagination):
    
    def get(self, request):
        try:
            user_id = int(request.query_params.get('user_id'))
            user = MyUser.objects.get(pk=user_id)
            if user.is_admin or user.is_superuser or user.is_staff:
                return Response({"error": "Can't Get the User"})
            profile = user.profile
        except MyUser.DoesNotExist:
            return Response({"error": "No User Found!"}, status=204)

        following = profile.following.all().order_by('first_name')
        data = self.paginate_queryset(following, request, view=self)
        serializer = ProfileFollowingSerialzier(data, many=True)
        newdict = {}
        newdict.update({"friends": serializer.data})
        related_user = MyUser.objects.filter(province=user.province, is_verified=True).exclude(pk=user.id).order_by('?')[:10]
        people_you_may_know_serializer = ProfileFollowingSerialzier(related_user, many=True)
        newdict.update({"people_you_may_know": people_you_may_know_serializer.data})
        return self.get_paginated_response(newdict)


class ProfielDPAPIView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        try:
            user = request.user
            if user.is_admin:
                return Response({"error": "No User For Such Change!"})
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "No User Found"})

        if request.method == 'POST':
            serializer = ProfileDPSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": True, "message": "DP è cambiato con successo!"})


class ProfileUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        try:
            user = request.user
            if user.is_admin:
                return Response({"error": "No User For Such Actions!"})
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "No User Found!"})
        
        serializer = ProfileUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        profile.latitude = districts_dict[user.province]['latitude']
        profile.longitude = districts_dict[user.province]['longitude']
        profile.save()
        result = {"status": True}
        result.update(serializer.data)
        return Response(result)

    def get(self, request):
        try:
            user = request.user
            if user.is_admin:
                return Response({"error": "No User For Such Actions!"})
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "No User Found!"})

        serializer = ProfileUpdateSerializer(user)
        result = {"status": True}
        result.update(serializer.data)
        return Response(result)


class InviteAPIView(APIView):
    # authentication_classes = [TokenAuthentication,]
    # permission_classes = [IsAuthenticated,]
    
    def post(self, request):
        try:
            email = request.data.get('email')
            print(email)
        except Exception as e:
            return Response({"error": "Something went wrong"})
        
        if request.POST:
            sending_invite(email)
            return Response({"status": True, "msg": "Invitation sent successfully!"})


class PrivacyAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        privacy = Privacy.objects.first()
        return Response({"status": True, "data" : privacy.text})


class ConditionsAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        cnoditions = Conditions.objects.first()
        return Response({"status": True, "data" : cnoditions.text})


class CreditsAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        first_credit = Credits.objects.first()
        return Response({"status": True, "data" : first_credit.text})

from django.db.models import Count, Sum

class CompletedToursAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = ( IsAuthenticated,)

    def get(self, request):
        user = request.user
        earned_points = ReceivedPoint.objects.filter(user=user).values('game').distinct()
        print('Earned Points: ', earned_points)
        game_ids = []
        for game in earned_points:
            initial_games_all_completed = True
            challenges = Challenge.objects.filter(game=game['game'])
            print('Challenges are: ', challenges)
            for challenge in challenges:
                if challenge.trophy:
                    print('Challenges are trophy: ', challenge)
                    if not ReceivedPoint.objects.filter(user=user, challenge=challenge, received_for='submission').exists():
                        initial_games_all_completed = False
                        break
                if challenge.magic_box:
                    print('Challenges are magic: ', challenge)
                    print('is done: ', ReceivedPoint.objects.filter(user=user, challenge=challenge, received_for='content'))
                    if not ReceivedPoint.objects.filter(user=user, challenge=challenge, received_for='content').exists():
                        initial_games_all_completed = False
                        break

            
            if initial_games_all_completed:
                print('Completed game ID: ', game['game'])
                game_ids.append(game['game'])
            
        games = Game.objects.filter(id__in=game_ids)
        print('game_ids: ', game_ids)
        print('Games are : ', games)
        serializer = CompletedToursSerializer(games, many=True)
        return Response({
            "status": True,
            "data": serializer.data
        })


class RunningToursAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = ( IsAuthenticated,)

    def get(self, request):
        user = request.user
        earned_points = ReceivedPoint.objects.filter(user=user).values('game').distinct()
        print('Earned Points: ', earned_points)
        game_ids = []
        for game in earned_points:
            initial_games_all_completed = True
            challenges = Challenge.objects.filter(game=game['game'])
            print('Challenges are: ', challenges)
            for challenge in challenges:
                if challenge.trophy:
                    print('Challenges are trophy: ', challenge)
                    if not ReceivedPoint.objects.filter(user=user, challenge=challenge, received_for='submission').exists():
                        initial_games_all_completed = False
                        break
                if challenge.magic_box:
                    print('Challenges are magic: ', challenge)
                    print('is done: ', ReceivedPoint.objects.filter(user=user, challenge=challenge, received_for='content'))
                    if not ReceivedPoint.objects.filter(user=user, challenge=challenge, received_for='content').exists():
                        initial_games_all_completed = False
                        break

            
            if not initial_games_all_completed:
                print('Completed game ID: ', game['game'])
                game_ids.append(game['game'])
            
        games = Game.objects.filter(id__in=game_ids)
        print('game_ids: ', game_ids)
        print('Games are : ', games)
        serializer = CompletedToursSerializer(games, many=True)
        return Response({
            "status": True,
            "data": serializer.data
        })
