from rest_framework import serializers
from watchlist.models import Movies, StreamingPlatform, Reviews
import datetime

#  normal serializers

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     Mname = serializers.CharField()
#     Mdesc = serializers.CharField()
#     isPublished = serializers.BooleanField()
#     Mdate = serializers.DateField()

#     def create(self, validated_data):
#         # we use the two asteriks for unpacking the dictionary
#         return Movies.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         # instance is the object that is already in the database
#         # validated_data is the data that is sent to the server
#         instance.Mname = validated_data.get('Mname', instance.Mname)
#         instance.Mdesc = validated_data.get('Mdesc', instance.Mdesc)
#         instance.isPublished = validated_data.get('isPublished', instance.isPublished)
#         instance.Mdate = validated_data.get('Mdate', instance.Mdate)
#         instance.save()
#         return instance

#  Model serializers


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True) # to get the username 
    class Meta:
        model = Reviews
        # the extra comma is important because it tells python that it is a tuple
        exclude = ('movie',)


class MovieSerializer(serializers.ModelSerializer):
    daysSinceRelease = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movies
        fields = "__all__"

    def get_daysSinceRelease(self, obj):
        return (datetime.date.today() - obj.Mdate).days
    # field validation

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short")
        elif len(value) > 100:
            raise serializers.ValidationError("Name is too long")
        else:
            return value
    # object validation

    def validate(self, data):
        if data['Mname'] == data['Mdesc']:
            raise serializers.ValidationError(
                "Name and Description should not be same")
        else:
            return data

#  thats it but for validation we still need to def the function whereas in normal serilizer we dont need to def the function and can use core api


class StreamingSerializer(serializers.ModelSerializer):
    # we need to add the moviesAvailable field in the StreamingPlatform model
    # the vairable name should be same as the related_name in the Movies model
    # moviesAvailable = MovieSerializer(many=True, read_only=True)
    # to get a link to the moviesAvailable
    # we use the hyperlinked related field

    watchlist = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='movie_details',
        lookup_field='id'
    )

    class Meta:
        model = StreamingPlatform
        fields = "__all__"
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
