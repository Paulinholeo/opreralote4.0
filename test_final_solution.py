import os
import tempfile
from file_renamer import FileRenamer

def test_real_case_solution():
    """
    Demonstra a solução para o caso real reportado:
    L08685/0000125/... -> L08685/0008685/...
    Onde apenas o subdiretório e arquivos precisam ser renomeados
    """
    # Cria um diretório temporário para simular o caso real
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Simulando caso real em: {temp_dir}")
        
        # Cria a estrutura conforme o caso real
        l08685_dir = os.path.join(temp_dir, "L08685")
        subdir_0000125 = os.path.join(l08685_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria os arquivos exatamente como no caso reportado
        files_to_create = [
            (os.path.join(subdir_0000125, "cd0010000125.txt"), "Content 0000125"),
            (os.path.join(aits_dir, "cd0010000125.txt"), "AITs content 0000125")
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
        
        print("\n=== ANTES DA CORREÇÃO ===")
        print_structure(temp_dir)
        
        # Aplica a correção usando a nova função
        renamer = FileRenamer(temp_dir)
        
        print("\n=== APLICANDO CORREÇÃO ===")
        print("Renomeando subdiretório 0000125 para 0008685...")
        
        # Usa a nova função que resolve o problema completo
        success = renamer.rename_subdirectory_and_files(l08685_dir, "0000125", "0008685")
        
        print(f"Resultado: {'✓ SUCESSO' if success else '✗ FALHA'}")
        
        print("\n=== APÓS A CORREÇÃO ===")
        print_structure(temp_dir)
        
        # Verifica o resultado
        expected_files = [
            os.path.join(l08685_dir, "0008685", "cd0010008685.txt"),
            os.path.join(l08685_dir, "0008685", "AITs", "cd0010008685.txt")
        ]
        
        print("\n=== VERIFICAÇÃO FINAL ===")
        all_correct = True
        
        # Verifica se o subdiretório antigo não existe mais
        old_subdir = os.path.join(l08685_dir, "0000125")
        old_exists = os.path.exists(old_subdir)
        print(f"Subdiretório antigo (0000125) removido: {'✓' if not old_exists else '✗'}")
        if old_exists:
            all_correct = False
        
        # Verifica se o novo subdiretório existe
        new_subdir = os.path.join(l08685_dir, "0008685")
        new_exists = os.path.exists(new_subdir)
        print(f"Novo subdiretório (0008685) criado: {'✓' if new_exists else '✗'}")
        if not new_exists:
            all_correct = False
        
        # Verifica se todos os arquivos foram renomeados
        for expected_file in expected_files:
            exists = os.path.exists(expected_file)
            file_name = os.path.basename(expected_file)
            dir_name = os.path.basename(os.path.dirname(expected_file))
            print(f"Arquivo {file_name} em {dir_name}: {'✓' if exists else '✗'}")
            if not exists:
                all_correct = False
        
        if all_correct:
            print(f"\n🎉 PROBLEMA RESOLVIDO! ")
            print("📋 Para usar no seu caso:")
            print("   renamer = FileRenamer('/caminho/para/diretorio/pai')")
            print("   renamer.rename_subdirectory_and_files('/caminho/para/L08685', '0000125', '0008685')")
        else:
            print(f"\n❌ Ainda há problemas na implementação.")

def print_structure(root_dir, level=0):
    """Imprime a estrutura hierárquica"""
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
            print_structure(extra_info, level + 1)
        else:
            print(f"{indent}📄 {item_name}")

if __name__ == "__main__":
    test_real_case_solution()