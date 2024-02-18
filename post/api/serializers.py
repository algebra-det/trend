from post.models import Post, Comment, Like

from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    comment_id = serializers.SerializerMethodField('get_comment_id')
    post_id = serializers.SerializerMethodField('get_post_id')

    class Meta:
        model = Comment
        fields = ('comment_id', 'post_id', 'post', 'name', 'text', 'user')
        extra_kwargs = { 'post': {'write_only': True}}

    def get_name(self, comment):
        name = '{} {}'.format(comment.user.first_name, comment.user.last_name)
        return name

    def get_comment_id(self, comment):
        return comment.id

    def get_post_id(self, comment):
        return comment.post.id


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField('get_num_likes')
    name = serializers.SerializerMethodField('get_name')
    post_id = serializers.SerializerMethodField('get_post_id')
    challenge_id = serializers.SerializerMethodField('get_challenge_id')
    tour_name = serializers.SerializerMethodField()

    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['post_id', 'challenge_id', 'name', 'image', 'text', 'likes', 'commented', 'created_at', 'type_of_reward', 'tour_name']
    
    def get_tour_name(self, post):
        return post.challenge.game.title

    def get_num_likes(self, post):
        return post.liked.all().count()

    def get_name(self, post):
        name = '{} {}'.format(post.user.first_name, post.user.last_name)
        return name

    def get_post_id(self, post):
        return post.id

    def get_challenge_id(self, post):
        return post.challenge.id
    
    def get_image(self, post):
        if not post.submit_challenge:
            if not post.image:
                return False
            else:
                return post.image.url
            return False
        return post.submit_challenge.image.url


class PostDetailSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField('get_num_likes')
    comments = CommentSerializer(many=True, read_only=True)
    name = serializers.SerializerMethodField('get_name')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'name', 'image', 'text', 'likes', 'comments', 'type_of_reward']

    def get_num_likes(self, post):
        return post.liked.all().count()

    def get_name(self, post):
        name = '{} {}'.format(post.user.first_name, post.user.last_name)
        return name

    def get_image(self, post):
        if not post.submit_challenge:
            if not post.image:
                return False
            else:
                return post.image.url
            return False
        return post.submit_challenge.image.url
