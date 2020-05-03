from django.urls import path
from . import views


urlpatterns = [
    path('message', views.message),
    path('home_message', views.home_message),
    path('comment', views.comment),
    path('home/', views.home),
    path('my_account/<int:user_id>/', views.my_account),
    path('add_rides/<int:id>/', views.add_rides),
    path('follow_rides/<int:id>/', views.follow_rides),
    path('ride_blog/', views.ride_blog),
    path('delete_message/<int:message_id>', views.delete_message),
    path('update_account', views.update_account),
]
