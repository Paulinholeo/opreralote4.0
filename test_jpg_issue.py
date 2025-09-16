#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar o problema com arquivos JPG
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_jpg_issue():
    """
    Testa o problema com arquivos JPG como '00126000132a.jpg' 
    que deveriam ser renomeados para '0000126000132a.jpg'
    """
    print("=== Teste de problema com arquivos JPG ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_jpg_issue_")
    
    try:
        # Cria a estrutura exata do problema
        lote_dir = os.path.join(test_dir, "L00126")
        subdir = os.path.join(lote_dir, "0000126")
        aits_dir = os.path.join(subdir, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria o arquivo problemático: 00126000132a.jpg
        jpg_path = os.path.join(aits_dir, "00126000132a.jpg")
        with open(jpg_path, "w", encoding='utf-8') as f:
            f.write("fake jpg content")
        
        print(f"Estrutura inicial:")
        print(f"Diretório base: {test_dir}")
        print_structure(test_dir)
        
        # Etapa 1: Simula exatamente o que acontece na GUI
        print(f"\n{'='*60}")
        print(f"ETAPA 1: Criando FileRenamer")
        print(f"{'='*60}")
        
        file_renamer = FileRenamer(test_dir)
        print(f"FileRenamer criado com diretório: {test_dir}")
        
        # Etapa 2: Executa rename_files
        print(f"\n{'='*60}")
        print(f"ETAPA 2: Executando rename_files('L00126', 'L00126')")
        print(f"{'='*60}")
        print(f"Este é o caso onde old_name == new_name")
        print(f"Mas o arquivo contém '00126' que deve ser padronizado para '0000126'")
        
        # Executa exatamente como na GUI
        file_renamer.rename_files("L00126", "L00126")
        
        print(f"\nEstrutura após rename_files:")
        print_structure(test_dir)
        
        # Etapa 3: Verifica o resultado
        print(f"\n{'='*60}")
        print(f"ETAPA 3: Verificando resultado")
        print(f"{'='*60}")
        
        # Verifica se o arquivo foi renomeado corretamente
        expected_file = os.path.join(aits_dir, "0000126000132a.jpg")
        original_file = os.path.join(aits_dir, "00126000132a.jpg")
        
        if os.path.exists(expected_file):
            print(f"✅ ARQUIVO CORRETO EXISTE: {expected_file}")
        else:
            print(f"❌ ARQUIVO CORRETO NÃO EXISTE: {expected_file}")
            
        if os.path.exists(original_file):
            print(f"❌ ARQUIVO ORIGINAL AINDA EXISTE: {original_file}")
            print(f"   Este é o problema! O arquivo não foi renomeado.")
        else:
            print(f"✅ ARQUIVO ORIGINAL NÃO EXISTE: {original_file}")
            
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
    test_jpg_issue()