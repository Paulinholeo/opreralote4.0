#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste exato do problema relatado com L08685
"""

import os
import tempfile
import shutil
from infraction_analyzer import InfractionAnalyzer
from file_renamer import FileRenamer

def test_l08685_exact_issue():
    """
    Testa exatamente o problema relatado com L08685
    """
    print("=== Teste Exato do Problema L08685 ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_l08685_exact_")
    
    try:
        # Reproduzindo EXATAMENTE a estrutura relatada:
        # "Arquivo processado: D:/.../L08685/0000125/AITs/L08685.txt"
        # "Deveria ser:       D:/.../L08685/0008685/AITs/L08685.txt"
        
        lote_dir = os.path.join(test_dir, "L08685")
        subdir_wrong = os.path.join(lote_dir, "0000125")  # Diretório errado
        aits_dir = os.path.join(subdir_wrong, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria o arquivo exatamente como relatado
        l08685_txt_path = os.path.join(aits_dir, "L08685.txt")
        with open(l08685_txt_path, "w", encoding='utf-8') as f:
            # Conteúdo com infrações
            f.write("0000125;BRI1306/2023;20250905;14:49:38;2;000;000,0;00125000070a.jpg;00125000070b.jpg;001306;Av Getulio Vargas x Durval Carneiro SCB;5673\n")
            f.write("0000125;BRI1306/2023;20250905;15:30:22;1;000;000,0;00125000071a.jpg;00125000071b.jpg;001306;Rua Principal x Secundaria;6050\n")
            f.write("0000125;BRI1306/2023;20250905;16:15:45;3;000;000,0;00125000073a.jpg;00125000073b.jpg;001306;Via Expressa;7587\n")
        
        print(f"Estrutura inicial (PROBLEMA):")
        print(f"Diretório base: {test_dir}")
        print_structure(test_dir)
        
        # Etapa 1: Simula exatamente o que acontece na GUI
        print(f"\n{'='*70}")
        print(f"ETAPA 1: Simulando exatamente o que acontece na GUI")
        print(f"{'='*70}")
        
        # Cria os objetos como na GUI
        file_renamer = FileRenamer(test_dir)
        infraction_analyzer = InfractionAnalyzer(test_dir)
        
        print(f"1. FileRenamer criado com diretório: {test_dir}")
        print(f"2. InfractionAnalyzer criado com diretório: {test_dir}")
        
        # Etapa 2: Executa exatamente o que a GUI faz
        print(f"\n3. Executando: file_renamer.rename_directory('L08685', 'L08685')")
        print(f"   (Este é o caso especial onde old_name == new_name)")
        
        rename_result = file_renamer.rename_directory("L08685", "L08685")
        print(f"   Resultado: {rename_result}")
        
        print(f"\nEstrutura após rename_directory:")
        print_structure(test_dir)
        
        # Etapa 3: Verifica se a estrutura foi corrigida
        print(f"\n{'='*70}")
        print(f"ETAPA 3: Verificando correção da estrutura")
        print(f"{'='*70}")
        
        subdir_correct = os.path.join(lote_dir, "0008685")  # Diretório correto
        
        if os.path.exists(subdir_correct):
            print(f"✅ DIRETÓRIO CORRETO EXISTE: {subdir_correct}")
            aits_correct = os.path.join(subdir_correct, "AITs")
            if os.path.exists(aits_correct):
                print(f"✅ DIRETÓRIO AITs CORRETO EXISTE: {aits_correct}")
                l08685_file_correct = os.path.join(aits_correct, "L08685.txt")
                if os.path.exists(l08685_file_correct):
                    print(f"✅ ARQUIVO L08685.txt CORRETO EXISTE: {l08685_file_correct}")
                else:
                    print(f"❌ ARQUIVO L08685.txt CORRETO NÃO EXISTE")
            else:
                print(f"❌ DIRETÓRIO AITs CORRETO NÃO EXISTE")
        else:
            print(f"❌ DIRETÓRIO CORRETO NÃO EXISTE: {subdir_correct}")
            
        if os.path.exists(subdir_wrong):
            print(f"⚠️  DIRETÓRIO ERRADO AINDA EXISTE: {subdir_wrong}")
        else:
            print(f"✅ DIRETÓRIO ERRADO FOI REMOVIDO: {subdir_wrong}")
        
        # Etapa 4: Executa análise de infrações como na GUI
        print(f"\n{'='*70}")
        print(f"ETAPA 4: Executando análise de infrações (como na GUI)")
        print(f"{'='*70}")
        
        print(f"Executando: infraction_analyzer.analyze_infractions('L08685')")
        infraction_counts = infraction_analyzer.analyze_infractions("L08685")
        
        print(f"\nContadores de infrações encontrados:")
        if infraction_counts:
            total = sum(infraction_counts.values())
            for code, count in infraction_counts.items():
                description = infraction_analyzer.get_infraction_description(code)
                print(f"  {code}: {count} ocorrências ({description})")
            print(f"  TOTAL: {total} infrações")
            
            if total > 0:
                print(f"\n✅ SUCESSO! As infrações foram encontradas corretamente!")
                print(f"   Isso significa que o problema NÃO está na análise de infrações.")
                print(f"   O problema pode estar em outro lugar do fluxo.")
            else:
                print(f"\n❌ FALHA! Nenhuma infração encontrada apesar de existirem arquivos.")
                print(f"   Isso indica um problema na lógica de busca.")
        else:
            print(f"  NENHUMA infração encontrada!")
            print(f"  Isso é um problema que precisa ser investigado.")
            
            # Debug detalhado dos diretórios de busca
            print(f"\n--- Debug detalhado dos diretórios de busca ---")
            search_dirs = infraction_analyzer._get_search_directories("L08685")
            print(f"Diretórios onde o analyzer procura: {search_dirs}")
            
            for i, search_dir in enumerate(search_dirs):
                print(f"\n  {i+1}. Verificando diretório: {search_dir}")
                if os.path.exists(search_dir):
                    rel_path = os.path.relpath(search_dir, test_dir)
                    print(f"     Relativo: {rel_path}")
                    print(f"     Existe: SIM")
                    
                    # Lista arquivos .txt
                    txt_files = [f for f in os.listdir(search_dir) if f.endswith('.txt')]
                    if txt_files:
                        print(f"     Arquivos .txt encontrados: {txt_files}")
                        # Verifica conteúdo dos arquivos
                        for txt_file in txt_files:
                            txt_path = os.path.join(search_dir, txt_file)
                            try:
                                with open(txt_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    lines = content.strip().split('\n')
                                    print(f"       {txt_file}: {len(lines)} linhas")
                                    for j, line in enumerate(lines[:3]):  # Mostra as 3 primeiras linhas
                                        if line.strip():
                                            parts = line.split(';')
                                            if len(parts) > 0:
                                                code = parts[-1].strip()
                                                if code.isdigit():
                                                    print(f"         Linha {j+1}: código {code}")
                            except Exception as e:
                                print(f"       Erro ao ler {txt_file}: {e}")
                    else:
                        print(f"     Arquivos .txt encontrados: (nenhum)")
                else:
                    print(f"     Existe: NÃO")
        
        # Etapa 5: Simula o resto do fluxo da GUI
        print(f"\n{'='*70}")
        print(f"ETAPA 5: Simulando o resto do fluxo da GUI")
        print(f"{'='*70}")
        
        print(f"Executando: file_renamer.rename_files('L08685', 'L08685')")
        file_renamer.rename_files("L08685", "L08685")
        
        print(f"Executando: file_renamer.rename_text_content('L08685', 'L08685')")
        file_renamer.rename_text_content("L08685", "L08685")
        
        print(f"\nEstrutura final:")
        print_structure(test_dir)
        
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
    test_l08685_exact_issue()