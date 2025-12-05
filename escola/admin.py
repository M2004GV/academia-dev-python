from django.contrib import admin
from .models import Aluno, Curso, Matricula


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'cpf', 'data_ingresso')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('data_ingresso',)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'carga_horaria', 'valor_inscricao', 'status_curso')
    search_fields = ('nome',)
    list_filter = ('status_curso',)


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('id', 'aluno', 'curso', 'data_matricula', 'status_pagamento', 'valor_pago')
    search_fields = ('aluno__nome', 'curso__nome')
    list_filter = ('status_pagamento', 'data_matricula')
