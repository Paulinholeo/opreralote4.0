#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico para identificar arquivos que não estão sendo renomeados
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def diagnostic_test():
    """
    Teste de diagnóstico para identificar problemas de renomeação
    """
    print("=== Diagnóstico de Renomeação ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="diagnostic_")
    
    try:
        # Simula estrutura real com vários tipos de arquivo
        lote_dir = os.path.join(test_dir, "L05456")
        subdir = os.path.join(lote_dir, "0000125")
        aits_dir = os.path.join(subdir, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria diferentes tipos de arquivo para testar
        test_files = {
            # Arquivo principal
            os.path.join(lote_dir, "05456.txt"): "05456;data;test",
            
            # Arquivos no subdiretório
            os.path.join(subdir, "0000125.txt"): "0000125;data;test",
            
            # Arquivos no AITs
            os.path.join(aits_dir, "L00125.txt"): "0000125;data;test;AITs",
            os.path.join(aits_dir, "0000125001.jpg"): "fake jpg",
            os.path.join(aits_dir, "0000125002.jpg"): "fake jpg",
            
            # Outros arquivos
            os.path.join(subdir, "0000125001.jpg"): "fake jpg main",
        }
        
        for file_path, content in test_files.items():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content)
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Arquivos ANTES da renomeação:")
        print_detailed_structure(test_dir)
        
        # Testa renomeação
        file_renamer = FileRenamer(test_dir)
        
        print(f"\n{'='*50}")
        print(f"EXECUTANDO RENOMEAÇÃO: L0000125 -> L05456")
        print(f"{'='*50}")
        
        old_name = "L0000125"
        new_name = "L05456"
        
        # Executa com logs detalhados
        file_renamer.rename_files(old_name, new_name)
        
        print(f"\n{'='*50}")
        print(f"RESULTADO APÓS RENOMEAÇÃO:")
        print(f"{'='*50}")
        
        print("\nArquivos APÓS a renomeação:")
        print_detailed_structure(test_dir)
        
        # Análise dos resultados
        print(f"\n{'='*50}")
        print(f"ANÁLISE DE RESULTADOS:")
        print(f"{'='*50}")
        
        all_files_after = []
        for root, dirs, files in os.walk(test_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, test_dir)
                all_files_after.append((rel_path, file))
        
        # Verifica cada tipo de arquivo
        checks = [
            ("Arquivo principal .txt com L", "L05456.txt"),
            ("Arquivo L00125.txt renomeado", "L05456.txt"),
            ("Arquivos .jpg com novo número", "05456"),
            ("Arquivos no subdiretório", "05456"),
        ]
        
        for check_name, pattern in checks:
            found = [f for _, f in all_files_after if pattern in f]
            if found:
                print(f"✅ {check_name}: {found}")
            else:
                print(f"❌ {check_name}: NÃO ENCONTRADO")
        
        # Lista arquivos que podem não ter sido processados
        print(f"\n⚠️ ARQUIVOS QUE PODEM TER PROBLEMAS:")
        for rel_path, file_name in all_files_after:
            if "0000125" in file_name or "00125" in file_name:
                print(f"  - {rel_path} (ainda contém números antigos)")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

def print_detailed_structure(directory, indent=""):
    """
    Imprime estrutura detalhada com tamanhos
    """
    if not os.path.exists(directory):
        return
        
    items = sorted(os.listdir(directory))
    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path)
            print(f"{indent}📄 {item} ({size} bytes)")
        else:
            print(f"{indent}📁 {item}/")
            print_detailed_structure(item_path, indent + "  ")

if __name__ == "__main__":
    diagnostic_test()