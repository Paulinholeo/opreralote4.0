#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificação final da correção do problema com JPGs
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_final_verification():
    """
    Verifica que a correção está funcionando corretamente
    """
    print("=== Verificação Final da Correção JPG ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_final_")
    
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
        file_renamer.rename_directory("L08976", "L08976")  # Mesmo nome
        file_renamer.rename_files("00126", "08976")
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
        
        # Verifica se os arquivos foram renomeados corretamente
        # O padrão é: 00126XXXXXX.jpg -> 08976XXXXXX.jpg
        expected_renames = {
            "00126000001a.jpg": "08976000001a.jpg",
            "00126000001b.jpg": "08976000001b.jpg",
            "00126000002a.jpg": "08976000002a.jpg",
            "00126000002b.jpg": "08976000002b.jpg",
            "00126000003a.jpg": "08976000003a.jpg",  # Arquivo problemático
            "00126000003b.jpg": "08976000003b.jpg",  # Arquivo problemático
            "00126000004a.jpg": "08976000004a.jpg",
            "00126000004b.jpg": "08976000004b.jpg",
            "00126000005a.jpg": "08976000005a.jpg",
            "00126000005b.jpg": "08976000005b.jpg",
            "00126000006a.jpg": "08976000006a.jpg",
            "00126000006b.jpg": "08976000006b.jpg"
        }
        
        all_correct = True
        for original, expected in expected_renames.items():
            if expected in renamed_files:
                print(f"✓ {original} -> {expected}")
            else:
                print(f"✗ {original} NÃO FOI RENOMEADO PARA {expected}")
                all_correct = False
        
        if all_correct:
            print("\n🎉 SUCESSO TOTAL: Todos os arquivos JPG foram renomeados corretamente!")
            print("✅ Especificamente, os arquivos problemáticos 00126000003a.jpg e 00126000003b.jpg foram renomeados!")
        else:
            print("\n❌ FALHA: Alguns arquivos não foram renomeados corretamente.")
            
        return all_correct
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    test_final_verification()