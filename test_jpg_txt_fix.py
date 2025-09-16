#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para corrigir problemas de renomeação de arquivos JPG e TXT
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_jpg_txt_rename_fix():
    """
    Testa a correção da renomeação de arquivos JPG e TXT
    """
    print("=== Teste de Correção JPG e TXT ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_jpg_txt_")
    
    try:
        # Cria estrutura: test_dir/L05043/
        lote_dir = os.path.join(test_dir, "L05043")
        os.makedirs(lote_dir, exist_ok=True)
        
        # Cria arquivos que simulam o problema real
        files_to_create = [
            "020250907000001pa.jpg",
            "020250907000001pb.jpg", 
            "020250907000001za.jpg",
            "020250907000001zb.jpg",
            "020250907.txt"  # Arquivo txt que não estava sendo renomeado
        ]
        
        for file_name in files_to_create:
            file_path = os.path.join(lote_dir, file_name)
            with open(file_path, "w") as f:
                if file_name.endswith(".txt"):
                    f.write("0250907;BRI3002/2023;20250907;13:44:33;1;110;121,0;020250907000001za.jpg;020250907000001pa.jpg;020250907000001zb.jpg;020250907000001pb.jpg;003002;MG - 010 KM 26,9 VESPASIANO SD;7455")
                else:
                    f.write("fake image content")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Arquivos antes da renomeação:")
        for file_name in sorted(os.listdir(lote_dir)):
            print(f"  - {file_name}")
        
        # Testa a renomeação
        file_renamer = FileRenamer(test_dir)
        
        print(f"\nExecutando renomeação de 'L05043' para 'L05043' (mesmo nome, simula renomeação interna)...")
        print("Chamando rename_files('0250907', '05043')...\n")
        
        # Simula o que acontece na aplicação
        file_renamer.rename_files("0250907", "05043")
        
        print("\nArquivos após a renomeação:")
        final_files = sorted(os.listdir(lote_dir))
        for file_name in final_files:
            print(f"  - {file_name}")
        
        # Verifica se as correções funcionaram
        success_jpg = True
        success_txt = False
        
        for file_name in final_files:
            if ".jp.jpg" in file_name:
                print(f"\n⚠ PROBLEMA: Arquivo com extensão incorreta: {file_name}")
                success_jpg = False
            elif file_name.endswith(".jpg") and "05043" in file_name:
                print(f"✓ JPG renomeado corretamente: {file_name}")
            elif file_name.endswith(".txt") and "05043" in file_name:
                print(f"✓ TXT renomeado corretamente: {file_name}")
                success_txt = True
        
        if success_jpg:
            print("\n✓ SUCESSO: Todos os arquivos JPG têm extensão correta!")
        else:
            print("\n✗ ERRO: Problemas com extensões JPG detectados")
            
        if success_txt:
            print("✓ SUCESSO: Arquivo TXT foi renomeado!")
        else:
            print("⚠ AVISO: Arquivo TXT pode não ter sido renomeado")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    test_jpg_txt_rename_fix()