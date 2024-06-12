from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('datos/', views.database, name="base_de_datos"),
    path('crear_cardumen/', views.crear_cardumen, name="crear_cardumen"),
    path('obtener_viaje/', views.obtener_viaje, name="obtener_viaje"),
    path('obtener_viaje/estadisticas_viaje/<int:coordenadaX>/<int:coordenadaY>', views.estadisticas_viaje , name="estadisticas_viaje")

] 