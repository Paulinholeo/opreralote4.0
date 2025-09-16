import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_l05456_aits_structure():
    """
    Testa o caso específico:
    📁 L05456/
      📁 0000125/
        📄 0005456.txt
        📄 0005456001.jpg
        📁 AITs/
          📄 0005456001.jpg
          📄 0005456002.jpg
          📄 L05456.txt
      📄 L05456.txt
    """
    # Cria um diretório temporário para o teste
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Diretório de teste: {temp_dir}")
        
        # Cria a estrutura de diretórios
        l05456_dir = os.path.join(temp_dir, "L05456")
        subdir_0000125 = os.path.join(l05456_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria os arquivos conforme a estrutura fornecida
        files_to_create = [
            (os.path.join(l05456_dir, "L05456.txt"), "Arquivo principal L05456"),
            (os.path.join(subdir_0000125, "0005456.txt"), "Arquivo 0005456"),
            (os.path.join(subdir_0000125, "0005456001.jpg"), "fake jpg data"),
            (os.path.join(aits_dir, "0005456001.jpg"), "aits jpg 1"),
            (os.path.join(aits_dir, "0005456002.jpg"), "aits jpg 2"),
            (os.path.join(aits_dir, "L05456.txt"), "Arquivo L05456 no AITs")
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Criado: {file_path}")
        
        print("\n=== ESTRUTURA ANTES DA RENOMEAÇÃO ===")
        print_directory_structure(temp_dir)
        
        # Executa a renomeação
        renamer = FileRenamer(temp_dir)
        
        # Renomeia de L05456 para L02544
        old_name = "L05456"
        new_name = "L02544"
        
        print(f"\n=== RENOMEANDO DE {old_name} PARA {new_name} ===")
        
        # Renomeia o diretório
        success = renamer.rename_directory(old_name, new_name)
        print(f"Resultado rename_directory: {success}")
        
        # Renomeia os arquivos
        print("\n--- Renomeando arquivos ---")
        renamer.rename_files(old_name, new_name)
        
        # Renomeia o conteúdo dos arquivos de texto
        print("\n--- Renomeando conteúdo dos arquivos ---")
        renamer.rename_text_content(old_name, new_name)
        
        print("\n=== ESTRUTURA APÓS A RENOMEAÇÃO ===")
        print_directory_structure(temp_dir)
        
        # Verifica se todos os arquivos foram renomeados corretamente
        expected_files = [
            os.path.join(temp_dir, "L02544", "L02544.txt"),  # Este arquivo fica no diretório principal
            os.path.join(temp_dir, "L02544", "02544", "0002544.txt"),
            os.path.join(temp_dir, "L02544", "02544", "0002544001.jpg"),
            os.path.join(temp_dir, "L02544", "02544", "AITs", "0002544001.jpg"),
            os.path.join(temp_dir, "L02544", "02544", "AITs", "0002544002.jpg"),
            os.path.join(temp_dir, "L02544", "02544", "AITs", "L02544.txt")
        ]
        
        print("\n=== VERIFICAÇÃO DOS ARQUIVOS ESPERADOS ===")
        all_renamed = True
        for expected_file in expected_files:
            exists = os.path.exists(expected_file)
            print(f"{'✓' if exists else '✗'} {expected_file}")
            if not exists:
                all_renamed = False
        
        if all_renamed:
            print("\n🎉 SUCESSO: Todos os arquivos foram renomeados corretamente!")
        else:
            print("\n❌ FALHA: Alguns arquivos não foram renomeados corretamente.")
            
        return all_renamed

def print_directory_structure(root_dir, level=0):
    """Imprime a estrutura de diretórios de forma hierárquica"""
    items = []
    try:
        for item in os.listdir(root_dir):
            item_path = os.path.join(root_dir, item)
            if os.path.isdir(item_path):
                items.append(('dir', item, item_path))
            else:
                size = os.path.getsize(item_path)
                items.append(('file', item, f"{size} bytes"))
    except PermissionError:
        print("  " * level + "❌ Acesso negado")
        return
    
    # Ordena: diretórios primeiro, depois arquivos
    items.sort(key=lambda x: (x[0] != 'dir', x[1]))
    
    for item_type, item_name, extra_info in items:
        indent = "  " * level
        if item_type == 'dir':
            print(f"{indent}📁 {item_name}/")
            print_directory_structure(extra_info, level + 1)
        else:
            print(f"{indent}📄 {item_name} ({extra_info})")

if __name__ == "__main__":
    test_l05456_aits_structure()