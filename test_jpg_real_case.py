#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para o caso real relatado:
";0010637000003a.jpg neste caso deveria ter mais dois digitos 0000126000003a.jpg"

Na verdade, o caso é:
old_name = "0010637" (com zeros à esquerda)
new_name = "10637" (sem zeros à esquerda)

Arquivo: "0010637000003a.jpg" deveria virar "00010637000003a.jpg"
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_jpg_real_case():
    """
    Testa o caso real relatado:
    old_name = "0010637" 
    new_name = "10637"
    Arquivo: "0010637000003a.jpg" deveria virar "00010637000003a.jpg"
    """
    print("=== Teste do caso real relatado ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_jpg_real_case_")
    
    try:
        # Cria a estrutura exata do problema
        lote_dir = os.path.join(test_dir, "10637")
        subdir_correct = os.path.join(lote_dir, "00010637")  # Diretório correto após correção
        aits_dir = os.path.join(subdir_correct, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria o arquivo problemático: 0010637000003a.jpg que deve ser renomeado para 00010637000003a.jpg
        # quando old_name = "0010637" e new_name = "10637"
        jpg_path = os.path.join(aits_dir, "0010637000003a.jpg")
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
        
        # Etapa 2: Executa rename_files com old_name != new_name
        print(f"\n{'='*60}")
        print(f"ETAPA 2: Executando rename_files('0010637', '10637')")
        print(f"{'='*60}")
        print(f"old_name = '0010637' (com zeros à esquerda)")
        print(f"new_name = '10637' (sem zeros à esquerda)")
        print(f"Arquivo 0010637000003a.jpg deve ser renomeado para 00010637000003a.jpg")
        
        # Executa exatamente como na GUI
        file_renamer.rename_files("0010637", "10637")
        
        print(f"\nEstrutura após rename_files:")
        print_structure(test_dir)
        
        # Etapa 3: Verifica o resultado
        print(f"\n{'='*60}")
        print(f"ETAPA 3: Verificando resultado")
        print(f"{'='*60}")
        
        # Verifica se o arquivo foi renomeado corretamente
        expected_file = os.path.join(aits_dir, "00010637000003a.jpg")
        original_file = os.path.join(aits_dir, "0010637000003a.jpg")
        
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
    test_jpg_real_case()