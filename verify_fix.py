#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de verificação para confirmar se a correção de renomeação de subdiretórios está ativa.
"""

import os
import inspect
from file_renamer import FileRenamer

def verify_fix_implementation():
    """Verifica se a correção está implementada corretamente"""
    
    print("=== VERIFICAÇÃO DA CORREÇÃO DE SUBDIRETÓRIOS ===\\n")
    
    # 1. Verifica se a função update_internal_structure existe
    print("1. Verificando função update_internal_structure...")
    if hasattr(FileRenamer, 'update_internal_structure'):
        print("   ✅ Função update_internal_structure encontrada")
        
        # Mostra a assinatura da função
        sig = inspect.signature(FileRenamer.update_internal_structure)
        print(f"   📋 Assinatura: {sig}")
    else:
        print("   ❌ Função update_internal_structure NÃO encontrada")
        print("   🔧 AÇÃO NECESSÁRIA: Código não foi atualizado corretamente")
        return False
    
    # 2. Verifica se a função rename_directory tem a lógica de mesmo nome
    print("\\n2. Verificando lógica de mesmo nome em rename_directory...")
    source = inspect.getsource(FileRenamer.rename_directory)
    
    if "Mesmo nome de diretório" in source:
        print("   ✅ Lógica de mesmo nome encontrada")
    else:
        print("   ❌ Lógica de mesmo nome NÃO encontrada")
        print("   🔧 AÇÃO NECESSÁRIA: rename_directory não foi atualizada")
        return False
    
    if "update_internal_structure" in source:
        print("   ✅ Chamada para update_internal_structure encontrada")
    else:
        print("   ❌ Chamada para update_internal_structure NÃO encontrada")
        return False
    
    # 3. Verifica se a função rename_directories_recursively existe
    print("\\n3. Verificando função rename_directories_recursively...")
    if hasattr(FileRenamer, 'rename_directories_recursively'):
        print("   ✅ Função rename_directories_recursively encontrada")
    else:
        print("   ❌ Função rename_directories_recursively NÃO encontrada")
        return False
    
    # 4. Testa um caso simples
    print("\\n4. Testando funcionalidade básica...")
    try:
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            # Cria estrutura de teste
            test_dir = os.path.join(temp_dir, "L08685")
            subdir = os.path.join(test_dir, "0000125")
            os.makedirs(subdir)
            
            # Testa o FileRenamer
            renamer = FileRenamer(temp_dir)
            result = renamer.rename_directory("L08685", "L08685")
            
            # Verifica resultado
            expected_subdir = os.path.join(test_dir, "0008685")
            if os.path.exists(expected_subdir):
                print("   ✅ Teste funcional passou - subdiretório foi renomeado")
            else:
                print("   ❌ Teste funcional falhou - subdiretório não foi renomeado")
                return False
            
    except Exception as e:
        print(f"   ❌ Erro no teste funcional: {e}")
        return False
    
    print("\\n=== RESULTADO FINAL ===")
    print("✅ CORREÇÃO ESTÁ IMPLEMENTADA E FUNCIONANDO!")
    print("\\n📋 INSTRUÇÕES PARA USAR:")
    print("1. Feche completamente a aplicação OperaLote se estiver aberta")
    print("2. Reinicie a aplicação")
    print("3. Execute uma renomeação normalmente")
    print("4. Agora o subdiretório será renomeado automaticamente")
    print("\\n🔍 COMO VERIFICAR SE FUNCIONOU:")
    print("Veja se o log mostra:")
    print("  ANTES: D:/.../L08685/0000125/AITs/arquivo.txt")
    print("  DEPOIS: D:/.../L08685/0008685/AITs/arquivo.txt")
    
    return True

def show_current_version_info():
    """Mostra informações da versão atual"""
    print("\\n=== INFORMAÇÕES DA VERSÃO ATUAL ===")
    
    file_path = os.path.abspath(FileRenamer.__module__.replace('.', os.sep) + '.py')
    if os.path.exists(file_path):
        stat = os.stat(file_path)
        import time
        mod_time = time.ctime(stat.st_mtime)
        print(f"📁 Arquivo: {file_path}")
        print(f"🕒 Última modificação: {mod_time}")
        print(f"📏 Tamanho: {stat.st_size} bytes")
    
    # Mostra quantas funções existem na classe
    methods = [method for method in dir(FileRenamer) if not method.startswith('_')]
    print(f"🔧 Métodos disponíveis: {len(methods)}")
    print(f"📝 Lista: {', '.join(methods)}")

if __name__ == "__main__":
    print("VERIFICAÇÃO DE CORREÇÃO - OperaLote 4.0")
    print("=" * 50)
    
    try:
        success = verify_fix_implementation()
        show_current_version_info()
        
        if success:
            print("\\n🎉 TUDO PRONTO! A correção está ativa.")
        else:
            print("\\n⚠️ PROBLEMA DETECTADO! Correção não está ativa.")
            print("\\n🔧 SOLUÇÃO:")
            print("1. Verifique se você salvou o arquivo file_renamer.py")
            print("2. Reinicie a aplicação completamente")
            print("3. Execute este script novamente")
            
    except Exception as e:
        print(f"\\n❌ ERRO DURANTE VERIFICAÇÃO: {e}")
        print("\\n🔧 POSSÍVEIS CAUSAS:")
        print("1. Arquivo file_renamer.py não encontrado")
        print("2. Erro de sintaxe no código")
        print("3. Problema de importação")