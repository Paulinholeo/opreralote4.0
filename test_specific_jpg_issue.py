#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para o problema relatado:
'nao esra renomaneando 00126000003a.jpg nem a e b'
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_specific_jpg_issue():
    """
    Testa especificamente o caso onde 00126000003a.jpg e 00126000003b.jpg não estão sendo renomeados
    """
    print("=== Teste Específico do Problema com JPGs ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_specific_jpg_")
    
    try:
        # Cria estrutura similar ao caso real:
        # L08976/0008976/AITs/
        lote_dir = os.path.join(test_dir, "L08976")
        subdir = os.path.join(lote_dir, "0008976")  # Número novo do lote
        aits_dir = os.path.join(subdir, "AITs")
        
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria os arquivos JPG problemáticos especificamente mencionados
        problematic_files = [
            "00126000003a.jpg",  # Este arquivo específico não estava sendo renomeado
            "00126000003b.jpg"   # Este arquivo específico não estava sendo renomeado
        ]
        
        # Também cria outros arquivos para teste completo
        other_files = [
            "00126000001a.jpg",
            "00126000001b.jpg",
            "00126000002a.jpg", 
            "00126000002b.jpg",
            "00126000004a.jpg",
            "00126000004b.jpg",
            "00126000005a.jpg",
            "00126000005b.jpg",
            "00126000006a.jpg",
            "00126000006b.jpg"
        ]
        
        all_files = problematic_files + other_files
        
        for jpg_file in all_files:
            file_path = os.path.join(aits_dir, jpg_file)
            with open(file_path, "w") as f:
                f.write("fake jpg content")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Arquivos JPG antes da renomeação:")
        for file in sorted(all_files):
            print(f"  - {file}")
        
        # Testa a renomeação
        file_renamer = FileRenamer(test_dir)
        
        print(f"\nExecutando renomeação de '00126' para '08976'...")
        # Simula o processo real:
        # 1. Renomeia diretório (já deve estar correto)
        file_renamer.rename_directory("L08976", "L08976")  # Mesmo nome
        # 2. Renomeia arquivos
        file_renamer.rename_files("00126", "08976")
        # 3. Renomeia conteúdo dos arquivos de texto
        file_renamer.rename_text_content("00126", "08976")
        
        print("\nArquivos JPG após a renomeação:")
        renamed_files = []
        for file in os.listdir(aits_dir):
            if file.endswith('.jpg'):
                renamed_files.append(file)
                print(f"  - {file}")
        
        # Verifica especificamente os arquivos problemáticos
        print("\n=== VERIFICAÇÃO ESPECÍFICA ===")
        success = True
        
        # Verifica se os arquivos problemáticos foram renomeados
        for original_file in problematic_files:
            # O nome esperado após renomeação seria "08976000003a.jpg" e "08976000003b.jpg"
            # Mas na lógica atual, o padrão é substituir "00126" por "008976"
            expected_part = original_file.replace("00126", "008976")
            
            found = False
            for renamed_file in renamed_files:
                if expected_part in renamed_file:
                    print(f"✓ {original_file} -> {renamed_file}")
                    found = True
                    break
            
            if not found:
                print(f"✗ {original_file} NÃO FOI RENOMEADO CORRETAMENTE")
                success = False
        
        # Verifica se todos os arquivos foram renomeados
        all_renamed_correctly = True
        for original_file in all_files:
            expected_part = original_file.replace("00126", "008976")
            found = any(expected_part in renamed_file for renamed_file in renamed_files)
            if not found:
                print(f"✗ {original_file} NÃO FOI RENOMEADO")
                all_renamed_correctly = False
        
        if success and all_renamed_correctly:
            print("\n🎉 SUCESSO TOTAL: Todos os arquivos JPG foram renomeados corretamente!")
            print("✅ Especificamente, os arquivos problemáticos 00126000003a.jpg e 00126000003b.jpg foram renomeados!")
        elif success:
            print("\n⚠ SUCESSO PARCIAL: Os arquivos problemáticos foram renomeados, mas alguns outros não.")
        else:
            print("\n❌ FALHA: Os arquivos problemáticos não foram renomeados.")
            
        return success
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    test_specific_jpg_issue()