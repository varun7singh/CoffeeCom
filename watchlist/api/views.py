from django.shortcuts import render
from rest_framework import status
from watchlist.models import Movies, StreamingPlatform, Reviews
from watchlist.api.serializers import MovieSerializer, StreamingSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.exceptions import ValidationError
# from rest_framework import mixins

#  below is function defined api_view


@api_view(['GET', 'POST'])
def movie_list(req):
    if (req.method == "GET"):
        # complex data
        movie = Movies.objects.all()
        print(movie)
        # we use serialiser to convert complex data to json
        serializer = MovieSerializer(movie, many=True)
        return Response(serializer.data)
    if (req.method == "POST"):
        serializer = MovieSerializer(data=req.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_details(req, id):
    if (req.method == 'GET'):
        try:
            movie = Movies.objects.get(id=id)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movies.DoesNotExist:
            return Response({"message": f"Record not found with id:{id}"}, status=status.HTTP_404_NOT_FOUND)

    if (req.method == 'PUT'):
        movie = Movies.objects.get(id=id)
        serializer = MovieSerializer(movie, req.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    if (req.method == 'DELETE'):
        try:
            movie = Movies.objects.get(id=id)
            movie.delete()
            return Response({"message": f"Record successfully deleted with id:{id}"}, status=status.HTTP_204_NO_CONTENT)
        except Movies.DoesNotExist:
            return Response({"message": f"Record not found with id:{id}"}, status=status.HTTP_404_NOT_FOUND)

# below is class based view APIViews

# class streaming_list(APIView):
#     def get(self, req):
#         movie = Movies.objects.all()
#         serializer = MovieSerializer(movie, many=True)
#         return Response(serializer.data)
#     def post(self, req):
#         serializer = MovieSerializer(data=req.data)
#         if (serializer.is_valid()):
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# class streaming_details(APIView):


@api_view(['GET', 'POST'])
def streaming_list(req):
    if (req.method == "GET"):
        streamingPlatform = StreamingPlatform.objects.all()
        serializer = StreamingSerializer(
            streamingPlatform, many=True, context={'request': req})
        return Response(serializer.data)
    if (req.method == "POST"):
        serializer = StreamingSerializer(data=req.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def streaming_details(req, id):
    if (req.method == 'GET'):
        try:
            objects = StreamingPlatform.objects.get(id=id)
            serializer = StreamingSerializer(objects)
            return Response(serializer.data)
        except StreamingPlatform.DoesNotExist:
            return Response({"message": f"Record not found with id:{id}"}, status=status.HTTP_404_NOT_FOUND)

    if (req.method == 'PUT'):
        objects = StreamingPlatform.objects.get(id=id)
        serializer = StreamingSerializer(objects, req.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    if (req.method == 'DELETE'):
        try:
            movie = StreamingPlatform.objects.get(id=id)
            movie.delete()
            return Response({"message": f"Record successfully deleted with id:{id}"}, status=status.HTTP_204_NO_CONTENT)
        except StreamingPlatform.DoesNotExist:
            return Response({"message": f"Record not found with id:{id}"}, status=status.HTTP_404_NOT_FOUND)

# we can also use mixins along with generic viewsa api class

# class ReviewList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, req):
#         return self.list(req)

#     def post(self, req):
#         return self.create(req)


# class ReviewDetails(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializer
#     # as default lookup_field is pk but we have used id in our model
#     lookup_field = 'id'

#     def get(self, req, id):
#         return self.retrieve(req, id)

#     def put(self, req, id):
#         return self.update(req, id)

#     def delete(self, req, id):
#         return self.destroy(req, id)


# same can be done using generic views

class ReviewList(generics.ListAPIView):
    #  each concrete view must either define a queryset attribute, or override the get_queryset() method.
    serializer_class = ReviewSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        return Reviews.objects.filter(movie=id)


class ReviewCreate(generics.CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

    # overinding the perform_create method to add review to movie we want rather than specifying the movie_id in url to add review
    def perform_create(self, serializer):
        id = self.kwargs['id']
        movie = Movies.objects.get(id=id)
        # user should be able to review only once
        author = self.request.user
        isReviewed = Reviews.objects.filter(
            movie=movie, author=author).exists()
        if (isReviewed):
            raise ValidationError("You can review only once")
        serializer.save(movie=movie, author=author)
        return Response(serializer.data)


class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    # as default lookup_field is pk but we have used id in our model
    lookup_field = 'id'
