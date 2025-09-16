import os
import sys
from text_file_editor import TextFileEditor

# Teste para verificar a correção da duplicação de dígitos em nomes de arquivos JPG

def test_jpg_filename_fix():
    # Cria uma instância do TextFileEditor
    editor = TextFileEditor(os.getcwd())
    
    # Caso de teste 1: Duplicação de dígitos (problema original)
    old_name = "L0125"
    new_name = "L0125"  # Mesmo número, mas queremos corrigir o formato
    
    # Teste com o arquivo problemático mencionado pelo usuário
    filename = "00001252525000002a.jpg"
    corrected = editor._update_jpg_filename(filename, "0125", "0125")
    print(f"Original: {filename}")
    print(f"Corrigido: {corrected}")
    print(f"Esperado: 0000125000002a.jpg")
    print(f"Correto: {corrected == '0000125000002a.jpg'}")
    print()
    
    # Teste com outro exemplo similar
    filename2 = "00001252525000002b.jpg"
    corrected2 = editor._update_jpg_filename(filename2, "0125", "0125")
    print(f"Original: {filename2}")
    print(f"Corrigido: {corrected2}")
    print(f"Esperado: 0000125000002b.jpg")
    print(f"Correto: {corrected2 == '0000125000002b.jpg'}")
    print()
    
    # Caso de teste 2: Sem duplicação (deve manter o comportamento normal)
    filename3 = "0000125000003a.jpg"
    corrected3 = editor._update_jpg_filename(filename3, "0125", "0125")
    print(f"Original: {filename3}")
    print(f"Corrigido: {corrected3}")
    print(f"Esperado: 0000125000003a.jpg")
    print(f"Correto: {corrected3 == '0000125000003a.jpg'}")
    
    # Caso de teste 3: Mudança de número do lote
    filename4 = "00001252525000002a.jpg"
    corrected4 = editor._update_jpg_filename(filename4, "0125", "0789")
    print(f"Original: {filename4}")
    print(f"Corrigido: {corrected4}")
    print(f"Esperado: 0000789000002a.jpg")
    print(f"Correto: {corrected4 == '0000789000002a.jpg'}")

if __name__ == "__main__":
    test_jpg_filename_fix()