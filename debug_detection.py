#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de debug para entender a lógica de detecção de arquivos JPG
"""

import re

def debug_detection():
    """
    Debug da lógica de detecção de arquivos JPG
    """
    print("=== Debug da lógica de detecção de arquivos JPG ===\n")
    
    # Parâmetros do caso problemático
    old_name = "0010637"
    new_name = "10637"
    filename = "0010637000017a.jpg"
    
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
    
    # Análise do arquivo
    base_filename = filename
    file_ext = ".jpg"
    file_name_without_ext = "0010637000017a"
    
    print(f"\nAnalisando arquivo: {filename}")
    print(f"base_filename: {base_filename}")
    print(f"file_ext: {file_ext}")
    print(f"file_name_without_ext: {file_name_without_ext}")
    
    # Verifica padrões numéricos específicos primeiro, especialmente para JPG
    if file_ext.lower() == '.jpg':
        # Procura por padrões numéricos no nome do arquivo JPG
        # Procura por sequências de 5 ou mais dígitos
        digit_sequences = re.findall(r'\d{5,}', file_name_without_ext)
        print(f"\nSequências numéricas encontradas: {digit_sequences}")
        
        # Verifica se alguma sequência corresponde ao padrão do old_name_number
        contains_old_number = False
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
                    contains_old_number = True
                    break
                else:
                    print(f"    ❌ seq_trimmed.startswith(old_number_trimmed) = False")
            elif (seq == old_name_number or 
                seq_trimmed == old_number_trimmed or
                seq == old_name_number.lstrip('0').zfill(6) or 
                seq == old_name_number.lstrip('0').zfill(7)):
                print(f"    ✅ Sequência corresponde ao padrão")
                contains_old_number = True
                break
            else:
                print(f"    ❌ Sequência NÃO corresponde ao padrão")
            
            # Verificação adicional para casos onde old_name == new_name
            # mas os números têm formatos diferentes
            if old_name == new_name and numbers_are_different:
                print(f"    Verificação adicional: old_name == new_name e numbers_are_different")
                # Verifica se a sequência contém o número antigo em qualquer posição
                if old_number_trimmed in seq_trimmed:
                    print(f"    ✅ old_number_trimmed in seq_trimmed = True")
                    contains_old_number = True
                    break
                else:
                    print(f"    ❌ old_number_trimmed in seq_trimmed = False")
        
        print(f"\nResultado final da detecção: contains_old_number = {contains_old_number}")

if __name__ == "__main__":
    debug_detection()