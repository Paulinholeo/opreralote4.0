#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simplificado para o caso relatado pelo usuário:
Arquivos JPG não estão sendo renomeados corretamente
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_simple_user_case():
    """
    Testa o caso específico relatado pelo usuário onde arquivos JPG não são renomeados
    """
    print("=== Teste Simplificado do Caso do Usuário ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_simple_user_case_")
    
    try:
        # Cria estrutura mais simples:
        # L08976/0008976/AITs/
        lote_dir = os.path.join(test_dir, "L08976")
        subdir = os.path.join(lote_dir, "0008976")
        aits_dir = os.path.join(subdir, "AITs")
        
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria arquivos JPG como os mencionados pelo usuário
        jpg_files = [
            "00126000001a.jpg",
            "00126000001b.jpg",
            "00126000002a.jpg", 
            "00126000002b.jpg",
            "00126000003a.jpg",
            "00126000003b.jpg",
            "00126000004a.jpg",
            "00126000004b.jpg",
            "00126000005a.jpg",
            "00126000005b.jpg",
            "00126000006a.jpg",
            "00126000006b.jpg"
        ]
        
        for jpg_file in jpg_files:
            file_path = os.path.join(aits_dir, jpg_file)
            with open(file_path, "w") as f:
                f.write("fake jpg content")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Arquivos JPG antes da renomeação:")
        for root, dirs, files in os.walk(aits_dir):
            for file in files:
                if file.endswith('.jpg'):
                    print(f"  - {file}")
        
        # Testa a renomeação
        file_renamer = FileRenamer(test_dir)
        
        print(f"\nExecutando renomeação...")
        # Aqui simulamos o que acontece na aplicação real
        # A renomeação seria de "L08976" para "L08976" (mesmo nome, mas com atualização interna)
        file_renamer.rename_directory("L08976", "L08976")
        file_renamer.rename_files("00126", "08976")  # Exemplo de renomeação interna
        file_renamer.rename_text_content("00126", "08976")
        
        print("\nArquivos JPG após a renomeação:")
        final_files = []
        for root, dirs, files in os.walk(aits_dir):
            for file in files:
                if file.endswith('.jpg'):
                    final_files.append(file)
                    print(f"  - {file}")
        
        # Verifica se as correções funcionaram
        renamed_correctly = True
        for file_name in final_files:
            # Verifica se os arquivos foram renomeados corretamente
            # Esperamos que "00126" seja substituído por "008976"
            if "00126" in file_name and "008976" not in file_name:
                print(f"\n⚠ PROBLEMA: Arquivo não renomeado: {file_name}")
                renamed_correctly = False
            elif "008976" in file_name:
                print(f"✓ JPG renomeado corretamente: {file_name}")
        
        if renamed_correctly:
            print("\n✓ SUCESSO: Todos os arquivos JPG foram renomeados!")
        else:
            print("\n✗ ERRO: Alguns arquivos JPG não foram renomeados")
            
        return renamed_correctly
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    test_simple_user_case()