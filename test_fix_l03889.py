#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a correção do problema específico com L03889
"""

import os
import tempfile
import re
from file_renamer import FileRenamer

def test_fix_l03889():
    """
    Testa a correção do problema com L03889
    """
    print("=== Teste da correção do problema com L03889 ===\n")
    
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
    
    # Simula a lógica de renomeação JPG
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
        files_found = []
        for root, dirs, files in os.walk(aits_dir):
            for file in files:
                files_found.append(file)
                print(f"  - {file}")
        
        # Verifica se o arquivo foi renomeado corretamente
        expected_filename = "0003889000011pfb.jpg"
        if expected_filename in files_found:
            print(f"\n✅ SUCESSO: Arquivo renomeado corretamente para {expected_filename}")
            return True
        elif len(files_found) > 0:
            print(f"\n❌ FALHA: Arquivo não foi renomeado corretamente. Arquivo atual: {files_found[0]}")
            return False
        else:
            print(f"\n❌ FALHA: Nenhum arquivo encontrado após renomeação")
            return False

if __name__ == "__main__":
    test_fix_l03889()