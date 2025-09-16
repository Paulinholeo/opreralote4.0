#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para o caso relatado pelo usuário:
Arquivos JPG não estão sendo renomeados corretamente
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_user_case():
    """
    Testa o caso específico relatado pelo usuário onde arquivos JPG não são renomeados
    """
    print("=== Teste do Caso do Usuário ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_user_case_")
    
    try:
        # Cria estrutura semelhante à relatada:
        # L08976/BRI1309/20250905/010242/1/000/000,0/00126000001a.jpg
        # (substituído ":" por "" para evitar problemas no Windows)
        lote_dir = os.path.join(test_dir, "L08976")
        infra_dir = os.path.join(lote_dir, "BRI1309")
        date_dir = os.path.join(infra_dir, "20250905")
        time_dir = os.path.join(date_dir, "010242")  # Removido ":"
        type_dir = os.path.join(time_dir, "1")
        speed_dir = os.path.join(type_dir, "000")
        coord_dir = os.path.join(speed_dir, "000,0")
        
        os.makedirs(coord_dir, exist_ok=True)
        
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
            file_path = os.path.join(coord_dir, jpg_file)
            with open(file_path, "w") as f:
                f.write("fake jpg content")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Arquivos JPG antes da renomeação:")
        for root, dirs, files in os.walk(coord_dir):
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
        for root, dirs, files in os.walk(coord_dir):
            for file in files:
                if file.endswith('.jpg'):
                    final_files.append(file)
                    print(f"  - {file}")
        
        # Verifica se as correções funcionaram
        renamed_correctly = True
        for file_name in final_files:
            # Verifica se os arquivos foram renomeados corretamente
            if "00126" in file_name and "08976" not in file_name:
                print(f"\n⚠ PROBLEMA: Arquivo não renomeado: {file_name}")
                renamed_correctly = False
            elif "08976" in file_name:
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
    test_user_case()