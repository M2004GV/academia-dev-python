import os
import django
import random
from datetime import date, timedelta

# Configura o Django para rodar fora do manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from escola.models import Aluno, Curso, Matricula


def run():
    # criar alunos
    alunos_data = [
        ("Ana Bezerra", "ana@example.com", "11111111111"),
        ("Bruno Henrique", "bruno@example.com", "22222222222"),
        ("Carla Souza", "carla@example.com", "33333333333"),
        ("Daniel Rocha", "daniel@example.com", "44444444444"),
        ("Eduarda Martins", "eduarda@example.com", "55555555555"),
        ("Fernanda Torres", "fernanda@example.com", "66666666666"),
        ("Gabriel Ferreira", "gabriel@example.com", "77777777777"),
        ("Helena Dias", "helena@example.com", "88888888888"),
        ("Igor Almeida", "igor@example.com", "99999999999"),
        ("Joana Melo", "joana@example.com", "10101010101"),
        ("Kleber Castro", "kleber@example.com", "12121212121"),
        ("Larissa Andrade", "larissa@example.com", "13131313131"),
        ("Marcelo Farias", "marcelo@example.com", "14141414141"),
        ("Natália Freire", "natalia@example.com", "15151515151"),
        ("Otávio Ramos", "otavio@example.com", "16161616161"),
    ]

    alunos = []
    for nome, email, cpf in alunos_data:
        aluno, _ = Aluno.objects.get_or_create(
            email=email,
            defaults={"nome": nome, "cpf": cpf},
        )
        alunos.append(aluno)

    print(f"Alunos inseridos: {len(alunos)}")

    #criar cursos
    cursos_data = [
        ("Python Básico", 40, 300.00),
        ("Django Web Framework", 60, 500.00),
        ("Banco de Dados PostgreSQL", 50, 450.00),
        ("Machine Learning Intro", 70, 800.00),
        ("Data Science Completo", 100, 1200.00),
        ("API Design com DRF", 30, 350.00),
        ("Docker e DevOps", 40, 400.00),
        ("Git e Controle de Versão", 20, 150.00),
        ("Estruturas de Dados", 60, 600.00),
        ("Algoritmos Avançados", 80, 900.00),
    ]

    cursos = []
    for nome, carga, valor in cursos_data:
        curso, _ = Curso.objects.get_or_create(
            nome=nome,
            defaults={
                "carga_horaria": carga,
                "valor_inscricao": valor,
                "status_curso": True,
            }
        )
        cursos.append(curso)

    print(f"Cursos inseridos: {len(cursos)}")

    #criar matrículas aleatórias
    status_choices = ["pago", "pendente"]
    total_matriculas = 0

    for _ in range(25):
        aluno = random.choice(alunos)
        curso = random.choice(cursos)

        status = random.choice(status_choices)

        valor_pago = curso.valor_inscricao if status == "pago" else random.choice([0, 0, 0, 50, 100])

        data_matricula = date.today() - timedelta(days=random.randint(0, 120))

        _, created = Matricula.objects.get_or_create(
            aluno=aluno,
            curso=curso,
            defaults={
                "status_pagamento": status,
                "valor_pago": valor_pago,
                "data_matricula": data_matricula,
            }
        )

        if created:
            total_matriculas += 1

    print(f"Matrículas inseridas: {total_matriculas}")


if __name__ == "__main__":
    run()
