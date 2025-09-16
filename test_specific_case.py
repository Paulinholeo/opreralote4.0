#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para o arquivo 05456.txt que não está sendo renomeado
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_specific_case():
    """
    Testa especificamente o caso do arquivo 05456.txt
    """
    print("=== Teste Específico: 05456.txt ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_specific_")
    
    try:
        # Cria estrutura simples: L05456/05456.txt
        lote_dir = os.path.join(test_dir, "L05456")
        os.makedirs(lote_dir, exist_ok=True)
        
        # Cria apenas o arquivo problemático
        problem_file = os.path.join(lote_dir, "05456.txt")
        with open(problem_file, "w") as f:
            f.write("05456;data;test")
        
        print(f"Arquivo criado: {problem_file}")
        print(f"Conteúdo: 05456;data;test")
        
        # Testa os parâmetros de detecção
        old_name = "L0000125"
        new_name = "L05456"
        old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
        new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
        
        print(f"\nParâmetros:")
        print(f"  old_name: '{old_name}'")
        print(f"  new_name: '{new_name}'")
        print(f"  old_name_number: '{old_name_number}'")
        print(f"  new_name_number: '{new_name_number}'")
        
        # Testa manualmente as condições
        base_filename = "05456.txt"
        file_ext = ".txt"
        file_name_without_ext = "05456"
        
        print(f"\nTeste das condições de detecção para '{base_filename}':")
        
        # Condição 1: old_name_number in base_filename
        cond1 = old_name_number in base_filename
        print(f"  1. '{old_name_number}' in '{base_filename}': {cond1}")
        
        # Condição 2: padrão L00XXX
        cond2 = False
        if len(old_name_number) >= 6 and old_name_number.startswith('00'):
            old_number_trimmed = old_name_number.lstrip('0')
            cond2 = f"L{old_number_trimmed.zfill(5)}" in base_filename or f"L00{old_number_trimmed}" in base_filename
        print(f"  2. Padrão L00XXX: {cond2}")
        
        # Condição 3: padrão reverso
        cond3 = old_name.startswith('L') and any(part in base_filename for part in [old_name_number, old_name_number.lstrip('0')])
        print(f"  3. Padrão reverso: {cond3}")
        
        # Condição 4: caso especial .txt sem L
        cond4 = (file_ext == '.txt' and new_name.startswith('L') and 
                not file_name_without_ext.startswith('L') and
                file_name_without_ext == new_name[1:])
        print(f"  4. Caso especial .txt: {cond4}")
        print(f"     file_name_without_ext == new_name[1:]: '{file_name_without_ext}' == '{new_name[1:]}' = {file_name_without_ext == new_name[1:]}")
        
        should_be_detected = cond1 or cond2 or cond3 or cond4
        print(f"\n  RESULTADO: Deveria ser detectado? {should_be_detected}")
        
        if should_be_detected:
            expected_new_name = new_name + file_ext
            print(f"  Nome esperado: {expected_new_name}")
        
        # Executa a função real
        print(f"\n{'='*50}")
        print(f"EXECUTANDO FUNÇÃO REAL:")
        print(f"{'='*50}")
        
        file_renamer = FileRenamer(test_dir)
        file_renamer.rename_files(old_name, new_name)
        
        # Verifica resultado
        final_files = os.listdir(lote_dir)
        print(f"\nArquivos após execução: {final_files}")
        
        if "L05456.txt" in final_files:
            print("✅ SUCESSO: Arquivo renomeado para L05456.txt")
        elif "05456.txt" in final_files:
            print("❌ PROBLEMA: Arquivo ainda é 05456.txt (não foi renomeado)")
        else:
            print("❓ SITUAÇÃO INESPERADA: Arquivo não encontrado")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    test_specific_case()