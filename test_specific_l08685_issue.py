#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para reproduzir o problema relatado com L08685
"""

import os
import tempfile
import shutil
from infraction_analyzer import InfractionAnalyzer
from file_renamer import FileRenamer

def test_l08685_specific_issue():
    """
    Testa o problema específico relatado com L08685
    """
    print("=== Teste Específico L08685 ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_l08685_")
    
    try:
        # Reproduzindo exatamente a estrutura relatada:
        # D:/Brascontrol/Opera_lote_4.0/L08685/0000125/AITs/L08685.txt
        lote_dir = os.path.join(test_dir, "L08685")
        subdir_0000125 = os.path.join(lote_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria o arquivo exatamente como relatado
        l08685_txt_path = os.path.join(aits_dir, "L08685.txt")
        with open(l08685_txt_path, "w", encoding='utf-8') as f:
            # Conteúdo típico de um arquivo AIT com infrações
            f.write("0000125;BRI1306/2023;20250905;14:49:38;2;000;000,0;00125000070a.jpg;00125000070b.jpg;001306;Av Getulio Vargas x Durval Carneiro SCB;5673\n")
            f.write("0000125;BRI1306/2023;20250905;15:30:22;1;000;000,0;00125000071a.jpg;00125000071b.jpg;001306;Rua Principal x Secundaria;6050\n")
        
        print(f"Estrutura criada em: {test_dir}")
        print("Arquivos criados:")
        print_structure(test_dir)
        
        # Testa o InfractionAnalyzer com o diretório base correto
        print(f"\n{'='*60}")
        print(f"TESTANDO InfractionAnalyzer com diretório base: {test_dir}")
        print(f"{'='*60}")
        
        analyzer = InfractionAnalyzer(test_dir)
        infraction_counts = analyzer.analyze_infractions("L08685")
        
        print(f"\nContadores de infrações encontrados:")
        if infraction_counts:
            for code, count in infraction_counts.items():
                description = analyzer.get_infraction_description(code)
                print(f"  {code}: {count} ocorrências ({description})")
        else:
            print("  NENHUMA infração encontrada!")
            print("  Isso indica que o analyzer não está encontrando os arquivos")
            
            # Vamos debugar os diretórios que ele está procurando
            print(f"\n--- Debugando diretórios de busca ---")
            search_dirs = analyzer._get_search_directories("L08685")
            print(f"Diretórios onde o analyzer procura: {search_dirs}")
            
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    print(f"  Conteúdo de {search_dir}:")
                    for item in os.listdir(search_dir):
                        item_path = os.path.join(search_dir, item)
                        if os.path.isfile(item_path):
                            print(f"    📄 {item}")
                        else:
                            print(f"    📁 {item}/")
                else:
                    print(f"  Diretório não existe: {search_dir}")
        
        # Agora vamos testar o que acontece quando corrigimos o diretório
        print(f"\n{'='*60}")
        print(f"SIMULANDO CORREÇÃO DO DIRETÓRIO")
        print(f"{'='*60}")
        
        # O diretório correto deveria ser 0008685, não 0000125
        subdir_0008685 = os.path.join(lote_dir, "0008685")
        
        if os.path.exists(subdir_0000125) and not os.path.exists(subdir_0008685):
            print(f"Renomeando diretório: {subdir_0000125} -> {subdir_0008685}")
            os.rename(subdir_0000125, subdir_0008685)
            
            # Move também o arquivo para o novo diretório
            new_aits_dir = os.path.join(subdir_0008685, "AITs")
            new_l08685_txt_path = os.path.join(new_aits_dir, "L08685.txt")
            
            print(f"Arquivo movido para: {new_l08685_txt_path}")
        
        print("\nEstrutura após correção:")
        print_structure(test_dir)
        
        # Testa novamente após correção
        print(f"\n{'='*60}")
        print(f"ANÁLISE APÓS CORREÇÃO DO DIRETÓRIO")
        print(f"{'='*60}")
        
        infraction_counts_after = analyzer.analyze_infractions("L08685")
        
        print(f"Contadores de infrações após correção:")
        if infraction_counts_after:
            for code, count in infraction_counts_after.items():
                description = analyzer.get_infraction_description(code)
                print(f"  {code}: {count} ocorrências ({description})")
        else:
            print("  AINDA NENHUMA infração encontrada!")
            
            # Debuga novamente os diretórios
            print(f"\n--- Debugando diretórios de busca após correção ---")
            search_dirs = analyzer._get_search_directories("L08685")
            print(f"Diretórios onde o analyzer procura: {search_dirs}")
            
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    print(f"  Conteúdo de {search_dir}:")
                    for item in os.listdir(search_dir):
                        item_path = os.path.join(search_dir, item)
                        if os.path.isfile(item_path):
                            print(f"    📄 {item}")
                        else:
                            print(f"    📁 {item}/")
                else:
                    print(f"  Diretório não existe: {search_dir}")
            
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
    test_l08685_specific_issue()