#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para debugar o problema de busca no diretório errado
"""

import os
import tempfile
import shutil
from infraction_analyzer import InfractionAnalyzer
from file_renamer import FileRenamer

def test_directory_search_issue():
    """
    Testa o problema de busca no diretório errado
    """
    print("=== Teste de Problema de Diretório ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="debug_directory_")
    
    try:
        # Simula estrutura real com problema de diretório
        # Estrutura correta: L08685/0008685/AITs/arquivo.txt
        # Estrutura errada: L08685/0000125/AITs/arquivo.txt (não renomeado)
        lote_dir = os.path.join(test_dir, "L08685")
        subdir_wrong = os.path.join(lote_dir, "0000125")  # Diretório errado
        aits_dir = os.path.join(subdir_wrong, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria arquivos com infrações no diretório errado
        test_files = {
            os.path.join(aits_dir, "teste_infraction.txt"): "0000125;data;5673\n0000125;data2;6050\n0000125;data3;7587",
        }
        
        for file_path, content in test_files.items():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(content)
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Arquivos ANTES da correção:")
        print_structure(test_dir)
        
        # Testa o InfractionAnalyzer
        analyzer = InfractionAnalyzer(test_dir)
        
        print(f"\n{'='*50}")
        print(f"EXECUTANDO ANÁLISE DE INFRAÇÕES")
        print(f"{'='*50}")
        
        # Aqui está o problema - o analyzer está procurando no diretório errado
        infraction_counts = analyzer.analyze_infractions("L08685")
        
        print(f"\nContadores de infrações encontrados:")
        if infraction_counts:
            for code, count in infraction_counts.items():
                description = analyzer.get_infraction_description(code)
                print(f"  {code}: {count} ocorrências ({description})")
        else:
            print("  Nenhuma infração encontrada!")
            print("  PROVAVELMENTE porque está procurando no diretório errado")
        
        # Agora vamos testar a correção do diretório
        print(f"\n{'='*50}")
        print(f"TESTANDO CORREÇÃO DO DIRETÓRIO")
        print(f"{'='*50}")
        
        # Simula a correção do diretório (o que deveria acontecer no rename_directory)
        correct_subdir = os.path.join(lote_dir, "0008685")
        if os.path.exists(subdir_wrong) and not os.path.exists(correct_subdir):
            print(f"Corrigindo diretório: {subdir_wrong} -> {correct_subdir}")
            os.rename(subdir_wrong, correct_subdir)
            
            # Também corrige o AITs
            wrong_aits = os.path.join(correct_subdir, "AITs")
            if os.path.exists(wrong_aits):
                print(f"Diretório AITs já está no lugar certo")
        
        print("\nEstrutura APÓS correção:")
        print_structure(test_dir)
        
        # Testa novamente após correção
        print(f"\n{'='*50}")
        print(f"ANÁLISE APÓS CORREÇÃO")
        print(f"{'='*50}")
        
        infraction_counts_after = analyzer.analyze_infractions("L08685")
        
        print(f"Contadores de infrações após correção:")
        if infraction_counts_after:
            for code, count in infraction_counts_after.items():
                description = analyzer.get_infraction_description(code)
                print(f"  {code}: {count} ocorrências ({description})")
        else:
            print("  Ainda nenhuma infração encontrada!")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

def print_structure(directory, indent=""):
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
            print_structure(item_path, indent + "  ")

if __name__ == "__main__":
    test_directory_search_issue()