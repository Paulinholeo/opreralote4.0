#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a correção do problema específico com L03889 na função _update_jpg_filename
"""

import os
import sys
import tempfile
# Adiciona o diretório atual ao path para importar text_file_editor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from text_file_editor import TextFileEditor

def test_text_fix_l03889():
    """
    Testa a correção do problema com L03889 na função _update_jpg_filename
    """
    print("=== Teste da correção do problema com L03889 na função _update_jpg_filename ===\n")
    
    # Parâmetros do caso problemático
    old_name_number = "03889"
    new_name_number = "03889"
    
    # Arquivo problemático da saída do terminal
    problematic_filename = "0003889889000011pfb.jpg"
    
    print(f"old_name_number: {old_name_number}")
    print(f"new_name_number: {new_name_number}")
    print(f"Arquivo problemático: {problematic_filename}")
    
    # Cria instância do TextFileEditor
    with tempfile.TemporaryDirectory() as temp_dir:
        editor = TextFileEditor(temp_dir)
        
        # Testa a função _update_jpg_filename
        print(f"\n=== TESTANDO _update_jpg_filename ===")
        result = editor._update_jpg_filename(problematic_filename, old_name_number, new_name_number)
        print(f"Resultado da atualização: {result}")
        
        # Verifica se o resultado está correto
        expected_result = "0003889000011pfb.jpg"
        if result == expected_result:
            print(f"\n✅ SUCESSO: Arquivo atualizado corretamente para {expected_result}")
            return True
        else:
            print(f"\n❌ FALHA: Arquivo não foi atualizado corretamente.")
            print(f"  Esperado: {expected_result}")
            print(f"  Obtido:   {result}")
            return False

if __name__ == "__main__":
    test_text_fix_l03889()