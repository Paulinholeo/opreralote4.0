#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar a correção do problema com dígitos em arquivos JPG
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_jpg_digit_issue():
    """
    Testa o problema específico com arquivos JPG que não estão sendo renomeados corretamente
    """
    print("=== Teste de Correção de Dígitos em Arquivos JPG ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_jpg_digit_")
    
    try:
        # Cria a estrutura exata do problema
        lote_dir = os.path.join(test_dir, "L00126")
        subdir_correct = os.path.join(lote_dir, "0000126")  # Diretório correto
        aits_dir = os.path.join(subdir_correct, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria os arquivos problemáticos
        test_files = [
            # Arquivo JPG com o problema: deveria manter 7 dígitos
            (os.path.join(aits_dir, "0000126000003a.jpg"), "fake jpg content"),
            # Outros arquivos para teste completo
            (os.path.join(aits_dir, "0000126000003b.jpg"), "fake jpg content"),
            (os.path.join(aits_dir, "cd0010000126.txt"), "0000126;conteúdo;teste"),
            (os.path.join(aits_dir, "L00126.txt"), "0000126;conteúdo;teste"),
        ]
        
        for file_path, content in test_files:
            with open(file_path, "w") as f:
                f.write(content)
        
        print(f"Estrutura inicial:")
        print(f"Diretório base: {test_dir}")
        print_structure(test_dir)
        
        # Etapa 1: Simula exatamente o que acontece na GUI
        print(f"\n{'='*60}")
        print(f"ETAPA 1: Criando FileRenamer")
        print(f"{'='*60}")
        
        file_renamer = FileRenamer(test_dir)
        print(f"FileRenamer criado com diretório: {test_dir}")
        
        # Etapa 2: Executa rename_files com old_name == new_name
        print(f"\n{'='*60}")
        print(f"ETAPA 2: Executando rename_files('L00126', 'L00126')")
        print(f"{'='*60}")
        
        # Executa exatamente como na GUI
        file_renamer.rename_files("L00126", "L00126")
        
        print(f"\nEstrutura após rename_files:")
        print_structure(test_dir)
        
        # Etapa 3: Verifica o resultado
        print(f"\n{'='*60}")
        print(f"ETAPA 3: Verificando resultado")
        print(f"{'='*60}")
        
        # Verifica se os arquivos JPG ainda existem com o nome correto
        expected_files = [
            os.path.join(aits_dir, "0000126000003a.jpg"),
            os.path.join(aits_dir, "0000126000003b.jpg"),
        ]
        
        wrong_files = [
            os.path.join(aits_dir, "0000126000003a.jpg"),  # Este não deveria mudar
            os.path.join(aits_dir, "0000126000003b.jpg"),  # Este não deveria mudar
        ]
        
        for expected_file in expected_files:
            if os.path.exists(expected_file):
                print(f"✅ ARQUIVO CORRETO EXISTE: {os.path.basename(expected_file)}")
            else:
                print(f"❌ ARQUIVO CORRETO NÃO EXISTE: {os.path.basename(expected_file)}")
                
        # Verifica se os arquivos .txt foram tratados corretamente
        txt_files = [
            os.path.join(aits_dir, "cd0010000126.txt"),
            os.path.join(aits_dir, "L00126.txt"),
        ]
        
        for txt_file in txt_files:
            if os.path.exists(txt_file):
                print(f"✅ ARQUIVO TXT EXISTE: {os.path.basename(txt_file)}")
            else:
                print(f"❌ ARQUIVO TXT NÃO EXISTE: {os.path.basename(txt_file)}")
        
        # Etapa 4: Teste com renomeação real (diferentes nomes)
        print(f"\n{'='*60}")
        print(f"ETAPA 4: Testando renomeação real (L00126 -> L00127)")
        print(f"{'='*60}")
        
        # Cria nova estrutura para teste
        lote_dir_new = os.path.join(test_dir, "L00127")
        subdir_new = os.path.join(lote_dir_new, "0000127")
        aits_dir_new = os.path.join(subdir_new, "AITs")
        os.makedirs(aits_dir_new, exist_ok=True)
        
        # Copia os arquivos para a nova estrutura
        test_files_new = [
            (os.path.join(aits_dir_new, "0000126000003a.jpg"), "fake jpg content"),
            (os.path.join(aits_dir_new, "0000126000003b.jpg"), "fake jpg content"),
            (os.path.join(aits_dir_new, "cd0010000126.txt"), "0000126;conteúdo;teste"),
        ]
        
        for file_path, content in test_files_new:
            with open(file_path, "w") as f:
                f.write(content)
        
        print(f"Estrutura para teste de renomeação:")
        print_structure(lote_dir_new)
        
        # Executa renomeação
        file_renamer_new = FileRenamer(test_dir)
        file_renamer_new.rename_files("L00126", "L00127")
        
        print(f"\nEstrutura após renomeação:")
        print_structure(lote_dir_new)
        
        # Verifica resultados da renomeação
        print(f"\nVerificando resultados da renomeação:")
        renamed_files = [
            os.path.join(aits_dir_new, "0000127000003a.jpg"),
            os.path.join(aits_dir_new, "0000127000003b.jpg"),
        ]
        
        for renamed_file in renamed_files:
            if os.path.exists(renamed_file):
                print(f"✅ ARQUIVO RENOMEADO CORRETAMENTE: {os.path.basename(renamed_file)}")
            else:
                print(f"❌ ARQUIVO NÃO RENOMEADO: {os.path.basename(renamed_file)}")
                
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
    test_jpg_digit_issue()