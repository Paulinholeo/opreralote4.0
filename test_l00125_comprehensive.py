#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste abrangente para verificar a correção do arquivo L00125.txt em diferentes cenários
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_l00125_comprehensive():
    """
    Teste abrangente para L00125.txt em diferentes estruturas
    """
    print("=== Teste Abrangente L00125.txt ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_l00125_comprehensive_")
    
    try:
        # Cenário 1: L08421\0000125\AITs\L00125.txt
        scenario1_dir = os.path.join(test_dir, "L08421", "0000125", "AITs")
        os.makedirs(scenario1_dir, exist_ok=True)
        
        file1 = os.path.join(scenario1_dir, "L00125.txt")
        with open(file1, "w") as f:
            f.write("0000125;test1;data")
        
        # Cenário 2: L05456\L05456\AITs\L00125.txt
        scenario2_dir = os.path.join(test_dir, "L05456", "L05456", "AITs")
        os.makedirs(scenario2_dir, exist_ok=True)
        
        file2 = os.path.join(scenario2_dir, "L00125.txt")
        with open(file2, "w") as f:
            f.write("0000125;test2;data")
        
        # Cenário 3: L09999\AITs\L00125.txt (AITs direto)
        scenario3_dir = os.path.join(test_dir, "L09999", "AITs")
        os.makedirs(scenario3_dir, exist_ok=True)
        
        file3 = os.path.join(scenario3_dir, "L00125.txt")
        with open(file3, "w") as f:
            f.write("0000125;test3;data")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Estrutura ANTES:")
        print_structure(test_dir)
        
        # Testa cada cenário
        file_renamer = FileRenamer(test_dir)
        
        scenarios = [
            ("L08421", "L08421"),
            ("L05456", "L05456"), 
            ("L09999", "L09999")
        ]
        
        for old_name, new_name in scenarios:
            print(f"\n{'='*60}")
            print(f"TESTANDO CENÁRIO: {old_name} -> {new_name}")
            print(f"{'='*60}")
            
            # Verifica se o diretório existe
            main_dir = os.path.join(test_dir, old_name)
            if os.path.exists(main_dir):
                print(f"Executando renomeação para {old_name}...")
                file_renamer.rename_files(old_name, new_name)
            else:
                print(f"Diretório {old_name} não existe, pulando...")
        
        print(f"\n{'='*60}")
        print(f"ESTRUTURA FINAL")
        print(f"{'='*60}")
        print_structure(test_dir)
        
        # Verifica resultados
        print(f"\n{'='*60}")
        print(f"VERIFICAÇÃO DE RESULTADOS")
        print(f"{'='*60}")
        
        results = []
        for root, dirs, files in os.walk(test_dir):
            for file in files:
                if file.endswith('.txt'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, test_dir)
                    results.append((rel_path, file))
        
        success_count = 0
        total_count = len(results)
        
        print(f"Arquivos .txt encontrados após renomeação:")
        for rel_path, file_name in results:
            if file_name == 'L00125.txt':
                print(f"❌ {rel_path} - AINDA NÃO RENOMEADO")
            elif file_name.startswith('L') and file_name.endswith('.txt') and file_name != 'L00125.txt':
                print(f"✅ {rel_path} - RENOMEADO CORRETAMENTE")
                success_count += 1
            else:
                print(f"❓ {rel_path} - RESULTADO INESPERADO")
        
        print(f"\nResumo: {success_count}/{total_count} arquivos renomeados com sucesso")
        
        if success_count == total_count:
            print(f"\n🎉 TODOS OS ARQUIVOS L00125.txt FORAM RENOMEADOS CORRETAMENTE!")
        else:
            print(f"\n⚠️ ALGUNS ARQUIVOS AINDA PRECISAM DE CORREÇÃO")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

def print_structure(directory, indent=""):
    """
    Imprime estrutura detalhada
    """
    if not os.path.exists(directory):
        return
        
    items = sorted(os.listdir(directory))
    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            print(f"{indent}📄 {item}")
        else:
            print(f"{indent}📁 {item}/")
            print_structure(item_path, indent + "  ")

if __name__ == "__main__":
    test_l00125_comprehensive()