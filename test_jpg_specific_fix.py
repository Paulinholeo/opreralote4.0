#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para debugar o problema com arquivos JPG quando old_name == new_name
mas os números têm formatos diferentes.
"""

import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_jpg_specific_fix():
    """
    Testa o problema específico com arquivos JPG quando:
    old_name = "10637" 
    new_name = "10637"
    Mas os números nos arquivos têm formatos diferentes:
    Arquivo: "0010637000017a.jpg" deveria virar "00010637000017a.jpg"
    """
    print("=== Teste JPG com old_name == new_name e formatos diferentes ===\n")
    
    # Cria diretório temporário
    test_dir = tempfile.mkdtemp(prefix="test_jpg_specific_")
    
    try:
        # Cria a estrutura exata do problema
        lote_dir = os.path.join(test_dir, "10637")
        subdir_correct = os.path.join(lote_dir, "00010637")  # Diretório correto após correção
        aits_dir = os.path.join(subdir_correct, "AITs")
        os.makedirs(aits_dir, exist_ok=True)
        
        # Cria o arquivo problemático: 0010637000017a.jpg que deve ser renomeado para 00010637000017a.jpg
        # quando old_name == new_name ("10637" == "10637")
        # Mas o arquivo contém "0010637" (formato com zeros à esquerda)
        jpg_path = os.path.join(aits_dir, "0010637000017a.jpg")
        with open(jpg_path, "w", encoding='utf-8') as f:
            f.write("fake jpg content")
        
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
        print(f"ETAPA 2: Executando rename_files('10637', '10637')")
        print(f"{'='*60}")
        print(f"Este é o caso problemático onde old_name == new_name")
        print(f"Mas os números nos arquivos têm formatos diferentes:")
        print(f"  old_name = '10637'")
        print(f"  new_name = '10637'")
        print(f"O arquivo 0010637000017a.jpg deve ser renomeado para 00010637000017a.jpg")
        
        # Executa exatamente como na GUI
        file_renamer.rename_files("10637", "10637")
        
        print(f"\nEstrutura após rename_files:")
        print_structure(test_dir)
        
        # Etapa 3: Verifica o resultado
        print(f"\n{'='*60}")
        print(f"ETAPA 3: Verificando resultado")
        print(f"{'='*60}")
        
        # Verifica se o arquivo foi renomeado corretamente
        expected_file = os.path.join(aits_dir, "00010637000017a.jpg")
        original_file = os.path.join(aits_dir, "0010637000017a.jpg")
        
        if os.path.exists(expected_file):
            print(f"✅ ARQUIVO CORRETO EXISTE: {expected_file}")
        else:
            print(f"❌ ARQUIVO CORRETO NÃO EXISTE: {expected_file}")
            
        if os.path.exists(original_file):
            print(f"❌ ARQUIVO ORIGINAL AINDA EXISTE: {original_file}")
            print(f"   Este é o problema! O arquivo não foi renomeado.")
        else:
            print(f"✅ ARQUIVO ORIGINAL NÃO EXISTE: {original_file}")
        
        # Etapa 4: Debug detalhado da lógica de detecção
        print(f"\n{'='*60}")
        print(f"ETAPA 4: Debug detalhado da lógica de detecção")
        print(f"{'='*60}")
        
        old_name = "10637"
        new_name = "10637"
        
        old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
        new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
        
        print(f"old_name: {old_name}")
        print(f"new_name: {new_name}")
        print(f"old_name_number: {old_name_number}")
        print(f"new_name_number: {new_name_number}")
        
        # Testa a detecção do arquivo problemático
        test_filename = "0010637000017a.jpg"
        base_filename = os.path.basename(test_filename)
        file_ext = os.path.splitext(base_filename)[1]
        file_name_without_ext = os.path.splitext(base_filename)[0]
        
        print(f"\nAnalisando arquivo: {test_filename}")
        print(f"base_filename: {base_filename}")
        print(f"file_ext: {file_ext}")
        print(f"file_name_without_ext: {file_name_without_ext}")
        
        # Verifica as condições de detecção específicas para JPG
        contains_old_number = False
        processed_by_special_logic = False
        
        # Verifica padrões numéricos específicos primeiro, especialmente para JPG
        if file_ext.lower() == '.jpg':
            # Procura por padrões numéricos no nome do arquivo JPG
            import re
            # Procura por sequências de 5 ou mais dígitos
            digit_sequences = re.findall(r'\d{5,}', file_name_without_ext)
            print(f"Sequências numéricas encontradas: {digit_sequences}")
            
            # Verifica se alguma sequência corresponde ao padrão do old_name_number
            for seq in digit_sequences:
                # Verifica se a sequência corresponde ao padrão do old_name_number
                # Por exemplo, se old_name_number é "00126", procuramos por "00126" ou "000126"
                old_number_trimmed = old_name_number.lstrip('0')
                seq_trimmed = seq.lstrip('0')
                
                print(f"  Comparando seq '{seq}' com old_name_number '{old_name_number}'")
                print(f"  old_number_trimmed: '{old_number_trimmed}', seq_trimmed: '{seq_trimmed}'")
                
                if (seq == old_name_number or 
                    seq_trimmed == old_number_trimmed or
                    seq == old_name_number.lstrip('0').zfill(6) or 
                    seq == old_name_number.lstrip('0').zfill(7)):
                    contains_old_number = True
                    print(f"  ✓ Sequência '{seq}' corresponde ao padrão")
                    break
                else:
                    print(f"  ✗ Sequência '{seq}' NÃO corresponde ao padrão")
        
        print(f"\nResultado da detecção:")
        print(f"contains_old_number: {contains_old_number}")
        print(f"processed_by_special_logic: {processed_by_special_logic}")
        
        if contains_old_number:
            print(f"\n✅ ARQUIVO SERIA DETECTADO PARA RENOMEAÇÃO!")
            print(f"   Isso é correto! Quando old_name == new_name mas os números")
            print(f"   têm formatos diferentes, o arquivo deve ser renomeado.")
        else:
            print(f"\n❌ ARQUIVO NÃO SERIA DETECTADO!")
            print(f"   Este é o problema! O arquivo deveria ser detectado para renomeação.")
            
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
    test_jpg_specific_fix()