#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste detalhado para verificar a correção de padrões JPG
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_jpg_fix_detailed():
    """
    Testa especificamente a correção de padrões JPG
    """
    print("=== Teste Detalhado: Correção de Padrões JPG ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_jpg_fix_detailed_")
    
    try:
        # Cria uma instância do FileRenamer
        file_renamer = FileRenamer(test_dir)
        
        # Testa casos específicos
        test_cases = [
            # Caso problemático relatado
            ("000017070000060a.jpg", "00170", "00001700000060a.jpg"),
            ("000017070000060b.jpg", "00170", "00001700000060b.jpg"),
            # Casos que já estão corretos
            ("00001700000060a.jpg", "00170", "00001700000060a.jpg"),
            ("00001700000060b.jpg", "00170", "00001700000060b.jpg"),
        ]
        
        print("Testando função _fix_jpg_filename_pattern:")
        all_passed = True
        for i, (input_name, lot_number, expected) in enumerate(test_cases):
            result = file_renamer._fix_jpg_filename_pattern(input_name, lot_number)
            status = "✅" if result == expected else "❌"
            if result != expected:
                all_passed = False
            print(f"  {status} Caso {i+1}: '{input_name}' -> '{result}' (esperado: '{expected}')")
            
        if all_passed:
            print("  ✅ Todos os testes passaram!")
        else:
            print("  ❌ Alguns testes falharam!")
        
        # Testa com o caso real do problema
        print(f"\n{'='*50}")
        print(f"TESTE COM CASO REAL:")
        print(f"{'='*50}")
        
        # Cria estrutura: L00170/0000170/AITs/L00170.txt
        lote_dir = os.path.join(test_dir, "L00170")
        subdir = os.path.join(lote_dir, "0000170")
        aits_dir = os.path.join(subdir, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria o arquivo problemático com conteúdo específico
        problem_file = os.path.join(aits_dir, "L00170.txt")
        # Conteúdo com nomes de arquivos JPG que precisam ser corrigidos
        content = "0;000017070000060a.jpg;000017070000060b.jpg;016811;Av esta renomenado errado no arquivo L00170.txt deveria ser 00001700000060a.jpg;00001700000060b.jpg;"
        with open(problem_file, "w") as f:
            f.write(content)
        
        print(f"Arquivo criado: {problem_file}")
        print(f"Conteúdo original:")
        print(f"  {content}")
        
        # Mostra o conteúdo antes da renomeação
        print(f"\nConteúdo do arquivo antes da renomeação:")
        with open(problem_file, "r") as f:
            original_content = f.read()
        print(f"  {original_content}")
        
        # Analisa cada parte do conteúdo
        parts = original_content.split(';')
        print(f"\nAnálise parte a parte:")
        for i, part in enumerate(parts):
            if '.jpg' in part:
                corrected = file_renamer._fix_jpg_filename_pattern(part, "00170")
                status = "✅" if corrected != part else "ℹ️"
                print(f"  [{i}] '{part}' -> '{corrected}' {status}")
            else:
                print(f"  [{i}] '{part}'")
        
        # Executa a função real
        print(f"\n{'='*50}")
        print(f"EXECUTANDO RENAME_TEXT_CONTENT:")
        print(f"{'='*50}")
        
        file_renamer.rename_text_content("L0000125", "L00170")
        
        # Verifica resultado
        print(f"\nConteúdo do arquivo após renomeação:")
        with open(problem_file, "r") as f:
            new_content = f.read()
        print(f"  {new_content}")
        
        # Verifica se houve alguma mudança
        if new_content == original_content:
            print(f"\n❌ NENHUMA MUDANÇA: O conteúdo não foi modificado")
        else:
            print(f"\n✅ CONTEÚDO MODIFICADO")
            # Mostra as diferenças
            old_parts = original_content.split(';')
            new_parts = new_content.split(';')
            print(f"\nComparação parte a parte:")
            for i, (old_part, new_part) in enumerate(zip(old_parts, new_parts)):
                if old_part != new_part:
                    print(f"  [{i}] '{old_part}' -> '{new_part}'")
                else:
                    print(f"  [{i}] '{old_part}' (sem alteração)")
            
            # Verifica se a correção foi feita corretamente
            expected_content = "0;00001700000060a.jpg;00001700000060b.jpg;016811;Av esta renomenado errado no arquivo L00170.txt deveria ser 00001700000060a.jpg;00001700000060b.jpg;"
            if new_content == expected_content:
                print(f"\n🎉 SUCESSO TOTAL: Conteúdo corrigido exatamente como esperado!")
            else:
                print(f"\n⚠️  CONTEÚDO MODIFICADO, MAS NÃO EXATAMENTE COMO ESPERADO")
                print(f"   Esperado: {expected_content}")
                print(f"   Obtido:   {new_content}")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    test_jpg_fix_detailed()