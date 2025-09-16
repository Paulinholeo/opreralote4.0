#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug detalhado da função _fix_jpg_filename_pattern
"""

def create_padded_number(number, padding=7):
    """
    Cria um número com padding específico de zeros à esquerda.
    """
    return str(number).zfill(padding)

def fix_jpg_filename_pattern(filename_part, lot_number):
    """
    Corrige padrões incorretos em nomes de arquivos JPG.
    """
    print(f"\n=== DEBUG DA FUNÇÃO ===")
    print(f"Entrada: filename_part='{filename_part}', lot_number='{lot_number}'")
    
    try:
        # Verifica se é um arquivo JPG
        if not filename_part.lower().endswith('.jpg'):
            print(f"Não é JPG, retornando original")
            return filename_part
            
        # Extrai o nome do arquivo sem extensão
        file_name_without_ext = filename_part[:-4]  # Remove .jpg
        file_ext = '.jpg'
        print(f"file_name_without_ext='{file_name_without_ext}', file_ext='{file_ext}'")
        
        # Número do lote com padding
        lot_number_padded = create_padded_number(lot_number)
        lot_number_trimmed = lot_number.lstrip('0')
        print(f"lot_number_padded='{lot_number_padded}'")
        print(f"lot_number_trimmed='{lot_number_trimmed}'")
        
        # Verifica se o número do lote está no nome do arquivo
        if lot_number_padded in file_name_without_ext:
            print(f"Número do lote encontrado no nome")
            # Encontra a posição do número do lote
            lot_pos = file_name_without_ext.find(lot_number_padded)
            print(f"lot_pos={lot_pos}")
            if lot_pos != -1:
                # Pega o restante do nome após o número do lote
                rest_part = file_name_without_ext[lot_pos + len(lot_number_padded):]
                print(f"rest_part='{rest_part}'")
                
                # Verifica se o restante começa com o primeiro dígito do número do lote sem zeros
                # Isso indica que houve uma duplicação
                if (len(rest_part) > 0 and len(lot_number_trimmed) > 0 and 
                    rest_part[0] == lot_number_trimmed[0]):
                    print(f"Restante começa com primeiro dígito do lote sem zeros (duplicação detectada)")
                    print(f"rest_part[0]='{rest_part[0]}'")
                    print(f"lot_number_trimmed[0]='{lot_number_trimmed[0]}'")
                    # Remove o primeiro caractere do restante (que é duplicado)
                    corrected_rest = rest_part[1:] if len(rest_part) > 1 else ""
                    print(f"corrected_rest='{corrected_rest}'")
                    # Reconstrói o nome do arquivo
                    corrected_name = lot_number_padded + corrected_rest
                    result = corrected_name + file_ext
                    print(f"Corrigido: '{filename_part}' -> '{result}'")
                    return result
                else:
                    print(f"Restante NÃO começa com primeiro dígito do lote sem zeros")
                    if len(rest_part) > 0:
                        print(f"rest_part[0]='{rest_part[0]}'")
                    else:
                        print(f"rest_part está vazio")
                    if len(lot_number_trimmed) > 0:
                        print(f"lot_number_trimmed[0]='{lot_number_trimmed[0]}'")
                    else:
                        print(f"lot_number_trimmed está vazio")
        else:
            print(f"Número do lote NÃO encontrado no nome")
            
        # Retorna o nome original se não encontrou padrões incorretos
        return filename_part
    except Exception as e:
        print(f"Erro ao corrigir padrão de nome de arquivo JPG: {e}")
        return filename_part

def debug_test():
    """
    Testa especificamente a função _fix_jpg_filename_pattern com debug detalhado
    """
    print("=== Debug Detalhado: _fix_jpg_filename_pattern ===\n")
    
    # Testa o caso problemático
    input_name = "000017070000060a.jpg"
    lot_number = "00170"
    
    print(f"Testando caso problemático:")
    print(f"  Input: '{input_name}'")
    print(f"  Lote:  '{lot_number}'")
    print(f"  Esperado: '00001700000060a.jpg'")
    print()
    
    result = fix_jpg_filename_pattern(input_name, lot_number)
    status = "✅" if result == "00001700000060a.jpg" else "❌"
    print(f"\n{status} Resultado: '{result}'")
    
    if result != "00001700000060a.jpg":
        print(f"❌ Diferença encontrada!")

if __name__ == "__main__":
    debug_test()