from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet, CursoViewSet, MatriculaViewSet, RelatoriosViewSet

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet)   
router.register(r'cursos', CursoViewSet)
router.register(r'matriculas', MatriculaViewSet)
router.register(r'relatorios', RelatoriosViewSet, basename='relatorios')

urlpatterns = [
    path('', include(router.urls)),
]