#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de debug para entender a lógica de substituição
"""

def debug_substitution():
    """
    Debug da lógica de substituição
    """
    print("=== Debug da lógica de substituição ===\n")
    
    # Parâmetros do caso problemático
    old_name = "0010637"
    new_name = "10637"
    filename = "0010637000003a.jpg"
    
    old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
    new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
    
    print(f"old_name: {old_name}")
    print(f"new_name: {new_name}")
    print(f"old_name_number: {old_name_number}")
    print(f"new_name_number: {new_name_number}")
    
    # Parâmetros para a substituição
    file_name_without_ext = "0010637000003a"
    seq = "0010637000003"
    old_name_number = "0010637"
    new_name_number = "10637"
    
    print(f"\nParâmetros para substituição:")
    print(f"file_name_without_ext: {file_name_without_ext}")
    print(f"seq: {seq}")
    print(f"old_name_number: {old_name_number}")
    print(f"new_name_number: {new_name_number}")
    
    # Verifica se old_name_number está em seq
    if old_name_number in seq:
        print(f"\nold_name_number '{old_name_number}' está contido em seq '{seq}'")
        
        # Calcula o novo número com 7 dígitos
        correct_new_number = new_name_number.zfill(7)
        print(f"correct_new_number: {correct_new_number}")
        
        # Faz a substituição
        new_seq = seq.replace(old_name_number, correct_new_number, 1)
        print(f"new_seq após substituição: {new_seq}")
        
        # Calcula a posição
        old_pos = file_name_without_ext.find(seq)
        seq_pos_in_seq = seq.find(old_name_number)
        print(f"old_pos: {old_pos}")
        print(f"seq_pos_in_seq: {seq_pos_in_seq}")
        
        if old_pos != -1 and seq_pos_in_seq != -1:
            # Substitui apenas a parte correspondente ao número do lote
            new_file_name_without_ext = (
                file_name_without_ext[:old_pos] + 
                new_seq + 
                file_name_without_ext[old_pos + len(seq):]
            )
            print(f"new_file_name_without_ext: {new_file_name_without_ext}")
            
            # Verifica se o resultado está correto
            expected = "00010637000003a"
            if new_file_name_without_ext == expected:
                print(f"✅ Resultado correto! Esperado: {expected}")
            else:
                print(f"❌ Resultado incorreto! Esperado: {expected}, Obtido: {new_file_name_without_ext}")
        else:
            print("❌ Não foi possível calcular as posições")
    else:
        print(f"old_name_number '{old_name_number}' NÃO está contido em seq '{seq}'")

if __name__ == "__main__":
    debug_substitution()