#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug detalhado da função rename_files
"""

import os
import tempfile
import shutil
import glob

def debug_rename_logic():
    """
    Debug manual da lógica de renomeação
    """
    print("=== Debug Detalhado da Lógica ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="debug_detailed_")
    
    try:
        # Cria estrutura: L05456/05456.txt
        lote_dir = os.path.join(test_dir, "L05456")
        os.makedirs(lote_dir, exist_ok=True)
        
        problem_file = os.path.join(lote_dir, "05456.txt")
        with open(problem_file, "w") as f:
            f.write("05456;data;test")
        
        # Simula exatamente o que a função faz
        directory = test_dir
        old_name = "L0000125"
        new_name = "L05456"
        
        old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
        new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
        
        print(f"Diretório: {directory}")
        print(f"old_name: {old_name}")
        print(f"new_name: {new_name}")
        print(f"old_name_number: {old_name_number}")
        print(f"new_name_number: {new_name_number}")
        
        # Define os diretórios onde procurar arquivos
        search_directories = [os.path.join(directory, new_name)]
        
        # Se há estrutura com AITs, adiciona os subdiretórios à busca
        main_dir = os.path.join(directory, new_name)
        if os.path.exists(main_dir):
            for item in os.listdir(main_dir):
                item_path = os.path.join(main_dir, item)
                if os.path.isdir(item_path):
                    search_directories.append(item_path)
                    # Adiciona também subdiretórios de AITs se existirem
                    aits_path = os.path.join(item_path, 'AITs')
                    if os.path.exists(aits_path):
                        search_directories.append(aits_path)
        
        print(f"\nDiretórios de busca: {search_directories}")
        
        # Processa arquivos em todos os diretórios relevantes
        for search_dir in search_directories:
            if not os.path.exists(search_dir):
                print(f"Pulando diretório inexistente: {search_dir}")
                continue
                
            print(f"\nProcessando diretório: {search_dir}")
            
            files_in_dir = glob.glob(os.path.join(search_dir, '*'))
            print(f"Arquivos encontrados: {files_in_dir}")
            
            for filename in files_in_dir:
                base_filename = os.path.basename(filename)
                print(f"\n  Processando arquivo: {base_filename}")
                
                # Pula diretórios
                if os.path.isdir(filename):
                    print(f"    -> Pulando (é diretório)")
                    continue
                
                # Verifica se o arquivo contém o número antigo (mais flexível)
                contains_old_number = False
                processed_by_special_logic = False
                file_ext = os.path.splitext(base_filename)[1]
                file_name_without_ext = os.path.splitext(base_filename)[0]
                
                print(f"    file_ext: {file_ext}")
                print(f"    file_name_without_ext: {file_name_without_ext}")
                
                if old_name_number in base_filename:
                    contains_old_number = True
                    print(f"    -> Condição 1: TRUE (old_name_number in base_filename)")
                # Verifica padrões como "L00125" quando old_name_number é "0000125"
                if not contains_old_number and len(old_name_number) >= 6 and old_name_number.startswith('00'):
                    old_number_trimmed = old_name_number.lstrip('0')
                    if f"L{old_number_trimmed.zfill(5)}" in base_filename or f"L00{old_number_trimmed}" in base_filename:
                        contains_old_number = True
                        processed_by_special_logic = True
                        print(f"    -> Condição 2: TRUE (padrão L00XXX)")
                    else:
                        print(f"    -> Condição 2: FALSE")
                # Verifica padrão reverso: se old_name contém "L" e arquivo contém número
                if not contains_old_number and old_name.startswith('L') and any(part in base_filename for part in [old_name_number, old_name_number.lstrip('0')]):
                    contains_old_number = True
                    print(f"    -> Condição 3: TRUE (padrão reverso)")
                elif not contains_old_number:
                    print(f"    -> Condição 3: FALSE")
                # Caso especial: arquivo .txt sem prefixo L quando new_name tem L
                if not contains_old_number and (file_ext == '.txt' and new_name.startswith('L') and 
                      not file_name_without_ext.startswith('L') and
                      file_name_without_ext == new_name[1:]):
                    contains_old_number = True
                    processed_by_special_logic = True
                    print(f"    -> Condição 4: TRUE (caso especial .txt)")
                    print(f"       file_ext == '.txt': {file_ext == '.txt'}")
                    print(f"       new_name.startswith('L'): {new_name.startswith('L')}")
                    print(f"       not file_name_without_ext.startswith('L'): {not file_name_without_ext.startswith('L')}")
                    print(f"       file_name_without_ext == new_name[1:]: {file_name_without_ext} == {new_name[1:]} = {file_name_without_ext == new_name[1:]}")
                elif not contains_old_number:
                    print(f"    -> Condição 4: FALSE")
                    print(f"       file_ext == '.txt': {file_ext == '.txt'}")
                    print(f"       new_name.startswith('L'): {new_name.startswith('L')}")
                    print(f"       not file_name_without_ext.startswith('L'): {not file_name_without_ext.startswith('L')}")
                    print(f"       file_name_without_ext == new_name[1:]: {file_name_without_ext} == {new_name[1:]} = {file_name_without_ext == new_name[1:]}")
                
                print(f"    contains_old_number: {contains_old_number}")
                print(f"    processed_by_special_logic: {processed_by_special_logic}")
                
                if contains_old_number:
                    print(f"    -> PROCESSANDO ARQUIVO...")
                    
                    # Calcula o novo nome do arquivo
                    dir_name = os.path.dirname(filename)
                    
                    # Lógica de renomeação mais robusta
                    new_file_name_without_ext = file_name_without_ext
                    
                    print(f"    Lógica de renomeação:")
                    
                    # Casos especiais para arquivos com padrão "L00125"
                    if file_name_without_ext.startswith('L00') and len(file_name_without_ext) >= 6:
                        new_file_name_without_ext = f"L{new_name_number}"
                        processed_by_special_logic = True
                        print(f"      -> Caso L00XXX: {new_file_name_without_ext}")
                    # Caso especial: arquivo sem L que deveria ter L
                    elif (file_ext == '.txt' and new_name.startswith('L') and 
                          not file_name_without_ext.startswith('L') and
                          file_name_without_ext == new_name[1:]):
                        new_file_name_without_ext = new_name
                        processed_by_special_logic = True
                        print(f"      -> Caso especial .txt: {new_file_name_without_ext}")
                    # Caso padrão
                    elif old_name_number in file_name_without_ext:
                        if len(old_name_number) >= 6:
                            new_file_name_without_ext = file_name_without_ext.replace(old_name_number, new_name_number.zfill(7))
                        else:
                            new_file_name_without_ext = file_name_without_ext.replace(old_name_number, new_name_number)
                        print(f"      -> Caso padrão: {new_file_name_without_ext}")
                    else:
                        old_trimmed = old_name_number.lstrip('0')
                        if old_trimmed in file_name_without_ext:
                            new_trimmed = new_name_number.lstrip('0')
                            new_file_name_without_ext = file_name_without_ext.replace(old_trimmed, new_trimmed)
                            print(f"      -> Caso trimmed: {new_file_name_without_ext}")
                    
                    new_filename = os.path.join(dir_name, new_file_name_without_ext + file_ext)
                    print(f"    -> Nome final: {new_filename}")
                    
                    if filename != new_filename:
                        print(f"    -> RENOMEANDO: {filename} -> {new_filename}")
                        os.rename(filename, new_filename)
                    else:
                        print(f"    -> SEM ALTERAÇÃO (nomes iguais)")
                else:
                    print(f"    -> ARQUIVO IGNORADO")
        
        print(f"\n{'='*50}")
        print(f"RESULTADO FINAL:")
        print(f"{'='*50}")
        
        final_files = os.listdir(lote_dir)
        print(f"Arquivos finais: {final_files}")
        
        if "L05456.txt" in final_files:
            print("✅ SUCESSO: Arquivo renomeado")
        else:
            print("❌ FALHA: Arquivo não renomeado")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    debug_rename_logic()