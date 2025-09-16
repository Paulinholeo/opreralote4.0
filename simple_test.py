#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples e direto do text editor
"""

import os
import tempfile
import shutil
from text_file_editor import TextFileEditor

def simple_test():
    print("=== Teste Simples do Text Editor ===\\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="simple_test_")
    
    try:
        # Cria estrutura: test_dir/L02999/ (nome já renomeado)
        new_lote_dir = os.path.join(test_dir, "L02999")
        os.makedirs(new_lote_dir, exist_ok=True)
        
        # Cria arquivo de teste diretamente no diretório renomeado
        txt_file = os.path.join(new_lote_dir, "test.txt")
        original_content = "0000544;BRI1306/2023;20250905;14:49:38;2;000;000,0;00125000070a.jpg;00125000070b.jpg;001306;Av Getulio Vargas x Durval Carneiro SCB;5673"
        
        with open(txt_file, "w", encoding='utf-8') as f:
            f.write(original_content)
        
        print(f"Arquivo criado: {txt_file}")
        print(f"Conteúdo original: {original_content}")
        
        # Testa o TextFileEditor
        editor = TextFileEditor(test_dir)
        
        print("\\nChamando edit_text_content('L0544', 'L02999')...")
        editor.edit_text_content("L0544", "L02999")
        
        # Verifica resultado
        with open(txt_file, "r", encoding='utf-8') as f:
            new_content = f.read().strip()
        
        print(f"Conteúdo após edição: {new_content}")
        
        # Analisa mudanças
        if new_content != original_content:
            print("\\n✓ Arquivo foi modificado")
            if "0002999" in new_content:
                print("✓ Número do lote atualizado corretamente")
            if "/2023/2023" in new_content:
                print("⚠ PROBLEMA: Duplicação de /2023 detectada")
            elif "BRI1306/2023" in new_content:
                print("✓ Campo com /2023 preservado corretamente")
        else:
            print("\\n⚠ Arquivo não foi modificado")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        shutil.rmtree(test_dir)
        print(f"\\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    simple_test()