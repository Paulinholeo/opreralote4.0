#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para reorganização de subdiretórios
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_subdirectory_reorganization():
    """
    Testa a reorganização correta de subdiretórios
    Caso: L0544/0000125/AITs -> L0544/02544/AITs
    """
    print("=== Teste de Reorganização de Subdiretórios ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_subdir_")
    
    try:
        # Cria estrutura que simula o problema:
        # L0544/0000125/AITs/arquivo.jpg
        main_lote_dir = os.path.join(test_dir, "L0544")
        old_subdir = os.path.join(main_lote_dir, "0000125")
        aits_dir = os.path.join(old_subdir, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria alguns arquivos dentro
        with open(os.path.join(aits_dir, "0000125000070a.jpg"), "w") as f:
            f.write("test image a")
        with open(os.path.join(aits_dir, "0000125000070b.jpg"), "w") as f:
            f.write("test image b")
        with open(os.path.join(old_subdir, "0000125.txt"), "w") as f:
            f.write("0000544;BRI1306/2023;20250905;14:49:38;2;000;000,0;00125000070a.jpg;00125000070b.jpg;001306")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Estrutura inicial:")
        print_structure(test_dir)
        
        # Testa a reorganização
        file_renamer = FileRenamer(test_dir)
        
        print(f"\nExecutando renomeação de 'L0544' para 'L02544'...")
        success = file_renamer.rename_directory("L0544", "L02544")
        
        if success:
            print("✓ Renomeação principal realizada")
            
            # Executa as outras funções
            file_renamer.rename_files("L0544", "L02544")
            print("✓ Renomeação de arquivos realizada")
            
            print("\nEstrutura após renomeação:")
            print_structure(test_dir)
            
            # Verifica se a estrutura está correta
            expected_structure = os.path.join(test_dir, "L02544", "02544", "AITs")
            if os.path.exists(expected_structure):
                print(f"\n✓ SUCESSO: Estrutura corrigida!")
                print(f"  Diretório criado: {expected_structure}")
                
                # Verifica se os arquivos foram movidos
                files_in_aits = os.listdir(expected_structure)
                print(f"  Arquivos em AITs: {files_in_aits}")
                
                # Verifica se não sobrou o diretório antigo
                old_structure = os.path.join(test_dir, "L02544", "0000125")
                if not os.path.exists(old_structure):
                    print("✓ Diretório antigo removido corretamente")
                else:
                    print("⚠ Diretório antigo ainda existe")
                    
            else:
                print(f"\n⚠ Estrutura esperada não encontrada: {expected_structure}")
                
        else:
            print("✗ Falha na renomeação")
            
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
    test_subdirectory_reorganization()