from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),

    path('trips/add', views.add),
    path('add_travel', views.add_travel),
    path('travels/trips/<int:trip_id>', views.destination),
    path('travels/join/<int:trip_id>', views.join_trip),
    path('cancel/<int:trip_id>', views.cancel),
    path('delete/<int:trip_id>', views.delete),
]
