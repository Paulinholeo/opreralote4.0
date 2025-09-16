#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debugar o problema do text_file_editor
"""

import re

def debug_text_editor():
    """
    Debug da lógica do text_file_editor
    """
    print("=== Debug da lógica do text_file_editor ===\n")
    
    # Parâmetros do caso problemático
    old_name = "L00126"
    new_name = "L00126"
    old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
    new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
    
    # Campo problemático
    field_content = "00126000132b.jpg"
    
    print(f"old_name: {old_name}")
    print(f"new_name: {new_name}")
    print(f"old_name_number: {old_name_number}")
    print(f"new_name_number: {new_name_number}")
    print(f"field_content: {field_content}")
    
    # Remove prefixo '00' se existir
    if field_content.startswith('00'):
        field_content = field_content[2:]
        print(f"Após remover prefixo '00': {field_content}")
    
    # Verifica se o campo contém um nome de arquivo JPG
    if field_content.endswith('.jpg'):
        print("Campo contém nome de arquivo JPG")
        # Aplica a lógica de substituição para nomes de arquivos JPG
        # Procura por sequências de 5 ou mais dígitos
        digit_sequences = re.findall(r'\d{5,}', field_content)
        print(f"Sequências numéricas encontradas: {digit_sequences}")
        
        # Para cada sequência encontrada, verifica se corresponde ao padrão antigo
        for seq in sorted(digit_sequences, key=len, reverse=True):
            print(f"\nAnalisando sequência: '{seq}'")
            # Verifica se a sequência contém o número antigo
            old_number_trimmed = old_name_number.lstrip('0')
            seq_trimmed = seq.lstrip('0')
            
            print(f"  old_number_trimmed: '{old_number_trimmed}'")
            print(f"  seq_trimmed: '{seq_trimmed}'")
            
            if seq_trimmed.startswith(old_number_trimmed):
                print(f"  seq_trimmed.startswith(old_number_trimmed) = True")
                # Substitui apenas a parte que corresponde ao número do lote
                # Garantindo que o novo número tenha exatamente 7 dígitos
                correct_new_number = new_name_number.zfill(7)
                print(f"  correct_new_number: '{correct_new_number}'")
                # Calcula a parte restante após o número do lote
                # A parte restante é o que vem depois do número do lote na sequência
                rest_part = seq[len(old_number_trimmed):]
                print(f"  rest_part: '{rest_part}'")
                # Cria o novo padrão: novo número com 7 dígitos + parte restante
                new_seq = correct_new_number + rest_part
                print(f"  new_seq: '{new_seq}'")
                field_content = field_content.replace(seq, new_seq)
                print(f"  field_content após substituição: '{field_content}'")
                break  # Processa apenas a primeira sequência encontrada
            # Verifica também se a sequência inteira corresponde ao número do lote
            elif seq == old_name_number or seq_trimmed == old_number_trimmed:
                print(f"  Sequência corresponde exatamente ao número do lote")
                # Substitui a sequência inteira pelo novo número padronizado
                correct_new_number = new_name_number.zfill(7)
                field_content = field_content.replace(seq, correct_new_number)
                print(f"  field_content após substituição: '{field_content}'")
                break  # Processa apenas a primeira sequência encontrada
            else:
                print(f"  Sequência NÃO corresponde ao padrão")
    
    # Resultado esperado: "0000126000132b.jpg"
    expected = "0000126000132b.jpg"
    print(f"\nResultado obtido: '{field_content}'")
    print(f"Resultado esperado: '{expected}'")
    print(f"Correto? {field_content == expected}")

if __name__ == "__main__":
    debug_text_editor()