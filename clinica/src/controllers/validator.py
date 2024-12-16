import re
from datetime import datetime

class Validator:
    @staticmethod
    def validate_cpf(cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
            
        # Validação do primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        if int(cpf[9]) != digito1:
            return False
            
        # Validação do segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        return int(cpf[10]) == digito2

    @staticmethod
    def validate_phone(phone):
        phone = ''.join(filter(str.isdigit, phone))
        return len(phone) >= 10 and len(phone) <= 11 and phone.isdigit()

    @staticmethod
    def validate_cro(cro):
        cro = cro.upper().strip()
        pattern = r'^[A-Z]{2}-\d{5}$'
        return bool(re.match(pattern, cro))

    @staticmethod
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
