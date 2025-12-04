from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db import connection
from django.db.models import Sum, Count

from .models import Aluno, Curso, Matricula
from .serializers import AlunoSerializer, CursoSerializer, MatriculaSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer 

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class MatriculaViewSet(viewsets.ModelViewSet):  
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer

    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        matricula = self.get_object()
        matricula.status_pagamento = 'pago'
        matricula.valor_pago = matricula.curso.valor_inscricao
        matricula.save()
        return Response({'status': 'pago'})
    

class RelatoriosViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def total_matriculas_por_curso(self, request):
        query = """
            SELECT c.nome AS curso, COUNT(m.id) AS total
            FROM curso c
            LEFT JOIN matricula m ON m.curso_id = c.id
            GROUP BY c.nome;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        data = [{'curso': row[0], 'total_matriculas': row[1]} for row in rows]
        return Response(data)