from django.core.exceptions import ValidationError

# Funções de validação customizadas para CPF e telefone

def validar_cpf(cpf: str):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.")

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    if digito1 >= 10:
        digito1 = 0

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    if digito2 >= 10:
        digito2 = 0

    if cpf[-2:] != f"{digito1}{digito2}":
        raise ValidationError("CPF inválido.")

def validar_telefone(telefone: str) -> bool:
    telefone = ''.join(filter(str.isdigit, telefone))
    # Celular: 11 dígitos, começa com 9 após o DDD
    if len(telefone) == 11 and telefone[2] == '9':
        return True
    # Fixo: 10 dígitos, não começa com 9 após o DDD
    elif len(telefone) == 10 and telefone[2] != '9':
        return True
    else:
        return False

def telefone_validator(telefone: str):
    if not validar_telefone(telefone):
        raise ValidationError("Número de telefone inválido.")