import os
import tempfile
from file_renamer import FileRenamer

def test_recursive_directory_rename():
    """
    Testa a renomeacao recursiva de diretorios apenas (sem alterar arquivos)
    Exemplo: 0000125 -> 0005654
    """
    # Cria um diretorio temporario para o teste
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Diretorio de teste: {temp_dir}")
        
        # Cria uma estrutura complexa com subdiretorios aninhados
        l05654_dir = os.path.join(temp_dir, "L05654")
        subdir_0000125 = os.path.join(l05654_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        nested_0000125 = os.path.join(aits_dir, "0000125")  # Subdiretorio com mesmo nome
        deep_nested = os.path.join(nested_0000125, "subdir")
        another_0000125 = os.path.join(deep_nested, "0000125")  # Mais um nivel
        
        # Cria toda a estrutura de diretorios
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
        
        print("\n=== ESTRUTURA ANTES DA RENOMEACAO ===")
        print_directory_structure(temp_dir)
        
        # Le o conteudo original dos arquivos md5sum.txt para verificar se nao foram alterados
        md5sum_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower() == 'md5sum.txt':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                    md5sum_files.append((file_path, content))
        
        print(f"\nEncontrados {len(md5sum_files)} arquivos md5sum.txt")
        
        # Executa a renomeacao usando a nova funcao
        renamer = FileRenamer(temp_dir)
        
        old_name = "0000125"
        new_name = "0005654"
        
        print(f"\n=== EXECUTANDO RENOMEACAO RECURSIVA: {old_name} -> {new_name} ===")
        
        # Aplica renomeacao recursiva apenas de diretorios
        success = renamer.rename_directories_recursively(l05654_dir, old_name, new_name)
        print(f"Resultado: {'SUCESSO' if success else 'FALHA'}")
        
        print("\n=== ESTRUTURA APOS A RENOMEACAO ===")
        print_directory_structure(temp_dir)
        
        # Verifica se todos os diretorios foram renomeados corretamente
        print("\n=== VERIFICACAO DE DIRETORIOS ===")
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
            print(f"{'EXISTE' if exists else 'FALTA'} Diretorio: {relative_path}")
            if not exists:
                directories_correct = False
        
        # Verifica se diretorios antigos nao existem mais
        old_directories = [
            os.path.join(l05654_dir, "0000125"),
        ]
        
        for old_dir in old_directories:
            if os.path.exists(old_dir):
                relative_path = os.path.relpath(old_dir, temp_dir)
                print(f"ERRO: Diretorio antigo ainda existe: {relative_path}")
                directories_correct = False
        
        # Verifica se arquivos md5sum.txt mantiveram conteudo original
        print("\n=== VERIFICACAO DE ARQUIVOS MD5SUM ===")
        md5sum_preserved = True
        
        current_md5sum_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower() == 'md5sum.txt':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                    current_md5sum_files.append((file_path, content))
        
        # Verifica se o conteudo dos arquivos md5sum.txt foi preservado
        for current_path, current_content in current_md5sum_files:
            # Procura por conteudo correspondente nos arquivos originais
            content_found = False
            for orig_path, orig_content in md5sum_files:
                if current_content == orig_content:
                    content_found = True
                    relative_path = os.path.relpath(current_path, temp_dir)
                    print(f"OK md5sum.txt preservado: {relative_path}")
                    break
            
            if not content_found:
                relative_path = os.path.relpath(current_path, temp_dir)
                print(f"ERRO md5sum.txt alterado: {relative_path}")
                print(f"  Conteudo atual: {current_content}")
                md5sum_preserved = False
        
        # Resultado final
        if directories_correct and md5sum_preserved:
            print("\nTESTE PASSOU! Diretorios renomeados recursivamente, arquivos preservados.")
            return True
        else:
            print("\nTESTE FALHOU!")
            if not directories_correct:
                print("   - Diretorios nao foram renomeados corretamente")
            if not md5sum_preserved:
                print("   - Arquivos md5sum.txt foram alterados")
            return False

def print_directory_structure(root_dir, level=0):
    """Imprime a estrutura de diretorios de forma hierarquica"""
    if level > 5:  # Evita recursao muito profunda
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
            print(f"{indent}DIR {item_name}/")
            if extra_info:
                print_directory_structure(extra_info, level + 1)
        else:
            print(f"{indent}FILE {item_name}")

if __name__ == "__main__":
    test_recursive_directory_rename()