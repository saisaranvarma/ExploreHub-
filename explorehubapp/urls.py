from django.urls import path
from . views import *
from . import views

urlpatterns = [
    path('create/',DestinationsCreateView.as_view(),name="create-destination"),
    path('detail/<int:pk>/',DestinationsDetail.as_view(),name="detail"),
    path('update/<int:pk>/',DestinationsUpdateView.as_view(),name="update-destination"),
    path('delete/<int:pk>/',DestinationsDelete.as_view(),name="delete-destination"),
    path('search/<str:Name>/',DestinationsSearchView.as_view(),name="search"),
    path('create_destination/',views.create_destination,name="create"),
    path('update_destination/<int:id>/',views.update_destination,name="update-destination"),
    path('',views.index,name='index'),
    path('destination_fetch/<int:id>/',views.destination_fetch,name='destination_fetch'),
    path('destination_delete/<int:id>/',views.destination_delete,name='destination_delete'),

]