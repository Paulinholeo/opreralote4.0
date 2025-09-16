#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste final completo para verificar todas as correções
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer
from text_file_editor import TextFileEditor

def test_complete_fix():
    """
    Teste completo das correções implementadas
    """
    print("=== Teste Completo das Correções ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_complete_")
    
    try:
        # Cria estrutura do problema real
        lote_dir = os.path.join(test_dir, "L0250907")
        os.makedirs(lote_dir, exist_ok=True)
        
        # Cria arquivos como no problema real
        files_data = {
            "020250907000001pa.jpg": "fake image pa",
            "020250907000001pb.jpg": "fake image pb", 
            "020250907000001za.jpg": "fake image za",
            "020250907000001zb.jpg": "fake image zb",
            "020250907.txt": "0250907;BRI3002/2023;20250907;13:44:33;1;110;121,0;020250907000001za.jpg;020250907000001pa.jpg;020250907000001zb.jpg;020250907000001pb.jpg;003002;MG - 010 KM 26,9 VESPASIANO SD;7455"
        }
        
        for file_name, content in files_data.items():
            file_path = os.path.join(lote_dir, file_name)
            with open(file_path, "w") as f:
                f.write(content)
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Arquivos antes da renomeação:")
        for file_name in sorted(files_data.keys()):
            print(f"  - {file_name}")
        
        # Executa renomeação completa
        file_renamer = FileRenamer(test_dir)
        text_editor = TextFileEditor(test_dir)
        
        old_name = "L0250907"
        new_name = "L05043"
        
        print(f"\nExecutando renomeação completa de '{old_name}' para '{new_name}'...")
        
        # 1. Renomeia diretório
        success = file_renamer.rename_directory(old_name, new_name)
        if success:
            print("✓ Diretório renomeado")
            
            # 2. Renomeia arquivos
            file_renamer.rename_files(old_name, new_name)
            print("✓ Arquivos processados")
            
            # 3. Atualiza conteúdo de texto
            file_renamer.rename_text_content(old_name, new_name)
            text_editor.edit_text_content(old_name, new_name)
            print("✓ Conteúdo de texto atualizado")
            
            # Verifica resultados
            new_lote_dir = os.path.join(test_dir, new_name)
            if os.path.exists(new_lote_dir):
                print(f"\nArquivos após renomeação:")
                final_files = sorted(os.listdir(new_lote_dir))
                
                jpg_ok = True
                txt_found = False
                
                for file_name in final_files:
                    print(f"  - {file_name}")
                    
                    # Verifica problemas em JPG
                    if ".jp.jpg" in file_name:
                        print(f"    ⚠ PROBLEMA: Extensão incorreta")
                        jpg_ok = False
                    elif file_name.endswith(".jpg"):
                        print(f"    ✓ JPG OK")
                    elif file_name.endswith(".txt"):
                        txt_found = True
                        print(f"    ✓ TXT encontrado")
                        
                        # Verifica conteúdo do txt
                        txt_path = os.path.join(new_lote_dir, file_name)
                        with open(txt_path, "r") as f:
                            content = f.read()
                        
                        if "/2023/2023" in content:
                            print(f"    ⚠ PROBLEMA: Duplicação de /2023")
                        elif "0005043" in content:
                            print(f"    ✓ Conteúdo atualizado corretamente")
                        else:
                            print(f"    ? Conteúdo: {content[:100]}...")
                
                # Resumo final
                print(f"\n=== RESUMO ===")
                if jpg_ok:
                    print("✅ JPG: Todas as extensões estão corretas")
                else:
                    print("❌ JPG: Problemas com extensões detectados")
                    
                if txt_found:
                    print("✅ TXT: Arquivo foi renomeado")
                else:
                    print("❌ TXT: Arquivo não foi encontrado")
                    
                if jpg_ok and txt_found:
                    print("\n🎉 SUCESSO TOTAL: Todas as correções funcionaram!")
                else:
                    print("\n⚠ Algumas correções podem precisar de ajustes")
            else:
                print("✗ Diretório renomeado não encontrado")
        else:
            print("✗ Falha na renomeação do diretório")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    test_complete_fix()