from validate_docbr import CPF
from django.core.exceptions import ValidationError

def validar_cpf(numero_cpf):
    cpf = CPF()
    if not cpf.validate(numero_cpf):
        raise ValidationError("CPF inválido.")
    return numero_cpf