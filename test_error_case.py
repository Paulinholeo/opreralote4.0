#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para o caso que estava gerando erro:
FileNotFoundError: [WinError 3] The system cannot find the path specified: 
'D:/Brascontrol/Opera_lote_4.0\\L02543\\0000125\\AITs\\0000125.log' 
-> 'D:/Brascontrol/Opera_lote_4.0\\L02543\\00002543\\AITs\\00002543.log'
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer
from text_file_editor import TextFileEditor

def create_error_case_structure():
    """
    Cria a estrutura exata que estava causando o erro:
    test_dir/
    └── L02543/
        └── 0000125/
            └── AITs/
                └── 0000125.log
    """
    # Cria diretório temporário para teste
    test_dir = tempfile.mkdtemp(prefix="test_error_case_")
    
    # Cria estrutura de diretórios como no erro
    lote_dir = os.path.join(test_dir, "L02543")
    internal_dir = os.path.join(lote_dir, "0000125")
    aits_dir = os.path.join(internal_dir, "AITs")
    os.makedirs(aits_dir, exist_ok=True)
    
    # Cria o arquivo que estava causando problema
    log_file = os.path.join(aits_dir, "0000125.log")
    with open(log_file, "w") as f:
        f.write("Log file content for test")
    
    print(f"Estrutura de teste criada em: {test_dir}")
    print("Estrutura simulando o erro:")
    print_directory_structure(test_dir)
    
    return test_dir

def print_directory_structure(directory, indent=""):
    """
    Imprime a estrutura de diretórios de forma hierárquica
    """
    if not os.path.exists(directory):
        print(f"{indent}[DIRECTORY NOT FOUND: {directory}]")
        return
        
    items = sorted(os.listdir(directory))
    for item in items:
        item_path = os.path.join(directory, item)
        print(f"{indent}├── {item}")
        if os.path.isdir(item_path):
            print_directory_structure(item_path, indent + "│   ")

def test_error_case():
    """
    Testa o caso específico que estava gerando erro
    """
    print("=== Teste do Caso de Erro Específico ===\n")
    
    # Cria estrutura de teste
    test_dir = create_error_case_structure()
    
    try:
        # Muda o diretório de trabalho do FileRenamer para o diretório de teste
        file_renamer = FileRenamer(test_dir)
        text_editor = TextFileEditor(test_dir)
        
        print(f"\nExecutando renomeação de 'L02543' para um novo nome...")
        
        # O problema era que a função tentava renomear a estrutura interna
        # mas o diretório "00002543" não existia ainda
        
        # Simula a situação: tentar renomear arquivos dentro de L02543/0000125/AITs/
        old_name = "L02543"  # Nome do lote atual
        new_name = "L02999"  # Novo nome desejado
        
        # Primeiro, testa a detecção de AITs
        old_dir_path = os.path.join(test_dir, old_name)
        has_aits = file_renamer.has_aits_subdirectory(old_dir_path)
        print(f"Detecção de AITs: {'✓' if has_aits else '✗'} ({'Encontrado' if has_aits else 'Não encontrado'})")
        
        # Executa a renomeação completa
        print(f"\\nRenomeando '{old_name}' para '{new_name}'...")
        success = file_renamer.rename_directory(old_name, new_name)
        
        if success:
            print("✓ Renomeação do diretório principal realizada com sucesso")
            
            # Executa renomeação de arquivos (aqui estava o erro)
            print("Executando renomeação de arquivos...")
            file_renamer.rename_files(old_name, new_name)
            print("✓ Renomeação de arquivos realizada sem erro")
            
            print("\\nEstrutura após a renomeação:")
            print_directory_structure(test_dir)
            
            # Verifica se o arquivo .log foi renomeado corretamente
            expected_log_path = None
            for root, dirs, files in os.walk(test_dir):
                for file in files:
                    if file.endswith('.log'):
                        expected_log_path = os.path.join(root, file)
                        break
                if expected_log_path:
                    break
            
            if expected_log_path and "02999" in expected_log_path:
                print(f"\\n✓ SUCESSO: Arquivo .log renomeado corretamente!")
                print(f"  Arquivo encontrado: {expected_log_path}")
            else:
                print(f"\\n⚠ Aviso: Arquivo .log não encontrado ou não renomeado")
                if expected_log_path:
                    print(f"  Arquivo encontrado: {expected_log_path}")
                    
        else:
            print("✗ Falha na renomeação do diretório")
            
    except Exception as e:
        print(f"✗ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Limpa o diretório de teste
        try:
            shutil.rmtree(test_dir)
            print(f"\\nDiretório de teste removido: {test_dir}")
        except Exception as e:
            print(f"Aviso: Não foi possível remover o diretório de teste: {e}")

if __name__ == "__main__":
    test_error_case()