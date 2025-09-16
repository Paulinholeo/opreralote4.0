#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de integração final para verificar se todas as correções estão funcionando em conjunto
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_final_integration():
    """
    Testa um caso completo de renomeação de diretório, arquivos JPG e conteúdo de texto
    """
    print("=== Teste de Integração Final ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_final_integration_")
    
    try:
        # Cria estrutura similar ao caso real:
        # L03313/0003313/AITs/
        lote_dir = os.path.join(test_dir, "L03313")
        subdir = os.path.join(lote_dir, "0003313")
        aits_dir = os.path.join(subdir, "AITs")
        
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria arquivos JPG com diferentes padrões numéricos
        jpg_files = [
            "0003313000008a.jpg",
            "0003313000008b.jpg",
            "003313000009a.jpg",
            "003313000009b.jpg",
        ]
        
        for jpg_file in jpg_files:
            file_path = os.path.join(aits_dir, jpg_file)
            with open(file_path, "w") as f:
                f.write("fake jpg content")
        
        # Cria um arquivo de texto com conteúdo que precisa ser substituído
        test_content = "0003313;BRI1284;20250430;13:40:34;1;000;000,0;0003313000008a.jpg;0003313000008b.jpg;012841;R DELMIRA GONCALVES ESQ R SETE DE SETEMBRO SCB    ;6050"
        
        txt_file_path = os.path.join(aits_dir, "teste.txt")
        with open(txt_file_path, "w") as f:
            f.write(test_content)
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Arquivos JPG antes da renomeação:")
        for file in sorted(os.listdir(aits_dir)):
            if file.endswith('.jpg'):
                print(f"  - {file}")
        
        print("Conteúdo do arquivo de texto antes da substituição:")
        with open(txt_file_path, "r") as f:
            content_before = f.read()
            print(f"  {content_before}")
        
        # Testa a renomeação completa
        file_renamer = FileRenamer(test_dir)
        
        print(f"\nExecutando renomeação completa de '0003313' para '0005453'...")
        file_renamer.rename_directory("L03313", "L05453")  # Renomeia diretório
        file_renamer.rename_files("0003313", "0005453")    # Renomeia arquivos
        file_renamer.rename_text_content("0003313", "0005453")  # Substitui conteúdo
        
        # Verifica os resultados
        new_lote_dir = os.path.join(test_dir, "L05453")
        new_subdir = os.path.join(new_lote_dir, "0005453")
        new_aits_dir = os.path.join(new_subdir, "AITs")
        
        print("\nArquivos JPG após a renomeação:")
        renamed_jpg_files = []
        for file in os.listdir(new_aits_dir):
            if file.endswith('.jpg'):
                renamed_jpg_files.append(file)
                print(f"  - {file}")
        
        print("\nConteúdo do arquivo de texto após a substituição:")
        with open(os.path.join(new_aits_dir, "teste.txt"), "r") as f:
            content_after = f.read()
            print(f"  {content_after}")
        
        # Verifica se os arquivos JPG foram renomeados corretamente com 7 dígitos
        print("\n=== VERIFICAÇÃO DE ARQUIVOS JPG ===")
        expected_jpg_renames = {
            "0003313000008a.jpg": "0005453000008a.jpg",
            "0003313000008b.jpg": "0005453000008b.jpg",
            "003313000009a.jpg": "0005453000009a.jpg",
            "003313000009b.jpg": "0005453000009b.jpg",
        }
        
        jpg_success_count = 0
        jpg_total_count = len(expected_jpg_renames)
        
        for original, expected in expected_jpg_renames.items():
            if expected in renamed_jpg_files:
                print(f"✓ {original} -> {expected} (7 dígitos corretos)")
                jpg_success_count += 1
            else:
                print(f"✗ {original} -> NÃO RENOMEADO CORRETAMENTE")
        
        # Verifica se o conteúdo do texto foi substituído corretamente
        print("\n=== VERIFICAÇÃO DE CONTEÚDO DE TEXTO ===")
        expected_content = test_content.replace("0003313", "0005453")
        
        if content_after == expected_content:
            print("✓ Substituição de conteúdo realizada corretamente!")
            text_success = True
        else:
            print("✗ Substituição de conteúdo NÃO foi realizada corretamente")
            text_success = False
        
        # Resultados finais
        jpg_success_rate = (jpg_success_count / jpg_total_count) * 100 if jpg_total_count > 0 else 0
        overall_success = jpg_success_rate == 100 and text_success
        
        print(f"\n=== RESULTADOS FINAIS ===")
        print(f"Taxa de sucesso JPG: {jpg_success_rate:.1f}% ({jpg_success_count}/{jpg_total_count})")
        print(f"Substituição de texto: {'✓ SUCESSO' if text_success else '✗ FALHA'}")
        
        if overall_success:
            print("\n🎉 SUCESSO TOTAL: Todos os testes passaram!")
        else:
            print("\n❌ FALHA: Alguns testes não passaram")
            
        return overall_success
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    success = test_final_integration()
    if success:
        print("\n✅ INTEGRAÇÃO FINAL BEM SUCEDIDA!")
    else:
        print("\n❌ INTEGRAÇÃO FINAL FALHOU!")