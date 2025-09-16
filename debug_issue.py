#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debugar o problema de substituição
"""

def debug_substitution():
    """
    Debug da lógica de substituição
    """
    print("=== Debug da lógica de substituição ===\n")
    
    # Parâmetros do caso problemático
    old_name_number = "00126"
    new_name_number = "00126"
    file_name_without_ext = "00126000132a"
    seq = "00126000132"
    
    print(f"old_name_number: {old_name_number}")
    print(f"new_name_number: {new_name_number}")
    print(f"file_name_without_ext: {file_name_without_ext}")
    print(f"seq: {seq}")
    
    # Simula a lógica atual
    old_pos = file_name_without_ext.find(seq)
    seq_pos_in_seq = seq.find(old_name_number)
    
    print(f"\nold_pos: {old_pos}")
    print(f"seq_pos_in_seq: {seq_pos_in_seq}")
    
    if old_pos != -1 and seq_pos_in_seq != -1:
        # CORREÇÃO: Usa o número correto com 7 dígitos
        # O novo número deve ser new_name_number padronizado para 7 dígitos
        correct_new_number = new_name_number.zfill(7)
        print(f"correct_new_number: {correct_new_number}")
        
        # Calcula a parte restante após o número do lote
        rest_part = seq[seq_pos_in_seq + len(old_name_number):]
        print(f"rest_part: {rest_part}")
        
        # Cria o novo padrão: novo número com 7 dígitos + parte restante
        new_seq = correct_new_number + rest_part
        print(f"new_seq: {new_seq}")
        
        new_file_name_without_ext = (
            file_name_without_ext[:old_pos] + 
            new_seq + 
            file_name_without_ext[old_pos + len(seq):]
        )
        print(f"new_file_name_without_ext: {new_file_name_without_ext}")
        
        # O resultado esperado é "0000126000132a"
        expected = "0000126000132a"
        print(f"Esperado: {expected}")
        print(f"Obtido: {new_file_name_without_ext}")
        print(f"Correto? {new_file_name_without_ext == expected}")

if __name__ == "__main__":
    debug_substitution()