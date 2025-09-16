import os
import tempfile
from file_renamer import FileRenamer

def test_gui_flow_simulation():
    """
    Simula exatamente o fluxo da GUI para o caso L08786
    onde subdiretório 0000125 não estava sendo renomeado antes do processamento
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Simulando fluxo GUI para L08786 em: {temp_dir}")
        
        # Simula estrutura como D:/Brascontrol/Opera_lote_4.0/
        l08786_dir = os.path.join(temp_dir, "L08786")
        subdir_0000125 = os.path.join(l08786_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria arquivos conforme o caso real
        files_to_create = [
            (os.path.join(l08786_dir, "L08786.txt"), "Dados do lote L08786"),
            (os.path.join(subdir_0000125, "data.txt"), "Dados 0000125"), 
            (os.path.join(subdir_0000125, "md5sum.txt"), "hash123;0000125;hash_original"),
            (os.path.join(aits_dir, "L00125.txt"), "L00125 dados"),
            (os.path.join(aits_dir, "md5sum.txt"), "hash456;0000125;hash_aits"),
            (os.path.join(aits_dir, "0000125000001a.jpg"), "fake jpg"),
            (os.path.join(aits_dir, "0000125000001b.jpg"), "fake jpg"),
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
        
        print("\\n=== ESTRUTURA ANTES (problema atual) ===")
        print("L08786/0000125/AITs/L00125.txt  ← Subdiretório não renomeado")
        print_structure(l08786_dir, "L08786")
        
        # Simula o FileRenamer como na GUI
        renamer = FileRenamer(temp_dir)
        
        print("\\n=== EXECUTANDO FLUXO DA GUI ===")
        print("1. Chamando rename_directory('L08786', 'L08786')...")
        
        # Passo 1: rename_directory (como na GUI linha 124)
        success = renamer.rename_directory("L08786", "L08786")
        print(f"   Resultado: {'SUCESSO' if success else 'FALHA'}")
        
        print("\\n=== ESTRUTURA APÓS rename_directory ===")
        print("L08786/0008786/AITs/L00125.txt  ← Deveria estar assim agora")
        print_structure(l08786_dir, "L08786")
        
        # Verifica se subdiretório foi renomeado ANTES do processamento de arquivos
        expected_subdir = os.path.join(l08786_dir, "0008786")  # Esperamos 0008786 baseado no padrão
        old_subdir = os.path.join(l08786_dir, "0000125")
        
        print("\\n=== VERIFICAÇÃO CRÍTICA ===")
        subdir_renamed = os.path.exists(expected_subdir)
        old_subdir_removed = not os.path.exists(old_subdir)
        
        print(f"Subdiretório 0008786 existe: {'SIM' if subdir_renamed else 'NÃO'}")
        print(f"Subdiretório antigo 0000125 removido: {'SIM' if old_subdir_removed else 'NÃO'}")
        
        if subdir_renamed and old_subdir_removed:
            print("✅ PROBLEMA RESOLVIDO! Subdiretório renomeado ANTES do processamento")
            
            # Agora simula os próximos passos da GUI
            print("\\n2. Chamando rename_files('L08786', 'L08786')...")
            renamer.rename_files("L08786", "L08786")
            
            print("3. Chamando rename_text_content('L08786', 'L08786')...")
            renamer.rename_text_content("L08786", "L08786")
            
            print("\\n=== ESTRUTURA FINAL ===")
            print_structure(l08786_dir, "L08786")
            
            # Verifica se arquivos estão nos caminhos corretos
            expected_files = [
                os.path.join(l08786_dir, "0008786", "AITs", "L08786.txt"),  # L00125.txt renomeado
                os.path.join(l08786_dir, "0008786", "AITs", "md5sum.txt"),  # md5sum preservado
                os.path.join(l08786_dir, "0008786", "AITs", "0008786000001a.jpg"),  # jpg renomeado
            ]
            
            files_correct = True
            for expected_file in expected_files:
                exists = os.path.exists(expected_file)
                rel_path = os.path.relpath(expected_file, temp_dir)
                print(f"{'✅' if exists else '❌'} {rel_path}")
                if not exists:
                    files_correct = False
            
            if files_correct:
                print("\\n🎉 FLUXO GUI CORRIGIDO COM SUCESSO!")
                print("Agora o log mostrará:")
                print("   Renomeando arquivo: .../L08786/0008786/AITs/L00125.txt -> .../L08786/0008786/AITs/L08786.txt")
                return True
            else:
                print("\\n⚠️ Subdiretório foi renomeado, mas alguns arquivos ainda têm problemas")
                return False
        else:
            print("\\n❌ PROBLEMA PERSISTE! Subdiretório ainda não foi renomeado corretamente")
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
    test_gui_flow_simulation()