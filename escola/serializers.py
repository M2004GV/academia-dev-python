from rest_framework import serializers
from .models import Aluno, Curso, Matricula
from .validators import validar_cpf

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

    def validate_cpf(self, value):
        try:
            validar_cpf(value)
            return value
        except Exception as e:
            raise serializers.ValidationError(str(e))
    

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class MatriculaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)

    class Meta:
        model = Matricula
        fields = '__all__'