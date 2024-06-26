from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('obtener_viaje/', views.obtener_viaje, name="obtener_viaje"),
    path('obtener_viaje/estadisticas_viaje/', views.estadisticas_viaje , name="estadisticas_viaje")

] 