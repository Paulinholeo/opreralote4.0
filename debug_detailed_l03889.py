#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script detalhado para debugar o problema específico com L03889
"""

import os
import re

def debug_detailed_l03889():
    """
    Debug detalhado do problema com L03889
    """
    print("=== Debug detalhado do problema com L03889 ===\n")
    
    # Parâmetros do caso problemático
    old_name_number = "03889"
    new_name_number = "03889"
    new_number_padded = "0003889"
    old_number_trimmed = "3889"
    
    # Arquivo problemático da saída do terminal
    problematic_file = "0003889889000011pfb.jpg"
    file_name_without_ext = os.path.splitext(problematic_file)[0]
    
    print(f"old_name_number: {old_name_number}")
    print(f"new_name_number: {new_name_number}")
    print(f"new_number_padded: {new_number_padded}")
    print(f"old_number_trimmed: {old_number_trimmed}")
    print(f"file_name_without_ext: {file_name_without_ext}")
    
    # Procura por sequências de 5 ou mais dígitos
    digit_sequences = re.findall(r'\d{5,}', file_name_without_ext)
    print(f"\nSequências de 5+ dígitos encontradas: {digit_sequences}")
    
    # Analisa cada sequência
    for seq in digit_sequences:
        print(f"\nAnalisando sequência: '{seq}'")
        seq_trimmed = seq.lstrip('0')
        print(f"  seq_trimmed: '{seq_trimmed}'")
        
        # Verifica se contém o número do lote
        if old_number_trimmed in seq_trimmed:
            print(f"  ✅ Contém old_number_trimmed ('{old_number_trimmed}')")
            
            # Encontra posição
            pos_in_seq = seq_trimmed.find(old_number_trimmed)
            print(f"  Posição em seq_trimmed: {pos_in_seq}")
            
            # Calcula posição real
            real_pos = len(seq) - len(seq_trimmed) + pos_in_seq
            print(f"  Posição real em seq: {real_pos}")
            
            # Partes
            prefix_part = seq[:real_pos]
            suffix_part = seq[real_pos + len(old_number_trimmed):]
            print(f"  prefix_part: '{prefix_part}'")
            print(f"  suffix_part: '{suffix_part}'")
            
            # Nova sequência
            new_seq = prefix_part + new_number_padded + suffix_part
            print(f"  new_seq: '{new_seq}'")
            
            # Substituição no nome do arquivo
            new_file_name_without_ext = file_name_without_ext.replace(seq, new_seq, 1)
            print(f"  new_file_name_without_ext: '{new_file_name_without_ext}'")
        else:
            print(f"  ❌ Não contém old_number_trimmed ('{old_number_trimmed}')")

if __name__ == "__main__":
    debug_detailed_l03889()