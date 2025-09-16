#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para o erro de edição de conteúdo de texto
com dados que já contêm /2023
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer
from text_file_editor import TextFileEditor

def test_text_editor_with_existing_year():
    """
    Testa a edição de texto com dados que já contêm /2023
    """
    print("=== Teste de Correção do Text Editor ===\n")
    
    # Cria diretório temporário para teste
    test_dir = tempfile.mkdtemp(prefix="test_text_editor_")
    
    try:
        # Cria estrutura de diretórios
        lote_dir = os.path.join(test_dir, "L0544")
        internal_dir = os.path.join(lote_dir, "0000125")
        aits_dir = os.path.join(internal_dir, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria arquivo de texto com conteúdo real que estava causando erro
        txt_file = os.path.join(aits_dir, "0000125.txt")
        with open(txt_file, "w") as f:
            f.write("0000544;BRI1306/2023;20250905;14:49:38;2;000;000,0;00125000070a.jpg;00125000070b.jpg;001306;Av Getulio Vargas x Durval Carneiro SCB           ;5673\\n")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Conteúdo original do arquivo:")
        with open(txt_file, "r") as f:
            print(f"  {f.read().strip()}")
        
        # Inicializa o editor
        text_editor = TextFileEditor(test_dir)
        
        # Testa a edição (aqui estava o erro)
        print("\\nExecutando edição do conteúdo...")
        try:
            text_editor.edit_text_content("L0544", "L02999")
            print("✓ Edição realizada sem erro")
            
            # Verifica o conteúdo após edição
            with open(txt_file, "r") as f:
                new_content = f.read().strip()
                print(f"Conteúdo após edição:\\n  {new_content}")
                
            # Verifica se o conteúdo foi alterado corretamente
            if "0002999" in new_content and "BRI1306/2023" in new_content:
                print("\\n✓ SUCESSO: Conteúdo editado corretamente!")
                print("  - Número do lote atualizado para 0002999")
                print("  - Campo BRI1306/2023 mantido sem duplicação")
            elif "/2023/2023" in new_content:
                print("\\n⚠ AVISO: Duplicação de /2023 detectada")
            else:
                print("\\n? Resultado inesperado no conteúdo")
                
        except Exception as e:
            print(f"✗ Erro durante a edição: {e}")
            import traceback
            traceback.print_exc()
            
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
    test_text_editor_with_existing_year()