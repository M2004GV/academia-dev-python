"""
URL configuration for core project.

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
from django.urls import path, include
from escola import views as escola_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # endpoint /api/
    path('api/', include('escola.urls')),

    path('dashboard/', escola_views.dashboard, name='dashboard'),
    path('alunos/<int:aluno_id>/historico/', escola_views.historico_aluno, name='aluno_historico'),

]
