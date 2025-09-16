#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste mais preciso para verificar o problema com a substituição de conteúdo em arquivos de texto
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_text_content_precise():
    """
    Testa o problema com a substituição de conteúdo em arquivos de texto
    Exemplo: Text Content: 0005453, Text Old Number: 0003313
    Ou seja, queremos substituir 0003313 por 0005453
    """
    print("=== Teste Preciso do Problema com Conteúdo de Texto ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_text_content_precise_")
    
    try:
        # Cria estrutura similar ao caso real:
        # L03313/0003313/AITs/
        lote_dir = os.path.join(test_dir, "L03313")
        subdir = os.path.join(lote_dir, "0003313")
        aits_dir = os.path.join(subdir, "AITs")
        
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria um arquivo de texto com conteúdo que precisa ser substituído
        # Vamos usar um conteúdo que contenha o número antigo 0003313
        # Exemplo modificado: 0003313 deve ser substituído por 0005453
        test_content = "0003313;BRI1284;20250430;13:40:34;1;000;000,0;0003313000008a.jpg;0003313000008b.jpg;012841;R DELMIRA GONCALVES ESQ R SETE DE SETEMBRO SCB    ;6050"
        
        txt_file_path = os.path.join(aits_dir, "teste.txt")
        with open(txt_file_path, "w") as f:
            f.write(test_content)
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Conteúdo do arquivo antes da substituição:")
        with open(txt_file_path, "r") as f:
            content_before = f.read()
            print(f"  {content_before}")
        
        # Testa a substituição de conteúdo
        file_renamer = FileRenamer(test_dir)
        
        print(f"\nExecutando substituição de conteúdo de '0003313' para '0005453'...")
        file_renamer.rename_text_content("0003313", "0005453")
        
        print("\nConteúdo do arquivo após a substituição:")
        with open(txt_file_path, "r") as f:
            content_after = f.read()
            print(f"  {content_after}")
        
        # Verifica se a substituição foi feita corretamente
        print("\n=== VERIFICAÇÃO ===")
        # O número 0003313 deve ser substituído por 0005453 (mantendo 7 dígitos)
        expected_content = test_content.replace("0003313", "0005453")
        
        print(f"Conteúdo esperado: {expected_content}")
        print(f"Conteúdo obtido:   {content_after}")
        
        if content_after == expected_content:
            print("✓ Substituição de conteúdo realizada corretamente!")
            return True
        else:
            print("✗ Substituição de conteúdo NÃO foi realizada corretamente")
            return False
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    success = test_text_content_precise()
    if success:
        print("\n🎉 SUCESSO: A substituição de conteúdo está funcionando corretamente!")
    else:
        print("\n❌ FALHA: A substituição de conteúdo não está funcionando como esperado!")