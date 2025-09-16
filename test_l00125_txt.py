#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para renomeação do arquivo L00125.txt
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_l00125_txt_rename():
    """
    Testa a renomeação específica do arquivo L00125.txt
    """
    print("=== Teste de Renomeação L00125.txt ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_l00125_")
    
    try:
        # Cria estrutura: L05454/0000125/AITs/L00125.txt (depois da reorganização)
        lote_dir = os.path.join(test_dir, "L05454")
        subdir = os.path.join(lote_dir, "05454")  # Após reorganização
        aits_dir = os.path.join(subdir, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria o arquivo problemático
        problem_file = os.path.join(aits_dir, "L00125.txt")
        with open(problem_file, "w") as f:
            f.write("0000125;BRI1306/2023;20250905;14:49:38;2;000;000,0;00125000070a.jpg;00125000070b.jpg;001306;Test Location;5673")
        
        # Cria outros arquivos para contexto
        other_files = [
            os.path.join(aits_dir, "0000125000070a.jpg"),
            os.path.join(aits_dir, "0000125000070b.jpg"),
            os.path.join(subdir, "0000125.txt")
        ]
        
        for file_path in other_files:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write("test content")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Estrutura antes da renomeação:")
        print_structure(test_dir)
        
        # Testa a renomeação
        file_renamer = FileRenamer(test_dir)
        
        print(f"\nExecutando renomeação de arquivos...")
        print("Simulando: old_name='L0000125', new_name='L05454'")
        
        # Simula os parâmetros que chegam na função
        old_name = "L0000125"  # Nome original do lote
        new_name = "L05454"    # Nome novo do lote
        
        # Calcula os números como a função faz
        old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
        new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
        
        print(f"old_name_number: '{old_name_number}'")
        print(f"new_name_number: '{new_name_number}'")
        
        # Verifica detecção do arquivo problemático
        print(f"\nVerificando detecção do arquivo 'L00125.txt':")
        test_filename = "L00125.txt"
        
        # Testa as condições de detecção
        if old_name_number in test_filename:
            print(f"✓ Detecção direta: '{old_name_number}' encontrado em '{test_filename}'")
        elif len(old_name_number) >= 6 and old_name_number.startswith('00'):
            old_number_trimmed = old_name_number.lstrip('0')
            if f"L{old_number_trimmed.zfill(5)}" in test_filename or f"L00{old_number_trimmed}" in test_filename:
                print(f"✓ Detecção por padrão: L00{old_number_trimmed} detectado em '{test_filename}'")
            else:
                print(f"✗ Padrão L00{old_number_trimmed} NÃO detectado em '{test_filename}'")
        else:
            print(f"✗ Arquivo '{test_filename}' NÃO será detectado")
        
        # Executa a função
        file_renamer.rename_files(old_name, new_name)
        
        print(f"\nEstrutura após renomeação:")
        print_structure(test_dir)
        
        # Verifica se o arquivo foi renomeado
        expected_new_name = f"L{new_name_number}.txt"
        expected_path = os.path.join(aits_dir, expected_new_name)
        
        if os.path.exists(expected_path):
            print(f"\n✅ SUCESSO: Arquivo renomeado para '{expected_new_name}'")
        elif os.path.exists(problem_file):
            print(f"\n⚠ AVISO: Arquivo original ainda existe (não foi renomeado)")
        else:
            # Procura por qualquer arquivo .txt no diretório AITs
            txt_files = [f for f in os.listdir(aits_dir) if f.endswith('.txt')]
            if txt_files:
                print(f"\n? Arquivos .txt encontrados: {txt_files}")
            else:
                print(f"\n✗ ERRO: Nenhum arquivo .txt encontrado")
                
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

def print_structure(directory, indent=""):
    """
    Imprime a estrutura de diretórios
    """
    if not os.path.exists(directory):
        return
        
    items = sorted(os.listdir(directory))
    for item in items:
        item_path = os.path.join(directory, item)
        print(f"{indent}├── {item}")
        if os.path.isdir(item_path):
            print_structure(item_path, indent + "│   ")

if __name__ == "__main__":
    test_l00125_txt_rename()