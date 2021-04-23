from rest_framework import serializers

from my_profile.models import Profile, CodeImage, Review, Like, Favourite


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image', )

    def _get_image_url(self, obj):
        request = self.context.get('request')

        if obj.image:
            url = obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''
    def to_representation(self, instance):
        representation = super(ImageSerializer, self).to_representation(instance)
        representation['image'] = self._get_image_url(instance)

        return representation


class ProfileSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)


    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'gender', 'hobbies', 'images')

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        author = request.user
        validated_data.setdefault('user', author)
        profile = Profile.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            CodeImage.objects.create(profile=profile, image=image)
        return profile

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.images.all().delete()
        images_data = request.FILES
        for image in images_data.getlist('images'):
            CodeImage.objects.create(
                profile=instance, image=image
                )
        instance.save()
        return instance

    def to_representation(self, instance):
        print(instance)
        representation = super().to_representation(instance)
        # representation['like'] = LikeSerializer(instance.likes.filter(like=True), many=True, context=self.context).data
        return representation



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        review = Review.objects.create(
            author=author, **validated_data
        )
        return review


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'create':
            fields.pop('from_user')
            fields.pop('to_user')
        return fields

    def create(self, validated_data):
        request = self.context.get('request')
        from_user = request.user
        to_user = validated_data.get('from_user')
        like = Like.objects.get_or_create(from_user=from_user, to_user=to_user)[0]
        if like.like is False:
            like.like = True
        else:
            like.like = False
        like.save()
        return like


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = '__all__'


# class FavoriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Favorite
#         fields = ('id', 'post', 'user', 'favorite')
#
#     def get_fields(self):
#         action = self.context.get('action')
#         fields = super().get_fields()
#         if action == 'create':
#             fields.pop('user')
#             fields.pop('favorite')
#         return fields
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         post = validated_data.get('post')
#         favorite = Favorite.objects.get_or_create(user=user, post=post)[0]
#         if favorite.favorite == False:
#             favorite.favorite = True
#         else:
#             favorite.favorite = False
#         favorite.save()
#         return favorite