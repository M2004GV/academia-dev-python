from django.shortcuts import render, get_object_or_404
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
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """
        Lista as matrículas de um aluno espífico
        """
        aluno_id = request.query_params.get('aluno_id')
        if not aluno_id:
            return Response({'detail': 'aluno_id é obrigatório como parâmetro de consulta.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            aluno_id = int(aluno_id)
        except ValueError:
            return Response({'detail': 'aluno_id deve ser um número inteiro.'}, status=status.HTTP_400_BAD_REQUEST)
        qs = self.queryset.filter(aluno_id=aluno_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    

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
    
    @action(detail=False, methods=['get'])
    def total_devido_por_aluno(self, request):
        """ Retorna o valor total devido por cada aluno"""
        query = """
            SELECT a.id, a.nome, COALESCE(SUM(c.valor_inscricao), 0) AS total_devido
            FROM aluno a
            LEFT JOIN matricula m ON m.aluno_id = a.id
            LEFT JOIN curso c ON c.id = m.curso_id
            GROUP BY a.id, a.nome
            ORDER BY a.nome
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        data = [
            {
                'aluno_id': row[0],
                'aluno': row[1],
                'total_devido': float(row[2]) if row[2] is not None else 0.0,
            }
            for row in rows
        ]
        return Response(data)

    @action(detail=False, methods=['get'])
    def pagamentos_pendentes(self, request):
        """ Retorna o valor total pendente por aluno."""
        query = """
            SELECT a.id, a.nome,
                   COALESCE(SUM(c.valor_inscricao), 0) AS total_devido,
                   COALESCE(SUM(m.valor_pago), 0) AS total_pago,
                   COALESCE(SUM(c.valor_inscricao), 0) - COALESCE(SUM(m.valor_pago), 0) AS total_pendente
            FROM aluno a
            LEFT JOIN matricula m ON m.aluno_id = a.id
            LEFT JOIN curso c ON c.id = m.curso_id
            GROUP BY a.id, a.nome
            ORDER BY a.nome
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        data = [
            {
                'aluno_id': row[0],
                'aluno': row[1],
                'total_devido': float(row[2]) if row[2] is not None else 0.0,
                'total_pago': float(row[3]) if row[3] is not None else 0.0,
                'total_pendente': float(row[4]) if row[4] is not None else 0.0,
            }
            for row in rows
        ]
        return Response(data)


# -----------------------------------------------------------------------------
# Views para relatórios HTML
# -----------------------------------------------------------------------------
def historico_aluno(request, aluno_id: int):
    """   Gera o relatório de histórico de um aluno específico."""
    aluno = get_object_or_404(Aluno, pk=aluno_id)

    # otimizar consultas com select_related
    matriculas = Matricula.objects.filter(aluno=aluno).select_related('curso')
    total_matriculas = matriculas.count()
    total_pago = matriculas.aggregate(total=Sum('valor_pago'))['total'] or 0
    total_devido = sum(m.curso.valor_inscricao for m in matriculas)
    total_pendente = total_devido - total_pago
    context = {
        'aluno': aluno,
        'matriculas': matriculas,
        'total_matriculas': total_matriculas,
        'total_pago': total_pago,
        'total_devido': total_devido,
        'total_pendente': total_pendente,
    }
    return render(request, 'aluno_historico.html', context)


def dashboard(request):
    """
    Exibe o dashboard geral
    Os dados exibidos incluem:

    total de alunos
    total de cursos ativos e inativos
    total de matrículas pagas e pendentes
    receita total recebida e receita pendente
    número de matrículas por curso

    """

    total_alunos = Aluno.objects.count()
    cursos_ativos = Curso.objects.filter(status_curso=True).count()
    cursos_inativos = Curso.objects.filter(status_curso=False).count()
    matriculas_pagas = Matricula.objects.filter(status_pagamento='pago').count()
    matriculas_pendentes = Matricula.objects.filter(status_pagamento='pendente').count()
    total_valor_pago = Matricula.objects.filter(status_pagamento='pago').aggregate(total=Sum('valor_pago'))['total'] or 0
    total_valor_pendente = Matricula.objects.filter(status_pagamento='pendente').aggregate(total=Sum('curso__valor_inscricao'))['total'] or 0
    matriculas_por_curso_qs = Matricula.objects.values('curso__nome').annotate(total=Count('id')).order_by('curso__nome')
    matriculas_por_curso = [
        {'curso': item['curso__nome'], 'total_matriculas': item['total']}
        for item in matriculas_por_curso_qs
    ]
    context = {
        'total_alunos': total_alunos,
        'cursos_ativos': cursos_ativos,
        'cursos_inativos': cursos_inativos,
        'matriculas_pagas': matriculas_pagas,
        'matriculas_pendentes': matriculas_pendentes,
        'total_valor_pago': total_valor_pago,
        'total_valor_pendente': total_valor_pendente,
        'matriculas_por_curso': matriculas_por_curso,
    }
    return render(request, 'dashboard.html', context)