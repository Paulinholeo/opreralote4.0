#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug da função de renomeação
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def debug_rename():
    """
    Debug detalhado da função de renomeação
    """
    print("=== Debug da Renomeação ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="debug_rename_")
    
    try:
        # Cria estrutura exata: test_dir/L05043/ (já renomeado)
        lote_dir = os.path.join(test_dir, "L05043")
        os.makedirs(lote_dir, exist_ok=True)
        
        # Cria arquivos exatos do problema
        files_to_create = [
            "020250907000001pa.jpg",
            "020250907000001pb.jpg", 
            "020250907000001za.jpg",
            "020250907000001zb.jpg",
            "020250907.txt"
        ]
        
        for file_name in files_to_create:
            file_path = os.path.join(lote_dir, file_name)
            with open(file_path, "w") as f:
                f.write("test content")
        
        print(f"Diretório de teste: {test_dir}")
        print(f"Diretório do lote: {lote_dir}")
        print("Arquivos criados:")
        for f in files_to_create:
            print(f"  - {f}")
        
        # Testa com parâmetros exatos
        file_renamer = FileRenamer(test_dir)
        
        print(f"\nChamando rename_files('L0250907', 'L05043')...")
        old_name = "L0250907"  # Nome original
        new_name = "L05043"    # Nome para o qual já foi renomeado
        
        # Calcula os números como a função faz
        old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
        new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
        
        print(f"old_name_number: '{old_name_number}'")
        print(f"new_name_number: '{new_name_number}'")
        
        # Verifica se a detecção está funcionando
        for filename in files_to_create:
            if old_name_number in filename:
                print(f"✓ '{old_name_number}' encontrado em '{filename}'")
            else:
                print(f"✗ '{old_name_number}' NÃO encontrado em '{filename}'")
        
        # Executa a função
        file_renamer.rename_files(old_name, new_name)
        
        print("\nArquivos após renomeação:")
        final_files = sorted(os.listdir(lote_dir))
        for file_name in final_files:
            print(f"  - {file_name}")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    debug_rename()