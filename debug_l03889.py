#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debugar o problema específico com L03889
"""

import os
import tempfile
import re
from file_renamer import FileRenamer

def debug_l03889():
    """
    Debug do problema com L03889
    """
    print("=== Debug do problema com L03889 ===\n")
    
    # Parâmetros do caso problemático
    old_name = "L03889"
    new_name = "L03889"
    
    # Arquivo problemático da saída do terminal
    problematic_file = "0003889889000011pfb.jpg"
    
    print(f"old_name: {old_name}")
    print(f"new_name: {new_name}")
    print(f"Arquivo problemático: {problematic_file}")
    
    # Extrai números
    old_name_number = old_name[1:] if old_name.startswith('L') else old_name
    new_name_number = new_name[1:] if new_name.startswith('L') else new_name
    
    print(f"old_name_number: {old_name_number}")
    print(f"new_name_number: {new_name_number}")
    
    # Verifica se os números são diferentes
    old_number_trimmed = old_name_number.lstrip('0')
    new_number_trimmed = new_name_number.lstrip('0')
    numbers_are_different = old_number_trimmed != new_number_trimmed or old_name_number != new_name_number
    
    print(f"old_number_trimmed: {old_number_trimmed}")
    print(f"new_number_trimmed: {new_number_trimmed}")
    print(f"numbers_are_different: {numbers_are_different}")
    print(f"old_name == new_name: {old_name == new_name}")
    
    # Análise do arquivo problemático
    base_filename = os.path.basename(problematic_file)
    file_ext = os.path.splitext(base_filename)[1]
    file_name_without_ext = os.path.splitext(base_filename)[0]
    
    print(f"\nAnálise do arquivo:")
    print(f"base_filename: {base_filename}")
    print(f"file_ext: {file_ext}")
    print(f"file_name_without_ext: {file_name_without_ext}")
    
    # Verifica se deve renomear o arquivo
    print(f"\n=== VERIFICAÇÃO DE RENOMEAÇÃO ===")
    
    # Verifica se o arquivo deve ser renomeado
    should_rename = False
    
    # Verifica se o arquivo contém o número antigo
    if old_name_number in file_name_without_ext:
        should_rename = True
        print(f"✅ Contém old_name_number ({old_name_number})")
    else:
        print(f"❌ NÃO contém old_name_number ({old_name_number})")
        
    # Verifica padrões numéricos equivalentes
    old_number_trimmed = old_name_number.lstrip('0')
    if old_number_trimmed in file_name_without_ext:
        # Verifica se a sequência encontrada representa o mesmo número
        found_sequences = re.findall(r'\d+', file_name_without_ext)
        for seq in found_sequences:
            seq_trimmed = seq.lstrip('0')
            # Verifica se o número antigo está no início da sequência encontrada
            if seq_trimmed.startswith(old_number_trimmed) and len(seq) >= 5:
                should_rename = True
                print(f"✅ Sequência '{seq}' corresponde ao padrão")
                break
        else:
            print(f"❌ Sequências encontradas não correspondem ao padrão: {found_sequences}")
    
    # Verifica padrão específico para JPG
    if file_ext.lower() == '.jpg':
        # Procura por sequências de 5 ou mais dígitos
        digit_sequences = re.findall(r'\d{5,}', file_name_without_ext)
        print(f"Sequências numéricas encontradas: {digit_sequences}")
        
        # Verifica se alguma sequência começa com o número antigo
        for seq in digit_sequences:
            seq_trimmed = seq.lstrip('0')
            if seq_trimmed.startswith(old_number_trimmed):
                should_rename = True
                print(f"✅ Sequência JPG '{seq}' começa com o número antigo")
                break
        else:
            print(f"❌ Nenhuma sequência JPG corresponde ao padrão")
    
    print(f"\nResultado: {'DEVE RENOMEAR' if should_rename else 'NÃO DEVE RENOMEAR'}")
    
    # Simula a lógica de renomeação JPG
    if should_rename and file_ext.lower() == '.jpg':
        print(f"\n=== SIMULAÇÃO DE RENOMEAÇÃO JPG ===")
        
        # Cria uma instância do FileRenamer para testar
        with tempfile.TemporaryDirectory() as temp_dir:
            # Cria estrutura de teste
            lote_dir = os.path.join(temp_dir, "L03889")
            subdir = os.path.join(lote_dir, "0003889")
            aits_dir = os.path.join(subdir, "AITs")
            os.makedirs(aits_dir, exist_ok=True)
            
            # Cria o arquivo problemático
            test_file_path = os.path.join(aits_dir, problematic_file)
            with open(test_file_path, "w") as f:
                f.write("fake jpg content")
            
            print(f"Estrutura de teste criada em: {temp_dir}")
            
            # Cria instância do FileRenamer
            renamer = FileRenamer(temp_dir)
            
            # Tenta renomear o arquivo usando a função específica
            print(f"\nTentando renomear usando _rename_jpg_file...")
            result = renamer._rename_jpg_file(test_file_path, old_name_number, new_name_number)
            print(f"Resultado da renomeação: {result}")
            
            # Verifica o estado após a tentativa
            print(f"\nArquivos após tentativa de renomeação:")
            for root, dirs, files in os.walk(aits_dir):
                for file in files:
                    print(f"  - {file}")

if __name__ == "__main__":
    debug_l03889()