#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste complexo para verificar a correção em cenários com diferentes padrões de numeração
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_complex_jpg_case():
    """
    Testa cenários complexos de renomeação de JPGs com diferentes padrões
    """
    print("=== Teste Complexo de Renomeação JPG ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_complex_jpg_")
    
    try:
        # Cria estrutura complexa:
        # L08976/0008976/AITs/
        lote_dir = os.path.join(test_dir, "L08976")
        subdir = os.path.join(lote_dir, "0008976")
        aits_dir = os.path.join(subdir, "AITs")
        
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria arquivos JPG com diferentes padrões numéricos
        test_files = [
            # Padrão relatado pelo usuário
            "00126000001a.jpg",
            "00126000001b.jpg",
            "00126000003a.jpg",  # Arquivo problemático mencionado
            "00126000003b.jpg",  # Arquivo problemático mencionado
            
            # Outros padrões numéricos
            "00126000005a.jpg",
            "00126000005b.jpg",
            
            # Padrões com diferentes comprimentos
            "0126000007a.jpg",
            "0126000007b.jpg",
            
            # Padrões complexos
            "test_00126_file_00126000008a.jpg",
            "test_00126_file_00126000008b.jpg",
        ]
        
        for jpg_file in test_files:
            file_path = os.path.join(aits_dir, jpg_file)
            with open(file_path, "w") as f:
                f.write("fake jpg content")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Arquivos JPG antes da renomeação:")
        for file in sorted(test_files):
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
        
        # Verifica os resultados
        print("\n=== VERIFICAÇÃO ===")
        success_count = 0
        total_count = len(test_files)
        
        # Verifica se os arquivos problemáticos foram renomeados
        problematic_files = ["00126000003a.jpg", "00126000003b.jpg"]
        for original in problematic_files:
            # Procura por arquivos renomeados que contenham o padrão esperado
            expected_pattern = original.replace("00126", "08976")
            found = any(expected_pattern in renamed for renamed in renamed_files)
            if found:
                print(f"✓ {original} -> OK (contém {expected_pattern})")
                success_count += 1
            else:
                print(f"✗ {original} -> FALHOU")
        
        # Verifica todos os arquivos
        for original in test_files:
            # Para arquivos com padrão "00126", verificamos se foram substituídos por "08976"
            if "00126" in original:
                expected_pattern = original.replace("00126", "08976")
                found = any(expected_pattern in renamed for renamed in renamed_files)
                if found:
                    print(f"✓ {original} -> OK")
                    success_count += 1
                else:
                    print(f"✗ {original} -> FALHOU")
            else:
                # Arquivos que não contêm "00126" devem permanecer inalterados
                if original in renamed_files:
                    print(f"✓ {original} -> Mantido (OK)")
                    success_count += 1
                else:
                    print(f"✗ {original} -> FALHOU (arquivo desapareceu)")
        
        success_rate = (success_count / total_count) * 100
        print(f"\nTaxa de sucesso: {success_rate:.1f}% ({success_count}/{total_count})")
        
        if success_rate == 100:
            print("\n🎉 SUCESSO TOTAL: Todos os arquivos JPG foram tratados corretamente!")
            print("✅ Os arquivos problemáticos 00126000003a.jpg e 00126000003b.jpg foram renomeados!")
        elif success_rate >= 80:
            print(f"\n⚠ SUCESSO PARCIAL: {success_rate:.1f}% dos arquivos foram tratados corretamente")
        else:
            print(f"\n❌ FALHA: Apenas {success_rate:.1f}% dos arquivos foram tratados corretamente")
            
        return success_rate >= 80
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    test_complex_jpg_case()