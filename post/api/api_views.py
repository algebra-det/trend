from .serializers import PostSerializer, CommentSerializer, PostDetailSerializer
from post.models import Post, Comment, Like

from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import MyUser
from core.models import Reward, SubmitChallenge, ReceivedPoint
from game.models import Game, Challenge

from trend.pagination import CustomPagination

from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated


def check_for_liked(user, serializer_data):
    resultant_serializer = list()

    if user:
        for post in serializer_data:
            data = post
            id = data['post_id']
            post = Post.objects.get(pk=id)
            if user in post.liked.all():
                data.update({'have_liked': True})
            else:
                data.update({'have_liked': False})
            
            data.update({'user_id': post.user.id})
            data.update({'user_image': post.user.profile.image.url})
            if post.user in user.profile.following.all():
                data.update({'follow': False})
            else:
                data.update({'follow': True})
            resultant_serializer.append(data)
    else:
        for post in serializer_data:
            data = post
            post = Post.objects.get(pk=data['post_id'])
            data.update({'user_id': post.user.id})
            data.update({'user_image': post.user.profile.image.url})
            data.update({'have_liked': False})
            data.update({'follow': False})
            resultant_serializer.append(data)

    return resultant_serializer


class PostView(APIView, CustomPagination):
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        posts = Post.objects.filter(is_approved=True)
        data = self.paginate_queryset(posts, request, view=self)
        serializer = PostSerializer(data, many=True)
        if request.user.is_authenticated:
            resultant_serializer = check_for_liked(request.user, serializer.data)
            return self.get_paginated_response(resultant_serializer)
        else:
            resultant_serializer = check_for_liked(False, serializer.data)
            return self.get_paginated_response(serializer.data)


# POST VIEW IN A SINGLE CLASS AND FUNCTION
# class PostView(APIView, CustomPagination):
#     authentication_classes = [TokenAuthentication, SessionAuthentication]

#     def get(self, request):
#         posts = Post.objects.all()
#         data = self.paginate_queryset(posts, request, view=self)
#         serializer = PostSerializer(data, many=True)
#         resultant_serializer = list()
#         if request.user.is_authenticated:

#             for post in serializer.data:
#                 data = post
#                 id = data['id']
#                 post = Post.objects.get(pk=id)
#                 if request.user in post.liked.all():
#                     data.update({'have_liked': True})
#                 else:
#                     data.update({'have_liked': False})
#                 resultant_serializer.append(data)

#             print('\n\n\n Via Token\n\n',request.user)
#             return self.get_paginated_response(resultant_serializer)
#         else:
#             print('\n\n\n Via Not TOKEN\n\n')
#             return self.get_paginated_response(serializer.data)


class PostDetailView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        try:
            id = request.query_params.get('post_id')
            post = Post.objects.get(pk=id)
            if not post.is_approved:
                return Response({"error": "No Post Found!"})
        except Post.DoesNotExist:
            return Response({"error": "No Post Found!"})
        
        serializer = PostDetailSerializer(post)
        if not request.user.is_anonymous:
            if request.user in post.liked.all():
                have_liked = True
            else:
                have_liked = False
            
            if post.user in request.user.profile.following.all():
                follow = False
            else:
                follow = True

            result = {'status': True, 'have_liked': have_liked, 'follow': follow}
        else:
            result = {'status': True, 'have_liked': False}
        result.update({'user_image': post.user.profile.image.url})
        result.update(serializer.data)
        return Response(result, status=200)


@api_view(['POST'])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated,])
def create_post(request):
    user = request.user
    try:
        challenge_id = request.data.get('challenge_id', None)
        if challenge_id == None:
            return Response({"error": "challenge_id is required parameter"})

        if not Challenge.objects.filter(pk=challenge_id).exists():
            return Response({"error": "challenge does not exist!"})

        challenge = Challenge.objects.get(pk=challenge_id)

        if not SubmitChallenge.objects.filter(user=user).exists():
            return Response({"error": "No Submission Found by this user!"})

        if not SubmitChallenge.objects.filter(user=user, challenge=challenge).exists():
            return Response({"error": "No Submission Found for this challenge!"})

        submit_challenge = SubmitChallenge.objects.get(user=user, challenge=challenge)
        # if submit_challenge.challenge != challenge:
        #     return Response({"error": "Creating Post for this Submission is not available!"})

        if Post.objects.filter(challenge=challenge, user=user, submit_challenge=submit_challenge).exists():
            return Response({"error": "Il post esiste già!"})
    except SubmitChallenge.DoesNotExist:
        return Response({"error": "No Submission Found!"})

    if request.method == 'POST':
        post = Post.objects.create(user=user, challenge=challenge, submit_challenge=submit_challenge, type_of_reward='object')
        # serializer = PostDetailSerializer(post)
        # Reward for Rewarding

        # text = request.data.get('text', None)
        # if text:
        #     post.text = text
        #     post.save()
        #     post_reward = Reward.objects.all().first().per_post
        #     user.profile.credits += post_reward
        #     user.profile.save()

        # post_reward = Reward.objects.all().first().per_post
        # user.profile.credits += post_reward
        # user.profile.save()

        result = {'status': True, "msg": "Post creato con successo!"}
        # result.update(serializer.data)
        return Response(result, status=200)


# @api_view(['POST'])
# @authentication_classes([TokenAuthentication,])
# @permission_classes([IsAuthenticated,])
# def create_post(request):
#     user = request.user
#     try:
#         challenge_id = request.data.get('challenge_id', None)
#         if challenge_id == None:
#             return Response({"error": "challenge_id is required parameter"})
#         if not Challenge.objects.filter(pk=challenge_id).exists():
#             return Response({"error": "challenge does not exist!"})
#         challenge = Challenge.objects.get(pk=challenge_id)
#         if not SubmitChallenge.objects.filter(user=user).exists():
#             return Response({"error": "No Submission Found by this user!"})
#         if not SubmitChallenge.objects.filter(user=user, challenge=challenge).exists():
#             return Response({"error": "No Submission Found for this challenge!"})

#         submit_challenge = SubmitChallenge.objects.get(user=user, challenge=challenge)
#         # if submit_challenge.challenge != challenge:
#         #     return Response({"error": "Creating Post for this Submission is not available!"})

#         if Post.objects.filter(challenge=challenge, user=user).exists():
#             return Response({"error": "Il post esiste già!"})
#     except SubmitChallenge.DoesNotExist:
#         return Response({"error": "No Submission Found!"})

#     if request.method == 'POST':
#         post = Post.objects.create(user=user, challenge=challenge)
#         # serializer = PostDetailSerializer(post)
#         # Reward for Rewarding
#         text = request.data.get('text', None)
#         if text:
#             post.text = text
#             post.save()
#             post_reward = Reward.objects.all().first().per_post
#             user.profile.credits += post_reward
#             user.profile.save()
#         result = {'status': True, "msg": "Post created Successfulll!"}
#         # result.update(serializer.data)
#         return Response(result, status=200)



@api_view(['POST'])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated,])
def edit_post(request):

    if request.method == 'POST':
        user = request.user
        try:
            challenge_id = request.data.get('challenge_id')
            challenge = Challenge.objects.filter(pk=challenge_id)
            if not challenge.exists():
                return Response({"error": "Challenge Not Found!"})
            challenge = challenge.first()
            if not challenge.magic_box:
                return Response({"error": "NO social content task for this challenge!"})
            text = request.data.get('text', None)
            image = request.FILES.get('image', None)
            if not text:
                return Response({"error": "Text is mendatory!"})
            post = Post.objects.filter(user=user, challenge=challenge, text__isnull=False, type_of_reward='social')
            if post.exists():
                return Response({"error": "Post Already Exists!"})
            else:
                if image:
                    post = Post.objects.create(user=user, challenge=challenge, text=text, image=image, type_of_reward='social')
                else:
                    post = Post.objects.create(user=user, challenge=challenge, text=text, type_of_reward='social')
        except Post.DoesNotExist:
            return Response({"error": "No Post Found!"})

        challenges = challenge.game.games.all()
        initial_submission = True
        for chal in challenges:
            if initial_submission:
                if Post.objects.filter(user=user, challenge=chal, text__isnull=False, submit_challenge__isnull=True, type_of_reward='social' ).exists():
                    print("Is Available: ", chal)
                else:
                    initial_submission = False
                    print("Not Available: ", chal)
        if initial_submission:
            user.profile.credits += challenge.game.total_point

        user.profile.credits += challenge.magic_box.points
        user.profile.save()
        ReceivedPoint.objects.create(user=user, points=challenge.magic_box.points, challenge=challenge, received_for='content')
        return Response({"status": True, "msg": "Post creato con successo!", "reward": challenge.magic_box.image.url }, status=200)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication,])
# @permission_classes([IsAuthenticated,])
# def edit_post(request):
#     user = request.user
#     try:
#         challenge_id = request.data.get('challenge_id')
#         text = request.data.get('text')
#         submitted_challenge = SubmitChallenge.objects.get(challenge_id=challenge_id, user=user)
#         post = Post.objects.get(user=user, challenge=submitted_challenge)
#         if post.text:
#             return Response({"error": "Can't change previously written text!"})
#     except Post.DoesNotExist:
#         return Response({"error": "No Post Found!"})

#     if request.method == 'POST':
#         post.text = text
#         post.save()
#         per_post = Reward.objects.all().first().per_post
#         user.profile.credits += per_post
#         user.profile.save()
#         return Response({"status": True, "msg": "Successfully added text to post"}, status=200)


@api_view(['POST',])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated,])
def create_comment(request):
    user = request.user
    comment = Comment(user=user)

    if request.method == 'POST':
        serializer = CommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        result = {'status': True}
        result.update(serializer.data)
        return Response(result, status=200)


@api_view(['DELETE',])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated,])
def delete_comment(request):
    try:
        id = request.query_params.get('comment_id')
        comment = Comment.objects.get(pk=id)
    except Exception:
        return Response({"error": "comment not found"}, status=500)

    if comment.user == request.user:
        if request.method == 'DELETE':
            comment.delete()
            return Response({"status": True, "message": "comment deleted"}, status=200)
    else:
        return Response({"error": "You are not authorized to command this request"})




@api_view(['POST',])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated,])
def add_like(request):
    user = request.user
    try:
        id = request.data.get('post_id')
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({"error": "Post does not exist"}, status=404)

    if request.method == 'POST':
        if user in post.liked.all():
            post.liked.remove(user)
        else:
            post.liked.add(user)

        post.save()
        serializer = PostSerializer(post)
        result = {'status': True}
        result.update(serializer.data)
        return Response(result, status=200)




# FUNCTION BASED PAGINATION
# Currently on work
@api_view(['GET'])
def UserPostAPIView(request):
    paginator = PageNumberPagination()

    try:
        id = request.query_params.get('user_id')
        user = MyUser.objects.get(pk=id)
        if user.is_admin or user.is_superuser:
            return Response({"error": "No Post's Found"})
    except MyUser.DoesNotExist:
        return Response({"error": "No User's Post Found!"}, status=404)

    if request.method == 'GET':
        posts = Post.objects.filter(user=user)
        result = paginator.paginate_queryset(posts, request)
        serializer = PostDetailSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)


# APIView CLASS BASED PAGINATION

class UserPostView(APIView, PageNumberPagination):

    def get(self, request):
        try:
            id = request.query_params.get('user_id')
            user = MyUser.objects.get(pk=id)
        except MyUser.DoesNotExist:
            return Response({"error": "No User's Post Found!"}, status=404)
        
        if request.method == 'GET':
            posts = Post.objects.filter(Q(user=user) & Q(is_approved=True))
            results = self.paginate_queryset(posts, request, view=self)
            serializer = PostSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)
