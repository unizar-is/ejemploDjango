"""
URL configuration for tutorialUnizar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from encuestas import views as encuestas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', encuestas.home_view, name='home'),

    path('resultados/<pregunta_id>/', encuestas.resultados_view, name='resultados'),
    path('votar/<pregunta_id>/', encuestas.votar_view, name='votar'),

    path('login/', encuestas.login_view, name='login'),
    path("logout/", encuestas.logout_view, name="logout"),

        path('crear/', encuestas.crear_view, name='crear'),
        path("editar/<int:pregunta_id>/",encuestas.editar_view,name="editar"),
        path("eliminar/<int:pregunta_id>/", encuestas.eliminar_view, name="eliminar"),
]