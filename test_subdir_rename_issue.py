import os
import tempfile
import shutil
from file_renamer import FileRenamer

def test_subdir_rename_issue():
    """
    Testa o caso onde o subdiretório não é renomeado:
    L08685/0000125/... -> L08685/0008685/...
    """
    # Cria um diretório temporário para o teste
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Diretório de teste: {temp_dir}")
        
        # Cria a estrutura de diretórios
        l08685_dir = os.path.join(temp_dir, "L08685")
        subdir_0000125 = os.path.join(l08685_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria os arquivos conforme o caso reportado
        files_to_create = [
            (os.path.join(subdir_0000125, "cd0010000125.txt"), "Content with 0000125"),
            (os.path.join(aits_dir, "cd0010000125.txt"), "AITs content with 0000125")
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Criado: {file_path}")
        
        print("\n=== ESTRUTURA ANTES DA RENOMEAÇÃO ===")
        print_directory_structure(temp_dir)
        
        # Executa a renomeação
        renamer = FileRenamer(temp_dir)
        
        # Simula o caso: de L08685 (com subdir 0000125) para L08685 (com número 0008685)
        old_name = "L08685"  # Mesmo nome do diretório
        new_name = "L08685"  # Mantém o mesmo nome, mas deveria renomear subdir de 0000125 para 0008685
        
        print(f"\n=== SIMULANDO CENÁRIO: Renomeando subdiretório de 0000125 para 0008685 ===")
        
        # Para simular o cenário real, vamos chamar diretamente a função de renomeação interna
        # passando o old_name como "0000125" e new_name como "0008685"
        internal_old = "0000125"
        internal_new = "0008685"
        
        print(f"Renomeando estrutura interna de {internal_old} para {internal_new}")
        success = renamer.rename_internal_directories_with_aits(l08685_dir, internal_old, internal_new)
        print(f"Resultado rename_internal_directories_with_aits: {success}")
        
        # Renomeia os arquivos também - usando o diretório correto
        print("\n--- Renomeando arquivos ---")
        # Muda o diretório base do renamer para L08685 temporáriamente
        original_dir = renamer.directory
        renamer.directory = l08685_dir
        renamer.rename_files(internal_old, internal_new)
        renamer.directory = original_dir
        
        print("\n=== ESTRUTURA APÓS A RENOMEAÇÃO ===")
        print_directory_structure(temp_dir)
        
        # Verifica se o subdiretório foi renomeado corretamente
        expected_subdir = os.path.join(l08685_dir, "0008685")
        expected_files = [
            os.path.join(expected_subdir, "cd0010008685.txt"),
            os.path.join(expected_subdir, "AITs", "cd0010008685.txt")
        ]
        
        print("\n=== VERIFICAÇÃO ===")
        subdir_renamed = os.path.exists(expected_subdir)
        old_subdir_exists = os.path.exists(os.path.join(l08685_dir, "0000125"))
        
        print(f"Subdiretório 0008685 existe: {'✓' if subdir_renamed else '✗'}")
        print(f"Subdiretório antigo 0000125 ainda existe: {'✗' if not old_subdir_exists else '✓'}")
        
        all_files_renamed = True
        for expected_file in expected_files:
            exists = os.path.exists(expected_file)
            print(f"{'✓' if exists else '✗'} {expected_file}")
            if not exists:
                all_files_renamed = False
        
        if subdir_renamed and not old_subdir_exists and all_files_renamed:
            print("\n🎉 SUCESSO: Subdiretório e arquivos renomeados corretamente!")
            return True
        else:
            print("\n❌ FALHA: Subdiretório não foi renomeado corretamente.")
            return False

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
    test_subdir_rename_issue()