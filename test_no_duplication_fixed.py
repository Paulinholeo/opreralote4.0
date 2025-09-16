#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar se não há duplicação na renomeação do L00125.txt
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_no_duplication():
    """
    Testa se o arquivo L00125.txt é renomeado sem criar duplicatas
    """
    print("=== Teste de Não Duplicação L00125.txt ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_no_dup_")
    
    try:
        # Cria estrutura: L08487/0000125/AITs/L00125.txt
        lote_dir = os.path.join(test_dir, "L08487")
        subdir = os.path.join(lote_dir, "0000125")
        aits_dir = os.path.join(subdir, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria o arquivo L00125.txt com conteúdo
        l00125_file = os.path.join(aits_dir, "L00125.txt")
        with open(l00125_file, "w") as f:
            f.write("0000125;BRI1306/2023;20250905;14:49:38;2;000;000,0;00125000070a.jpg;00125000070b.jpg;001306;Test Location AITs;5673")
        
        # Cria outros arquivos para contexto
        other_files = [
            os.path.join(aits_dir, "0000125000070a.jpg"),
            os.path.join(aits_dir, "0000125000070b.jpg"),
            os.path.join(subdir, "0000125.txt")
        ]
        
        for file_path in other_files:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write("test content")
        
        print(f"Estrutura de teste criada em: {test_dir}")
        print("Estrutura antes da renomeação:")
        print_structure(test_dir)
        
        # Simula a renomeação completa
        file_renamer = FileRenamer(test_dir)
        
        print(f"\nExecutando renomeação: L0000125 -> L08487")
        
        # Simula os parâmetros reais
        old_name = "L0000125"
        new_name = "L08487"
        
        # Executa a função
        file_renamer.rename_files(old_name, new_name)
        
        print(f"\nEstrutura após renomeação:")
        print_structure(test_dir)
        
        # Verifica se há duplicação
        txt_files_in_aits = [f for f in os.listdir(aits_dir) if f.endswith('.txt')]
        print(f"\nArquivos .txt no diretório AITs: {txt_files_in_aits}")
        
        # Análise dos resultados
        if len(txt_files_in_aits) == 1:
            if txt_files_in_aits[0] == "L08487.txt":
                print(f"\n✅ SUCESSO TOTAL:")
                print(f"  - Arquivo único: {txt_files_in_aits[0]}")
                print(f"  - Não houve duplicação")
                print(f"  - Nome correto aplicado")
                
                # Verifica se o arquivo tem conteúdo
                txt_path = os.path.join(aits_dir, txt_files_in_aits[0])
                with open(txt_path, "r") as f:
                    content = f.read()
                if content and "Test Location AITs" in content:
                    print(f"  - Conteúdo preservado: OK")
                else:
                    print(f"  - AVISO: Conteúdo pode ter sido perdido")
                    
            else:
                print(f"\n⚠ PROBLEMA: Nome incorreto: {txt_files_in_aits[0]}")
        elif len(txt_files_in_aits) > 1:
            print(f"\n❌ ERRO: Duplicação detectada!")
            for f in txt_files_in_aits:
                file_path = os.path.join(aits_dir, f)
                size = os.path.getsize(file_path)
                print(f"  - {f} (tamanho: {size} bytes)")
        else:
            print(f"\n❌ ERRO: Nenhum arquivo .txt encontrado!")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

def print_structure(directory, indent=""):
    """
    Imprime a estrutura de diretórios
    """
    if not os.path.exists(directory):
        return
        
    items = sorted(os.listdir(directory))
    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path)
            print(f"{indent}├── {item} ({size} bytes)")
        else:
            print(f"{indent}├── {item}/")
            print_structure(item_path, indent + "│   ")

if __name__ == "__main__":
    test_no_duplication()