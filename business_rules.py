def validate_person(data):
    if 'name' not in data or len(data['name']) == 0:
        return False, "O nome é obrigatório"
    if 'cpf_cnpj' not in data or len(data['cpf_cnpj']) < 11:
        return False, "CPF ou CNPJ inválido"
    # Outras validações...
    return True, "Validado com sucesso"


# business_rules.py

def validate_case(data):
    # Exemplo de validações simples
    if 'description' not in data or not data['description']:
        return False, "A descrição é obrigatória."

    if 'entry_date' not in data:
        return False, "A data de entrada é obrigatória."

    if 'status' not in data or data['status'] not in ['Open', 'Closed', 'Pending']:
        return False, "Status inválido. Deve ser 'Open', 'Closed' ou 'Pending'."

    if 'insurance_company_id' not in data:
        return False, "O ID da companhia de seguros é obrigatório."

    # Se todas as validações passarem
    return True, "Validação bem-sucedida."

