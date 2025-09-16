#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste completo para debugar o fluxo exato da GUI
"""

import os
import tempfile
import shutil
from infraction_analyzer import InfractionAnalyzer
from file_renamer import FileRenamer

def test_full_flow_debug():
    """
    Testa o fluxo completo exatamente como acontece na GUI
    """
    print("=== Teste Completo do Fluxo da GUI ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_full_flow_")
    
    try:
        # Simula a estrutura exata que causa problemas
        # D:/Brascontrol/Opera_lote_4.0/L08685/0000125/AITs/arquivo.txt
        lote_dir = os.path.join(test_dir, "L08685")
        subdir_wrong = os.path.join(lote_dir, "0000125")  # Diretório errado
        aits_dir = os.path.join(subdir_wrong, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria arquivos exatamente como no caso real
        files_to_create = [
            (os.path.join(lote_dir, "L08685.txt"), "Dados do lote L08685"),
            (os.path.join(subdir_wrong, "data.txt"), "Dados 0000125"), 
            (os.path.join(aits_dir, "L08685.txt"), "0000125;BRI1306/2023;20250905;14:49:38;2;000;000,0;00125000070a.jpg;00125000070b.jpg;001306;Av Getulio Vargas x Durval Carneiro SCB;5673"),
            (os.path.join(aits_dir, "outro.txt"), "0000125;BRI1306/2023;20250905;15:30:22;1;000;000,0;00125000071a.jpg;00125000071b.jpg;001306;Rua Principal x Secundaria;6050"),
        ]
        
        for file_path, content in files_to_create:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(content)
        
        print(f"Estrutura inicial em: {test_dir}")
        print_structure(test_dir)
        
        # Etapa 1: Cria os objetos como na GUI
        print(f"\n{'='*60}")
        print(f"ETAPA 1: Criação dos objetos (como na GUI)")
        print(f"{'='*60}")
        
        file_renamer = FileRenamer(test_dir)
        infraction_analyzer = InfractionAnalyzer(test_dir)
        
        print(f"FileRenamer criado com diretório base: {test_dir}")
        print(f"InfractionAnalyzer criado com diretório base: {test_dir}")
        
        # Etapa 2: Executa rename_directory (como na GUI)
        print(f"\n{'='*60}")
        print(f"ETAPA 2: Executando rename_directory('L08685', 'L08685')")
        print(f"{'='*60}")
        print("Este é o caso especial onde old_name == new_name")
        print("Deveria corrigir a estrutura interna de 0000125 -> 0008685")
        
        # Esta é a chamada que acontece na GUI
        result = file_renamer.rename_directory("L08685", "L08685")
        print(f"Resultado do rename_directory: {result}")
        
        print(f"\nEstrutura após rename_directory:")
        print_structure(test_dir)
        
        # Etapa 3: Verifica se a estrutura foi corrigida
        print(f"\n{'='*60}")
        print(f"ETAPA 3: Verificando correção da estrutura")
        print(f"{'='*60}")
        
        expected_correct_dir = os.path.join(lote_dir, "0008685")
        expected_wrong_dir = os.path.join(lote_dir, "0000125")
        
        if os.path.exists(expected_correct_dir):
            print(f"✅ Diretório correto existe: {expected_correct_dir}")
        else:
            print(f"❌ Diretório correto NÃO existe: {expected_correct_dir}")
            
        if os.path.exists(expected_wrong_dir):
            print(f"⚠️  Diretório errado AINDA existe: {expected_wrong_dir}")
        else:
            print(f"✅ Diretório errado foi removido: {expected_wrong_dir}")
        
        # Etapa 4: Executa análise de infrações (como na GUI)
        print(f"\n{'='*60}")
        print(f"ETAPA 4: Executando análise de infrações")
        print(f"{'='*60}")
        
        # Esta é a chamada que acontece na GUI após a renomeação
        infraction_counts = infraction_analyzer.analyze_infractions("L08685")
        
        print(f"Contadores de infrações encontrados:")
        if infraction_counts:
            total = sum(infraction_counts.values())
            for code, count in infraction_counts.items():
                description = infraction_analyzer.get_infraction_description(code)
                print(f"  {code}: {count} ocorrências ({description})")
            print(f"  TOTAL: {total} infrações")
        else:
            print("  NENHUMA infração encontrada!")
            print("  Isso indica que os arquivos não estão nos diretórios esperados")
            
            # Debuga os diretórios de busca
            print(f"\n--- Debugando diretórios de busca ---")
            search_dirs = infraction_analyzer._get_search_directories("L08685")
            print(f"Diretórios onde o analyzer procura: {search_dirs}")
            
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    rel_path = os.path.relpath(search_dir, test_dir)
                    print(f"  Existe: {rel_path}")
                    txt_files = [f for f in os.listdir(search_dir) if f.endswith('.txt')]
                    if txt_files:
                        print(f"    Arquivos .txt: {txt_files}")
                    else:
                        print(f"    Arquivos .txt: (nenhum)")
                else:
                    print(f"  Não existe: {search_dir}")
        
        # Etapa 5: Simula o que deveria acontecer
        print(f"\n{'='*60}")
        print(f"ETAPA 5: Simulando correção manual (se necessário)")
        print(f"{'='*60}")
        
        # Se o diretório errado ainda existe, tenta corrigir manualmente
        if os.path.exists(expected_wrong_dir) and not os.path.exists(expected_correct_dir):
            print(f"Corrigindo manualmente: {expected_wrong_dir} -> {expected_correct_dir}")
            os.rename(expected_wrong_dir, expected_correct_dir)
            
            print(f"\nEstrutura após correção manual:")
            print_structure(test_dir)
            
            # Testa novamente a análise
            print(f"\nTestando análise após correção manual:")
            infraction_counts_after_fix = infraction_analyzer.analyze_infractions("L08685")
            
            if infraction_counts_after_fix:
                total = sum(infraction_counts_after_fix.values())
                for code, count in infraction_counts_after_fix.items():
                    description = infraction_analyzer.get_infraction_description(code)
                    print(f"  {code}: {count} ocorrências ({description})")
                print(f"  TOTAL: {total} infrações")
            else:
                print("  AINDA NENHUMA infração encontrada!")
        
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
    test_full_flow_debug()