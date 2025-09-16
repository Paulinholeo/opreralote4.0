#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para o caso onde old_name == new_name mas os números são diferentes
Exemplo: old_name = "0010637", new_name = "10637" (mesmo valor, formatos diferentes)
Arquivo: 0010637000017a.jpg deve virar 00010637000017a.jpg
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_specific_case_fix():
    """
    Testa o caso específico onde old_name == new_name mas os números são diferentes
    """
    print("=== Teste Caso Específico: old_name == new_name mas números diferentes ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_specific_case_fix_")
    
    try:
        # Cria a estrutura exata do problema
        lote_dir = os.path.join(test_dir, "10637")
        subdir_correct = os.path.join(lote_dir, "0010637")  # Diretório com número não padronizado
        aits_dir = os.path.join(subdir_correct, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria o arquivo problemático
        test_file = os.path.join(aits_dir, "0010637000017a.jpg")
        with open(test_file, "w") as f:
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
        
        # Etapa 2: Executa rename_files com old_name == new_name mas números diferentes
        print(f"\n{'='*60}")
        print(f"ETAPA 2: Executando rename_files('0010637', '10637')")
        print(f"{'='*60}")
        print(f"Este é o caso onde old_name == new_name ('10637') mas os números são diferentes")
        print(f"old_name_number: '0010637' -> new_name_number: '10637'")
        print(f"O arquivo 0010637000017a.jpg deve ser renomeado para 00010637000017a.jpg")
        
        # Executa exatamente como na GUI
        file_renamer.rename_files("0010637", "10637")
        
        print(f"\nEstrutura após rename_files:")
        print_structure(test_dir)
        
        # Etapa 3: Verifica o resultado
        print(f"\n{'='*60}")
        print(f"ETAPA 3: Verificando resultado")
        print(f"{'='*60}")
        
        # Verifica se o arquivo foi renomeado corretamente
        expected_file = os.path.join(aits_dir, "00010637000017a.jpg")
        old_file = os.path.join(aits_dir, "0010637000017a.jpg")
        
        if os.path.exists(expected_file):
            print(f"✅ ARQUIVO RENOMEADO CORRETAMENTE: {os.path.basename(expected_file)}")
        else:
            print(f"❌ ARQUIVO NÃO RENOMEADO CORRETAMENTE: {os.path.basename(expected_file)}")
            
        if os.path.exists(old_file):
            print(f"❌ ARQUIVO ANTIGO AINDA EXISTE: {os.path.basename(old_file)}")
        else:
            print(f"✅ ARQUIVO ANTIGO REMOVIDO: {os.path.basename(old_file)}")
        
        # Etapa 4: Teste com outro caso
        print(f"\n{'='*60}")
        print(f"ETAPA 4: Testando com L08685")
        print(f"{'='*60}")
        
        # Cria nova estrutura
        lote_dir2 = os.path.join(test_dir, "L08685")
        subdir2 = os.path.join(lote_dir2, "0000125")
        aits_dir2 = os.path.join(subdir2, "AITs")
        os.makedirs(aits_dir2, exist_ok=True)
        
        # Cria arquivo
        test_file2 = os.path.join(aits_dir2, "0000125000017a.jpg")
        with open(test_file2, "w") as f:
            f.write("fake jpg content")
            
        print(f"Estrutura antes:")
        print_structure(lote_dir2)
        
        file_renamer2 = FileRenamer(test_dir)
        file_renamer2.rename_files("L08685", "L08685")
        
        print(f"Estrutura após:")
        print_structure(lote_dir2)
        
        # Verifica resultado
        expected_file2 = os.path.join(aits_dir2, "0008685000017a.jpg")
        old_file2 = os.path.join(aits_dir2, "0000125000017a.jpg")
        
        if os.path.exists(expected_file2):
            print(f"✅ ARQUIVO RENOMEADO CORRETAMENTE: {os.path.basename(expected_file2)}")
        else:
            print(f"❌ ARQUIVO NÃO RENOMEADO CORRETAMENTE: {os.path.basename(expected_file2)}")
            
        if os.path.exists(old_file2):
            print(f"❌ ARQUIVO ANTIGO AINDA EXISTE: {os.path.basename(old_file2)}")
        else:
            print(f"✅ ARQUIVO ANTIGO REMOVIDO: {os.path.basename(old_file2)}")
            
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
    test_specific_case_fix()