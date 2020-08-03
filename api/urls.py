from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('finite_values_entity', views.finite_values_entity, name='finite_values_entity'),
    path('numeric_entity', views.numeric_entity, name='numeric_entity'),
]