import os
import tempfile
from file_renamer import FileRenamer

def test_recursive_directory_rename():
    """
    Testa a renomeação recursiva de diretórios apenas (sem alterar arquivos)
    Exemplo: 0000125 -> 0005654
    """
    # Cria um diretório temporário para o teste
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Diretório de teste: {temp_dir}")
        
        # Cria uma estrutura complexa com subdiretórios aninhados
        l05654_dir = os.path.join(temp_dir, "L05654")
        subdir_0000125 = os.path.join(l05654_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        nested_0000125 = os.path.join(aits_dir, "0000125")  # Subdiretório com mesmo nome
        deep_nested = os.path.join(nested_0000125, "subdir")
        another_0000125 = os.path.join(deep_nested, "0000125")  # Mais um nível
        
        # Cria toda a estrutura de diretórios
        os.makedirs(another_0000125)
        
        # Cria alguns arquivos incluindo md5sum.txt
        files_to_create = [
            (os.path.join(l05654_dir, "L05654.txt"), "Content L05654"),
            (os.path.join(subdir_0000125, "data.txt"), "Content 0000125"),
            (os.path.join(subdir_0000125, "md5sum.txt"), "hash123;0000125;original_hash"),
            (os.path.join(aits_dir, "image001.jpg"), "fake jpg data"),
            (os.path.join(aits_dir, "md5sum.txt"), "hash456;0000125;aits_hash"),
            (os.path.join(nested_0000125, "nested_file.txt"), "nested content"),
            (os.path.join(nested_0000125, "md5sum.txt"), "hash789;0000125;nested_hash"),
            (os.path.join(another_0000125, "deep_file.txt"), "deep content"),
            (os.path.join(another_0000125, "md5sum.txt"), "hashABC;0000125;deep_hash")
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Criado: {file_path}")
        
        print("\n=== ESTRUTURA ANTES DA RENOMEAÇÃO ===")
        print_directory_structure(temp_dir)
        
        # Lê o conteúdo original dos arquivos md5sum.txt para verificar se não foram alterados
        md5sum_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower() == 'md5sum.txt':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                    md5sum_files.append((file_path, content))
        
        print(f"\nEncontrados {len(md5sum_files)} arquivos md5sum.txt")
        
        # Executa a renomeação usando a nova função
        renamer = FileRenamer(temp_dir)
        
        old_name = "0000125"
        new_name = "0005654"
        
        print(f"\n=== EXECUTANDO RENOMEAÇÃO RECURSIVA: {old_name} -> {new_name} ===")
        
        # Aplica renomeação recursiva apenas de diretórios
        success = renamer.rename_directories_recursively(l05654_dir, old_name, new_name)
        print(f"Resultado: {'✓ SUCESSO' if success else '✗ FALHA'}")
        
        print("\n=== ESTRUTURA APÓS A RENOMEAÇÃO ===")
        print_directory_structure(temp_dir)
        
        # Verifica se todos os diretórios foram renomeados corretamente
        print("\n=== VERIFICAÇÃO DE DIRETÓRIOS ===")
        directories_correct = True
        
        expected_directories = [
            os.path.join(l05654_dir, "0005654"),
            os.path.join(l05654_dir, "0005654", "AITs"),
            os.path.join(l05654_dir, "0005654", "AITs", "0005654"),
            os.path.join(l05654_dir, "0005654", "AITs", "0005654", "subdir"),
            os.path.join(l05654_dir, "0005654", "AITs", "0005654", "subdir", "0005654")
        ]
        
        for expected_dir in expected_directories:
            exists = os.path.exists(expected_dir) and os.path.isdir(expected_dir)
            relative_path = os.path.relpath(expected_dir, temp_dir)
            print(f"{'✓' if exists else '✗'} Diretório: {relative_path}")
            if not exists:
                directories_correct = False
        
        # Verifica se diretórios antigos não existem mais
        old_directories = [
            os.path.join(l05654_dir, "0000125"),
            os.path.join(l05654_dir, "0005654", "AITs", "0000125"),  # Este seria o caminho se não fosse renomeado
        ]
        
        for old_dir in old_directories:
            if os.path.exists(old_dir):
                relative_path = os.path.relpath(old_dir, temp_dir)
                print(f"✗ Diretório antigo ainda existe: {relative_path}")
                directories_correct = False
        
        # Verifica se arquivos md5sum.txt mantiveram conteúdo original
        print("\n=== VERIFICAÇÃO DE ARQUIVOS MD5SUM ===")
        md5sum_preserved = True
        
        current_md5sum_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower() == 'md5sum.txt':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                    current_md5sum_files.append((file_path, content))
        
        # Verifica se o conteúdo dos arquivos md5sum.txt foi preservado
        for current_path, current_content in current_md5sum_files:
            # Procura por conteúdo correspondente nos arquivos originais
            content_found = False
            for orig_path, orig_content in md5sum_files:
                if current_content == orig_content:
                    content_found = True
                    relative_path = os.path.relpath(current_path, temp_dir)
                    print(f"✓ md5sum.txt preservado: {relative_path}")
                    break
            
            if not content_found:
                relative_path = os.path.relpath(current_path, temp_dir)
                print(f"✗ md5sum.txt alterado: {relative_path}")
                print(f"  Conteúdo atual: {current_content}")
                md5sum_preserved = False
        
        # Verifica se arquivos estão nos locais corretos
        print("\n=== VERIFICAÇÃO DE ARQUIVOS ===")
        files_in_correct_location = True
        
        expected_files = [
            os.path.join(l05654_dir, "0005654", "data.txt"),
            os.path.join(l05654_dir, "0005654", "md5sum.txt"),
            os.path.join(l05654_dir, "0005654", "AITs", "image001.jpg"),
            os.path.join(l05654_dir, "0005654", "AITs", "md5sum.txt"),
            os.path.join(l05654_dir, "0005654", "AITs", "0005654", "nested_file.txt"),
            os.path.join(l05654_dir, "0005654", "AITs", "0005654", "md5sum.txt"),
            os.path.join(l05654_dir, "0005654", "AITs", "0005654", "subdir", "0005654", "deep_file.txt"),
            os.path.join(l05654_dir, "0005654", "AITs", "0005654", "subdir", "0005654", "md5sum.txt")
        ]
        
        for expected_file in expected_files:
            exists = os.path.exists(expected_file) and os.path.isfile(expected_file)
            relative_path = os.path.relpath(expected_file, temp_dir)
            print(f"{'✓' if exists else '✗'} Arquivo: {relative_path}")
            if not exists:
                files_in_correct_location = False
        
        # Resultado final
        if directories_correct and md5sum_preserved and files_in_correct_location:
            print("\n🎉 TESTE PASSOU! Diretórios renomeados recursivamente, arquivos preservados.")
            print("📋 Próximos passos: Aplicar na função rename_internal_directories_with_aits")
            return True
        else:
            print("\n❌ TESTE FALHOU!")
            if not directories_correct:
                print("   - Diretórios não foram renomeados corretamente")
            if not md5sum_preserved:
                print("   - Arquivos md5sum.txt foram alterados")
            if not files_in_correct_location:
                print("   - Arquivos não estão nos locais corretos")
            return False

def print_directory_structure(root_dir, level=0):
    """Imprime a estrutura de diretórios de forma hierárquica"""
    if level > 5:  # Evita recursão muito profunda
        return
        
    items = []
    try:
        for item in os.listdir(root_dir):
            item_path = os.path.join(root_dir, item)
            if os.path.isdir(item_path):
                items.append(('dir', item, item_path))
            else:
                items.append(('file', item, None))
    except PermissionError:
        return
    
    items.sort(key=lambda x: (x[0] != 'dir', x[1]))
    
    for item_type, item_name, extra_info in items:
        indent = "  " * level
        if item_type == 'dir':
            print(f"{indent}📁 {item_name}/")
            if extra_info:
                print_directory_structure(extra_info, level + 1)
        else:
            print(f"{indent}📄 {item_name}")

if __name__ == "__main__":
    test_recursive_directory_rename()