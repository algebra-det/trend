from game.models import Challenge
from product.models import Product, ProductRequest
from account.models import MyUser
from core.models import Profile, ReceivedPoint
from post.models import Post
from game.api.serializers import GameSerializer, UserChallengeSerializer
from post.api.serializers import PostSerializer
from product.api.serializers import ProductSerailizer

from rest_framework import serializers

from trend import utils


districts_dict = utils.get_districts_dict()

districts = utils.get_districts_list()

# districts = ['Lombardy', 'Non Valley']

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


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField('get_username')
    game_tours = serializers.SerializerMethodField('get_games')
    posts = PostSerializer(many=True, read_only=True)
    user_id = serializers.SerializerMethodField()
    products_purchased = serializers.SerializerMethodField()
    challenges_completed = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['image', 'username', 'user_id', 'latitude', 'longitude', 'game_tours', 'posted', 'credits', 'posts', 'products_purchased', 'challenges_completed', 'email']
        extra_kwargs = {
            'latitude': {'write_only': True},
            'longitude': {'write_only': True},
            }
    
    def get_email(self, profile):
        return profile.user.email
    
    def get_challenges_completed(self, profile):
        user = profile.user
        challenges = ReceivedPoint.objects.filter(user=user).select_related('challenge').values('challenge')
        print("challenges: ", challenges)
        challenges = Challenge.objects.filter(id__in=[challenge['challenge'] for challenge in challenges])
        serializer = UserChallengeSerializer(challenges, many=True)
        return serializer.data
    
    def get_products_purchased(self, profile):
        requests = ProductRequest.objects.filter(user=profile.user, fullfilled=True).select_related('product')
        products = []
        for request in requests:
            product = request.product
            products.append(product)

        serializer = ProductSerailizer(products, many=True)
        return serializer.data

    def get_username(self, profile):
        return '{} {}'.format(profile.user.first_name, profile.user.last_name)
    
    def get_games(self, profile):
        return profile.usergame.game_tours.all().count()

    def get_user_id(self, profile):
        return profile.user.id


class ProfileFollowingSerialzier(serializers.ModelSerializer):
    province = serializers.SerializerMethodField('get_province')
    image = serializers.SerializerMethodField('get_image')
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = MyUser
        fields = ['id', 'image', 'username', 'province']
        # extra_kwargs = {
        #     'image': {'write_only': True},
        #     'username': {'write_only': True},
        #     'image': {'write_only': True}
        # }


    def get_province(self, user):
        return user.province
        
    def get_image(self, user):
        return user.profile.image.url
    
    def get_username(self, user):
        return '{} {}'.format(user.first_name, user.last_name)



class ProfileDPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']



class ProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'dob', 'city', 'province', 'email']

    def get_email(self, user):
        return user.email
    
    def validate(self, attrs):
        province = attrs.get('province', '')
        if province and province not in districts:
            raise serializers.ValidationError('Choose province from the option!')

        return attrs

    def update(self, instance, validated_data):
        instance = instance

        if validated_data.get('province', None):
            province = validated_data['province']
            instance.province = province
            instance.profile.latitude = districts_dict[province]['latitude']
            instance.profile.longitude = districts_dict[province]['longitude']
        if validated_data.get('first_name', None):
            instance.first_name = validated_data['first_name']

        if validated_data.get('last_name', None):
            instance.last_name = validated_data['last_name']

        if validated_data.get('dob', None):
            instance.dob = validated_data['dob']

        if validated_data.get('city', None):
            instance.city = validated_data['city']

        if validated_data.get('province', None):
            instance.province = validated_data['province']

        instance.save()
        return instance
