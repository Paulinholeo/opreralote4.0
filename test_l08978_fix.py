import os
import tempfile
from file_renamer import FileRenamer

def test_l08978_case():
    """
    Testa o caso específico L08978 onde subdiretório 0000125 não estava sendo renomeado
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Testando caso L08978 em: {temp_dir}")
        
        # Simula a estrutura D:/Brascontrol/Opera_lote_4.0/L08978/
        base_dir = os.path.join(temp_dir, "Opera_lote_4.0")
        l08978_dir = os.path.join(base_dir, "L08978")
        subdir_0000125 = os.path.join(l08978_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria arquivos como no caso real
        files_to_create = [
            (os.path.join(l08978_dir, "L08978.txt"), "Dados do lote L08978"),
            (os.path.join(subdir_0000125, "data.txt"), "Dados 0000125"), 
            (os.path.join(subdir_0000125, "md5sum.txt"), "hash123;0000125;hash_original"),
            (os.path.join(aits_dir, "L00125.txt"), "L00125 dados"),  # Este arquivo está sendo renomeado
            (os.path.join(aits_dir, "md5sum.txt"), "hash456;0000125;hash_aits"),
            (os.path.join(aits_dir, "0000125000001a.jpg"), "fake jpg"),
            (os.path.join(aits_dir, "0000125000001b.jpg"), "fake jpg"),
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
        
        print("\\n=== ESTRUTURA ANTES (como estava acontecendo) ===")
        print("L08978/0000125/AITs/L00125.txt  ← Problema: subdiretório não renomeado")
        print_structure(l08978_dir, "L08978")
        
        # Simula a renomeação usando FileRenamer
        renamer = FileRenamer(base_dir)
        
        print("\\n=== EXECUTANDO RENOMEAÇÃO L08978 (0000125 -> 0008978) ===")
        
        # Primeiro renomeia o diretório (isso chama rename_directory)
        success = renamer.rename_directory("L08978", "L08978")  # Mesmo nome para focar no subdiretório
        print(f"Resultado rename_directory: {success}")
        
        # Agora simula o que deveria acontecer: renomear subdiretório de 0000125 para 0008978
        print("\\nRenomeando subdiretório interno de 0000125 para 0008978...")
        renamer.rename_directories_recursively(l08978_dir, "0000125", "0008978")
        
        print("\\n=== ESTRUTURA DEPOIS (como deveria ficar) ===")
        print("L08978/0008978/AITs/L00125.txt  ← Correção: subdiretório renomeado")
        print_structure(l08978_dir, "L08978")
        
        # Verifica se a correção funcionou
        print("\\n=== VERIFICAÇÃO ===")
        
        # Verifica se novo subdiretório existe
        new_subdir = os.path.join(l08978_dir, "0008978")
        new_aits = os.path.join(new_subdir, "AITs")
        
        print(f"Subdiretório 0008978 criado: {'SIM' if os.path.exists(new_subdir) else 'NÃO'}")
        print(f"Subdiretório 0008978/AITs existe: {'SIM' if os.path.exists(new_aits) else 'NÃO'}")
        
        # Verifica se subdiretório antigo foi removido
        old_subdir = os.path.join(l08978_dir, "0000125")
        print(f"Subdiretório antigo 0000125 removido: {'SIM' if not os.path.exists(old_subdir) else 'NÃO'}")
        
        # Verifica se arquivo L00125.txt está no local correto
        expected_file = os.path.join(new_aits, "L00125.txt")
        print(f"Arquivo L00125.txt no local correto: {'SIM' if os.path.exists(expected_file) else 'NÃO'}")
        
        # Verifica se md5sum.txt foi preservado
        md5sum_file = os.path.join(new_aits, "md5sum.txt")
        if os.path.exists(md5sum_file):
            with open(md5sum_file, 'r') as f:
                content = f.read()
            print(f"Arquivo md5sum.txt preservado: {'SIM' if 'hash456;0000125;hash_aits' in content else 'NÃO'}")
        
        # Resultado
        all_correct = (os.path.exists(new_subdir) and 
                      os.path.exists(new_aits) and 
                      not os.path.exists(old_subdir) and 
                      os.path.exists(expected_file))
        
        if all_correct:
            print("\\n🎉 CORREÇÃO FUNCIONOU!")
            print("✅ Subdiretório 0000125 renomeado para 0008978")
            print("✅ Estrutura AITs preservada")
            print("✅ Arquivos movidos para local correto")
            print("\\n📋 Agora os arquivos serão processados no caminho correto:")
            print("   L08978/0008978/AITs/L00125.txt")
            return True
        else:
            print("\\n❌ Ainda há problemas na renomeação de subdiretórios")
            return False

def print_structure(root_dir, label):
    """Imprime estrutura de forma simples"""
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = '  ' * level
        folder_name = os.path.basename(root) if level > 0 else label
        print(f"{indent}{folder_name}/")
        sub_indent = '  ' * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")

if __name__ == "__main__":
    test_l08978_case()