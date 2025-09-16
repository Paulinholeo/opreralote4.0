import os
import tempfile
from file_renamer import FileRenamer

def test_l08685_real_case():
    """
    Reproduz exatamente o caso L08685 que não está funcionando na prática
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Testando caso real L08685 em: {temp_dir}")
        
        # Simula D:/Brascontrol/Opera_lote_4.0/L08685/
        l08685_dir = os.path.join(temp_dir, "L08685")
        subdir_0000125 = os.path.join(l08685_dir, "0000125")
        aits_dir = os.path.join(subdir_0000125, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria arquivos conforme o caso real
        files_to_create = [
            (os.path.join(l08685_dir, "L08685.txt"), "Dados do lote L08685"),
            (os.path.join(subdir_0000125, "data.txt"), "Dados 0000125"), 
            (os.path.join(subdir_0000125, "md5sum.txt"), "hash123;0000125;hash_original"),
            (os.path.join(aits_dir, "L00125.txt"), "L00125 dados"),
            (os.path.join(aits_dir, "L08685.txt"), "L08685 dados no AITs"),  # Arquivo que está sendo processado
            (os.path.join(aits_dir, "md5sum.txt"), "hash456;0000125;hash_aits"),
            (os.path.join(aits_dir, "0000125000001a.jpg"), "fake jpg"),
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
        
        print("\\n=== PROBLEMA ATUAL (como você está vendo) ===")
        print("Arquivo processado: D:/.../L08685/0000125/AITs/L08685.txt")
        print("Deveria ser:       D:/.../L08685/0008685/AITs/L08685.txt")
        print_structure(l08685_dir, "L08685")
        
        # Simula o FileRenamer exatamente como na GUI
        renamer = FileRenamer(temp_dir)
        
        print("\\n=== DIAGNÓSTICO DETALHADO ===")
        
        # Vamos testar diferentes cenários possíveis
        scenarios = [
            ("L08685", "L08685"),  # Mesmo nome (deve ativar lógica especial)
            ("L08685", "L08685"),  # Repetindo para confirmar
        ]
        
        for old_name, new_name in scenarios:
            print(f"\\nTeste: rename_directory('{old_name}', '{new_name}')")
            
            # Verifica estado antes
            before_0000125 = os.path.exists(os.path.join(l08685_dir, "0000125"))
            before_0008685 = os.path.exists(os.path.join(l08685_dir, "0008685"))
            print(f"  Antes: 0000125={before_0000125}, 0008685={before_0008685}")
            
            # Executa rename_directory
            result = renamer.rename_directory(old_name, new_name)
            print(f"  Resultado: {result}")
            
            # Verifica estado depois
            after_0000125 = os.path.exists(os.path.join(l08685_dir, "0000125"))
            after_0008685 = os.path.exists(os.path.join(l08685_dir, "0008685"))
            print(f"  Depois: 0000125={after_0000125}, 0008685={after_0008685}")
            
            if after_0008685 and not after_0000125:
                print("  ✅ FUNCIONOU! Subdiretório renomeado")
                break
            elif after_0000125:
                print("  ❌ FALHOU! Subdiretório não foi renomeado")
                
                # Vamos tentar diagnosticar por que falhou
                print("\\n  === DIAGNÓSTICO ADICIONAL ===")
                items = os.listdir(l08685_dir)
                print(f"  Itens em L08685: {items}")
                
                for item in items:
                    item_path = os.path.join(l08685_dir, item)
                    if os.path.isdir(item_path):
                        print(f"  Diretório encontrado: {item}")
                        print(f"    É numérico: {item.isdigit()}")
                        print(f"    Tem 6+ caracteres: {len(item) >= 6}")
                        
                        if item.isdigit() and len(item) >= 6:
                            expected = "08685".zfill(7)  # "0008685"
                            print(f"    Deveria ser: {expected}")
                            print(f"    É diferente: {item != expected}")
            else:
                print("  ⚠️ Estado inesperado")
        
        print("\\n=== ESTRUTURA FINAL ===")
        print_structure(l08685_dir, "L08685")
        
        # Verifica se funcionou
        final_check = os.path.exists(os.path.join(l08685_dir, "0008685"))
        if final_check:
            print("\\n✅ PROBLEMA RESOLVIDO!")
            print("Agora o arquivo será processado em:")
            print("D:/.../L08685/0008685/AITs/L08685.txt")
        else:
            print("\\n❌ PROBLEMA PERSISTE!")
            print("Precisa investigar mais a fundo...")
            
            # Vamos tentar forçar a renomeação manualmente
            print("\\n=== TENTATIVA DE CORREÇÃO MANUAL ===")
            old_path = os.path.join(l08685_dir, "0000125")
            new_path = os.path.join(l08685_dir, "0008685")
            
            if os.path.exists(old_path):
                try:
                    os.rename(old_path, new_path)
                    print("✅ Renomeação manual funcionou!")
                    print_structure(l08685_dir, "L08685")
                except Exception as e:
                    print(f"❌ Renomeação manual falhou: {e}")
        
        return final_check

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
    test_l08685_real_case()