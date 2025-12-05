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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Escola API",
        default_version='v1',
        description="Documentação da API da Escola",
        contact=openapi.Contact(email="garciamateus@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # endpoint /api/
    path('api/', include('escola.urls')),

    path('docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),

    path('dashboard/', escola_views.dashboard, name='dashboard'),
    path('alunos/<int:aluno_id>/historico/', escola_views.historico_aluno, name='aluno_historico'),

]
