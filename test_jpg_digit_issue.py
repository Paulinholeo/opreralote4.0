#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar o problema com a quantidade de dígitos nos arquivos JPG
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_jpg_digit_issue():
    """
    Testa o problema com a quantidade de dígitos nos arquivos JPG
    """
    print("=== Teste do Problema com Dígitos em JPGs ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_jpg_digits_")
    
    try:
        # Cria estrutura similar ao caso real:
        # L08976/0008976/AITs/
        lote_dir = os.path.join(test_dir, "L08976")
        subdir = os.path.join(lote_dir, "0008976")
        aits_dir = os.path.join(subdir, "AITs")
        
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria arquivos JPG com diferentes padrões numéricos
        test_files = [
            # Arquivos com 6 dígitos (padrão antigo) - "00126" deve virar "0008976"
            "00126000001a.jpg",
            "00126000001b.jpg",
            
            # Arquivos com 7 dígitos (padrão esperado) - "000126" deve virar "0008976"
            "000126000002a.jpg",
            "000126000002b.jpg",
        ]
        
        for jpg_file in test_files:
            file_path = os.path.join(aits_dir, jpg_file)
            with open(file_path, "w") as f:
                f.write("fake jpg content")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Arquivos JPG antes da renomeação:")
        for file in sorted(os.listdir(aits_dir)):
            if file.endswith('.jpg'):
                print(f"  - {file}")
        
        # Testa a renomeação
        file_renamer = FileRenamer(test_dir)
        
        print(f"\nExecutando renomeação de '00126' para '08976'...")
        file_renamer.rename_directory("L08976", "L08976")  # Mesmo nome
        file_renamer.rename_files("00126", "08976")
        file_renamer.rename_text_content("00126", "08976")
        
        print("\nArquivos JPG após a renomeação:")
        renamed_files = []
        for file in os.listdir(aits_dir):
            if file.endswith('.jpg'):
                renamed_files.append(file)
                print(f"  - {file}")
        
        # Verifica se os arquivos mantêm 7 dígitos
        print("\n=== VERIFICAÇÃO DE DÍGITOS ===")
        success_count = 0
        total_count = 0
        
        # Padrões esperados após renomeação (substituindo "00126" ou "000126" por "0008976")
        expected_renames = {
            "00126000001a.jpg": "0008976000001a.jpg",  # "00126" -> "0008976"
            "00126000001b.jpg": "0008976000001b.jpg",  # "00126" -> "0008976"
            "000126000002a.jpg": "0008976000002a.jpg", # "000126" -> "0008976"
            "000126000002b.jpg": "0008976000002b.jpg", # "000126" -> "0008976"
        }
        
        for original_file, expected_file in expected_renames.items():
            total_count += 1
            if expected_file in renamed_files:
                print(f"✓ {original_file} -> {expected_file} (7 dígitos corretos)")
                success_count += 1
            else:
                # Verifica se há algum arquivo renomeado com padrão diferente
                found = False
                for renamed_file in renamed_files:
                    if "0008976" in renamed_file and "00126" not in renamed_file:
                        print(f"⚠ {original_file} -> {renamed_file} (contém 0008976, mas padrão diferente)")
                        found = True
                        break
                
                if not found:
                    print(f"✗ {original_file} -> NÃO RENOMEADO CORRETAMENTE")
        
        success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
        print(f"\nTaxa de sucesso: {success_rate:.1f}% ({success_count}/{total_count})")
        
        if success_rate == 100:
            print("\n🎉 SUCESSO TOTAL: Todos os arquivos JPG foram renomeados corretamente com 7 dígitos!")
        elif success_rate >= 50:
            print(f"\n⚠ SUCESSO PARCIAL: {success_rate:.1f}% dos arquivos foram renomeados corretamente")
        else:
            print(f"\n❌ FALHA: Apenas {success_rate:.1f}% dos arquivos foram renomeados corretamente")
            
        return success_rate >= 50
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    test_jpg_digit_issue()