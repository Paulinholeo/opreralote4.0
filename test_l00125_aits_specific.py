#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para o problema do arquivo L00125.txt no diretório AITs
Simula exatamente: D:\Brascontrol\Opera_lote_4.0\L08421\0000125\AITs\L00125.txt
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_l00125_aits_specific():
    """
    Teste específico para L00125.txt em AITs que não está sendo renomeado
    """
    print("=== Teste Específico L00125.txt em AITs ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_l00125_aits_")
    
    try:
        # Simula estrutura EXATA do problema: L08421\0000125\AITs\L00125.txt
        lote_dir = os.path.join(test_dir, "L08421")
        subdir = os.path.join(lote_dir, "0000125")
        aits_dir = os.path.join(subdir, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria o arquivo problemático
        problem_file = os.path.join(aits_dir, "L00125.txt")
        with open(problem_file, "w") as f:
            f.write("0000125;BRI3002/2023;20250907;13:44:33;1;110;121,0;test")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Estrutura ANTES:")
        print_structure(test_dir)
        
        # Vamos analisar passo a passo o que acontece
        file_renamer = FileRenamer(test_dir)
        
        print(f"\n{'='*60}")
        print(f"TESTE: Renomeando L08421 (que já existe) simulando o processo real")
        print(f"old_name: L08421")
        print(f"new_name: L08421")
        print(f"{'='*60}")
        
        old_name = "L08421"
        new_name = "L08421"
        
        # Extraindo a lógica do file_renamer para debug
        old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
        new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
        
        print(f"old_name_number: '{old_name_number}'")
        print(f"new_name_number: '{new_name_number}'")
        
        # Define os diretórios onde procurar arquivos
        search_directories = [os.path.join(test_dir, new_name)]
        
        # Se há estrutura com AITs, adiciona os subdiretórios à busca
        main_dir = os.path.join(test_dir, new_name)
        if os.path.exists(main_dir):
            for item in os.listdir(main_dir):
                item_path = os.path.join(main_dir, item)
                if os.path.isdir(item_path):
                    search_directories.append(item_path)
                    # Adiciona também subdiretórios de AITs se existirem
                    aits_path = os.path.join(item_path, 'AITs')
                    if os.path.exists(aits_path):
                        search_directories.append(aits_path)
        
        print(f"\nDiretórios de busca encontrados:")
        for search_dir in search_directories:
            print(f"  - {search_dir}")
        
        # Vamos testar especificamente o arquivo problema
        problem_file_rel = os.path.relpath(problem_file, test_dir)
        base_filename = os.path.basename(problem_file)
        file_ext = os.path.splitext(base_filename)[1]
        file_name_without_ext = os.path.splitext(base_filename)[0]
        
        print(f"\n=== ANÁLISE DO ARQUIVO PROBLEMA ===")
        print(f"Arquivo: {problem_file_rel}")
        print(f"base_filename: '{base_filename}'")
        print(f"file_name_without_ext: '{file_name_without_ext}'")
        print(f"file_ext: '{file_ext}'")
        
        # Testando as condições de detecção
        contains_old_number = False
        processed_by_special_logic = False
        
        print(f"\n=== TESTANDO CONDIÇÕES DE DETECÇÃO ===")
        
        # Condição 1: old_name_number in base_filename
        condition1 = old_name_number in base_filename
        print(f"Condição 1 - '{old_name_number}' in '{base_filename}': {condition1}")
        if condition1:
            contains_old_number = True
        
        # Condição 2: padrão L00XXX quando old_name_number começa com 00
        if not contains_old_number and len(old_name_number) >= 6 and old_name_number.startswith('00'):
            old_number_trimmed = old_name_number.lstrip('0')
            pattern1 = f"L{old_number_trimmed.zfill(5)}"
            pattern2 = f"L00{old_number_trimmed}"
            condition2a = pattern1 in base_filename
            condition2b = pattern2 in base_filename
            condition2 = condition2a or condition2b
            print(f"Condição 2a - '{pattern1}' in '{base_filename}': {condition2a}")
            print(f"Condição 2b - '{pattern2}' in '{base_filename}': {condition2b}")
            print(f"Condição 2 (qualquer): {condition2}")
            if condition2:
                contains_old_number = True
                processed_by_special_logic = True
        
        # Condição 3: old_name tem L e arquivo contém número
        if not contains_old_number and old_name.startswith('L'):
            parts_check = [old_name_number, old_name_number.lstrip('0')]
            condition3_parts = [part in base_filename for part in parts_check]
            condition3 = any(condition3_parts)
            print(f"Condição 3 - old_name tem L e partes {parts_check} in '{base_filename}': {condition3_parts} -> {condition3}")
            if condition3:
                contains_old_number = True
        
        # Condição 4: arquivo .txt sem L quando new_name tem L
        if not contains_old_number:
            condition4_checks = [
                file_ext == '.txt',
                new_name.startswith('L'),
                not file_name_without_ext.startswith('L'),
                file_name_without_ext == new_name[1:]
            ]
            condition4 = all(condition4_checks)
            print(f"Condição 4 - arquivo .txt sem L: {condition4_checks} -> {condition4}")
            if condition4:
                contains_old_number = True
                processed_by_special_logic = True
        
        # Condição 5: arquivo L00125.txt específico
        if not contains_old_number:
            condition5 = file_name_without_ext == 'L00125' and file_ext == '.txt'
            print(f"Condição 5 - arquivo L00125.txt específico: {condition5}")
            if condition5:
                contains_old_number = True
                processed_by_special_logic = True
        
        print(f"\n=== RESULTADO DA DETECÇÃO ===")
        print(f"contains_old_number: {contains_old_number}")
        print(f"processed_by_special_logic: {processed_by_special_logic}")
        
        if contains_old_number:
            print(f"\n✅ ARQUIVO SERIA DETECTADO para renomeação!")
            
            # Simula a lógica de renomeação
            new_file_name_without_ext = file_name_without_ext
            
            # Casos especiais para arquivos com padrão "L00125"
            if file_name_without_ext.startswith('L00') and len(file_name_without_ext) >= 6:
                new_file_name_without_ext = f"L{new_name_number}"
                print(f"  - Aplicando caso especial L00XXX: '{file_name_without_ext}' -> '{new_file_name_without_ext}'")
            
            new_filename_expected = new_file_name_without_ext + file_ext
            print(f"  - Nome esperado após renomeação: '{new_filename_expected}'")
        else:
            print(f"\n❌ ARQUIVO NÃO SERIA DETECTADO - Esse é o problema!")
        
        print(f"\n{'='*60}")
        print(f"EXECUTANDO RENOMEAÇÃO REAL...")
        print(f"{'='*60}")
        
        # Executa a renomeação real
        file_renamer.rename_files(old_name, new_name)
        
        print(f"\nEstrutura APÓS renomeação:")
        print_structure(test_dir)
        
        # Verifica se o arquivo foi renomeado
        aits_files_after = []
        if os.path.exists(aits_dir):
            aits_files_after = os.listdir(aits_dir)
        
        print(f"\nArquivos no diretório AITs após renomeação:")
        for file in aits_files_after:
            print(f"  - {file}")
        
        if 'L08421.txt' in aits_files_after:
            print(f"\n✅ SUCESSO: Arquivo foi renomeado para L08421.txt!")
        elif 'L00125.txt' in aits_files_after:
            print(f"\n❌ PROBLEMA: Arquivo ainda se chama L00125.txt (não foi renomeado)")
        else:
            print(f"\n❓ RESULTADO INESPERADO: Não encontrei nem L00125.txt nem L08421.txt")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

def print_structure(directory, indent=""):
    """
    Imprime estrutura detalhada
    """
    if not os.path.exists(directory):
        return
        
    items = sorted(os.listdir(directory))
    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            print(f"{indent}📄 {item}")
        else:
            print(f"{indent}📁 {item}/")
            print_structure(item_path, indent + "  ")

if __name__ == "__main__":
    test_l00125_aits_specific()