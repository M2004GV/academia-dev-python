import os
import django
import random
from datetime import date, timedelta
from validate_docbr import CPF

# Configura o Django para rodar fora do manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from escola.models import Aluno, Curso, Matricula


def run():
    # Inicializa o gerador de CPF
    cpf_generator = CPF()

    # criar alunos
    alunos_data = [
        ("Pedro Alcântara", "pedro.alcantara@teste.com"),
        ("Quitéria Chagas", "quiteria@teste.com"),
        ("Ricardo Oliveira", "ricardo.oliveira@teste.com"),
        ("Sandra Lima", "sandra.lima@teste.com"),
        ("Thiago Monteiro", "thiago.monteiro@teste.com"),
        ("Ulisses Guimarães", "ulisses@teste.com"),
        ("Vanessa Camargo", "vanessa@teste.com"),
        ("William Bonner", "william@teste.com"),
        ("Ximena Morales", "ximena@teste.com"),
        ("Yuri Martins", "yuri@teste.com"),
        ("Zélia Duncan", "zelia@teste.com"),
        ("Amanda Nunes", "amanda.nunes@teste.com"),
        ("Beto Falcão", "beto@teste.com"),
        ("Camila Pitanga", "camila@teste.com"),
        ("Diego Ribas", "diego.ribas@teste.com"),
    ]

    alunos = []
    for nome, email in alunos_data:
        cpf_valido = cpf_generator.generate()

        aluno, created = Aluno.objects.get_or_create(
            email=email,
            defaults={"nome": nome, "cpf": cpf_valido},
        )
        alunos.append(aluno)

        if created:
            print(f"{nome} criado com CPF: {cpf_valido}")
        else:
            print(f"{nome} já existia")

    print(f"\n Total de alunos no banco: {len(alunos)}")

    # criar cursos
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
        curso, created = Curso.objects.get_or_create(
            nome=nome,
            defaults={
                "carga_horaria": carga,
                "valor_inscricao": valor,
                "status_curso": True,
            }
        )
        cursos.append(curso)

        if created:
            print(f"✓ Curso '{nome}' criado")
        else:
            print(f"→ Curso '{nome}' já existia")

    print(f"\n Total de cursos no banco: {len(cursos)}")

    # criar matrículas aleatórias
    status_choices = ["pago", "pendente"]
    total_matriculas = 0

    print("\n Gerando matrículas...")
    for _ in range(25):
        aluno = random.choice(alunos)
        curso = random.choice(cursos)
        status = random.choice(status_choices)

        # Lógica de valor pago
        if status == "pago":
            valor_pago = curso.valor_inscricao
        else:
            valor_pago = 0

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

    print(f"\nMatrículas novas inseridas: {total_matriculas}")
    print(f"Total de matrículas no banco: {Matricula.objects.count()}")


if __name__ == "__main__":
    run()