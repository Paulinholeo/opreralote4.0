import os
import tempfile
from file_renamer import FileRenamer

def test_urgent_fix_l08987():
    """
    Teste para verificar a correção urgente do problema L08987
    onde arquivos eram processados no caminho antigo 0000125
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Teste da correção urgente em: {temp_dir}")
        
        # Simula exatamente a estrutura problemática: L08987/0000125/AITs/
        l08987_dir = os.path.join(temp_dir, "L08987")
        subdir_0000125 = os.path.join(l08987_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria os arquivos como no caso real
        files_to_create = [
            (os.path.join(l08987_dir, "L08987.txt"), "Dados do lote L08987"),
            (os.path.join(aits_dir, "L00125.txt"), "L00125 dados"),
            (os.path.join(aits_dir, "0000125000001a.jpg"), "fake jpg"),
            (os.path.join(aits_dir, "0000125000001b.jpg"), "fake jpg"),
            (os.path.join(aits_dir, "md5sum.txt"), "hash123;0000125;original"),
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
        
        print("\n=== ANTES DA CORREÇÃO ===")
        print("❌ PROBLEMA: Arquivos estão em L08987/0000125/AITs/")
        print_structure(l08987_dir)
        
        # Aplica o FileRenamer
        renamer = FileRenamer(temp_dir)
        
        print("\n=== APLICANDO CORREÇÃO ===")
        print("📝 Simulando chamada: rename_files('L08987', 'L08987')")
        
        # Esta chamada deve FORÇAR a correção do subdiretório ANTES de processar arquivos
        renamer.rename_files("L08987", "L08987")
        
        print("\n=== APÓS A CORREÇÃO ===")
        print("✅ ESPERADO: Arquivos agora em L08987/0008987/AITs/")
        print_structure(l08987_dir)
        
        # Verificação crítica
        old_path = os.path.join(l08987_dir, "0000125")
        new_path = os.path.join(l08987_dir, "0008987")
        
        old_exists = os.path.exists(old_path)
        new_exists = os.path.exists(new_path)
        
        print("\n=== VERIFICAÇÃO FINAL ===")
        print(f"Subdiretório antigo (0000125) ainda existe: {'❌ SIM' if old_exists else '✅ NÃO'}")
        print(f"Novo subdiretório (0008987) criado: {'✅ SIM' if new_exists else '❌ NÃO'}")
        
        # Verifica se arquivos estão no lugar correto
        expected_files = [
            os.path.join(new_path, "AITs", "L08987.txt"),  # L00125.txt renomeado
            os.path.join(new_path, "AITs", "0008987000001a.jpg"),  # jpg renomeado
            os.path.join(new_path, "AITs", "md5sum.txt"),  # md5sum preservado
        ]
        
        files_ok = True
        for expected_file in expected_files:
            exists = os.path.exists(expected_file)
            file_name = os.path.basename(expected_file)
            print(f"Arquivo {file_name}: {'✅' if exists else '❌'}")
            if not exists:
                files_ok = False
        
        success = not old_exists and new_exists and files_ok
        
        if success:
            print("\n🎉 CORREÇÃO BEM-SUCEDIDA!")
            print("📋 Agora o log mostrará:")
            print("   Renomeando arquivo: .../L08987/0008987/AITs/L00125.txt -> .../L08987/0008987/AITs/L08987.txt")
            print("\n🔧 Para aplicar no sistema real:")
            print("   1. Feche a aplicação OperaLote")
            print("   2. Reinicie a aplicação") 
            print("   3. Execute uma renomeação")
        else:
            print("\n❌ CORREÇÃO FALHOU - precisa de mais ajustes")
            
        return success

def print_structure(root_dir):
    """Imprime a estrutura de forma simples"""
    try:
        for root, dirs, files in os.walk(root_dir):
            level = root.replace(root_dir, '').count(os.sep)
            indent = '  ' * level
            folder_name = os.path.basename(root) if level > 0 else os.path.basename(root_dir)
            print(f"{indent}📁 {folder_name}/")
            sub_indent = '  ' * (level + 1)
            for file in files:
                print(f"{sub_indent}📄 {file}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_urgent_fix_l08987()