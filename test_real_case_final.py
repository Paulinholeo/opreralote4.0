import os
import tempfile
from file_renamer import FileRenamer

def test_real_case_example():
    """
    Simula o caso real: renomear estrutura de L05654 com subdiretorio 0000125 para 0005654
    Antes: D:/.../L05654/0000125/AITs/md5sum.txt
    Depois: D:/.../L05654/0005654/AITs/md5sum.txt
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Simulando caso real em: {temp_dir}")
        
        # Simula a estrutura D:/Brascontrol/Opera_lote_4.0/L05654/
        base_dir = os.path.join(temp_dir, "Opera_lote_4.0")
        l05654_dir = os.path.join(base_dir, "L05654")
        subdir_0000125 = os.path.join(l05654_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria arquivos como no caso real
        files_to_create = [
            (os.path.join(l05654_dir, "L05654.txt"), "Dados do lote L05654"),
            (os.path.join(subdir_0000125, "data.txt"), "Dados 0000125"), 
            (os.path.join(subdir_0000125, "md5sum.txt"), "abc123;0000125;hash_original"),
            (os.path.join(aits_dir, "md5sum.txt"), "def456;0000125;hash_aits"),
            (os.path.join(aits_dir, "L00125.txt"), "L00125 dados"),
            (os.path.join(aits_dir, "0000125000001a.jpg"), "fake jpg"),
            (os.path.join(aits_dir, "0000125000001b.jpg"), "fake jpg"),
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
        
        print("\\n=== ESTRUTURA ANTES (como no caso real) ===")
        print(f"D:/Brascontrol/Opera_lote_4.0/L05654/0000125/AITs/md5sum.txt")
        print_structure(l05654_dir, "L05654")
        
        # Le conteudo dos md5sum.txt para verificar preservacao
        md5sum_original = {}
        for root, dirs, files in os.walk(l05654_dir):
            for file in files:
                if file.lower() == 'md5sum.txt':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        md5sum_original[file_path] = f.read()
        
        print(f"\\nArquivos md5sum.txt encontrados: {len(md5sum_original)}")
        for path, content in md5sum_original.items():
            rel_path = os.path.relpath(path, l05654_dir)
            print(f"  {rel_path}: {content}")
        
        # Aplica a correcao usando o FileRenamer
        renamer = FileRenamer(base_dir)
        
        print("\\n=== APLICANDO CORRECAO ===")
        print("Executando: rename_internal_directories_with_aits(L05654, '0000125', '0005654')")
        
        # Simula o que acontece quando usuario renomeia de L05654 com 0000125 para L05654 com 0005654
        success = renamer.rename_internal_directories_with_aits(l05654_dir, "0000125", "0005654")
        
        print(f"Resultado: {'SUCESSO' if success else 'FALHA'}")
        
        print("\\n=== ESTRUTURA DEPOIS (corrigida) ===")
        print(f"D:/Brascontrol/Opera_lote_4.0/L05654/0005654/AITs/md5sum.txt")
        print_structure(l05654_dir, "L05654")
        
        # Verifica se diretorios foram renomeados
        print("\\n=== VERIFICACAO FINAL ===")
        
        # Verifica se novo diretorio existe
        new_subdir = os.path.join(l05654_dir, "0005654")
        new_aits = os.path.join(new_subdir, "AITs")
        
        success_rename = os.path.exists(new_subdir) and os.path.exists(new_aits)
        print(f"Diretorio 0005654 criado: {'SIM' if os.path.exists(new_subdir) else 'NAO'}")
        print(f"Diretorio 0005654/AITs existe: {'SIM' if os.path.exists(new_aits) else 'NAO'}")
        
        # Verifica se diretorio antigo foi removido
        old_subdir = os.path.join(l05654_dir, "0000125")
        old_removed = not os.path.exists(old_subdir)
        print(f"Diretorio antigo 0000125 removido: {'SIM' if old_removed else 'NAO'}")
        
        # Verifica se md5sum.txt foi preservado
        md5sum_preserved = True
        new_md5sum_files = []
        
        for root, dirs, files in os.walk(l05654_dir):
            for file in files:
                if file.lower() == 'md5sum.txt':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                    new_md5sum_files.append((file_path, content))
        
        print(f"\\nArquivos md5sum.txt apos renomeacao: {len(new_md5sum_files)}")
        
        for new_path, new_content in new_md5sum_files:
            rel_path = os.path.relpath(new_path, l05654_dir)
            # Verifica se conteudo foi preservado
            content_preserved = new_content in md5sum_original.values()
            print(f"  {rel_path}: {'PRESERVADO' if content_preserved else 'ALTERADO'}")
            print(f"    Conteudo: {new_content}")
            if not content_preserved:
                md5sum_preserved = False
        
        # Resultado final
        if success_rename and old_removed and md5sum_preserved:
            print("\\n🎉 SOLUCAO FUNCIONANDO!")
            print("✅ Diretorios renomeados corretamente")
            print("✅ Diretorio antigo removido") 
            print("✅ Arquivos md5sum.txt preservados")
            print("\\n📋 PRONTO PARA USO NO SISTEMA REAL!")
            return True
        else:
            print("\\n❌ Ainda ha problemas:")
            if not success_rename:
                print("  - Diretorios nao foram renomeados")
            if not old_removed:
                print("  - Diretorio antigo nao foi removido")
            if not md5sum_preserved:
                print("  - Arquivos md5sum.txt foram alterados")
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
    test_real_case_example()