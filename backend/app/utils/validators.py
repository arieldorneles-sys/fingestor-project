import re
from typing import Optional


def validate_cpf(cpf: str) -> bool:
    """Valida CPF brasileiro"""
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit1 = 11 - (sum1 % 11)
    if digit1 >= 10:
        digit1 = 0
    
    # Calcula segundo dígito verificador
    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit2 = 11 - (sum2 % 11)
    if digit2 >= 10:
        digit2 = 0
    
    # Verifica se os dígitos calculados conferem
    return cpf[-2:] == f"{digit1}{digit2}"


def validate_cnpj(cnpj: str) -> bool:
    """Valida CNPJ brasileiro"""
    # Remove caracteres não numéricos
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        return False
    
    # Calcula primeiro dígito verificador
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
    digit1 = 11 - (sum1 % 11)
    if digit1 >= 10:
        digit1 = 0
    
    # Calcula segundo dígito verificador
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
    digit2 = 11 - (sum2 % 11)
    if digit2 >= 10:
        digit2 = 0
    
    # Verifica se os dígitos calculados conferem
    return cnpj[-2:] == f"{digit1}{digit2}"


def validate_document(document: str) -> bool:
    """Valida CPF ou CNPJ"""
    document = re.sub(r'[^0-9]', '', document)
    
    if len(document) == 11:
        return validate_cpf(document)
    elif len(document) == 14:
        return validate_cnpj(document)
    else:
        return False


def validate_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Valida formato de telefone brasileiro"""
    # Remove caracteres não numéricos
    phone = re.sub(r'[^0-9]', '', phone)
    
    # Verifica se tem 10 ou 11 dígitos (com DDD)
    return len(phone) in [10, 11]


def format_document(document: str) -> str:
    """Formata CPF ou CNPJ para exibição"""
    document = re.sub(r'[^0-9]', '', document)
    
    if len(document) == 11:  # CPF
        return f"{document[:3]}.{document[3:6]}.{document[6:9]}-{document[9:]}"
    elif len(document) == 14:  # CNPJ
        return f"{document[:2]}.{document[2:5]}.{document[5:8]}/{document[8:12]}-{document[12:]}"
    else:
        return document


def format_phone(phone: str) -> str:
    """Formata telefone para exibição"""
    phone = re.sub(r'[^0-9]', '', phone)
    
    if len(phone) == 10:  # Telefone fixo
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    elif len(phone) == 11:  # Celular
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    else:
        return phone

