#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para correção do prefixo L em arquivos .txt
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_l_prefix_correction():
    """
    Testa a correção do prefixo L em arquivos .txt
    """
    print("=== Teste de Correção do Prefixo L ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_l_prefix_")
    
    try:
        # Cria estrutura: L05456/ (já renomeado)
        lote_dir = os.path.join(test_dir, "L05456")
        os.makedirs(lote_dir, exist_ok=True)
        
        # Cria arquivo que está sendo renomeado incorretamente
        problem_file = os.path.join(lote_dir, "05456.txt")  # Sem prefixo L
        with open(problem_file, "w") as f:
            f.write("05456;BRI1306/2023;20250905;14:49:38;2;000;000,0;05456000070a.jpg;05456000070b.jpg;001306;Test Location;5673")
        
        # Cria outros arquivos para contexto
        other_files = [
            os.path.join(lote_dir, "05456000070a.jpg"),
            os.path.join(lote_dir, "05456000070b.jpg")
        ]
        
        for file_path in other_files:
            with open(file_path, "w") as f:
                f.write("test content")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Arquivos antes da correção:")
        for file_name in sorted(os.listdir(lote_dir)):
            print(f"  - {file_name}")
        
        # Simula a situação real onde o arquivo já foi renomeado mas sem o prefixo L
        file_renamer = FileRenamer(test_dir)
        
        print(f"\nSimulando correção: renomeando arquivos em lote L05456")
        print("old_name='L05456', new_name='L05456' (mesmo nome para testar lógica de prefixo)")
        
        # Simula os parâmetros que chegam na função
        old_name = "L05456"
        new_name = "L05456"
        
        # Calcula os números como a função faz
        old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
        new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
        
        print(f"old_name_number: '{old_name_number}'")
        print(f"new_name_number: '{new_name_number}'")
        print(f"new_name: '{new_name}'")
        print(f"new_name.startswith('L'): {new_name.startswith('L')}")
        
        # Verifica lógica para o arquivo problemático
        test_filename = "05456.txt"
        base_name = os.path.splitext(test_filename)[0]
        print(f"\nArquivo teste: '{test_filename}' (base_name: '{base_name}')")
        print(f"base_name.startswith('L'): {base_name.startswith('L')}")
        
        if new_name.startswith('L') and not base_name.startswith('L'):
            expected_new_name = f"{new_name}.txt"
            print(f"✓ Deve ser renomeado para: {expected_new_name}")
        else:
            print(f"? Lógica não aplicável")
        
        # Executa a função
        file_renamer.rename_files(old_name, new_name)
        
        print(f"\nArquivos após renomeação:")
        final_files = sorted(os.listdir(lote_dir))
        for file_name in final_files:
            print(f"  - {file_name}")
        
        # Verifica se a correção funcionou
        expected_file = "L05456.txt"
        if expected_file in final_files:
            print(f"\n✅ SUCESSO: Arquivo renomeado para '{expected_file}'")
        elif "05456.txt" in final_files:
            print(f"\n⚠ PROBLEMA: Arquivo ainda sem prefixo L: '05456.txt'")
        else:
            txt_files = [f for f in final_files if f.endswith('.txt')]
            print(f"\n? Arquivos .txt encontrados: {txt_files}")
                
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    test_l_prefix_correction()