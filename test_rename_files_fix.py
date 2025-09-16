import os
import tempfile
from file_renamer import FileRenamer

def test_rename_files_path_fix():
    """
    Testa se rename_files agora processa arquivos nos caminhos corretos
    após a correção de renomeação de subdiretórios
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Testando correção de caminhos em rename_files: {temp_dir}")
        
        # Simula a estrutura exata do problema
        l08685_dir = os.path.join(temp_dir, "L08685")
        subdir_0000125 = os.path.join(l08685_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria os arquivos como no caso real
        files_to_create = [
            (os.path.join(l08685_dir, "L08685.txt"), "Dados do lote L08685"),
            (os.path.join(aits_dir, "L00125.txt"), "L00125 dados"),  # Este arquivo causa o problema
            (os.path.join(aits_dir, "md5sum.txt"), "hash456;0000125;hash_aits"),
            (os.path.join(aits_dir, "0000125000001a.jpg"), "fake jpg"),
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
        
        print("\\n=== ESTRUTURA INICIAL (problema) ===")
        print("L08685/0000125/AITs/L00125.txt  ← Caminho incorreto")
        print_structure(l08685_dir, "L08685")
        
        # Simula o FileRenamer como na GUI
        renamer = FileRenamer(temp_dir)
        
        print("\\n=== TESTE 1: Chama rename_directory primeiro ===")
        success = renamer.rename_directory("L08685", "L08685")
        print(f"rename_directory resultado: {success}")
        
        print("\\n=== ESTRUTURA APÓS rename_directory ===")
        print_structure(l08685_dir, "L08685")
        
        # Verifica se subdiretório foi renomeado
        expected_subdir = os.path.join(l08685_dir, "0008685")
        old_subdir = os.path.join(l08685_dir, "0000125")
        
        subdir_renamed = os.path.exists(expected_subdir)
        old_subdir_gone = not os.path.exists(old_subdir)
        
        print(f"\\nSubdiretório 0008685 existe: {'SIM' if subdir_renamed else 'NÃO'}")
        print(f"Subdiretório antigo 0000125 removido: {'SIM' if old_subdir_gone else 'NÃO'}")
        
        if not subdir_renamed:
            print("\\n❌ PROBLEMA: rename_directory não funcionou!")
            return False
        
        print("\\n=== TESTE 2: Chama rename_files ===")
        print("Verificando se rename_files encontra arquivos no caminho correto...")
        
        # Antes de chamar rename_files, verifica onde estão os arquivos
        l00125_old_path = os.path.join(old_subdir, "AITs", "L00125.txt")
        l00125_new_path = os.path.join(expected_subdir, "AITs", "L00125.txt")
        
        print(f"\\nArquivo no caminho antigo: {'SIM' if os.path.exists(l00125_old_path) else 'NÃO'}")
        print(f"Arquivo no caminho novo: {'SIM' if os.path.exists(l00125_new_path) else 'NÃO'}")
        
        # Chama rename_files
        renamer.rename_files("L08685", "L08685")
        
        print("\\n=== ESTRUTURA APÓS rename_files ===")
        print_structure(l08685_dir, "L08685")
        
        # Verifica se arquivo foi renomeado no caminho correto
        expected_renamed_file = os.path.join(expected_subdir, "AITs", "L08685.txt")
        file_renamed_correctly = os.path.exists(expected_renamed_file)
        
        print(f"\\nArquivo L08685.txt no caminho correto: {'SIM' if file_renamed_correctly else 'NÃO'}")
        
        if file_renamed_correctly:
            print("\\n✅ CORREÇÃO FUNCIONOU!")
            print("Agora o log mostrará:")
            print("   Renomeando arquivo: .../L08685/0008685/AITs/L00125.txt -> .../L08685/0008685/AITs/L08685.txt")
            return True
        else:
            print("\\n❌ PROBLEMA PERSISTE!")
            print("rename_files ainda está processando arquivos no caminho antigo")
            
            # Diagnóstico adicional
            print("\\n=== DIAGNÓSTICO ===")
            all_txt_files = []
            for root, dirs, files in os.walk(l08685_dir):
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        all_txt_files.append(file_path)
            
            print("Todos os arquivos .txt encontrados:")
            for txt_file in all_txt_files:
                rel_path = os.path.relpath(txt_file, temp_dir)
                print(f"  {rel_path}")
            
            return False

def print_structure(root_dir, label):
    """Imprime estrutura de forma simples"""
    try:
        for root, dirs, files in os.walk(root_dir):
            level = root.replace(root_dir, '').count(os.sep)
            indent = '  ' * level
            folder_name = os.path.basename(root) if level > 0 else label
            print(f"{indent}{folder_name}/")
            sub_indent = '  ' * (level + 1)
            for file in files:
                print(f"{sub_indent}{file}")
    except Exception as e:
        print(f"Erro ao imprimir estrutura: {e}")

if __name__ == "__main__":
    test_rename_files_path_fix()