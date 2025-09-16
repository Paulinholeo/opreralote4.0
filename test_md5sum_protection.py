import os
import tempfile
from file_renamer import FileRenamer

def test_md5sum_protection():
    """
    Testa se o arquivo md5sum.txt é protegido contra alteração de conteúdo
    """
    # Cria um diretório temporário para o teste
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Diretório de teste: {temp_dir}")
        
        # Cria a estrutura de diretórios
        l05456_dir = os.path.join(temp_dir, "L05456")
        subdir_0000125 = os.path.join(l05456_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria os arquivos incluindo md5sum.txt
        files_to_create = [
            (os.path.join(l05456_dir, "L05456.txt"), "Content with 0000125"),
            (os.path.join(subdir_0000125, "0005456.txt"), "Content 0000125"),
            (os.path.join(subdir_0000125, "md5sum.txt"), "abc123def456;0000125;hash_value"),
            (os.path.join(aits_dir, "0005456001.jpg"), "fake jpg data"),
            (os.path.join(aits_dir, "md5sum.txt"), "xyz789uvw012;0000125;another_hash")
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Criado: {file_path}")
        
        print("\n=== ESTRUTURA ANTES DA RENOMEAÇÃO ===")
        print_directory_structure(temp_dir)
        
        # Lê o conteúdo original dos arquivos md5sum.txt
        md5sum_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower() == 'md5sum.txt':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        original_content = f.read()
                    md5sum_files.append((file_path, original_content))
                    print(f"MD5SUM original: {file_path} -> {original_content}")
        
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
        
        # Renomeia o conteúdo dos arquivos de texto (aqui que deve pular md5sum.txt)
        print("\n--- Renomeando conteúdo dos arquivos ---")
        renamer.rename_text_content(old_name, new_name)
        
        print("\n=== ESTRUTURA APÓS A RENOMEAÇÃO ===")
        print_directory_structure(temp_dir)
        
        # Verifica se os arquivos md5sum.txt mantiveram o conteúdo original
        print("\n=== VERIFICAÇÃO DE PROTEÇÃO MD5SUM ===")
        md5sum_protected = True
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower() == 'md5sum.txt':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        current_content = f.read()
                    
                    # Procura o conteúdo original correspondente
                    original_content = None
                    for orig_path, orig_content in md5sum_files:
                        # Compara baseado na estrutura relativa
                        if orig_path.replace(old_name, new_name).replace("0000125", "02544") == file_path:
                            original_content = orig_content
                            break
                    
                    if original_content and current_content == original_content:
                        print(f"✓ MD5SUM protegido: {file_path}")
                        print(f"  Conteúdo mantido: {current_content}")
                    else:
                        print(f"✗ MD5SUM alterado: {file_path}")
                        print(f"  Original: {original_content}")
                        print(f"  Atual: {current_content}")
                        md5sum_protected = False
        
        # Verifica se outros arquivos .txt foram alterados corretamente
        print("\n=== VERIFICAÇÃO DE OUTROS ARQUIVOS TXT ===")
        other_files_updated = True
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.txt') and file.lower() != 'md5sum.txt':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Verifica se o conteúdo foi atualizado (não deve conter "0000125")
                    if "0000125" in content:
                        print(f"✗ Arquivo não atualizado: {file_path}")
                        print(f"  Conteúdo: {content}")
                        other_files_updated = False
                    else:
                        print(f"✓ Arquivo atualizado: {file_path}")
                        print(f"  Conteúdo: {content}")
        
        if md5sum_protected and other_files_updated:
            print("\n🎉 SUCESSO: md5sum.txt protegido e outros arquivos atualizados!")
        else:
            print("\n❌ FALHA: Proteção não funcionou corretamente.")
            
        return md5sum_protected and other_files_updated

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
    test_md5sum_protection()