#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debugar o problema de substituição em detalhes
"""

import re

def debug_detailed():
    """
    Debug detalhado da lógica de substituição
    """
    print("=== Debug detalhado da lógica de substituição ===\n")
    
    # Parâmetros do caso problemático
    old_name = "L00126"
    new_name = "L00126"
    file_name_without_ext = "00126000132a"
    
    old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
    new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
    
    # Extrai os números para comparação
    old_number_trimmed = old_name_number.lstrip('0')
    new_number_trimmed = new_name_number.lstrip('0')
    
    # Verifica se os números são realmente diferentes
    numbers_are_different = old_number_trimmed != new_number_trimmed or old_name_number != new_name_number
    
    print(f"old_name: {old_name}")
    print(f"new_name: {new_name}")
    print(f"old_name_number: {old_name_number}")
    print(f"new_name_number: {new_name_number}")
    print(f"old_number_trimmed: {old_number_trimmed}")
    print(f"new_number_trimmed: {new_number_trimmed}")
    print(f"numbers_are_different: {numbers_are_different}")
    print(f"old_name == new_name: {old_name == new_name}")
    print(f"file_name_without_ext: {file_name_without_ext}")
    
    # Procura por padrões numéricos no nome do arquivo JPG
    # Procura por sequências de 5 ou mais dígitos
    digit_sequences = re.findall(r'\d{5,}', file_name_without_ext)
    print(f"\nSequências numéricas encontradas: {digit_sequences}")
    
    # Verifica se alguma sequência corresponde ao padrão do old_name_number
    for seq in digit_sequences:
        # Verifica se a sequência corresponde ao padrão do old_name_number
        # Por exemplo, se old_name_number é "00126", procuramos por "00126" ou "000126"
        old_number_trimmed = old_name_number.lstrip('0')
        seq_trimmed = seq.lstrip('0')
        
        print(f"\n  Analisando sequência: '{seq}'")
        print(f"    old_number_trimmed: '{old_number_trimmed}'")
        print(f"    seq_trimmed: '{seq_trimmed}'")
        
        # Verificação para casos onde old_name == new_name
        # mas os números têm formatos diferentes
        if old_name == new_name and numbers_are_different:
            print(f"    Caso especial: old_name == new_name e numbers_are_different")
            # Neste caso, estamos padronizando números, então precisamos verificar
            # se a sequência começa com o número antigo (sem zeros à esquerda)
            if seq_trimmed.startswith(old_number_trimmed):
                print(f"    ✅ seq_trimmed.startswith(old_number_trimmed) = True")
            else:
                print(f"    ❌ seq_trimmed.startswith(old_number_trimmed) = False")
        elif (seq == old_name_number or 
            seq_trimmed == old_number_trimmed or
            seq == old_name_number.lstrip('0').zfill(6) or 
            seq == old_name_number.lstrip('0').zfill(7)):
            print(f"    ✅ Sequência corresponde ao padrão")
        else:
            print(f"    ❌ Sequência NÃO corresponde ao padrão")
        
        # CORREÇÃO ADICIONAL: Verificação mais abrangente para casos onde old_name == new_name
        # mas os números têm formatos diferentes
        if old_name == new_name and numbers_are_different:
            print(f"    Verificação adicional: old_name == new_name e numbers_are_different")
            # Verifica se a sequência contém o número antigo em qualquer posição
            if old_number_trimmed in seq_trimmed:
                print(f"    ✅ old_number_trimmed in seq_trimmed = True")
            else:
                print(f"    ❌ old_number_trimmed in seq_trimmed = False")
        
        # Verificação específica do problema: old_name_number in seq
        if old_name_number in seq:
            print(f"    ✅ old_name_number in seq = True")
            # Substitui apenas a parte que corresponde ao número do lote
            old_pos = file_name_without_ext.find(seq)
            seq_pos_in_seq = seq.find(old_name_number)
            print(f"    old_pos: {old_pos}")
            print(f"    seq_pos_in_seq: {seq_pos_in_seq}")
            
            if old_pos != -1 and seq_pos_in_seq != -1:
                # Substitui apenas a parte correspondente ao número do lote
                # CORREÇÃO: Usa o número correto com 7 dígitos
                # O novo número deve ser new_name_number padronizado para 7 dígitos
                correct_new_number = new_name_number.zfill(7)
                print(f"    correct_new_number: {correct_new_number}")
                
                # Calcula a parte restante após o número do lote
                rest_part = seq[seq_pos_in_seq + len(old_name_number):]
                print(f"    rest_part: '{rest_part}'")
                
                # Cria o novo padrão: novo número com 7 dígitos + parte restante
                new_seq = correct_new_number + rest_part
                print(f"    new_seq: '{new_seq}'")
                
                new_file_name_without_ext = (
                    file_name_without_ext[:old_pos] + 
                    new_seq + 
                    file_name_without_ext[old_pos + len(seq):]
                )
                print(f"    new_file_name_without_ext: '{new_file_name_without_ext}'")
                
                # Verifica o resultado
                expected = "0000126000132a"
                print(f"    Esperado: '{expected}'")
                print(f"    Correto? {new_file_name_without_ext == expected}")
        else:
            print(f"    ❌ old_name_number in seq = False")

if __name__ == "__main__":
    debug_detailed()