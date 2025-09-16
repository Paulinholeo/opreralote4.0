#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar a funcionalidade de renomeação com subdiretórios AITs
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer
from text_file_editor import TextFileEditor

def create_test_structure():
    """
    Cria uma estrutura de teste que simula o caso real:
    test_dir/
    └── 0000126/
        └── AITs/
            ├── arquivo1.txt
            └── foto1.jpg
    """
    # Cria diretório temporário para teste
    test_dir = tempfile.mkdtemp(prefix="test_operalote_")
    
    # Cria estrutura de diretórios
    lote_dir = os.path.join(test_dir, "0000126")
    aits_dir = os.path.join(lote_dir, "AITs")
    os.makedirs(aits_dir, exist_ok=True)
    
    # Cria alguns arquivos de teste
    with open(os.path.join(aits_dir, "0000126001.txt"), "w") as f:
        f.write("0000126;data1;info;;;;;arquivo0000126001.jpg;arquivo0000126002.jpg;foto0000126001.jpg;foto0000126002.jpg")
    
    with open(os.path.join(lote_dir, "0000126.txt"), "w") as f:
        f.write("0000126;data2;info;;;;;arquivo0000126.jpg;arquivo0000126b.jpg;foto0000126.jpg;foto0000126b.jpg")
    
    # Cria arquivos jpg de teste (vazios)
    open(os.path.join(aits_dir, "0000126001.jpg"), "w").close()
    open(os.path.join(lote_dir, "0000126.jpg"), "w").close()
    
    print(f"Estrutura de teste criada em: {test_dir}")
    print("Estrutura antes da renomeação:")
    print_directory_structure(test_dir)
    
    return test_dir

def print_directory_structure(directory, indent=""):
    """
    Imprime a estrutura de diretórios de forma hierárquica
    """
    items = sorted(os.listdir(directory))
    for item in items:
        item_path = os.path.join(directory, item)
        print(f"{indent}├── {item}")
        if os.path.isdir(item_path):
            print_directory_structure(item_path, indent + "│   ")

def test_aits_functionality():
    """
    Testa a funcionalidade de renomeação com AITs
    """
    print("=== Teste de Funcionalidade AITs ===\n")
    
    # Cria estrutura de teste
    test_dir = create_test_structure()
    
    try:
        # Inicializa o FileRenamer
        file_renamer = FileRenamer(test_dir)
        text_editor = TextFileEditor(test_dir)
        
        # Testa a detecção de AITs
        old_dir_path = os.path.join(test_dir, "0000126")
        has_aits = file_renamer.has_aits_subdirectory(old_dir_path)
        print(f"\nDetecção de AITs: {'✓' if has_aits else '✗'} ({'Encontrado' if has_aits else 'Não encontrado'})")
        
        # Executa a renomeação
        print(f"\nRenomeando '0000126' para 'L02504'...")
        success = file_renamer.rename_directory("0000126", "L02504")
        
        if success:
            print("✓ Renomeação do diretório principal realizada com sucesso")
            
            # Executa renomeação de arquivos
            file_renamer.rename_files("0000126", "L02504")
            print("✓ Renomeação de arquivos realizada")
            
            # Executa renomeação do conteúdo dos arquivos de texto
            file_renamer.rename_text_content("0000126", "L02504")
            text_editor.edit_text_content("0000126", "L02504")
            print("✓ Atualização do conteúdo dos arquivos realizada")
            
            print("\nEstrutura após a renomeação:")
            print_directory_structure(test_dir)
            
            # Verifica se a estrutura está correta
            # Primeiro verifica a estrutura com nome completo: L02504/L02504/AITs
            expected_structure_full = os.path.join(test_dir, "L02504", "L02504", "AITs")
            # Depois verifica estrutura com número apenas: L02504/02504/AITs  
            expected_structure_num = os.path.join(test_dir, "L02504", "02504", "AITs")
            # E estrutura alternativa: L02504/AITs
            alt_structure = os.path.join(test_dir, "L02504", "AITs")
            
            if os.path.exists(expected_structure_full):
                print("\n✓ SUCESSO: Estrutura AITs renomeada corretamente (nome completo)!")
                print(f"  Diretório criado: {expected_structure_full}")
            elif os.path.exists(expected_structure_num):
                print("\n✓ SUCESSO: Estrutura AITs renomeada corretamente (número do lote)!")
                print(f"  Diretório criado: {expected_structure_num}")
            elif os.path.exists(alt_structure):
                print("\n✓ SUCESSO: Estrutura AITs encontrada (estrutura alternativa)!")
                print(f"  Diretório criado: {alt_structure}")
            else:
                print("\n✗ ERRO: Estrutura AITs não foi renomeada corretamente")
                    
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
            print(f"\nDiretório de teste removido: {test_dir}")
        except Exception as e:
            print(f"Aviso: Não foi possível remover o diretório de teste: {e}")

if __name__ == "__main__":
    test_aits_functionality()