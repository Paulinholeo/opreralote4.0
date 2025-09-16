#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar o funcionamento do text_file_editor
"""

import os
import tempfile
import shutil
from text_file_editor import TextFileEditor

def test_text_editor():
    """
    Testa o funcionamento do TextFileEditor com arquivos JPG
    """
    print("=== Teste do TextFileEditor ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_text_editor_")
    
    try:
        # Cria a estrutura exata do problema
        lote_dir = os.path.join(test_dir, "L00126")
        subdir = os.path.join(lote_dir, "0000126")
        aits_dir = os.path.join(subdir, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria um arquivo de texto de exemplo
        txt_path = os.path.join(aits_dir, "exemplo.txt")
        with open(txt_path, "w", encoding='utf-8') as f:
            f.write("00126000132a.jpg;00126000132b.jpg;outros dados\n")
            f.write("0000126;outros dados\n")
        
        print(f"Estrutura inicial:")
        print(f"Diretório base: {test_dir}")
        print_structure(test_dir)
        
        # Lê o conteúdo do arquivo antes da edição
        print(f"\nConteúdo do arquivo antes da edição:")
        with open(txt_path, "r", encoding='utf-8') as f:
            print(f.read())
        
        # Etapa 1: Cria o TextFileEditor
        print(f"\n{'='*60}")
        print(f"ETAPA 1: Criando TextFileEditor")
        print(f"{'='*60}")
        
        text_editor = TextFileEditor(test_dir)
        print(f"TextFileEditor criado com diretório: {test_dir}")
        
        # Etapa 2: Executa edit_text_content
        print(f"\n{'='*60}")
        print(f"ETAPA 2: Executando edit_text_content('L00126', 'L00126')")
        print(f"{'='*60}")
        
        # Executa exatamente como na GUI
        text_editor.edit_text_content("L00126", "L00126")
        
        # Etapa 3: Verifica o resultado
        print(f"\n{'='*60}")
        print(f"ETAPA 3: Verificando resultado")
        print(f"{'='*60}")
        
        print(f"Estrutura após edit_text_content:")
        print_structure(test_dir)
        
        # Lê o conteúdo do arquivo após a edição
        print(f"\nConteúdo do arquivo após edição:")
        with open(txt_path, "r", encoding='utf-8') as f:
            content = f.read()
            print(content)
            
            # Verifica se o conteúdo foi atualizado corretamente
            # O primeiro campo "00126000132a.jpg" deve ser convertido para "0000126" (número do lote)
            # O segundo campo "00126000132b.jpg" deve ser convertido para "0000126000132b.jpg"
            if "0000126" in content and "0000126000132b.jpg" in content:
                print("✅ Conteúdo atualizado corretamente!")
            else:
                print("❌ Conteúdo NÃO foi atualizado corretamente!")
            
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
    test_text_editor()