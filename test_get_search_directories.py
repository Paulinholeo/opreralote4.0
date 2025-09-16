#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para entender como _get_search_directories funciona
"""

import os
import tempfile
import shutil
from infraction_analyzer import InfractionAnalyzer

def test_get_search_directories():
    """
    Testa a função _get_search_directories para entender como ela encontra diretórios
    """
    print("=== Teste _get_search_directories ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_search_dirs_")
    
    try:
        # Cria uma estrutura complexa
        lote_dir = os.path.join(test_dir, "L08685")
        subdir_0000125 = os.path.join(lote_dir, "0000125")
        subdir_0008685 = os.path.join(lote_dir, "0008685")
        aits_dir_old = os.path.join(subdir_0000125, "AITs")
        aits_dir_new = os.path.join(subdir_0008685, "AITs")
        
        # Cria ambos os diretórios para testar
        os.makedirs(aits_dir_old, exist_ok=True)
        # os.makedirs(aits_dir_new, exist_ok=True)  # Não cria o novo ainda
        
        # Cria arquivos de teste
        test_files = [
            (os.path.join(lote_dir, "L08685.txt"), "arquivo no diretório principal"),
            (os.path.join(subdir_0000125, "0000125.txt"), "arquivo no subdiretório errado"),
            (os.path.join(aits_dir_old, "teste.txt"), "arquivo no AITs errado"),
        ]
        
        for file_path, content in test_files:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content)
        
        print(f"Estrutura criada em: {test_dir}")
        print_structure(test_dir)
        
        # Testa o InfractionAnalyzer
        analyzer = InfractionAnalyzer(test_dir)
        
        print(f"\n{'='*50}")
        print(f"EXECUTANDO _get_search_directories('L08685')")
        print(f"{'='*50}")
        
        search_dirs = analyzer._get_search_directories("L08685")
        print(f"Diretórios encontrados: {search_dirs}")
        
        # Verifica cada diretório
        for i, search_dir in enumerate(search_dirs):
            print(f"\n{i+1}. Verificando diretório: {search_dir}")
            if os.path.exists(search_dir):
                rel_path = os.path.relpath(search_dir, test_dir)
                print(f"   Relativo: {rel_path}")
                print(f"   Existe: SIM")
                items = os.listdir(search_dir)
                if items:
                    print(f"   Conteúdo: {items}")
                else:
                    print(f"   Conteúdo: (vazio)")
            else:
                print(f"   Existe: NÃO")
        
        # Agora cria o diretório correto e move arquivos
        print(f"\n{'='*50}")
        print(f"CRIANDO ESTRUTURA CORRETA")
        print(f"{'='*50}")
        
        # Cria o diretório correto
        os.makedirs(subdir_0008685, exist_ok=True)
        os.makedirs(aits_dir_new, exist_ok=True)
        
        # Move arquivos do diretório errado para o correto
        if os.path.exists(aits_dir_old):
            for item in os.listdir(aits_dir_old):
                old_path = os.path.join(aits_dir_old, item)
                new_path = os.path.join(aits_dir_new, item)
                print(f"Movendo: {old_path} -> {new_path}")
                shutil.move(old_path, new_path)
        
        print("\nEstrutura após correção:")
        print_structure(test_dir)
        
        # Testa novamente
        print(f"\n{'='*50}")
        print(f"EXECUTANDO _get_search_directories('L08685') APÓS CORREÇÃO")
        print(f"{'='*50}")
        
        search_dirs_after = analyzer._get_search_directories("L08685")
        print(f"Diretórios encontrados: {search_dirs_after}")
        
        # Verifica cada diretório
        for i, search_dir in enumerate(search_dirs_after):
            print(f"\n{i+1}. Verificando diretório: {search_dir}")
            if os.path.exists(search_dir):
                rel_path = os.path.relpath(search_dir, test_dir)
                print(f"   Relativo: {rel_path}")
                print(f"   Existe: SIM")
                items = os.listdir(search_dir)
                if items:
                    print(f"   Conteúdo: {items}")
                else:
                    print(f"   Conteúdo: (vazio)")
            else:
                print(f"   Existe: NÃO")
                
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
            size = os.path.getsize(item_path)
            print(f"{indent}📄 {item} ({size} bytes)")
        else:
            print(f"{indent}📁 {item}/")
            print_structure(item_path, indent + "  ")

if __name__ == "__main__":
    test_get_search_directories()