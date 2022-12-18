from django.urls import path
from .views import movie_list, movie_details, streaming_list, streaming_details, ReviewList, ReviewDetails, ReviewCreate

urlpatterns = [
    path("list/", movie_list, name="movie_list"),
    path("<int:id>/", movie_details, name="movie_details"),
    path("streaming/", streaming_list, name="streaming_list"),
    path("streaming/<int:id>/", streaming_details, name="streaming_details"),
    path("streaming/<int:id>/reviews/", ReviewList.as_view(), name="review_list"),
    path("streaming/<int:id>/reviews_create/",
         ReviewCreate.as_view(), name="review_create"),
    path("streaming/reviews/<int:id>/",
         ReviewDetails.as_view(), name="review_details"),
]
