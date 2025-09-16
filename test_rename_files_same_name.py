#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para debugar o problema com rename_files quando old_name == new_name
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_rename_files_same_name():
    """
    Testa o problema específico com rename_files quando old_name == new_name
    """
    print("=== Teste rename_files com old_name == new_name ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_rename_same_")
    
    try:
        # Cria a estrutura exata do problema
        lote_dir = os.path.join(test_dir, "L08685")
        subdir_correct = os.path.join(lote_dir, "0008685")  # Diretório correto após correção
        aits_dir = os.path.join(subdir_correct, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria o arquivo problemático: L08685.txt que NÃO deve ser renomeado
        # quando old_name == new_name == "L08685"
        l08685_txt_path = os.path.join(aits_dir, "L08685.txt")
        with open(l08685_txt_path, "w", encoding='utf-8') as f:
            f.write("0008685;conteúdo;teste")
        
        print(f"Estrutura inicial:")
        print(f"Diretório base: {test_dir}")
        print_structure(test_dir)
        
        # Etapa 1: Simula exatamente o que acontece na GUI
        print(f"\n{'='*60}")
        print(f"ETAPA 1: Criando FileRenamer")
        print(f"{'='*60}")
        
        file_renamer = FileRenamer(test_dir)
        print(f"FileRenamer criado com diretório: {test_dir}")
        
        # Etapa 2: Executa rename_files com old_name == new_name
        print(f"\n{'='*60}")
        print(f"ETAPA 2: Executando rename_files('L08685', 'L08685')")
        print(f"{'='*60}")
        print(f"Este é o caso problemático onde old_name == new_name")
        print(f"O arquivo L08685.txt NÃO deveria ser renomeado para L0008685.txt")
        
        # Executa exatamente como na GUI
        file_renamer.rename_files("L08685", "L08685")
        
        print(f"\nEstrutura após rename_files:")
        print_structure(test_dir)
        
        # Etapa 3: Verifica o resultado
        print(f"\n{'='*60}")
        print(f"ETAPA 3: Verificando resultado")
        print(f"{'='*60}")
        
        # Verifica se o arquivo ainda existe com o nome correto
        expected_file = os.path.join(aits_dir, "L08685.txt")
        wrong_file = os.path.join(aits_dir, "L0008685.txt")
        
        if os.path.exists(expected_file):
            print(f"✅ ARQUIVO CORRETO EXISTE: {expected_file}")
        else:
            print(f"❌ ARQUIVO CORRETO NÃO EXISTE: {expected_file}")
            
        if os.path.exists(wrong_file):
            print(f"❌ ARQUIVO ERRADO FOI CRIADO: {wrong_file}")
            print(f"   Este é o problema! O arquivo foi renomeado incorretamente.")
        else:
            print(f"✅ ARQUIVO ERRADO NÃO EXISTE: {wrong_file}")
        
        # Etapa 4: Debug detalhado da lógica de detecção
        print(f"\n{'='*60}")
        print(f"ETAPA 4: Debug detalhado da lógica de detecção")
        print(f"{'='*60}")
        
        old_name = "L08685"
        new_name = "L08685"
        
        old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
        new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
        
        print(f"old_name: {old_name}")
        print(f"new_name: {new_name}")
        print(f"old_name_number: {old_name_number}")
        print(f"new_name_number: {new_name_number}")
        
        # Testa a detecção do arquivo problemático
        test_filename = "L08685.txt"
        base_filename = os.path.basename(test_filename)
        file_ext = os.path.splitext(base_filename)[1]
        file_name_without_ext = os.path.splitext(base_filename)[0]
        
        print(f"\nAnalisando arquivo: {test_filename}")
        print(f"base_filename: {base_filename}")
        print(f"file_ext: {file_ext}")
        print(f"file_name_without_ext: {file_name_without_ext}")
        
        # Verifica as condições de detecção
        contains_old_number = False
        processed_by_special_logic = False
        
        # Verifica se old_name_number está diretamente no nome do arquivo
        if old_name_number in file_name_without_ext:
            contains_old_number = True
            print(f"✓ old_name_number '{old_name_number}' encontrado diretamente em '{file_name_without_ext}'")
        else:
            print(f"✗ old_name_number '{old_name_number}' NÃO encontrado diretamente em '{file_name_without_ext}'")
        
        # Verifica padrões como "L00125" quando old_name_number é "0000125"
        if not contains_old_number and len(old_name_number) >= 6 and old_name_number.startswith('00'):
            old_number_trimmed = old_name_number.lstrip('0')
            if f"L{old_number_trimmed.zfill(5)}" in base_filename or f"L00{old_number_trimmed}" in base_filename:
                contains_old_number = True
                processed_by_special_logic = True
                print(f"✓ Padrão L00{old_number_trimmed} encontrado em '{base_filename}'")
            else:
                print(f"✗ Padrão L00{old_number_trimmed} NÃO encontrado em '{base_filename}'")
        
        # Verifica padrão reverso: se old_name contém "L" e arquivo contém número
        if not contains_old_number and old_name.startswith('L') and any(part in base_filename for part in [old_name_number, old_name_number.lstrip('0')]):
            contains_old_number = True
            print(f"✓ Padrão reverso encontrado: old_name '{old_name}' contém 'L' e arquivo contém número")
        
        # Caso especial: arquivo .txt sem prefixo L quando new_name tem L
        if not contains_old_number and (file_ext == '.txt' and new_name.startswith('L') and 
              not file_name_without_ext.startswith('L') and
              file_name_without_ext == new_name[1:]):  # Ex: 05456.txt quando new_name é L05456
            contains_old_number = True
            processed_by_special_logic = True
            print(f"✓ Caso especial .txt sem prefixo L: '{file_name_without_ext}' == '{new_name[1:]}'")
        
        # Caso especial: arquivo L00125.txt que sempre deve ser renomeado para o lote atual
        if not contains_old_number and file_name_without_ext == 'L00125' and file_ext == '.txt':
            contains_old_number = True
            processed_by_special_logic = True
            print(f"✓ Caso especial L00125.txt")
        
        print(f"\nResultado da detecção:")
        print(f"contains_old_number: {contains_old_number}")
        print(f"processed_by_special_logic: {processed_by_special_logic}")
        
        if contains_old_number:
            print(f"\n⚠️  ARQUIVO SERIA DETECTADO PARA RENOMEAÇÃO!")
            print(f"   Isso é o problema! Quando old_name == new_name,")
            print(f"   o arquivo não deveria ser detectado para renomeação.")
        else:
            print(f"\n✅ ARQUIVO NÃO SERIA DETECTADO - Correto!")
            
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
            size = os.path.getsize(item_path)
            print(f"{indent}📄 {item} ({size} bytes)")
        else:
            print(f"{indent}📁 {item}/")
            print_structure(item_path, indent + "  ")

if __name__ == "__main__":
    test_rename_files_same_name()