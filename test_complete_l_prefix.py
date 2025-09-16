#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste final completo para verificar a correção do prefixo L
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_complete_l_prefix():
    """
    Teste completo da correção do prefixo L em diferentes cenários
    """
    print("=== Teste Completo do Prefixo L ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_complete_l_")
    
    try:
        # Cenário 1: Arquivo sem L que deveria ter L
        print("📂 CENÁRIO 1: Arquivo 05456.txt → L05456.txt")
        lote_dir1 = os.path.join(test_dir, "L05456")
        os.makedirs(lote_dir1, exist_ok=True)
        
        with open(os.path.join(lote_dir1, "05456.txt"), "w") as f:
            f.write("05456;data;test")
        
        file_renamer = FileRenamer(test_dir)
        file_renamer.rename_files("L05456", "L05456")
        
        result1 = "L05456.txt" in os.listdir(lote_dir1)
        print(f"✅ Sucesso: {result1}")
        if result1:
            print(f"   Arquivo corretamente renomeado para L05456.txt")
        else:
            files = [f for f in os.listdir(lote_dir1) if f.endswith('.txt')]
            print(f"   ⚠ Arquivos encontrados: {files}")
        
        # Cenário 2: Arquivo com L que deve manter L
        print(f"\n📂 CENÁRIO 2: Arquivo L05456.txt → L05456.txt (manter)")
        lote_dir2 = os.path.join(test_dir, "L05457")
        os.makedirs(lote_dir2, exist_ok=True)
        
        with open(os.path.join(lote_dir2, "L05457.txt"), "w") as f:
            f.write("05457;data;test")
        
        file_renamer2 = FileRenamer(test_dir)
        file_renamer2.rename_files("L05457", "L05457")
        
        result2 = "L05457.txt" in os.listdir(lote_dir2)
        print(f"✅ Sucesso: {result2}")
        if result2:
            print(f"   Arquivo mantido como L05457.txt")
        
        # Cenário 3: Lote sem L (caso tradicional)
        print(f"\n📂 CENÁRIO 3: Lote tradicional 0005458 → 0005458.txt")
        lote_dir3 = os.path.join(test_dir, "0005458")
        os.makedirs(lote_dir3, exist_ok=True)
        
        with open(os.path.join(lote_dir3, "0005458.txt"), "w") as f:
            f.write("0005458;data;test")
        
        file_renamer3 = FileRenamer(test_dir)
        file_renamer3.rename_files("0005458", "0005459")
        
        # Renomeia o diretório primeiro
        os.rename(lote_dir3, os.path.join(test_dir, "0005459"))
        lote_dir3 = os.path.join(test_dir, "0005459")
        
        result3 = "0005459.txt" in os.listdir(lote_dir3)
        print(f"✅ Sucesso: {result3}")
        if result3:
            print(f"   Arquivo corretamente renomeado para 0005459.txt")
        
        print(f"\n=== RESUMO FINAL ===")
        success_count = sum([result1, result2, result3])
        print(f"✅ Cenários bem-sucedidos: {success_count}/3")
        
        if success_count == 3:
            print("🎉 SUCESSO TOTAL: Todas as correções funcionaram!")
        else:
            print("⚠ Alguns cenários precisam de ajustes")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(test_dir)
        print(f"\nDiretório removido: {test_dir}")

if __name__ == "__main__":
    test_complete_l_prefix()